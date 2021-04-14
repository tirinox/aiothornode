# aiothornode

This is a simple Python library to access [THORChain](https://thorchain.org/) nodes. It is asynchronous and uses **
aiohttp**.

Features:

* Connecting to a seed service
* Filter out inactive nodes
* Simple consensus algorithm (connecting to a random subset of active nodes and sending them the same request and
  choosing the most frequent answer)
* Automatically updates of the list of nodes

Supported endpoints:

* Constants
* Mimir
* Nodes (node accounts)
* Current TX queue length
* Pools (current and at arbitrary height)

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
