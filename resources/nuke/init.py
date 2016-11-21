

import nuke
import nukescripts

try:
    from efesto_mcontextpicker.nukectxpicker import NukeContextPickerPanelID, createContextPickerPanel, NukeContextPickerWidget
    nukescripts.registerPanel(NukeContextPickerPanelID, createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
