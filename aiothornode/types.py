import base64
import datetime
import re
import typing
from dataclasses import field
from hashlib import sha256
from typing import List

import ujson
from dateutil.parser import parse as date_parser

from .env import *

THOR_BASE_MULT = 10 ** 8


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
    internal: int = 0
    scheduled_outbound_value: int = 0

    @classmethod
    def from_json(cls, j):
        return cls(
            outbound=int(j.get('outbound', -1)),
            swap=int(j.get('swap', -1)),
            internal=int(j.get('internal', -1)),
            scheduled_outbound_value=int(j.get('scheduled_outbound_value', -1)),
        )

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
    bond_providers: dict = field(default_factory=dict)

    """
    {
  'node_address': 'thor104gsqwta048e80j909g6y9kkqdjrw0lff866ew',
  'status': 'Whitelisted',
  'pub_key_set': {},
  'validator_cons_pub_key': '',
  'bond': '2',
  'active_block_height': 0,
  'bond_address': 'thor1v6yh9m26tpytqndr368c42lt4ja0898djh5y7l',
  'status_since': 902755,
  'signer_membership': [],
  'requested_to_leave': False,
  'forced_to_leave': False,
  'leave_height': 0,
  'ip_address': '',
  'version': '0.0.0',
  'slash_points': 0,
  'jail': {
    'node_address': 'thor104gsqwta048e80j909g6y9kkqdjrw0lff866ew'
  },
  'current_award': '0',
  'observe_chains': None,
  'preflight_status': {
    'status': 'Standby',
    'reason': 'node account has invalid registered IP address',
    'code': 1
  },
  'bond_providers': {
    'node_address': 'thor104gsqwta048e80j909g6y9kkqdjrw0lff866ew',
    'node_operator_fee': '0',
    'providers': []
  }
}
    """

    @classmethod
    def from_json(cls: 'ThorNodeAccount', j):
        return cls(
            node_address=str(j.get('node_address', '')),
            status=str(j.get('status', '')),
            pub_key_set=j.get('pub_key_set'),
            validator_cons_pub_key=str(j.get('validator_cons_pub_key', '')),
            bond=int(j.get('bond', 0)),
            active_block_height=int(j.get('active_block_height', 0)),
            bond_address=str(j.get('bond_address', '')),
            status_since=int(j.get('status_since', 0)),
            signer_membership=j.get('signer_membership', []),
            requested_to_leave=bool(j.get('requested_to_leave', False)),
            forced_to_leave=bool(j.get('forced_to_leave', False)),
            leave_height=int(j.get('leave_height', 0)),
            ip_address=str(j.get('ip_address', '')),
            version=str(j.get('version', '')),
            slash_points=int(j.get('slash_points', 0)),
            jail=j.get('jail', {}),
            current_award=int(j.get('current_award', 0)),
            observe_chains=j.get('observe_chains', []),
            preflight_status=j.get('preflight_status', {}),
            bond_providers=j.get('bond_providers', {})
        )

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

    @property
    def amount_float(self):
        return self.amount / (10 ** self.decimals)

    @classmethod
    def from_json_bank(cls, j):
        return cls(
            amount=int(j.get('amount', 0)),
            asset=j.get('denom', ''),
            decimals=8
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


@dataclass
class ThorBalances:
    RUNE = 'rune'

    height: int
    assets: List[ThorCoin]
    address: str

    @property
    def runes(self):
        for asset in self.assets:
            if asset.asset == self.RUNE:
                return asset.amount
        return 0

    @property
    def runes_float(self):
        return self.runes / THOR_BASE_MULT

    @classmethod
    def from_json(cls, j, address):
        return cls(
            height=0,
            assets=[
                ThorCoin.from_json_bank(item) for item in j.get('balances')
            ],
            address=address
        )

    def find_by_name(self, name):
        candidates = [coin for coin in self.assets if coin.asset == name]
        return candidates[0] if candidates else None


@dataclass
class ThorBlock:
    height: int
    chain_id: str
    time: datetime.datetime
    hash: str
    txs_hashes: List[str]

    @classmethod
    def decode_tx_hash(cls, tx_b64: str):
        decoded = base64.b64decode(tx_b64.encode('utf-8'))
        return sha256(decoded).hexdigest().upper()

    @classmethod
    def from_json(cls, j):
        result = j.get('result', {})
        block = result['block']
        header = block['header']
        time = date_parser(header['time'])

        txs = [
            '0x' + cls.decode_tx_hash(content) for content in block['data']['txs']
        ]

        return cls(
            height=int(header['height']),
            chain_id=header['chain_id'],
            time=time,
            hash=result['block_id']['hash'],
            txs_hashes=txs
        )


class ThorTxAttribute(typing.NamedTuple):
    key: str
    value: str
    index: bool

    @classmethod
    def from_json(cls, j):
        return cls(
            base64.b64decode(j['key']).decode('utf-8'),
            base64.b64decode(j['value']).decode('utf-8'),
            bool(j['index'])
        )


class ThorTxEvent(typing.NamedTuple):
    type: str
    attributes: List[ThorTxAttribute]

    @classmethod
    def from_json(cls, j):
        return cls(
            type=j['type'],
            attributes=[ThorTxAttribute.from_json(a) for a in j['attributes']]
        )

    def value_of(self, key):
        return next(a.value for a in self.attributes if a.key == key)

    @property
    def sender(self):
        return self.value_of('sender')

    @property
    def recipient(self):
        return self.value_of('recipient')

    @property
    def amount(self):
        amt_str = self.value_of('amount')
        value, asset = re.findall(r'[A-Za-z]+|\d+', amt_str)
        return int(value), asset


@dataclass
class ThorNativeTX:
    hash: str
    height: int
    index: int
    code: int
    data: str
    log: List[dict]
    gas_wanted: int
    gas_used: int
    events: List[ThorTxEvent]

    TYPE_SET_MIMIR = 'set_mimir_attr'
    TYPE_ADD_LIQUIDITY = 'add_liquidity'
    TYPE_WITHDRAW = 'withdraw'

    @property
    def type(self):
        return re.sub(r'[^a-zA-Z0-9_]', '', self.data)

    @property
    def transfers(self):
        return [e for e in self.events if e.type == 'transfer']

    @classmethod
    def from_json(cls, j):
        result = j.get('result', j)
        tx_result = result['tx_result']
        data = base64.b64decode(tx_result['data']).decode('utf-8').strip()
        log = ujson.loads(tx_result['log'])
        events = [ThorTxEvent.from_json(e) for e in tx_result['events']]

        return cls(
            hash=result['hash'],
            height=int(result['height']),
            index=int(result['index']),
            code=int(tx_result['code']),
            data=data,
            log=log,
            gas_wanted=int(tx_result['gas_wanted']),
            gas_used=int(tx_result['gas_used']),
            events=events
        )


class ThorNativeTXSearchResults(typing.NamedTuple):
    total_count: int
    txs: List[ThorNativeTX]

    @classmethod
    def from_json(cls, j):
        result = j.get('result', {})
        return cls(
            total_count=int(result.get('total_count', 0)),
            txs=[ThorNativeTX.from_json(tx) for tx in result.get('txs', [])]
        )
