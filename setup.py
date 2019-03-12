# :coding: utf-8
# :copyright: Copyright (c) 2019 ftrack


import os
import re
import shutil
from pip._internal import main as pip_main

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import setuptools

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')


HOOK_PATH = os.path.join(
    ROOT_PATH, 'hook'
)

RESOURCE_PATH = os.path.join(
    ROOT_PATH, 'resource'
)

BUILD_PATH = os.path.join(
    ROOT_PATH, 'build'
)


# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'efesto_context_navigator', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)

STAGING_PATH = os.path.join(
    BUILD_PATH, 'efesto-context-navigator-{}'.format(VERSION)
)


class BuildPlugin(setuptools.Command):
    '''Build plugin.'''

    description = 'Download dependencies and build plugin .'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Run the build step.'''
        # Clean staging path
        shutil.rmtree(STAGING_PATH, ignore_errors=True)

        # Copy resource files
        shutil.copytree(
            RESOURCE_PATH,
            os.path.join(STAGING_PATH, 'resource')
        )

        # Copy hook files
        shutil.copytree(
            HOOK_PATH,
            os.path.join(STAGING_PATH, 'hook')
        )

        pip_main(
            [
                'install',
                '.',
                '--target',
                os.path.join(STAGING_PATH, 'dependencies'),
                '--process-dependency-links'
            ]
        )

        result_path = shutil.make_archive(
            os.path.join(
                BUILD_PATH,
                'efesto-context-navigator-{0}'.format(VERSION)
            ),
            'zip',
            STAGING_PATH
        )


# Custom commands.
class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


setup(
    name='efesto-context-navigator',
    version=VERSION,
    description='Efesto context navigator.',
    url='http://www.efestolab.uk/',
    author='EfestoLab LTD',
    author_email='info@efestolab.uk',
    packages=find_packages(SOURCE_PATH),
    setup_requires=[
        'qtext',
    ],
    install_requires=[
        'qtext'
    ],
    dependency_links=[
        'git+https://bitbucket.org/ftrack/qtext/get/0.1.0.zip#egg=QtExt-0.1.0'
    ],
    package_dir={
        '': 'source'
    },
    cmdclass={
        'test': PyTest,
        'build_plugin': BuildPlugin
    },
)
