import logging
import urllib.parse
from typing import Dict

from aiohttp import ClientSession

from .env import ThorEnvironment
from .nodeclient import ThorNodePublicClient
from .types import *


class ThorConnector:
    def __init__(self, env: ThorEnvironment, session: ClientSession, logger=None):
        self.session = session
        self.env = env
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self._clients = []
        self.pub_client = ThorNodePublicClient(self.session, logger=self.logger, env=self.env)

    # --- METHODS ----

    async def query_custom_path(self, path):
        data = await self.pub_client.request(path)
        return data

    async def query_node_accounts(self) -> List[ThorNodeAccount]:
        data = await self.pub_client.request(self.env.path_nodes)
        return [ThorNodeAccount.from_json(j) for j in data] if data else []

    async def query_queue(self) -> ThorQueue:
        data = await self.pub_client.request(self.env.path_queue)
        return ThorQueue.from_json(data)

    async def query_pools(self, height=None) -> List[ThorPool]:
        if height:
            path = self.env.path_pools_height.format(height=height)
        else:
            path = self.env.path_pools
        data = await self.pub_client.request(path)
        return [ThorPool.from_json(j) for j in data]

    async def query_pool(self, pool: str, height=None) -> ThorPool:
        if height:
            path = self.env.path_pool_height.format(pool=pool, height=height)
        else:
            path = self.env.path_pool.format(pool=pool)
        data = await self.pub_client.request(path)
        return ThorPool.from_json(data)

    async def query_last_blocks(self) -> List[ThorLastBlock]:
        data = await self.pub_client.request(self.env.path_last_blocks)
        return [ThorLastBlock.from_json(j) for j in data] if isinstance(data, list) else [ThorLastBlock.from_json(data)]

    async def query_constants(self) -> ThorConstants:
        data = await self.pub_client.request(self.env.path_constants)
        return ThorConstants.from_json(data)

    async def query_mimir(self) -> ThorMimir:
        data = await self.pub_client.request(self.env.path_mimir)
        return ThorMimir.from_json(data)

    async def query_chain_info(self) -> Dict[str, ThorChainInfo]:
        data = await self.pub_client.request(self.env.path_inbound_addresses)
        if isinstance(data, list):
            info_list = [ThorChainInfo.from_json(j) for j in data]
        else:
            # noinspection PyUnresolvedReferences
            current = data.get('current', {})  # single-chain
            info_list = [ThorChainInfo.from_json(j) for j in current]
        return {info.chain: info for info in info_list}

    async def query_vault(self, vault_type=ThorVault.TYPE_ASGARD) -> List[ThorVault]:
        path = self.env.path_vault_asgard if vault_type == ThorVault.TYPE_ASGARD else self.env.path_vault_yggdrasil
        data = await self.pub_client.request(path)
        return [ThorVault.from_json(v) for v in data]

    async def query_balance(self, address: str) -> ThorBalances:
        path = self.env.path_balance.format(address=address)
        data = await self.pub_client.request(path)
        return ThorBalances.from_json(data, address)

    async def query_tendermint_block_raw(self, height):
        path = self.env.path_block_by_height.format(height=height)
        data = await self.pub_client.request(path, is_rpc=True)
        return data

    async def query_block(self, height) -> ThorBalances:
        data = await self.query_tendermint_block_raw(height)
        return ThorBlock.from_json(data)

    async def query_native_tx(self, tx_hash: str, before_hard_fork=False):
        tx_hash = str(tx_hash)
        if not tx_hash.startswith('0x') and not tx_hash.startswith('0X'):
            tx_hash = f'0x{tx_hash}'

        path_pattern = self.env.path_tx_by_hash_old if before_hard_fork else self.env.path_tx_by_hash
        path = path_pattern.format(hash=tx_hash)
        data = await self.pub_client.request(path, is_rpc=True)
        return ThorNativeTX.from_json(data)

    async def query_native_tx_search(self,
                                     query: str,
                                     page: int = 1, per_page: int = 50, order_by='"asc"',
                                     prove=True):
        if not query.startswith('"'):
            query = f'"{query}"'
        if not order_by.startswith('"'):
            order_by = f'"{order_by}"'
        query = urllib.parse.quote_plus(query)
        order_by = urllib.parse.quote_plus(order_by)
        path = self.env.path_tx_search.format(
            query=query,
            prove='true' if prove else 'false',
            page=page,
            per_page=per_page,
            order_by=order_by
        )
        data = await self.pub_client.request(path, is_rpc=True)
        return ThorNativeTXSearchResults.from_json(data)

    async def query_genesis(self):
        data = await self.pub_client.request(self.env.path_genesis, is_rpc=True)
        return data['result']['genesis'] if data else None

    async def query_native_status(self):
        data = await self.pub_client.request(self.env.path_status, is_rpc=True)
        return data['result']
