from .fixtures import *


@pytest.mark.asyncio
async def test_mccn_balance(chaosnet_connector: ThorConnector):
    address = 'thor1q9vhc5zz8f097eyx7la4m35wsn7u3vds6sv9kg'
    balance = await chaosnet_connector.query_balance(address, consensus=False)
    assert balance.height > 0
    assert balance.assets
    assert balance.runes == 101124885115  # ???
    assert balance.runes_float == 1011.24885115
    assert balance.address == address
