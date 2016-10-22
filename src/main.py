import logging
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidgetItem

from CalendarReader import Calendar
from MarkdownCreator import markdownCreator as md
from invoiceCreator import invoiceCreator
from hud import mainForm as mainForm

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        try:
            self.cal = Calendar(BASE_DIR)
            try:
                self.cal.fill()
            except BaseException as E:
                logging.error("{} \\ while filling calendar".format(E))
                exit()

        except BaseException as E:
            logging.error("{} \\ while opening calendar".format(E))
            exit()
        self.gui = mainForm.Ui_MainWindow()
        self.gui.setupUi(self)
        self.eventLabelSet()
        self.gui.pushButton.clicked.connect(self.getEventsCheckList)

        self.comboUtil = QComboBox(self)

    def getEventsCheckList(self):
        """
        check all the checkboxes
        :return:
        """
        # res = dict()
        res = []
        for i in range(0, self.gui.scrollLayout.count()):
            scrollItem = self.gui.scrollLayout.itemAt(i)
            if type(scrollItem) is QHBoxLayout:
                name = ""
                for y in range(0, scrollItem.count()):
                    hboxItem = scrollItem.itemAt(y)

                    if type(hboxItem) is QWidgetItem:
                        itemWidget = hboxItem.widget()
                        if type(itemWidget) is QLabel:
                            name = itemWidget.objectName().lstrip("label_")
                            logging.debug("logged {} label".format(name))
                        elif type(itemWidget) is QCheckBox:
                            # res[name] = itemWidget.isChecked()
                            if itemWidget.isChecked():
                                res.append(name)
                        else:
                            self.comboUtil.addItems("{} hasn't to be there".format(itemWidget))
                            self.comboUtil.show()
                            logging.error("{} hasn't to be there".format(itemWidget))

        # self.comboUtil.addItems(res)
        # self.comboUtil.show()

        # try:
        self.pay(res)
        # except BaseException as E:
        #     logging.error("{} \\ while creating files".format(E))

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

        # going to change events into the calendar
        for client in clientEvents.keys():
            if False:
                self.cal.payedEvents(clientEvents[client])
                # TODO: try it

            overview = md()
            overview.write(clientEvents[client])
            tex = invoiceCreator(BASE_DIR)
            tex.load(clientEvents[client])
        try:
            tex.write()
            tex.compiling()
        except Exception as E:
            logging.error("Error {} while writing {} tex file".format(E, tex))

    def eventLabelSet(self): #TODO: a better interface
        """
        set the event list
        :return:
        """
        events = self.cal.getEvents()
        head = "Client\tDurate\tDay"
        label = QLabel(self.gui.centralwidget)
        label.setObjectName(head)
        label.setStyleSheet("QLabel { background-color : grey; color : black; }")
        label.setText(head)

        self.gui.scrollLayout.addWidget(label)
        for event in events:
            elem = "{}\t{}\t{}".format(event.client, event.duration, event.date)

            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName("horizontalLayout")

            label = QLabel(self.gui.scrollAreaWidgetContents)
            label.setObjectName("label_{}".format(event.key))
            label.setText(elem)
            if event.payed:
                label.setStyleSheet("QLabel { background-color : darkRed; color : black; }")
                horizontalLayout.addWidget(label)

            else:
                label.setStyleSheet("QLabel { background-color : grey; color : black; }")
                horizontalLayout.addWidget(label)

                checkBox = QtWidgets.QCheckBox(self.gui.scrollAreaWidgetContents)
                checkBox.setObjectName("checkBox_{}".format(event.key))
                checkBox.setText("Select")
                checkBox.setStyleSheet("QLabel { background-color : darkRed; color : black; }")
                horizontalLayout.addWidget(checkBox)
            self.gui.scrollLayout.addLayout(horizontalLayout)


def main():
    try:
        app = QApplication(sys.argv)
        intro = mainWindow()
        intro.show()
        sys.exit(app.exec_())

    except BaseException as E:
        logging.error("{} \\ while drawing calendar interface".format(E))
        exit()


if __name__ == '__main__':
    main()
