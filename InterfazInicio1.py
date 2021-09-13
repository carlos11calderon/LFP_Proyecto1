

from PyQt5 import QtCore, QtGui, QtWidgets
from Gestor import *

gestor = Gestor()
class Ui_Bixelart(object):
    
    def setupUi(self, Bixelart):
        Bixelart.setObjectName("Bixelart")
        Bixelart.resize(573, 454)
        Bixelart.setAutoFillBackground(False)
        self.groupBox = QtWidgets.QGroupBox(Bixelart)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 561, 451))
        self.groupBox.setObjectName("groupBox")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 541, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        ##creacion del boton cargar
        self.buttonCargar = QtWidgets.QPushButton(self.tab)
        self.buttonCargar.setGeometry(QtCore.QRect(20,300,100,35))
        self.buttonCargar.setObjectName("CargarPXLA")
        self.buttonCargar.clicked.connect(gestor.CargarArchivo)
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        ##creacion de una pestaña
        
        ## Creacion de un Groupbox
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 30, 111, 351))
        self.groupBox_2.setObjectName("groupBox_2")
        ##creacion de un boton
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(10, 50, 81, 51))
        self.pushButton.setObjectName("pushButton")
        ##creacion de otro boton
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 100, 81, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 150, 81, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 200, 81, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        

        self.retranslateUi(Bixelart)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Bixelart)

    def retranslateUi(self, Bixelart):
        _translate = QtCore.QCoreApplication.translate
        Bixelart.setWindowTitle(_translate("Bixelart", "Bitxelart"))
        self.groupBox.setTitle(_translate("Bixelart", "Menu"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Bixelart", "Cargar"))
        self.groupBox_2.setTitle(_translate("Bixelart", "Acciones"))
        self.buttonCargar.setText(_translate("Bixelart", "Cargar PXLA"))
        self.pushButton.setText(_translate("Bixelart", "Original"))
        self.pushButton_2.setText(_translate("Bixelart", "MirrorX"))
        self.pushButton_3.setText(_translate("Bixelart", "MirrorY"))
        self.pushButton_4.setText(_translate("Bixelart", "Double Mirror"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Bixelart", "Analizar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Bixelart", "Reportes"))
        
    
  