import ftrack
import sys
import os


def register(registry, **kwargs):
    if registry is not ftrack.EVENT_HANDLERS:
        return

    this_dir = os.path.abspath(os.path.dirname(__file__))
    interfaces_path = os.path.join(this_dir, "..", "resources", "interfaces")
    maya_resources_path = os.path.join(this_dir, "..", "resources", "maya")
    source_path = os.path.join(this_dir, '..', 'source')

    old_python_path = os.environ.get('PYTHONPATH', '')
    os.environ['PYTHONPATH'] = os.pathsep.join([old_python_path, interfaces_path, maya_resources_path, source_path])

    old_maya_script_path = os.environ.get('MAYA_SCRIPT_PATH', '')
    os.environ['MAYA_SCRIPT_PATH'] = os.pathsep.join([old_maya_script_path, maya_resources_path])

    os.environ['EFESTO_CONTEXT_IFACE'] = 'ftrack'
