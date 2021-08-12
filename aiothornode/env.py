from copy import copy
from dataclasses import dataclass


@dataclass
class ThorEnvironment:
    seed_url: str = ''
    midgard_url: str = ''

    timeout: float = 3.0
    consensus_min: int = 2
    consensus_total: int = 3

    path_queue: str = '/thorchain/queue'
    path_nodes: str = '/thorchain/nodes'
    path_pools: str = "/thorchain/pools"
    path_pools_height: str = "/thorchain/pools?height={height}"
    path_pool: str = "/thorchain/pool/{pool}"
    path_pool_height: str = "/thorchain/pool/{pool}?height={height}"

    path_last_blocks: str = "/thorchain/lastblock"
    path_constants: str = "/thorchain/constants"
    path_mimir: str = "/thorchain/mimir"
    path_inbound_addresses: str = "/thorchain/inbound_addresses"
    path_vault_yggdrasil: str = "/thorchain/vaults/yggdrasil"
    path_vault_asgard: str = "/thorchain/vaults/asgard"
    path_balance: str = '/bank/balances/{address}'
    path_block_by_height: str = '/block?height={height}'
    path_tx_by_hash: str = '/tx?hash={hash}'
    path_tx_search: str = '/tx_search?query={query}&prove={prove}&page={page}&per_page={per_page}&order_by={order_by}'

    def copy(self):
        return copy(self)

    def set_consensus(self, minimum, total):
        assert total >= 1
        assert 1 <= minimum <= total
        self.consensus_total = total
        self.consensus_min = minimum
        return self

    def set_timeout(self, timeout):
        assert timeout > 0.0
        self.timeout = timeout
        return self


# deprecated!
CHAOS_NET_BNB_ENVIRONMENT = ThorEnvironment(seed_url='https://chaosnet-seed.thorchain.info/',
                                            midgard_url='https://chaosnet-midgard.bepswap.com/',
                                            path_nodes='/thorchain/nodeaccounts',
                                            path_inbound_addresses='/thorchain/pool_addresses')

TEST_NET_ENVIRONMENT_MULTI_1 = ThorEnvironment(seed_url='https://testnet.seed.thorchain.info',
                                               midgard_url='https://testnet.midgard.thorchain.info/')

MULTICHAIN_CHAOSNET_ENVIRONMENT = ThorEnvironment(seed_url='https://seed.thorchain.info/',
                                                  midgard_url='https://midgard.thorchain.info/')

SCCN = CHAOS_NET_BNB_ENVIRONMENT  # alias
MCCN = MULTICHAIN_CHAOSNET_ENVIRONMENT  # alias
MCTN = TEST_NET_ENVIRONMENT_MULTI_1  # alias
