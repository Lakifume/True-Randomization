import json
import os
import shutil

#Content
with open("Data\\SystemStringTable\\Content\\PBSystemStringTable.json", "r") as file_reader:
    content = json.load(file_reader)

def rename_difficulty(normal, hard, nightmare):
    content["Table"]["SYS_SEN_Difficulty_Normal"] = normal
    content["Table"]["SYS_SEN_Difficulty_Hard"] = hard
    content["Table"]["SYS_SEN_Difficulty_Nightmare"] = nightmare

def write_patched_system():
    with open("Serializer\\PBSystemStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBSystemStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBSystemStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset")
    os.remove("Serializer\\PBSystemStringTable.json")

def write_system():
    shutil.copyfile("Serializer\\PBSystemStringTable.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset")

def reset_system():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset")