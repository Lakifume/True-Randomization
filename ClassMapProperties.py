import json
import os
import shutil

log = []

def create_room_log(path):
    name, extension = os.path.splitext(path)
    log_data = {}
    log_data["Key"] = "Map"
    log_data["Value"] = {}
    log_data["Value"]["FileName"] = name.split("\\")[-1]
    log.append(log_data)
    debug("create_room_log(" + path + ")")

def write_patched_room(path):
    shutil.copyfile(path, "Serializer\\PB_DT_RoomMaster.json")
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin -force PB_DT_RoomMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_RoomMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_RoomMaster.uasset")
    os.remove("Serializer\\PB_DT_RoomMaster.json")
    debug("write_patched_room()")

def write_room():
    shutil.copyfile("Serializer\\PB_DT_RoomMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_RoomMaster.uasset")
    debug("write_room()")

def write_crown_icon():
    shutil.copyfile("Serializer\\Uasset\\icon_8bitCrown.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\K2C\\icon_8bitCrown.uasset")
    debug("write_crown_icon()")

def write_map_icon():
    shutil.copyfile("Serializer\\Uasset\\Map_Icon_Keyperson.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_Icon_Keyperson.uasset")
    shutil.copyfile("Serializer\\Uasset\\Map_Icon_RootBox.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_Icon_RootBox.uasset")
    shutil.copyfile("Serializer\\Uasset\\Map_StartingPoint.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Map\\Texture\\Map_StartingPoint.uasset")
    debug("write_map_icon()")

def write_map_log():
    with open("SpoilerLog\\MapSelection.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
    debug("write_map_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()