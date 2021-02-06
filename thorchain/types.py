from dataclasses import dataclass, field


class ThorException(Exception):
    def __init__(self, j, *args) -> None:
        super().__init__(*args)
        if j and isinstance(j, dict):
            self.code = j.get('code', '')
            self.message = j.get('message', '')
            self.details = j.get('details', [])
        else:
            self.code = -10000
            self.message = 'Failed to decode the error'
            self.details = [
                repr(j)
            ]


@dataclass
class ThorQueue:
    outbound: int = 0
    swap: int = 0


@dataclass
class ThorNodeAccount:
    STATUS_STANDBY = 'standby'
    STATUS_ACTIVE = 'active'
    STATUS_READY = 'ready'
    STATUS_WHITELISTED = 'whitelisted'
    STATUS_UNKNOWN = 'unknown'
    STATUS_DISABLED = 'disabled'

    node_address: str = 'thor?'
    status: str = ''
    pub_key_set: dict = field(default_factory=dict)
    validator_cons_pub_key: str = ''
    bond: str = ''
    active_block_height: int = 0
    bond_address: str = ''
    status_since: str = ''
    signer_membership: list = field(default_factory=list)
    requested_to_leave: bool = False
    forced_to_leave: bool = False
    leave_height: int = 0
    ip_address: str = ''
    version: str = ''
    slash_points: int = 0
    jail: dict = field(default_factory=dict)
    current_award: str = ''
    observe_chains: list = field(default_factory=list)
    preflight_status: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, j):
        return cls(**j)

    @property
    def preflight_status_reason_and_code(self):
        status = self.preflight_status.get('status', '').lower()
        reason = self.preflight_status.get('reason', '')
        code = self.preflight_status.get('code', 0)
        return status, reason, code

    @property
    def is_good(self):
        status = self.status.lower()
        return status in (self.STATUS_ACTIVE, self.STATUS_WHITELISTED) \
               and not self.requested_to_leave and not self.forced_to_leave and self.ip_address


@dataclass
class ThorEnvironment:
    seed_url: str = ''
    midgard_url: str = ''

    timeout: float = 3.0
    consensus_min: int = 2
    consensus_total: int = 3

    path_queue: str = '/thorchain/queue'
    path_nodes: str = '/thorchain/nodes'


CHAOS_NET_BNB_ENVIRONMENT = ThorEnvironment(seed_url='https://chaosnet-seed.thorchain.info/',
                                            midgard_url='https://chaosnet-midgard.bepswap.com/',
                                            path_nodes='/thorchain/nodeaccounts')

TEST_NET_ENVIRONMENT_MULTI_1 = ThorEnvironment(seed_url='https://testnet.seed.thorchain.info',
                                               midgard_url='https://testnet.midgard.thorchain.info/')
