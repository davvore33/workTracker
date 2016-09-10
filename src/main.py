import os
import logging
import lastDateFinder
from CalendarReader import Calendar
from DatasheetCreator import datasheetcreator as csv
from MarkdownCreator import markdownCreator as md

#location finder
from TexCreator import texCreator
from dbAccess.calendarDb import calendarDb

base = os.path.abspath(__file__)
base, null = os.path.split(base)
BASE_DIR = os.path.dirname(base)

def main():
    db = calendarDb(BASE_DIR)
    startdate = lastDateFinder.getDate(db)
    try:
        cal = Calendar()
    except BaseException as E:
        logging.error("{}".format(E))
        exit()

    try:
        cal.fill(startdate)
    except BaseException as E:
        logging.error("{} while filling calendar".format(E))
        pass

    dbPopulation(cal,db)
    fileCreation(db)

    db.drop()


def dbPopulation(cal,db):
    events = cal.getObj()

    db.writeEvent(events)
    db.commit()

def fileCreation(db):

    events = db.getAllEvent()

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
