from PySide import QtGui, QtCore
import resources
import re


class ContextDock(QtGui.QWidget):
    def __init__(self, ctx_manager, main_context, parent=None):
        super(ContextDock, self).__init__(parent=parent)
        self.setObjectName('efesto-ctxpick')
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(3)

        self.root_btn = RootButton(self)
        self.main_layout.addWidget(self.root_btn)

        self.button_widget = QtGui.QWidget(self)
        self.button_layout = QtGui.QVBoxLayout()
        self.button_widget.setLayout(self.button_layout)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(3)
        self.main_layout.addWidget(self.button_widget)

        self.buttons = []
        self.bookmarks = set()

        self.ctx_manager = ctx_manager
        if isinstance(main_context, basestring):
            self.get_button(0, main_context)
        elif isinstance(main_context, list):
            self.set_full_context(main_context)

        fileObject = QtCore.QFile(':/efesto/style')
        fileObject.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(fileObject)
        styleSheetContent = stream.readAll()

        self.setStyleSheet(styleSheetContent)

    def get_widget_index(self, widget):
        return self.button_layout.indexOf(widget)

    def get_widget_at(self, index):
        return self.button_layout.itemAt(index).widget()

    def create_button(self):
        btn = ContextButton(None, self)
        self.button_layout.addWidget(btn)
        self.buttons.append(btn)

        return btn

    def get_button(self, index, context):
        try:
            btn = self.buttons[index]
        except IndexError:
            btn = self.create_button()
        btn.update_ctx(context)
        btn.show()
        return btn

    def clamp_buttons(self, index):
        for i, btn in enumerate(self.buttons):
            if i > index:
                btn.hide()

    def get_widget_parents(self, widget):
        index = self.button_layout.indexOf(widget)
        hierarchy = []
        for i in range(index + 1):
            widget = self.button_layout.itemAt(i).widget()
            if isinstance(widget, RootButton):
                continue
            ctx = widget.ctx
            hierarchy.append(ctx)
        return hierarchy

    def execute(self, index):
        btn = self.button_layout.itemAt(index).widget()
        self.ctx_manager.execute(btn.hierarchy)
        if btn.build_menu_items() == 0:
            if not self.ctx_manager.can_be_bookmark(btn.hierarchy):
                return
            self.bookmarks.add(tuple(btn.hierarchy))
            self.root_btn.refresh_bookmarks()

    def set_full_context(self, hierarchy):
        for i, item in enumerate(hierarchy):
            self.get_button(i, item)

        self.execute(len(hierarchy) - 1)


class RootButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(RootButton, self).__init__(parent=parent)
        self.setMinimumHeight(34)
        self.setMinimumWidth(34)
        self.dock = parent
        self.build_bookmarks()
        self.clicked.connect(self.refresh_bookmarks)

    def build_bookmarks(self):
        self.bookmarks_menu = QtGui.QMenu(self)
        self.setMenu(self.bookmarks_menu)
        self.bookmarks_menu.triggered.connect(self.on_bookmark_action)

    def refresh_bookmarks(self):
        self.bookmarks_menu.clear()
        for i in self.dock.bookmarks:
            self.bookmarks_menu.addAction(':'.join(i))

    def on_bookmark_action(self, value):
        value = value.text()
        self.dock.set_full_context(value.split(':'))


class ContextButton(QtGui.QPushButton):
    def __init__(self, ctx=None, parent=None):
        super(ContextButton, self).__init__(parent=parent)
        self.setMinimumHeight(34)
        self.setMinimumWidth(34)

        self.setText(ctx)

        self.dock = parent
        self.ctx_manager = self.dock.ctx_manager

        self.ctx = None or ctx
        self.context_menu = QtGui.QMenu()
        self.context_menu.triggered.connect(self.on_menu_click)

    def __repr__(self):
        return '<btn %s>' % self.ctx

    def on_menu_click(self, value):
        current_index = self.dock.get_widget_index(self)
        parent = self.dock.get_button(current_index + 1, value.text())
        new_index = self.dock.get_widget_index(parent)
        self.dock.clamp_buttons(new_index)

        self.dock.execute(new_index)

    def update_ctx(self, ctx):
        self.ctx = ctx
        self.hierarchy = self.get_hierarchy()
        self._ctx_data = self.ctx_manager.get_context_data(self.hierarchy)
        label = self.ctx_manager.get_label(self._ctx_data)
        self.setToolTip(label)
        if len(label) > 5:
            items = re.findall(r'[a-zA-Z\d]+', label)
            seq = []
            for i in items:
                if i.isdigit():
                    seq.append(i)
                else:
                    seq.append(i[0].upper())

            seq = ''.join(seq)
            if len(seq) > 5:
                seq = seq[:4]
        else:
            seq = label
        self.setText(seq)

    def get_hierarchy(self):
        return self.dock.get_widget_parents(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            items = self.build_menu_items()
            if items:
                cursor = QtGui.QCursor()
                self.context_menu.exec_(cursor.pos())
        super(ContextButton, self).mousePressEvent(event)

    def build_menu_items(self):
        children = self.ctx_manager.get_children(self._ctx_data)
        self.context_menu.clear()

        for child in children:
            self.context_menu.addAction(child)
        return len(children)
