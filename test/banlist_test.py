from logging import INFO

import aiohttp

from aiothornode.connector import *
from aiothornode.env import CHAOS_NET_BNB_ENVIRONMENT


async def main():
    env = CHAOS_NET_BNB_ENVIRONMENT

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session, auto_ban=True)

        for block in range(100000, 500000, 1000):
            pools = await connector.query_pools(block)
            print(f'#{block = }: {len(pools)} pools')


if __name__ == '__main__':
    logging.basicConfig(level=logging.getLevelName(INFO))
    asyncio.run(main())
