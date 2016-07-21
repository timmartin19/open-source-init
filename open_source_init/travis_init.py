from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import json

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from retrying import retry


try:
    from urllib import urlopen
except:
    from urllib.request import urlopen

from travispy import TravisPy
import yaml

from open_source_init.credentials import get_keyring_item


def instantiate_travis_ci(github_token, repo_slug):
    travis = TravisPy.github_auth(github_token)
    travis_user = travis.user()
    _instantiate_travis_retry_loop(travis, travis_user, repo_slug)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def _instantiate_travis_retry_loop(travis, travis_user, repo_slug):
    synced = travis_user.sync()
    assert synced, "Failed to sync github repos in Travis CI"
    repo = travis.repo(repo_slug)
    enabled = repo.enable()
    assert enabled, "Failed to enable repo {0}".format(repo_slug)



def get_travis_data(full_travis_path):
    with open(full_travis_path, mode='rb') as f:
        return yaml.safe_load(f.read())


def set_travis_data(full_travis_path, data):
    with open(full_travis_path, mode='wb') as f:
        f.write(yaml.dump(data).encode('utf-8'))


def travis_encrypt(data, repo):
    public_key = fetch_public_key(repo)
    return {b'secure': encrypt(public_key, data)}


def coveralls_init(full_travis_path):
    data = get_travis_data(full_travis_path)
    after_success = data.get(b'after_success', [])
    after_success.append(b'bash <(curl -s https://codecov.io/bash)')
    data[b'after_success'] = after_success
    set_travis_data(full_travis_path, data)



##############################
# Stolen from  https://github.com/audreyr/cookiecutter-pypackage
##############################
def load_key(pubkey):
    """Load public RSA key, with work-around for keys using
    incorrect header/footer format.

    Read more about RSA encryption with cryptography:
    https://cryptography.io/latest/hazmat/primitives/asymmetric/rsa/
    """
    try:
        return load_pem_public_key(pubkey.encode(), default_backend())
    except ValueError:
        # workaround for https://github.com/travis-ci/travis-api/issues/196
        pubkey = pubkey.replace('BEGIN RSA', 'BEGIN').replace('END RSA', 'END')
        return load_pem_public_key(pubkey.encode(), default_backend())


def encrypt(pubkey, password):
    """Encrypt password using given RSA public key and encode it with base64.

    The encrypted password can only be decrypted by someone with the
    private key (in this case, only Travis).
    """
    key = load_key(pubkey)
    encrypted_password = key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password)


def fetch_public_key(repo):
    """Download RSA public key Travis will use for this repo.

    Travis API docs: http://docs.travis-ci.com/api/#repository-keys
    """
    keyurl = 'https://api.travis-ci.org/repos/{0}/key'.format(repo)
    data = json.loads(urlopen(keyurl).read().decode())
    if 'key' not in data:
        errmsg = "Could not find public key for repo: {}.\n".format(repo)
        errmsg += "Have you already added your GitHub repo to Travis?"
        raise ValueError(errmsg)
    return data['key']
