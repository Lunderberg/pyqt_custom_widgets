#!/usr/bin/env python3

import sys
from PyQt4 import uic, QtGui, QtCore

(Ui_MainWindow, QMainWindow) = uic.loadUiType('example.ui')

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ipython.clicked.connect(self.start_ipython_interpreter)

    def start_ipython_interpreter(self,*args):
        QtCore.pyqtRemoveInputHook()
        import IPython; IPython.embed()
        QtCore.pyqtRestoreInputHook()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
