import asyncio

import aiohttp

from aiothornode.connector import *
from aiothornode.env import MAINNET


async def main():
    env = MAINNET.copy()

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)

        asgards = await connector.query_vault(ThorVault.TYPE_ASGARD)
        print(asgards)

        print('-----')

        yggdrasils = await connector.query_vault(ThorVault.TYPE_YGGDRASIL)
        print(yggdrasils)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
