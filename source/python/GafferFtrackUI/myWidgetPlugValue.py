from __future__ import with_statement
import logging
import os

import IECore
import Gaffer
import GafferUI
import GafferFtrack

import ftrack

from context_selector import ContextSelector
from myWidget import MyWidget

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


logger.info('loading: %s' % MyWidget)


class MyWidgetWrapper(GafferUI.Widget):
    '''Create a wrapper around my custom widget'''

    def __init__(self, *args, **kw):
        logger.info('creating: %s ' % self.__class__.__name__)
        entity = os.getenv(
            'FTRACK_TASKID',
            os.getenv('FTRACK_SHOTID', '1ca0f86e-1d6e-11e5-b7ab-04013398c801')
        )
        # hardcoded Id for testing if not running through the hook

        current_entity = ftrack.Task(entity)
        self.mywidget = ContextSelector(current_entity)
        super(MyWidgetWrapper, self).__init__(
            self.mywidget,
            toolTip='mywidget',
            **kw
        )


class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''

    def __init__(self, plug, **kw):
        logger.info('creating: %s ' % self.__class__.__name__)

        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, plug, **kw)
        self._updateFromPlug()

    def _updateFromPlug(self):
        logger.info('updating from plug...')
        pass
