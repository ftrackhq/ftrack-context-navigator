# :coding: utf-8
# :copyright: Copyright (c) 2020 ftrack

import nuke
import nukescripts

try:
    from ftrack_context_navigator.nuke_navigator import NukeContextPickerPanelID, createContextPickerPanel, NukeContextPickerWidget
    nukescripts.registerPanel(NukeContextPickerPanelID, createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
