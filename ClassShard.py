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
    "Venomsmog"
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

def default_shard():
    for i in range(79):
        base = ClassManagement.shard_content[i]["Value"]["useMP"] * ClassManagement.shard_base_data[ClassManagement.shard_content[i]["Key"]]["Base"]
        if ClassManagement.shard_content[i]["Key"] in skip_list or ClassManagement.shard_content[i]["Key"] == "Healing":
            multiplier = 1.0
        else:
            multiplier = (base/50 - (base/50 - 1)/7.5)/(base/50)
        ClassManagement.shard_content[i]["Value"]["minGradeValue"] = round(base * multiplier, 3)
        ClassManagement.shard_content[i]["Value"]["maxGradeValue"] = round(base * multiplier * ClassManagement.shard_base_data[ClassManagement.shard_content[i]["Key"]]["Grade"], 3)
    ClassManagement.debug("ClassShard.default_shard()")

def rand_shard(scale):
    for i in range(79):
        if ClassManagement.shard_content[i]["Key"] in skip_list or ClassManagement.shard_content[i]["Key"] == "LigaDoin":
            continue
        #Power
        base = ClassManagement.shard_content[i]["Value"]["useMP"] * ClassManagement.shard_base_data[ClassManagement.shard_content[i]["Key"]]["Base"]
        multiplier = random.choice(create_list(int(base), int(ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]/20), ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]))/base
        new_base = base*multiplier
        ClassManagement.shard_content[i]["Value"]["minGradeValue"] = round(new_base, 3)
        ClassManagement.shard_content[i]["Value"]["maxGradeValue"] = round(new_base * ClassManagement.shard_base_data[ClassManagement.shard_content[i]["Key"]]["Grade"], 3)
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            doin_base = ClassManagement.shard_content[73]["Value"]["useMP"] * ClassManagement.shard_base_data[ClassManagement.shard_content[73]["Key"]]["Base"]
            ClassManagement.shard_content[73]["Value"]["minGradeValue"] = round(doin_base * multiplier, 3)
            ClassManagement.shard_content[73]["Value"]["maxGradeValue"] = round(doin_base * multiplier * ClassManagement.shard_base_data[ClassManagement.shard_content[73]["Key"]]["Grade"], 3)
        #MP
        if not scale:
            multiplier = random.choice(create_list(int(base), int(ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]/20), ClassManagement.shard_range_data[ClassManagement.shard_content[i]["Key"]]))/base
        if ClassManagement.shard_content[i]["Key"] in special_list:
            multiplier *= multiplier
        elif ClassManagement.shard_content[i]["Key"] != "Healing":
            multiplier *= (new_base/50 + (new_base/50 - 1)/6.5)/(new_base/50)
        ClassManagement.shard_content[i]["Value"]["useMP"] = int(ClassManagement.shard_content[i]["Value"]["useMP"] * multiplier) + 0.0
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            ClassManagement.shard_content[73]["Value"]["useMP"] = int(ClassManagement.shard_content[73]["Value"]["useMP"] * multiplier) + 0.0
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]] = {}
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]]["BasePower"] = round(ClassManagement.shard_content[i]["Value"]["minGradeValue"])
        log[ClassManagement.shard_translation[ClassManagement.shard_content[i]["Key"]]]["MPCost"] = round(ClassManagement.shard_content[i]["Value"]["useMP"])

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