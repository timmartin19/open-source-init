from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from getpass import getpass
import keyring


def get_keyring_item(username, display, refresh=False):
    system = 'open-source-init'
    password = None
    if not refresh:
        password = keyring.get_password(system, username)
    if not password:
        password = getpass(display)
        keyring.set_password(system, username, password)
    return password
