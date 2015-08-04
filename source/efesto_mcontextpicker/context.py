class ContextInterface(object):
    def get_root_context(self):
        '''Returns the root context where the plugin will be initialized.

        :returns: Initial context
        :rtype: list or str
        '''
        raise NotImplementedError()

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
        raise NotImplementedError()

    def get_children(self, data):
        ''':param data: Data from the context to extact the children.
        :type data: any

        :returns: All the children of this entity
        :rtype: list of str
        '''
        raise NotImplementedError()

    def get_label(self, data):
        ''':param data: Data from the context to extact the label.
        :type data: any

        :returns: The label (what the user will see) of the entity.
        :rtype: str
        '''
        raise NotImplementedError()

    def execute(self, hierarchy):
        '''Executes the necessary logic to set the current context in a global
        scope.

        :param hierarchy: Hierarchy where to extract the data
        :type hierarchy: list
        '''
        raise NotImplementedError()

    def can_be_bookmark(self, hierarchy):
        ''':param hierarchy: Hierarchy where to extract the data
        :type hierarchy: list

        :returns: Whether the item corresponding to this hierarchy can be
            considered as a valid bookmark.
        :rtype: bool
        '''
        raise NotImplementedError()
