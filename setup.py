import os
import subprocess
import sys
import fileinput
from setuptools import setup, find_packages
from distutils.command.build import build

root_dir = os.path.dirname(__file__)
source_dir = os.path.join(root_dir, 'source')
resource_file = os.path.join(root_dir, 'resources', 'ui', 'resource.qrc')
resource_file_dest = os.path.join(
    source_dir,
    'efesto_mcontextpicker',
    'resources.py'
)


class Build(build):

    def _replace_imports_(self, destination):
        replace = 'from QtExt import QtCore'
        for line in fileinput.input(destination, inplace=True):
            if 'import QtCore' in line:
                print line.replace(line, replace)
            else:
                print line

    def run(self):
        pyside_rcc_command = 'pyside-rcc'
        if sys.platform == 'win32':
            import PySide
            pyside_rcc_command = os.path.join(
                os.path.dirname(PySide.__file__),
                'pyside-rcc.exe'
            )

        subprocess.check_call([
            pyside_rcc_command,
            '-o',
            resource_file_dest,
            resource_file
        ])

        build.run(self)
        self.replace__imports_(resource_file)


setup(
    name='efesto-mcontextpicker',
    version='0.1.0',
    description='Maya context picker.',
    url='http://www.efestolab.uk/',
    author='EfestoLab LTD',
    author_email='info@efestolab.uk',
    packages=find_packages(source_dir),
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
        'build': Build,
    },
)
