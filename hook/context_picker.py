import ftrack
import sys
import os

def register(registry, **kwargs):
    if registry is not ftrack.EVENT_HANDLERS:
        return

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    interfaces_path = os.path.abspath('../resources/interfaces')
    resources_maya_path = os.path.abspath('../resources/maya')
    source_code = os.path.abspath('../source')

    old_python_path = os.environ.get('PYTHONPATH', '')
    os.environ['PYTHONPATH'] = os.pathsep.join([old_python_path, interfaces_path, resources_maya_path, source_code])

    old_maya_script_path = os.environ.get('MAYA_SCRIPT_PATH', '')
    os.environ['MAYA_SCRIPT_PATH'] = os.pathsep.join([old_maya_script_path, resources_maya_path])

    os.environ['EFESTO_CONTEXT_IFACE'] = 'ftrack'


