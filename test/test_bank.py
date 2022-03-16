from .fixtures import *


@pytest.mark.asyncio
async def test_mccn_balance(chaosnet_connector: ThorConnector):
    address = 'thor1q9vhc5zz8f097eyx7la4m35wsn7u3vds6sv9kg'
    balance = await chaosnet_connector.query_balance(address, consensus=False)
    # assert balance.height > 0  # no longer available
    assert balance.assets
    assert balance.runes == 341656201145
    assert balance.runes_float == 3416.56201145
    assert balance.address == address
    assert balance.assets

    synth_btc = balance.find_by_name('btc/btc')
    assert synth_btc.amount_float > 0
    assert synth_btc.asset == 'btc/btc'
