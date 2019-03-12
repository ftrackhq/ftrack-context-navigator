

import nuke
import nukescripts

try:
    from efesto_context_navigator.nukectxpicker import NukeContextPickerPanelID, createContextPickerPanel, NukeContextPickerWidget
    nukescripts.registerPanel(NukeContextPickerPanelID, createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
