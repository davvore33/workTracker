import logging
import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidgetItem

from CalendarReader import Calendar, setCalId, Credentials, calidNotFoundException
from MarkdownCreator import markdownCreator as md
from invoiceCreator import invoiceCreator
from hud import mainForm as mainForm

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        credentials = Credentials(BASE_DIR)

        # I'm going to create calendar using "calid" into the config file
        self.cal = None
        while self.cal is None:
            try:
                self.cal = Calendar(BASE_DIR, credentials.getService())
            except calidNotFoundException as c:
                logging.debug(c)
                setCalId(BASE_DIR, credentials.getService())

        self.cal.fill()
        self.gui = mainForm.Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.actionUpdate.triggered.connect(self.eventLabelSet)
        self.gui.pushButton.clicked.connect(self.getEventsCheckList)

        # self.comboUtil = QComboBox(self)

    def getEventsCheckList(self):
        """
        check all the checkboxes
        :return:
        """
        res = []
        for i in range(0, self.gui.scrollLayout.count()):
            scrollItem = self.gui.scrollLayout.itemAt(i)
            if type(scrollItem) is QHBoxLayout:
                for y in range(0, scrollItem.count()):
                    hboxItem = scrollItem.itemAt(y)
                    if type(hboxItem) is QWidgetItem:
                        itemWidget = hboxItem.widget()
                        if type(itemWidget) is QCheckBox:
                            if itemWidget.isChecked():
                                name = itemWidget.objectName()
                                name = name[len("checkBox_"):]
                                res.append(name)
        self.pay(res)

    def pay(self, idChecked):
        """
        pay release function: proceeds to create a markdown overview, a tex based invoice, modify events into the calendar, add a record to a csv report
        :param idChecked:
        :return:
        """

        clientEvents = dict()

        for id in idChecked:
            event = self.cal.getEventById(id)
            if event.client not in clientEvents.keys():
                a = []
            else:
                a = clientEvents[event.client]
            a.append(event)
            clientEvents[event.client] = a

        # self.comboUtil.addItems(clientEvents)
        # self.comboUtil.show()

        # going to change events into the calendar
        for client in clientEvents.keys():
            if False:
                self.cal.payedEvents(clientEvents[client])
                # TODO: try it

            overview = md()
            overview.write(clientEvents[client])
            tex = invoiceCreator(BASE_DIR, clientEvents[client], client)
            try:
                tex.write()
                tex.compiling()
            except Exception as E:
                logging.error("Error {} while writing {} tex file".format(E, client))

    def getNewLabel(self, text, status, name=None):
        label = QLabel(self.gui.scrollAreaWidgetContents)
        label.setText(str(text))
        label.setObjectName(name)
        if status is "head":
            label.setStyleSheet("QLabel { background-color : grey; color : black; }")
        elif status is "payed":
            label.setStyleSheet("QLabel { background-color : darkRed; color : black; }")
        else:
            label.setStyleSheet("QLabel { background-color : grey; color : black; }")
        return label

    def changeCheckboxesStatus(self):
        for i in range(0, self.gui.scrollLayout.count()):
            scrollItem = self.gui.scrollLayout.itemAt(i)
            if type(scrollItem) is QHBoxLayout:
                for y in range(0, scrollItem.count()):
                    hboxItem = scrollItem.itemAt(y)
                    if type(hboxItem) is QWidgetItem:
                        itemWidget = hboxItem.widget()
                        if type(itemWidget) is QCheckBox:
                            if itemWidget.isChecked():
                                itemWidget.setChecked(0)
                            else:
                                itemWidget.setChecked(1)

    def eventLabelSet(self):  # TODO: a better style
        """
        set the event list
        :return:
        """

        self.gui.checboxesController.clicked.connect(self.changeCheckboxesStatus)

        events = self.cal.getEvents()

        for event in events:
            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName("horizontalLayout")

            checkBox = QtWidgets.QCheckBox(self.gui.scrollAreaWidgetContents)
            checkBox.setMaximumSize(QtCore.QSize(25, 20))
            checkBox.setMinimumSize(QtCore.QSize(25, 20))
            checkBox.setObjectName("checkBox_{}".format(event.key))
            if event.payed:
                checkBox.setCheckable(False)
                # checkBox.setStyleSheet("QCheckBox { background-color : darkRed; color : black; }")
            else:
                checkBox.setCheckable(True)
                # checkBox.setStyleSheet("QCheckBox { background-color : grey; color : black; }")

            horizontalLayout.addWidget(checkBox)

            label = self.getNewLabel(event.client, "payed" if event.payed else "not payed",
                                     "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)
            label = self.getNewLabel(event.duration, "payed" if event.payed else "not payed",
                                     "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)
            label = self.getNewLabel(event.date, "payed" if event.payed else "not payed",
                                     "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)

            self.gui.scrollLayout.addLayout(horizontalLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gui.scrollLayout.addItem(spacerItem)


def main():
    app = QApplication(sys.argv)
    intro = mainWindow()
    intro.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
