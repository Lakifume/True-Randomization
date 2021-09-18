import json
import os
import shutil

#Content
with open("Data\\BloodlessAbilityData\\Content\\PB_DT_BloodlessAbilityData.json", "r") as file_reader:
    content = json.load(file_reader)

def bloodless_all_upgrades():
    for i in content:
        if i["Value"]["GimmickBloodColor"] == "EPBBloodColor::Purple":
            i["Value"]["IsUnlockedByDefault"] = True

def write_patched_bloodless():
    with open("Serializer\\PB_DT_BloodlessAbilityData.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BloodlessAbilityData.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BloodlessAbilityData.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset")
    os.remove("Serializer\\PB_DT_BloodlessAbilityData.json")

def write_bloodless():
    shutil.copyfile("Serializer\\PB_DT_BloodlessAbilityData.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset")