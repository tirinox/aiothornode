from .fixtures import *


@pytest.mark.asyncio
async def test_mccn_block_txs(chaosnet_connector: ThorConnector):
    height = 545084
    blk = await chaosnet_connector.query_block(height, consensus=False)
    print(blk)