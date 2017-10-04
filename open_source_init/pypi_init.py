import os

import six

from open_source_init.credentials import get_keyring_item
from open_source_init.travis_init import travis_encrypt, get_travis_data, set_travis_data


def _travis_pypi_init(full_travis_path, pyppi_username, repo_slug):
    pypi_password = get_keyring_item('pypi-{0}'.format(pyppi_username), 'PyPI password for {0}: '.format(pyppi_username))
    pypi_password = pypi_password.encode('utf-8') if isinstance(pypi_password, six.text_type) else pypi_password
    pypi_password = travis_encrypt(pypi_password, repo_slug)
    _write_to_travis_yaml(full_travis_path, pyppi_username, repo_slug, pypi_password)


def _write_to_travis_yaml(full_travis_path, pypi_username, repo_slug, pypi_password):
    deploy = {
        'provider': 'pypi',
        'distributions': 'sdist bdist_wheel',
        'user': pypi_username,
        'password': pypi_password,
        'on': {
            'tags': True,
            'repo': repo_slug
        }
    }
    travis_data = get_travis_data(full_travis_path)
    travis_data['deploy'] = deploy
    set_travis_data(full_travis_path, travis_data)


def pypi_init(full_travis_path, pypi_username, repo_slug, setup_py_path, pypi_registry):
    os.system('python {0} register -r {1} sdist'.format(setup_py_path, pypi_registry))
    _travis_pypi_init(full_travis_path, pypi_username, repo_slug)
