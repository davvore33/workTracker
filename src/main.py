import logging
import os
import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow

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
    app = QApplication(sys.argv)
    intro = mainWindow()
    intro.show()

    try:
        cal = Calendar(BASE_DIR)
        try:
            cal.fill()
        except BaseException as E:
            logging.error("{} \\ while filling calendar".format(E))
            exit()

        try:
            intro.eventLabelSet(cal)

            try:
                fileCreation(cal)
            except BaseException as E:
                logging.error("{} \\ while creating files".format(E))
            # cal.payedEvents(cal.getToPayEvents)
            sys.exit(app.exec_())

        except BaseException as E:
            logging.error("{} \\ while drawing calendar interface".format(E))
    except BaseException as E:
        logging.error("{} \\ while opening calendar".format(E))
        exit()


def fileCreation(cal):

    toPayEvents = cal.getToPayEvents()

    invoicesOverview = csv()
    invoicesOverview.writecsv()
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
