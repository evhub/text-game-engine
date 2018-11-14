#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# DATA made in 2012
# This program provides functions for the TextGameProcessor.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *
from TextGameGlobals import *

class player(object):
    def __init__(self, password, maxhealth, attack, mana):
        self.password = password
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.attack = attack
        self.mana = mana
        self.location = options["location"]
        self.flags = []
        self.inventory = []
        self.head = ""
        self.chest = ""
        self.legs = ""
        self.feet = ""
        self.powers = []
    def addflag(self, flag):
        self.flags.append(flag)
    def delflag(self, flag):
        self.flags.remove(flag)
    def hurt(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxhealth:
            self.health = self.maxhealth
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
    def give(self, item):
        self.inventory.append(item)
    def take(self, item):
        self.inventory.remove(item)
    def addspell(self, spell):
        self.powers.append(spell)
    def delspell(self, spell):
        self.powers.remove(spell)

def directions(self):
    direction = []
    locx, locy = self.location
    north = locx, locy + 1
    south = locx, locy - 1
    east = locx + 1, locy
    west = locx - 1, locy
    try:
        world[north]
    except KeyError:
        pass
    else:
        direction.append("north")
    try:
        world[south]
    except KeyError:
        pass
    else:
        direction.append("south")
    try:
        world[east]
    except KeyError:
        pass
    else:
        direction.append("east")
    try:
        world[west]
    except KeyError:
        pass
    else:
        direction.append("west")
    return direction

def create(name, password, maxhealth, attack, mana, location=None, flags=None, health=None, inventory=None, powers=None):
    players[name] = player(password, int(maxhealth), int(attack), int(mana))
    if health != None:
        players[name].health = int(health)
    if flags != None:
        players[name].flags = flags
    if location != None:
        players[name].location = location
    if inventory != None:
        players[name].inventory = inventory
    if powers != None:
        players[name].powers = powers

class room(object):
    def __init__(self, name):
        self.name = name
        self.inventory = []
    def give(self, item):
        self.inventory.append(item)
    def take(self, item):
        self.inventory.remove(item)

def make(x, y, name, inventory=None):
    world[x,y] = room(name)
    if inventory != None:
        world[x,y].inventory = inventory

class classtype(object):
    def __init__(self, maxhealth, attack, mana):
        self.maxhealth = maxhealth
        self.attack = attack
        self.mana = mana
        self.flags = []

class item(object):
    def __init__(self, itemtype):
        self.itemtype = itemtype
        self.attributes = {}
    def setatt(self, attribute, value):
        self.attributes[attribute] = value
    def delatt(self, attribute):
        del self.attributes[attribute]

def put(name, itemtype):
    items[name] = item(itemtype)

class spell(object):
    def __init__(self, damage, mana):
        self.damage = damage
        self.mana = mana
        self.powers = []
        self.cooldown = 0
    def addpower(self, power):
        self.powers.append(power)
    def delpower(self, power):
        self.powers.remove(power)

def exist(name, damage, mana, powers=None):
    spells[name] = spell(damage, mana)
    if powers != None:
        spells[name].powers = powers

def addatts(username, itemname):
    if "addhealth" in items[itemname].attributes:
        players[username].maxhealth += int(items[itemname].attributes["addhealth"])
    if "addmana" in items[itemname].attributes:
        players[username].mana += int(items[itemname].attributes["addmana"])
    if "addattack" in items[itemname].attributes:
        players[username].attack += int(items[itemname].attributes["addattack"])
    if "power" in items[itemname].attributes:
        for x in items[itemname].attributes["power"].split(";"):
            players[username].addspell(x)

def subatts(username, itemname):
    if "addhealth" in items[itemname].attributes:
        players[username].maxhealth -= int(items[itemname].attributes["addhealth"])
    if "addmana" in items[itemname].attributes:
        players[username].mana -= int(items[itemname].attributes["addmana"])
    if "addattack" in items[itemname].attributes:
        players[username].attack -= int(items[itemname].attributes["addattack"])
    if "power" in items[itemname].attributes:
        for x in items[itemname].attributes["power"].split(";"):
            players[username].delspell(x)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print "This Is Not A Runnable File. Run TextGameProcessor Instead."
    raw_input("Press Enter To End.")
