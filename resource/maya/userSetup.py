
import maya

try:
    import efesto_context_navigator.maya_navigator
    maya.utils.executeDeferred(efesto_context_navigator.maya_navigator.main)
except:
    import traceback
    print traceback.format_exc()
