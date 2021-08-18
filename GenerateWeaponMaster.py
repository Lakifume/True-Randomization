import json
import os
import shutil
import random

log = []

#Content
with open("Data\\WeaponMaster\\Content\\PB_DT_WeaponMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\WeaponMaster\\WeaponRange.json", "r") as file_reader:
    data = json.load(file_reader)

with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

def rand_weapon(power, rate):
    if power:
        i = 168
        while i <= 175:
            content[i]["Value"]["MeleeAttack"] = random.randint(data["Value"]["Min"], data["Value"]["Max"])
            i += 1
    if rate:
        content[171]["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
        content[173]["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
        content[174]["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
        content[175]["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
    i = 168
    while i <= 175:
        log_data = {}
        log_data["Key"] = translation["Value"][content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["WeaponPower"] = content[i]["Value"]["MeleeAttack"]
        if content[i]["Value"]["SpecialEffectDenominator"] == 3.0:
            log_data["Value"]["SpecialEffectRate"] = "Rare"
        elif content[i]["Value"]["SpecialEffectDenominator"] == 2.0:
            log_data["Value"]["SpecialEffectRate"] = "Occasional"
        elif content[i]["Value"]["SpecialEffectDenominator"] == 1.0:
            log_data["Value"]["SpecialEffectRate"] = "Frequent"
        else:
            log_data["Value"]["SpecialEffectRate"] = "None"
        log.append(log_data)
        i += 1

def write_patched_weapon():
    with open("Serializer\\PB_DT_WeaponMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_WeaponMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_WeaponMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset")
    os.remove("Serializer\\PB_DT_WeaponMaster.json")

def write_weapon():
    shutil.copyfile("Serializer\\PB_DT_WeaponMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset")

def reset_weapon():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_WeaponMaster.uasset")

def write_weapon_log():
    with open("SpoilerLog\\Weapon.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))

def reset_weapon_log():
    if os.path.isfile("SpoilerLog\\Weapon.json"):
        os.remove("SpoilerLog\\Weapon.json")