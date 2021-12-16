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
log = []

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
        stat_num = random.choice(stat_pool)
        ClassManagement.shard_content[i]["Value"]["minGradeValue"] = round(ClassManagement.shard_content[i]["Value"]["minGradeValue"] * (stat_num/100), 3)
        ClassManagement.shard_content[i]["Value"]["maxGradeValue"] = round(ClassManagement.shard_content[i]["Value"]["maxGradeValue"] * (stat_num/100), 3)
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            ClassManagement.shard_content[73]["Value"]["minGradeValue"] = round(ClassManagement.shard_content[73]["Value"]["minGradeValue"] * (stat_num/100), 3)
            ClassManagement.shard_content[73]["Value"]["maxGradeValue"] = round(ClassManagement.shard_content[73]["Value"]["maxGradeValue"] * (stat_num/100), 3)
        log_data = {}
        log_data["Key"] = ClassManagement.shard_translation["Value"][ClassManagement.shard_content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["PowerPercentage"] = stat_num
        if scale:
            if stat_num > 100 and ClassManagement.shard_content[i]["Key"] in special_list:
                stat_num += (stat_num-100)*4
            else:
                stat_num += (stat_num-100)/4
        else:
            stat_num = random.choice(stat_pool)
        ClassManagement.shard_content[i]["Value"]["useMP"] = int(ClassManagement.shard_content[i]["Value"]["useMP"] * (stat_num/100)) + 0.0
        if ClassManagement.shard_content[i]["Key"] == "LigaStreyma":
            ClassManagement.shard_content[73]["Value"]["useMP"] = int(ClassManagement.shard_content[73]["Value"]["useMP"] * (stat_num/100)) + 0.0
            if ClassManagement.shard_content[73]["Value"]["useMP"] <= 0.0:
                ClassManagement.shard_content[73]["Value"]["useMP"] = 1.0
        if ClassManagement.shard_content[i]["Value"]["useMP"] <= 0.0:
            ClassManagement.shard_content[i]["Value"]["useMP"] = 1.0
            stat_num = 1.0
        log_data["Value"]["CostPercentage"] = int(stat_num)
        log.append(log_data)
    ClassManagement.debug("ClassShard.rand_shard(" + str(scale) + ")")

def eye_max_range():
    ClassManagement.shard_content[114]["Value"]["minGradeValue"] = 999.0
    ClassManagement.shard_content[114]["Value"]["maxGradeValue"] = 999.0
    ClassManagement.debug("ClassShard.eye_max_range()")

def get_log():
    return log