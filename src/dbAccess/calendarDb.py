import parser
from Events import Events
from dbAccess.sqlite import Database


class calendarDb(Database):
    columns = ('client', 'description', 'duration', 'payed', 'date', 'key')

    tablename = "calendar"

    def __init__(self, path):
        configPath = path + "/Configuration.ini"
        data = parser.getdata(configPath, "Database")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0] == "name":
                    name = i[1]
                elif i[0] == "dir":
                    dir = i[1]
            database = path + dir + name
            super().__init__(database=database)

    def insert(self, data, **kwargs):
        super().insert(table=self.tablename, columns=self.columns, data=data)

    def writeEvent(self, Events):
        """
        :param Calendar:
        :return:
        """
        for event in Events:
            date = event.date
            duration = event.duration
            description = event.description
            client = event.client
            payed = event.payed
            key = event.key
            self.insert(data=[(client, description, duration, payed, date, key)])

    def getAllEvent(self):
        rawEvents = super().get(table=self.tablename)
        if rawEvents is not None:
            events = []
            for rawEvent in rawEvents:
                events.append(Events(date=rawEvent[4], duration=rawEvent[2], description=rawEvent[1], client=rawEvent[0],
                                payed=rawEvent[3], key=rawEvent[5]))
            return events
        else:
            return None

    def getLast(self):
        sql = "select * from calendar ORDER BY key DESC LIMIT 1"
        listEvents = super().execute(sql)
        rawEvent = listEvents.pop()
        event = Events(date=rawEvent[4], duration=rawEvent[2], description=rawEvent[1], client=rawEvent[0],
                       payed=rawEvent[3], key=rawEvent[5])
        return event

    def searchEvent(self, where):
        return super().get(table=self.tablename, where=where)

    def drop(self):
        super.drop(self.tablename)