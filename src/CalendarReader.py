#!/usr/bin/env python3

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from DateTime import DateTime

from Events import Events


class Calendar:
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'  # string or iterable of strings, scope(s) to request.
    CLIENT_SECRET_FILE = '../credential/client_secret_818319143567-0sd9u05ih2halljjtof34i650893kl67.apps.googleusercontent.com.json'  # string, File name of client secrets.
    APPLICATION_NAME = 'prova'

    def __init__(self):
        self.credentials = self.getCredentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3',
                                       http=self.http)  # Construct a Resource for interacting with an API.
        # A Resource object with methods for interacting with the service.

        self.calid = self.getCalendar(self.service)
        self.events = []

    def fill(self, startdate):
        self.events = self.getEvents(self.calid, self.service, startdate)
        if not self.events:
            raise BaseException('No upcoming events found')

    def getObj(self):

        res = []

        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            try:
                start = DateTime(event['start'].get('dateTime'))
                end = DateTime(event['end'].get('dateTime'))
                duration = (end - start) * 24
                key = event['id']
                if duration < 1:
                    duration = 0.00
            except:
                duration = 0.00
            try:
                description=event['description']
            except:
                description=None
                pass
            event = Events(date=start.Date(), client=event['summary'], description=description,duration=duration, payed=False, key=key)
            res.append(event)
        return res

    def getCredentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')  # TODO: sostitute with a path
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(filename=Calendar.CLIENT_SECRET_FILE, scope=Calendar.SCOPES)
            flow.user_agent = Calendar.APPLICATION_NAME
            credentials = tools.run(flow, store)
            # print('Storing credentials to ' + credential_path)
        return credentials

    def getEvents(self, calid, service, startdate):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # gonna pass my calid or, eventually, primary calendar
        strdate = startdate.isoformat() + 'Z'
        eventsResult = service.events().list(
            calendarId=calid if calid is not None else 'primary', timeMin=strdate, singleEvents=True, timeMax=now,
            orderBy='startTime', ).execute()
        return eventsResult.get('items', [])

    def getCalendar(self, service):
        # print('Getting a list of calendars')
        calendars = service.calendarList().list().execute()
        for i in calendars['items']:
            if i['accessRole'] == 'owner':
                # print('summary ' + i['summary'])
                # print('id ' + i['id'])
                if i['summary'] == 'Work':  # this represents my choice
                    calid = i['id']
        return calid
