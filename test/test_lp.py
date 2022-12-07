import pytest

from .fixtures import *


@pytest.mark.asyncio
async def test_providers(mainnet_connector: ThorConnector):
    def subtest_providers(providers, is_savers):
        assert len(providers) > 0
        if is_savers:
            assert all(p.rune_deposit_value == 0 for p in providers)
        else:
            assert any(p.pending_tx_id for p in providers)
        assert all(p.rune_address or p.asset_address for p in providers)
        assert any(p.asset_deposit_value > 0 or p.rune_deposit_value > 0 for p in providers)
        assert all(p.last_add_height > 0 for p in providers)
        assert all(
            p.units > 0 or ((p.pending_rune > 0 or p.pending_asset > 0) and p.pending_tx_id) for p in providers)
        assert any(p.last_withdraw_height > 0 for p in providers)

    liq_providers = await mainnet_connector.query_liquidity_providers('BTC.BTC')
    subtest_providers(liq_providers, False)

    savers = await mainnet_connector.query_savers('BTC.BTC')
    subtest_providers(savers, True)
