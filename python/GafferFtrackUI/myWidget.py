import sys
from PySide import QtGui


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
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
