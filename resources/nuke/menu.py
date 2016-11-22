
import nuke

try:
    from efesto_mcontextpicker.nukectxpicker import createContextPickerPanel, NukeContextPickerWidget
    paneMenu = nuke.menu('Pane')
    paneMenu.addCommand('Context Picker', createContextPickerPanel)
except:
    import traceback
    print traceback.format_exc()
