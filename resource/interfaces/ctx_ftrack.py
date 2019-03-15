
import os

from ftrack_context_navigator.context import ContextInterface


class FtrackContextManager(ContextInterface):

    def __init__(self, execute_cb):
        super(FtrackContextManager, self).__init__(execute_cb)
        import ftrack_api
        self.session = ftrack_api.Session()

    def get_interface_name(self):
        return 'ftrack'

    def get_root_context(self):
        import ftrack_api
        id = os.getenv('FTRACK_CONTEXTID', os.getenv('FTRACK_TASKID', os.getenv('FTRACK_SHOTID')))
        task = self.session.get('Context', id)
        hierarchy = [x['name'] for x in task['link']]
        return hierarchy

    def get_context_data(self, hierarchy):
        import ftrack_api
        query_str = 'Context where name is "%s"' % hierarchy[-1]

        # Build a query string of the form:
        parent_select = 'parent'
        for parent in reversed(hierarchy[:-1]):
            query_str += ' and {0}.name is "{1}"'.format(
                parent_select, parent
            )
            parent_select += '.parent'

        return self.session.query(query_str).one()

    def get_children(self, obj):
        result = [x['name'] for x in obj['children']]

        if not result:
            tasks = self.session.query(
                'select name from Task where parent.id is {0}'.format(obj['id'])).all()
            result = [x['name'] for x in tasks]

        return result

    def get_label(self, obj):
        return obj.get('full_name') or obj['name']

    def can_be_bookmark(self, hierarchy):
        obj = self.get_context_data(hierarchy)
        return obj.get('context_type') == 'task'

    def execute(self, hierarchy):
        from ftrack_connect.connector import panelcom

        obj = self.get_context_data(hierarchy)
        if obj.get('context_type') == 'task':
            # Update ftrack environment variables for the new context.
            # In ftrack, all three env vars point to the current task.
            os.environ['FTRACK_CONTEXTID'] = obj['id']
            os.environ['FTRACK_TASKID'] = obj['id']
            os.environ['FTRACK_SHOTID'] = obj['id']

        self.execute_cb(self.get_interface_name(), hierarchy, None)

        panelComInstance = panelcom.PanelComInstance.instance()
        panelComInstance.switchedShotListeners()

IFACE = FtrackContextManager
