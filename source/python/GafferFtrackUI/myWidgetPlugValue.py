from __future__ import with_statement
import logging

import IECore
import Gaffer
import GafferUI
import GafferFtrack

from ContextSelector import ContextSelector


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


logger.info('loading: %s' % MyWidget)

class MyWidgetWrapper(GafferUI.Widget) :
    '''Create a wrapper around my custom widget'''

    def __init__( self, *args, **kw ):
        logger.info('creating: %s ' % self.__class__.__name__)
        self.mywidget = ContextSelector()
        super(MyWidgetWrapper, self).__init__(
            self.mywidget,
            toolTip='mywidget',
            **kw
        )

    def setText( self, text ) :

        self._qtWidget().setText( text )

    def getText( self ) :

        return str( self._qtWidget().text() )


class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''

    def __init__( self, plug, **kw ) :
        logger.info('creating: %s ' % self.__class__.__name__)

        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, plug, **kw)
        #self._addPopupMenu(self.__myWidget)
        self._updateFromPlug()

    def _updateFromPlug( self ) :
        logger.info('updating from plug...')
        pass