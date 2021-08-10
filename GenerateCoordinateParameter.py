import json
import os
import shutil

#Content
with open("Data\\CoordinateParameter\\Content\\PB_DT_CoordinateParameter.json", "r", encoding="utf-8") as file_reader:
    content = json.load(file_reader)

def change_scaling(hard, nightmare):
    content[7]["Value"]["Value"] = hard
    content[9]["Value"]["Value"] = hard
    content[10]["Value"]["Value"] = hard
    content[12]["Value"]["Value"] = nightmare
    content[14]["Value"]["Value"] = nightmare
    content[15]["Value"]["Value"] = nightmare

def bloodless_low_HP_growth():
    content[65]["Value"]["Value"] -= 10.0

def zangetsu_growth():
    content[51]["Value"]["Value"] = 40.0
    content[52]["Value"]["Value"] = 20.0
    content[53]["Value"]["Value"] = 6.2
    content[54]["Value"]["Value"] = 6.0
    content[55]["Value"]["Value"] = 6.0
    content[56]["Value"]["Value"] = 5.8
    content[57]["Value"]["Value"] = 2.94

def write_coordinate(patched):
    if patched:
        with open("Serializer\\PB_DT_CoordinateParameter.json", "w", encoding="utf-8") as file_writer:
            file_writer.write(json.dumps(content, indent=2))
        root = os.getcwd()
        os.chdir("Serializer")
        os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CoordinateParameter.json")
        os.chdir(root)
        shutil.move("Serializer\\PB_DT_CoordinateParameter.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
        os.remove("Serializer\\PB_DT_CoordinateParameter.json")
    else:
        shutil.copyfile("Serializer\\PB_DT_CoordinateParameter.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")

def reset_coordinate():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")