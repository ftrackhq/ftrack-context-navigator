
import os
import sys

from QtExt import QtGui, QtCore, QtWidgets

import nuke
import nukescripts

from efesto_mcontextpicker import interfaces
from efesto_mcontextpicker import widgets


def nuke_interface_execute_callback(interface_name, hierarchy, path):
    pass


class NukeContextPickerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NukeContextPickerWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(QtCore.Qt.AlignLeft)

        iface_name = os.getenv('EFESTO_CONTEXT_IFACE') or 'filesystem'
        if not iface_name:
            raise ValueError('No interface name specified.')

        iface = interfaces.get_interface(iface_name)

        ctx_manager = iface(nuke_interface_execute_callback)
        main_context = ctx_manager.get_root_context()

        ctx_picker = widgets.ContextDock(ctx_manager, main_context, 'nuke', parent)
        layout.addWidget(ctx_picker)

        spacer = QtWidgets.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.setLayout(layout)

    def event(self, evt):
        if evt.type() == QtCore.QEvent.Show:
            # Reset the margins of parent widget's layouts.
            self.__fixParentHierarchyMargins()

        super(NukeContextPickerWidget, self).event(evt)

    def __fixParentHierarchyMargins(self):
        # Go up the parent hierarchy of the widget,
        # setting the margins to 0 until we arrive to a QScrollArea.
        p = self
        while p != None:
            layout = p.layout()
            if layout:
                layout.setContentsMargins(0, 0, 0, 0)

            if isinstance(p, QtWidgets.QScrollArea):
                break

            p = p.parent()


NukeContextPickerPanelID = "com.efestolab.context_picker"

class NukeContextPickerPanel(nukescripts.PythonPanel):
    def __init__(self):
        super(NukeContextPickerPanel, self).__init__("CtxPicker", NukeContextPickerPanelID)
        self.customKnob = nuke.PyCustom_Knob(
            "CtxPicker",
            "",
            "__import__('nukescripts').panels.WidgetKnob(NukeContextPickerWidget)")
        self.addKnob(self.customKnob)


def createContextPickerPanel():
    ctxPickerPanel = NukeContextPickerPanel()
    return ctxPickerPanel.addToPane()
