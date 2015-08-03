import os
from efesto_mcontextpicker import utils
from efesto_mcontextpicker import widgets


def main(main_context=None, iface_name='filesystem'):
    dock = utils.get_widget('efesto-ctxpick')
    if dock:
        dock.setParent(None)

    utils.hide_maya_help_button()

    iface_name = os.getenv('EFESTO_CONTEXT_IFACE') or iface_name
    if not iface_name:
        raise ValueError('A')

    iface = utils.InterfacePicker.get(iface_name)

    ctx_manager = iface()
    main_context = main_context or ctx_manager.get_root_context()

    dock = widgets.ContextDock(ctx_manager, main_context)
    utils.append_toolbox_widget(dock)
