#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# EDITOR made in 2012
# This program serves as a graphical editor for the World.txt file for the TextGameProcessor.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *

class main(base):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("TextGameObjectsEditor")
        self.box = texter(self.root, 100, 40)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.bind("<Return>", lambda event: self.load())
        self.root.bind("<Control-Tab>", lambda event: self.save())
        try:
            self.objectfile = open("Objects.txt", "r+b")
        except IOError:
            self.objectfile = open("Objects.txt", "wb")
            self.objectfile = open("Objects.txt", "r+b")
        self.box.display(readfile(self.objectfile))
        self.load()
        self.register(lambda: popup("info", "Controls:\nControl + Tab = Save", "Help"), 200)

    def load(self):
        objectlines = self.box.output().splitlines()
        for x in objectlines:
            if x != "":
                if not x.startswith("#"):
                    objectlist = x.split(",")
                    try:
                        test = objectlist[0], objectlist[1]
                    except IndexError:
                        popup("warning", "Not Enough Entries In Objects File At Line: "+x, "Error")
                    for y in xrange(2, len(objectlist)):
                        ylist = objectlist[y].split("=")
                        try:
                            test = ylist[0], ylist[1]
                        except IndexError:
                            popup("warning", "Not Enough Values In Objects File At Line: "+x+" And Area: "+y, "Error")

    def save(self):
        writefile(self.objectfile, self.box.output())
        popup("Info", "File Saved.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main().start()
