from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from open_source_init.credentials import get_keyring_item
from open_source_init.travis_init import travis_encrypt, get_travis_data, set_travis_data


def _travis_pypi_init(full_travis_path, pyppi_username, repo_slug):
    conditions = {b'tags': True, b'repo': repo_slug.encode('utf-8')}
    pypi_password = get_keyring_item('pypi-{0}'.format(pyppi_username), 'PyPI password for {0}: '.format(pyppi_username))
    pypi_password = travis_encrypt(pypi_password.encode('utf-8'), repo_slug)
    deploy = {
        b'provider': b'pypi',
        b'distributions': b'sdist bdist_wheel',
        b'user': pyppi_username.encode('utf-8'),
        b'password': pypi_password,
        b'on': conditions
    }
    travis_data = get_travis_data(full_travis_path)
    travis_data['deploy'] = deploy
    set_travis_data(full_travis_path, travis_data)


def pypi_init(full_travis_path, pypi_username, repo_slug, setup_py_path, pypi_registry):
    os.system('python {0} register -r {1} sdist'.format(setup_py_path, pypi_registry))
    _travis_pypi_init(full_travis_path, pypi_username, repo_slug)
