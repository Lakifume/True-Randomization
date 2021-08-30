import json
import os
import shutil

#Content
with open("Data\\CoordinateParameter\\Content\\PB_DT_CoordinateParameter.json", "r") as file_reader:
    content = json.load(file_reader)

def bloodless_low_HP_growth():
    content[65]["Value"]["Value"] -= 10.0

def write_patched_coordinate():
    with open("Serializer\\PB_DT_CoordinateParameter.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CoordinateParameter.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CoordinateParameter.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
    os.remove("Serializer\\PB_DT_CoordinateParameter.json")

def write_coordinate():
    shutil.copyfile("Serializer\\PB_DT_CoordinateParameter.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")

def reset_coordinate():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")