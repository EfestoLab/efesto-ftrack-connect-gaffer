import logging

import IECore
import Gaffer
import GafferScene

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('module')

class FtrackImport(GafferScene.AlembicSource):
    def __init__(self, name='FtrackImport'):
        super(FtrackImport, self).__init__(name=name)
        logger.info('creating : %s' % self.__class__.__name__)
        logger.info(self['fileName'])
        # add manually a chid
        self.addChild(Gaffer.StringPlug('something'))

        # try setting the custom widget as child
        # import GafferFtrackUI
        # self.addChild( GafferFtrackUI.MyWidgetWrapper(
        #    GafferFtrackUI.MyWidgetPlugValue )
        # )


IECore.registerRunTimeTyped(FtrackImport, typeName="Ftrack::Import" )
