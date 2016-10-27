# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout_3")
        self.horizontalLayout.setSpacing(1)

        self.checboxesController = QtWidgets.QCheckBox(self.centralwidget)
        self.checboxesController.setObjectName("checboxesController")
        self.checboxesController.setMaximumSize(QtCore.QSize(25, 20))
        self.checboxesController.setMinimumSize(QtCore.QSize(25, 20))
        # self.checboxesController.setStyleSheet("QCheckBox { background-color : grey; color : black; }") # someone says that this kind of style is like a shit :(
        self.horizontalLayout.addWidget(self.checboxesController)

        self.label = self.getNewLabel("Client", "head")
        self.horizontalLayout.addWidget(self.label)

        self.label = self.getNewLabel("Durate", "head")
        self.horizontalLayout.addWidget(self.label)

        self.label = self.getNewLabel("Day", "head")
        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 784, 483))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setObjectName("scrollLayout")
        self.scrollLayout.setSpacing(1)

        # self.horizontalLayout = QtWidgets.QHBoxLayout() # I'll add this section by the main
        # self.horizontalLayout.setObjectName("horizontalLayout")
        # self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # self.label.setObjectName("label")
        # self.horizontalLayout.addWidget(self.label)
        # self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        # self.checkBox.setObjectName("checkBox")
        # self.horizontalLayout.addWidget(self.checkBox)
        # self.scrollLayout.addLayout(self.horizontalLayout)
        # spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.scrollLayout.addItem(spacerItem)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 32))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.menuFile.addAction(self.actionUpdate)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def getNewLabel(self, text, status, name=None):
        label = QLabel(self.centralwidget)
        label.setText(str(text))
        label.setObjectName(name)
        if status is "head":
            label.setStyleSheet("QLabel { background-color : grey; color : black; }")
        elif status is "payed":
            label.setStyleSheet("QLabel { background-color : darkRed; color : black; }")
        else:
            label.setStyleSheet("QLabel { background-color : grey; color : black; }")
        return label

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.label.setText(_translate("MainWindow", "TextLabel"))
        # self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.pushButton.setText(_translate("MainWindow", "Pay Off"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionUpdate.setText(_translate("MainWindow", "&Update"))

