import sys
import os

import ftrack
import ftrack_connect.application


def _is_fstructure_in_python_path(event):
    python_paths = event['data']['options']['env']['PYTHONPATH'].split(os.pathsep)

    # look for efesto_fstructure/mayadefaultstructure.py on PYTHONPATH
    for path in python_paths:
        test_file = os.path.join(path, "efesto_fstructure", "mayadefaultstructure.py")
        if os.path.exists(test_file):
            print "***Structure plugin found***"
            return True

    print "***Structure plugin NOT found***"
    return False

def register_context_picker(event):
    print "Registering context picker!!"

    this_dir = os.path.abspath(os.path.dirname(__file__))
    environment = event['data']['options']['env']

    interfaces_path = os.path.normpath(os.path.join(this_dir, "..", "resources", "interfaces"))
    ftrack_connect.application.appendPath(
        interfaces_path,
        'PYTHONPATH',
        environment)

    maya_resources_path = os.path.normpath(os.path.join(this_dir, "..", "resources", "maya"))
    ftrack_connect.application.appendPath(
        maya_resources_path,
        'PYTHONPATH',
        environment)
    ftrack_connect.application.appendPath(
        maya_resources_path,
        'MAYA_SCRIPT_PATH',
        environment)

    source_path = os.path.normpath(os.path.join(this_dir, '..', 'source'))
    ftrack_connect.application.appendPath(
        source_path,
        'PYTHONPATH',
        environment)

    if _is_fstructure_in_python_path(event):
        default_iface = 'ftrack'
    else:
        default_iface = 'filesystem'

    ftrack_connect.application.appendPath(
        os.getenv('EFESTO_CONTEXT_IFACE', default_iface),
        'EFESTO_CONTEXT_IFACE',
        environment)

def register(registry, *kw):
    if registry is not ftrack.EVENT_HANDLERS:
        return

    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        register_context_picker,
    )
