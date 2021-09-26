import json
import os
import math
import shutil
import random

percent_range = []
percent_range_hold_type = []
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
with open("Data\\ShardMaster\\ShardRange.json", "r") as file_reader:
    data = json.load(file_reader)

with open("Data\\ShardMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

if data["Value"]["Min"] <= 100:
    i = data["Value"]["Min"]
    while i <= 100:
        percent_range.append(i)
        i += 1

if data["Value"]["Max"] > 100:
    increase = math.ceil((data["Value"]["Max"]-100)/(100-data["Value"]["Min"]))
    i = 100 + increase
    while i <= data["Value"]["Max"]:
        percent_range.append(i)
        i += increase
    if not data["Value"]["Max"] in percent_range:
        percent_range.append(data["Value"]["Max"])

def rand_shard(scale):
    for i in range(79):
        if content[i]["Key"] in skip_list:
            continue
        percent = random.choice(percent_range)
        content[i]["Value"]["minGradeValue"] = round(content[i]["Value"]["minGradeValue"] * (percent/100), 3)
        content[i]["Value"]["maxGradeValue"] = round(content[i]["Value"]["maxGradeValue"] * (percent/100), 3)
        if content[i]["Key"] == "LigaStreyma":
            content[73]["Value"]["minGradeValue"] = round(content[73]["Value"]["minGradeValue"] * (percent/100), 3)
            content[73]["Value"]["maxGradeValue"] = round(content[73]["Value"]["maxGradeValue"] * (percent/100), 3)
        log_data = {}
        log_data["Key"] = translation["Value"][content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["PowerPercentage"] = percent
        if scale:
            if percent > 100 and content[i]["Key"] in special_list:
                percent += (percent-100)*4
            else:
                percent += (percent-100)/4
        else:
            percent = random.choice(percent_range)
        content[i]["Value"]["useMP"] = int(content[i]["Value"]["useMP"] * (percent/100)) + 0.0
        if content[i]["Key"] == "LigaStreyma":
            content[73]["Value"]["useMP"] = int(content[73]["Value"]["useMP"] * (percent/100)) + 0.0
            if content[73]["Value"]["useMP"] <= 0.0:
                content[73]["Value"]["useMP"] = 1.0
        if content[i]["Value"]["useMP"] <= 0.0:
            content[i]["Value"]["useMP"] = 1.0
            percent = 1.0
        log_data["Value"]["CostPercentage"] = int(percent)
        log.append(log_data)

def eye_max():
    content[114]["Value"]["minGradeValue"] = content[114]["Value"]["maxGradeValue"]

def write_patched_shard():
    with open("Serializer\\PB_DT_ShardMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ShardMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ShardMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ShardMaster.uasset")
    os.remove("Serializer\\PB_DT_ShardMaster.json")

def write_shard():
    shutil.copyfile("Serializer\\PB_DT_ShardMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ShardMaster.uasset")

def write_shard_log():
    with open("SpoilerLog\\ShardPower.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))