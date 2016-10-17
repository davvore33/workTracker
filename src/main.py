import logging
import os
import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidgetItem

from CalendarReader import Calendar
from DatasheetCreator import datasheetcreator as csv
from MarkdownCreator import markdownCreator as md
from TexCreator import texCreator
from hud import mainForm

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.gui = mainForm.Ui_MainWindow()
        self.gui.setupUi(self)

    def getEventsCheckList(self):
        res = dict()
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
                            res[name] = True if itemWidget.checkState() is 0 else False
                        else:
                            logging.error("{} hasn't to be there".format(itemWidget))
        return res

    def eventLabelSet(self, cal):
        events = cal.getEvents()
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
        cal = Calendar(BASE_DIR)
        try:
            cal.fill()
        except BaseException as E:
            logging.error("{} \\ while filling calendar".format(E))
            exit()

    except BaseException as E:
        logging.error("{} \\ while opening calendar".format(E))
        exit()

    try:
        app = QApplication(sys.argv)
        intro = mainWindow()
        intro.show()
        intro.eventLabelSet(cal)
        intro.getEventsCheckList()
        sys.exit(app.exec_())

    except BaseException as E:
        logging.error("{} \\ while drawing calendar interface".format(E))
        # try:
        #     fileCreation(cal)
        # except BaseException as E:
        #     logging.error("{} \\ while creating files".format(E))
        # cal.payedEvents(cal.getToPayEvents())


def fileCreation(cal):
    toPayEvents = cal.getToPayEvents()

    overview = md()
    overview.write(toPayEvents)
    tex = texCreator(BASE_DIR)
    tex.write(toPayEvents)
    try:
        tex.compiling()
    except Exception as E:
        logging.error("Error {} while writing {} tex file".format(E, tex))


if __name__ == '__main__':
    main()
