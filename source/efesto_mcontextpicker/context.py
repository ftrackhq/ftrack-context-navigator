import ftrack
import os


class FtrackContextManager(object):

    def get_context_object(self, hierarchy):
        obj = ftrack.getFromPath(hierarchy)
        return obj

    def get_children(self, obj):
        result = [x.getName() for x in obj.getChildren()]
        result = result or [x.getName() for x in obj.getTasks()]
        return result

    def get_label(self, obj):
        return obj.dict.get('fullname') or obj.getName()

    def apply_global_context(self, hierarchy):
        obj = self.get_context_object(hierarchy)
        if obj.dict.get('entityType') == 'task':
            os.environ['FTRACK_TASKID'] = obj.getId()
