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
