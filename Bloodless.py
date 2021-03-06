import Manager
import random
import os
import copy

def init():
    #Declare variables
    global candle_to_room
    candle_to_room = {
        "BLD_ABILITY_HIGH_JUMP":           "m12SND_026",
        "BLD_ABILITY_WATER_PROTECT":       "m11UGD_015",
        "BLD_ABILITY_BLOOD_STEAL":         "m08TWR_019",
        "BLD_ABILITY_SOUL_STEAL":          "m14TAR_002",
        "BLD_ABILITY_FLOATING_UP":         "m01SIP_000",
        "BLD_ABILITY_UMBRELLA_CHARGE":     "m05SAN_011",
        "BLD_ABILITY_GUILLOTINE_UMBRELLA": "m02VIL_004",
        "BLD_ABILITY_UMBRELLA_TOSS":       "m07LIB_030",
        "BLD_ABILITY_SCARLET_THRUST":      "m05SAN_016",
        "BLD_ABILITY_SCARLET_THRUST(2)":   "m51EBT_000",
        "BLD_ABILITY_BLOOD_PILLAR":        "m11UGD_048",
        "BLD_ABILITY_BLOOD_PILLAR(2)":     "m17RVA_007",
        "BLD_ABILITY_SCARLET_CYCLONE":     "m13ARC_006",
        "BLD_ABILITY_BLOOD_RAIN":          "m15JPN_005",
        "BLD_ABILITY_STR_UP(1)":           "m07LIB_042",
        "BLD_ABILITY_STR_UP(2)":           "m11UGD_050",
        "BLD_ABILITY_STR_UP(3)":           "m03ENT_024",
        "BLD_ABILITY_STR_UP(4)":           "m17RVA_015",
        "BLD_ABILITY_STR_UP(5)":           "m01SIP_007",
        "BLD_ABILITY_STR_UP(6)":           "m05SAN_021",
        "BLD_ABILITY_STR_UP(7)":           "m88BKR_001",
        "BLD_ABILITY_STR_UP(8)":           "m10BIG_015",
        "BLD_ABILITY_INT_UP(1)":           "m05SAN_006",
        "BLD_ABILITY_INT_UP(2)":           "m11UGD_030",
        "BLD_ABILITY_INT_UP(3)":           "m08TWR_019(1)",
        "BLD_ABILITY_INT_UP(4)":           "m14TAR_006",
        "BLD_ABILITY_INT_UP(5)":           "m07LIB_009",
        "BLD_ABILITY_INT_UP(6)":           "m11UGD_051",
        "BLD_ABILITY_INT_UP(7)":           "m88BKR_004",
        "BLD_ABILITY_INT_UP(8)":           "m10BIG_014",
        "BLD_ABILITY_CON_UP(1)":           "m05SAN_014",
        "BLD_ABILITY_CON_UP(2)":           "m06KNG_022",
        "BLD_ABILITY_CON_UP(3)":           "m04GDN_004",
        "BLD_ABILITY_CON_UP(4)":           "m17RVA_004",
        "BLD_ABILITY_CON_UP(5)":           "m15JPN_017",
        "BLD_ABILITY_CON_UP(6)":           "m01SIP_026",
        "BLD_ABILITY_CON_UP(7)":           "m07LIB_040",
        "BLD_ABILITY_CON_UP(8)":           "m10BIG_002",
        "BLD_ABILITY_MND_UP(1)":           "m02VIL_005",
        "BLD_ABILITY_MND_UP(2)":           "m07LIB_041",
        "BLD_ABILITY_MND_UP(3)":           "m15JPN_018",
        "BLD_ABILITY_MND_UP(4)":           "m12SND_003",
        "BLD_ABILITY_MND_UP(5)":           "m11UGD_010",
        "BLD_ABILITY_MND_UP(6)":           "m05SAN_003",
        "BLD_ABILITY_MND_UP(7)":           "m88BKR_003",
        "BLD_ABILITY_MND_UP(8)":           "m10BIG_010",
        "BLD_ABILITY_LCK_UP(1)":           "m11UGD_049",
        "BLD_ABILITY_LCK_UP(2)":           "m88BKR_002",
        "BLD_ABILITY_LCK_UP(3)":           "m11UGD_038",
        "BLD_ABILITY_MP_REGEN_UP(1)":      "m07LIB_012",
        "BLD_ABILITY_MP_REGEN_UP(2)":      "m08TWR_018",
        "BLD_ABILITY_MP_REGEN_UP(3)":      "m12SND_024"
    }
    global candle_to_room_invert
    candle_to_room_invert = {}
    global bloodless_to_miriam
    bloodless_to_miriam = {
        "BLD_ABILITY_HIGH_JUMP":     "HighJump",  
        "BLD_ABILITY_WATER_PROTECT": "Deepsinker",
        "BLD_ABILITY_BLOOD_STEAL":   "Bloodsteel",
        "BLD_ABILITY_FLOATING_UP":   "Demoniccapture",
    }
    global irrelevant_gates
    irrelevant_gates = {
        "m05SAN_003": [12, 4],
        "m07LIB_022": [2, 1],
        "m07LIB_023": [5, 5],
        "m07LIB_044": [6, 4],
        "m11UGD_003": [8, 4, 13, 1, 14, 4]
    }
    global impossible_gates
    impossible_gates = {
        "m05SAN_003": [17, 1],
        "m07LIB_008": [2, 4],
        "m07LIB_014": [1, 4],
        "m11UGD_056": [4, 4],
        "m10BIG_000": []
    }
    global all_keys
    all_keys = []
    global key_order
    key_order = []
    global key_abilities
    key_abilities = []
    global key_ability_to_location
    key_ability_to_location = {}
    global candle_type
    candle_type = []
    global candle_room
    candle_room = []
    global bloodless_datatable
    bloodless_datatable = {}
    #Process variables
    for i in list(bloodless_to_miriam):
        key_abilities.append(i)
        all_keys.append(i)
    for i in candle_to_room:
        candle_type.append(i)
        candle_room.append(candle_to_room[i])
    for i in candle_to_room:
        candle_to_room_invert[candle_to_room[i]] = i

