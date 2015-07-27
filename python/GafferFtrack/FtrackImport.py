import logging

import IECore
import Gaffer
import GafferScene

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FtrackImport(Gaffer.Node):
    def __init__(self, name='FtrackImport'):
        super(FtrackImport, self).__init__(name=name)

        Gaffer.Node.__init__( self, name )

        self["fileName"] = Gaffer.StringPlug()
        self["out"] = GafferScene.ScenePlug( direction = Gaffer.Plug.Direction.Out )

        self["__reader"] = GafferScene.AlembicSource()
        self["__reader"]["fileName"].setInput( self["fileName"] )
        self["out"].setInput( self["__reader"]["out"] )

IECore.registerRunTimeTyped(FtrackImport)
