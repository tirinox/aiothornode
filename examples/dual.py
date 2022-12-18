import logging
import random

from aiothornode.connector import ThorConnector
from aiothornode.env import MAINNET_ENVIRONMENT
import asyncio
import aiohttp


def delim():
    print('-' * 100)


async def main():
    logging.basicConfig(
        level=logging.getLevelName(logging.DEBUG),
        format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    async with aiohttp.ClientSession() as session:
        primary_env = MAINNET_ENVIRONMENT.copy()
        primary_env.timeout = 0.05  # probably too low, but we want to see the timeout
        primary_env.retries = 2
        primary_env.retry_delay = 0.7

        backup_env = MAINNET_ENVIRONMENT.copy()
        backup_env.timeout = 5
        backup_env.thornode_url = 'https://thornode-archive.ninerealms.com'

        connector = ThorConnector(primary_env, session,
                                  additional_envs=backup_env)  # two envs: primary and backup
        connector.set_client_id_for_all('footest')

        votes = await connector.query_mimir_votes()
        print(f'Votes: {len(votes)}, example: {votes[0]}')
        assert all(v.key and v.value is not None and v.singer for v in votes)
        delim()

        node_mimir = await connector.query_mimir_node_accepted()
        print(f'Node mimir: {node_mimir}')
        delim()

        chains = await connector.query_chain_info()
        chains = list(chains.values())
        print('Chain info:', chains)
        delim()

        liq_providers = await connector.query_liquidity_providers('BTC.BTC')
        print(f'LProviders: {len(liq_providers)}')

        def test_providers(providers, is_savers):
            assert len(providers) > 0
            if is_savers:
                assert all(p.rune_deposit_value == 0 for p in providers)
            assert all(p.rune_address or p.asset_address for p in providers)
            assert any(p.asset_deposit_value > 0 or p.rune_deposit_value > 0 for p in providers)
            assert all(p.last_add_height > 0 for p in providers)
            assert all(
                p.units > 0 or ((p.pending_rune > 0 or p.pending_asset > 0) and p.pending_tx_id) for p in providers)
            assert any(p.last_withdraw_height > 0 for p in providers)

        test_providers(liq_providers, False)

        # archive does not support savers
        # savers = await connector.query_savers('BTC.BTC')
        # print(f'Savers: {len(savers)}')
        # test_providers(savers, True)

        delim()

        print('Tendermint Block:')
        tender_block = await connector.query_tendermint_block_raw(8218339)
        block_header = tender_block['result']['block']['header']
        print(f'{block_header["height"] = } and {block_header["time"] = }')
        delim()

        constants = await connector.query_constants()
        print(f'Constants: {constants}')
        delim()

        mimir = await connector.query_mimir()
        mimir_1 = mimir.get('MINIMUMBONDINRUNE')
        print(f'Mimir: {mimir}, MINIMUMBONDINRUNE = {mimir_1}')
        delim()

        queue = await connector.query_queue()
        print(f'Queue: {queue}')
        delim()

        node_accounts = await connector.query_node_accounts()
        print(f'Example node account: {random.sample(node_accounts, 1)[0]}')
        delim()

        pool = await connector.query_pool('BNB.BUSD-BD1', height=8218339)
        print(pool)
        delim()

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        delim()

        bank = await connector.query_balance('thor1lj62pg6ryxv2htekqx04nv7wd3g98qf9gfvamy')
        print(f'Balance of {bank.address} is {bank.runes_float} Rune')
        delim()

        status = await connector.query_native_status_raw()
        print(f'Status: {status}')
        delim()

        block_results = await connector.query_native_block_results_raw(8240015)
        print(f'Block: {block_results}')


if __name__ == '__main__':
    asyncio.run(main())
