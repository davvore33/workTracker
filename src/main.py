import datetime
import os
import logging
import lastDateFinder
from CalendarReader import Calendar
from DatasheetCreator import datasheetcreator as csv
from MarkdownCreator import markdownCreator as md

# location finder
from TexCreator import texCreator
from dbAccess.calendarDb import calendarDb

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)


def main():
    # db = calendarDb(BASE_DIR)
    # startdate = lastDateFinder.getDate(db)
    try:
        cal = Calendar(BASE_DIR)
    except BaseException as E:
        logging.error("{} \\ while opening calendar".format(E))
        exit()

    try:
        cal.fill(startdate=None)
    except BaseException as E:
        logging.error("{} \\ while filling calendar".format(E))
        pass

    startDate = datetime.datetime.utcnow() - datetime.timedelta(weeks=2)
    endDate = datetime.datetime.fromtimestamp(0)

    try:
        cal.payedEvents(startDate, endDate)
    except BaseException as E:
        logging.error("{} \\ paying calendar".format(E))
        pass

    fileCreation(cal)


def fileCreation(cal):
    events = cal.getEvents()

    csv1 = csv()
    csv1.writecsv(events)
    md1 = md()
    md1.write(events)
    tex = texCreator(BASE_DIR)
    tex.write(events)
    try:
        tex.compiling()
    except Exception as E:
        logging.error("Error {} while writing {} tex file".format(E, tex))


if __name__ == '__main__':
    main()
