#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_open_source_init
----------------------------------

Tests for `open_source_init` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from open_source_init import open_source_init
from open_source_init import cli



class TestOpen_source_init(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'open_source_init.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())
