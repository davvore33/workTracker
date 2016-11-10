import datetime


class spreadsheet_creator:
    def __init__(self, path, fileName):
        if path is not None:
            self.__path__ = path
        elif self.__path__ is None:
            raise IOError('You have to give me a path, please')

        if type(fileName) is datetime:
            self.__fileName__ = fileName.year + ".csv"
        elif type(fileName) is str and fileName.endswith(end=".csv"):
            self.__fileName__ = fileName
        elif fileName is None:
            self.__fileName__ = datetime.datetime.now().year + ".csv"
        else:
            raise IOError('What have you done?')

    def read_csv(self):
        with open(self.__path__, 'rb') as csvfile:
            spamreader = csvfile.read()
            print(spamreader)

    def write_csv_data(self, invoiceNumber, date, howmuch):
        with open(self.__path__ + "/" + self.__fileName__, 'w', newline='') as csvfile:
            csvfile.write("{},{},{}\n".format(invoiceNumber, date, howmuch))

    def write_append_csv(self, data):
        if type(data) is dict:
            with open(self.__path__ + "/" + self.__fileName__, 'wa', newline='') as csvfile:
                csvfile.write("{},{},{}\n".format(data.get('invoiceNumber'), data.get('date'),
                                                  data.get('howmuch')))
        else:
            raise IOError("wrong data type {}".format(type(data)))

