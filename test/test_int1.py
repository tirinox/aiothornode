import aiohttp
import pytest
from thorchain.connector import ThorConnector
from thorchain.types import TEST_NET_ENVIRONMENT_MULTI_1, CHAOS_NET_ENVIRONMENT


@pytest.fixture()
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
async def testnet_connector(session):
    return ThorConnector(TEST_NET_ENVIRONMENT_MULTI_1, session)


@pytest.fixture()
async def chaosnet_connector(session):
    return ThorConnector(CHAOS_NET_ENVIRONMENT, session)


@pytest.mark.asyncio
async def test_1(chaosnet_connector: ThorConnector):
    await chaosnet_connector.update_nodes()
    print(chaosnet_connector._clients)
