from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Room
import Graphic
import Sound
import Bloodless

def init():
    global wheight_exponents
    wheight_exponents = [3, 1.8, 1.25]

def simplify_item_name(name):
    return name.replace("Familiar:", "").replace(" ", "").replace("'", "").replace("-", "").replace(".", "").replace("é", "e").replace("è", "e").replace("&", "and").lower()

def remove_inst_number(name):
    #Return a string without its instance number the same way Unreal does it
    name = name.split("_")
    if name[-1][0] != "0":
        try:
            int(name[-1])
            name.pop()
        except ValueError:
            pass
    return "_".join(name)

def export_name_to_index(filename, export_name):
    count = 0
    for export in game_data[filename].Exports:
        if str(export.ObjectName) == export_name:
            return count
        count += 1
    raise Exception("Export not found")

def squircle(value, exponent):
    return -(1-value**exponent)**(1/exponent)+1

def invert_squircle(value, exponent):
    return (1-(-value+1)**exponent)**(1/exponent)

def random_weighted(value, minimum, maximum, step, exponent, adaptive = True):
    full_range = maximum - minimum
    if random.randint(0, 1) > 0:
        distance = maximum - value
        if adaptive:
            exponent = (exponent-1)*(0.5*4**(distance/full_range))+1
        return round(round((value + squircle(random.random(), exponent)*distance)/step)*step, 3)
    else:
        distance = value - minimum
        if adaptive:
            exponent = (exponent-1)*(0.5*4**(distance/full_range))+1
        return round(round((value - squircle(random.random(), exponent)*distance)/step)*step, 3)