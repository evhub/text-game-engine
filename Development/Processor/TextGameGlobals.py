#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# DATA made in 2012
# This program provides globals for the TextGameProcessor.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

readlist = ["none", "item"]
talklist = ["pass", "agg"]

players = {}

world = {}

items = {}

spells = {}

options = {
    "stack" : False,
    
    "commandlist" : ["north", "south", "east", "west", "drop", "take", "equip", "stats", "armor", "inventory", "health", "read", "open", "talk", "eat", "delete", "powers", "unequip", "spawn", "give to", "look", "loot", "inspect", "check", "abandon"],
    "battlelist" : ["health", "armor", "equip", "stats", "inventory", "eat", "powers", "attack", "use", "cast", "unequip", "wait", "throw", "inspect", "check"],

    "northlist" : ["n", "north"],
    "southlist" : ["s", "south"],
    "eastlist" : ["e", "east"],
    "westlist" : ["w", "west"],
    "exitlist" : ["exit", "logout", "quit"],
    "invlist" : ["i", "inv", "inventory"],
    "statlist" : ["stats", "mana", "player", "class"],
    "helplist" : ["help", "?"],
    "healthlist" : ["health", "maxhealth"],
    "waitlist" : ["wait", "nothing"],
    "looklist" : ["look", "look around"],

    "spawnlist" : ["spawn"],
    "armorlist" : ["armor", "clothes", "clothing"],
    "powerlist" : ["powers"],
    "deletelist" : ["delete", "destroy"],

    "maxhealth" : 5,
    "attack" : 1,
    "mana" : 0,
    "health" : 1,

    "location" : (0,0)
    }

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print "This Is Not A Runnable File. Run TextGameProcessor Instead."
    raw_input("Press Enter To End.")
