import logging

from docutils import core, io

import os

import parser


class texCreator:
    def __init__(self, passedPath):
        self.modelName = None
        self.cmdPDF = None
        self.cmdPDFargs = ""
        self.basePath = passedPath
        self.invoicesPath = None
        self.tex = []

        configPath = self.basePath + "/Configuration.ini"
        self.clientspath = self.basePath + "/Clients.ini"

        self.config(configPath)
        try:
            self.read()
        except Exception as E:
            logging.error("Error {} reading {}".format(self.modelName, E))

    def write(self, args):
        howmuch = 0
        for event in args:
            howmuch = howmuch + float(event.duration) * 12.5
        regex = [('_incname_', "EveryNet di Federico Scarpa"),
                 ('_incaddress_', "Via Vincenzo Magnanini 1"),
                 ('_incaddress2_', "Cap. 42015 Correggio \(RE\)"),
                 ('_incpi_', "02009870359"),
                 ('_howmuch_', str(howmuch)),
                 ('_description_', "sono stati pagati {} per un totale di {} ore".format(howmuch, howmuch / 12.5)), ]
        # self.__gimmeargs__("EveryNet di Federico Scarpa", args) TODO: uses this stuff
        texComplete = []
        for line in self.tex:
            for (reg, var) in regex:
                if reg in line:
                    line = line.replace(reg, var)
            texComplete.append(line)
        with open(self.invoicesPath + "/" + "ciaone.tex", 'w') as texfile:
            for line in texComplete:
                texfile.write(line + "\n")

    def read(self):
        try:
            texfile = open(self.invoicesPath + "/" + self.modelName, 'r')
            rawTex = texfile.read()
            self.tex = rawTex.split("\n")
        except IOError as E:
            logging.error("{} \\ during openoing {}".format(E, texfile))

    def __gimmeargs__(self, cliente, args):
        data = parser.getdata(self.clientspath, cliente)

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == "dir".upper():
                    self.basePath = i[1]
                elif i[0].upper() == "cmdPDF".upper():
                    cose = i[1].split(' ')
                    self.cmdPDF = cose.pop(0)  # I'm removing the cmd modelName
                    for cosa in cose:
                        self.cmdPDFargs = self.cmdPDFargs + " " + cosa  # in this way the otherone will be the arguments
                elif i[0].upper() == "file".upper():
                    self.modelName = i[1]

    def compiling(self):
        newpid = os.fork()
        if not newpid:
            try:
                os.execlp('./pdflatex.sh', './pdflatex.sh', self.basePath + "/ciaone.tex")
            except Exception as E:
                logging.error("Error \"{}\" while compiling tex".format(E))

    def config(self, configPath):
        data = parser.getdata(configPath, "Invoices")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == "dir".upper():
                    self.invoicesPath = self.basePath + i[1]
                elif i[0].upper() == "cmdPDF".upper():
                    cose = i[1].split(' ')
                    self.cmdPDF = cose.pop(0)  # I'm removing the cmd modelName
                    for cosa in cose:
                        self.cmdPDFargs = self.cmdPDFargs + " " + cosa  # in this way the otherone will be the arguments
                elif i[0].upper() == "file".upper():
                    self.modelName = i[1]
