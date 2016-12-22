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


# Exception loaded when there's no calid into the config
class CalidNotfoundexception(BaseException):
    def __init__(self, args):
        super(self)
        logging.error(args)


class SetCalId(QDialog):
    def __init__(self, configPath, service):
        """
        calid set constructor
        :param configPath:
        :param service:
        """
        super(SetCalId, self).__init__(flags=None)
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
                logging.debug("added {} item".format(i))
        ok, canc = self.gui.buttonBox.buttons()
        ok.clicked.connect(self._get_checked_calid)
        self.exec()

    def _get_checked_calid(self):
        """
        Function that set the calid chosen
        :return:
        """
        for i in range(0, self.gui.verticalLayout.count()):
            item = self.gui.verticalLayout.itemAt(i)
            widget = item.widget()
            logging.debug("i'm watching {} item".format(widget))
            if type(widget) is QRadioButton and widget.isChecked():
                id = widget.objectName()[len("Radiobutton_"):]
                logging.debug("found {} id".format(id))
                self._write_conf(id)
                return
        message = "empty list while _get_checked_calid"
        logging.error(message)
        raise BaseException(message)

    def _write_conf(self, calid):
        """
        Private function needed to save the calid into the credential file
        :param calid: calid to save
        :return:
        """
        path = os.path.join(self.configPath, "Configuration.ini")
        data = parser.get_dict(path)
        elem = data["Calendar"]
        elem["calid"] = calid
        data["Calendar"] = elem
        parser.write_data(data, path)


class Credentials:
    def __init__(self, baseDir):
        """
        Credentials constructor
        :param baseDir:
        """
        self.baseDir = baseDir
        self.credentialDir = self.baseDir + "/credentials"
        if not os.path.exists(self.credentialDir):
            os.makedirs(self.credentialDir)
        self.clientSecretFile = self.credentialDir + '/client_secret.json'  # string, File name of client secrets.
        self.clientScope = "https://accounts.google.com/o/oauth2/v2/auth"
        self.userScope = 'https://www.googleapis.com/auth/calendar'
        # string or iterable of strings, scope(s) to request.
        self.userSecretFile = self.credentialDir + 'user_secret.json'
        self.applicationName = 'workTracker'

        self.credentials = self._get_user_secret()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def get_service(self):
        """
        Function that allow to get the service initialized by this class
        :return: service
        """
        if self.service is not None:
            return self.service
        else:
            raise BaseException("No service founded")

    def _get_user_secret(self):
        """
        Function that allow to get the google client secret
        :return:
        """
        credentialFile = os.path.join(self.credentialDir, 'user_secret.json')
        store = oauth2client.file.Storage(credentialFile)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(filename=self.clientSecretFile, scope=self.userScope)
            flow.user_agent = self.applicationName
            credentials = tools.run_flow(flow, store)
            logging.debug('Storing credentials to {}'.format(credentialFile))
        return credentials

    def _get_client_secret(self):  # TODO: makes this work properly
        """
        Function that allow to get the google client secret
        :return: google client secret
        """
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
        """
        Calendar constructor
        :param baseDir: where the project is located
        :param passedService: services needed to use google calendar
        """
        self.service = passedService

        self.cal_id = self._conf_loading(baseDir)

        self.events = []

    def get_event_by_id(self, key):
        """
        Function that allow to return a particular event
        :param key: which event to get
        :return: the event
        """
        for event in self.events:
            if event.key == key:
                return event
        raise BaseException("this id doesn't exists")

    def _patch_event(self, key, patch):
        """
        Private function that allot to modify events
        :param key: event to patch
        :param patch: what have to be modified
        :return:
        """
        updated_event = self.service.events().patch(calendarId=self.cal_id, eventId=key, body=patch).execute()
        logging.debug(updated_event)

    def get_events(self):
        """
        Function that return events of this calendar
        :return: events of this calendar
        """
        return self.events

    def pay_events(self, events):
        """
        Function that set "payed" status to passed events
        :param events: events to set as payed
        :return:
        """
        for event in events:
            patch = {'colorId': "11"}
            # patch = {'summary': "[ payed ] " + event.client} old way
            self._patch_event(event.key, patch)

    @staticmethod
    def _conf_loading(configPath):
        """
        Private function that allow to load your config file
        :param configPath: config file path
        :return:
        """
        path = os.path.join(configPath, "Configuration.ini")
        data = parser.get_list(path, "Calendar")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == 'calid'.upper() and i[1].upper() != "none".upper():
                    return i[1]
            raise CalidNotfoundexception("calid not found in {}".format(configPath))

    def download_events(self, startDate=None, endDate=None):
        """
        Function that allow to download events from your google calendar
        :param startDate: download from this date
        :param endDate: downloadload to this date
        :return: list of Events
        """
        if startDate is None:
            startDate = datetime.datetime.utcnow() - datetime.timedelta(weeks=8)
        if endDate is None:
            endDate = datetime.datetime.utcnow()
        if type(startDate) is datetime.datetime and type(endDate) is datetime.datetime:
            startDateRaw = startDate.isoformat() + 'Z'
            endDateRaw = endDate.isoformat() + 'Z'
        else:
            raise BaseException("Wrong date type {}".format(startDate))
        eventsResult = self.service.events().list(calendarId=self.cal_id, timeMin=startDateRaw, timeMax=endDateRaw,
                                                  singleEvents=True, orderBy='startTime', ).execute()

        rawEvents = eventsResult.get('items', [])
        events = []

        # Format a list of dictionary to a list of Events
        for rawEvent in rawEvents:
            event = None
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
            if 'colorId' in rawEvent:
                if '11' in rawEvent['colorId']:
                    event = Events(date=start.Date(), client=rawEvent['summary'].rstrip(" "),
                                   description=description,
                                   duration=duration,
                                   payed=True, key=key)
            else:
                event = Events(date=start.Date(), client=rawEvent['summary'].lstrip("[ payed ]").rstrip(" "),
                               description=description,
                               duration=duration, payed=False, key=key)
            events.append(event)
        self.events = events
