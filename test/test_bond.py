import pytest

from .fixtures import *


async def do_checks(connector: ThorConnector):
    nodes = await connector.query_node_accounts()
    n = len(nodes)
    assert n >= 3
    n_with_bond = sum(1 for n in nodes if n.bond > 0)
    assert n_with_bond >= 0.3 * n

    n_with_node_op_addr = sum(1 for n in nodes if n.bond_address)
    assert n_with_node_op_addr >= 0.3 * n


@pytest.mark.asyncio
async def test_bond_mainnet(mainnet_connector: ThorConnector):
    await do_checks(mainnet_connector)


@pytest.mark.asyncio
async def test_bond_stagent(stagenet_connector: ThorConnector):
    await do_checks(stagenet_connector)
