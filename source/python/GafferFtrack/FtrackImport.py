import logging

import IECore
import Gaffer
import GafferScene

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FtrackAbcImport(Gaffer.Node):
    def __init__(self, name='FtrackAbcImport'):
        super(FtrackAbcImport, self).__init__(name=name)

        self["asset"] = Gaffer.StringPlug()
        self["out"] = GafferScene.ScenePlug( direction = Gaffer.Plug.Direction.Out )

        self["__reader"] = GafferScene.AlembicSource()
        self["__reader"]["fileName"].setInput( self["asset"] )
        self["out"].setInput( self["__reader"]["out"] )

IECore.registerRunTimeTyped(FtrackAbcImport)
