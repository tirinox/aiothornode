import pytest

from aiothornode.types import ThorPool
from .fixtures import *



async def internal_constants_test(c: ThorConnector):
    constants = await c.query_constants()
    assert constants['BlocksPerYear'] > 100
    assert constants.get('blabla', 'lol') == 'lol'
    str_const = constants.get('DefaultPoolStatus')
    assert isinstance(str_const, str) and len(str_const) > 1
    assert constants['BadValidatorRate'] > 10


@pytest.mark.asyncio
async def test_constants(mainnet_connector: ThorConnector):
    await internal_constants_test(mainnet_connector)


@pytest.mark.asyncio
async def test_constants_chaos(mainnet_connector: ThorConnector):
    await internal_constants_test(mainnet_connector)


async def internal_queue_test(c: ThorConnector):
    queue = await c.query_queue()
    assert int(queue.swap) >= 0
    assert int(queue.outbound) >= 0


@pytest.mark.asyncio
async def test_update_nodes(mainnet_connector: ThorConnector):
    print(mainnet_connector._clients)


@pytest.mark.asyncio
async def test_queue_test(mainnet_connector: ThorConnector):
    await internal_queue_test(mainnet_connector)


@pytest.mark.asyncio
async def test_queue_chaos(mainnet_connector: ThorConnector):
    await internal_queue_test(mainnet_connector)


def pool_validate(pool: ThorPool):
    assert pool
    assert pool.asset
    assert pool.runes_per_asset > 0
    assert pool.assets_per_rune > 0
    assert pool.pool_units > 0
    assert pool.balance_asset > 0
    assert pool.balance_rune > 0
    assert pool.status in (pool.STATUS_AVAILABLE, pool.STATUS_BOOTSTRAP, pool.STATUS_ENABLED)


async def internal_pools_test(c: ThorConnector, height=None):
    pools = await c.query_pools(height)
    # print(pools)
    assert pools, "no pools"
    for pool in pools:
        pool_validate(pool)


async def internal_pool_test(c: ThorConnector, pool, height=None):
    pool = await c.query_pool(pool, height)
    # print(pools)
    assert pool, "no pool"
    pool_validate(pool)


@pytest.mark.asyncio
async def test_pools_test(mainnet_connector: ThorConnector):
    await internal_pools_test(mainnet_connector)
    await internal_pools_test(mainnet_connector, height=36001)
    await internal_pool_test(mainnet_connector, 'BTC.BTC')
    await internal_pool_test(mainnet_connector, 'BTC.BTC', 36002)


@pytest.mark.asyncio
async def test_pools_chaos(mainnet_connector: ThorConnector):
    await internal_pools_test(mainnet_connector)
    await internal_pools_test(mainnet_connector, height=1000001)
    await internal_pool_test(mainnet_connector, 'BNB.BNB')
    await internal_pool_test(mainnet_connector, 'BNB.BNB', height=100001)


async def internal_last_blocks_test(c: ThorConnector):
    lb = await c.query_last_blocks()
    assert lb


@pytest.mark.asyncio
async def test_last_block_test(mainnet_connector: ThorConnector):
    await internal_last_blocks_test(mainnet_connector)


@pytest.mark.asyncio
async def test_last_block_chaos(mainnet_connector: ThorConnector):
    await internal_last_blocks_test(mainnet_connector)
