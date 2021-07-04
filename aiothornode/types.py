from copy import copy
from dataclasses import dataclass, field
from typing import List


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
    outbound: str = '0'
    swap: str = '0'
    internal: str = '0'

    @classmethod
    def from_json(cls, j):
        return cls(**j)

    @property
    def total(self):
        return int(self.outbound) + int(self.swap) + int(self.internal)


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
class ThorLastBlock:
    chain: str = ''
    last_observed_in: int = 0
    last_signed_out: int = 0
    thorchain: int = 0

    @classmethod
    def from_json(cls, j):
        x = cls()
        x.chain = j.get('chain', '')
        x.thorchain = j.get('thorchain', 0)
        x.last_observed_in = j.get('last_observed_in', 0) if 'last_observed_in' in j else j.get('lastobservedin')
        x.last_signed_out = j.get('last_signed_out', 0) if 'last_signed_out' in j else j.get('lastsignedout')
        return x


@dataclass
class ThorPool:
    STATUS_AVAILABLE = 'Available'
    STATUS_BOOTSTRAP = 'Bootstrap'
    STATUS_ENABLED = 'Enabled'

    balance_asset: str = '0'
    balance_rune: str = '0'
    asset: str = ''
    pool_units: str = '0'
    status: str = ''
    synth_units: str = ''
    decimals: str = '0'
    error: str = ''
    pending_inbound_rune: str = '0'
    pending_inbound_asset: str = '0'

    @property
    def balance_asset_int(self):
        return int(self.balance_asset)

    @property
    def balance_rune_int(self):
        return int(self.balance_rune)

    @property
    def pool_units_int(self):
        return int(self.pool_units)

    @property
    def assets_per_rune(self):
        return self.balance_asset_int / self.balance_rune_int

    @property
    def runes_per_asset(self):
        return self.balance_rune_int / self.balance_asset_int

    @classmethod
    def from_json(cls, j):
        return cls(
            balance_asset=j.get('balance_asset', '0'),
            balance_rune=j.get('balance_rune', '0'),
            asset=j.get('asset', ''),
            pool_units=j.get('LP_units', '0') if 'LP_units' in j else j.get('pool_units', '0'),
            status=j.get('status', cls.STATUS_BOOTSTRAP),
            synth_units=j.get('synth_units', '0'),
            decimals=j.get('decimals', '0'),
            error=j.get('error', ''),
            pending_inbound_rune=j.get('pending_inbound_rune', '0'),
            pending_inbound_asset=j.get('pending_inbound_asset', '0'),
        )


@dataclass
class ThorConstants:
    constants: dict = field(default_factory=dict)
    data_types: dict = field(default_factory=dict)

    DATA_TYPES = ('int_64_values', 'bool_values', 'string_values')

    @classmethod
    def from_json(cls, j):
        holder = cls()
        for dt in cls.DATA_TYPES:
            subset = j.get(dt, {})
            holder.data_types[dt] = {}
            for k, v in subset.items():
                holder.constants[k] = v
                holder.data_types[dt][k] = v

        return holder

    def get(self, name, default=None):
        return self.constants.get(name, default)

    def __getitem__(self, item):
        return self.constants[item]


@dataclass
class ThorMimir:
    constants: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, j: dict):
        holder = cls()
        for k, v in j.items():
            holder.constants[k] = v
        return holder

    def get(self, name, default=None):
        return self.constants.get(name, default)

    def __getitem__(self, item):
        return self.constants[item]


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

    def copy(self):
        return copy(self)

    def set_consensus(self, minimum, total):
        assert total >= 1
        assert 1 <= minimum <= total
        self.consensus_total = total
        self.consensus_min = minimum


@dataclass
class ThorChainInfo:
    chain: str = ''
    pub_key: str = ''
    address: str = ''
    router: str = ''  # for smart-contract based chains
    halted: bool = False
    gas_rate: int = 0

    @property
    def is_ok(self):
        return self.chain and self.pub_key and self.address

    @classmethod
    def from_json(cls, j):
        return cls(
            chain=j.get('chain', ''),
            pub_key=j.get('pub_key', ''),
            address=j.get('address', ''),
            router=j.get('router', ''),
            halted=bool(j.get('halted', True)),
            gas_rate=int(j.get('gas_rate', 0)),
        )


@dataclass
class ThorCoin:
    asset: str = ''
    amount: int = 0
    decimals: int = 18

    @classmethod
    def from_json(cls, j):
        return cls(
            asset=j.get('asset'),
            amount=int(j.get('amount', 0)),
            decimals=int(j.get('decimals', 18))
        )


@dataclass
class ThorRouter:
    chain: str = ''
    router: str = ''

    @classmethod
    def from_json(cls, j):
        return cls(
            chain=j.get('chain', ''),
            router=j.get('router', '')
        )


@dataclass
class ThorAddress:
    chain: str = ''
    address: str = ''

    @classmethod
    def from_json(cls, j):
        return cls(
            chain=j.get('chain', ''),
            address=j.get('address', '')
        )


@dataclass
class ThorVault:
    block_height: int = 0
    pub_key: str = ''
    coins: List[ThorCoin] = field(default_factory=list)
    type: str = ''
    status: str = ''
    status_since: int = 0
    membership: List[str] = field(default_factory=list)
    chains: List[str] = field(default_factory=list)
    inbound_tx_count: int = 0
    outbound_tx_count: int = 0
    routers: List[ThorRouter] = field(default_factory=list)
    addresses: List[ThorAddress] = field(default_factory=list)

    TYPE_YGGDRASIL = 'YggdrasilVault'
    TYPE_ASGARD = 'AsgardVault'

    STATUS_ACTIVE = "Active"
    STATUS_ACTIVE_VAULT = "ActiveVault"
    STATUS_STANDBY = "Standby"
    STATUS_RETIRING = "RetiringVault"

    @property
    def is_active(self):
        return self.status in (self.STATUS_ACTIVE, self.STATUS_ACTIVE_VAULT)

    @classmethod
    def from_json(cls, j):
        return cls(
            block_height=int(j.get('block_height', 0)),
            pub_key=j.get('pub_key', ''),
            coins=[ThorCoin.from_json(coin) for coin in j.get('coins', [])],
            type=j.get('type', ''),
            status=j.get('status', ''),
            status_since=int(j.get('status_since', 0)),
            membership=j.get('membership', []),
            chains=j.get('chains', []),
            inbound_tx_count=int(j.get('inbound_tx_count', 0)),
            outbound_tx_count=int(j.get('outbound_tx_count', 0)),
            routers=[ThorRouter.from_json(r) for r in j.get('routers', [])],
            addresses=[ThorAddress.from_json(a) for a in j.get('addresses', [])],
        )
