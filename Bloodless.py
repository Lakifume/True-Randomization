import Manager
import random
import os

def init():
    #Declare variables
    global ability_to_room
    ability_to_room = {
        "BLD_ABILITY_HIGH_JUMP":           "m12SND_026",
        "BLD_ABILITY_WATER_PROTECT":       "m11UGD_015",
        "BLD_ABILITY_BLOOD_STEAL":         "m08TWR_019",
        "BLD_ABILITY_SOUL_STEAL":          "m14TAR_002",
        "BLD_ABILITY_FLOATING_UP":         "m01SIP_000",
        "BLD_ABILITY_UMBRELLA_CHARGE":     "m05SAN_011",
        "BLD_ABILITY_GUILLOTINE_UMBRELLA": "m02VIL_004",
        "BLD_ABILITY_UMBRELLA_TOSS":       "m07LIB_030",
        "BLD_ABILITY_SCARLET_THRUST":      "m05SAN_016",
        "BLD_ABILITY_SCARLET_THRUST_3":    "m51EBT_000",
        "BLD_ABILITY_BLOOD_PILLAR":        "m11UGD_048",
        "BLD_ABILITY_BLOOD_PILLAR_3":      "m17RVA_007",
        "BLD_ABILITY_SCARLET_CYCLONE":     "m13ARC_006",
        "BLD_ABILITY_BLOOD_RAIN":          "m15JPN_005"
    }
    global upgrade_to_room
    upgrade_to_room = {
        "BLD_ABILITY_STR_UP_2":      "m07LIB_042",
        "BLD_ABILITY_STR_UP_3":      "m11UGD_050",
        "BLD_ABILITY_STR_UP_4":      "m03ENT_024",
        "BLD_ABILITY_STR_UP_5":      "m17RVA_015",
        "BLD_ABILITY_STR_UP_6":      "m01SIP_007",
        "BLD_ABILITY_STR_UP_7":      "m05SAN_021",
        "BLD_ABILITY_STR_UP_8":      "m88BKR_001",
        "BLD_ABILITY_STR_UP_9":      "m10BIG_015",
        "BLD_ABILITY_INT_UP_2":      "m05SAN_006",
        "BLD_ABILITY_INT_UP_3":      "m11UGD_030",
        "BLD_ABILITY_INT_UP_4":      "m08TWR_019_2",
        "BLD_ABILITY_INT_UP_5":      "m14TAR_006",
        "BLD_ABILITY_INT_UP_6":      "m07LIB_009",
        "BLD_ABILITY_INT_UP_7":      "m11UGD_051",
        "BLD_ABILITY_INT_UP_8":      "m88BKR_004",
        "BLD_ABILITY_INT_UP_9":      "m10BIG_014",
        "BLD_ABILITY_CON_UP_2":      "m05SAN_014",
        "BLD_ABILITY_CON_UP_3":      "m06KNG_022",
        "BLD_ABILITY_CON_UP_4":      "m04GDN_004",
        "BLD_ABILITY_CON_UP_5":      "m17RVA_004",
        "BLD_ABILITY_CON_UP_6":      "m15JPN_017",
        "BLD_ABILITY_CON_UP_7":      "m01SIP_026",
        "BLD_ABILITY_CON_UP_8":      "m07LIB_040",
        "BLD_ABILITY_CON_UP_9":      "m10BIG_002",
        "BLD_ABILITY_MND_UP_2":      "m02VIL_005",
        "BLD_ABILITY_MND_UP_3":      "m07LIB_041",
        "BLD_ABILITY_MND_UP_4":      "m15JPN_018",
        "BLD_ABILITY_MND_UP_5":      "m12SND_003",
        "BLD_ABILITY_MND_UP_6":      "m11UGD_010",
        "BLD_ABILITY_MND_UP_7":      "m05SAN_003",
        "BLD_ABILITY_MND_UP_8":      "m88BKR_003",
        "BLD_ABILITY_MND_UP_9":      "m10BIG_010",
        "BLD_ABILITY_LCK_UP_2":      "m11UGD_049",
        "BLD_ABILITY_LCK_UP_3":      "m88BKR_002",
        "BLD_ABILITY_LCK_UP_4":      "m11UGD_038",
        "BLD_ABILITY_MP_REGEN_UP_2": "m07LIB_012",
        "BLD_ABILITY_MP_REGEN_UP_3": "m08TWR_018",
        "BLD_ABILITY_MP_REGEN_UP_4": "m12SND_024"
    }
    global portal_ban
    portal_ban = [
        "m10BIG_002",
        "m10BIG_010",
        "m10BIG_014",
        "m10BIG_015"
    ]
    global highjump_ban
    highjump_ban = [
        "m03ENT_024",
        "m05SAN_003",
        "m05SAN_021",
        "m08TWR_019_2",
        "m15JPN_005",
        "m15JPN_017",
        "m15JPN_018",
        "m88BKR_004"
    ]
    global waterprotect_ban
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
    global bloodsteal_ban
    bloodsteal_ban = [
        "m11UGD_015",
        "m11UGD_030",
        "m11UGD_038"
    ]
    global ability_room
    ability_room = []
    global ability_type
    ability_type = []
    global upgrade_room
    upgrade_room = []
    global upgrade_type
    upgrade_type = []
    global bloodless_datatable
    bloodless_datatable = {}
    #Process variables
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

