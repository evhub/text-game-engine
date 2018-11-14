#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# PROGRAM made in 2012
# This program serves as a crossover between nationstates.net and TextGameWorldCreator.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *
import xml.etree.ElementTree as et

class region(object):
    def __init__(self, weight):
        self.weight = int(weight)
        self.rooms = []
    def create(self, room):
        self.rooms.append(room)

class main(base):
    def initialize(self):
        self.app.display("Load What Nation State?")
        self.state = self.get()
        self.app.display("Loading...")
        self.register(self.load, 200)
    def load(self):
        request = "http://www.nationstates.net/cgi-bin/api.cgi?nation="+self.state+"&q=govt"
        for x in xrange(0, 69):
            request += "+censusscore-"+str(x)
        request += "&v=3"
        self.raw = download(request)
        self.tree = et.parse(self.raw[0])
        self.xmlroot = self.tree.getroot()
        self.e = evaluator()
        self.vars = self.e.variables
        for x in xrange(0, 11):
            self.vars[superformat(self.xmlroot[0][x].tag)] = float(self.xmlroot[0][x].text[:-1])
        for x in xrange(1, 70):
            self.vars["@"+str(x)] = float(self.xmlroot[x].text)
        self.app.display("Nation State Loaded.")
        self.app.display("Generating..")
        self.register(self.gen, 200)
    def gen(self):
        self.file = openfile("Parameters.txt")
        self.lines = readfile(self.file).splitlines()
        self.regions = []
        doregion = 0
        y = -1
        for x in self.lines:
            if x != "":
                if not x.startswith("#"):
                    if x.startswith("&"):
                        if self.e.test(x[1:], self.vars):
                            doregion = 1
                        else:
                            doregion = 0
                    elif x.startswith("%"):
                        if doregion == 1:
                            self.regions.append(region(float(self.e.calc(x[1:]))))
                            y += 1
                    else:
                        if doregion == 1:
                            self.regions[y].create(x)
        self.app.display("Generation Complete.")
        self.app.display("Write To What File?")
        self.filename = self.get()
        try:
            self.newfile = openfile(self.filename, "r+b")
        except IOError:
            self.newfile = openfile(self.filename, "wb")
        else:
            self.app.display("Overwrite File? [Y/n]")
            if formatisno(self.get()):
                self.newfile = openfile(self.filename, "r+b")
            else:
                self.writetype  = "wb"
        self.app.display("Writing To File...")
        self.register(self.write, 200)
    def write(self):
        self.writer = ""
        for x in self.regions:
            self.writer += "/ "+str(x.weight)+"\n"
            for y in x.rooms:
                self.writer += y+"\n"
            self.writer += "\n"
        writefile(self.newfile, self.writer[:-2])
        self.newfile.close()
        self.app.display("Wrote To File.")
        self.app.display("Press Enter To End.")
        self.get()
        self.root.destroy()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main(name="TextGameNationStates", message="Starting...").start()
