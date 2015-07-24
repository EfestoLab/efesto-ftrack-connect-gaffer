import IECore

import Gaffer
import GafferScene


class FtrackImport(GafferScene.AlembicSource):
    def __init__(self, name='FtrackImport'):
        super(FtrackImport, self).__init__(name=name)


IECore.registerRunTimeTyped(FtrackImport)
