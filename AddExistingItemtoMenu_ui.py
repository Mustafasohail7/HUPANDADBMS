# Form implementation generated from reading ui file 'c:\Users\ds_sa\Desktop\Fall 23\Database\Project\AddExistingItemtoMenu.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 271)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 30, 81, 16))
        self.label_7.setObjectName("label_7")
        self.ItemSelector = QtWidgets.QComboBox(parent=self.centralwidget)
        self.ItemSelector.setGeometry(QtCore.QRect(130, 30, 291, 22))
        self.ItemSelector.setObjectName("ItemSelector")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 90, 81, 16))
        self.label_8.setObjectName("label_8")
        self.CafeSelector = QtWidgets.QComboBox(parent=self.centralwidget)
        self.CafeSelector.setGeometry(QtCore.QRect(130, 90, 291, 22))
        self.CafeSelector.setObjectName("CafeSelector")
        self.CafeSelector.addItem("")
        self.CafeSelector.addItem("")
        self.AddToMenu = QtWidgets.QPushButton(parent=self.centralwidget)
        self.AddToMenu.setGeometry(QtCore.QRect(310, 160, 111, 28))
        self.AddToMenu.setObjectName("AddToMenu")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 446, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "Select Item:"))
        self.label_8.setText(_translate("MainWindow", "Select Cafe:"))
        self.CafeSelector.setItemText(0, _translate("MainWindow", "Tapal Cafeteria"))
        self.CafeSelector.setItemText(1, _translate("MainWindow", "Cafe2Go"))
        self.AddToMenu.setText(_translate("MainWindow", "Add to Menu"))
