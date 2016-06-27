import logging

import IECore
import Gaffer
import GafferScene

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FtrackAbcImport( GafferScene.SceneNode ) :

    def __init__( self, name = "FtrackAbcImport" ) :

        GafferScene.SceneNode.__init__( self, name )

        self["fileName"] = Gaffer.StringPlug(defaultValue = "")
        self["refreshCount"] = Gaffer.IntPlug()

        self["assetId"] = Gaffer.StringPlug(defaultValue = "")
        self["assetVersion"] = Gaffer.IntPlug(defaultValue = 0)
        self["assetPath"] = Gaffer.StringPlug(defaultValue = "")
        self["assetTake"] = Gaffer.StringPlug(defaultValue = "")
        self["assetComponentId"] = Gaffer.StringPlug(defaultValue = "")

        self["__source"] = GafferScene.AlembicSource()
        self["__source"]["enabled"].setInput( self["enabled"] )

        self["__source"]["fileName"].setInput( self["fileName"] )
        self["__source"]["refreshCount"].setInput( self["refreshCount"] )

        self["out"].setInput( self["__source"]["out"] )

IECore.registerRunTimeTyped( FtrackAbcImport )
