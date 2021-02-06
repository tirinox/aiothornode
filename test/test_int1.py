import aiohttp
import pytest
from thorchain.connector import ThorConnector
from thorchain.types import TEST_NET_ENVIRONMENT_MULTI_1, CHAOS_NET_BNB_ENVIRONMENT


@pytest.fixture()
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
async def testnet_connector(session):
    con = ThorConnector(TEST_NET_ENVIRONMENT_MULTI_1, session)
    await con.update_nodes()
    return con


@pytest.fixture()
async def chaosnet_connector(session):
    con = ThorConnector(CHAOS_NET_BNB_ENVIRONMENT, session)
    await con.update_nodes()
    return con


async def internal_queue_test(c: ThorConnector):
    queue = await c.query_queue()
    assert int(queue.swap) >= 0
    assert int(queue.outbound) >= 0


@pytest.mark.asyncio
async def test_update_nodes(testnet_connector: ThorConnector):
    print(testnet_connector._clients)


@pytest.mark.asyncio
async def test_queue_test(testnet_connector: ThorConnector):
    await internal_queue_test(testnet_connector)


@pytest.mark.asyncio
async def test_queue_chaos(chaosnet_connector: ThorConnector):
    await internal_queue_test(chaosnet_connector)


async def internal_pools_test(c: ThorConnector):
    pools = await c.query_pools()
    print(pools)
    assert pools, "no pools"
    for pool in pools:
        assert pool.asset
        assert pool.runes_per_asset > 0
        assert pool.assets_per_rune > 0
        assert pool.pool_units_int > 0
        assert pool.balance_asset_int > 0
        assert pool.balance_rune_int > 0
        assert pool.status in (pool.STATUS_AVAILABLE, pool.STATUS_BOOTSTRAP, pool.STATUS_ENABLED)


@pytest.mark.asyncio
async def test_pools_test(testnet_connector: ThorConnector):
    await internal_pools_test(testnet_connector)


@pytest.mark.asyncio
async def test_pools_chaos(chaosnet_connector: ThorConnector):
    await internal_pools_test(chaosnet_connector)
