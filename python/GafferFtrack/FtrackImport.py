import logging

import IECore
import Gaffer
import GafferScene

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FtrackImport(GafferScene.AlembicSource):
    def __init__(self, name='FtrackImport'):
        super(FtrackImport, self).__init__(name=name)
        logger.info('creating : %s' % self.__class__.__name__)
        self.addChild(Gaffer.StringPlug('something'))

        # import GafferFtrackUI
        # self.addChild( Gaffer.StringPlug(
        #    "myWidget", GafferFtrackUI.MyWidgetPlugValue )
        # )


IECore.registerRunTimeTyped(FtrackImport)
