
# Copyright (c) 2016 Efesto Lab LTD.

import os
import uuid

from PySide import QtCore, QtGui


from ftrack_connect.connector import base as maincon
from ftrack_connect.connector import FTAssetHandlerInstance

class Connector(maincon.Connector):
    def __init__(self):
        super(Connector, self).__init__()

    @staticmethod
    def getAssets():
        return []

    @staticmethod
    def getFileName():
        '''Return the *current scene* name'''

    @staticmethod
    def getMainWindow():
        return None

    @staticmethod
    def wrapinstance(ptr, base=None):
        """
        Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)

        :param ptr: Pointer to QObject in memory
        :type ptr: long or Swig instance
        :param base: (Optional) Base class to wrap with (Defaults to QObject, which should handle anything)
        :type base: QtGui.QWidget
        :return: QWidget or subclass instance
        :rtype: QtGui.QWidget
        """
        return ptr

    @staticmethod
    def importAsset(iAObj):
        '''Import the asset provided by *iAObj*'''
        iAObj.assetName = "_".join(
            [iAObj.assetType.upper(), iAObj.assetName, "AST"]
        )
        # Maya converts - to _ so let's do that as well
        iAObj.assetName = iAObj.assetName.replace('-', '_')

        # Check if this AssetName already exists in scene
        iAObj.assetName = Connector.getUniqueSceneName(iAObj.assetName)

        assetHandler = FTAssetHandlerInstance.instance()
        importAsset = assetHandler.getAssetClass(iAObj.assetType)
        if importAsset:
            result = importAsset.importAsset(iAObj)
            return result
        else:
            return 'assetType not supported'

    @staticmethod
    def selectObject(applicationObject=''):
        '''Select the *applicationObject*'''

    @staticmethod
    def selectObjects(selection):
        '''Select the given *selection*'''

    @staticmethod
    def removeObject(applicationObject=''):
        '''Remove the *applicationObject* from the scene'''

    @staticmethod
    def changeVersion(applicationObject=None, iAObj=None):
        '''Change version of *iAObj* for the given *applicationObject*'''

    @staticmethod
    def getSelectedObjects():
        '''Return the selected node names.'''

    @staticmethod
    def getSelectedAssets():
        '''Return the selected assets'''

    @staticmethod
    def setNodeColor(applicationObject='', latest=True):
        '''Set the node color'''

    @staticmethod
    def publishAsset(iAObj=None):
        '''Publish the asset provided by *iAObj*'''

    @staticmethod
    def getConnectorName():
        '''Return the connector name'''
        return 'gaffer'

    @staticmethod
    def getUniqueSceneName(assetName):
        return assetName

    @staticmethod
    def takeScreenshot():
        '''Take a screenshot and save it in the temp folder'''

    @staticmethod
    def batch():
        '''Return whether the application is in *batch mode* or not'''

    @classmethod
    def registerAssets(cls):
        '''Register all the available assets'''
        import gafferassets
        gafferassets.registerAssetTypes()
        super(Connector, cls).registerAssets()

    # Make certain scene validations before actualy publishing
    @classmethod
    def prePublish(cls, iAObj):
        '''Pre Publish check for given *iAObj*'''
        result, message = super(Connector, cls).prePublish(iAObj)
        if not result:
            return result, message

        return True, ''
