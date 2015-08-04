from PySide import QtGui, QtCore
try:
    # Sphinx
    import resources
except:
    pass
import re


class ContextDock(QtGui.QWidget):
    def __init__(self, ctx_manager, main_context, parent=None):
        '''
        '''
        super(ContextDock, self).__init__(parent=parent)
        # Set object name to delete the plugin before when recreating it.
        self.setObjectName('efesto-ctxpick')
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(3)

        self.settings = QtCore.QSettings('EfestoLab', 'context_picker')
        self.bookmarks = set()

        size = self.settings.beginReadArray("bookmarks")
        for i in range(size):
            self.settings.setArrayIndex(i)
            self.bookmarks.add(tuple(self.settings.value("key")))

        self.settings.endArray()

        self.root_btn = RootButton(self)
        self.main_layout.addWidget(self.root_btn)

        self.button_widget = QtGui.QWidget(self)
        self.button_layout = QtGui.QVBoxLayout()
        self.button_widget.setLayout(self.button_layout)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(3)
        self.main_layout.addWidget(self.button_widget)

        self.buttons = []

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
        ''':param widget: Button to get the index in :class:`ContextDock`
        :type widget: :class:`PySide.QtGui.QWidget` base class.

        :returns: The index of the button or -1 if it's not in ContextDock
        :rtype: int
        '''
        return self.button_layout.indexOf(widget)

    def get_widget_at(self, index):
        ''':param index: Index where to retrieve the button
        :type index: int

        :returns: Widget located in the specified index.
        :rtype: :class:`ContextButton`
        '''
        return self.button_layout.itemAt(index).widget()

    def create_button(self):
        '''Creates a :class:`ContextButton` and adds it to the layout.

        :returns: The created button.
        :rtype: :class:`ContextButton`
        '''
        btn = ContextButton(None, self)
        self.button_layout.addWidget(btn)
        self.buttons.append(btn)

        return btn

    def get_button(self, index, context=None):
        '''Retrieves the button at the specified index. Also, it can set the
        context of that specific button if kwarg ``context`` is specified.

        :param index: Index of the button to be retrieved in self.buttons.
        :type index: int
        :param context: Context to apply to the button.
        :type context: str


        '''
        try:
            btn = self.buttons[index]
        except IndexError:
            btn = self.create_button()
        if context:
            btn.update_ctx(context)

        btn.show()
        return btn

    def clamp_buttons(self, index):
        '''Hides all buttons over the specified index.

        :param index: Any button over this value, will be hidden.
        :type index: int
        '''
        for i, btn in enumerate(self.buttons):
            if i > index:
                btn.hide()

    def get_widget_parent_context(self, widget):
        '''Get the parent context of a button.

        :param widget: Button to retrieve the parent context.
        :type widget: :class:`ContextButton`

        :returns: Context of the parent buttons.
        :rtype: list of str
        '''
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
        '''This definition will commit in a global scope the change in the
        button hierarchy, thus setting through the current context manager
        the change in the hierarchy.

        :param index: Index of the button to be executed.
        :type index: int
        '''
        btn = self.button_layout.itemAt(index).widget()
        self.ctx_manager.execute(btn.hierarchy)

        if not btn.build_menu_items() == 0:
            return
        if not self.ctx_manager.can_be_bookmark(btn.hierarchy):
            return

        self.bookmarks.add(tuple(btn.hierarchy))
        self.root_btn.refresh_bookmarks()
        self.settings.beginWriteArray("bookmarks")

        for idx, value in enumerate(self.bookmarks):
            self.settings.setArrayIndex(idx)
            self.settings.setValue("key", value)

        self.settings.endArray()

    def set_full_context(self, hierarchy):
        '''Creates a set of buttons based in a specified hierarchy. Clamps the
        rest of the buttons, which means that the only visible buttons will be
        the ones specified in the input hierarchy.

        :param hierarchy: Hierarchy to set the buttons to.
        :type hierarchy: list of str
        '''
        for i, item in enumerate(hierarchy):
            self.get_button(i, item)

        self.execute(len(hierarchy) - 1)
        self.clamp_buttons(len(hierarchy) - 1)


class RootButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        '''Button that will serve as bookmark holder and company identifier.
        '''
        super(RootButton, self).__init__(parent=parent)
        self.setMinimumHeight(34)
        self.setMinimumWidth(34)
        self.dock = parent
        self.build_bookmarks()
        self.clicked.connect(self.refresh_bookmarks)
        self.refresh_bookmarks()

    def build_bookmarks(self):
        '''Creates the menu and connects it to the button.
        '''
        self.bookmarks_menu = QtGui.QMenu(self)
        self.setMenu(self.bookmarks_menu)
        self.bookmarks_menu.triggered.connect(self.on_bookmark_action)

    def refresh_bookmarks(self):
        '''Refreshes the bookmarks on the current menu.
        '''
        self.bookmarks_menu.clear()
        for i in self.dock.bookmarks:
            self.bookmarks_menu.addAction(':'.join(i))

    def on_bookmark_action(self, value):
        '''Triggers :func:`ContextDock.set_full_context` based on the bookmark
        clicked value.

        '''
        value = value.text()
        self.dock.set_full_context(value.split(':'))


class ContextButton(QtGui.QPushButton):
    def __init__(self, ctx=None, parent=None):
        '''Button that will define one step of a context.

        :param ctx: Starting context
        :type ctx: str
        :param parent: Qt parent
        '''
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
        '''On click, this func will be triggered, a new button will be
        retrieved, the buttons will be clamped to the new spawned button,
        and the :func:`ContextDock.execute` will be executed with the new
        button as argument.
        '''
        current_index = self.dock.get_widget_index(self)
        parent = self.dock.get_button(current_index + 1, value.text())
        new_index = self.dock.get_widget_index(parent)
        self.dock.clamp_buttons(new_index)

        self.dock.execute(new_index)

    def update_ctx(self, ctx):
        '''Updates the context. Based on a string, the hierarchy will be
        extracted from :func:`ContextButton.get_hierarchy` and ``ctx`` input.
        The information in the button will be updated.

        :param ctx: Relative of the button
        :type ctx: str
        '''
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
        ''':returns: the hierarchy of itself, based on the buttons that precede
            ``self`` within the :class:`ContextDock` hierarchy.
        :rtype: list of str
        '''
        return self.dock.get_widget_parent_context(self)

    def mousePressEvent(self, event):
        '''Qt class override to spawn custom contextual menu.
        '''
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            items = self.build_menu_items()
            if items:
                cursor = QtGui.QCursor()
                self.context_menu.exec_(cursor.pos())
        super(ContextButton, self).mousePressEvent(event)

    def build_menu_items(self):
        '''Adds all children to its contextual menu.

        :returns: The number of children the button has.
        :rtype: int
        '''
        children = self.ctx_manager.get_children(self._ctx_data)
        self.context_menu.clear()

        for child in children:
            self.context_menu.addAction(child)
        return len(children)
