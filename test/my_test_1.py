import aiohttp

from aiothornode.connector import *
from aiothornode.env import TEST_NET_ENVIRONMENT_MULTI_1


async def main():
    env = TEST_NET_ENVIRONMENT_MULTI_1

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)

        pools = await connector.query_pools(377)
        print(pools[0])
        print(f'Total {len(pools)} pools')


if __name__ == '__main__':
    asyncio.run(main())
