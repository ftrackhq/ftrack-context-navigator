# :coding: utf-8
# :copyright: Copyright (c) 2020 ftrack

import nuke

try:
    from ftrack_context_navigator.nuke_navigator import createContextPickerPanel, NukeContextPickerWidget
    paneMenu = nuke.menu('Pane')
    paneMenu.addCommand('Context Navigator', createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
