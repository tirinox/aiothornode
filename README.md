# aiothornode

This is a simple Python library to access [THORChain](https://thorchain.org/) nodes. It is asynchronous and uses _aiohttp_.

## Important

v.0.0.21 is hotfix. Port 1317 was disabled, so it is an emergency upgrade to save this lib. More news will be later... 

Features:

* Connecting to a seed service
* Filter out inactive nodes
* Simple consensus algorithm (connecting to a random subset of active nodes and sending them the same request and
  choosing the most frequent answer)
* Automatically updates of the list of nodes
* Automatic ban-list for bad nodes

Supported endpoints:

* Constants
* Mimir
* Nodes (node accounts)
* Current TX queue length
* Pools (current and at arbitrary height)
* Tendermint block at height
* Inbound addresses and other chain info
* Asgard & Yggdrasil vaults (new!)
* Balance of THOR account

## Installation

`python -m pip install git+https://github.com/tirinox/aiothornode`

## Quick start


The following code is quite self-documenting:

```
from aiothornode.connector import *
from aiothornode.types import *
import asyncio
import aiohttp

async def main():
    env = CHAOS_NET_BNB_ENVIRONMENT
    # env = TEST_NET_ENVIRONMENT_MULTI_1  # TestNet
    # env = ThorEnvironment(seed_url='https://my-thor-seed.org')  # custom
    
    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)
        
        chains = await connector.query_chain_info()
        chains = list(chains.values())
        print('Chain info:', chains)
        
        tender_block = await connector.query_tendermint_block_raw(10001)
        block_header = tender_block['result']['block']['header']
        print(f'{block_header["height"] = } and {block_header["time"] = }')

        constants = await connector.query_constants()
        print(f'Constants: {constants}')
        
        mimir = await connector.query_mimir()
        mimir_1 = mimir['mimir//EMISSIONCURVE']
        print(f'Mimir: {mimir}, EMISSIONCURVE = {mimir_1}')

        queue = await connector.query_queue()
        print(f'Queue: {queue}')

        node_accounts = await connector.query_node_accounts()
        print(f'Example node account: {node_accounts[0]}')

        pool = await connector.query_pool('BNB.BNB', height=888123)
        print(pool)

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        
        bank = await connector.query_balance('thor1q9vhc5zz8f097eyx7la4m35wsn7u3vds6sv9kg')
        print(f'Balance of {bank.address} is {bank.runes_float} Rune')
        
        txs = await connector.query_native_tx_search("tx.height=1522004", page=1, per_page=2)
        print(f'Txs search: {txs}')
        
        tx = await connector.query_native_tx(
            'E8510F9636377D66BEC8E263FBFE0B86C92CD3E801794BFFA553C5A9CA42CF09'
        )
        print(f'Tx = {tx}')

if __name__ == '__main__':
    asyncio.run(main())
```

## Testing

Install PyTest and an async plugin for it:

```
pip install pytest
pip install pytest-asyncio
```

Then run

```
pytest test
```
