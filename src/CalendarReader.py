from __future__ import print_function

import datetime
import logging
import os

import httplib2
import oauth2client
import parser
from DateTime import DateTime
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QRadioButton
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

from Events import Events
from hud import getCalIdForm as getCalUiForm


class calidNotFoundException(BaseException):
    def __init__(self, args):
        super()
        logging.error(args)


class setCalId(QDialog):
    def __init__(self, configPath, service):

        super(setCalId, self).__init__()
        self.gui = getCalUiForm.Ui_Dialog()
        self.gui.setupUi(self)
        self.configPath = configPath
        calendarList = service.calendarList().list().execute()
        for i in calendarList['items']:
            if i['accessRole'] == 'owner':
                radioButton = QRadioButton(self.gui.verticalLayoutWidget)
                radioButton.setText(i['summary'])
                radioButton.setObjectName("Radiobutton_" + i['id'])
                self.gui.verticalLayout.addWidget(radioButton)
        ok, canc = self.gui.buttonBox.buttons()
        ok.clicked.connect(self.getCheckedCalid)
        self.exec()
        logging.debug("added {} item".format(i))

    def getCheckedCalid(self):
        for i in range(0, self.gui.verticalLayout.count()):
            item = self.gui.verticalLayout.itemAt(i)
            widget = item.widget()
            logging.debug("i'm watching {} item".format(widget))
            if type(widget) is QRadioButton and widget.isChecked():
                id = widget.objectName()[len("Radiobutton_"):]
                logging.debug("found {} id".format(id))
                self.__writeConf__(id)
                return
                # TODO: write the configuration file
        message = "empty list while getCheckedCalid"
        logging.error(message)
        raise BaseException(message)

    def __writeConf__(self, calid):
        path = os.path.join(self.configPath, "Configuration.ini")
        data = parser.getDict(path)
        elem = data["Calendar"]
        elem["calid"] = calid
        data["Calendar"] = elem
        parser.writedata(data, path)


class Credentials:
    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.credentialDir = self.baseDir + "/credentials"
        self.clientSecretFile = self.credentialDir + '/client_secret.json'  # string, File name of client secrets.
        self.clientScope = "https://accounts.google.com/o/oauth2/v2/auth"
        self.userScope = 'https://www.googleapis.com/auth/calendar'  # string or iterable of strings, scope(s) to request.
        self.userSecretFile = self.credentialDir + 'user_secret.json'
        self.applicationName = 'workTracker'

        self.credentials = self.__getUserSecret__()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def getService(self):
        if self.service is not None:
            return self.service
        else:
            raise BaseException("non ce l'ho")

    def __getUserSecret__(self):
        credentialFile = os.path.join(self.credentialDir, 'user_secret.json')
        store = oauth2client.file.Storage(credentialFile)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(filename=self.clientSecretFile, scope=self.userScope)
            flow.user_agent = self.applicationName
            credentials = tools.run_flow(flow, store)
            logging.debug('Storing credentials to {}'.format(credentialFile))
        return credentials

    def __getClientSecret__(self):
        # client_id =
        # response_type = "token"
        credentialFile = os.path.join(self.credentialDir, 'client_secret_try.json')
        store = oauth2client.file.Storage(credentialFile)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(filename=self.userSecretFile, scope=self.clientScope)
            flow.user_agent = self.applicationName
            credentials = tools.run_flow(flow, store)
            logging.debug('Storing credentials to {}'.format(credentialFile))
        return credentials


class Calendar:
    def __init__(self, baseDir, passedService):
        self.service = passedService

        self.calid = self._confLoading(baseDir)

        self.events = []

    def getEventById(self, id):
        for event in self.events:
            if event.key == id:
                return event
        raise BaseException("this id doesn't exists")

    def _patchEvent(self, key, patch):
        updated_event = self.service.events().patch(calendarId=self.calid, eventId=key, body=patch).execute()
        logging.debug(updated_event)

    def getEvents(self):
        return self.events

    def fill(self, startDate, endDate):
        self.events = self._downloadEvents(startDate, endDate)

    # def getToPayEvents(self):
    #     res = []
    #     for event in self.events:
    #         if event.payed is False:
    #             res.append(event)
    #     return res

    def payedEvents(self, events):
        for event in events:
            patch = {'summary': "[ payed ] " + event.client}
            self._patchEvent(event.key, patch)

    def _confLoading(self, configPath):
        path = os.path.join(configPath, "Configuration.ini")
        data = parser.getList(path, "Calendar")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == 'calid'.upper() and i[1].upper() != "none".upper():
                    return i[1]
            raise calidNotFoundException("calid not found in {}".format(configPath))

    def _downloadEvents(self, startDate=None, endDate=None):
        if startDate is None:
            startDate = datetime.datetime.utcnow() - datetime.timedelta(weeks=8)
        if endDate is None:
            endDate = datetime.datetime.utcnow()
        if type(startDate) is datetime.datetime and type(endDate) is datetime.datetime:
            startDateRaw = startDate.isoformat() + 'Z'
            endDateRaw = endDate.isoformat() + 'Z'
        else:
            raise BaseException("Wrong date type {}".format(startDate))
        eventsResult = self.service.events().list(calendarId=self.calid, timeMin=startDateRaw, timeMax=endDateRaw,
                                                  singleEvents=True, orderBy='startTime', ).execute()

        rawEvents = eventsResult.get('items', [])
        events = []

        for rawEvent in rawEvents:
            start = rawEvent['start'].get('dateTime', rawEvent['start'].get('date'))
            key = rawEvent['id']
            try:
                start = DateTime(rawEvent['start'].get('dateTime'))
                end = DateTime(rawEvent['end'].get('dateTime'))
                duration = (end - start) * 24
                if duration < 1:
                    duration = 0.00
            except BaseException as E:
                logging.debug("{} \\ while creation duration time of {}".format(E, key))
                duration = 0.00
            try:
                description = rawEvent['description']
            except BaseException as E:
                logging.debug("{} \\ while catching description from {}".format(E, key))
                description = None
                pass
            if "[ payed ]" not in rawEvent['summary']:
                event = Events(date=start.Date(), client=rawEvent['summary'].rstrip(" "), description=description,
                               duration=duration,
                               payed=False, key=key)
            else:
                event = Events(date=start.Date(), client=rawEvent['summary'].lstrip("[ payed ]").rstrip(" "),
                               description=description,
                               duration=duration, payed=True, key=key)
            events.append(event)
        return events
