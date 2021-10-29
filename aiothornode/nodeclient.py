import asyncio
import logging

import ujson
from aiohttp import ClientSession, ClientConnectorError

THORNODE_PORT = 1317
TENDERMINT_RPC_PORT_TESTNET = 26657
TENDERMINT_RPC_PORT_MAINNET = 27147

PUBLIC_THORNODE_URL = 'https://thornode.thorchain.info'
PUBLIC_THORNODE_RPC_URL = 'https://rpc.thorchain.info/'


class ThorNodeClient:
    def connection_url(self, ip_address, path, is_rpc):
        port = self.tendermint_rpc_port if is_rpc else self.thornode_port
        path = '/' + path.lstrip('/')
        return f'http://{ip_address}:{port}{path}'

    def __init__(self, node_ip: str, session: ClientSession, timeout=3.0, logger=None,
                 thornode_port=THORNODE_PORT,
                 tendermint_rpc_port=TENDERMINT_RPC_PORT_MAINNET):
        self.session = session
        self.timeout = timeout
        self.node_ip = node_ip
        self.logger = logger or logging.getLogger('ThorNodeClient')
        self.tendermint_rpc_port = tendermint_rpc_port
        self.thornode_port = thornode_port

    async def request(self, path, is_rpc=False):
        url = self.connection_url(self.node_ip, path, is_rpc)
        try:
            self.logger.debug(f'Node GET "{url}"')
            async with self.session.get(url, timeout=self.timeout) as resp:
                text = await resp.text()
                return ujson.loads(text)
        except (ClientConnectorError, asyncio.TimeoutError, ValueError) as e:
            self.logger.warning(f'Cannot connect to THORNode ({self.node_ip}) for "{path}" (err: {e}).')
            return None

    def __repr__(self) -> str:
        return f'ThorNodeClient({self.node_ip!r})'


class ThorNodePublicClient(ThorNodeClient):
    def __init__(self, session: ClientSession, timeout=3.0, logger=None,
                 tendermint_rpc_port=TENDERMINT_RPC_PORT_MAINNET):
        super().__init__('', session, timeout, logger, 0, tendermint_rpc_port)

    def connection_url(self, ip_address, path, is_rpc):
        if is_rpc:
            return f'{PUBLIC_THORNODE_RPC_URL}{path}'
        else:
            return f'{PUBLIC_THORNODE_URL}{path}'
