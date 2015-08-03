import os
import subprocess
import sys
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

setup(
    packages=find_packages(source_dir),
    package_dir={
        '': 'source'
    },
    cmdclass={
        'build': Build,
    }
)
