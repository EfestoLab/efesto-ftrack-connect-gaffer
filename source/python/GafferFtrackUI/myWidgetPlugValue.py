from __future__ import with_statement
import logging
import os

import IECore
import Gaffer
import GafferUI
import GafferFtrack

import ftrack

from context_selector import AssetSelector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


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
        self.mywidget = AssetSelector(current_entity)

        super(MyWidgetWrapper, self).__init__(
            self.mywidget,
            toolTip='mywidget',
            **kw
        )
        self.__importComponentSignal = GafferUI.WidgetSignal()
        self._qtWidget().importComponent.connect(
            Gaffer.WeakMethod(self.__importComponent)
        )

    def importComponentSignal(self):
        return self.__importComponentSignal

    def __importComponent(self, state):
        logger.info(state)
        self.__importComponentSignal(self)

    def getValue(self):
        return self.mywidget.selectedComponentPath


class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''

    def __init__(self, plug, **kw):
        logger.info('creating: %s ' % self.__class__.__name__)

        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, plug, **kw)
        self.__importComponentConnection = self.__myWidget.importComponentSignal().connect(
            Gaffer.WeakMethod(self.__importComponent)
        )
        self._updateFromPlug()

    def _updateFromPlug(self):
        pass
        # if self.getPlug() is not None:
        #     with self.getContext():
        #         with Gaffer.BlockedConnection(self.__stateChangedConnection):
        #             self.__myWidget.setState(self.getPlug().getValue())

    def __importComponent(self, value):
        logger.info(value)
        with Gaffer.UndoContext(self.getPlug().ancestor(Gaffer.ScriptNode)):
            self.getPlug().setValue(self.__myWidget.getValue())
