from .fixtures import *


@pytest.mark.asyncio
async def test_mccn_search_txs(chaosnet_connector: ThorConnector):
    results = await chaosnet_connector.query_native_tx_search("tx.height=1522004", page=1, per_page=2)
    assert results.total_count == 4
    assert len(results.txs) == 2


@pytest.mark.asyncio
async def test_mccn_block_txs_1(chaosnet_connector: ThorConnector):
    tx_hash = '0xE8510F9636377D66BEC8E263FBFE0B86C92CD3E801794BFFA553C5A9CA42CF09'
    tx = await chaosnet_connector.query_native_tx(tx_hash, consensus=False)
    assert tx.type == 'send'
    assert tx.hash == 'E8510F9636377D66BEC8E263FBFE0B86C92CD3E801794BFFA553C5A9CA42CF09'
    assert len(tx.transfers) == 2
    assert tx.transfers[0].amount == (2000000, 'rune')
    assert tx.transfers[0].recipient == 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
    assert tx.transfers[0].sender == 'thor179wpxmm5f7asaqwfwnnf8sn3rductlq3ywmrl0'
    assert tx.transfers[0].type == 'transfer'

    assert tx.transfers[1].amount == (4700000000, 'rune')


@pytest.mark.asyncio
async def test_mccn_block_txs_2(chaosnet_connector: ThorConnector):
    tx_hash = 'CE244B951949C3D54DD76C1DAB2FE83C535A1023AE1B9558CF6282AC2C157395'
    tx = await chaosnet_connector.query_native_tx(tx_hash, consensus=False)
    assert tx.type == 'send'
    assert tx.code == 0
    assert tx.height == 1568824
    assert tx.hash == 'CE244B951949C3D54DD76C1DAB2FE83C535A1023AE1B9558CF6282AC2C157395'
