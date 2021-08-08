import json
import os
import shutil

#Content
with open("Data\\ArmorMaster\\Content\\PB_DT_ArmorMaster.json", "r") as file_reader:
    content = json.load(file_reader)

def no_black_belt():
    content[109]["Value"]["STR"] = 0
    content[109]["Value"]["CON"] = 0

def write_armor(patched):
    if patched:
        with open("Serializer\\PB_DT_ArmorMaster.json", "w") as file_writer:
            file_writer.write(json.dumps(content, indent=2))
        root = os.getcwd()
        os.chdir("Serializer")
        os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ArmorMaster.json")
        os.chdir(root)
        shutil.move("Serializer\\PB_DT_ArmorMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")
        os.remove("Serializer\\PB_DT_ArmorMaster.json")
    else:
        shutil.copyfile("Serializer\\PB_DT_ArmorMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")

def reset_armor():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")