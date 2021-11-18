import json
import math
import os
import shutil
import random

stat_pool = []
armor_log = []
weapon_log = []

#Content
with open("Data\\ArmorMaster\\Content\\PB_DT_ArmorMaster.json", "r") as file_reader:
    armor_content = json.load(file_reader)

with open("Data\\MasterStringTable\\Content\\PBMasterStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

with open("Data\\WeaponMaster\\Content\\PB_DT_WeaponMaster.json", "r") as file_reader:
    weapon_content = json.load(file_reader)

#Data
with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

stat_int = -50
for i in range(50 + 25 + 1):
    if stat_int < 0:
        for e in range(2**(abs(math.ceil(abs(stat_int)/10)-5))):
            stat_pool.append(stat_int)
    elif stat_int > 0:
        for e in range(2**(abs(math.ceil(stat_int/5)-5))*10):
            stat_pool.append(stat_int)
    stat_int += 1
for i in range(len(stat_pool)*5):
    stat_pool.append(0)

def zangetsu_black_belt():
    armor_content[109]["Value"]["STR"] = 0
    armor_content[109]["Value"]["CON"] = 0
    debug("zangetsu_black_belt()")

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
            armor_log.append(log_data)
        i += 1
    debug("rand_equip()")

def rand_weapon():
    i = 168
    while i <= 175:
        weapon_content[i]["Value"]["MeleeAttack"] = random.randint(1, 60)
        if weapon_content[i]["Value"]["SpecialEffectDenominator"] != 0.0:
            weapon_content[i]["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
        log_data = {}
        log_data["Key"] = translation["Value"][weapon_content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["MeleeAttack"] = weapon_content[i]["Value"]["MeleeAttack"]
        if weapon_content[i]["Value"]["SpecialEffectDenominator"] == 3.0:
            log_data["Value"]["SpecialEffectRate"] = "Rare"
        elif weapon_content[i]["Value"]["SpecialEffectDenominator"] == 2.0:
            log_data["Value"]["SpecialEffectRate"] = "Occasional"
        elif weapon_content[i]["Value"]["SpecialEffectDenominator"] == 1.0:
            log_data["Value"]["SpecialEffectRate"] = "Frequent"
        else:
            log_data["Value"]["SpecialEffectRate"] = "None"
        weapon_log.append(log_data)
        i += 1
    debug("rand_weapon()")

def write_patched_armor():
    with open("Serializer\\PB_DT_ArmorMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(armor_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ArmorMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ArmorMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")
    os.remove("Serializer\\PB_DT_ArmorMaster.json")
    debug("write_patched_armor()")

def write_armor():
    shutil.copyfile("Serializer\\PB_DT_ArmorMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")
    debug("write_armor()")

def write_patched_weapon():
    with open("Serializer\\PB_DT_WeaponMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(weapon_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_WeaponMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_WeaponMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset")
    os.remove("Serializer\\PB_DT_WeaponMaster.json")
    debug("write_patched_weapon()")

def write_weapon():
    shutil.copyfile("Serializer\\PB_DT_WeaponMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset")
    debug("write_weapon()")

def write_patched_master():
    with open("Serializer\\PBMasterStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBMasterStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBMasterStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")
    os.remove("Serializer\\PBMasterStringTable.json")
    debug("write_patched_master()")

def write_master():
    shutil.copyfile("Serializer\\PBMasterStringTable.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")
    debug("write_master()")

def write_armor_log():
    with open("SpoilerLog\\CheatEquipmentStats.json", "w") as file_writer:
        file_writer.write(json.dumps(armor_log, indent=2))
    debug("write_armor_log()")

def write_weapon_log():
    with open("SpoilerLog\\CheatWeaponStats.json", "w") as file_writer:
        file_writer.write(json.dumps(weapon_log, indent=2))
    debug("write_weapon_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()