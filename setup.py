#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyGithub',
    'PyYaml',
    'TravisPy',
    'cryptography',
    'gitpython',
    'keyring',
    'py-env-config',
    'requests',
    'retrying'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='open-source-init',
    version='0.1.0',
    description="A tool to automatically create a github repo, integrate travis, code coverage, read the docs, and everything else necessary for OSS development",
    long_description=readme + '\n\n' + history,
    author="Tim Martin",
    author_email='tim@timmartin.me',
    url='https://github.com/timmartin19/open_source_init',
    packages=[
        'open_source_init',
    ],
    package_dir={'open_source_init':
                 'open_source_init'},
    entry_points={
        'console_scripts': [
            'open_source_init=open_source_init.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='open_source_init',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
