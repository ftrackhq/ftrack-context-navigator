import sys
import os

import ftrack_api
import ftrack_connect.application


plugin_base_dir = os.path.normpath(
    os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        '..'
    )
)

resources_path = os.path.join(
    plugin_base_dir, 'resource'
)

python_dependencies = os.path.join(
    plugin_base_dir, 'dependencies'
)


def register_context_picker_common(event):
    this_dir = os.path.abspath(os.path.dirname(__file__))
    environment = event['data']['options']['env']

    interfaces_path = os.path.normpath(os.path.join(resources_path, "interfaces"))
    ftrack_connect.application.appendPath(
        interfaces_path,
        'PYTHONPATH',
        environment)

    ftrack_connect.application.appendPath(
        python_dependencies,
        'PYTHONPATH',
        environment)

    default_iface = 'ftrack'

    if 'EFESTO_CONTEXT_IFACE' not in environment:
        environment['EFESTO_CONTEXT_IFACE'] = default_iface


def register_maya_context_picker(event):
    register_context_picker_common(event)
    environment = event['data']['options']['env']

    maya_resources_path = os.path.normpath(os.path.join(resources_path, "maya"))
    ftrack_connect.application.appendPath(
        maya_resources_path,
        'PYTHONPATH',
        environment)

    ftrack_connect.application.appendPath(
        maya_resources_path,
        'MAYA_SCRIPT_PATH',
        environment)


def register_nuke_context_picker(event):
    # Filter out Nuke studio for now.
    if event['data']['application']['identifier'].startswith('nuke_studio'):
        return

    register_context_picker_common(event)

    this_dir = os.path.abspath(os.path.dirname(__file__))
    environment = event['data']['options']['env']

    nuke_resources_path = os.path.normpath(os.path.join(resources_path, "nuke"))

    ftrack_connect.application.appendPath(
        nuke_resources_path,
        'NUKE_PATH',
        environment
    )


def register(api_object, *kw):
    if not isinstance(api_object, ftrack_api.session.Session):
        return

    api_object.event_hub.subscribe(
        'topic=ftrack.connect.application.launch and data.application.identifier=maya*',
        register_maya_context_picker,
    )

    api_object.event_hub.subscribe(
        'topic=ftrack.connect.application.launch and data.application.identifier=nuke*',
        register_nuke_context_picker
    )
