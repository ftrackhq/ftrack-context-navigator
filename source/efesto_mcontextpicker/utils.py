from PySide import QtGui
from maya import OpenMayaUI as omui
from shiboken import wrapInstance


def get_widget(widget_name, query_type=None, wrapper=None):
    wrapper = wrapper or QtGui.QWidget

    _type_map = {
        'control': omui.MQtUtil.findControl,
        'layout': omui.MQtUtil.findLayout,
        'menu_item': omui.MQtUtil.findMenuItem,
        'window': omui.MQtUtil.findWindow,
    }

    _type = query_type or 'control'
    proc = _type_map.get(_type)
    ui_item = proc(widget_name)
    if not ui_item:
        return None
    ui_item = wrapInstance(long(ui_item), wrapper)

    return ui_item


def hide_maya_help_button():
    _id = 'mayaWebButton'
    widget = get_widget(_id)
    widget.hide()


def append_toolbox_widget(widget):
    layout_placeholder = get_widget('flowLayout2')
    layout_placeholder.layout().addWidget(widget)
