import os
from efesto_mcontextpicker.context import ContextInterface


class FileSystemContextManager(ContextInterface):
    def get_root_context(self):
        return os.getcwd()

    def get_context_data(self, hierarchy):
        return os.path.join(*hierarchy)

    def get_children(self, data):
        children = os.listdir(data)
        if 'workspace.mel' in children:
            return []
        children = [
            x for x in children if os.path.isdir(os.path.join(data, x))
        ]
        return children

    def get_label(self, data):
        return os.path.split(data)[-1]

    def execute(self, hierarchy):
        import maya.mel as mel
        path = os.path.join(*hierarchy)
        if 'workspace.mel' in os.listdir(path):
            print 'setProject "%s"' % path
            mel.eval('setProject "%s"' % path)

    def can_be_bookmark(self, hierarchy):
        return 'workspace.mel' in os.listdir(os.path.join(*hierarchy))

IFACE = FileSystemContextManager
