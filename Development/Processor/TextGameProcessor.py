#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# PROCESSOR made in 2012
# This program processes text game files into a playable game.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import md5

from TextGameFunctions import *

def startconsole(root, handler=None, message=None, name="PythonPlus", height=None):
    root.title(str(name))
    if height != None:
        app = console(root, message, height)
    else:
        app = console(root, message)
    root.bind("<Escape>", lambda event: root.destroy())
    root.bind("<MouseWheel>", app.scroll)
    if handler != None:
        box = entry(app)
        box.main.bind("<Control-z>", lambda event: box.main.delete(0, "end"))
        box.main.bind("<Return>", handler)
        return app, box
    else:
        return app

class main(base):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.domap = 0
        self.doactive = 0
        todo = ["Loading Images..."]
        try:
            self.defroom = openphoto("Room.gif")
        except:
            todo.append("Warning: Unable To Load Room Image.")
        else:
            self.ysize = self.defroom.height()
            self.xsize = self.defroom.height()
            self.domap = 1
            try:
                self.back = openphoto("Map.gif")
            except:
                todo.append("Warning: Unable To Load Map Image.")
            else:
                self.domap = 2
            try:
                self.active = openphoto("Active.gif")
            except:
                todo.append("Warning: Unable To Load Active Image.")
            else:
                self.doactive = 1
        if self.domap == 0:
            self.app, self.box = startconsole(self.root, self.handler, "Welcome To A Text Game Processor!\nLoading...", "Text Game Processor")
        else:
            self.app, self.box = startconsole(self.root, self.handler, "Welcome To A Text Game Processor!\nLoading...", "Text Game Processor", 15)
        for x in todo:
            self.app.display(x)
        if self.domap >= 1:
            self.mapper = displayer(self.root)
            self.photos = {}
            self.identifiers = []
        if self.domap == 2:
            self.mapper.new(self.back)
        self.returned = 0
        self.register(self.run, 200)

    def render(self, username, width=800, height=400):
        for x in self.identifiers:
            self.mapper.clear(x)
        self.identifiers = []
        locx, locy = players[username].location
        top, side = width/self.xsize, height/self.ysize
        centerx, centery = top/2, side/2
        newx = 0
        for x in xrange(0, top+1):
            newx += self.xsize
            newy = 0
            for y in reversed(xrange(0, side+1)):
                newy += self.ysize
                try:
                    name = world[x+locx-centerx, y+locy-centery].name
                except KeyError:
                    pass
                else:
                    if name in self.photos:
                        self.identifiers.append(self.mapper.new(self.photos[name], newx, newy))
                    elif self.doactive == 1:
                        if (locx, locy) == (x+locx-centerx, y+locy-centery):
                            self.identifiers.append(self.mapper.new(self.active, newx, newy))
                        else:
                            self.identifiers.append(self.mapper.new(self.defroom, newx, newy))
                    else:
                        self.identifiers.append(self.mapper.new(self.defroom, newx, newy))

    def assemble(self):
        for x,y in world:
            try:
                xphoto = openphoto(world[x,y].name+".gif")
            except:
                pass
            else:
                self.photos[world[x,y].name] = xphoto

    def playerturn(self, username,mobhealth,frozen,sacrifice,necrosis,burn):
        for x in spells:
            if spells[x].cooldown > 0:
                spells[x].cooldown -= 1
        turn = 1
        while turn == 1:
            self.app.display("What Do You Do?")
            move = self.get()
            fmove = superformat(move)

            if move in options["helplist"]:
                self.app.display("Battle Command List:", options["battlelist"])

            elif fmove == "attack":
                self.app.display("You Attack!")
                mobhealth -= players[username].attack
                turn = 0

            elif fmove.startswith("inspect "):
                itemname = ""
                for x in xrange(8,len(move)):
                    itemname += move[x]
                if itemname in players[username].inventory:
                    self.app.display("You Inspect The", itemname + ".")
                    for y in items[itemname].attributes:
                        if y == "damage":
                            self.app.display("It Deals", items[itemname].attributes[y], "Damage.")
                        elif y == "slot":
                            self.app.display("It Is Equiped In The", items[itemname].attributes[y], "Slot.")
                        elif y == "addhealth":
                            self.app.display("It Adds", items[itemname].attributes[y], "To Your Maximum Health.")
                        elif y == "addmana":
                            self.app.display("It Adds", items[itemname].attributes[y], "To Your Maximum Mana.")
                        elif y == "addattack":
                            self.app.display("It Adds", items[itemname].attributes[y], "To Your Melee Damage.")
                        elif y == "power":
                            self.app.display("It Allows You To Use The", items[itemname].attributes[y], "Power.")
                        elif y == "heal":
                            self.app.display("When Eaten, It Heals", items[itemname].attributes[y], "Health.")
                        elif y == "throw":
                            self.app.display("When Thrown, It Deals", items[itemname].attributes[y], "Damage.")
                        elif y == "loc":
                            self.app.display("It Goes Somewhere.")
                else:
                    self.app.display("You Don't Have A", itemname + ".")

            elif fmove.startswith("check "):
                itemname = ""
                for x in xrange(6,len(move)):
                    itemname += move[x]
                if itemname in players[username].powers:
                    self.app.display("You Check Your", itemname, "Power.")
                    self.app.display("It Deals", spells[itemname].damage, "Damage.")
                    self.app.display("It Requires", spells[itemname].mana, "Mana Power.")
                    for z in spells[itemname].powers:
                        if z == "hurt":
                            self.app.display("When Cast, It Hurts You For", spells[itemname].powers[z], "Damage.")
                        elif z == "burn":
                            self.app.display("It Inflicts", spells[itemname].powers[z], "Damage Over Time.")
                        elif z == "freeze":
                            self.app.display("It Freezes The Opponent For", spells[itemname].powers[z], "Turns.")
                        elif z == "heal":
                            self.app.display("When Cast, It Heals You For", spells[itemname].powers[z], "Health.")
                        elif z == "necrosis":
                            self.app.display("It Prevents The Opponent From Attacking When Under", spells[itemname].powers[z], "Health.")
                        elif z == "sacrifice":
                            self.app.display("It Heals You", spells[itemname].powers[z], "Health If Used To Kill An Opponent.")
                        elif z == "cooldown":
                            self.app.display("It Has A Cooldown Of", spells[itemname].powers[z], "Turns.")

            elif fmove == "armor":
                self.app.display("You Are Wearing:")
                self.app.display("Head:", players[username].head)
                self.app.display("Chest:", players[username].chest)
                self.app.display("Legs:", players[username].legs)
                self.app.display("Feet:", players[username].feet)

            elif fmove in options["invlist"]:
                newinvdict = {}
                newinvlist = []
                for x in players[username].inventory:
                    try:
                        newinvdict[x] += 1
                    except KeyError:
                        newinvdict[x] = 1
                for x in newinvdict:
                    if newinvdict[x] == 1:
                        newinvlist.append(x)
                    elif newinvdict[x] > 1:
                        newinvlist.append(x + " x" + str(newinvdict[x]))
                self.app.display("You Are Currently Carrying:", str(newinvlist) + ".")


            elif fmove in options["healthlist"]:
                self.app.display("You Are Currently At", str(players[username].health) + "/" + str(players[username].maxhealth), "Health.")

            elif fmove in options["statlist"]:
                self.app.display("Your Stats Are:")
                self.app.display("Maximum Health:", players[username].maxhealth)
                self.app.display("Melee Attack Power:", players[username].attack)
                self.app.display("Mana Power:", players[username].mana)

            elif fmove == "powers":
                self.app.display("You Know The Powers:", players[username].powers)

            elif fmove.startswith("eat "):
                itemname = ""
                for x in xrange(4,len(move)):
                    itemname += move[x]
                if itemname in players[username].inventory:
                    if "heal" in items[itemname].attributes:
                        players[username].take(itemname)
                        players[username].heal(int(items[itemname].attributes["heal"]))
                    else:
                        self.app.display("You Can't Eat", itemname + ".")
                else:
                    self.app.display("You Don't Have Any", itemname + ".")

            elif fmove.startswith("equip "):
                itemname = ""
                for x in xrange(6,len(move)):
                    itemname += move[x]
                if itemname in players[username].inventory:
                    if "slot" in items[itemname].attributes:
                        players[username].take(itemname)
                        if items[itemname].attributes["slot"] == "head":
                            if players[username].head != "":
                                players[username].give(players[username].head)
                                subatts(username, players[username].head)
                            players[username].head = itemname
                        elif items[itemname].attributes["slot"] == "chest":
                            if players[username].chest != "":
                                players[username].give(players[username].chest)
                                subatts(username, players[username].chest)
                        elif items[itemname].attributes["slot"] == "legs":
                            if players[username].legs != "":
                                players[username].give(players[username].legs)
                                subatts(username, players[username].legs)
                            players[username].legs = itemname
                        elif items[itemname].attributes["slot"] == "feet":
                            if players[username].feet != "":
                                players[username].give(players[username].feet)
                                subatts(username, players[username].feet)
                            players[username].feet = itemname
                        addatts(username, itemname)
                    else:
                        self.app.display("You Can't Equip A", itemname + ".")
                else:
                    self.app.display("You Don't Have A", itemname + ".")

            elif fmove.startswith("use "):
                itemname = ""
                for x in xrange(4,len(move)):
                    itemname += move[x]
                if itemname in players[username].inventory:
                    if "damage" in items[itemname].attributes:
                        self.app.display("You Use Your", itemname, "Item To Attack!")
                        mobhealth -= int(items[itemname].attributes["damage"])
                        if options["stack"]:
                            mobhealth -= int(players[username].attack)
                        turn = 0
                    else:
                        self.app.display("You Can't Use A", itemname + ".")
                else:
                    self.app.display("You Don't Have A", itemname + ".")

            elif fmove.startswith("throw "):
                itemname = ""
                for x in xrange(6,len(move)):
                    itemname += move[x]
                if itemname in players[username].inventory:
                    if "throw" in items[itemname].attributes:
                        self.app.display("You Throw Your", itemname, "Item To Attack!")
                        mobhealth -= int(items[itemname].attributes["throw"])
                        players[username].take(itemname)
                        turn = 0
                    else:
                        self.app.display("You Can't Throw A", itemname + ".")
                else:
                    self.app.display("You Don't Have A", itemname + ".")


            elif fmove.startswith("unequip "):
                itemname = ""
                for x in xrange(8,len(move)):
                    itemname += move[x]
                if players[username].chest == itemname:
                    players[username].chest == ""
                    players[username].give(itemname)
                    subatts(username, itemname)
                elif players[username].head == itemname:
                    players[username].head == ""
                    players[username].give(itemname)
                    subatts(username, itemname)
                elif players[username].feet == itemname:
                    players[username].feet == ""
                    players[username].give(itemname)
                    subatts(username, itemname)
                elif players[username].legs == itemname:
                    players[username].legs == ""
                    players[username].give(itemname)
                    subatts(username, itemname)
                else:
                    self.app.display("You Aren't Wearing A", itemname + ".")

            elif fmove.startswith("cast "):
                magicname = ""
                for x in xrange(5,len(move)):
                    magicname += move[x]
                if magicname in players[username].powers:
                    if players[username].mana >= spells[magicname].mana:
                        if spells[magicname].cooldown <= 0:
                            self.app.display("You Use Your", magicname, "Power To Attack!")
                            mobhealth -= int(spells[magicname].damage)
                            for x in spells[magicname].powers:
                                if x.startswith("cooldown"):
                                    spells[magicname].cooldown = int(x.split("=")[1]) + 1
                            for x in spells[magicname].powers:
                                if x.startswith("freeze"):
                                    z,y = x.split("=")
                                    frozen = int(y)
                                elif x.startswith("heal"):
                                    z,y = x.split("=")
                                    players[username].heal(int(y))
                                elif x.startswith("hurt"):
                                    z,y = x.split("=")
                                    players[username].hurt(int(y))
                                elif x.startswith("sacrifice"):
                                    z,y = x.split("=")
                                    sacrifice = int(y)
                                elif x.startswith("necrosis"):
                                    z,y = x.split("=")
                                    necrosis = int(y)
                                elif x.startswith("burn"):
                                    z,y = x.split("=")
                                    burn = int(y)
                            turn = 0
                        else:
                            self.app.display("You Have To Wait To Use", magicname, "Again.")
                    else:
                        self.app.display("You Don't Have Enough Mana Power To Use", magicname, "Magic.")
                else:
                    self.app.display("You Don't Know How To Use", magicname, "Magic.")

            elif fmove in options["waitlist"]:
                self.app.display("You Do Nothing.")
                turn = 0

            else:
                self.app.display("Huh?")
        return mobhealth,frozen,sacrifice,necrosis,burn

    def mobturn(self, objectname,username,mobhealth,mobdamage,frozen,necrosis,burn):
        if burn > 0:
            self.app.display("The", objectname, "Takes Extra Damage From Its Burn!")
            mobhealth -= burn
        elif burn < 0:
            self.app.display("The", objectname, "Is Healed!")
            mobhealth -= burn
        if frozen > 0:
            self.app.display("The", objectname, "Is Frozen!")
            frozen -= 1
        elif necrosis != 0:
            if mobhealth >= necrosis:
                self.app.display("The", objectname, "Attacks!")
                players[username].hurt(mobdamage)
            else:
                self.app.display("The", objectname + "'s Necrosis Prevents It From Attacking!")
        else:
            self.app.display("The", objectname, "Attacks!")
            players[username].hurt(mobdamage)
        return mobhealth,frozen

    def run(self):
        do = 0
        save = 0
        self.app.display("Loading World...")
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
                            self.app.display("Data Error In World File At Line:", x)
                        except ValueError:
                            self.app.display("Data Error In World File At Line:", x)
        except IOError:
            self.app.display("Fatal Error: Unable To Load World File.")

        else:
            self.app.display("Loading Options...")
            try:
                configfile = open("Options.txt", "rb")
            except IOError:
                self.app.display("Unable To Load Options.")
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
                                    self.app.display("Data Error: No Known Option:", go)
                            except ValueError:
                                self.app.display("Data Error In Options File At Line:", x)
                            except IndexError:
                                self.app.display("Data Error In Options File At Line:", x)
            finally:
                try:
                    configfile.close()
                except NameError:
                    self.app.display("Warning: No Options Data.")

            self.app.display("Loading Objects...")
            try:
                objectfile = open("Objects.txt", "rb")
            except IOError:
                self.app.display("Unable To Load Objects.")
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
                                self.app.display("Data Error In Objects File At Line:", x)
                            for y in xrange(2, len(objectlist)):
                                ylist = objectlist[y].split("=")
                                try:
                                    items[objectlist[0]].setatt(ylist[0],ylist[1])
                                except IndexError:
                                    self.app.display("Data Error In Objects File At Line:", x)
            finally:
                try:
                    objectfile.close()
                except NameError:
                    self.app.display("Warning: No Object Data.")

            self.app.display("Loading Players...")
            try:
                savefile = openfile("PlayerSave.dat")
            except IOError:
                self.app.display("Unable To Load Player Saves.")
            else:
                savedata = readfile(savefile)
                savelines = savedata.splitlines()
                for x in savelines:
                    if x != "":
                        if not x.startswith("#"):
                            toplist = x.split(";")
                            savelist = toplist[0].split(",")
                            flaglist = []
                            for y in xrange(8, len(savelist)):
                                flaglist.append(savelist[y])
                            itemlist = []
                            for z in toplist[1].split(","):
                                itemlist.append(z)
                            powerlist = []
                            for w in toplist[2].split(","):
                                powerlist.append(w)
                            armorlist = toplist[3].split(",")
                            create(savelist[0], savelist[1], savelist[2], savelist[4], savelist[5], (int(savelist[6]),int(savelist[7])), flaglist, savelist[3], itemlist, powerlist)
                            players[savelist[0]].head = armorlist[0]
                            players[savelist[0]].chest = armorlist[1]
                            players[savelist[0]].legs = armorlist[2]
                            players[savelist[0]].feet = armorlist[3]

            self.app.display("Loading World Data...")
            try:
                worldsavefile = openfile("WorldSave.dat")
            except IOError:
                self.app.display("Unable To Load Saved World Data.")
            else:
                worldsavedata = readfile(worldsavefile)
                worldsavelines = worldsavedata.splitlines()
                for x in worldsavelines:
                    if x != "":
                        if not x.startswith("#"):
                            worldsavelist = x.split(",")
                            if len(worldsavelist) > 2:
                                worldinvlist = []
                                for y in xrange(2, len(worldsavelist)):
                                    worldinvlist.append(worldsavelist[y])
                                world[int(worldsavelist[0]),int(worldsavelist[1])].inventory = worldinvlist
                            else:
                                world[int(worldsavelist[0]),int(worldsavelist[1])].inventory = []

            self.app.display("Loading Powers...")
            try:
                spellfile = open("Powers.txt", "rb")
            except IOError:
                self.app.display("Unable To Load Powers.")
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
                                self.app.display("Data Error In Powers File At Line:", x)
                            except ValueError:
                                self.app.display("Data Error In Powers File At Line:", x)
            finally:
                try:
                    spellfile.close()
                except NameError:
                    self.app.display("Warning: No Powers Data.")

            self.app.display("Verifying...")

            if self.domap >= 1:
                self.assemble()

            for x in players:
                for y in players[x].inventory:
                    if y == "":
                        players[x].take(y)
                for z in players[x].powers:
                    if z == "":
                        players[x].delspell(z)
                for w in players[x].flags:
                    if w == "":
                        players[x].delflag(w)

            acceptables = ["none", "item"]
            moblisters = ["pass", "agg"]
            for x in items:
                if items[x].itemtype in moblisters:
                    try:
                        items[x].attributes["health"]
                        items[x].attributes["damage"]
                    except KeyError:
                        self.app.display("Data Error:", x, "Is Missing Attributes.")
                elif items[x].itemtype not in acceptables:
                    self.app.display("Data Error:", x, "Has Invalid Type.")

            for x in world:
                for y in world[x].inventory:
                    if y == "":
                        world[x].take(y)
                    else:
                        try:
                            items[y]
                        except KeyError:
                            self.app.display("Data Error:", y, "Not Defined In Objects File.")
                            world[x].take(y)

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

            try:
                world[options["location"]]
            except KeyError:
                self.app.display("Error: Spawn Location Unavailable.")
            else:
                self.app.display("Game Loaded.")
                do = 1

        finally:
            try:
                worldfile.close()
            except NameError:
                self.app.display("Fatal Error: No World Data.")

        if do == 1:
            self.app.display("Login? [Y/n]")
            answer = superformat(self.get())

            if answer == "debug":
                self.app.display("WARNING: THE DEBUG FUNCTION CAN DO SERIOUS HARM. PROCEED? [y/N]")
                docreate = 0
                if formatisyes(self.get()):
                    self.app.display("To Exit Debug Mode Enter: debug = False")
                    debug = True
                    while debug:
                        try:
                            self.app.display("Enter A Command:")
                            command = self.get()
                            if command != "":
                                runcode(command, locals())
                        except:
                            self.app.display("An Error Occured.")
                self.app.display("Returning To Login...")

            elif isno(answer) == False:
                docreate = 0
            else:
                docreate = 1

            while docreate == 0:
                self.app.display("Username:")
                username = self.get()
                if username in players:
                    self.app.display("Password:")
                    password = self.get()
                    if players[username].password == md5.new(password).hexdigest():
                        self.app.display("Login Successful.")
                        break
                    else:
                        self.app.display("Login Failed. Try Again? [Y/n]")
                        if formatisno(self.get()):
                            docreate = 1
                else:
                    self.app.display("That Player Does Not Exist. Try Again? [y/N]")
                    if formatisyes(self.get()) == False:
                        docreate = 1

            if docreate == 1:
                self.app.display("Welcome To Character Creation.")
                creation = 1
                while creation == 1:
                    self.app.display("Username:")
                    username = self.get()
                    if username in players:
                        self.app.display("That Username Is Already Taken. Try Again.")
                    elif username == "":
                        self.app.display("Your Username May Not Be Blank. Try Again.")
                    elif "," in username:
                        self.app.display("Your Username May Not Contain Commas. Try Again.")
                    elif ";" in username:
                        self.app.display("Your Username May Not Contain Semicolons. Try Again.")
                    elif "#" in username:
                        self.app.display("Your Username May Not Contain Pounds. Try Again.")
                    else:
                        creation = 0

                dopass = 1
                while dopass == 1:
                    self.app.display("Password:")
                    password = self.get()
                    if password == "":
                        self.app.display("Your Password May Not Be Blank. Try Again.")
                    else:
                        dopass = 0

                self.app.display("Loading Classes...")
                classes = {}
                try:
                    classfile = open("Classes.txt", "rb")
                    classdata = readfile(classfile)
                    classlines = classdata.splitlines()
                    for x in classlines:
                        if x != "":
                            if not x.startswith("#"):
                                classlist = x.split(",")
                                flaglist = []
                                for y in xrange(4, len(classlist)):
                                    flaglist.append(classlist[y])
                                try:
                                    classes[classlist[0]] = classtype(classlist[1], classlist[2], classlist[3])
                                except IndexError:
                                    self.app.display("Data Error In Classes File At Line:", x)
                                else:
                                    classes[classlist[0]].flags = flaglist
                    self.app.display("Classes Loaded.")

                    classeslist = []
                    for x in classes:
                        classeslist.append(x)
                    choosing = 1
                    while choosing == 1:
                        self.app.display("Choose A Class:", classeslist)
                        classchoice = self.get()
                        if classchoice in classeslist:
                            create(username, md5.new(password).hexdigest(), classes[classchoice].maxhealth, classes[classchoice].attack, classes[classchoice].mana, flags=classes[classchoice].flags)
                            self.app.display("You Are Now A", classchoice + ".")
                            choosing = 0
                        else:
                            self.app.display("Huh?")
                except IOError:
                    self.app.display("Unable To Load Classes. Player Will Have Default Class.")
                    create(username, md5.new(password).hexdigest(), options["maxhealth"], options["attack"], options["mana"], flags=["default"])
                finally:
                    try:
                        classfile.close()
                    except NameError:
                        self.app.display("Warning: No Class Data.")

            try:
                world[players[username].location]
            except KeyError:
                players[username].location = options["location"]
            self.app.display("Welcome", username + ".")
            start = 0
            playing = 1
            while playing == 1:
                dead = 0
                if start == 0:
                    travel = directions(players[username])
                    self.app.display("You Arrive At The", world[players[username].location].name + ". You May Travel:", str(travel) + ".")
                    if self.domap >= 1:
                        self.render(username)
                    worldnewinvdict = {}
                    for x in world[players[username].location].inventory:
                        x = str(x)
                        try:
                            worldnewinvdict[x] += 1
                        except KeyError:
                            worldnewinvdict[x] = 1
                    for x in worldnewinvdict:
                        if worldnewinvdict[x] == 1:
                            self.app.display("You See A", str(x) + ".")
                        elif worldnewinvdict[x] > 1:
                            self.app.display("You See A", str(x), "x" + str(worldnewinvdict[x]) + ".")
                    start = 1

                for x in world[players[username].location].inventory:
                    if items[x].itemtype == "agg":
                        objectname = str(x)
                        self.app.display("The", objectname, "Makes For You.")
                        if "text" in items[objectname].attributes:
                            self.app.display("He/She Says", items[objectname].attributes["text"] + ".")
                        mobhealth = int(items[objectname].attributes["health"])
                        mobdamage = int(items[objectname].attributes["damage"])
                        frozen = 0
                        necrosis = 0
                        burn = 0
                        battle = 1
                        while battle == 1:
                            sacrifice = 0

                            mobhealth,frozen = self.mobturn(objectname,username,mobhealth,mobdamage,frozen,necrosis,burn)

                            if players[username].health <= 0:
                                self.app.display("You Have Been Killed!")
                                players[username].location = options["location"]
                                players[username].health = health
                                start = 0
                                battle = 0
                                dead = 1
                            else:

                                mobhealth,frozen,sacrifice,necrosis,burn = self.playerturn(username,mobhealth,frozen,sacrifice,necrosis,burn)

                            if mobhealth <= 0:
                                self.app.display("You Kill The", objectname + ".")
                                world[players[username].location].take(objectname)
                                if sacrifice > 0:
                                    players[username].heal(sacrifice)
                                elif sacrifice < 0:
                                    players[username].hurt(sacrifice)
                                if "drop" in items[objectname].attributes:
                                    for x in items[objectname].attributes["drop"].split(";"):
                                        world[players[username].location].give(x)
                                battle = 0

                if dead == 0:
                    command = self.get()
                    fcommand = superformat(command)

                    if fcommand in options["helplist"]:
                        self.app.display("Command List:", options["commandlist"])

                    elif fcommand in options["northlist"]:
                        if "north" in travel:
                            players[username].move("north")
                            start = 0
                        else:
                            self.app.display("You Can't Go That Way!")

                    elif fcommand in options["southlist"]:
                        if "south" in travel:
                            players[username].move("south")
                            start = 0
                        else:
                            self.app.display("You Can't Go That Way!")

                    elif fcommand in options["eastlist"]:
                        if "east" in travel:
                            players[username].move("east")
                            start = 0
                        else:
                            self.app.display("You Can't Go That Way!")

                    elif fcommand in options["westlist"]:
                        if "west" in travel:
                            players[username].move("west")
                            start = 0
                        else:
                            self.app.display("You Can't Go That Way!")

                    elif fcommand in options["spawnlist"]:
                        self.app.display("You Travel Back To Spawn.")
                        players[username].location = options["location"]
                        start = 0

                    elif fcommand.startswith("drop "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in players[username].inventory:
                            players[username].take(itemname)
                            world[players[username].location].give(itemname)
                            if "slot" not in items[itemname].attributes:
                                subatts(username, itemname)
                        else:
                            self.app.display("You Don't Have A", itemname + ".")

                    elif fcommand.startswith("abandon "):
                        itemname = ""
                        for x in xrange(8,len(command)):
                            itemname += command[x]
                        if itemname in players[username].inventory:
                            doabandon = 0
                            for x in players[username].inventory:
                                if x == itemname:
                                    doabandon += 1
                            for x in xrange(0, doabandon):
                                players[username].take(itemname)
                                world[players[username].location].give(itemname)
                                if "slot" not in items[itemname].attributes:
                                    subatts(username, itemname)
                        else:
                            self.app.display("You Don't Have Any", itemname + ".")

                    elif fcommand.startswith("attack "):
                        objectname = ""
                        for x in xrange(7,len(command)):
                            objectname += command[x]
                        if objectname in world[players[username].location].inventory:
                            if items[objectname].itemtype in talklist:
                                canfight = 1
                                if "health" not in items[objectname].attributes:
                                    canfight = 0
                                if "damage" not in items[objectname].attributes:
                                    canfight = 0
                                if canfight == 1:
                                    mobhealth = int(items[objectname].attributes["health"])
                                    mobdamage = int(items[objectname].attributes["damage"])
                                    frozen = 0
                                    necrosis = 0
                                    burn = 0
                                    battle = 1
                                    while battle == 1:
                                        sacrifice = 0

                                        mobhealth,frozen,sacrifice,necrosis,burn = self.playerturn(username,mobhealth,frozen,sacrifice,necrosis,burn)

                                        if mobhealth <= 0:
                                            self.app.display("You Kill The", objectname + ".")
                                            world[players[username].location].take(objectname)
                                            if sacrifice > 0:
                                                players[username].heal(sacrifice)
                                            elif sacrifice < 0:
                                                players[username].hurt(sacrifice)
                                            if "drop" in items[objectname].attributes:
                                                for x in items[objectname].attributes["drop"].split(";"):
                                                    world[players[username].location].give(x)
                                            battle = 0
                                        else:

                                            mobhealth,frozen = self.mobturn(objectname,username,mobhealth,mobdamage,frozen,necrosis,burn)

                                        if players[username].health <= 0:
                                            self.app.display("You Have Been Killed!")
                                            players[username].location = options["location"]
                                            players[username].health = health
                                            start = 0
                                            battle = 0

                                else:
                                    self.app.display("You Can't Attack A", objectname + ".")
                            else:
                                self.app.display("You Can't Attack A", objectname + ".")
                        else:
                            self.app.display("You Don't See A", objectname, "Here.")

                    elif fcommand.startswith("take "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            cantake = 1
                            if items[itemname].itemtype != "item":
                                self.app.display("You Can't Take A", itemname + ".")
                                cantake = 0
                            if "req" in items[itemname].attributes:
                                if items[itemname].attributes["req"] not in players[username].inventory:
                                    self.app.display("You Lack The Required Item", items[itemname].attributes["req"], "To Take A", itemname + ".")
                                    cantake = 0
                            if "reqflag" in items[itemname].attributes:
                                if items[itemname].attributes["reqflag"] not in players[username].flags:
                                    self.app.display("You Lack The Required Ability", items[itemname].attributes["reqflag"], "To Take A", itemname + ".")
                                    cantake = 0
                            if "not" in items[itemname].attributes:
                                if items[itemname].attributes["not"] in players[username].inventory:
                                    self.app.display("You Can't Have A", items[itemname].attributes["not"], "Item And A", itemname, "Item At The Same Time.")
                                    cantake = 0
                            if "notflag" in items[itemname].attributes:
                                if items[itemname].attributes["notflag"] in players[username].flags:
                                    self.app.display("Your Ability", items[itemname].attributes["notflag"], "Prevents You From Taking A", itemname + ".")
                                    cantake = 0
                            if cantake == 1:
                                world[players[username].location].take(itemname)
                                players[username].give(itemname)
                                if "slot" not in items[itemname].attributes:
                                    addatts(username, itemname)
                        else:
                            self.app.display("You Don't See A", itemname, "Here.")

                    elif fcommand.startswith("loot "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            cantake = 1
                            if items[itemname].itemtype != "item":
                                self.app.display("You Can't Take A", itemname + ".")
                                cantake = 0
                            if "req" in items[itemname].attributes:
                                if items[itemname].attributes["req"] not in players[username].inventory:
                                    self.app.display("You Lack The Required Item", items[itemname].attributes["req"], "To Take A", itemname + ".")
                                    cantake = 0
                            if "reqflag" in items[itemname].attributes:
                                if items[itemname].attributes["reqflag"] not in players[username].flags:
                                    self.app.display("You Lack The Required Ability", items[itemname].attributes["reqflag"], "To Take A", itemname + ".")
                                    cantake = 0
                            if "not" in items[itemname].attributes:
                                if items[itemname].attributes["not"] in players[username].inventory:
                                    self.app.display("You Can't Have A", items[itemname].attributes["not"], "Item And A", itemname, "Item At The Same Time.")
                                    cantake = 0
                            if "notflag" in items[itemname].attributes:
                                if items[itemname].attributes["notflag"] in players[username].flags:
                                    self.app.display("Your Ability", items[itemname].attributes["notflag"], "Prevents You From Taking A", itemname + ".")
                                    cantake = 0
                            if cantake == 1:
                                doloot = 0
                                for x in world[players[username].location].inventory:
                                    if itemname == x:
                                        doloot += 1
                                for x in xrange(0, doloot):
                                    players[username].give(itemname)
                                    if "slot" not in items[itemname].attributes:
                                        addatts(username, itemname)
                                    world[players[username].location].take(itemname)
                        else:
                            self.app.display("You Don't See Any", itemname, "Here.")

                    elif fcommand.startswith("unequip "):
                        itemname = ""
                        for x in xrange(8,len(command)):
                            itemname += command[x]
                        if players[username].chest == itemname:
                            players[username].chest == ""
                            players[username].give(itemname)
                            subatts(username, itemname)
                        elif players[username].head == itemname:
                            players[username].head == ""
                            players[username].give(itemname)
                            subatts(username, itemname)
                        elif players[username].feet == itemname:
                            players[username].feet == ""
                            players[username].give(itemname)
                            subatts(username, itemname)
                        elif players[username].legs == itemname:
                            players[username].legs == ""
                            players[username].give(itemname)
                            subatts(username, itemname)
                        else:
                            self.app.display("You Aren't Wearing A", itemname + ".")

                    elif fcommand.startswith("equip "):
                        itemname = ""
                        for x in xrange(6,len(command)):
                            itemname += command[x]
                        if itemname in players[username].inventory:
                            if "slot" in items[itemname].attributes:
                                players[username].take(itemname)
                                if items[itemname].attributes["slot"] == "head":
                                    if players[username].head != "":
                                        players[username].give(players[username].head)
                                        subatts(username, players[username].head)
                                    players[username].head = itemname
                                elif items[itemname].attributes["slot"] == "chest":
                                    if players[username].chest != "":
                                        players[username].give(players[username].chest)
                                        subatts(username, players[username].chest)
                                elif items[itemname].attributes["slot"] == "legs":
                                    if players[username].legs != "":
                                        players[username].give(players[username].legs)
                                        subatts(username, players[username].legs)
                                    players[username].legs = itemname
                                elif items[itemname].attributes["slot"] == "feet":
                                    if players[username].feet != "":
                                        players[username].give(players[username].feet)
                                        subatts(username, players[username].feet)
                                    players[username].feet = itemname
                                addatts(username, itemname)
                            else:
                                self.app.display("You Can't Equip A", itemname + ".")
                        else:
                            self.app.display("You Don't Have A", itemname + ".")

                    elif fcommand in options["armorlist"]:
                        self.app.display("You Are Wearing:")
                        self.app.display("Head:", players[username].head)
                        self.app.display("Chest:", players[username].chest)
                        self.app.display("Legs:", players[username].legs)
                        self.app.display("Feet:", players[username].feet)

                    elif fcommand in options["invlist"]:
                        newinvdict = {}
                        newinvlist = []
                        for x in players[username].inventory:
                            try:
                                newinvdict[x] += 1
                            except KeyError:
                                newinvdict[x] = 1
                        for x in newinvdict:
                            if newinvdict[x] == 1:
                                newinvlist.append(x)
                            elif newinvdict[x] > 1:
                                newinvlist.append(x + " x" + str(newinvdict[x]))
                        self.app.display("You Are Currently Carrying:", str(newinvlist) + ".")

                    elif fcommand in options["healthlist"]:
                        self.app.display("You Are Currently At", str(players[username].health) + "/" + str(players[username].maxhealth), "Health.")

                    elif fcommand in options["statlist"]:
                        self.app.display("Your Stats Are:")
                        self.app.display("Maximum Health:", players[username].maxhealth)
                        self.app.display("Melee Attack Power:", players[username].attack)
                        self.app.display("Mana Power:", players[username].mana)

                    elif fcommand.startswith("read "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            if items[itemname].itemtype in readlist:
                                if "text" in items[itemname].attributes:
                                    self.app.display("It Says:", items[itemname].attributes["text"] + ".")
                                else:
                                    self.app.display("You Can't Read A", itemname + ".")
                            else:
                                self.app.display("You Can't Read A", itemname + ".")
                        else:
                            self.app.display("You Don't See A", itemname, "Here.")

                    elif fcommand.startswith("open "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            canopen = 1
                            if items[itemname].itemtype not in readlist:
                                self.app.display("You Can't Open A", itemname + ".")
                                canopen = 0
                            if "loc" not in items[itemname].attributes:
                                self.app.display("You Can't Open A", itemname + ".")
                                canopen = 0
                            if "req" in items[itemname].attributes:
                                if items[itemname].attributes["req"] not in players[username].inventory:
                                    self.app.display("You Lack The Required Item", items[itemname].attributes["req"], "To Open A", itemname + ".")
                                    canopen = 0
                            if "reqflag" in items[itemname].attributes:
                                if items[itemname].attributes["reqflag"] not in players[username].flags:
                                    self.app.display("You Lack The Required Ability", items[itemname].attributes["reqflag"], "To Open A", itemname + ".")
                                    canopen = 0
                            if "not" in items[itemname].attributes:
                                if items[itemname].attributes["not"] in players[username].inventory:
                                    self.app.display("You Can't Have A", items[itemname].attributes["not"], "Item And Open A", itemname + ".")
                                    canopen = 0
                            if "notflag" in items[itemname].attributes:
                                if items[itemname].attributes["notflag"] in players[username].flags:
                                    self.app.display("Your Ability", items[itemname].attributes["notflag"], "Prevents You From Opening A", itemname + ".")
                                    canopen = 0
                            if canopen == 1:
                                placex,placey = items[itemname].attributes["loc"].split(";")
                                placex = int(placex)
                                placey = int(placey)
                                try:
                                    world[placex, placey]
                                except KeyError:
                                    self.app.display("That", itemname, "Doesn't Go Anywhere.")
                                else:
                                    players[username].location = placex,placey
                                    start = 0
                        else:
                            self.app.display("You Don't See A", itemname, "Here.")

                    elif fcommand.startswith("talk "):
                        itemname = ""
                        for x in xrange(5,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            if items[itemname].itemtype in talklist:
                                if "text" in items[itemname].attributes:
                                    self.app.display("He/She Says", items[itemname].attributes["text"] + ".")
                                else:
                                    self.app.display("You Can't Talk To A", itemname + ".")
                            else:
                                self.app.display("You Can't Talk To A", itemname + ".")
                        else:
                            self.app.display("You Don't See A", itemname, "Here.")

                    elif fcommand in options["powerlist"]:
                        self.app.display("You Know The Powers:", players[username].powers)

                    elif fcommand.startswith("give to "):
                        itemname = ""
                        for x in xrange(8,len(command)):
                            itemname += command[x]
                        if itemname in world[players[username].location].inventory:
                            if items[itemname].itemtype in talklist:
                                if "req" in items[itemname].attributes:
                                    dogive = 1
                                    for x in items[itemname].attributes["req"].split(";"):
                                        if x not in players[username].inventory:
                                            x = str(x)
                                            self.app.display("You Lack The Required", x, "To Give.")
                                            dogive = 0
                                    if dogive == 1:
                                            for x in items[itemname].attributes["req"].split(";"):
                                                x = str(x)
                                                self.app.display("You Give Your", x + ".")
                                                players[username].take(x)
                                                if "slot" not in items[x].attributes:
                                                    subatts(username, x)
                                            for x in items[itemname].attributes["drop"].split(";"):
                                                x = str(x)
                                                self.app.display("You Get A", x + ".")
                                                players[username].give(x)
                                                if "slot" not in items[x].attributes:
                                                    addatts(username, x)
                                else:
                                    self.app.display("You Can't Give To A", itemname + ".")
                            else:
                                self.app.display("You Can't Give To A", itemname + ".")
                        else:
                            self.app.display("You Don't See A", itemname + ".")

                    elif fcommand.startswith("eat "):
                        itemname = ""
                        for x in xrange(4,len(command)):
                            itemname += command[x]
                        if itemname in players[username].inventory:
                            if "heal" in items[itemname].attributes:
                                players[username].take(itemname)
                                players[username].heal(int(items[itemname].attributes["heal"]))
                            else:
                                self.app.display("You Can't Eat", itemname + ".")
                        else:
                            if itemname in world[players[username].location].inventory:
                                caneat = 1
                                if items[itemname].itemtype not in readlist:
                                    self.app.display("You Can't Eat", itemname + ".")
                                    caneat = 0
                                if not "heal" in items[itemname].attributes:
                                    self.app.display("You Can't Eat", itemname + ".")
                                    caneat = 0
                                if "req" in items[itemname].attributes:
                                    if items[itemname].attributes["req"] not in players[username].inventory:
                                        self.app.display("You Lack The Required Item", items[itemname].attributes["req"], "To Eat", itemname + ".")
                                        caneat = 0
                                if "reqflag" in items[itemname].attributes:
                                    if items[itemname].attributes["reqflag"] not in players[username].flags:
                                        self.app.display("You Lack The Required Ability", items[itemname].attributes["reqflag"], "To Eat", itemname + ".")
                                        caneat = 0
                                if "not" in items[itemname].attributes:
                                    if items[itemname].attributes["not"] in players[username].inventory:
                                        self.app.display("You Can't Have A", items[itemname].attributes["not"], "Item And Eat", itemname + ".")
                                        caneat = 0
                                if "notflag" in items[itemname].attributes:
                                    if items[itemname].attributes["notflag"] in players[username].flags:
                                        self.app.display("Your Ability", items[itemname].attributes["notflag"], "Prevents You From Eating", itemname + ".")
                                        caneat = 0
                                if caneat == 1:
                                    if items[itemname].itemtype == "item":
                                        world[players[username].location].take(itemname)
                                    players[username].heal(int(items[itemname].attributes["heal"]))
                            else:
                                self.app.display("You Don't Have Any", itemname + ".")

                    elif fcommand in options["looklist"]:
                        self.app.display("You Look Around.")
                        worldnewinvdict = {}
                        for x in world[players[username].location].inventory:
                            x = str(x)
                            try:
                                worldnewinvdict[x] += 1
                            except KeyError:
                                worldnewinvdict[x] = 1
                        for x in worldnewinvdict:
                            if worldnewinvdict[x] == 1:
                                self.app.display("You See A", str(x) + ".")
                            elif worldnewinvdict[x] > 1:
                                self.app.display("You See A", str(x), "x" + str(worldnewinvdict[x]) + ".")

                    elif fcommand.startswith("inspect "):
                        itemname = ""
                        for x in xrange(8,len(command)):
                            itemname += command[x]
                        if itemname in players[username].inventory:
                            self.app.display("You Inspect The", itemname + ".")
                            for y in items[itemname].attributes:
                                if y == "damage":
                                    self.app.display("It Deals", items[itemname].attributes[y], "Damage.")
                                elif y == "slot":
                                    self.app.display("It Is Equiped In The", items[itemname].attributes[y], "Slot.")
                                elif y == "addhealth":
                                    self.app.display("It Adds", items[itemname].attributes[y], "To Your Maximum Health.")
                                elif y == "addmana":
                                    self.app.display("It Adds", items[itemname].attributes[y], "To Your Maximum Mana.")
                                elif y == "addattack":
                                    self.app.display("It Adds", items[itemname].attributes[y], "To Your Melee Damage.")
                                elif y == "power":
                                    self.app.display("It Allows You To Use The", items[itemname].attributes[y], "Power.")
                                elif y == "heal":
                                    self.app.display("When Eaten, It Heals", items[itemname].attributes[y], "Health.")
                                elif y == "throw":
                                    self.app.display("When Thrown, It Deals", items[itemname].attributes[y], "Damage.")
                                elif y == "loc":
                                    self.app.display("It Goes Somewhere.")
                        else:
                            self.app.display("You Don't Have A", itemname + ".")

                    elif fcommand.startswith("check "):
                        itemname = ""
                        for x in xrange(6,len(command)):
                            itemname += command[x]
                        if itemname in players[username].powers:
                            self.app.display("You Check Your", itemname, "Power.")
                            self.app.display("It Deals", spells[itemname].damage, "Damage.")
                            self.app.display("It Requires", spells[itemname].mana, "Mana Power.")
                            for z in spells[itemname].powers:
                                if z == "hurt":
                                    self.app.display("When Cast, It Hurts You For", spells[itemname].powers[z], "Damage.")
                                elif z == "burn":
                                    self.app.display("It Inflicts", spells[itemname].powers[z], "Damage Over Time.")
                                elif z == "freeze":
                                    self.app.display("It Freezes The Opponent For", spells[itemname].powers[z], "Turns.")
                                elif z == "heal":
                                    self.app.display("When Cast, It Heals You For", spells[itemname].powers[z], "Health.")
                                elif z == "necrosis":
                                    self.app.display("It Prevents The Opponent From Attacking When Under", spells[itemname].powers[z], "Health.")
                                elif z == "sacrifice":
                                    self.app.display("It Heals You", spells[itemname].powers[z], "Health If Used To Kill An Opponent.")
                                elif z == "cooldown":
                                    self.app.display("It Has A Cooldown Of", spells[itemname].powers[z], "Turns.")

                    elif fcommand in options["exitlist"]:
                        self.app.display("Quit Game? [y/N]")
                        if formatisyes(self.get()):
                            playing = 0

                    elif fcommand in options["deletelist"]:
                        self.app.display("Are You Sure You Want To Delete", username + "? [y/N]")
                        if formatisyes(self.get()):
                            del players[username]
                            playing = 0

                    else:
                        self.app.display("Huh?")

            save = 1

        if save == 1:
            self.app.display("Save Game? [Y/n]")
            if formatisno(self.get()) == False:
                try:
                    self.app.display("Saving Player Data...")
                    savefile = open("PlayerSave.dat", "wb")
                    writer = ""
                    for x in players:
                        writer += x
                        writer += ","
                        writer += players[x].password
                        writer += ","
                        writer += str(players[x].maxhealth)
                        writer += ","
                        writer += str(players[x].health)
                        writer += ","
                        writer += str(players[x].attack)
                        writer += ","
                        writer += str(players[x].mana)
                        writer += ","
                        writer += str(players[x].location[0])
                        writer += ","
                        writer += str(players[x].location[1])
                        if len(players[x].flags) > 0:
                            for y in players[x].flags:
                                writer += ","
                                writer += str(y)
                        writer += ";"
                        if len(players[x].inventory) > 0:
                            for z in players[x].inventory:
                                writer += str(z)
                                writer += ","
                        writer += ";"
                        if len(players[x].powers) > 0:
                            for w in players[x].powers:
                                writer += str(w)
                                writer += ","
                        writer += ";" + str(players[x].head) + "," + str(players[x].chest) + "," + str(players[x].legs) + "," + str(players[x].feet) + "\n"
                    savefile.write(writer)

                    self.app.display("Saving World Data...")
                    worldsavefile = open("WorldSave.dat", "wb")
                    writer = ""
                    for x in world:
                        a,b = x
                        writer += str(a)
                        writer += ","
                        writer += str(b)
                        if len(world[x].inventory) > 0:
                            for y in world[x].inventory:
                                writer += ","
                                writer += str(y)
                        writer += "\n"
                    worldsavefile.write(writer)

                finally:
                    try:
                        savefile.close()
                        worldsavefile.close()
                    except NameError:
                        self.app.display("Error: Unable To Save Game.")
                    else:
                        self.app.display("Game Saved.")

        self.app.display("Press Enter To End.")
        self.get()
        self.root.destroy()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main().start()
