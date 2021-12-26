import ClassManagement
import random

ability_to_room = {
    "BLD_ABILITY_HIGH_JUMP(0)":           "m12SND_026",
    "BLD_ABILITY_WATER_PROTECT(0)":       "m11UGD_015",
    "BLD_ABILITY_BLOOD_STEAL(0)":         "m08TWR_019",
    "BLD_ABILITY_SOUL_STEAL(0)":          "m14TAR_002",
    "BLD_ABILITY_FLOATING_UP(0)":         "m01SIP_000",
    "BLD_ABILITY_UMBRELLA_CHARGE(0)":     "m05SAN_011",
    "BLD_ABILITY_GUILLOTINE_UMBRELLA(0)": "m02VIL_004",
    "BLD_ABILITY_UMBRELLA_TOSS(0)":       "m07LIB_030",
    "BLD_ABILITY_SCARLET_THRUST(0)":      "m05SAN_016",
    "BLD_ABILITY_SCARLET_THRUST(3)":      "m51EBT_000",
    "BLD_ABILITY_BLOOD_PILLAR(0)":        "m11UGD_048",
    "BLD_ABILITY_BLOOD_PILLAR(3)":        "m17RVA_007",
    "BLD_ABILITY_SCARLET_CYCLONE(0)":     "m13ARC_006",
    "BLD_ABILITY_BLOOD_RAIN(0)":          "m15JPN_005"
}
upgrade_to_room = {
    "BLD_ABILITY_STR_UP(2)":      "m07LIB_042",
    "BLD_ABILITY_STR_UP(3)":      "m11UGD_050",
    "BLD_ABILITY_STR_UP(4)":      "m03ENT_024",
    "BLD_ABILITY_STR_UP(5)":      "m17RVA_015",
    "BLD_ABILITY_STR_UP(6)":      "m01SIP_007",
    "BLD_ABILITY_STR_UP(7)":      "m05SAN_021",
    "BLD_ABILITY_STR_UP(8)":      "m88BKR_001",
    "BLD_ABILITY_STR_UP(9)":      "m10BIG_015",
    "BLD_ABILITY_INT_UP(2)":      "m05SAN_006",
    "BLD_ABILITY_INT_UP(3)":      "m11UGD_030",
    "BLD_ABILITY_INT_UP(4)":      "m08TWR_019(2)",
    "BLD_ABILITY_INT_UP(5)":      "m14TAR_006",
    "BLD_ABILITY_INT_UP(6)":      "m07LIB_009",
    "BLD_ABILITY_INT_UP(7)":      "m11UGD_051",
    "BLD_ABILITY_INT_UP(8)":      "m88BKR_004",
    "BLD_ABILITY_INT_UP(9)":      "m10BIG_014",
    "BLD_ABILITY_CON_UP(2)":      "m05SAN_014",
    "BLD_ABILITY_CON_UP(3)":      "m06KNG_022",
    "BLD_ABILITY_CON_UP(4)":      "m04GDN_004",
    "BLD_ABILITY_CON_UP(5)":      "m17RVA_004",
    "BLD_ABILITY_CON_UP(6)":      "m15JPN_017",
    "BLD_ABILITY_CON_UP(7)":      "m01SIP_026",
    "BLD_ABILITY_CON_UP(8)":      "m07LIB_040",
    "BLD_ABILITY_CON_UP(9)":      "m10BIG_002",
    "BLD_ABILITY_MND_UP(2)":      "m02VIL_005",
    "BLD_ABILITY_MND_UP(3)":      "m07LIB_041",
    "BLD_ABILITY_MND_UP(4)":      "m15JPN_018",
    "BLD_ABILITY_MND_UP(5)":      "m12SND_003",
    "BLD_ABILITY_MND_UP(6)":      "m11UGD_010",
    "BLD_ABILITY_MND_UP(7)":      "m05SAN_003",
    "BLD_ABILITY_MND_UP(8)":      "m88BKR_003",
    "BLD_ABILITY_MND_UP(9)":      "m10BIG_010",
    "BLD_ABILITY_LCK_UP(2)":      "m11UGD_049",
    "BLD_ABILITY_LCK_UP(3)":      "m88BKR_002",
    "BLD_ABILITY_LCK_UP(4)":      "m11UGD_038",
    "BLD_ABILITY_MP_REGEN_UP(2)": "m07LIB_012",
    "BLD_ABILITY_MP_REGEN_UP(3)": "m08TWR_018",
    "BLD_ABILITY_MP_REGEN_UP(4)": "m12SND_024"
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
json_placeholder = {}
log = {}
    
def init():
    for i in ability_to_room:
        ability_type.append(i)
        ability_room.append(ability_to_room[i])
    for i in upgrade_to_room:
        upgrade_type.append(i)
        upgrade_room.append(upgrade_to_room[i])
    for i in portal_ban:
        highjump_ban.append(i)
    for i in portal_ban:
        waterprotect_ban.append(i)
    for i in waterprotect_ban:
        bloodsteal_ban.append(i)
    ClassManagement.debug("ClassBloodless.init()")

def chaos_candle():
    for i in ability_to_room:
        upgrade_room.append(ability_to_room[i])
    for i in upgrade_to_room:
        ability_room.append(upgrade_to_room[i])
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
        if i == "BLD_ABILITY_HIGH_JUMP(0)":
            json_placeholder[i] = highjump_location
        elif i == "BLD_ABILITY_WATER_PROTECT(0)":
            json_placeholder[i] = waterprotect_location
        elif i == "BLD_ABILITY_BLOOD_STEAL(0)":
            json_placeholder[i] = bloodsteal_location
        else:
            json_placeholder[i] = any_pick(ability_room)
    
    for i in upgrade_type:
        json_placeholder[i] = any_pick(upgrade_room)
    
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
        log[ClassManagement.bloodless_translation[i.replace(")", "").split("(")[0]]] = []
    for i in json_placeholder:
        log[ClassManagement.bloodless_translation[i.replace(")", "").split("(")[0]]].append(json_placeholder[i].replace(")", "").split("(")[0])
    for i in log:
        log[i].sort()
    ClassManagement.debug("ClassBloodless.create_log()")

def get_log():
    return log