import json
import math
import os
import shutil
import random

stat_pool = []
log = []

#Content
with open("Data\\ArmorMaster\\Content\\PB_DT_ArmorMaster.json", "r") as file_reader:
    armor_content = json.load(file_reader)

with open("Data\\MasterStringTable\\Content\\PBMasterStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

#Data
with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

stat_int = -50
for i in range(76):
    if stat_int < 0:
        for e in range(2**(abs(math.ceil(abs(stat_int)/10)-5))):
            stat_pool.append(stat_int)
    elif stat_int > 0:
        for e in range(2**(abs(math.ceil(abs(stat_int)/5)-5))*10):
            stat_pool.append(stat_int)
    else:
        for e in range(9300):
            stat_pool.append(stat_int)
    stat_int += 1

def rand_equip():
    i = 37
    while i <= 81:
        if not (i > 40 and i < 76):
            armor_content[i]["Value"]["MeleeAttack"] = random.choice(stat_pool)
            armor_content[i]["Value"]["MagicAttack"] = random.choice(stat_pool)
            armor_content[i]["Value"]["MeleeDefense"] = random.choice(stat_pool)
            armor_content[i]["Value"]["MagicDefense"] = random.choice(stat_pool)
            armor_content[i]["Value"]["ZAN"] = random.choice(stat_pool)
            armor_content[i]["Value"]["DAG"] = random.choice(stat_pool)
            armor_content[i]["Value"]["TOT"] = random.choice(stat_pool)
            armor_content[i]["Value"]["FLA"] = random.choice(stat_pool)
            armor_content[i]["Value"]["ICE"] = random.choice(stat_pool)
            armor_content[i]["Value"]["LIG"] = random.choice(stat_pool)
            armor_content[i]["Value"]["HOL"] = random.choice(stat_pool)
            armor_content[i]["Value"]["DAR"] = random.choice(stat_pool)
            armor_content[i]["Value"]["POI"] = random.choice(stat_pool)
            armor_content[i]["Value"]["CUR"] = random.choice(stat_pool)
            armor_content[i]["Value"]["STO"] = random.choice(stat_pool)
            armor_content[i]["Value"]["STR"] = random.choice(stat_pool)
            armor_content[i]["Value"]["CON"] = random.choice(stat_pool)
            armor_content[i]["Value"]["INT"] = random.choice(stat_pool)
            armor_content[i]["Value"]["MND"] = random.choice(stat_pool)
            armor_content[i]["Value"]["LUC"] = random.choice(stat_pool)
            if armor_content[i]["Value"]["MagicAttack"] != 0:
                string_content["Table"]["ITEM_EXPLAIN_" + armor_content[i]["Key"]] += "<span color=\"#ff8000\">mATK " + str(armor_content[i]["Value"]["MagicAttack"]) + " </>"
            if armor_content[i]["Value"]["MagicDefense"] != 0:
                string_content["Table"]["ITEM_EXPLAIN_" + armor_content[i]["Key"]] += "<span color=\"#ff00ff\">mDEF " + str(armor_content[i]["Value"]["MagicDefense"]) + "</>"
            log_data = {}
            log_data["Key"] = translation["Value"][armor_content[i]["Key"]]
            log_data["Value"] = {}
            log_data["Value"]["MeleeAttack"] = armor_content[i]["Value"]["MeleeAttack"]
            log_data["Value"]["MagicAttack"] = armor_content[i]["Value"]["MagicAttack"]
            log_data["Value"]["MeleeDefense"] = armor_content[i]["Value"]["MeleeDefense"]
            log_data["Value"]["MagicDefense"] = armor_content[i]["Value"]["MagicDefense"]
            log_data["Value"]["ZAN"] = armor_content[i]["Value"]["ZAN"]
            log_data["Value"]["DAG"] = armor_content[i]["Value"]["DAG"]
            log_data["Value"]["TOT"] = armor_content[i]["Value"]["TOT"]
            log_data["Value"]["FLA"] = armor_content[i]["Value"]["FLA"]
            log_data["Value"]["ICE"] = armor_content[i]["Value"]["ICE"]
            log_data["Value"]["LIG"] = armor_content[i]["Value"]["LIG"]
            log_data["Value"]["HOL"] = armor_content[i]["Value"]["HOL"]
            log_data["Value"]["DAR"] = armor_content[i]["Value"]["DAR"]
            log_data["Value"]["POI"] = armor_content[i]["Value"]["POI"]
            log_data["Value"]["CUR"] = armor_content[i]["Value"]["CUR"]
            log_data["Value"]["STO"] = armor_content[i]["Value"]["STO"]
            log_data["Value"]["STR"] = armor_content[i]["Value"]["STR"]
            log_data["Value"]["CON"] = armor_content[i]["Value"]["CON"]
            log_data["Value"]["INT"] = armor_content[i]["Value"]["INT"]
            log_data["Value"]["MND"] = armor_content[i]["Value"]["MND"]
            log_data["Value"]["LUC"] = armor_content[i]["Value"]["LUC"]
            log.append(log_data)
        i += 1

def write_patched_armor():
    with open("Serializer\\PB_DT_ArmorMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(armor_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ArmorMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ArmorMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")
    os.remove("Serializer\\PB_DT_ArmorMaster.json")

def write_armor():
    shutil.copyfile("Serializer\\PB_DT_ArmorMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")

def write_patched_master():
    with open("Serializer\\PBMasterStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBMasterStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBMasterStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")
    os.remove("Serializer\\PBMasterStringTable.json")

def write_master():
    shutil.copyfile("Serializer\\PBMasterStringTable.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")

def write_armor_log():
    with open("SpoilerLog\\CheatEquipmentStats.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))