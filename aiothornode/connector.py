import asyncio
import logging
import time
from operator import itemgetter
from random import Random
from typing import List, Dict

from aiohttp import ClientSession

from .consensus import consensus_response, first_not_null
from .nodeclient import ThorNodeClient
from .types import *


class ThorConnector:
    def __init__(self, env: ThorEnvironment, session: ClientSession, logger=None, rng: Random = None,
                 auto_ban=False):
        self.session = session
        self.env = env
        self.logger = logger or logging.getLogger('ThorConnector')
        self._clients = []
        self._rng = rng or Random()
        self.client_update_period = 120  # sec
        self._last_client_update = 0.0
        self.use_all_nodes_when_updating = True
        self.auto_ban = auto_ban
        self.ban_list = set()

    @property
    def active_ip_addresses(self):
        return [c.node_ip for c in self._clients]

    async def _request(self, path: str, clients: List[ThorNodeClient], consensus=True, post_processor=None,
                       is_rpc=False):
        self.logger.debug(f'Start request to Thor node "{path}"')

        m, n = self.env.consensus_min, self.env.consensus_total
        if len(clients) < n:
            self.logger.warning(f'Too few nodes in the network!')
            m = 0

        # clients = clients[:self.env.consensus_total]  # limit requests!
        json_responses = await asyncio.gather(*[client.request(path, is_rpc=is_rpc) for client in clients])

        bad_clients = [client.node_ip for client, json_response in zip(clients, json_responses) if
                       json_response is None]
        if self.auto_ban and bad_clients:
            self.logger.info(f'Banning clients: {bad_clients}.')
            self.ban_list.update(set(bad_clients))

        if consensus:
            best_response, ratio = consensus_response(json_responses, consensus_n=m, total_n=n,
                                                      post_processor=post_processor)
        else:
            best_response, ratio = first_not_null(json_responses), 1.0

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

        for ip in seed_ips:
            client = self._new_client(ip)
            accounts = await client.request(self.env.path_nodes)
            if not accounts:
                continue
            nodes = [ThorNodeAccount.from_json(j) for j in accounts]
            ip_addresses = [node.ip_address for node in nodes if node.is_good]
            self._clients = [self._new_client(ip_address) for ip_address in ip_addresses]
            self.logger.info(f'Active clients: {len(self._clients)} from {len(accounts)}')
            self._last_client_update = time.monotonic()
            return

        self.logger.error('No active clients!')

    @property
    def seconds_from_last_node_update(self):
        return time.monotonic() - self._last_client_update

    async def update_nodes(self):
        seeds = await self._load_seed_list()
        await self._load_active_nodes(seeds)

    def client_list_except_banned(self):
        return [c for c in self._clients if c.node_ip not in self.ban_list]

    async def get_random_clients(self, n=0):
        if not self._last_client_update or time.monotonic() - self._last_client_update > self.client_update_period:
            await self.update_nodes()

        if self.env.consensus_total > len(self._clients):
            return self._clients
        else:
            clients = self.client_list_except_banned() if self.auto_ban else self._clients
            if len(clients) < self.env.consensus_total:
                self.logger.info('Opps! Banned to many clients! Unban them all!')
                self.ban_list = set()
                clients = self._clients

            population_n = self.env.consensus_total if n == 0 else n
            return self._rng.sample(clients, population_n)

    # --- METHODS ----

    async def query_custom_path(self, path, clients=None):
        clients = clients or (await self.get_random_clients())
        data = await self._request(path, clients)
        return data

    async def query_node_accounts(self, clients=None, consensus=True) -> List[ThorNodeAccount]:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_nodes, clients, consensus=consensus,
                                   post_processor=self.post_processor_for_pools)
        return [ThorNodeAccount.from_json(j) for j in data] if data else []

    async def query_queue(self, clients=None, consensus=True) -> ThorQueue:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_queue, clients, consensus=consensus)
        return ThorQueue.from_json(data)

    async def query_pools(self, height=None, *, clients=None, consensus=True) -> List[ThorPool]:
        clients = clients or (await self.get_random_clients())
        if height:
            path = self.env.path_pools_height.format(height=height)
        else:
            path = self.env.path_pools
        data = await self._request(path, clients, consensus=consensus)
        return [ThorPool.from_json(j) for j in data]

    async def query_pool(self, pool: str, height=None, *, clients=None, consensus=True) -> ThorPool:
        clients = clients or (await self.get_random_clients())
        if height:
            path = self.env.path_pool_height.format(pool=pool, height=height)
        else:
            path = self.env.path_pool.format(pool=pool)
        data = await self._request(path, clients, consensus=consensus)
        return ThorPool.from_json(data)

    async def query_last_blocks(self, clients=None, consensus=True) -> List[ThorLastBlock]:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_last_blocks, clients=clients, consensus=consensus)
        return [ThorLastBlock.from_json(j) for j in data] if isinstance(data, list) else [ThorLastBlock.from_json(data)]

    async def query_constants(self, clients=None, consensus=True) -> ThorConstants:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_constants, clients=clients, consensus=consensus)
        return ThorConstants.from_json(data)

    async def query_mimir(self, clients=None, consensus=True) -> ThorMimir:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_mimir, clients=clients, consensus=consensus)
        return ThorMimir.from_json(data)

    async def query_tendermint_block_raw(self, height, clients=None, consensus=True):
        clients = clients or (await self.get_random_clients())
        data = await self._request(f'/block?height={height}', clients, consensus=consensus, is_rpc=True)
        return data

    async def query_chain_info(self, clients=None, consensus=True) -> Dict[str, ThorChainInfo]:
        clients = clients or (await self.get_random_clients())
        data = await self._request(self.env.path_inbound_addresses, clients, consensus=consensus)
        if isinstance(data, list):
            info_list = [ThorChainInfo.from_json(j) for j in data]
        else:
            # noinspection PyUnresolvedReferences
            current = data.get('current', {})  # single-chain
            info_list = [ThorChainInfo.from_json(j) for j in current]
        return {info.chain: info for info in info_list}

    async def query_vault(self, vault_type=ThorVault.TYPE_ASGARD, clients=None, consensus=True) -> List[ThorVault]:
        clients = clients or (await self.get_random_clients())
        path = self.env.path_vault_asgard if vault_type == ThorVault.TYPE_ASGARD else self.env.path_vault_yggdrasil
        data = await self._request(path, clients, consensus=consensus)
        return [ThorVault.from_json(v) for v in data]

    # --- POST PROCESSORS ----

    @staticmethod
    def post_processor_for_pools(result):
        if not result:
            return result

        r = list(sorted(result, key=itemgetter('node_address')))
        return r
