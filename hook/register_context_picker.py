import ftrack
import sys
import os


def _append_to_env_path(event, env_var, path):
    if env_var in event['data']['options']['env']:
        old_path = event['data']['options']['env'][env_var]
        event['data']['options']['env'][env_var] = os.pathsep.join([old_path, path])
    else:
        event['data']['options']['env'][env_var] = path

def _is_fstructure_in_python_path(event):
    python_paths = event['data']['options']['env']['PYTHONPATH'].split(os.pathsep)
    print python_paths

    # todo: a more robust (and slower) solution would be check if a specific file
    # from fstructure i.e. mayadefaultstructure.py exists.
    for path in python_paths:
        test_file = os.path.join(path, "efesto_fstructure", "mayadefaultstructure.py")
        print "Checking if %s exists" % test_file
        if os.path.exists(test_file):
            print "***Structure plugin found***"
            return True

    return False

def register_context_picker(event):
    print "Registering context picker!!"

    this_dir = os.path.abspath(os.path.dirname(__file__))
    interfaces_path = os.path.normpath(os.path.join(this_dir, "..", "resources", "interfaces"))
    _append_to_env_path(event, 'PYTHONPATH', interfaces_path)

    maya_resources_path = os.path.normpath(os.path.join(this_dir, "..", "resources", "maya"))
    _append_to_env_path(event, 'PYTHONPATH', maya_resources_path)
    _append_to_env_path(event, 'MAYA_SCRIPT_PATH', maya_resources_path)

    source_path = os.path.normpath(os.path.join(this_dir, '..', 'source'))
    _append_to_env_path(event, 'PYTHONPATH', source_path)

    if _is_fstructure_in_python_path(event):
        default_iface = 'ftrack'
    else:
        default_iface = 'filesystem'

    _append_to_env_path(
        event,
        'EFESTO_CONTEXT_IFACE',
        os.getenv('EFESTO_CONTEXT_IFACE', default_iface)
    )

def register(registry, *kw):
    if registry is not ftrack.EVENT_HANDLERS:
        return

    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        register_context_picker,
    )
