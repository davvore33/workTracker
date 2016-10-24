import logging
import tex

import os

import parser


class invoiceCreator:  # TODO: create a preview interface, use a tex library
    def __init__(self, passedPath, events, client):
        #Invoice creation and compiling variable
        self.modelName = None
        self.cmd = None
        self.cmdArgs = ""
        self.invoicesPath = None
        self.__modelTex__ = []
        self.finalTex = []
        self.invoiceClient = client

        # Configuration variable
        self.basePath = passedPath
        configPath = self.basePath + "/Configuration.ini"
        self.clientsPath = self.basePath + "/Clients.ini"
        self.__config__(configPath)

        try:
            self.__readModel__()
        except Exception as E:
            logging.error("Error {} reading {}".format(self.modelName, E))

        # now I can load
        self.__createInvoice__(events)

    def __createInvoice__(self, events):
        if self.__modelTex__ is None:
            raise BaseException("give me the model")
        hours = 0
        for event in events:
            hours += float(event.duration)
        regex = self.__loadArgs__()  # TODO: uses this stuff
        self.finalTex = []
        for line in self.__modelTex__:
            for (reg, var) in regex:
                if reg == "#howmuch":
                    var *= hours
                if reg in line:
                    line = line.replace(reg, var)
            self.finalTex.append(line)

    def __readModel__(self):
        try:
            texfile = open(self.invoicesPath + "/" + self.modelName, 'r')
            rawTex = texfile.read()
            self.__modelTex__ = rawTex.split("\n")
        except IOError as E:
            logging.error("{} \\ during opening {}".format(E, texfile))

    def __loadArgs__(self):
        data = parser.getdata(self.clientsPath, self.invoiceClient)
        res = dict()
        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == "#incname".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "#incaddress".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "#incaddress2".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "#incpi".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "#howmuch".upper():
                    res[i[0]] = i[1]
                elif i[0].upper() == "#description".upper():
                    res[i[0]] = i[1]
            return res
        else:
            raise BaseException("this client doesn't exist")

    def __config__(self, configPath):
        data = parser.getdata(configPath, "Invoices")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == "dir".upper():
                    self.invoicesPath = self.basePath + i[1]
                elif i[0].upper() == "cmdPDF".upper():
                    cose = i[1].split(' ')
                    self.cmd = cose.pop(0)  # I'm removing the cmd modelName
                    for cosa in cose:
                        self.cmdArgs = self.cmdArgs + " " + cosa  # in this way the otherone will be the arguments
                elif i[0].upper() == "file".upper():
                    self.modelName = i[1]
        else:
            raise BaseException("no {} file here".format(configPath))

    def write(self):
        with open(self.invoicesPath + "/" + self.invoiceClient + ".tex", 'w') as texfile:
            for line in self.finalTex:
                texfile.write(line + "\n")

    def compiling(self):
        # file = tex.latex2pdf(self.finalTex) # TODO: let this shit works
        # print(file)
        newpid = os.fork()
        if not newpid:
            try:
                os.execlp('./pdflatex.sh', './pdflatex.sh', self.basePath + "/ciaone.tex")
            except Exception as E:
                logging.error("Error \"{}\" while compiling tex".format(E))
