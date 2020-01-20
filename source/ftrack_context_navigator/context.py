# :coding: utf-8
# :copyright: Copyright (c) 2020 ftrack

import os
import re
import logging
import unicodedata
import ftrack_api


class Context(object):

    def __init__(self, session, execute_cb):
        self.illegal_character_substitute = ''
        self.execute_cb = execute_cb
        self.session = session
        self.logger = logging.getLogger(
            '{0}.{1}'.format(__name__, self.__class__.__name__)
        )

    def sanitise_for_filesystem(self, value):
        if self.illegal_character_substitute is None:
            return value

        if isinstance(value, str):
            value = value.decode('utf-8')

        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = value.replace(' ', '_')
        value = re.sub('([^a-zA-Z0-9._]+)', self.illegal_character_substitute, value)
        return unicode(value.strip().lower())

    def get_interface_name(self):
        '''Returns the name of this context interface.'''
        return 'ftrack'

    def get_root_context(self):
        '''Returns the root context where the plugin will be initialized.

        :returns: Initial context
        :rtype: list or str
        '''
        id = os.getenv('FTRACK_CONTEXTID', os.getenv('FTRACK_TASKID', os.getenv('FTRACK_SHOTID')))
        task = self.session.get('Context', id)
        hierarchy = [self.sanitise_for_filesystem(x['name']) for x in task['link']]
        self.logger.info('hierarchy :{}'.format(hierarchy))
        return hierarchy

    def get_context_data(self, hierarchy):
        '''From a hierarchy, extracts a data that will provide access to other
        functions as children or labels. Example: If this were to be an Ftrack
        interface an Ftrack object will be returned, if it was a FileSystem
        interface, a path will be returned.


        :param hierarchy: Hierarchy where to extract the data
        :type hierarchy: list

        :returns: An object that defines the current context
        :rtype: any
        '''
        query_str = 'Context where name is "%s"' % hierarchy[-1]


        # Build a query string of the form:
        parent_select = 'parent'
        for parent in reversed(hierarchy[:-1]):
            query_str += ' and {0}.name is "{1}"'.format(
                parent_select, parent
            )
            parent_select += '.parent'

        self.logger.debug(query_str)

        return self.session.query(query_str).first()

    def get_children(self, data):
        ''':param data: Data from the context to extact the children.
        :type data: any

        :returns: All the children of this entity
        :rtype: list of str
        '''
        result = [x['name'] for x in data['children']]

        if not result:
            tasks = self.session.query(
                'select name from Task where parent.id is {0}'.format(
                    data['id']
                )
            ).all()
            result = [x['name'] for x in tasks]

        return result

    def get_label(self, data):
        ''':param data: Data from the context to extact the label.
        :type data: any

        :returns: The label (what the user will see) of the entity.
        :rtype: str
        '''
        return data.get('full_name') or data['name']

    def execute(self, hierarchy):
        '''Executes the necessary logic to set the current context in a global
        scope.

        :param hierarchy: Hierarchy where to extract the data
        :type hierarchy: list
        '''
        obj = self.get_context_data(hierarchy)
        if obj.get('context_type') == 'task':
            # Update ftrack environment variables for the new context.
            # In ftrack, all three env vars point to the current task.
            os.environ['FTRACK_CONTEXTID'] = obj['id']
            os.environ['FTRACK_TASKID'] = obj['id']
            os.environ['FTRACK_SHOTID'] = obj['id']

        self.execute_cb(self.get_interface_name(), hierarchy, None)
        try:
            from ftrack_connect.connector import panelcom
            panelComInstance = panelcom.PanelComInstance.instance()
            panelComInstance.switchedShotListeners()
        except Exception:
            self.logger.warning('Ftrack connect does not seems to be installed.')

    def can_be_bookmark(self, hierarchy):
        ''':param hierarchy: Hierarchy where to extract the data
        :type hierarchy: list

        :returns: Whether the item corresponding to this hierarchy can be
            considered as a valid bookmark.
        :rtype: bool
        '''
        obj = self.get_context_data(hierarchy)
        return obj.get('context_type') == 'task'