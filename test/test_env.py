import pytest

from aiothornode.env import CHAOS_NET_BNB_ENVIRONMENT, TEST_NET_ENVIRONMENT_MULTI_1


def test_env_copy():
    env = CHAOS_NET_BNB_ENVIRONMENT.copy()
    env.seed_url = 'lol'
    assert CHAOS_NET_BNB_ENVIRONMENT.seed_url is not 'lol'

    with pytest.raises(AssertionError):
        env.set_consensus(0, 0)

    with pytest.raises(AssertionError):
        env.set_consensus(10, 5)

    env.set_consensus(1, 5)
    assert env.consensus_total == 5
    assert env.consensus_min == 1
