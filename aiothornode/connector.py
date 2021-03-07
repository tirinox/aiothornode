import asyncio
import logging
from random import Random
from typing import List

import ujson
from aiohttp import ClientSession

from .consensus import consensus_response
from .nodeclient import ThorNodeClient
from .types import *
import time


class ThorConnector:
    def __init__(self, env: ThorEnvironment, session: ClientSession, logger=None, rng: Random = None):
        self.session = session
        self.env = env
        self.logger = logger or logging.getLogger('ThorConnector')
        self._clients = []
        self._rng = rng or Random()
        self.client_update_period = 120  # sec
        self._last_client_update = 0.0

    async def _request(self, path: str, clients: List[ThorNodeClient]):
        self.logger.debug(f'Start request to Thor node "{path}"')

        m, n = self.env.consensus_min, self.env.consensus_total
        if len(clients) < n:
            self.logger.warning(f'Too few nodes in the network!')
            m = 0

        clients = clients[:self.env.consensus_total]  # limit requests!
        json_responses = await asyncio.gather(*[client.request(path) for client in clients])
        best_response, ratio = consensus_response(json_responses, consensus_n=m, total_n=n)
        if best_response is None:
            ips = [client.node_ip for client in clients]
            self.logger.error(f'No consensus reached between nodes: {ips} for request "{path}"!')
            return None
        else:
            self.logger.debug(f'Success for the request "{path}" consensus: {(ratio * 100.0):.0f}%')
            if isinstance(best_response, dict) and 'code' in best_response:
                raise ThorException(best_response)
            else:
                return best_response

    async def _load_seed_list(self):
        assert self.session
        self.logger.debug(f'Using seed URL: {self.env.seed_url}')
        async with self.session.get(self.env.seed_url) as resp:
            seed_nodes = await resp.json()
            return seed_nodes

    def _new_client(self, ip_addr):
        return ThorNodeClient(ip_addr, self.session, self.env.timeout, self.logger)

    async def _load_active_nodes(self, seed_ips: List[str]):
        self._rng.shuffle(seed_ips)
        clients = [self._new_client(ip_addr) for ip_addr in seed_ips[:self.env.consensus_total]]
        accounts = await self.query_node_accounts(clients)
        if accounts:
            ip_addresses = [node.ip_address for node in accounts if node.is_good]
            self._clients = [self._new_client(ip_address) for ip_address in ip_addresses]
            self.logger.info(f'Active clients: {len(self._clients)} from {len(accounts)}')
            self._last_client_update = time.monotonic()
        else:
            self.logger.error('No active clients!')

    @property
    def seconds_from_last_node_update(self):
        return time.monotonic() - self._last_client_update

    async def update_nodes(self):
        seeds = await self._load_seed_list()
        await self._load_active_nodes(seeds)

    async def _get_random_clients(self):
        if not self._last_client_update or time.monotonic() - self._last_client_update > self.client_update_period:
            await self.update_nodes()
        if self.env.consensus_total > len(self._clients):
            return self._clients
        else:
            return self._rng.sample(self._clients, self.env.consensus_total)

    # --- METHODS ----

    async def query_custom_path(self, path, clients=None):
        clients = clients or (await self._get_random_clients())
        data = await self._request(path, clients)
        return data

    async def query_node_accounts(self, clients=None) -> List[ThorNodeAccount]:
        clients = clients or (await self._get_random_clients())
        data = await self._request(self.env.path_nodes, clients)
        return [ThorNodeAccount.from_json(j) for j in data] if data else []

    async def query_queue(self, clients=None) -> ThorQueue:
        clients = clients or (await self._get_random_clients())
        data = await self._request(self.env.path_queue, clients)
        return ThorQueue.from_json(data)

    async def query_pools(self, height=None, *, clients=None) -> List[ThorPool]:
        clients = clients or (await self._get_random_clients())
        if height:
            path = self.env.path_pools_height.format(height=height)
        else:
            path = self.env.path_pools
        data = await self._request(path, clients)
        return [ThorPool.from_json(j) for j in data]

    async def query_pool(self, pool: str, height=None, *, clients=None) -> ThorPool:
        clients = clients or (await self._get_random_clients())
        if height:
            path = self.env.path_pool_height.format(pool=pool, height=height)
        else:
            path = self.env.path_pool.format(pool=pool)
        data = await self._request(path, clients)
        return ThorPool.from_json(data)

    async def query_last_blocks(self, clients=None) -> List[ThorLastBlock]:
        clients = clients or (await self._get_random_clients())
        data = await self._request(self.env.path_last_blocks, clients=clients)
        return [ThorLastBlock.from_json(j) for j in data] if isinstance(data, list) else [ThorLastBlock.from_json(data)]

    async def query_constants(self, clients=None) -> ThorConstants:
        clients = clients or (await self._get_random_clients())
        data = await self._request(self.env.path_constants, clients=clients)
        return ThorConstants.from_json(data)

    async def query_mimir(self, clients=None) -> ThorMimir:
        clients = clients or (await self._get_random_clients())
        data = await self._request(self.env.path_mimir, clients=clients)
        return ThorMimir.from_json(data)

# https://gitlab.com/thorchain/thornode/-/blob/master/x/thorchain/query/query.go
# /observe_chains new path
