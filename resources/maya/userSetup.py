
import maya

try:
    import efesto_mcontextpicker.mayactxpicker
    maya.utils.executeDeferred(efesto_mcontextpicker.mayactxpicker.main)
except:
    import traceback
    print traceback.format_exc()
