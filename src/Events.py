# TODO: change class, use a dictionary list to save entire events list
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
        if key is None:
            raise BaseException("can't give to me a none key")
        else:
            self.key = key