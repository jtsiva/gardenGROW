import sys

from PyQt4 import QtCore, QtGui
from form import Ui_mainWindow
 
class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
 
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        myapp = MyWindow()
        myapp.show()
        sys.exit(app.exec_())