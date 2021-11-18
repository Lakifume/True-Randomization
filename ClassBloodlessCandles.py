import json
import random
import os
import shutil

portal_ban = [
    "m10BIG_002",
    "m10BIG_010",
    "m10BIG_014",
    "m10BIG_015"
]
highjump_ban = [
    "m03ENT_024",
    "m05SAN_003",
    "m05SAN_021",
    "m08TWR_019(2)",
    "m15JPN_005",
    "m15JPN_017",
    "m15JPN_018",
    "m88BKR_004"
]
waterprotect_ban = [
    "m11UGD_051",
    "m12SND_003",
    "m12SND_024",
    "m12SND_026",
    "m14TAR_002",
    "m14TAR_006",
    "m17RVA_004",
    "m17RVA_007",
    "m17RVA_015"
]
bloodsteal_ban = [
    "m11UGD_015",
    "m11UGD_030",
    "m11UGD_038"
]

ability_room = []
ability_type = []
upgrade_room = []
upgrade_type = []
json_placeholder = []
log = []

with open("Data\\BloodlessAbilityData\\BloodlessAbility.json", "r") as file_reader:
    ability = json.load(file_reader)

with open("Data\\BloodlessAbilityData\\BloodlessUpgrade.json", "r") as file_reader:
    upgrade = json.load(file_reader)

with open("Data\\BloodlessAbilityData\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

for i in ability:
    ability_type.append(i["Key"])
    ability_room.append(i["Value"]["RoomId"])

for i in upgrade:
    upgrade_type.append(i["Key"])
    upgrade_room.append(i["Value"]["RoomId"])

for i in portal_ban:
    highjump_ban.append(i)

for i in portal_ban:
    waterprotect_ban.append(i)

for i in waterprotect_ban:
    bloodsteal_ban.append(i)

def chaos_candle():
    for i in ability:
        upgrade_room.append(i["Value"]["RoomId"])
    for i in upgrade:
        ability_room.append(i["Value"]["RoomId"])
    debug("chaos_candle()")

def candle_shuffle():
    #HighJump
    
    highjump_location = random.choice(ability_room)
    while highjump_location in highjump_ban:
        highjump_location = random.choice(ability_room)
    highjump_location = any_pick([highjump_location])
    
    #WaterProtect
    
    if highjump_location in waterprotect_ban:
        for i in highjump_ban:
            waterprotect_ban.append(i)
    
    waterprotect_location = random.choice(ability_room)
    while waterprotect_location in waterprotect_ban:
        waterprotect_location = random.choice(ability_room)
    waterprotect_location = any_pick([waterprotect_location])
    
    #BloodSteal
    
    if highjump_location in bloodsteal_ban and waterprotect_location in highjump_ban:
        for i in highjump_ban:
            bloodsteal_ban.append(i)
    
    if not waterprotect_location in bloodsteal_ban:
        bloodsteal_ban.clear()
    
    bloodsteal_location = random.choice(ability_room)
    while bloodsteal_location in bloodsteal_ban:
        bloodsteal_location = random.choice(ability_room)
    bloodsteal_location = any_pick([bloodsteal_location])

    for i in ability_type:
        entry = {}
        entry["Key"] = i
        entry["Value"] = {}
        if i == "BLD_ABILITY_HIGH_JUMP(0)":
            entry["Value"]["RoomId"] = highjump_location
        elif i == "BLD_ABILITY_WATER_PROTECT(0)":
            entry["Value"]["RoomId"] = waterprotect_location
        elif i == "BLD_ABILITY_BLOOD_STEAL(0)":
            entry["Value"]["RoomId"] = bloodsteal_location
        else:
            entry["Value"]["RoomId"] = any_pick(ability_room)
        json_placeholder.append(entry)
    
    for i in upgrade_type:
        entry = {}
        entry["Key"] = i
        entry["Value"] = {}
        entry["Value"]["RoomId"] = any_pick(upgrade_room)
        json_placeholder.append(entry)
    
    debug("candle_shuffle()")

def any_pick(item_array):
    item = random.choice(item_array)
    if item in ability_room:
        ability_room.remove(item)
    if item in upgrade_room:
        upgrade_room.remove(item)
    return item

def write_patched_gimmick():
    #Start
    print("mXXXXX_XXX_Gimmick.umap")
    tower_check = 0
    for i in json_placeholder:
        #RoomToFile
        file_name = i["Value"]["RoomId"].replace(")", "").split("(")[0] + "_Gimmick"
        #TowerCheck
        if i["Value"]["RoomId"] == "m08TWR_019":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_BLOOD_STEAL"
        elif i["Value"]["RoomId"] == "m08TWR_019(2)":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP"
        else:
            search = "EPBBloodlessAbilityType::"
        #ReadJson
        if "m08TWR_019" in file_name and tower_check == 1:
            with open("UAssetGUI\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        else:
            with open("UAssetGUI\\Json\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        #PatchJson
        for e in content["Exports"]:
            try:
                if search in e["Data"][1]["Value"]:
                    e["Data"][1]["Value"] = "EPBBloodlessAbilityType::" + i["Key"]
            except TypeError:
                continue
            except IndexError:
                continue
        for e in range(len(content["NameMap"])):
            if search in content["NameMap"][e]:
                content["NameMap"][e] = "EPBBloodlessAbilityType::" + i["Key"][:-3]
        #WriteJson
        with open("UAssetGUI\\" + file_name + ".json", "w") as file_writer:
            file_writer.write(json.dumps(content))
        #UAssetGUI
        if not ("m08TWR_019" in file_name and tower_check == 0):
            #CommandFromJson
            root = os.getcwd()
            os.chdir("UAssetGUI")
            os.system("cmd /c UAssetGUI.exe fromjson " + file_name + ".json " + file_name + ".umap")
            os.chdir(root)
            #Move
            shutil.move("UAssetGUI\\" + file_name + ".umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name + ".umap")
            #Delete
            os.remove("UAssetGUI\\" + file_name + ".json")
        #TowerCheck
        if "m08TWR_019" in file_name:
            tower_check += 1
    #Done
    print("Done")
    debug("write_patched_gimmick()")

def create_gimmick_log():
    candle_type = []
    for i in json_placeholder:
        if not i["Key"].replace(")", "").split("(")[0] in candle_type:
            candle_type.append(i["Key"].replace(")", "").split("(")[0])
    for i in candle_type:
        log_data = {}
        log_data["Key"] = translation["Value"][i]
        log_data["Value"] = {}
        log_data["Value"]["RoomList"] = []
        log.append(log_data)
    for i in json_placeholder:
        for e in log:
            if e["Key"] == translation["Value"][i["Key"].replace(")", "").split("(")[0]]:
                e["Value"]["RoomList"].append(i["Value"]["RoomId"].replace(")", "").split("(")[0])
    debug("create_gimmick_log()")

def write_gimmick_log():
    for i in log:
        i["Value"]["RoomList"].sort()
    with open("MapEdit\\Key\\KeyLocation.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
    debug("write_gimmick_log()")

def convert_to_json():
    for i in os.listdir("UAssetGUI\\Umap"):
        shutil.copyfile("UAssetGUI\\Umap\\" + i, "UAssetGUI\\" + i)
        
        root = os.getcwd()
        os.chdir("UAssetGUI")
        os.system("cmd /c UAssetGUI.exe tojson " + i + " " + i[:-5] + ".json 514")
        os.chdir(root)
        
        shutil.move("UAssetGUI\\" + i[:-5] + ".json", "UAssetGUI\\Json\\" + i[:-5] + ".json")
        os.remove("UAssetGUI\\" + i)

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()