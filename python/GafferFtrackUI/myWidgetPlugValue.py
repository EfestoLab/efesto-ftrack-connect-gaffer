from __future__ import with_statement
import logging

import IECore

import Gaffer
import GafferUI
import GafferFtrack

from myWidget import MyWidget


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


class MyWidgetWrapper(GafferUI.Widget) :
    '''Create a wrapper around my custom widget'''
    def __init__( self, *args, **kw ):
        logger.info('creating: %s ' % self.__class__.__name__)
        self.mywidget = MyWidget()
        super(MyWidgetWrapper, self).__init__(self.mywidget, *args, **kw)
        self.__stateChangedSignal = GafferUI.WidgetSignal()

    def stateChangedSignal( self ) :
        return self.__stateChangedSignal

    def __stateChanged( self, state ) :
        self.__stateChangedSignal( self )

    def setState(self, state):
        pass

    def getState(self):
        return True

class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''
    def __init__( self, *args, **kw ) :
        logger.info('creating: %s ' % self.__class__.__name__)

        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, *args, **kw )
        self._addPopupMenu(self.__myWidget)
        self.__stateChangedConnection = self.__myWidget.stateChangedSignal().connect(
            Gaffer.WeakMethod(self.__stateChanged)
        )
        self._updateFromPlug()

    def _updateFromPlug( self ) :
        if self.getPlug() is not None :
            with self.getContext() :
                with Gaffer.BlockedConnection( self.__stateChangedConnection ) :
                    self.__myWidget.setState( self.getPlug().getValue() )

        self.__myWidget.setEnabled( self._editable() )

    def setHighlighted( self, highlighted ) :
        GafferUI.PlugValueWidget.setHighlighted( self, highlighted )
        self.__myWidget.setHighlighted( highlighted )

    def __stateChanged( self, widget ) :
        self.__setPlugValue()
        return False

    def __setPlugValue( self ) :
        with Gaffer.UndoContext( self.getPlug().ancestor( Gaffer.ScriptNode ) ) :
            self.getPlug().setValue( self.__myWidget.getState() )
