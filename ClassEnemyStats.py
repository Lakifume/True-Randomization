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
    chara_content = json.load(file_reader)

with open("Data\\CoordinateParameter\\Content\\PB_DT_CoordinateParameter.json", "r") as file_reader:
    coord_content = json.load(file_reader)

with open("Data\\SystemStringTable\\Content\\PBSystemStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

with open("Data\\SpecialEffectDefinitionMaster\\Content\\PB_DT_SpecialEffectDefinitionMaster.json", "r") as file_reader:
    effect_content = json.load(file_reader)

with open("Data\\BRVAttackDamage\\Content\\PB_DT_BRVAttackDamage.json", "r") as file_reader:
    brv_content = json.load(file_reader)

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
        original_area_to_progress[original_order_data["Value"]["AreaList"][i]] = i + 1.0
        area_to_progress[order_data["Value"]["AreaList"][i]] = i + 1.0
    #Special
    original_area_to_progress["m04GDN(2)"] = (original_area_to_progress["m04GDN"] + original_area_to_progress["m05SAN"])/2
    area_to_progress["m04GDN(2)"] = area_to_progress["m04GDN"]
    original_area_to_progress["m05SAN(2)"] = original_area_to_progress["m06KNG"]
    area_to_progress["m05SAN(2)"] = area_to_progress["m05SAN"]
    original_area_to_progress["m07LIB(2)"] = original_area_to_progress["m06KNG"]
    area_to_progress["m07LIB(2)"] = area_to_progress["m07LIB"]
    original_area_to_progress["m08TWR(2)"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m08TWR(2)"] = area_to_progress["m08TWR"]
    original_area_to_progress["m11UGD(2)"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m11UGD(2)"] = area_to_progress["m11UGD"]

def convert_area_to_list():
    #Variable
    for i in area:
        list = []
        for e in range(99):
            if e <= 49:
                for o in range(abs(int(area_to_progress[i]) - 19)):
                    list.append(e+1)
            else:
                list.append(e+1)
        area_to_list[i] = list
    #SpecialCases
    area_to_list["m04GDN(2)"] = area_to_list["m04GDN"]
    area_to_list["m05SAN(2)"] = area_to_list["m05SAN"]
    area_to_list["m07LIB(2)"] = area_to_list["m07LIB"]
    area_to_list["m08TWR(2)"] = area_to_list["m08TWR"]
    area_to_list["m11UGD(2)"] = area_to_list["m11UGD"]
    #Static
    list = []
    for i in range(50):
        list.append(i+1)
    area_to_list["Minor"] = list
    list = []
    for e in range(99):
        if e <= 49:
            for o in range(2):
                list.append(e+1)
        else:
            list.append(e+1)
    area_to_list["PreMajor"] = list
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

def rename_difficulty(normal, hard, nightmare):
    string_content["Table"]["SYS_SEN_Difficulty_Normal"] = normal
    string_content["Table"]["SYS_SEN_Difficulty_Hard"] = hard
    string_content["Table"]["SYS_SEN_Difficulty_Nightmare"] = nightmare
    debug("rename_difficulty(" + normal + ", " + hard + ", " + nightmare + ")")

def more_HPMP():
    chara_content[5]["Value"]["MaxHP"] += 300.0
    chara_content[5]["Value"]["MaxMP"] += 150.0
    chara_content[5]["Value"]["MaxHP99Enemy"] += 300.0
    chara_content[5]["Value"]["MaxMP99Enemy"] += 150.0
    chara_content[6]["Value"]["MaxHP"] += 300.0
    chara_content[6]["Value"]["MaxMP"] += 150.0
    chara_content[6]["Value"]["MaxHP99Enemy"] += 300.0
    chara_content[6]["Value"]["MaxMP99Enemy"] += 150.0
    debug("more_HPMP()")

def no_upgrade_cap():
    coord_content[130]["Value"]["Value"] = 9999.0
    coord_content[131]["Value"]["Value"] = 9999.0
    coord_content[3]["Value"]["Value"] = 999.0
    debug("no_upgrade_cap()")

def low_HPMP_growth():
    effect_content[105]["Value"]["Parameter01"] -= 10.0
    effect_content[106]["Value"]["Parameter01"] -= 5.0
    debug("low_HPMP_growth()")

def zangetsu_growth(nightmare):
    if nightmare:
        coord_content[51]["Value"]["Value"] = 0.0
        coord_content[52]["Value"]["Value"] = 0.0
        coord_content[53]["Value"]["Value"] = 6.2
        coord_content[54]["Value"]["Value"] = 6.0
        coord_content[55]["Value"]["Value"] = 6.0
        coord_content[56]["Value"]["Value"] = 5.8
        coord_content[57]["Value"]["Value"] = 3.0
    else:
        coord_content[53]["Value"]["Value"] = 3.1
        coord_content[54]["Value"]["Value"] = 3.0
        coord_content[55]["Value"]["Value"] = 3.0
        coord_content[56]["Value"]["Value"] = 2.9
        coord_content[57]["Value"]["Value"] = 1.5
    debug("zangetsu_growth(" + str(nightmare) + ")")

def nightmare_damage():
    coord_content[7]["Value"]["Value"] = 3.0
    coord_content[9]["Value"]["Value"] = 3.0
    coord_content[10]["Value"]["Value"] = 3.0
    debug("nightmare_damage()")

def zangetsu_progress():
    #Enemies
    i = 12
    while i <= 137:
        chara_content[i]["Value"]["Experience99Enemy"] = 0
        chara_content[i]["Value"]["Experience"] = 0
        i += 1
    #Bosses
    i = 138
    while i <= 161:
        chara_content[i]["Value"]["Experience99Enemy"] = zangetsu_exp[i-138]
        chara_content[i]["Value"]["Experience"] = zangetsu_exp[i-138]
        i += 1
    #Rest
    i = 162
    while i <= 188:
        chara_content[i]["Value"]["Experience99Enemy"] = 0
        chara_content[i]["Value"]["Experience"] = 0
        i += 1
    debug("zangetsu_progress()")

def zangetsu_no_stats():
    chara_content[6]["Value"]["STR"] = 0.0
    chara_content[6]["Value"]["INT"] = 0.0
    chara_content[6]["Value"]["CON"] = 0.0
    chara_content[6]["Value"]["MND"] = 0.0
    chara_content[6]["Value"]["LUC"] = 0.0
    chara_content[6]["Value"]["STR99Enemy"] = 0.0
    chara_content[6]["Value"]["INT99Enemy"] = 0.0
    chara_content[6]["Value"]["CON99Enemy"] = 0.0
    chara_content[6]["Value"]["MND99Enemy"] = 0.0
    chara_content[6]["Value"]["LUC99Enemy"] = 0.0
    debug("write_chara_log()")

def brv_speed():
    chara_content[159]["Value"]["AnimaionPlayRateNormal"] = 1.25
    chara_content[161]["Value"]["AnimaionPlayRateNormal"] = 1.25
    chara_content[177]["Value"]["AnimaionPlayRateNormal"] = 1.25
    debug("brv_speed()")

def brv_damage(factor):
    for i in brv_content:
        i["Value"]["VsAndrealphus"] *= factor
        i["Value"]["VsBathin"] *= factor
        i["Value"]["VsBloodless"] *= factor
        i["Value"]["VsGremory"] *= factor
    debug("brv_damage(" + str(factor) + ")")

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
                if chara_content[i]["Key"] == e["Key"]:
                    check = False
                    patch_level(area_to_list[e["Value"]["AreaID"]], i)
            if check:
                patch_level([0], i)
        elif map:
            check = True
            for e in location:
                if chara_content[i]["Key"] == e["Key"]:
                    check = False
                    #Area
                    if e["Value"]["AreaID"] == "Minor":
                        current_area = e["Value"]["NormalModeRooms"][0][:6]
                    elif "Major" in e["Value"]["AreaID"]:
                        continue
                    else:
                        current_area = e["Value"]["AreaID"]
                    #Level
                    new_level = round(chara_content[i]["Value"]["DefaultEnemyLevel"] + ((area_to_progress[current_area] - original_area_to_progress[current_area])*(40/17)))
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
        patch_level(area_to_list["Major"], 185)
        patch_level(area_to_list["Major"], 186)
    create_log(185)
    debug("enemy_level(" + str(level) + ", " + str(resist) + ", " + str(map) + ", " + str(custom) + ", " + str(value) + ")")

def patch_level(array, i):
    #BuerArmor
    if chara_content[i]["Key"] == "N3001_Armor":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = chara_content[38]["Value"]["DefaultEnemyLevel"]
    #Scylla
    elif chara_content[i]["Key"] == "N3098_Guard":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = chara_content[i-2]["Value"]["DefaultEnemyLevel"]
    #Vepar
    elif chara_content[i]["Key"] == "N1001":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        chara_content[i]["Value"]["BloodlessModeEnemyHPOverride"] = int(int(((chara_content[i]["Value"]["MaxHP99Enemy"] - chara_content[i]["Value"]["MaxHP"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["MaxHP"])*2.0) + 0.0
    #Gebel
    elif chara_content[i]["Key"] == "N1012":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        coord_content[140]["Value"]["Value"] = int(int(((chara_content[i]["Value"]["MaxHP99Enemy"] - chara_content[i]["Value"]["MaxHP"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["MaxHP"])*0.15) + 0.0
    #Dom
    elif chara_content[i]["Key"] == "N1009_Enemy":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = abs(random.choice(array) - 100)
    #Bael
    elif chara_content[i]["Key"][0:5] == "N1013" or chara_content[i]["Key"] == "N1009_Bael":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = abs(chara_content[159]["Value"]["DefaultEnemyLevel"] - 100)
    #Duplicate
    elif chara_content[i]["Key"][0:5] == chara_content[i-1]["Key"][0:5] and chara_content[i]["Key"] != "N1011_STRONG" or chara_content[i]["Key"][0:5] == "N3125":
        chara_content[i]["Value"]["DefaultEnemyLevel"] = chara_content[i-1]["Value"]["DefaultEnemyLevel"]
        chara_content[i]["Value"]["BloodlessModeEnemyHPOverride"] = chara_content[i-1]["Value"]["BloodlessModeEnemyHPOverride"]
    #Other
    else:
        chara_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
    stat_scale(i)
    
    chara_content[i]["Value"]["HardEnemyLevel"] = chara_content[i]["Value"]["DefaultEnemyLevel"]
    chara_content[i]["Value"]["NightmareEnemyLevel"] = chara_content[i]["Value"]["DefaultEnemyLevel"]
    chara_content[i]["Value"]["BloodlessModeDefaultEnemyLevel"] = chara_content[i]["Value"]["DefaultEnemyLevel"]
    chara_content[i]["Value"]["BloodlessModeHardEnemyLevel"] = chara_content[i]["Value"]["DefaultEnemyLevel"]
    chara_content[i]["Value"]["BloodlessModeNightmareEnemyLevel"] = chara_content[i]["Value"]["DefaultEnemyLevel"]

def stat_scale(i):
    for e in second_stat:
        stat_num = chara_content[i]["Value"][e]
        #BossStoneCheck
        if e == "STO" and chara_content[i]["Value"]["StoneType"] == "EPBStoneType::Boss":
            continue
        #Gain
        if chara_content[i]["Value"]["DefaultEnemyLevel"] > chara_content[i]["Value"]["HardEnemyLevel"]:
            stat_num += 25.0
        if chara_content[i]["Value"]["DefaultEnemyLevel"] > chara_content[i]["Value"]["HardEnemyLevel"] + ((99 - chara_content[i]["Value"]["HardEnemyLevel"]) * 0.5):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        if e == "STO" and stat_num > 99.9:
            stat_num = 99.9
        #Immunity
        if chara_content[i]["Value"]["POI"] == 100.0 and chara_content[i]["Value"]["CUR"] == 100.0 and chara_content[i]["Value"]["STO"] >= 99.0 and chara_content[i]["Value"]["SLO"] == 100.0:
            continue
        #Loss
        if chara_content[i]["Value"]["DefaultEnemyLevel"] < chara_content[i]["Value"]["HardEnemyLevel"]:
            stat_num = math.ceil(stat_num - 25.0)
        if chara_content[i]["Value"]["DefaultEnemyLevel"] < chara_content[i]["Value"]["HardEnemyLevel"] * 0.5:
            stat_num -= 25.0
        if stat_num < 0.0:
            stat_num = 0.0
        chara_content[i]["Value"][e] = stat_num

def rand_stat(i):
    #Immunity
    if chara_content[i]["Value"]["ZAN"] == 100.0 and chara_content[i]["Value"]["DAG"] == 100.0 and chara_content[i]["Value"]["TOT"] == 100.0 and chara_content[i]["Value"]["FLA"] == 100.0 and chara_content[i]["Value"]["ICE"] == 100.0 and chara_content[i]["Value"]["LIG"] == 100.0 and chara_content[i]["Value"]["HOL"] == 100.0 and chara_content[i]["Value"]["DAR"] == 100.0:
        return
    #WeakPoints
    if chara_content[i]["Key"] == "N3015_HEAD" or chara_content[i]["Key"] == "N1001_HEAD" or chara_content[i]["Key"] == "N2001_HEAD":
        for e in stat:
            if chara_content[i-1]["Value"][e] < -20:
                chara_content[i]["Value"][e] = -100
            else:
                chara_content[i]["Value"][e] = chara_content[i-1]["Value"][e]-80
    #BuerArmor
    elif chara_content[i]["Key"] == "N3001_Armor":
        for e in stat:
            chara_content[i]["Value"][e] = chara_content[38]["Value"][e]
    #Vepar
    elif chara_content[i]["Key"] == "N1001_Tentacle":
        for e in stat:
            chara_content[i]["Value"][e] = chara_content[i-2]["Value"][e]
    #StrongParts
    elif chara_content[i]["Key"] == "N3108_GUARD" or chara_content[i]["Key"] == "N2001_ARMOR":
        for e in stat:
            if chara_content[i-2]["Value"][e] > 20:
                    chara_content[i]["Value"][e] = 100
            else:
                chara_content[i]["Value"][e] = chara_content[i-2]["Value"][e]+80
    #Bael
    elif chara_content[i]["Key"][0:5] == "N1013" and chara_content[i]["Key"] != "N1013_Bael" or chara_content[i]["Key"] == "N1009_Bael":
        for e in stat:
            chara_content[i]["Value"][e] = chara_content[168]["Value"][e]
    #Duplicate
    elif chara_content[i]["Key"][0:5] == chara_content[i-1]["Key"][0:5] and chara_content[i]["Key"] != "N1011_STRONG" or chara_content[i]["Key"][0:5] == "N3125":
        for e in stat:
            chara_content[i]["Value"][e] = chara_content[i-1]["Value"][e]
    #Other
    else:
        for e in stat:
            chara_content[i]["Value"][e] = random.choice(stat_pool)

def create_log(i):
    try:
        log_data = {}
        log_data["Key"] = translation["Value"][chara_content[i]["Key"]]
    except KeyError:
        return
    log_data["Value"] = {}
    log_data["Value"]["Level"] = chara_content[i]["Value"]["DefaultEnemyLevel"]
    log_data["Value"]["MainStats"] = {}
    log_data["Value"]["MainStats"]["HP"] = int(((chara_content[i]["Value"]["MaxHP99Enemy"] - chara_content[i]["Value"]["MaxHP"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["MaxHP"])
    log_data["Value"]["MainStats"]["STR"] = int(((chara_content[i]["Value"]["STR99Enemy"] - chara_content[i]["Value"]["STR"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["STR"])
    log_data["Value"]["MainStats"]["INT"] = int(((chara_content[i]["Value"]["INT99Enemy"] - chara_content[i]["Value"]["INT"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["INT"])
    log_data["Value"]["MainStats"]["CON"] = int(((chara_content[i]["Value"]["CON99Enemy"] - chara_content[i]["Value"]["CON"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["CON"])
    log_data["Value"]["MainStats"]["MND"] = int(((chara_content[i]["Value"]["MND99Enemy"] - chara_content[i]["Value"]["MND"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["MND"])
    log_data["Value"]["MainStats"]["LUC"] = int(((chara_content[i]["Value"]["LUC99Enemy"] - chara_content[i]["Value"]["LUC"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["LUC"])
    log_data["Value"]["MainStats"]["EXP"] = int(((chara_content[i]["Value"]["Experience99Enemy"] - chara_content[i]["Value"]["Experience"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["Experience"])
    log_data["Value"]["MainStats"]["AP"] = int(((chara_content[i]["Value"]["ArtsExperience99Enemy"] - chara_content[i]["Value"]["ArtsExperience"])/98)*(chara_content[i]["Value"]["DefaultEnemyLevel"]-1) + chara_content[i]["Value"]["ArtsExperience"])
    log_data["Value"]["Resistances"] = {}
    for e in stat:
        log_data["Value"]["Resistances"][e] = int(chara_content[i]["Value"][e])
    for e in second_stat:
        log_data["Value"]["Resistances"][e] = int(chara_content[i]["Value"][e])
    log.append(log_data)

def write_patched_chara():
    with open("Serializer\\PB_DT_CharacterParameterMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(chara_content, indent=2))
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

def write_patched_coordinate():
    with open("Serializer\\PB_DT_CoordinateParameter.json", "w") as file_writer:
        file_writer.write(json.dumps(coord_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CoordinateParameter.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CoordinateParameter.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
    os.remove("Serializer\\PB_DT_CoordinateParameter.json")
    debug("write_patched_coordinate()")

def write_coordinate():
    shutil.copyfile("Serializer\\PB_DT_CoordinateParameter.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
    debug("write_coordinate()")

def write_patched_system():
    with open("Serializer\\PBSystemStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBSystemStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBSystemStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset")
    os.remove("Serializer\\PBSystemStringTable.json")
    debug("write_patched_system()")

def write_patched_effect():
    with open("Serializer\\PB_DT_SpecialEffectDefinitionMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(effect_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_SpecialEffectDefinitionMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_SpecialEffectDefinitionMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset")
    os.remove("Serializer\\PB_DT_SpecialEffectDefinitionMaster.json")
    debug("write_patched_effect()")

def write_effect():
    shutil.copyfile("Serializer\\PB_DT_SpecialEffectDefinitionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset")
    debug("write_effect()")

def write_patched_brv_atk():
    with open("Serializer\\PB_DT_BRVAttackDamage.json", "w") as file_writer:
        file_writer.write(json.dumps(brv_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BRVAttackDamage.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BRVAttackDamage.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset")
    os.remove("Serializer\\PB_DT_BRVAttackDamage.json")
    debug("write_patched_brv_atk()")

def write_brv_atk():
    shutil.copyfile("Serializer\\PB_DT_BRVAttackDamage.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset")
    debug("write_brv_atk()")

def write_chara_log():
    with open("SpoilerLog\\EnemyProperties.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
    debug("write_chara_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()