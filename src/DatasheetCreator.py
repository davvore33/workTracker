import csv


class datasheetcreator:
    def readcsv(self):
        with open('eggs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(", ".join(row))

    def writecsv(self, invoiceNumber, date, howmuch):
        with open('datasheet.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['invoiceNumber', 'date', 'howmuch'])
            spamwriter.writerow(invoiceNumber, date, howmuch)

    def writeappendcsv(self, invoiceNumber, date, howmuch):
        with open('datasheet.csv', 'wa', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(invoiceNumber, date, howmuch)
