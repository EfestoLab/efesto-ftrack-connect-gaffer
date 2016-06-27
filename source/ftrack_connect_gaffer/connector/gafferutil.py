
from PySide import QtGui

import GafferUI

def getScriptNode():
    # Use raw Qt to find the active window
    app = QtGui.QApplication.instance()
    qActiveWindow = app.activeWindow()
    # Find the GafferUI.Widget which owns that QWidget
    activeWindow = GafferUI.Widget._owner(qActiveWindow)

    if not isinstance(activeWindow, GafferUI.ScriptWindow):
        activeWindow = activeWindow.ancestor(GafferUI.ScriptWindow)

    return activeWindow.scriptNode()
