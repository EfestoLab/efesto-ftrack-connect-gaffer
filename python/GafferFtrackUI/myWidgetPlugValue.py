
import IECore

import Gaffer
import GafferUI
import GafferFtrack

from myWidget import MyWidget

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


class MyWidgetWrapper(GafferUI.Widget) :
    '''Create a wrapper around my custom widget'''
    def __init__( self, *args, **kw ):
        mywidget = MyWidget()
        super(MyWidgetWrapper, self).__init__(mywidget, *args, **kw)
        self.__stateChangedSignal = GafferUI.WidgetSignal()


class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''
    def __init__( self, *args, **kw ) :
        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, *args, **kw )
        self._addPopupMenu(self.__myWidget)

    def setHighlighted( self, highlighted ) :

        GafferUI.PlugValueWidget.setHighlighted( self, highlighted )
        self.__boolWidget.setHighlighted( highlighted )


GafferUI.PlugValueWidget.registerType(GafferFtrack.FtrackImport, MyWidgetPlugValue)
