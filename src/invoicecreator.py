import csv
import os
from datetime import datetime

import logging

# import plasTeX.Base as Base
# import plasTeX.TeX as TeX
# from pypandoc import convert_text as convert

import parser


def _config(configPath, type):
    """
    Private function that load the config file
    :param configPath: config file path
    :return:
    """
    data = parser.get_list(configPath, type)

    'If you give a correct configuration i\'load that from your file'
    if type is "Invoices":
        if data is not None:
            for i in data:
                if i[0].upper() == "output".upper():
                    return i[1]
        else:
            raise BaseException("no {} file here".format(configPath))
    elif type is "InvoiceReports":
        if data is not None:
            res = dict()
            for i in data:
                res[i[0]] = i[1]
            return res
        else:
            raise BaseException("no {} file here".format(configPath))
        

class InvoiceCreator:  # TODO: create a preview interface, use a tex library
    def __init__(self, basePath, events, client):
        """
        Invoice creator constructor
        :param passedPath:
        :param events:
        :param client:
        """
        # Invoice creation and compiling regex[reg]iable
        self.tab = InvoiceReport(basePath)
        self.invoiceNumber = self.tab.new_number()
        self.invoiceYear = datetime.utcnow().year
        self.invoiceName = "invoice_" + str(self.invoiceYear) + "_" + str(self.invoiceNumber)
        self.invoiceDate = datetime.utcnow().date()
        self.cmd = None
        self.cmdArgs = ""
        self.invoicesPath = None
        self._modelTex = []
        self.final_tex = []
        self.final_html = []
        self.invoiceClient = client

        # Configuration regex[reg]
        configPath = basePath + "/Configuration.ini"
        model_path = basePath + "/invoice/model.tex"
        self.clientsPath = basePath + "/Clients.ini"
        self.invoicesPath = _config(configPath, "Invoices")

        # proceed to read model tex file
        self._modelTex = self._read_model(model_path)

        # now I can load
        try:
            self._create_invoice(events)
        except BaseException as E:
            logging.error("Error \"{}\" while compiling tex".format(E))

    def _create_invoice(self, events):
        """
        Private function that allow to create an invoice from events passed
        :param events: source  evens
        :return:
        """
        if self._modelTex is None:
            raise BaseException("give me the model")
        hours = 0
        for event in events:
            hours += float(event.duration)
        regex = self._load_args(self.clientsPath, self.invoiceClient)  # loading invoices args
        try:
            description = self._description_appender(events)
        except BaseException as E:
            logging.error(E)
            raise
        regex = self._reg_modifier(regex, hours, self.invoiceYear, self.invoiceNumber, description)
        self.final_tex = []
        for line in self._modelTex:
            if line.find("$") != -1:
                for reg in regex.keys():
                    if reg in line:
                        line = line.replace(reg, regex[reg])
                        break
            self.final_tex.append(line)

    def _reg_modifier(self, regex, hours, year, number, description):
        regex['$data^'] = str(self.invoiceDate)
        regex['$innr^'] = str(year) + "/" + str(number)
        howmuch = regex['$howperhour^'] * hours
        regex['$howmuch^'] = str(howmuch)
        regex['$description^'] = description
        return regex

    def _read_model(self, model_path):
        """
        Private function that allow to read the tex model file
        :param model_path: tex model path
        :return:
        """
        texfile = open(model_path, 'r')
        rawTex = texfile.read()
        return rawTex.split("\n")

    def _load_args(self, clientsPath, invoiceClient):
        """
        Private function that allow to read the client dictionary args
        :return:
        """
        data = parser.get_list(clientsPath, invoiceClient)
        res = dict()

        if data is not None:
            for i in data:
                if i[0].upper() == "$incname^".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "$incaddress^".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "$incaddress2^".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "$incpi^".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "$howperhour^".upper():
                    res[i[0]] = float(i[1])
                elif i[0].upper() == "$description^".upper():
                    res[i[0]] = i[1]
            return res
        else:
            raise BaseException("this client doesn't exist")

    def _description_appender(self, events):
        description = str()
        for event in events:
            if event.description is not None:
                description += str(event.description)
        if description is not None:
            return description
        else:
            return "Produzione progetti"

    # def write(self):
    #     """
    #     Function that allow to write this invoice
    #     :return:
    #     """
    #     # TODO: remember to update a datasheet
    #     file = self.invoicesPath + "/" + self.invoiceClient + ".tex"
    #     with open(file, 'w') as texfile:
    #         for line in self.final_tex:
    #             texfile.write(line + "\n")

    def compiling(self, basePath):
        """
        Old method to write the pdf file from a tex source using an external exec
        :return:
        """
        final_tex = ""
        for elem in self.final_tex:
            final_tex = final_tex + "\n" + elem

        self._compiling_pdflatex(basePath, final_tex)
        self.tab.update(self.invoiceNumber, )

    # def _compiling_pandoc(self):
    #     self.final_html = convert(source=final_tex, to="html", format="tex") # TODO: let this shit works
    #     print(self.final_tex)
    #     convert(source=final_tex, format="tex", to="pdf", outputfile=self.invoicesPath + self.invoiceName)
    #     tex = TeX()
    #     tex.input(self.final_tex)
    #     file = Base.Command.invoke(self, self.final_tex)

    def _compiling_pdflatex(self, basePath, final_tex):

        file = self.invoiceName + ".tex"

        with open(basePath + file, 'w', newline='') as texFile:
            texFile.write(final_tex)

        newpid = os.fork()
        if not newpid:
            os.execlp('./pdflatex.sh', './pdflatex.sh', basePath, file)

        os.remove(basePath+file)

        logging.debug("I've compiled {}".format(file))


class InvoiceReport:
    def __init__(self, basePath):
        self.tab = []
        configPath = basePath + "/Configuration.ini"

        conf = _config(configPath, "InvoiceReports")
        self.filepath = conf['filepath']
        self.filename = conf['filename']
        self._report_open()

    def update(self, Number, Date, Howmuch):
        for tabRow in self.tab:
            if Number is tabRow['Number']:
                raise BaseException("{} invoice already exists".format(Number))

        self._report_update(Number, Date, Howmuch)

    def _report_update(self, number, date, howmuch):
        with open(self.filepath + self.filename, 'wa', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(number, date, howmuch)

    def _report_open(self):
        titles = None
        with open(self.filepath + self.filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                tabRow = dict()
                if titles is None:
                    titles = row[0].split(',')
                else:
                    values = row[0].split(',')
                    for value in values:
                        tabRow[titles[values.index(value)]] = value
                    self.tab.append(tabRow)

    def new_number(self):
        tabcpy = self.tab
        return int(tabcpy.pop()['Number'].split('/')[1]) + 1
