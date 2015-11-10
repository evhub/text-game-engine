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

from PythonPlus import *

class main(base):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("TextGameWorldEditor")
        self.app = displayer(self.root)
        self.box = texter(self.root)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.bind("<Return>", lambda event: self.load())
        self.root.bind("<Control-Tab>", lambda event: self.save())
        self.root.bind("<Control-g>", lambda event: self.goto())
        self.root.bind("<Control-l>", lambda event: self.locate())
        self.root.bind("<Control-s>", lambda event: self.up())
        self.root.bind("<Control-z>", lambda event: self.left())
        self.root.bind("<Control-x>", lambda event: self.down())
        self.root.bind("<Control-c>", lambda event: self.right())
        self.location = 0,0
        self.defroom = openphoto("Room.gif")
        self.ysize = self.defroom.height()
        self.xsize = self.defroom.height()
        try:
            self.back = openphoto("Map.gif")
        except:
            pass
        else:
            self.app.new(self.back)
        try:
            self.active = openphoto("Active.gif")
        except:
            self.doactive = 0
        else:
            self.doactive = 1
        try:
            self.worldfile = open("World.txt", "r+b")
        except IOError:
            self.worldfile = open("World.txt", "wb")
            self.worldfile = open("World.txt", "r+b")
        self.box.display(readfile(self.worldfile))
        self.identifiers = []
        self.load()
        self.register(lambda: popup("info", "Controls:\nControl + Tab = Save\nControl + g = Go To Location\nControl + l = Get Location\nControl + s = Up\nControl + z = Left\nControl + x = Down\nControl + c = Right", "Help"), 200)

    def load(self):
        global world
        world = {}
        worldlines = self.box.output().splitlines()
        for x in worldlines:
            if x != "":
                if not x.startswith("#"):
                    worldlist = x.split(",")
                    try:
                        world[int(worldlist[0]), int(worldlist[1])] = worldlist[2]
                    except IndexError:
                        popup("warning", "Not Enough Entries In World File At Line: "+x, "Error")
                    except ValueError:
                        popup("warning", "Invalid Coordinates In World File At Line: "+x, "Error")
        self.photos = {}
        for x,y in world:
            try:
                xphoto = openphoto(world[x,y]+".gif")
            except:
                pass
            else:
                self.photos[world[x,y]] = xphoto
        self.render()

    def render(self, width=800, height=400):
        for x in self.identifiers:
            self.app.clear(x)
        self.identifiers = []
        locx, locy = self.location
        top, side = width/self.xsize, height/self.ysize
        centerx, centery = top/2, side/2
        newx = 0
        for x in xrange(0, top+1):
            newx += self.xsize
            newy = 0
            for y in reversed(xrange(0, side+1)):
                newy += self.ysize
                try:
                    name = world[x+locx-centerx, y+locy-centery]
                except KeyError:
                    pass
                else:
                    if name in self.photos:
                        self.identifiers.append(self.app.new(self.photos[name], newx, newy))
                    elif self.doactive == 1:
                        if (locx, locy) == (x+locx-centerx, y+locy-centery):
                            self.identifiers.append(self.app.new(self.active, newx, newy))
                        else:
                            self.identifiers.append(self.app.new(self.defroom, newx, newy))
                    else:
                        self.identifiers.append(self.app.new(self.defroom, newx, newy)) 

    def up(self):
        self.move("north")
        self.render()

    def down(self):
        self.move("south")
        self.render()

    def left(self):
        self.move("west")
        self.render()

    def right(self):
        self.move("east")
        self.render()

    def save(self):
        writefile(self.worldfile, self.box.output())
        popup("Info", "File Saved.")

    def goto(self):
        try:
            x = int(popup("integer", "X-Coordinate:", "Location"))
            y = int(popup("integer", "Y-Coordinate:", "Location"))
        except ValueError:
            popup("warning", "Invalid Coordinate.", "Error")
        else:
            self.location = x,y
            self.render()

    def locate(self):
        try:
            world[self.location]
        except KeyError:
            displayer = "Current Coordinates: "+str(self.location)
        else:
            displayer = "Current Coordinates: "+str(self.location)+"\nAt Place: "+world[self.location]
        popup("info", displayer, "Location")

    def move(self, direction):
        locx, locy = self.location
        if direction == "north":
            self.location = locx, locy + 1
        elif direction == "south":
            self.location = locx, locy - 1
        elif direction == "east":
            self.location = locx + 1, locy
        elif direction == "west":
            self.location = locx - 1, locy

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main().start()
