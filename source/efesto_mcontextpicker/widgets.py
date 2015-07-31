from PySide import QtGui, QtCore
import re


class ContextDock(QtGui.QWidget):
    def __init__(self, ctx_manager, main_context, parent=None):
        super(ContextDock, self).__init__(parent=parent)
        self.setObjectName('efesto-ctxpick')
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.buttons = []
        self.current_level = 0

        self.ctx_manager = ctx_manager

        self.create_button(main_context)

    def get_button(self):
        if self.current_level + 1 > len(self.buttons) or not len(self.buttons):
            btn = ContextButton(None, self)

            self.main_layout.addWidget(btn)
            self.buttons.append(btn)
        else:
            btn = self.buttons[self.current_level]
            btn.show()

        return btn

    def create_button(self, context):
        btn = self.get_button()

        btn.update_ctx(context)

    def remove_button(self):
        for i, btn in enumerate(self.buttons):
            if i > self.current_level:
                btn.hide()

    def get_widget_parents(self, widget):
        index = self.main_layout.indexOf(widget)
        hierarchy = []
        for i in range(index + 1):
            ctx = self.main_layout.itemAt(i).widget().ctx
            hierarchy.append(ctx)
        return hierarchy

    def clamp_buttons(self, widget):
        self.remove_button()

    def set_level(self, widget):
        self.current_level = self.main_layout.indexOf(widget) + 1

    def set_context(self):
        btn = self.main_layout.itemAt(self.current_level).widget()
        self.ctx_manager.apply_global_context(btn.hierarchy)


class ContextButton(QtGui.QPushButton):
    def __init__(self, ctx=None, parent=None):
        super(ContextButton, self).__init__(parent=parent)
        self.setMinimumHeight(34)
        self.setMinimumWidth(34)

        self.setText(ctx)

        self.dock = parent
        self.ctx_manager = self.dock.ctx_manager

        self.ctx = None or ctx
        self.menu = QtGui.QMenu()
        self.menu.triggered.connect(self.on_menu_click)

    def __repr__(self):
        return '<btn %s>' % self.ctx

    def on_menu_click(self, value):
        self.dock.set_level(self)
        self.dock.create_button(value.text())
        self.dock.clamp_buttons(self)
        self.dock.set_context()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            items = self.build_menu_items()
            if items:
                cursor = QtGui.QCursor()
                self.menu.exec_(cursor.pos())
        super(ContextButton, self).mousePressEvent(event)

    def update_ctx(self, ctx):
        self.ctx = ctx
        self.hierarchy = self.get_hierarchy()
        self._ctx_object = self.ctx_manager.get_context_object(self.hierarchy)
        label = self.ctx_manager.get_label(self._ctx_object)
        self.setToolTip(label)
        items = re.findall(r"[a-zA-Z\d]+", label)
        seq = []
        for i in items:
            if i.isdigit():
                seq.append(i)
            else:
                seq.append(i[0].upper())

        seq = ''.join(seq)
        self.setText(seq)

    def get_hierarchy(self):
        return self.dock.get_widget_parents(self)

    def build_menu_items(self):
        children = self.ctx_manager.get_children(self._ctx_object)
        self.menu.clear()

        for child in children:
            self.menu.addAction(child)
        return len(children)
