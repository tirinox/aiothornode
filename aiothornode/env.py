from aiothornode.types import ThorEnvironment

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

