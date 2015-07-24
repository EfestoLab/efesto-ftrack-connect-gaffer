
import IECore

import Gaffer
import GafferUI
from myWidget import MyWidget

QtCore = GafferUI._qtImport( "QtCore" )
QtGui = GafferUI._qtImport( "QtGui" )


class MyWidgetWrapper(GafferUI.Widget) :
    '''Create a wrapper around my custom widget'''
    def __init__( self, *args, **kw ):
        mywidget = MyWidget()
        super(MyWidgetWrapper, self).__init__(mywidget, *args, **kw)



class MyWidgetPlugValue(GafferUI.PlugValueWidget):
    '''Createa a plug value using my custom widget'''
    def __init__( self, plug, **kw ) :
        self.__myWidget = MyWidgetWrapper()
        super(MyWidgetPlugValue, self).__init__(self.__myWidget, plug, **kw )
        self._addPopupMenu( self.__myWidget )
