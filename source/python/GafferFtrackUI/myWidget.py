import sys
import logging

from PySide import QtGui, QtCore
import ftrack

try:
    ftrack.setup()
except:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetPicker(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AssetPicker, self).__init__(parent=parent)
        self.layout = QtGui.QVBoxLayout()
        btn = QtGui.QPushButton('HERE WE GO')
        self.layout.addWidget(btn)
        self.setLayout(self.layout)


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        logger.info('creating : %s' % self.__class__.__name__)
        super(MyWidget, self).__init__(parent=parent)
        self.asset_picker = AssetPicker()
        self.build_ui()
        self.connect_signals()

    def build_ui(self):
        self.mainlayout = QtGui.QVBoxLayout()
        self.hlayout = QtGui.QHBoxLayout()
        self.mainlayout.addLayout(self.hlayout)
        self.versions = QtGui.QComboBox()
        self.setLayout(self.mainlayout)
        self.asset_path = QtGui.QLineEdit()
        self.asset_btn = QtGui.QPushButton('select asset')
        self.hlayout.addWidget(self.asset_path)
        self.hlayout.addWidget(self.asset_btn)
        self.mainlayout.addWidget(self.versions)

    def connect_signals(self):
        self.asset_btn.clicked.connect(self.asset_picker.exec_)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
