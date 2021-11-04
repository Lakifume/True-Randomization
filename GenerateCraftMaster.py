import json
import os
import shutil

#Content
with open("Data\\CraftMaster\\Content\\PB_DT_CraftMaster.json", "r") as file_reader:
    content = json.load(file_reader)

def no_shard_craft():
    i = 345
    while i <= 356:
        content[i]["Value"]["Type"] = "ECraftType::None"
        i += 1
    debug("no_shard_craft()")

def write_patched_craft():
    with open("Serializer\\PB_DT_CraftMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CraftMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CraftMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset")
    os.remove("Serializer\\PB_DT_CraftMaster.json")
    debug("write_patched_craft()")

def write_craft():
    shutil.copyfile("Serializer\\PB_DT_CraftMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset")
    debug("write_craft()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()