# :coding: utf-8
# :copyright: Copyright (c) 2020 ftrack

import maya

try:
    import ftrack_context_navigator.maya_navigator
    maya.utils.executeDeferred(ftrack_context_navigator.maya_navigator.main)
except:
    import traceback
    print traceback.format_exc()
