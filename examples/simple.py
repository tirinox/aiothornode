from aiothornode.connector import *
from aiothornode.types import *
import asyncio
import aiohttp


def delim():
    print('-' * 100)


async def main():
    env = CHAOS_NET_BNB_ENVIRONMENT
    # env = TEST_NET_ENVIRONMENT_MULTI_1  # TestNet
    # env = ThorEnvironment(seed_url='https://my-thor-seed.org')  # custom

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)

        constants = await connector.query_constants()
        print(f'Constants: {constants}')
        delim()

        mimir = await connector.query_mimir()
        mimir_1 = mimir['mimir//EMISSIONCURVE']
        print(f'Mimir: {mimir}, EMISSIONCURVE = {mimir_1}')
        delim()

        queue = await connector.query_queue()
        print(f'Queue: {queue}')
        delim()

        node_accounts = await connector.query_node_accounts()
        print(f'Example node account: {node_accounts[0]}')
        delim()

        pool = await connector.query_pool('BNB.BNB', height=888123)
        print(pool)
        delim()

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        delim()


if __name__ == '__main__':
    asyncio.run(main())