def extra_logic():
    #Update the logic to reflect the new starting point
    room_to_list = {}
    gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"]["m05SAN_023"]["NearestGate"])
    previous_gate = []
    current_gate = []
    #Start by emptying gate lists in the upper cathedral rooms
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        if Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"] == gate_list:
            room_to_list[i] = current_gate
    #Then move backwards toward the first galleon room to inverse the logic
    while gate_list:
        for i in Manager.mod_data["BloodlessModeMapLogic"]:
            if i in gate_list:
                current_gate.append(i)
        for i in current_gate:
            room_to_list[i] = []
            for e in previous_gate:
                if i in Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"]:
                    room_to_list[i].append(e)
        for i in Manager.mod_data["BloodlessModeMapLogic"]:
            for e in current_gate:
                if Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"] == Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"] and i != e:
                    room_to_list[i] = []
            for e in current_gate:
                if Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"] == Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"] and i != e:
                    room_to_list[i].append(e)
        previous_gate = copy.deepcopy(current_gate)
        current_gate.clear()
        gate_list.clear()
        for i in previous_gate:
            gate_list.extend(Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"])
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        if i in room_to_list:
            Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"] = room_to_list[i]
    #Convert doors to their actual gates
    irrelevant_list = []
    for i in irrelevant_gates:
        irrelevant_list.extend(Manager.convert_door_to_adjacent_room(i, irrelevant_gates[i]))
    impossible_list = []
    for i in impossible_gates:
        impossible_list.extend(Manager.convert_door_to_adjacent_room(i, impossible_gates[i]))
    #Add 8 Bit Nightmare
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"] = {}
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["GateRoom"]             = False
    if Manager.mod_data["BloodlessModeMapLogic"]["m06KNG_021"]["GateRoom"]:
        Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["NearestGate"]      = ["m06KNG_021"]
    else:
        Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"]["m06KNG_021"]["NearestGate"])
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Doublejump"]           = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["HighJump"]             = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Invert"]               = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Deepsinker"]           = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Dimensionshift"]       = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Reflectionray"]        = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Aquastream"]           = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Bloodsteel"]           = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Swordsman"]            = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Silverbromide"]        = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Keyofbacker1"]         = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Keyofbacker2"]         = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Keyofbacker3"]         = False
    Manager.mod_data["BloodlessModeMapLogic"]["m51EBT_000"]["Keyofbacker4"]         = False
    #Emulate a Craftwork requirement in the garden bridge for the extended float ability
    #Normally Craftwork isn't in logic as that shard can't be moved
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        Manager.mod_data["BloodlessModeMapLogic"][i]["Demoniccapture"] = False
    Manager.mod_data["BloodlessModeMapLogic"]["m04GDN_006"]["Demoniccapture"] = True
    Manager.mod_data["BloodlessModeMapLogic"]["m04GDN_006"]["HighJump"] = True
    #Remove gates that don't matter in Bloodless mode
    #That includes the rooms that had platforms added
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        if i in impossible_list:
            continue
        check = True
        for e in key_abilities:
            if Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] and Manager.mod_data["BloodlessModeMapLogic"][i][bloodless_to_miriam[e]]:
                check = False
        if check or i in irrelevant_list or Manager.mod_data["BloodlessModeMapLogic"][i]["Doublejump"]:
            Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] = False
            for e in Manager.mod_data["BloodlessModeMapLogic"]:
                if i in Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"]:
                    Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"] = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"])
    #Adding seperate gate for the upper part of Valac's room
    Manager.mod_data["BloodlessModeMapLogic"]["m08TWR_019(1)"] = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"]["m08TWR_019"])
    Manager.mod_data["BloodlessModeMapLogic"]["m08TWR_019"]["GateRoom"] = False
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        while "m08TWR_019" in Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"]:
            index = Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"].index("m08TWR_019")
            Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"][index] = "m08TWR_019(1)"

