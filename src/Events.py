class Events(object):
    date = None
    duration = None
    description = None
    client = None
    payed = None
    key = None

    def __init__(self, date, duration, description, client, payed, key):
        self.date = date
        self.duration = duration
        self.description = description
        self.client = client
        self.payed = payed
        if key == None:
            return Exception
        else:
            self.key = key