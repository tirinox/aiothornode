import asyncio
import logging

import ujson
from aiohttp import ClientSession, ClientConnectorError

from aiothornode.env import ThorEnvironment

THORNODE_PORT = 1317
TENDERMINT_RPC_PORT_TESTNET = 26657
TENDERMINT_RPC_PORT_MAINNET = 27147


class ThorNodeClient:
    HEADER_CLIENT_ID = 'x-client-id'

    def connection_url(self, ip_address, path, is_rpc):
        port = self.tendermint_rpc_port if is_rpc else self.thornode_port
        path = '/' + path.lstrip('/')
        return f'http://{ip_address}:{port}{path}'

    def __init__(self, node_ip: str, session: ClientSession, timeout=3.0, logger=None,
                 thornode_port=THORNODE_PORT,
                 tendermint_rpc_port=TENDERMINT_RPC_PORT_MAINNET,
                 extra_headers=None):
        self.session = session
        self.timeout = timeout
        self.node_ip = node_ip
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.tendermint_rpc_port = tendermint_rpc_port
        self.thornode_port = thornode_port
        self.extra_headers = extra_headers

    async def request(self, path, is_rpc=False):
        url = self.connection_url(self.node_ip, path, is_rpc)
        try:
            self.logger.debug(f'Node GET "{url}"')
            async with self.session.get(url, timeout=self.timeout, headers=self.extra_headers) as resp:
                if resp.status == 404:
                    raise FileNotFoundError(f'{url} not found, sorry!')
                text = await resp.text()
                self.logger.debug(f'Node RESPONSE "{url}" code={resp.status}')
                return ujson.loads(text)
        except (ClientConnectorError, asyncio.TimeoutError, ValueError) as e:
            self.logger.warning(f'Cannot connect to THORNode ({self.node_ip}) for "{path}" (err: {e}).')
            return None

    def set_client_id_header(self, client_id: str):
        if not isinstance(self.extra_headers, dict):
            self.extra_headers = {}

        if not client_id:
            del self.extra_headers[self.HEADER_CLIENT_ID]
        else:
            self.extra_headers[self.HEADER_CLIENT_ID] = client_id

    def __repr__(self) -> str:
        return f'ThorNodeClient({self.node_ip!r})'


class ThorNodePublicClient(ThorNodeClient):
    def __init__(self, session: ClientSession, env: ThorEnvironment, logger=None, extra_headers=None):
        port = TENDERMINT_RPC_PORT_TESTNET if env.kind == 'testnet' else TENDERMINT_RPC_PORT_MAINNET
        super().__init__('', session, env.timeout, logger, 0, port, extra_headers=extra_headers)
        self.env = env

    def connection_url(self, ip_address, path, is_rpc):
        if is_rpc:
            return f'{self.env.rpc_url}{path}'
        else:
            return f'{self.env.thornode_url}{path}'

    def __repr__(self) -> str:
        return f"ThorNodePublicClient({self.env.thornode_url})"
