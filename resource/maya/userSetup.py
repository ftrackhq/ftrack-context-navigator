
import maya

try:
    import efesto_context_navigator.mayactxpicker
    maya.utils.executeDeferred(efesto_context_navigator.mayactxpicker.main)
except:
    import traceback
    print traceback.format_exc()
