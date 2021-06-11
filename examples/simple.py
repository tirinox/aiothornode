from aiothornode.connector import *
from aiothornode.env import *
import asyncio
import aiohttp


def delim():
    print('-' * 100)


async def main():
    env = MULTICHAIN_CHAOSNET_ENVIRONMENT.copy()
    # env = CHAOS_NET_BNB_ENVIRONMENT.copy()
    # env = TEST_NET_ENVIRONMENT_MULTI_1.copy()  # TestNet
    # env = ThorEnvironment(seed_url='https://my-thor-seed.org')  # custom

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)

        print('Tendermint Block:')
        tender_block = await connector.query_tendermint_block_raw(10001)
        block_header = tender_block['result']['block']['header']
        print(f'{block_header["height"] = } and {block_header["time"] = }')
        delim()

        constants = await connector.query_constants()
        print(f'Constants: {constants}')
        delim()

        mimir = await connector.query_mimir()
        mimir_1 = mimir.get('mimir//MINIMUMBONDINRUNE')
        print(f'Mimir: {mimir}, MINIMUMBONDINRUNE = {mimir_1}')
        delim()

        queue = await connector.query_queue()
        print(f'Queue: {queue}')
        delim()

        node_accounts = await connector.query_node_accounts(consensus=False)
        print(f'Example node account: {node_accounts[0]}')
        delim()

        pool = await connector.query_pool('BNB.BUSD-BD1', height=71111)
        print(pool)
        delim()

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        delim()


if __name__ == '__main__':
    asyncio.run(main())
