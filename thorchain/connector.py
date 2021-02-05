import asyncio
import logging
from random import shuffle
from typing import List

import ujson
from aiohttp import ClientSession

from consensus import consensus_response
from nodeclient import ThorNodeClient
from thorchain.types import ThorEnvironment


class ThorConnector:
    QUERY_NODE_ACCOUNTS = '/thorchain/nodeaccounts'

    def __init__(self, env: ThorEnvironment, session: ClientSession, logger=None):
        self.session = session
        self.env = env
        self.logger = logger or logging.getLogger('ThorConnector')
        self._clients = {}

    async def _request(self, path: str, clients: List[ThorNodeClient]):
        self.logger.info(f'Start request to Thor node "{path}"')

        m, n = self.env.consensus_min, self.env.consensus_total
        if len(clients) < n:
            self.logger.warning(f'Too few nodes in the network!')
            m = 0

        clients = clients[:self.env.consensus_total]  # limit requests!
        text_responses = await asyncio.gather(*[client.request_raw(path) for client in clients])
        best_text_response, ratio = consensus_response(text_responses, consensus_n=m, total_n=n)
        if best_text_response is None:
            ips = [client.node_ip for client in clients]
            self.logger.error(f'No consensus reached between nodes: {ips} for request "{path}"!')
            return None
        else:
            self.logger.info(f'Success for the request "{path}" consensus: {(ratio * 100.0):.0f}%')
            return ujson.loads(best_text_response)

    async def _load_seed_list(self):
        assert self.session
        self.logger.info(f'Using seed URL: {self.env.seed_url}')
        async with self.session.get(self.env.seed_url) as resp:
            seed_nodes = await resp.json()
            return seed_nodes

    @staticmethod
    def _is_ok_node(node_j):
        return (
                node_j['status'] == 'active' and
                not node_j['requested_to_leave'] and
                not node_j['forced_to_leave']
        )

    def _new_client(self, ip_addr):
        return ThorNodeClient(ip_addr, self.session, self.env.timeout, self.logger)

    async def _load_active_nodes(self, seed_ips: List[str]):
        shuffle(seed_ips)
        clients = [self._new_client(ip_addr) for ip_addr in seed_ips[:self.env.consensus_total]]
        data = await self._request(self.QUERY_NODE_ACCOUNTS, clients)
        if data:
            ip_addresses = [node['ip_address'] for node in data if self._is_ok_node(node)]
            self._clients = {
                ip_addr: self._new_client(ip_addr) for ip_addr in ip_addresses
            }
            self.logger.info(f'Active clients: {len(self._clients)}')
        else:
            self.logger.error('No active clients!')

    async def update_nodes(self):
        seeds = await self._load_seed_list()
        await self._load_active_nodes(seeds)

# https://gitlab.com/thorchain/thornode/-/blob/master/x/thorchain/query/query.go
# /observe_chains new path

# async def request(self, path: str):
#     if not path.startswith('/'):
#         path = '/' + path
#     node_ips = await self.node_ip_man.select_nodes(self.cohort_size)
#
#     self.logger.info(f'Start request to Thor node "{path}"')
#     text_responses = await asyncio.gather(*[self._request_one_node_as_text(ip, path) for ip in node_ips])
#     best_text_response, ratio = self._consensus_response(text_responses)
#     if best_text_response is None:
#         self.logger.error(f'No consensus reached between nodes: {node_ips} for request "{path}"!')
#         return None
#     else:
#         self.logger.info(f'Success for the request "{path}" consensus: {(ratio * 100.0):.0f}%')
#         return ujson.loads(best_text_response)
