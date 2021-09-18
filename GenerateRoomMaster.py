import json
import os
import shutil

log = []

def create_room_log(path):
    log_data = {}
    log_data["Key"] = "Map"
    log_data["Value"] = {}
    log_data["Value"]["FileName"] = path.split("\\")[-1][:-5]
    log.append(log_data)

def write_patched_room(path):
    shutil.copyfile(path, "Serializer\\PB_DT_RoomMaster.json")
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin -force PB_DT_RoomMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_RoomMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_RoomMaster.uasset")
    os.remove("Serializer\\PB_DT_RoomMaster.json")

def write_room():
    shutil.copyfile("Serializer\\PB_DT_RoomMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_RoomMaster.uasset")

def write_crown_icon():
    shutil.copyfile("Serializer\\icon_8bitCrown.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\K2C\\icon_8bitCrown.uasset")

def write_map_icon():
    shutil.copyfile("Serializer\\Map_Icon_Keyperson.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_Icon_Keyperson.uasset")
    shutil.copyfile("Serializer\\Map_Icon_RootBox.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_Icon_RootBox.uasset")
    shutil.copyfile("Serializer\\Map_StartingPoint.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_StartingPoint.uasset")

def write_map_log():
    with open("SpoilerLog\\Map.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))