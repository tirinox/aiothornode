from dataclasses import dataclass


@dataclass
class ThorEnvironment:
    seed_url: str = ''
    midgard_url: str = ''
    timeout: float = 3.0
    consensus_min: int = 2
    consensus_total: int = 3


CHAOS_NET_ENVIRONMENT = ThorEnvironment(seed_url='https://chaosnet-seed.thorchain.info/',
                                        midgard_url='https://chaosnet-midgard.bepswap.com/')

TEST_NET_ENVIRONMENT_MULTI_1 = ThorEnvironment(seed_url='https://testnet.seed.thorchain.info',
                                               midgard_url='https://testnet.midgard.thorchain.info/')


@dataclass
class ThorQueue:
    outbound: int = 0
    swap: int = 0
