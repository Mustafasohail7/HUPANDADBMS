# Form implementation generated from reading ui file 'c:\Users\ds_sa\Desktop\Fall 23\Database\Project\User Registration Form.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 553)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 0, 241, 81))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 70, 711, 331))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.EnterName = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EnterName.setGeometry(QtCore.QRect(130, 70, 501, 22))
        self.EnterName.setObjectName("EnterName")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 120, 61, 16))
        self.label_5.setObjectName("label_5")
        self.EnterID = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EnterID.setGeometry(QtCore.QRect(130, 20, 501, 22))
        self.EnterID.setObjectName("EnterID")
        self.EnterPassword = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EnterPassword.setGeometry(QtCore.QRect(130, 120, 501, 22))
        self.EnterPassword.setObjectName("EnterPassword")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 240, 91, 16))
        self.label_7.setObjectName("label_7")
        self.EnterPhone = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EnterPhone.setGeometry(QtCore.QRect(130, 240, 501, 22))
        self.EnterPhone.setObjectName("EnterPhone")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(20, 180, 91, 16))
        self.label_8.setObjectName("label_8")
        self.EnterAddress = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EnterAddress.setGeometry(QtCore.QRect(130, 180, 501, 22))
        self.EnterAddress.setObjectName("EnterAddress")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(370, 30, 111, 81))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.AddUser = QtWidgets.QPushButton(parent=self.centralwidget)
        self.AddUser.setGeometry(QtCore.QRect(660, 460, 93, 28))
        self.AddUser.setObjectName("AddUser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 26))
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
        self.label.setText(_translate("MainWindow", "Please enter your details below:"))
        self.label_2.setText(_translate("MainWindow", "Name:"))
        self.label_3.setText(_translate("MainWindow", "HU ID:"))
        self.label_5.setText(_translate("MainWindow", "Password:"))
        self.label_7.setText(_translate("MainWindow", "Phone Number:"))
        self.label_8.setText(_translate("MainWindow", "Address:"))
        self.AddUser.setText(_translate("MainWindow", "Sign Up"))
