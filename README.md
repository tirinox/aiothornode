# aiothornode

This is a simple Python library to access [THORChain](https://thorchain.org/) nodes. It is asynchronous and uses _aiohttp_.

### Important

v.0.1.0 breaking changes:
1. NamedTuples instead of DataClasses for Thor entities
2. Environments were renamed
3. No more consensus features

v.0.0.21 is hotfix. Port 1317 was disabled, so it is an emergency upgrade to save this lib. More news will be later... 

### Features:

* Now it is just a convenient wrapper for THORNode API

### Supported endpoints:

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
import random

from aiothornode.connector import *
from aiothornode.env import *
import asyncio
import aiohttp


def delim():
    print('-' * 100)


async def main():
    env = MAINNET.copy()
    # env = ThorEnvironment(...)  # custom

    async with aiohttp.ClientSession() as session:
        connector = ThorConnector(env, session)

        genesis = await connector.query_genesis()
        print(f'Chain ID = {genesis["chain_id"]}')
        delim()

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
        mimir_1 = mimir.get('MINIMUMBONDINRUNE')
        print(f'Mimir: {mimir}, MINIMUMBONDINRUNE = {mimir_1}')
        delim()

        queue = await connector.query_queue()
        print(f'Queue: {queue}')
        delim()

        node_accounts = await connector.query_node_accounts(consensus=False)
        print(f'Example node account: {random.sample(node_accounts, 1)[0]}')
        delim()

        pool = await connector.query_pool('BNB.BUSD-BD1', height=8218339)
        print(pool)
        delim()

        pools = await connector.query_pools()
        print(pools[0])
        print(f'Total {len(pools)} pools')
        delim()

        bank = await connector.query_balance('thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt')
        print(f'Balance of {bank.address} is {bank.runes_float} Rune')
        delim()


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
