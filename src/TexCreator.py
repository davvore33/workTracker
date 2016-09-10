import logging

from docutils import core, io

import os

import parser

class texCreator:
    def __init__(self, configPath):
        self.name = None
        self.cmdPDF = None
        self.path = None
        self.tex = []

        print(configPath)
        configPath = configPath + "/Configuration.ini"

        self.config(configPath)
        try:
            self.read()
        except Exception as E:
            logging.error("Error {} reading {}".format(self.name, E))

    def write(self, args):
        self.tex[0].format(args[0])

    def read(self):
        with  open(self.path+"/"+self.name,'r') as texfile:
            rawTex = texfile.read()
            self.tex = rawTex.split("\n")
    
    def compiling(self):
        os.execl(self.cmdPDF, self.path+"/"+self.name)
        
    def config(self,configPath):
        data = parser.getdata(configPath, "Invoices")
        
        'If you give a correct configuration i\'load that from your file'
        
        if data is not None:
            for i in data:
                if i[0].upper() == "dir".upper():
                    self.path = i[1]
                elif i[0].upper() == "cmdPDF".upper():
                    self.cmdPDF = i[1]
                elif i[0].upper() == "file".upper():
                    self.name = i[1]

