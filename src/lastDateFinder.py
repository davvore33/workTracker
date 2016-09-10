import logging
from datetime import datetime, timezone

# This class try to find last time that u have checked ur file

def getDate(db):
    try:
        Event = db.getLast()
        splittedDate = Event.date.split('/')
        return datetime(day=int(splittedDate[2]), month=int(splittedDate[1]), year=int(splittedDate[0]))
    except Exception as E:
        logging.error("{} while trying to cath last event".format(E))
        return datetime.fromtimestamp(0)
