# -*- coding: utf-8 -*-

import os

import click

from open_source_init.credentials import get_keyring_item
from open_source_init.github_init import create_repo
from open_source_init.travis_init import coveralls_init, instantiate_travis_ci
from open_source_init.pypi_init import pypi_init


path_option = click.option('--path', type=str, default=os.getcwd(), help='The pypi to look up in your $HOME/.pypirc')
pypi_option = click.option('--pypi', type=str, default='pypi', help='The pypi to look up in your $HOME/.pypirc')
pypi_username_option = click.option('--pypi-username', type=str)
repo_option = click.option('-s', '--repo-slug', type=str, help='The repo slug in the form <owner>/<repo_name>')
repo_name_argument = click.argument('repo_name', type=str)


@click.group()
def cli():
    pass


@cli.command()
@repo_name_argument
@path_option
@pypi_option
@pypi_username_option
def all(repo_name, path, pypi, pypi_username):
    repo_slug = github(repo_name, path)
    travis(repo_slug)
    pypi(path, pypi, pypi_username, repo_slug)
    codecov(path)


@cli.command()
@path_option
@pypi_option
@pypi_username_option
@repo_option
def pypi(path, pypi, pypi_username, repo_slug):
    travis_yml_path = os.path.join(path, '.travis.yml')
    setup_py_path = os.path.join(path, 'setup.py')
    pypi_init(travis_yml_path, pypi_username, repo_slug, setup_py_path, pypi)


@cli.command()
@path_option
def codecov(path):
    travis_yml_path = os.path.join(path, '.travis.yml')
    coveralls_init(travis_yml_path)


@cli.command()
@repo_option
def travis(repo_slug):
    github_token = get_keyring_item('github-token', 'Github Token: ')
    instantiate_travis_ci(github_token, repo_slug)


@cli.command()
@repo_name_argument
@path_option
def github(repo_name, path):
    github_token = get_keyring_item('github-token', 'Github Token: ')
    return create_repo(github_token, repo_name, path)


if __name__ == "__main__":
    cli()
