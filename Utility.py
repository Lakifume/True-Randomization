import random

def pick_and_remove(array):
    item = random.choice(array)
    array.remove(item)
    return item

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

def split_enemy_profile(profile):
    difficulty = ""
    enemy_id = profile
    if "Normal" in profile:
        enemy_id = profile.replace("_Normal", "")
        difficulty = "Normal"
    if "Hard" in profile:
        enemy_id = profile.replace("_Hard", "")
        difficulty = "Hard"
    return (enemy_id, difficulty)