#!/usr/bin/env python3
import getopt
import logging
import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidgetItem

import parser
from calendar_reader import Calendar, set_cal_id, Credentials, calid_NotFoundException
from markdown_creator import markdown_creator as md
from hud import getStartEndTimes
from hud import mainForm as mainForm
from invoice_creator import invoice_creator

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)


class getStartEndTime(QDialog):
    def __init__(self):
        super(getStartEndTime, self).__init__()
        self.gui = getStartEndTimes.Ui_Dialog()
        self.gui.setupUi(self)

        self.end = None
        self.start = None

        self.gui.EndTime.dateChanged.connect(self._set_end_time_date)
        self.gui.StartTime.dateChanged.connect(self._set_start_time_date)
        self.exec()

    def _set_end_time_date(self, t):
        self.end = datetime.combine(t.toPyDate(), datetime.min.time())

    def _set_start_time_date(self, t):
        self.start = datetime.combine(t.toPyDate(), datetime.min.time())

    def get_valors(self):
        return self.start, self.end


class date_popup(QDialog):
    def __init__(self):
        super(Qt.Popup, self).__init__()
        self.setSizeGripEnabled(False)
        self.resize(260, 230)
        self.widget = QWidget(self)
        self.widget.setObjectName(QtCore.QString.fromUtf8("self.widget"))
        self.widget.setGeometry(QRect(0, 10, 258, 215))

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(QtCore.QString.fromUtf8("self.verticalLayout"))
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.calendarWidget = QCalendarWidget(self.widget)
        self.calendarWidget.setObjectName(QtCore.QString.fromUtf8("calendarWidget"))

        self.verticalLayout.addWidget(self.calendarWidget)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(QtCore.QString.fromUtf8("self.buttonBox"))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QObject.self.buttonBox.accepted.connect(self.accept)
        QObject.self.buttonBox.rejected.connect(self.reject)

    def selectedDate(self):
        return self.calendarWidget.selectedDate()


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        self.cal = None
        self.gui = mainForm.Ui_MainWindow()
        self.gui.setupUi(self)

        # self.gui.actionUpdate.triggered.connect(self.eventLabelSet)
        self.gui.actionUpdate.triggered.connect(self.gimme_your_times)
        self.gui.actionChange_Calendar.triggered.connect(self.change_calendar)
        self.gui.pushButton.clicked.connect(self.get_events_check_list)

        # self.comboUtil = QComboBox(self)

    def gimme_your_times(self):
        startEndDialog = getStartEndTime()
        start, end = startEndDialog.get_valors()
        self.event_label_set(start, end)

    def get_events_check_list(self):
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
            event = self.cal.get_event_by_id(id)
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
                self.cal.pay_events(clientEvents[client])
                # TODO: try it

            overview = md()
            overview.write(clientEvents[client])
            tex = invoice_creator(BASE_DIR, clientEvents[client], client)
            try:
                # tex.write()
                tex.compiling()
            except Exception as E:
                logging.error("Error {} while writing {} tex file".format(E, client))

    def _getNewLabel(self, text, status, name=None):
        """
        allow to get
        :param text:
        :param status:
        :param name:
        :return:
        """
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

    def change_checkboxes_status(self):
        """
        usefull for set all the checkboxes using only one checkbox
        :return:
        """
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

    def change_calendar(self):
        """
        Blanck the calid entry in your configuration
        :return:
        """
        path = os.path.join(BASE_DIR, "Configuration.ini")
        data = parser.get_dict(path)
        elem = data["Calendar"]
        elem["calid"] = "none"
        data["Calendar"] = elem
        parser.write_data(data, path)
        self.cal = None

        self.gimme_your_times()

    def call_initializer(self):
        """
        initialize the calendart struct
        :return:
        """
        credentials = Credentials(BASE_DIR)

        # I'm going to create calendar using "calid" into the config file
        while self.cal is None:
            try:
                self.cal = Calendar(BASE_DIR, credentials.get_service())
            except calid_NotFoundException as c:
                logging.debug(c)
                set_cal_id(BASE_DIR, credentials.get_service())

    def event_label_set(self, startDate, endDate):  # TODO: a better style
        """
        set the event list
        :return:
        """
        if self.cal is None:
            self.call_initializer()
        self.cal.download_events(startDate, endDate)
        self.gui.checboxesController.clicked.connect(self.change_checkboxes_status)

        events = self.cal.get_events()
        # self.gui.scrollLayout.removeItem() #TODO: blank the event visualized
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

            label = self._getNewLabel(event.client, "payed" if event.payed else "not payed",
                                      "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)
            label = self._getNewLabel(event.duration, "payed" if event.payed else "not payed",
                                      "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)
            label = self._getNewLabel(event.date, "payed" if event.payed else "not payed",
                                      "checkBox_{}".format(event.key))
            horizontalLayout.addWidget(label)

            self.gui.scrollLayout.addLayout(horizontalLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gui.scrollLayout.addItem(spacerItem)


def main(argv=sys.argv):
    opts, args = getopt.getopt(argv[1:], 'g:', ['loglevel='])
    for opt, arg in opts:
        if opt in ('-g', '--loglevel'):
            if str(arg).upper() == 'debug'.upper():
                logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.DEBUG)
            if str(arg).upper() == 'info'.upper():
                logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.INFO)
        else:
            logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s')
    app = QApplication(sys.argv)
    intro = mainWindow()
    intro.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
