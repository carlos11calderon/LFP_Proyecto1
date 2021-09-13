from InterfazInicio import Ui_Bixelart 
from PyQt5 import QtCore, QtGui, QtWidgets
from Gestor import Gestor

gestor = Gestor()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Bixelart = QtWidgets.QDialog()
    ui = Ui_Bixelart()
    ui.setupUi(Bixelart)
    Bixelart.show()
    sys.exit(app.exec_())
    #ui.buttonCargar.clicked.connect(gestor.CargarArchivo)


