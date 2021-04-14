import aiohttp
import pytest

from aiothornode.connector import ThorConnector
from aiothornode.env import CHAOS_NET_BNB_ENVIRONMENT, TEST_NET_ENVIRONMENT_MULTI_1


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
