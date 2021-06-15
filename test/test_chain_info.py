from typing import Dict

from aiothornode.types import ThorChainInfo
from .fixtures import *


def assert_chains_ok(chain_dic: Dict[str, ThorChainInfo], multi):
    assert len(chain_dic) >= 1
    address_set = set()
    for c in chain_dic.values():
        assert len(c.chain) >= 3
        assert c.chain.upper() == c.chain
        assert len(c.pub_key) > 30
        assert c.pub_key.startswith('tthor') or c.pub_key.startswith('thor')
        if multi:
            assert c.gas_rate > 0
        else:
            assert c.gas_rate >= 0
        if c.chain == 'ETH':
            assert len(c.router) > 20

        assert len(c.address) > 10

        address_set.add(c.address)

        assert not c.halted  # I hope you test it when it is not halted, otherwise why are you even doing it?

    assert len(address_set) == len(chain_dic)


@pytest.mark.asyncio
async def test_mccn_chains(chaosnet_connector: ThorConnector):
    chain_dic = await chaosnet_connector.query_chain_info()
    assert_chains_ok(chain_dic, multi=True)


@pytest.mark.asyncio
async def test_sccn_chains(sc_chaosnet_connector: ThorConnector):
    chain_dic = await sc_chaosnet_connector.query_chain_info()
    assert_chains_ok(chain_dic, multi=False)
