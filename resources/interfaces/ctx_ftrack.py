import os
from efesto_mcontextpicker.context import ContextInterface


class FtrackContextManager(ContextInterface):

    def get_root_context(self):
        import ftrack
        task = ftrack.Task(
            os.getenv(
                'FTRACK_TASKID',
                os.getenv(
                    'FTRACK_SHOTID'
                )
            )
        )
        hierarchy = [x.getName() for x in task.getParents()]
        hierarchy.reverse()
        hierarchy.append(task.getName())
        return list(hierarchy)

    def get_context_data(self, hierarchy):
        import ftrack
        obj = ftrack.getFromPath(hierarchy)
        return obj

    def get_children(self, obj):
        result = [x.getName() for x in obj.getChildren()]
        result = result or [x.getName() for x in obj.getTasks()]
        return result

    def get_label(self, obj):
        return obj.dict.get('fullname') or obj.getName()

    def can_be_bookmark(self, hierarchy):
        obj = self.get_context_data(hierarchy)
        return obj.dict.get('entityType') == 'task'

    def execute(self, hierarchy):
        try:
            from ftrackplugin.ftrackConnector import panelcom
        except:
            from ftrack_connect.connector import panelcom

        obj = self.get_context_data(hierarchy)
        if obj.dict.get('entityType') == 'task':
            os.environ['FTRACK_TASKID'] = obj.getId()
            os.environ['FTRACK_SHOTID'] = obj.getParent().getId()

        panelComInstance = panelcom.PanelComInstance.instance()
        panelComInstance.switchedShotListeners()

IFACE = FtrackContextManager
