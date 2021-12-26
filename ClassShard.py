import ClassManagement
import math
import random

stat_pool = []

special_list = [
    "ChangeBunny",
    "Voidlay",
    "Chiselbalage",
    "TissRosain",
    "FoldingTurb"
]
skip_list = [
    "Bloodsteel",
    "SummonChair",
    "Demoniccapture",
    "Accelerator",
    "AccelWorld",
    "Beastguard",
    "Sacredshade",
    "Reflectionray",
    "Aquastream",
    "Dimensionshift",
    "GoldBarrett",
    "Aimingshield",
    "CurseDray",
    "Petrey",
    "PetraBless",
    "Acidgouache",
    "Venomsmog",
    "LigaDoin"
]
log = {}

def init():
    value = 100
    min = 20
    max = 500
    stat_int = min
    for i in range(max-min+1):
        if stat_int < value:
            num_range = (max-value)/(value-min)
        elif stat_int > value:
            num_range = (value-min)/(max-value)
        else:
            num_range = ((max-value)/(value-min)+(value-min)/(max-value))/2
        
        if num_range < 1:
            num_range = 1
        for e in range(round(num_range*10)):
            stat_pool.append(stat_int)
        stat_int += 1
    ClassManagement.debug("ClassShard.init()")

def rand_shard(scale):
    for i in range(79):
        if ClassManagement.shard_content[i]["Key"] in skip_list:
            continue
        multiplier = random.choice(create_list(int(ClassManagement.shard_content[i]["Value"]["minGradeValue"]), int(ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]/20), ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]))/ClassManagement.shard_content[i]["Value"]["minGradeValue"]
        ClassManagement.shard_content[i]["Value"]["minGradeValue"] = round(ClassManagement.shard_content[i]["Value"]["minGradeValue"] * multiplier) + 0.0
        ClassManagement.shard_content[i]["Value"]["maxGradeValue"] = round(ClassManagement.shard_content[i]["Value"]["maxGradeValue"] * multiplier) + 0.0
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            ClassManagement.shard_content[73]["Value"]["minGradeValue"] = round(ClassManagement.shard_content[73]["Value"]["minGradeValue"] * multiplier) + 0.0
            ClassManagement.shard_content[73]["Value"]["maxGradeValue"] = round(ClassManagement.shard_content[73]["Value"]["maxGradeValue"] * multiplier) + 0.0
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]] = {}
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]]["PowerPercentage"] = round(multiplier*100)
        if not scale:
            multiplier = random.choice(create_list(int(ClassManagement.shard_content[i]["Value"]["minGradeValue"]), int(ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]/20), ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]))/ClassManagement.shard_content[i]["Value"]["minGradeValue"]
        if multiplier > 1 and ClassManagement.shard_content[i]["Key"] in special_list:
            multiplier += (multiplier-1)*4
        ClassManagement.shard_content[i]["Value"]["useMP"] = int(ClassManagement.shard_content[i]["Value"]["useMP"] * multiplier) + 0.0
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            ClassManagement.shard_content[73]["Value"]["useMP"] = int(ClassManagement.shard_content[73]["Value"]["useMP"] * multiplier) + 0.0
            if ClassManagement.shard_content[73]["Value"]["useMP"] <= 0.0:
                ClassManagement.shard_content[73]["Value"]["useMP"] = 1.0
        if ClassManagement.shard_content[i]["Value"]["useMP"] <= 0.0:
            ClassManagement.shard_content[i]["Value"]["useMP"] = 1.0
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]]["CostPercentage"] = round(multiplier*100)

def create_list(value, minimum, maximum):
    list = []
    list_int = minimum
    for i in range(maximum-minimum+1):
        for e in range(2**(abs(math.ceil(abs(list_int-value)*5/max(value-minimum, maximum-value))-5))):
            list.append(list_int)
        list_int += 1
    return list
    ClassManagement.debug("ClassShard.rand_shard(" + str(scale) + ")")

def eye_max_range():
    ClassManagement.shard_content[114]["Value"]["minGradeValue"] = 999.0
    ClassManagement.shard_content[114]["Value"]["maxGradeValue"] = 999.0
    ClassManagement.debug("ClassShard.eye_max_range()")

def get_log():
    return log