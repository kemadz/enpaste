from enpaste.config import TestConfig
import enpaste.oauth
import os


conf = TestConfig()
fp = os.path.join(os.getenv('HOME'), '.enpaste')


def test_oauth_token_no_default():
    try:
        os.unlink(fp)
    except:
        pass
    assert enpaste.oauth.get_access_token_via_oauth(conf).startswith('S')


def test_oauth_token_with_default():
    try:
        with open(fp) as fr:
            token = fr.read().strip()
    except:
        token = None

    assert token == enpaste.oauth.get_access_token_via_oauth(conf)
