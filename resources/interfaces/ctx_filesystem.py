
import sys
import os

from efesto_mcontextpicker.context import ContextInterface

try:
    import efesto_logger as logging
except:
    import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    level = logging.INFO if not os.getenv('EFESTO_DEBUG') else logging.DEBUG
    handler.setLevel(level)
    logger.addHandler(handler)


class FileSystemContextManager(ContextInterface):

    def __init__(self, execute_cb):
        super(FileSystemContextManager, self).__init__(execute_cb)

    def get_interface_name(self):
        return 'filesystem'

    def get_root_context(self):
        logger.info('Got main context: %s' % os.getcwd())
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
        path = os.path.join(*hierarchy)
        self.execute_cb(self.get_interface_name(), hierarchy, path)

    def can_be_bookmark(self, hierarchy):
        return 'workspace.mel' in os.listdir(os.path.join(*hierarchy))

IFACE = FileSystemContextManager
