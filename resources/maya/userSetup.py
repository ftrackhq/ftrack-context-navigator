import maya
try:
    import efesto_mcontextpicker
    maya.utils.executeDeferred(efesto_mcontextpicker.main)
except:
    import traceback
    print traceback.format_exc()
