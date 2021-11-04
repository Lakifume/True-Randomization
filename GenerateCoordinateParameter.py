import json
import os
import shutil

#Content
with open("Data\\CoordinateParameter\\Content\\PB_DT_CoordinateParameter.json", "r") as file_reader:
    coord_content = json.load(file_reader)

with open("Data\\SystemStringTable\\Content\\PBSystemStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

def no_upgrade_cap():
    coord_content[130]["Value"]["Value"] = 9999.0
    coord_content[131]["Value"]["Value"] = 9999.0
    coord_content[3]["Value"]["Value"] = 999.0
    debug("no_upgrade_cap()")

def zangetsu_growth(nightmare):
    if nightmare:
        coord_content[51]["Value"]["Value"] = 0.0
        coord_content[52]["Value"]["Value"] = 0.0
        coord_content[53]["Value"]["Value"] = 6.2
        coord_content[54]["Value"]["Value"] = 6.0
        coord_content[55]["Value"]["Value"] = 6.0
        coord_content[56]["Value"]["Value"] = 5.8
        coord_content[57]["Value"]["Value"] = 3.0
    else:
        coord_content[53]["Value"]["Value"] = 3.1
        coord_content[54]["Value"]["Value"] = 3.0
        coord_content[55]["Value"]["Value"] = 3.0
        coord_content[56]["Value"]["Value"] = 2.9
        coord_content[57]["Value"]["Value"] = 1.5
    debug("zangetsu_growth(" + str(nightmare) + ")")

def nightmare_damage():
    coord_content[7]["Value"]["Value"] = 3.0
    coord_content[9]["Value"]["Value"] = 3.0
    coord_content[10]["Value"]["Value"] = 3.0
    debug("nightmare_damage()")

def rename_difficulty(normal, hard, nightmare):
    string_content["Table"]["SYS_SEN_Difficulty_Normal"] = normal
    string_content["Table"]["SYS_SEN_Difficulty_Hard"] = hard
    string_content["Table"]["SYS_SEN_Difficulty_Nightmare"] = nightmare
    debug("rename_difficulty(" + normal + ", " + hard + ", " + nightmare + ")")

def write_patched_coordinate():
    with open("Serializer\\PB_DT_CoordinateParameter.json", "w") as file_writer:
        file_writer.write(json.dumps(coord_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CoordinateParameter.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CoordinateParameter.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
    os.remove("Serializer\\PB_DT_CoordinateParameter.json")
    debug("write_patched_coordinate()")

def write_coordinate():
    shutil.copyfile("Serializer\\PB_DT_CoordinateParameter.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CoordinateParameter.uasset")
    debug("write_coordinate()")

def write_patched_system():
    with open("Serializer\\PBSystemStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBSystemStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBSystemStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBSystemStringTable.uasset")
    os.remove("Serializer\\PBSystemStringTable.json")
    debug("write_patched_system()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()