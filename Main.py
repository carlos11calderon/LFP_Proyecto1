from InterfazInicio import Ui_Bixelart 
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Bixelart = QtWidgets.QDialog()
    ui = Ui_Bixelart()
    ui.setupUi(Bixelart)
    Bixelart.show()
    sys.exit(app.exec_())





