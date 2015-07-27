import sys
import logging

from PySide import QtGui, QtCore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        logger.info('creating : %s' % self.__class__.__name__)

        super(MyWidget, self).__init__(parent=parent)

        layout = QtGui.QVBoxLayout()

        self.setLayout(layout)

        btn = QtGui.QPushButton('Hello')

        self.layout().addWidget(btn)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    w = MyWidget()

    w.show()

    sys.exit(app.exec_())
