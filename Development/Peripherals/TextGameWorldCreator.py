#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# PROGRAM made in 2012
# This program serves as a random generator for the World.txt file for the TextGameProcessor.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *
import random

class region(object):
    def __init__(self):
        self.rooms = {}
    def create(self, x, y, room):
        self.rooms[x,y] = room

class main(base):
    def initialize(self):
        try:
            self.places = openfile("Places.txt", "rb")
        except IOError:
            self.app.display("Unable To Load Places File.")
            self.app.display("Press Enter To End.")
            self.get()
            self.root.destroy()
        else:
            lines = readfile(self.places).splitlines()
            placelist = []
            y=-1
            for x in lines:
                if x != "":
                    if not x.startswith("#"):
                        if x.startswith("/"):
                            y+=1
                            placelist.append([])
                            x=x[1:].strip()
                            placelist[y].append(x)
                        else:
                            placelist[y].append(x.split(",",2))
            self.regions = {}
            self.weight = 0
            for x in placelist:
                weight = int(x[0])
                newregion = region()
                for y in xrange(1, len(x)):
                    newregion.create(int(x[y][0]), int(x[y][1]), x[y][2])
                self.regions[xrange(self.weight, self.weight+weight)] = newregion
                self.weight += weight
            self.app.display("Places Loaded.")
            self.app.display("World Height?")
            self.y = int(self.get())/2
            self.app.display("World Width?")
            self.x = int(self.get())/2
            self.app.display("Generating...")
            self.register(self.gen, 200)
    def gen(self):
        self.used = []
        self.file = ""
        for x,y in [(x,y) for x in xrange(-1*self.x, self.x) for y in xrange(-1*self.y, self.y)]:
            if (x,y) not in self.used:
                didgen = 0
                while didgen == 0:
                    choice = random.randrange(0,self.weight)
                    for z in self.regions:
                        if choice in z:
                            cangen = 1
                            for tx,ty in self.regions[z].rooms:
                                if (x+tx, y+ty) in self.used:
                                    cangen = 0
                                    break
                                elif x+tx >= self.x or y+ty >= self.y:
                                    cangen = 0
                                    break
                            if cangen == 1:
                                for tx,ty in self.regions[z].rooms:
                                    nx, ny = x+tx, y+ty
                                    self.used.append((nx, ny))
                                    if self.regions[z].rooms[tx,ty] != "":
                                        self.file += str(nx)+","+str(ny)+","+self.regions[z].rooms[tx,ty]
                                        self.file += "\n"
                                didgen = 1
                            break
        self.file = self.file[:-1]
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
        writefile(self.newfile, self.file)
        self.newfile.close()
        self.app.display("Wrote To File.")
        self.app.display("Press Enter To End.")
        self.get()
        self.root.destroy()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main(name="TextGameWorldCreator", message="Loading Places...").start()
