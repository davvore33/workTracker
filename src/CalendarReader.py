#!/usr/bin/env python3

from __future__ import print_function

import logging

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from DateTime import DateTime

from Events import Events


def getCalendar(service):  # TODO: create a calendar configuration interface, create a credential acquisition interface
    calendars = service.calendarList().list().execute()
    for i in calendars['items']:
        if i['accessRole'] == 'owner':
            if i['summary'] == 'Work':  # this represents my choice
                calid = i['id']
    return calid


class Calendar:
    def __init__(self, basedir):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'  # string or iterable of strings, scope(s) to request.
        self.CLIENT_SECRET_FILE = basedir + '/credentials/client_secret_818319143567-0sd9u05ih2halljjtof34i650893kl67.apps.googleusercontent.com.json'  # string, File name of client secrets.
        self.APPLICATION_NAME = 'prova'

        self.credentials = self.__downloadCredentials__()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

        self.calid = getCalendar(self.service)
        self.events = []

    def getEventById(self, id):
        for event in self.events:
            if event.key == id:
                return event
        raise BaseException("this id doesn't exists")

    def patchEvent(self, key, patch):
        updated_event = self.service.events().patch(calendarId=self.calid, eventId=key, body=patch).execute()
        logging.debug(updated_event)

    def getEvents(self):
        return self.events

    def fill(self, startDate=None):
        self.events = self.__downloadEvents__(startDate)

    def getToPayEvents(self):
        res = []
        for event in self.events:
            if event.payed is False:
                res.append(event)
        return res

    def payedEvents(self, events):
        for event in events:
            patch = {'summary': "[ payed ] " + event.client}
            self.patchEvent(event.key, patch)

    def __downloadCredentials__(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')  # TODO: sostitute with a path
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(filename=self.CLIENT_SECRET_FILE, scope=self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run(flow, store)
            logging.debug('Storing credentials to {}'.format(credential_path))
        return credentials

    def __downloadEvents__(self, startDate=None, endDate=None):
        if startDate is None:
            startDate = datetime.datetime.utcnow() - datetime.timedelta(weeks=26)

        if endDate is None:
            endDate = datetime.datetime.utcnow()

        startDateRaw = startDate.isoformat() + 'Z'
        endDateRaw = endDate.isoformat() + 'Z'

        eventsResult = self.service.events().list(
            calendarId=self.calid if self.calid is not None else 'primary', timeMin=startDateRaw, timeMax=endDateRaw,
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
