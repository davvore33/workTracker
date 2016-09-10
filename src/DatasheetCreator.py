import csv
class datasheetcreator:
    def writecsv(self, args=None):
        with open('datasheet.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Day','Duration','Payed'])
            for event in args:
                passed = (event.date, round(event.duration,2), event.payed)
                spamwriter.writerow(passed)