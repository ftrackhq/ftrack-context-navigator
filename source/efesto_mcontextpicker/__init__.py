from efesto_mcontextpicker import utils
from efesto_mcontextpicker import widgets
from efesto_mcontextpicker import context


def main(main_context):
    dock = utils.get_widget('efesto-ctxpick')
    if dock:
        dock.setParent(None)

    utils.hide_maya_help_button()
    ctx_manager = context.FtrackContextManager()
    dock = widgets.ContextDock(ctx_manager, main_context)
    utils.append_toolbox_widget(dock)
