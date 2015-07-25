from __future__ import with_statement
import logging

import IECore
import Gaffer
import GafferUI
import GafferFtrack

from myWidget import MyWidget


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('loading widget wrapper and plug value')

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


class MyWidgetWrapper(GafferUI.Widget) :
    '''Create a wrapper around my custom widget'''

    def __init__( self, *args, **kw ):
        logger.info('creating: %s ' % self.__class__.__name__)
        self.mywidget = MyWidget()
        super(MyWidgetWrapper, self).__init__(self.mywidget, toolTip='mywidget', **kw)


class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''

    def __init__( self, *args, **kw ) :
        logger.info('creating: %s ' % self.__class__.__name__)

        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, *args, **kw)
        self._addPopupMenu(self.__myWidget)
        self._updateFromPlug()

    def _updateFromPlug( self ) :
        logger.info('updating from plug...')
        pass