def candle_logic():
    #Function similar to the Miriam logic but simplified for Bloodless mode
    previous_gate = []
    requirement_to_gate = {}
    #Filling list with all room names
    all_rooms = copy.deepcopy(candle_room)
    #Loop through all keys until they've all been assigned
    while all_keys:
        #Reset lists and dicts
        requirement = []
        for i in key_abilities:
            requirement_to_gate[i] = []
        previous_room = []
        #Gathering upcoming gate requirements
        for i in Manager.mod_data["BloodlessModeMapLogic"]:
            if Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"]) and not i in previous_gate:
                for e in key_abilities:
                    if Manager.mod_data["BloodlessModeMapLogic"][i][bloodless_to_miriam[e]]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
        #Check if requirement isnt already satisfied
        check = False
        for i in key_ability_to_location:
            if i in requirement:
                check = True
                previous_gate.extend(requirement_to_gate[i])
        if check:
            continue
        #Gathering rooms available before gate
        for i in Manager.mod_data["BloodlessModeMapLogic"]:
            #Skip if room doesn't have a candle
            if not i in candle_room:
                continue
            if not Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"]) or i in previous_gate:
                #Increasing chances of late rooms
                #Otherwise early game areas are more likely to have everything
                gate_count = 1
                gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"])
                while gate_list:
                    nearest_gate = random.choice(gate_list)
                    for e in Manager.mod_data["BloodlessModeMapLogic"]:
                        if e == nearest_gate:
                            gate_count += 1
                            gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"])
                            break
                #Making multplier more extreme with exponent
                gate_count = round(gate_count**1.5)
                for e in range(gate_count):
                    previous_room.append(i)
        #Choosing key item based on requirements
        chosen_item = random.choice(all_keys)
        if requirement:
            while chosen_item not in requirement:
                chosen_item = random.choice(all_keys)
            logic_choice(chosen_item, previous_room)
        else:
            logic_choice(chosen_item, all_rooms)
        #Update previous gate
        previous_gate.extend(requirement_to_gate[chosen_item])

def previous_in_nearest(previous_gate, nearest_gate):
    if not nearest_gate:
        return True
    else:
        for i in previous_gate:
            if i in nearest_gate:
                return True
    return False

def logic_choice(chosen_item, room_list):
    #Removing key from list
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)
    #Choosing room to place item in
    chosen_room = random.choice(room_list)
    while chosen_room in list(key_ability_to_location.values()):
        chosen_room = random.choice(room_list)
    #Updating key location
    key_ability_to_location[chosen_item] = chosen_room

def candle_shuffle():
    candle_logic()
    #Key abilities
    for i in key_abilities:
        bloodless_datatable[i] = key_ability_to_location[i]
        candle_room.remove(key_ability_to_location[i])
    #Since there is no datatable for Bloodless ability drops create one here
    for i in candle_type:
        if i in key_abilities:
            continue
        chosen_room = any_pick(candle_room)
        bloodless_datatable[i] = chosen_room

def update_shard_candles():
    #All of Bloodless' abilities are stored inside of shard candles
    #Just like for Miriam those are defined inside of the level files
    for i in bloodless_datatable:
        Manager.search_and_replace_string(Manager.split_fname(bloodless_datatable[i])[0] + "_Gimmick", "BloodlessAbilityGimmick", "UnlockAbilityType", "EPBBloodlessAbilityType::" + candle_to_room_invert[bloodless_datatable[i]], "EPBBloodlessAbilityType::" + i)

def any_pick(item_array):
    item = random.choice(item_array)
    item_array.remove(item)
    return item

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    name, extension = os.path.splitext(map)
    log = {}
    log["Seed"] = seed
    log["Map"]  = name.split("\\")[-1]
    log["Key"]  = {}
    for i in key_order:
        log["Key"][Manager.mod_data["BloodlessTranslation"][Manager.split_fname(i)[0]]] = []
    for i in bloodless_datatable:
        log["Key"][Manager.mod_data["BloodlessTranslation"][Manager.split_fname(i)[0]]] = []
    for i in bloodless_datatable:
        log["Key"][Manager.mod_data["BloodlessTranslation"][Manager.split_fname(i)[0]]].append(Manager.split_fname(bloodless_datatable[i])[0])
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
    for i in key_order:
        log_string += "  " + Manager.mod_data["BloodlessTranslation"][Manager.split_fname(i)[0]] + ": " + bloodless_datatable[i] + "\n"
    for i in bloodless_datatable:
        if i in key_order:
            continue
        if "_UP(" in i:
            break
        log_string += "  " + Manager.mod_data["BloodlessTranslation"][Manager.split_fname(i)[0]] + ": " + bloodless_datatable[i] + "\n"
    return log_string