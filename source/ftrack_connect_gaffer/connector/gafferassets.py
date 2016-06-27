
# Copyright (c) 2016 Efesto Lab LTD.

import os
import copy
import uuid
import ftrack

from ftrack_connect.connector import (
    FTAssetHandlerInstance,
    FTAssetType,
    FTComponent
)

from ftrack_connect.connector import panelcom

import gaffercon

import Gaffer
import GafferScene
import GafferUI

import GafferFtrack

import logging
logger = logging.getLogger(__name__)

class GeometryAsset(FTAssetType):
    def __init__(self):
        super(GeometryAsset, self).__init__()

    def _getScriptNode(self):
        # Use raw Qt to find the active window
        QtGui = GafferUI._qtImport("QtGui")
        app = QtGui.QApplication.instance()
        qActiveWindow = app.activeWindow()
        # Find the GafferUI.Widget which owns that QWidget
        activeWindow = GafferUI.Widget._owner(qActiveWindow)

        print "*** activeWindow = ", activeWindow, ", type = ", type(activeWindow)

        if not isinstance(activeWindow, GafferUI.ScriptWindow):
            activeWindow = activeWindow.ancestor(GafferUI.ScriptWindow)
            print "*** activeWindow = ", activeWindow, ", type = ", type(activeWindow)

        return activeWindow.scriptNode()

    def _uniqueNodeName(self, script, prefix):
        name = prefix
        if not name in script:
            return name

        i = 1
        while True:
            name = prefix + str(i)
            if not name in script:
                return name

            i = i + 1

    def importAsset(self, iAObj=None):
        '''Import asset defined in *iAObj*'''

        if iAObj.componentName == 'alembic':
            node = GafferFtrack.FtrackAbcImport()
            node['fileName'].setValue(iAObj.filePath)
            node['assetId'].setValue(iAObj.assetVersionId)
            node['assetVersion'].setValue(int(iAObj.assetVersion))
            node['assetPath'].setValue(iAObj.filePath)
            node['assetTake'].setValue(iAObj.componentName)
            node['assetComponentId'].setValue(iAObj.componentId)

            script = self._getScriptNode()
            nodeName = self._uniqueNodeName(script, 'ftrackAbcImport')
            script[nodeName] = node

            logger.debug("Import asset done")
            return 'Imported ' + iAObj.assetType + ' asset'

        return 'Ignoring ' + iAObj.assetType + ' asset'

    def getGroupName(self, nodes, assetName):
        '''Return the node among the *nodes* containing the given *assetName*.'''

    def publishAsset(self, iAObj=None):
        '''Publish the asset defined by the provided *iAObj*.'''

    def getSceneSettingsObj(self, iAObj):
        '''Return default settings for the provided *iAObj*.'''

    def changeVersion(self, iAObj=None, applicationObject=None):
        '''Change the version of the asset defined in *iAObj*
        and *applicationObject*
        '''

def registerAssetTypes():
    assetHandler = FTAssetHandlerInstance.instance()
    assetHandler.registerAssetType(name='geo', cls=GeometryAsset)
