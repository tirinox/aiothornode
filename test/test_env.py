from aiothornode.env import MAINNET_ENVIRONMENT


def test_env_copy():
    env = MAINNET_ENVIRONMENT.copy()
    env.seed_url = 'lol'
    assert MAINNET_ENVIRONMENT.seed_url is not 'lol'

    env.set_timeout(1.25)
    assert env.timeout == 1.25
