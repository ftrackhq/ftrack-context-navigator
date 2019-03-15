import nuke

try:
    from ftrack_context_navigator.nuke_navigator import createContextPickerPanel, NukeContextPickerWidget
    paneMenu = nuke.menu('Pane')
    paneMenu.addCommand('Context Picker', createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
