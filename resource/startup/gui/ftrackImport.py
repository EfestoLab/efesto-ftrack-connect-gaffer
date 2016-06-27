# Copyright (c) 2016 Efesto Lab LTD.

import os
import sys
import logging
import ftrack
import functools
from PySide import QtCore, QtGui

import GafferUI
import GafferFtrack
import GafferFtrackUI

from ftrack_connect.ui.widget.import_asset import FtrackImportAssetDialog
from ftrack_connect.ui.widget.asset_manager import FtrackAssetManagerDialog

from ftrack_connect_gaffer.connector import Connector
from ftrack_connect_gaffer.ui.info import FtrackMayaInfoDialog
from ftrack_connect_gaffer.ui.publisher import PublishAssetDialog
from ftrack_connect_gaffer.ui.tasks import FtrackTasksDialog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ftrack.setup()

currentEntity = ftrack.Task(
	os.getenv('FTRACK_TASKID',
	os.getenv('FTRACK_SHOTID')))

'''
dialogs = [
	FtrackImportAssetDialog,
	functools.partial(
		PublishAssetDialog,
		currentEntity=currentEntity
	),
	'-----------------------',
	FtrackAssetManagerDialog,
	'-----------------------',
	FtrackMayaInfoDialog,
	FtrackTasksDialog
]
'''

connector = Connector()

def createAndShowFtrackDialog(Dialog):
	app = QtGui.QApplication.instance()
	qActiveWindow = app.activeWindow()
	# Find the GafferUI.Widget which owns that QWidget
	activeWindow = GafferUI.Widget._owner(qActiveWindow)

	if not isinstance(activeWindow, GafferUI.ScriptWindow):
		activeWindow = activeWindow.ancestor(GafferUI.ScriptWindow)

	parentWidget = activeWindow._qtWidget()
	print "*** parentWidget = ", parentWidget, ", type = ", type(parentWidget)
	print "*** parentParent = ", parentWidget.parent()

	ftrack_dialog = Dialog(parent=parentWidget, connector=connector)
	ftrack_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	ftrack_dialog.show()

def loadAndInit():

	logger.debug("Initializing Ftrack plugin...")
	connector.registerAssets()

	scriptWindowMenu = GafferUI.ScriptWindow.menuDefinition(application)

	scriptWindowMenu.append("/Ftrack/Import Asset", {
		"command" : functools.partial(createAndShowFtrackDialog, FtrackImportAssetDialog)})

	'''
	for Dialog in dialogs:
		if isinstance(Dialog, basestring):
			# todo: add separator here...
			continue

		widget_name = ftrack_dialog.windowTitle().replace('ftrack', '')

		logger.debug("Adding menu item for dialog: %s" % widget_name)
		scriptWindowMenu.append( "/Ftrack/" + widget_name, { "command" : ftrack_dialog.show } )
	'''

	nodeMenu.append(
		"/Ftrack/FtrackAbcImport",
		GafferFtrack.FtrackAbcImport,
		searchText="FtrackAbcImport"
	)

loadAndInit()
