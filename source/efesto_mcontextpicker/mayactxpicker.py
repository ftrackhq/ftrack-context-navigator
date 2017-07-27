
import os
import sys

import logging
logger = logging.getLogger(__name__)

from QtExt import QtGui, QtWidgets
from maya import OpenMayaUI as omui

try:
    # pyside
    from shiboken import wrapInstance
except:
    # pyside2
    from shiboken2 import wrapInstance

from efesto_mcontextpicker import interfaces
from efesto_mcontextpicker import widgets


def get_widget(widget_name, query_type=None, wrapper=None):
    '''Retrieve the widget within Maya based in it's objectName.

    :param widget_name: The objectName of the widget to retrieve.
    :type widget_name: str
    :param query_type: Method to retrieve the widget, based in all Maya
        methods to retrieve them. Valid types are **control**
        (``MQtUtil.findControl``), **layout** (``MQtUtil.findLayout``),
        **menu_item** (``MQtUtil.findMenuItem``) or **window**
        (``MQtUtil.findWindow``).
    :type query_type: str
    :param wrapper: Object where to wrap the retrieved widget. By default is
        :class:`PySide.QtGui.QWidget`.
    :type wrapper: :class:`PySide.QtCore.QObject` based class.

    :returns: An instance of ``wrapper`` with objectName ``widget_name``

    '''
    wrapper = wrapper or QtWidgets.QWidget

    logger.debug('Retrieving widget "%s"' % widget_name)

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
    '''Hides Maya Toolbox help button.
    '''
    logger.debug('Hiding Maya help button.')
    widget = get_widget('mayaWebButton')
    widget.hide()


def append_toolbox_widget(widget):
    '''Appends a widget to Maya's Toolbox.

    :param widget: Widget to append to Maya's Toolbox
    :type widget: :class:`PySide.QtGui.QWidget` based class.
    '''

    logger.debug('Appending "%s" to Maya Toolbox' % widget.objectName())
    layout_placeholder = get_widget('flowLayout2')
    layout_placeholder.layout().addWidget(widget)


def maya_interface_execute_callback(interface_name, hierarchy, path):
    if interface_name == 'ftrack':
        from efesto_fstructure.mayadefaultstructure import set_maya_project
        set_maya_project()
    elif interface_name == 'filesystem':
        import os
        import maya.mel as mel
        if 'workspace.mel' in os.listdir(path):
            mel.eval('setProject "%s"' % path)
    else:
        raise RuntimeError("Unknown ctx navigator interface type %s" % interface_name)


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
    dock = get_widget('efesto-ctxpick')
    if dock:
        dock.setParent(None)

    hide_maya_help_button()

    iface_name = os.getenv('EFESTO_CONTEXT_IFACE') or iface_name
    if not iface_name:
        raise ValueError('No interface name specified.')

    iface = interfaces.get_interface(iface_name)

    ctx_manager = iface(maya_interface_execute_callback)
    main_context = main_context or ctx_manager.get_root_context()

    dock = widgets.ContextDock(ctx_manager, main_context, 'maya')
    append_toolbox_widget(dock)
