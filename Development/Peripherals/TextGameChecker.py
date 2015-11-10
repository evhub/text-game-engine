#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# CHECKER made in 2012
# This program checks TextGameProcessor files for errors.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from TextGameFunctions import *

class main(base):

    def initialize(self, args):
        self.register(self.run, 200)

    def run(self):
        self.app.display("Analyzing World...")
        do = 0
        try:
            worldfile = open("World.txt", "rb")
            worlddata = readfile(worldfile)
            worldlines = worlddata.splitlines()
            for x in worldlines:
                if x != "":
                    if not x.startswith("#"):
                        worldlist = x.split(",")
                        itemlist = []
                        for y in xrange(3, len(worldlist)):
                            itemlist.append(worldlist[y])
                        try:
                            make(int(worldlist[0]), int(worldlist[1]), worldlist[2], itemlist)
                        except IndexError:
                            self.app.display("Not Enough Entries In World File At Line:", x)
                        except ValueError:
                            self.app.display("Invalid Coordinates In World File At Line:", x)
        except IOError:
            self.app.display("Fatal Error: Unable To Load World File.")

        else:
            self.app.display("Analyzing Options...")
            try:
                configfile = open("Options.txt", "rb")
            except IOError:
                self.app.display("Error: Unable To Load Options.")
            else:
                configdata = readfile(configfile)
                configlines = configdata.splitlines()
                for x in configlines:
                    if x != "":
                        if not x.startswith("#"):
                            optionentries = x.split("=")
                            go = optionentries[0]
                            try:
                                to = optionentries[1]
                            except IndexError:
                                to = ""
                                comps = []
                            else:
                                comps = to.split(",")
                            bools = ["stack"]
                            lists = ["northlist", "southlist", "eastlist", "westlist", "exitlist", "invlist", "statlist", "helplist", "healthlist", "waitlist", "looklist", "commandlist", "battlelist", "spawnlist", "armorlist", "powerlist", "deletelist"]
                            ints = ["maxhealth", "attack", "mana", "health"]
                            tuples = ["location"]
                            try:
                                if go in bools:
                                    if formatisyes(to):
                                        options[go] = True
                                elif go in lists:
                                    options[go] = comps
                                elif go in ints:
                                    options[go] = int(to)
                                elif go in tuples:
                                    options[go] = int(comps[0]), int(comps[1])
                                else:
                                    self.app.display("No Known Option", go, "In Options File At Line:", x)
                            except ValueError:
                                self.app.display("Invalid Value In Options File At Line:", x)
                            except IndexError:
                                self.app.display("Not Enough Values In Options File At Line:", x)
            finally:
                try:
                    configfile.close()
                except NameError:
                    self.app.display("Warning: No Options Data.")

            self.app.display("Analyzing Objects...")
            try:
                objectfile = open("Objects.txt", "rb")
            except IOError:
                self.app.display("Error: Unable To Load Objects.")
            else:
                objectdata = readfile(objectfile)
                objectlines = objectdata.splitlines()
                for x in objectlines:
                    if x != "":
                        if not x.startswith("#"):
                            item.attributes = {}
                            objectlist = x.split(",")
                            try:
                                put(objectlist[0], objectlist[1])
                            except IndexError:
                                self.app.display("Not Enough Entries In Objects File At Line:", x)
                            for y in xrange(2, len(objectlist)):
                                ylist = objectlist[y].split("=")
                                try:
                                    items[objectlist[0]].setatt(ylist[0],ylist[1])
                                except IndexError:
                                    self.app.display("Not Enough Values In Objects File At Line:", x, "And Area:", y)
            finally:
                try:
                    objectfile.close()
                except NameError:
                    self.app.display("Warning: No Object Data.")

            self.app.display("Analyzing Powers...")
            try:
                spellfile = open("Powers.txt", "rb")
            except IOError:
                self.app.display("Error: Unable To Load Powers.")
            else:
                spelldata = readfile(spellfile)
                spelllines = spelldata.splitlines()
                for x in spelllines:
                    if x != "":
                        if not x.startswith("#"):
                            tempspell = x.split(",")
                            powerlist = []
                            for y in xrange(3, len(tempspell)):
                                powerlist.append(tempspell[y])
                            try:
                                exist(tempspell[0],int(tempspell[1]),int(tempspell[2]),powerlist)
                            except IndexError:
                                self.app.display("Not Enough Entries In Powers File At Line:", x)
                            except ValueError:
                                self.app.display("Invalid Value In Powers File At Line:", x)
            finally:
                try:
                    spellfile.close()
                except NameError:
                    self.app.display("Warning: No Powers Data.")

            self.app.display("Analyzing File Compatibility...")

            acceptables = ["none", "item"]
            moblisters = ["pass", "agg"]
            for x in items:
                if items[x].itemtype in moblisters:
                    try:
                        items[x].attributes["health"]
                    except KeyError:
                        self.app.display("Data Error:", x, "Is Missing A Health Attribute.")
                    try:
                        items[x].attributes["damage"]
                    except KeyError:
                        self.app.display("Data Error:", x, "Is Missing A Damage Attribute.")
                elif items[x].itemtype not in acceptables:
                    self.app.display("Data Error:", x, "Has Invalid Type.")

            for x in world:
                for y in world[x].inventory:
                    try:
                        items[y]
                    except KeyError:
                        self.app.display("Data Error:", y, "Not Defined In Objects File.")

            for x in items:
                if "drop" in items[x].attributes:
                    for y in items[x].attributes["drop"].split(";"):
                        try:
                            items[y]
                        except KeyError:
                            self.app.display("Data Error:", y, "Not Defined In Objects File.")
                if "power" in items[x].attributes:
                    for y in items[x].attributes["power"].split(";"):
                        try:
                            spells[y]
                        except KeyError:
                            self.app.display("Data Error:", y, "Not Defined In Powers File.")

            self.app.display("Analysis Complete.")
            self.app.display("Perform What Task?")
            self.app.display("0 = Quit")
            self.app.display("1 = Find Unused Objects")
            self.app.display("2 = Find Unused Powers")
            do = 1

        finally:
            try:
                worldfile.close()
            except NameError:
                self.app.display("Fatal Error: No World Data.")

        while do == 1:
            task = self.get()
            try:
                task = int(task)
            except ValueError:
                self.app.display("Please Enter The Number Of A Task.")
            else:
                if task == 0:
                    do = 0
                    root.destroy()
                elif task == 1:
                    itemlist = []
                    for x in world:
                        for y in world[x].inventory:
                            itemlist.append(y)
                    for x in items:
                        if x in itemlist:
                            if "drop" in items[x].attributes:
                                for y in items[x].attributes["drop"].split(";"):
                                    itemlist.append(y)
                    done = 0
                    for x in items:
                        if x not in itemlist:
                            self.app.display("Unused Object:", x)
                            done = 1
                    if done == 0:
                        self.app.display("No Unused Objects.")
                elif task == 2:
                    powerlist = []
                    for x in items:
                        if "power" in items[x].attributes:
                            for y in items[x].attributes["power"].split(";"):
                                powerlist.append(y)
                    done = 0
                    for x in spells:
                        if x not in powerlist:
                            self.app.display("Unused Power:", x)
                            done = 1
                    if done == 0:
                        self.app.display("No Unused Powers.")
                else:
                    self.app.display("Invalid Task Number.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main("Analyzing...", "TextGameChecker").start()
