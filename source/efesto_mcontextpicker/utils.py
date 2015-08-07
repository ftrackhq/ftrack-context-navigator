import os
import sys
from PySide import QtGui
try:
    # Sphinx
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance
except:
    pass

try:
    import efesto_logger as logging
except:
    import logging

logger = logging.getLogger(__name__)


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
    wrapper = wrapper or QtGui.QWidget

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


def discover_ifaces():
    '''Scans ``sys.path`` to retrieve any module starting with ``ctx_``. All
    modules found, will be stripped from the prefix and returned.

    :returns: All modules starting with ``ctx_``
    :rtype: list of str
    '''
    interfaces = []

    for path in sys.path:
        if not os.path.isdir(path):
            continue
        for module in os.listdir(path):
            if 'egg' in module or 'dist' in module:
                module = module.split('-')[0]
            module = module.split('.')[0]
            if module.startswith('ctx_'):
                module = module[4:]
                interfaces.append(module)

    logger.debug('Interfaces found %s' % interfaces)
    return interfaces


def import_module(module):
    '''Imports a module and returns it. If not found, ``None`` is returned.

    :param module: Name of the module to be imported.
    :type module: str

    :returns: A module
    :rtype: module or :py:class:`None`
    '''
    try:
        return __import__(module)
    except Exception as e:
        logger.warning('Could not import %s: %s' % (module, e))


def get_interface(name):
    '''Retrieves an interface. The interface has to be a module, it's name
    has to start with ``ctx_``, it has to be in the ``PYTHONPATH`` and it must
    contain a ``IFACE`` global variable which has to contain an uninitialized
    interface class. Raises :class:`ValueError` if not found.

    :param name: Name of the interface module to search.
    :type name: str

    :returns: Interface
    :rtype: :class:`efesto_mcontextpicker.context.ContextInterface` base class
    '''
    interfaces = discover_ifaces()
    if name not in interfaces:
        raise ValueError(
            'Interface ctx_%s could not be found in PYTHONPATH' % name
        )
    return import_module('ctx_%s' % name).IFACE