def chaos_candle():
    #If full rando is chosen mix up abilities and uprades
    for i in ability_to_room:
        upgrade_room.append(ability_to_room[i])
    for i in upgrade_to_room:
        ability_room.append(upgrade_to_room[i])

def candle_shuffle():
    #The logic for Bloodless mode only revolves around 3 abilities
    #Extended float time is almost required but due to the new platforms in waterfall room it can be skipped
    #Not worth going through a complex logic like for Miriam so quickly set one up here
    
    #High Jump
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
    
    #Since there is no datatable for Bloodless ability drops create one here
    for i in ability_type:
        if i == "BLD_ABILITY_HIGH_JUMP":
            bloodless_datatable[i] = highjump_location
        elif i == "BLD_ABILITY_WATER_PROTECT":
            bloodless_datatable[i] = waterprotect_location
        elif i == "BLD_ABILITY_BLOOD_STEAL":
            bloodless_datatable[i] = bloodsteal_location
        else:
            bloodless_datatable[i] = any_pick(ability_room)
    
    for i in upgrade_type:
        bloodless_datatable[i] = any_pick(upgrade_room)

def any_pick(item_array):
    item = random.choice(item_array)
    if item in ability_room:
        ability_room.remove(item)
    if item in upgrade_room:
        upgrade_room.remove(item)
    return item

def get_datatable():
    return bloodless_datatable

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    name, extension = os.path.splitext(map)
    log = {}
    log["Seed"] = seed
    log["Map"]  = name.split("\\")[-1]
    log["Key"]  = {}
    for i in bloodless_datatable:
        log["Key"][Manager.dictionary["BloodlessTranslation"][Manager.remove_inst(i)]] = []
    for i in bloodless_datatable:
        log["Key"][Manager.dictionary["BloodlessTranslation"][Manager.remove_inst(i)]].append(Manager.remove_inst(bloodless_datatable[i]))
    return log

def create_log_string(seed, map):
    #Log string for quickly showing answer to a seed
    name, extension = os.path.splitext(map)
    if name.split("\\")[-1]:
        map_name = name.split("\\")[-1]
    else:
        map_name = "Default"
    log_string = ""
    log_string += "Seed: " + str(seed) + "\n"
    log_string += "Map: " + map_name + "\n"
    log_string += "Key:\n"
    for i in bloodless_datatable:
        if i in upgrade_type:
            break
        log_string += "  " + Manager.dictionary["BloodlessTranslation"][Manager.remove_inst(i)] + ": " + Manager.remove_inst(bloodless_datatable[i]) + "\n"
    return log_string