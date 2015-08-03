class ContextInterface(object):
    def get_root_context(self):
        raise NotImplementedError()

    def get_context_data(self, hierarchy):
        raise NotImplementedError()

    def get_children(self, data):
        raise NotImplementedError()

    def get_label(self, data):
        raise NotImplementedError()

    def execute(self, hierarchy):
        raise NotImplementedError()

    def can_be_bookmark(self, hierarchy):
        raise NotImplementedError()
