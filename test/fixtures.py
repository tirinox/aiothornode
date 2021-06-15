import aiohttp
import pytest

from aiothornode.connector import ThorConnector
from aiothornode.env import SCCN, MCCN, MCTN


@pytest.fixture()
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
async def testnet_connector(session):
    con = ThorConnector(MCTN, session)
    await con.update_nodes()
    return con


@pytest.fixture()
async def chaosnet_connector(session):
    con = ThorConnector(MCCN, session)
    await con.update_nodes()
    return con


@pytest.fixture()
async def sc_chaosnet_connector(session):
    con = ThorConnector(SCCN, session)
    await con.update_nodes()
    return con
