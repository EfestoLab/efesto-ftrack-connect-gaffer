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

connector = Connector()

def createAndShowFtrackDialog(Dialog, menu):
	scriptWindow = menu.ancestor(GafferUI.ScriptWindow)
	ftrack_dialog = Dialog(parent=scriptWindow._qtWidget(), connector=connector)
	ftrack_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	ftrack_dialog.show()

def loadAndInit():
	logger.debug("Initializing Ftrack plugin...")
	connector.registerAssets()

	scriptWindowMenu = GafferUI.ScriptWindow.menuDefinition(application)

	scriptWindowMenu.append("/Ftrack/Import Asset", {
		"command" : functools.partial(createAndShowFtrackDialog, Dialog=FtrackImportAssetDialog)})

	currentEntity = ftrack.Task(
		os.getenv('FTRACK_TASKID',
		os.getenv('FTRACK_SHOTID')))

	scriptWindowMenu.append("/Ftrack/Publish Asset", {
		"command" : functools.partial(createAndShowFtrackDialog, Dialog=PublishAssetDialog, currentEntity=currentEntity)})

	scriptWindowMenu.append("/Ftrack/Asset Manager", {
		"command" : functools.partial(createAndShowFtrackDialog, Dialog=FtrackAssetManagerDialog)})

	nodeMenu.append(
		"/Ftrack/FtrackAbcImport",
		GafferFtrack.FtrackAbcImport,
		searchText="FtrackAbcImport"
	)

loadAndInit()
