import json
import math
import os
import shutil
import random

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

area = [
    "m01SIP",
    "m02VIL",
    "m03ENT",
    "m04GDN",
    "m05SAN",
    "m06KNG",
    "m07LIB",
    "m08TWR",
    "m09TRN",
    "m10BIG",
    "m11UGD",
    "m12SND",
    "m13ARC",
    "m14TAR",
    "m15JPN",
    "m17RVA",
    "m18ICE"
]
original_area_to_progress = {}
area_to_progress = {}
area_to_list = {}

zangetsu_exp = [
    34,
    34,
    0,
    106,
    0,
    178,
    274,
    274,
    394,
    0,
    0,
    538,
    706,
    0,
    898,
    0,
    1114,
    1354,
    1618,
    2218,
    2554,
    0,
    58,
    1906
]

log = []

#Content
with open("Data\\CharacterParameterMaster\\Content\\PB_DT_CharacterParameterMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("MapEdit\\Data\\RoomMaster\\Content\\PB_DT_RoomMaster.order", "r") as file_reader:
    original_order_data = json.load(file_reader)

with open("MapEdit\\Data\\RoomMaster\\Content\\PB_DT_RoomMaster.order", "r") as file_reader:
    order_data = json.load(file_reader)

with open("Data\\DropRateMaster\\EnemyLocation.json", "r") as file_reader:
    location = json.load(file_reader)

with open("Data\\CharacterParameterMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

stat_int = -100
for i in range(int(100/5)*2 + 1):
    for e in range(2**(abs(math.ceil(abs(stat_int)/25)-4))):
        stat_pool.append(stat_int + 0.0)
    stat_int += 5

def convert_area_to_progress():
    #General
    for i in range(len(order_data["Value"]["AreaList"])):
        original_area_to_progress[original_order_data["Value"]["AreaList"][i]] = i + 1
        area_to_progress[order_data["Value"]["AreaList"][i]] = i + 1
    #Special
    original_area_to_progress["m05SAN(2)"] = original_area_to_progress["m06KNG"]
    area_to_progress["m05SAN(2)"] = area_to_progress["m05SAN"]
    original_area_to_progress["m07LIB(2)"] = original_area_to_progress["m13ARC"]
    area_to_progress["m07LIB(2)"] = area_to_progress["m07LIB"]
    original_area_to_progress["m11UGD(2)"] = original_area_to_progress["m07LIB"]
    area_to_progress["m11UGD(2)"] = area_to_progress["m11UGD"]

def convert_area_to_list():
    #Variable
    for i in area:
        list = []
        for e in range(99):
            if e <= 49:
                for o in range(abs(area_to_progress[i] - 19)):
                    list.append(e+1)
            else:
                list.append(e+1)
        area_to_list[i] = list
    #SpecialCases
    area_to_list["m05SAN(2)"] = area_to_list["m05SAN"]
    area_to_list["m07LIB(2)"] = area_to_list["m07LIB"]
    area_to_list["m11UGD(2)"] = area_to_list["m11UGD"]
    #Static
    list = []
    for i in range(50):
        list.append(i+1)
    area_to_list["Minor"] = list
    list = []
    for i in range(99):
        list.append(i+1)
    area_to_list["Major"] = list

def load_custom_order(path):
    global order_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".order"):
        with open(name + ".order", "r") as file_reader:
            order_data = json.load(file_reader)
    debug("load_custom_order(" + path + ")")

def more_HPMP():
    content[5]["Value"]["MaxHP"] += 300.0
    content[5]["Value"]["MaxMP"] += 150.0
    content[5]["Value"]["MaxHP99Enemy"] += 300.0
    content[5]["Value"]["MaxMP99Enemy"] += 150.0
    content[6]["Value"]["MaxHP"] += 300.0
    content[6]["Value"]["MaxMP"] += 150.0
    content[6]["Value"]["MaxHP99Enemy"] += 300.0
    content[6]["Value"]["MaxMP99Enemy"] += 150.0
    debug("more_HPMP()")

def zangetsu_progress():
    #Enemies
    i = 12
    while i <= 137:
        content[i]["Value"]["Experience99Enemy"] = 0
        content[i]["Value"]["Experience"] = 0
        i += 1
    #Bosses
    i = 138
    while i <= 161:
        content[i]["Value"]["Experience99Enemy"] = zangetsu_exp[i-138]
        content[i]["Value"]["Experience"] = zangetsu_exp[i-138]
        i += 1
    #Rest
    i = 162
    while i <= 188:
        content[i]["Value"]["Experience99Enemy"] = 0
        content[i]["Value"]["Experience"] = 0
        i += 1
    debug("zangetsu_progress()")

def zangetsu_no_stats():
    content[6]["Value"]["STR"] = 0.0
    content[6]["Value"]["INT"] = 0.0
    content[6]["Value"]["CON"] = 0.0
    content[6]["Value"]["MND"] = 0.0
    content[6]["Value"]["LUC"] = 0.0
    content[6]["Value"]["STR99Enemy"] = 0.0
    content[6]["Value"]["INT99Enemy"] = 0.0
    content[6]["Value"]["CON99Enemy"] = 0.0
    content[6]["Value"]["MND99Enemy"] = 0.0
    content[6]["Value"]["LUC99Enemy"] = 0.0
    debug("write_chara_log()")

def enemy_level(level, resist, map, custom, value):
    convert_area_to_progress()
    convert_area_to_list()
    #All
    i = 12
    while i <= 176:
        if resist:
            rand_stat(i)
        if custom:
            patch_level([value], i)
        elif level:
            check = True
            for e in location:
                if content[i]["Key"] == e["Key"]:
                    check = False
                    patch_level(area_to_list[e["Value"]["AreaID"]], i)
            if check:
                patch_level([0], i)
        elif map:
            check = True
            for e in location:
                if content[i]["Key"] == e["Key"]:
                    check = False
                    #Area
                    if e["Value"]["AreaID"] == "Minor":
                        current_area = e["Value"]["NormalModeRooms"][0][:6]
                    elif e["Value"]["AreaID"] == "Major":
                        continue
                    else:
                        current_area = e["Value"]["AreaID"]
                    #Level
                    new_level = round(content[i]["Value"]["DefaultEnemyLevel"] + ((area_to_progress[current_area] - original_area_to_progress[current_area])*(40/17)))
                    if new_level < 1:
                        new_level = 1
                    if new_level > 50:
                        new_level = 50
                    patch_level([new_level], i)
            if check:
                patch_level([0], i)
        create_log(i)
        i += 1
    #Miriam
    if resist:
        rand_stat(177)
    if custom:
        patch_level([value], 177)
    elif level:
        patch_level(area_to_list["Major"], 177)
    create_log(177)
    #Breeder
    if resist:
        rand_stat(185)
        rand_stat(186)
    if custom:
        patch_level([value], 185)
        patch_level([value], 186)
    elif level:
        patch_level(area_to_list["m09TRN"], 185)
        patch_level(area_to_list["m09TRN"], 186)
    create_log(185)
    debug("enemy_level(" + str(level) + ", " + str(resist) + ", " + str(map) + ", " + str(custom) + ", " + str(value) + ")")

def patch_level(array, i):
    if content[i]["Key"] == "N3001_Armor":
        content[i]["Value"]["DefaultEnemyLevel"] = content[38]["Value"]["DefaultEnemyLevel"]
    elif content[i]["Key"] == "N3098_Guard":
        content[i]["Value"]["DefaultEnemyLevel"] = content[i-2]["Value"]["DefaultEnemyLevel"]
    elif content[i]["Key"] == "N1009_Enemy":
        content[i]["Value"]["DefaultEnemyLevel"] = abs(random.choice(array) - 100)
    elif content[i]["Key"][0:5] == "N1013" or content[i]["Key"] == "N1009_Bael":
        content[i]["Value"]["DefaultEnemyLevel"] = abs(content[159]["Value"]["DefaultEnemyLevel"] - 100)
    elif content[i]["Key"][0:5] == content[i-1]["Key"][0:5] and content[i]["Key"] != "N1011_STRONG" or content[i]["Key"][0:5] == "N3125":
        content[i]["Value"]["DefaultEnemyLevel"] = content[i-1]["Value"]["DefaultEnemyLevel"]
    else:
        content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
    stat_scale(i)
    
    content[i]["Value"]["HardEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["NightmareEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeDefaultEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeHardEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]
    content[i]["Value"]["BloodlessModeNightmareEnemyLevel"] = content[i]["Value"]["DefaultEnemyLevel"]

def stat_scale(i):
    for e in second_stat:
        stat_num = content[i]["Value"][e]
        #BossStoneCheck
        if e == "STO" and content[i]["Value"]["StoneType"] == "EPBStoneType::Boss":
            continue
        #Gain
        if content[i]["Value"]["DefaultEnemyLevel"] > content[i]["Value"]["HardEnemyLevel"]:
            stat_num += 25.0
        if content[i]["Value"]["DefaultEnemyLevel"] > content[i]["Value"]["HardEnemyLevel"] + ((99 - content[i]["Value"]["HardEnemyLevel"]) * 0.5):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        #Immunity
        if content[i]["Value"]["POI"] == 100.0 and content[i]["Value"]["CUR"] == 100.0 and content[i]["Value"]["STO"] == 100.0 and content[i]["Value"]["SLO"] == 100.0:
            continue
        #Loss
        if content[i]["Value"]["DefaultEnemyLevel"] < content[i]["Value"]["HardEnemyLevel"]:
            stat_num -= 25.0
        if content[i]["Value"]["DefaultEnemyLevel"] < content[i]["Value"]["HardEnemyLevel"] * 0.5:
            stat_num -= 25.0
        if stat_num < 0.0:
            stat_num = 0.0
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
        elif content[i]["Key"][0:5] == content[i-1]["Key"][0:5] and content[i]["Key"] != "N1011_STRONG" or content[i]["Key"][0:5] == "N3125":
            for e in stat:
                content[i]["Value"][e] = content[i-1]["Value"][e]
        else:
            for e in stat:
                content[i]["Value"][e] = random.choice(stat_pool)

def create_log(i):
    try:
        log_data = {}
        log_data["Key"] = translation["Value"][content[i]["Key"]]
    except KeyError:
        return
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
    debug("write_patched_chara()")

def write_chara():
    shutil.copyfile("Serializer\\PB_DT_CharacterParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")
    debug("write_chara()")

def write_chara_log():
    with open("SpoilerLog\\EnemyProperties.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
    debug("write_chara_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()