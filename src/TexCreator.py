import logging

from docutils import core, io

import os

import parser


class texCreator:
    def __init__(self, configPath):
        self.modelName = None
        self.cmdPDF = None
        self.cmdPDFargs = ""
        self.path = None
        self.tex = []

        configPath = configPath + "/Configuration.ini"

        self.config(configPath)
        try:
            self.read()
        except Exception as E:
            logging.error("Error {} reading {}".format(self.modelName, E))

    def write(self, args):
        regex = [('_incname_', "EveryNet di Federico Scarpa"),
                 ('_incaddress_', "Via Vincenzo Magnanini 1"),
                 ('_incaddress2_', "Cap. 42015 Correggio \(RE\)"),
                 ('_incpi_', "xxxxxxxxxxxxxxxxxxxxxxxx"),
                 ('_howmuch_', "xx,xx"),
                 ('_description_',"boh il cazzo")]

        texComplete = []
        for line in self.tex:
            for (reg, var) in regex:
                if reg in line:
                    line = line.replace(reg, var)
            texComplete.append(line)
        with open(self.path + "/" + "ciaone.tex", 'w') as texfile:
            for line in texComplete:
                texfile.write(line + "\n")

    def read(self):
        with  open(self.path + "/" + self.modelName, 'r') as texfile:
            rawTex = texfile.read()
            self.tex = rawTex.split("\n")

    def compiling(self):
        newpid = os.fork()
        if not newpid:
            try:
                # os.execlp('pdflatex', 'pdflatex', '-synctex=1 -interaction=nonstopmode',
                #           '/home/matteo/Documenti/workTracker/invoice/ciaone.tex')
                # os.execlp(self.cmdPDF, self.cmdPDF, self.cmdPDFargs, self.path + "/" + self.modelName)
                os.execlp('./pdflatex.sh','./pdflatex.sh',self.path + "/ciaone.tex")
            except Exception as E:
                logging.error("Error \"{}\" while compiling tex".format(E))

    def config(self, configPath):
        data = parser.getdata(configPath, "Invoices")

        'If you give a correct configuration i\'load that from your file'

        if data is not None:
            for i in data:
                if i[0].upper() == "dir".upper():
                    self.path = i[1]
                elif i[0].upper() == "cmdPDF".upper():
                    cose = i[1].split(' ')
                    self.cmdPDF = cose.pop(0)  # I'm removing the cmd modelName
                    for cosa in cose:
                        self.cmdPDFargs = self.cmdPDFargs + " " + cosa  # in this way the otherone will be the arguments
                elif i[0].upper() == "file".upper():
                    self.modelName = i[1]
