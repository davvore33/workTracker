# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'getStartEndTimes.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(39, 29, 341, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StartTime_Label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.StartTime_Label.setObjectName("StartTime_Label")
        self.horizontalLayout.addWidget(self.StartTime_Label)
        self.StartTime = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.StartTime.setObjectName("StartTime")
        self.horizontalLayout.addWidget(self.StartTime)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EndTime_Label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.EndTime_Label.setObjectName("EndTime_Label")
        self.horizontalLayout_2.addWidget(self.EndTime_Label)
        self.EndTime = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.EndTime.setDate(QDate.currentDate())
        self.EndTime.setObjectName("EndTime")
        self.horizontalLayout_2.addWidget(self.EndTime)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.StartTime_Label.setText(_translate("Dialog", "StartTime"))
        self.EndTime_Label.setText(_translate("Dialog", "EndTime"))

