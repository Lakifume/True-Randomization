import json
import random
import os
import shutil

candle_to_offset = {
    "m01SIP_000": 49224,
    "m01SIP_007": 24690,
    "m01SIP_026": 21441,
    "m02VIL_004": 32424,
    "m02VIL_005": 29277,
    "m03ENT_024": 40518,
    "m04GDN_004": 20046,
    "m05SAN_003": 187124,
    "m05SAN_006": 16177,
    "m05SAN_011": 18897,
    "m05SAN_014": 28990,
    "m05SAN_016": 95486,
    "m05SAN_021": 100682,
    "m06KNG_022": 20212,
    "m07LIB_009": 32434,
    "m07LIB_012": 42204,
    "m07LIB_030": 26595,
    "m07LIB_040": 26395,
    "m07LIB_041": 24590,
    "m07LIB_042": 27173,
    "m08TWR_018": 324529,
    "m08TWR_019(1)": 162246,
    "m08TWR_019(2)": 160160,
    "m10BIG_002": 27960,
    "m10BIG_010": 20510,
    "m10BIG_014": 20465,
    "m10BIG_015": 42012,
    "m11UGD_010": 26683,
    "m11UGD_015": 28764,
    "m11UGD_030": 31364,
    "m11UGD_038": 82010,
    "m11UGD_048": 20251,
    "m11UGD_049": 16469,
    "m11UGD_050": 20245,
    "m11UGD_051": 36920,
    "m12SND_003": 27037,
    "m12SND_024": 27307,
    "m12SND_026": 24599,
    "m13ARC_006": 80678,
    "m14TAR_002": 32608,
    "m14TAR_006": 40071,
    "m15JPN_005": 30828,
    "m15JPN_017": 35501,
    "m15JPN_018": 20245,
    "m17RVA_004": 20212,
    "m17RVA_007": 21332,
    "m17RVA_015": 20508,
    "m51EBT_000": 46738,
    "m88BKR_001": 44461,
    "m88BKR_002": 31679,
    "m88BKR_003": 37387,
    "m88BKR_004": 27103,
}
length_to_char = {
    "18": ",",
    "21": "/",
    "22": "0",
    "23": "1",
    "24": "2",
    "25": "3",
    "26": "4",
    "27": "5",
    "31": "9",
}
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
log = []

with open("Data\\BloodlessAbilityData\\BloodlessAbility.json", "r") as file_reader:
    ability = json.load(file_reader)

with open("Data\\BloodlessAbilityData\\BloodlessUpgrade.json", "r") as file_reader:
    upgrade = json.load(file_reader)

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
        if i == "BLD_ABILITY_HIGH_JUMP":
            entry["Value"]["RoomId"] = highjump_location
        elif i == "BLD_ABILITY_WATER_PROTECT":
            entry["Value"]["RoomId"] = waterprotect_location
        elif i == "BLD_ABILITY_BLOOD_STEAL":
            entry["Value"]["RoomId"] = bloodsteal_location
        else:
            entry["Value"]["RoomId"] = any_pick(ability_room)
        log.append(entry)
    
    for i in upgrade_type:
        entry = {}
        entry["Key"] = i
        entry["Value"] = {}
        entry["Value"]["RoomId"] = any_pick(upgrade_room)
        log.append(entry)

def any_pick(item_array):
    item = random.choice(item_array)
    if item in ability_room:
        ability_room.remove(item)
    if item in upgrade_room:
        upgrade_room.remove(item)
    return item

def write_patched_gimmick():
    offset = 0
    new_length = 0
    old_length = 0
    new_length_tower = 0
    old_length_tower = 0
    tower_check = 0
    for i in log:
        file_name = i["Value"]["RoomId"].replace(")", "").split("(")[0] + "_Gimmick.umap"
        
        #TowerCheck
        
        if "m08TWR_019" in file_name:
            tower_check += 1
            if tower_check == 1:
                folder_name = "OffSetter\\Umap\\"
                input_suffix = ""
                output_suffix = ".temp"
            elif tower_check == 2:
                folder_name = "OffSetter\\"
                input_suffix = ".temp"
                output_suffix = ""
        else:
            folder_name = "OffSetter\\Umap\\"
            input_suffix = ""
            output_suffix = ""
        
        #ChangingAbilityId
        
        with open(folder_name + file_name + input_suffix, "rb") as inputfile, open("OffSetter\\" + file_name + output_suffix, "wb") as outfile:
            offset = inputfile.read().find(str.encode("EPBBloodlessAbilityType::")) + 25
            if i["Value"]["RoomId"] == "m08TWR_019(2)":
                inputfile.seek(offset + 1)
                offset += inputfile.read().find(str.encode("EPBBloodlessAbilityType::")) + 25 + 1
            
            inputfile.seek(0)
            outfile.write(inputfile.read(offset))
            outfile.write(str.encode(i["Key"].replace(")", "").split("(")[0]))
            
            old_length = inputfile.read().find((0).to_bytes(1, "big"))
            if "m08TWR_019" in file_name and tower_check == 1:
                old_length_tower = old_length
            inputfile.seek(offset + old_length)
            outfile.write(inputfile.read())
        
        #PatchingNums
        
        with open("OffSetter\\" + file_name + output_suffix, "r+b") as file:
            file.seek(offset - 29)
            new_length = len(i["Key"].replace(")", "").split("(")[0])
            if "m08TWR_019" in file_name and tower_check == 1:
                new_length_tower = new_length
            file.write(str.encode(length_to_char[str(new_length)]))
            
            if "m08TWR_019" in file_name and tower_check == 2:
                file.seek(candle_to_offset[i["Value"]["RoomId"]] + (new_length_tower - old_length_tower) + (new_length - old_length) + 12)
            else:
                file.seek(candle_to_offset[i["Value"]["RoomId"]] + (new_length - old_length) + 12)
            if len(i["Key"].replace(")", "").split("(")) == 1:
                file.write((0).to_bytes(1, "big"))
            else:
                file.write(int(i["Key"].replace(")", "").split("(")[1]).to_bytes(1, "big"))
        
        #OffsetFix
        
        if "m08TWR_019" in file_name and tower_check == 2:
            root = os.getcwd()
            os.chdir("OffSetter")
            os.system("cmd /c OffSetter.exe " + file_name + " -n -r -m " + str((new_length_tower - old_length_tower) + (new_length - old_length)) + " 0")
            os.chdir(root)
            shutil.move("OffSetter\\" + file_name, "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name)
            os.remove("OffSetter\\" + file_name + ".offset")
        elif not "m08TWR_019" in file_name:
            root = os.getcwd()
            os.chdir("OffSetter")
            os.system("cmd /c OffSetter.exe " + file_name + " -n -r -m " + str(new_length - old_length) + " 0")
            os.chdir(root)
            shutil.move("OffSetter\\" + file_name, "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name)
            os.remove("OffSetter\\" + file_name + ".offset")

def write_gimmick_log():
    with open("SpoilerLog\\Bloodless.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))