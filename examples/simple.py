import random

from aiothornode.connector import *
from aiothornode.env import *
import asyncio
import aiohttp


def delim():
    print('-' * 100)


async def main():
    env = MCCN.copy()
    # env = TEST_NET_ENVIRONMENT_MULTI_1.copy()  # TestNet
    # env = ThorEnvironment(seed_url='https://my-thor-seed.org')  # custom

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)


        chains = await connector.query_chain_info()
        chains = list(chains.values())
        print('Chain info:', chains)
        delim()

        print('Tendermint Block:')
        tender_block = await connector.query_tendermint_block_raw(100001)
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
        print(f'Example node account: {random.sample(node_accounts, 1)[0]}')
        delim()

        pool = await connector.query_pool('BNB.BUSD-BD1', height=71111)
        print(pool)
        delim()

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        delim()

        bank = await connector.query_balance('thor1q9vhc5zz8f097eyx7la4m35wsn7u3vds6sv9kg')
        print(f'Balance of {bank.address} is {bank.runes_float} Rune')
        delim()

        txs = await connector.query_native_tx_search("tx.height=1522004", page=1, per_page=2)
        print(f'Txs search: {txs}')
        delim()

        tx = await connector.query_native_tx(
            '3A65AED750FE0461C87760FCA1614DCF3410778A92B8F5878E38FD4CFEB81860',
            before_hard_fork=True
        )
        print(f'Tx = {tx}')
        delim()


if __name__ == '__main__':
    asyncio.run(main())
