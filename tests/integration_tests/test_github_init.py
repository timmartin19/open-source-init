from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import random
import shutil
import string
import unittest

from env_config import get_envvar_configuration
from git import Repo
from github import Github

from open_source_init.github_init import _create_github_repo, _initial_commit, \
    _create_remote_and_push


class TestGithubInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = get_envvar_configuration('OPEN_SOURCE_INIT')
        cls.github_token = cls.config['GITHUB_TOKEN']
        cls.github = Github(cls.github_token)
        cls.user = cls.github.get_user()

    def setUp(self):
        self.repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp-repo')
        os.mkdir(self.repo_dir)
        self.create_filename = os.path.join(self.repo_dir, 'sample.txt')
        with open(self.create_filename, 'wb') as f:
            f.write(b'some text')

    def tearDown(self):
        shutil.rmtree(self.repo_dir)

    def test_create_repo(self):
        repo_name = ''.join([random.choice(string.ascii_letters) for i in range(20)])
        repo = _create_github_repo(self.github_token, repo_name)
        try:
            repo = self.user.get_repo(repo_name)
            self.assertIsNotNone(repo)
        finally:
            repo.delete()

    def test_initial_commit(self):
        start_wd = os.getcwd()
        repo = Repo.init(self.repo_dir)
        os.chdir(self.repo_dir)
        os.system('git config user.email "blah@blah.com"')
        os.system('git config user.name "Blah Blah"')
        os.chdir(start_wd)
        self.assertEqual(0, len(repo.branches))
        _initial_commit(self.repo_dir)
        self.assertEqual(start_wd, os.getcwd())
        self.assertIsNotNone(repo.branches[0].commit)

    # TODO Need to do special config
    # def test_create_remote_and_push(self):
    #     repo_name = ''.join([random.choice(string.ascii_letters) for i in range(20)])
    #     github_repo = _create_github_repo(self.github_token, repo_name)
    #     try:
    #         repo = Repo.init(self.repo_dir)
    #         _initial_commit(self.repo_dir)
    #         self.assertEqual(0, len(repo.remotes))
    #         _create_remote_and_push(repo, github_repo.ssh_url, force=True)
    #         self.assertEqual(1, len(repo.remotes))
    #     finally:
    #         github_repo.delete()
