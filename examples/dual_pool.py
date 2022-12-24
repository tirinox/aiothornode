import asyncio
import logging

import aiohttp

from aiothornode.connector import ThorConnector
from aiothornode.env import MAINNET_ENVIRONMENT


async def main():
    logging.basicConfig(
        level=logging.getLevelName(logging.DEBUG),
        format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    async with aiohttp.ClientSession() as session:
        primary_env = MAINNET_ENVIRONMENT.copy()
        primary_env.timeout = 5
        primary_env.retries = 20
        primary_env.retry_delay = 10

        backup_env = MAINNET_ENVIRONMENT.copy()
        backup_env.timeout = 5
        backup_env.thornode_url = 'https://thornode-archive.ninerealms.com'

        connector = ThorConnector(primary_env, session,
                                  additional_envs=backup_env)  # two envs: primary and backup
        connector.set_client_id_for_all('footest')

        # this block is empty on the main node, but it is available on the archive node
        pools = await connector.query_pools(height=1000000)
        print(len(pools))


if __name__ == '__main__':
    asyncio.run(main())
