import pytest

from aiothornode.env import MAINNET_ENVIRONMENT


def test_env_copy():
    env = MAINNET_ENVIRONMENT.copy()
    env.seed_url = 'lol'
    assert MAINNET_ENVIRONMENT.seed_url is not 'lol'

    with pytest.raises(AssertionError):
        env.set_consensus(0, 0)

    with pytest.raises(AssertionError):
        env.set_consensus(10, 5)

    env.set_consensus(1, 5)
    assert env.consensus_total == 5
    assert env.consensus_min == 1
