from datetime import datetime

from pypandoc import convert_text as convert

import parser


def _reg_modifier(regex, hours, number):
    regex['$data^'] = str(datetime.utcnow().date())
    regex['$innr^'] = str(datetime.utcnow().year) + "/" + number
    howmuch = regex['$howperhour^'] * hours
    regex['$howmuch^'] = str(howmuch)
    return regex


def _config(configPath):
    """
    Private function that load the config file
    :param configPath: config file path
    :return:
    """
    data = parser.get_list(configPath, "Invoices")

    'If you give a correct configuration i\'load that from your file'

    if data is not None:
        for i in data:
            if i[0].upper() == "output".upper():
                return i[1]
    else:
        raise BaseException("no {} file here".format(configPath))


def _read_model(model_path):
    """
    Private function that allow to read the tex model file
    :param model_path: tex model path
    :return:
    """
    texfile = open(model_path, 'r')
    rawTex = texfile.read()
    return rawTex.split("\n")


def _load_args(clientsPath, invoiceClient):
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


class invoice_creator:  # TODO: create a preview interface, use a tex library
    def __init__(self, passedPath, events, client):
        """
        Invoice creator constructor
        :param passedPath:
        :param events:
        :param client:
        """
        # Invoice creation and compiling regex[reg]iable
        self.invoiceNumber = str(0)
        self.invoiceName = "invoice_"+str(datetime.utcnow().year) + "_" + self.invoiceNumber+".pdf"
        self.cmd = None
        self.cmdArgs = ""
        self.invoicesPath = None
        self._modelTex = []
        self.final_tex = []
        self.final_html = []
        self.invoiceClient = client

        # Configuration regex[reg]iable
        self.basePath = passedPath
        configPath = self.basePath + "/Configuration.ini"
        model_path = self.basePath + "/invoice/model.tex"
        self.clientsPath = self.basePath + "/Clients.ini"
        self.invoicesPath = _config(configPath)

        # proceed to read model tex file
        self._modelTex = _read_model(model_path)

        # now I can load
        self._create_invoice(events)

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
        regex = _load_args(self.clientsPath, self.invoiceClient)  # loading invoices args
        regex = _reg_modifier(regex, hours, self.invoiceNumber)
        self.final_tex = []
        for line in self._modelTex:
            if line.find("$") != -1:
                for reg in regex.keys():
                    if reg in line:
                        line = line.replace(reg, regex[reg])
                        break
            self.final_tex.append(line)

    def write(self):
        """
        Function that allow to write this invoice
        :return:
        """
        # TODO: remember to update a datasheet
        file = self.invoicesPath + "/" + self.invoiceClient + ".tex"
        with open(file, 'w') as texfile:
            for line in self.final_tex:
                texfile.write(line + "\n")

    def compiling(self):
        """
        Old method to write the pdf file from a tex source using an external exec
        :return:
        """
        final_tex = ""
        for elem in self.final_tex:
            final_tex = final_tex + "\n" + elem
        # self.final_html = convert(source=final_tex, to="html", format="tex") # TODO: let this shit works
        # print(self.final_tex)
        convert(source=final_tex, format="tex", to="pdf", outputfile=self.invoicesPath+self.invoiceName)
        # tex = TeX()
        # tex.input(self.finalTex)
        # file = Base.Command.invoke(self, self.finalTex)
        # print(tex)
        # newpid = os.fork()
        # if not newpid:
        #     try:
        #         os.execlp('./pdflatex.sh', './pdflatex.sh', self.basePath + "/ciaone.tex")
        #     except Exception as E:
        #         logging.error("Error \"{}\" while compiling tex".format(E))
