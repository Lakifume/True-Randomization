import json
import os
import math
import shutil
import random

stat_pool = []

cost_denominator = 4
cost_factor = 4

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

#Content
with open("Data\\ShardMaster\\Content\\PB_DT_ShardMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\ShardMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

stat_int = 33
for i in range(500 - 33 + 1):
    if stat_int <= 100:
        for e in range(math.ceil((500-100)/(100-33))):
            stat_pool.append(stat_int)
    else:
        stat_pool.append(stat_int)
    stat_int += 1
#print(stat_pool)

def rand_shard(scale):
    for i in range(79):
        if content[i]["Key"] in skip_list:
            continue
        stat_num = random.choice(stat_pool)
        content[i]["Value"]["minGradeValue"] = round(content[i]["Value"]["minGradeValue"] * (stat_num/100), 3)
        content[i]["Value"]["maxGradeValue"] = round(content[i]["Value"]["maxGradeValue"] * (stat_num/100), 3)
        if content[i]["Key"] == "LigaStreyma":
            content[73]["Value"]["minGradeValue"] = round(content[73]["Value"]["minGradeValue"] * (stat_num/100), 3)
            content[73]["Value"]["maxGradeValue"] = round(content[73]["Value"]["maxGradeValue"] * (stat_num/100), 3)
        log_data = {}
        log_data["Key"] = translation["Value"][content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["PowerPercentage"] = stat_num
        if scale:
            if stat_num > 100 and content[i]["Key"] in special_list:
                stat_num += (stat_num-100)*cost_factor
            else:
                stat_num += (stat_num-100)/cost_denominator
        else:
            stat_num = random.choice(stat_pool)
        content[i]["Value"]["useMP"] = int(content[i]["Value"]["useMP"] * (stat_num/100)) + 0.0
        if content[i]["Key"] == "LigaStreyma":
            content[73]["Value"]["useMP"] = int(content[73]["Value"]["useMP"] * (stat_num/100)) + 0.0
            if content[73]["Value"]["useMP"] <= 0.0:
                content[73]["Value"]["useMP"] = 1.0
        if content[i]["Value"]["useMP"] <= 0.0:
            content[i]["Value"]["useMP"] = 1.0
            stat_num = 1.0
        log_data["Value"]["CostPercentage"] = int(stat_num)
        log.append(log_data)
    debug("rand_shard(" + str(scale) + ")")

def eye_max():
    content[114]["Value"]["minGradeValue"] = 100.0
    content[114]["Value"]["maxGradeValue"] = 100.0
    debug("eye_max()")

def write_patched_shard():
    with open("Serializer\\PB_DT_ShardMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ShardMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ShardMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ShardMaster.uasset")
    os.remove("Serializer\\PB_DT_ShardMaster.json")
    debug("write_patched_shard()")

def write_shard():
    shutil.copyfile("Serializer\\PB_DT_ShardMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ShardMaster.uasset")
    debug("write_shard()")

def write_shard_log():
    with open("SpoilerLog\\ShardPower.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))
    debug("write_shard_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()