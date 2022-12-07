import aiohttp
import pytest_asyncio

from aiothornode.connector import ThorConnector
from aiothornode.env import MAINNET, STAGENET


@pytest_asyncio.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def mainnet_connector(session):
    con = ThorConnector(MAINNET, session)
    return con


@pytest_asyncio.fixture
async def stagenet_connector(session):
    con = ThorConnector(STAGENET, session)
    return con
