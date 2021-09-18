import json
import math
import os
import shutil
import random

below_25_range = []
below_50_range = []
chance_6_range = []
chance_4_range = []
chance_3_range = []
chance_2_range = []
stat_pool = []
stat = [
    "ZAN",
    "DAG",
    "TOT",
    "FLA",
    "ICE",
    "LIG",
    "HOL",
    "DAR"
]
second_stat = [
    "POI",
    "CUR",
    "STO",
    "SLO"
]
log = []

#Content
with open("Data\\CharacterParameterMaster\\Content\\PB_DT_CharacterParameterMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\CharacterParameterMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

for i in range(25):
    below_25_range.append(i+1)

for i in range(50):
    below_50_range.append(i+1)

for i in range(99):
    if i <= 49:
        for e in range(5):
            chance_6_range.append(i+1)
    else:
        chance_6_range.append(i+1)

for i in range(99):
    if i <= 49:
        for e in range(3):
            chance_4_range.append(i+1)
    else:
        chance_4_range.append(i+1)

for i in range(99):
    if i <= 49:
        for e in range(2):
            chance_3_range.append(i+1)
    else:
        chance_3_range.append(i+1)

for i in range(99):
    chance_2_range.append(i+1)

stat_int = -100.0
for i in range(41):
    for e in range(4**(abs(math.ceil(abs(stat_int)/25)-4))):
        stat_pool.append(stat_int)
    stat_int += 5.0

def more_HPMP():
    content[5]["Value"]["MaxHP"] += 300
    content[5]["Value"]["MaxMP"] += 150
    content[5]["Value"]["MaxHP99Enemy"] += 300
    content[5]["Value"]["MaxMP99Enemy"] += 150
    content[6]["Value"]["MaxHP"] += 300
    content[6]["Value"]["MaxMP"] += 150
    content[6]["Value"]["MaxHP99Enemy"] += 300
    content[6]["Value"]["MaxMP99Enemy"] += 150
    content[10]["Value"]["MaxHP"] += 300
    content[10]["Value"]["MaxMP"] += 150

def rand_enemy(level, resist, custom, value):
    #NG+
    if custom:
        below_25_range.clear()
        below_25_range.append(value)
        below_50_range.clear()
        below_50_range.append(value)
        chance_6_range.clear()
        chance_6_range.append(value)
        chance_4_range.clear()
        chance_4_range.append(value)
        chance_3_range.clear()
        chance_3_range.append(value)
        chance_2_range.clear()
        chance_2_range.append(value)
    #MainCastleEnemies
    i = 12
    while i <= 107:
        if resist:
            rand_stat(i)
        if level:
            if content[i]["Key"][0:5] == "N3006":
                patch_level(below_25_range, i)
            elif content[i]["Key"][0:5] == "N3025":
                patch_level(chance_2_range, i)
            else:
                patch_level(chance_6_range, i)
        i += 1
    #DenEnemies
    i = 108
    while i <= 121:
        if resist:
            rand_stat(i)
        if level:
            patch_level(chance_4_range, i)
        i += 1
    #IceEnemies
    i = 122
    while i <= 129:
        if resist:
            rand_stat(i)
        if level:
            patch_level(chance_3_range, i)
        i += 1
    #BackerBosses
    i = 130
    while i <= 137:
        if resist:
            rand_stat(i)
        if level:
            patch_level(chance_3_range, i)
        i += 1
    #MainCastleBosses
    i = 138
    while i <= 156:
        if resist:
            rand_stat(i)
        if level:
            if content[i]["Key"][0:5] == "N1001":
                patch_level(below_25_range, i)
            elif content[i]["Key"][0:5] == "N2001":
                patch_level(below_50_range, i)
            elif content[i]["Key"][0:5] == "N2015":
                patch_level(chance_3_range, i)
            else:
                patch_level(chance_6_range, i)
        i += 1
    #EndgameBosses
    i = 157
    while i <= 177:
        if resist:
            rand_stat(i)
        if level:
            if content[i]["Key"] == "N1011":
                patch_level(below_50_range, i)
            elif content[i]["Key"] == "N1004":
                patch_level(chance_4_range, i)
            elif content[i]["Key"] == "N1008" or content[i]["Key"] == "N1011_STRONG":
                patch_level(chance_3_range, i)
            else:
                patch_level(chance_2_range, i)
        i += 1
    #Breeder
    if resist:
        rand_stat(185)
        rand_stat(186)
    if level:
        patch_level(chance_6_range, 185)
        patch_level(chance_6_range, 186)

def patch_level(array, i):
    if content[i]["Key"] == "N3001_Armor":
        content[i]["Value"]["DefaultEnemyLevel"] = content[38]["Value"]["DefaultEnemyLevel"]
        stat_scale(i)
    elif content[i]["Key"] == "N3098_Guard":
        content[i]["Value"]["DefaultEnemyLevel"] = content[i-2]["Value"]["DefaultEnemyLevel"]
        stat_scale(i)
    elif content[i]["Key"] == "N1009_Enemy":
        content[i]["Value"]["DefaultEnemyLevel"] = abs(random.choice(array) - 100)
        stat_scale(i)
        create_log(i)
    elif content[i]["Key"][0:5] == "N1013" or content[i]["Key"] == "N1009_Bael":
        content[i]["Value"]["DefaultEnemyLevel"] = abs(content[159]["Value"]["DefaultEnemyLevel"] - 100)
        stat_scale(i)
        if content[i]["Key"] == "N1013_Dominique":
            create_log(i)
    elif content[i]["Key"][0:5] == content[i-1]["Key"][0:5] and content[i]["Key"][0:5] != "N1011" or content[i]["Key"] == "JuckPod" or content[i]["Key"][0:5] == "N3125":
        content[i]["Value"]["DefaultEnemyLevel"] = content[i-1]["Value"]["DefaultEnemyLevel"]
        stat_scale(i)
    elif content[i]["Key"] != "P1003" and content[i]["Key"] != "N1011_PL" and content[i]["Key"] != "N3049" and content[i]["Key"] != "N3050" and content[i]["Key"] != "N3068":
        content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        stat_scale(i)
        create_log(i)
    
    content[i]["Value"]["HardEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["NightmareEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeDefaultEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeHardEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeNightmareEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]

def stat_scale(i):
    for e in second_stat:
        stat_num = content[i]["Value"][e]
        if content[i]["Value"]["DefaultEnemyLevel"] > content[i]["Value"]["HardEnemyLevel"]:
            stat_num += 25.0
        if content[i]["Value"]["DefaultEnemyLevel"] > (content[i]["Value"]["HardEnemyLevel"] + ((99 - content[i]["Value"]["HardEnemyLevel"]) * (1/4))):
            stat_num += 25.0
        if content[i]["Value"]["DefaultEnemyLevel"] > (content[i]["Value"]["HardEnemyLevel"] + ((99 - content[i]["Value"]["HardEnemyLevel"]) * (2/4))):
            stat_num += 25.0
        if content[i]["Value"]["DefaultEnemyLevel"] > (content[i]["Value"]["HardEnemyLevel"] + ((99 - content[i]["Value"]["HardEnemyLevel"]) * (3/4))):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        content[i]["Value"][e] = stat_num

def rand_stat(i):
    if content[i]["Value"]["ZAN"] != 100.0:
        if content[i]["Key"] == "N3015_HEAD" or content[i]["Key"] == "N1001_HEAD" or content[i]["Key"] == "N2001_HEAD":
            for e in stat:
                if content[i-1]["Value"][e] < -50:
                    content[i]["Value"][e] = -100
                else:
                    content[i]["Value"][e] = content[i-1]["Value"][e]-50
        elif content[i]["Key"] == "N3001_Armor":
            for e in stat:
                content[i]["Value"][e] = content[38]["Value"][e]
        elif content[i]["Key"] == "N1001_Tentacle":
            for e in stat:
                content[i]["Value"][e] = content[i-2]["Value"][e]
        elif content[i]["Key"] == "N2001_ARMOR":
            for e in stat:
                if content[i-2]["Value"][e] > 50:
                        content[i]["Value"][e] = 100
                else:
                    content[i]["Value"][e] = content[i-2]["Value"][e]+50
        elif content[i]["Key"][0:5] == "N1013" and content[i]["Key"] != "N1013_Bael" or content[i]["Key"] == "N1009_Bael":
            for e in stat:
                content[i]["Value"][e] = content[168]["Value"][e]
        elif content[i]["Key"][0:5] == content[i-1]["Key"][0:5] and content[i]["Key"][0:5] != "N1011" or content[i]["Key"][0:5] == "N3125":
            for e in stat:
                content[i]["Value"][e] = content[i-1]["Value"][e]
        elif content[i]["Key"] != "P1003" and content[i]["Key"] != "JuckPod" and content[i]["Key"] != "N1011_PL" and content[i]["Key"] != "N3049" and content[i]["Key"] != "N3050" and content[i]["Key"] != "N3068":
            for e in stat:
                content[i]["Value"][e] = random.choice(stat_pool)

def create_log(i):
    log_data = {}
    log_data["Key"] = translation["Value"][content[i]["Key"]]
    log_data["Value"] = {}
    log_data["Value"]["Level"] = content[i]["Value"]["DefaultEnemyLevel"]
    log_data["Value"]["MainStats"] = {}
    log_data["Value"]["MainStats"]["HP"] = int(((content[i]["Value"]["MaxHP99Enemy"] - content[i]["Value"]["MaxHP"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["MaxHP"])
    log_data["Value"]["MainStats"]["STR"] = int(((content[i]["Value"]["STR99Enemy"] - content[i]["Value"]["STR"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["STR"])
    log_data["Value"]["MainStats"]["INT"] = int(((content[i]["Value"]["INT99Enemy"] - content[i]["Value"]["INT"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["INT"])
    log_data["Value"]["MainStats"]["CON"] = int(((content[i]["Value"]["CON99Enemy"] - content[i]["Value"]["CON"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["CON"])
    log_data["Value"]["MainStats"]["MND"] = int(((content[i]["Value"]["MND99Enemy"] - content[i]["Value"]["MND"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["MND"])
    log_data["Value"]["MainStats"]["LUC"] = int(((content[i]["Value"]["LUC99Enemy"] - content[i]["Value"]["LUC"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["LUC"])
    log_data["Value"]["MainStats"]["EXP"] = int(((content[i]["Value"]["Experience99Enemy"] - content[i]["Value"]["Experience"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["Experience"])
    log_data["Value"]["MainStats"]["AP"] = int(((content[i]["Value"]["ArtsExperience99Enemy"] - content[i]["Value"]["ArtsExperience"])/98)*(content[i]["Value"]["DefaultEnemyLevel"]-1) + content[i]["Value"]["ArtsExperience"])
    log_data["Value"]["Resistances"] = {}
    for e in stat:
        log_data["Value"]["Resistances"][e] = int(content[i]["Value"][e])
    for e in second_stat:
        log_data["Value"]["Resistances"][e] = int(content[i]["Value"][e])
    log.append(log_data)

def write_patched_chara():
    with open("Serializer\\PB_DT_CharacterParameterMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CharacterParameterMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CharacterParameterMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")
    os.remove("Serializer\\PB_DT_CharacterParameterMaster.json")

def write_chara():
    shutil.copyfile("Serializer\\PB_DT_CharacterParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")

def write_chara_log():
    with open("SpoilerLog\\Enemy.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))