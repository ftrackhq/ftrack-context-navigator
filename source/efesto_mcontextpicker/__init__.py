import os
from efesto_mcontextpicker import utils
from efesto_mcontextpicker import widgets


def main(iface_name='filesystem', main_context=None):
    ''':param iface_name: Name of the interface. This name will be searched as
        ``ctx_<name>`` in the ``PYTHONPATH``, and if found, will be used as
        interface.

    :type iface_name: str

    :param main_context: Force specify the context where the dock will be
        initialized. If this value is not specified, the interface will run
        :func:`efesto_mcontextpicker.context.ContextInterface.get_root_context`
        to retrieve it.
    :type main_context: str

    '''
    dock = utils.get_widget('efesto-ctxpick')
    if dock:
        dock.setParent(None)

    utils.hide_maya_help_button()

    iface_name = os.getenv('EFESTO_CONTEXT_IFACE') or iface_name
    if not iface_name:
        raise ValueError('No interface name specified.')

    iface = utils.get_interface(iface_name)

    ctx_manager = iface()
    main_context = main_context or ctx_manager.get_root_context()

    dock = widgets.ContextDock(ctx_manager, main_context)
    utils.append_toolbox_widget(dock)
