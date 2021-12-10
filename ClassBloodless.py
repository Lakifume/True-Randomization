import ClassManagement
import random

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
    
def init():
    for i in ClassManagement.bloodless_ability_data:
        ability_type.append(i["Key"])
        ability_room.append(i["Value"]["RoomId"])
    
    for i in ClassManagement.bloodless_upgrade_data:
        upgrade_type.append(i["Key"])
        upgrade_room.append(i["Value"]["RoomId"])
    
    for i in portal_ban:
        highjump_ban.append(i)
    
    for i in portal_ban:
        waterprotect_ban.append(i)
    
    for i in waterprotect_ban:
        bloodsteal_ban.append(i)
    ClassManagement.debug("ClassBloodless.init()")

def chaos_candle():
    for i in ClassManagement.bloodless_ability_data:
        upgrade_room.append(i["Value"]["RoomId"])
    for i in ClassManagement.bloodless_upgrade_data:
        ability_room.append(i["Value"]["RoomId"])
    ClassManagement.debug("ClassBloodless.chaos_candle()")

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
    
    ClassManagement.debug("ClassBloodless.candle_shuffle()")

def any_pick(item_array):
    item = random.choice(item_array)
    if item in ability_room:
        ability_room.remove(item)
    if item in upgrade_room:
        upgrade_room.remove(item)
    return item

def get_datatable():
    return json_placeholder

def create_log():
    candle_type = []
    for i in json_placeholder:
        if not i["Key"].replace(")", "").split("(")[0] in candle_type:
            candle_type.append(i["Key"].replace(")", "").split("(")[0])
    for i in candle_type:
        log_data = {}
        log_data["Key"] = ClassManagement.bloodless_translation["Value"][i]
        log_data["Value"] = {}
        log_data["Value"]["RoomList"] = []
        log.append(log_data)
    for i in json_placeholder:
        for e in log:
            if e["Key"] == ClassManagement.bloodless_translation["Value"][i["Key"].replace(")", "").split("(")[0]]:
                e["Value"]["RoomList"].append(i["Value"]["RoomId"].replace(")", "").split("(")[0])
    for i in log:
        i["Value"]["RoomList"].sort()
    ClassManagement.debug("ClassBloodless.create_log()")

def get_log():
    return log