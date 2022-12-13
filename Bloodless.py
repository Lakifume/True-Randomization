import Manager
import random
import os
import copy

def init():
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
        "BLD_ABILITY_SCARLET_THRUST_2":    "m51EBT_000",
        "BLD_ABILITY_BLOOD_PILLAR":        "m11UGD_048",
        "BLD_ABILITY_BLOOD_PILLAR_2":      "m17RVA_007",
        "BLD_ABILITY_SCARLET_CYCLONE":     "m13ARC_006",
        "BLD_ABILITY_BLOOD_RAIN":          "m15JPN_005",
        "BLD_ABILITY_STR_UP_1":            "m07LIB_042",
        "BLD_ABILITY_STR_UP_2":            "m11UGD_050",
        "BLD_ABILITY_STR_UP_3":            "m03ENT_024",
        "BLD_ABILITY_STR_UP_4":            "m17RVA_015",
        "BLD_ABILITY_STR_UP_5":            "m01SIP_007",
        "BLD_ABILITY_STR_UP_6":            "m05SAN_021",
        "BLD_ABILITY_STR_UP_7":            "m88BKR_001",
        "BLD_ABILITY_STR_UP_8":            "m10BIG_015",
        "BLD_ABILITY_INT_UP_1":            "m05SAN_006",
        "BLD_ABILITY_INT_UP_2":            "m11UGD_030",
        "BLD_ABILITY_INT_UP_3":            "m08TWR_019_1",
        "BLD_ABILITY_INT_UP_4":            "m14TAR_006",
        "BLD_ABILITY_INT_UP_5":            "m07LIB_009",
        "BLD_ABILITY_INT_UP_6":            "m11UGD_051",
        "BLD_ABILITY_INT_UP_7":            "m88BKR_004",
        "BLD_ABILITY_INT_UP_8":            "m10BIG_014",
        "BLD_ABILITY_CON_UP_1":            "m05SAN_014",
        "BLD_ABILITY_CON_UP_2":            "m06KNG_022",
        "BLD_ABILITY_CON_UP_3":            "m04GDN_004",
        "BLD_ABILITY_CON_UP_4":            "m17RVA_004",
        "BLD_ABILITY_CON_UP_5":            "m15JPN_017",
        "BLD_ABILITY_CON_UP_6":            "m01SIP_026",
        "BLD_ABILITY_CON_UP_7":            "m07LIB_040",
        "BLD_ABILITY_CON_UP_8":            "m10BIG_002",
        "BLD_ABILITY_MND_UP_1":            "m02VIL_005",
        "BLD_ABILITY_MND_UP_2":            "m07LIB_041",
        "BLD_ABILITY_MND_UP_3":            "m15JPN_018",
        "BLD_ABILITY_MND_UP_4":            "m12SND_003",
        "BLD_ABILITY_MND_UP_5":            "m11UGD_010",
        "BLD_ABILITY_MND_UP_6":            "m05SAN_003",
        "BLD_ABILITY_MND_UP_7":            "m88BKR_003",
        "BLD_ABILITY_MND_UP_8":            "m10BIG_010",
        "BLD_ABILITY_LCK_UP_1":            "m11UGD_049",
        "BLD_ABILITY_LCK_UP_2":            "m88BKR_002",
        "BLD_ABILITY_LCK_UP_3":            "m11UGD_038",
        "BLD_ABILITY_MP_REGEN_UP_1":       "m07LIB_012",
        "BLD_ABILITY_MP_REGEN_UP_2":       "m08TWR_018",
        "BLD_ABILITY_MP_REGEN_UP_3":       "m12SND_024"
    }
    global candle_to_room_invert
    candle_to_room_invert = {}
    global room_to_requirement
    room_to_requirement = {
        "m05SAN_021":   ["BLD_ABILITY_HIGH_JUMP"],
        "m08TWR_019_1": ["BLD_ABILITY_HIGH_JUMP"]
    }
    global bloodless_to_miriam
    bloodless_to_miriam = {
        "BLD_ABILITY_HIGH_JUMP":     "HighJump",  
        "BLD_ABILITY_WATER_PROTECT": "Deepsinker",
        "BLD_ABILITY_BLOOD_STEAL":   "Bloodsteel",
        "BLD_ABILITY_FLOATING_UP":   "Demoniccapture",
    }
    global irrelevant_doors
    irrelevant_doors = {
        "SAN_003_1_5_RIGHT",
        "LIB_022_0_1_LEFT",
        "LIB_023_0_4_LEFT",
        "LIB_023_0_4_RIGHT",
        "LIB_044_2_1_RIGHT",
        "UGD_003_1_3_RIGHT",
        "UGD_003_0_6_LEFT",
        "UGD_003_1_6_RIGHT"
    }
    global requirement_doors
    requirement_doors = [
        "SAN_003_0_8_LEFT",
        "UGD_056_0_3_LEFT",
        "UGD_056_0_3_RIGHT"
    ]
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
    for i in bloodless_to_miriam:
        key_abilities.append(i)
        all_keys.append(i)
    for i in candle_to_room:
        candle_type.append(i)
        candle_room.append(candle_to_room[i])
    for i in candle_to_room:
        candle_to_room_invert[candle_to_room[i]] = i

def extra_logic():
    Manager.mod_data["BloodlessModeMapLogic"] = copy.deepcopy(Manager.mod_data["MapLogic"])
    #Update the logic to reflect the new starting point
    room_to_list = {}
    gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"]["m05SAN_023"]["NearestGate"])
    previous_gate = []
    current_gate = []
    #Start by emptying gate lists in the upper cathedral rooms
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        if Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"] == gate_list:
            room_to_list[i] = current_gate
    #Then move backwards toward the first galleon room to invert the logic
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
    #Emulate a Craftwork requirement in the garden bridge for the extended float ability
    #Normally Craftwork isn't in logic as that shard can't be moved
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        Manager.mod_data["BloodlessModeMapLogic"][i]["Demoniccapture"] = False
    Manager.mod_data["BloodlessModeMapLogic"]["m04GDN_006"]["Demoniccapture"] = True
    Manager.mod_data["BloodlessModeMapLogic"]["m04GDN_006"]["HighJump"] = True
    #Convert doors to their actual gates
    irrelevant_gates = []
    for i in irrelevant_doors:
        irrelevant_gates.extend(Manager.convert_door_to_adjacent_room(i))
    requirement_gates = []
    for i in requirement_doors:
        requirement_gates.extend(Manager.convert_door_to_adjacent_room(i))
    #Since the missing tori warps were added for extra characters some gates act differently
    for i in requirement_gates:
        if i in Manager.mod_data["BloodlessModeMapLogic"]:
            Manager.mod_data["BloodlessModeMapLogic"][i]["HighJump"] = True
    #Remove gates that don't matter in Bloodless mode
    #That includes the rooms that had platforms added
    for i in Manager.mod_data["BloodlessModeMapLogic"]:
        if Manager.mod_data["BloodlessModeMapLogic"][i]["Swordsman"] or i in requirement_gates:
            continue
        check = True
        for e in key_abilities:
            if Manager.mod_data["BloodlessModeMapLogic"][i][bloodless_to_miriam[e]]:
                check = False
        if check or i in irrelevant_gates or Manager.mod_data["BloodlessModeMapLogic"][i]["Doublejump"]:
            Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] = False
            for e in Manager.mod_data["BloodlessModeMapLogic"]:
                if i in Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"]:
                    Manager.mod_data["BloodlessModeMapLogic"][e]["NearestGate"] = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"])
    #Adding seperate gate for the upper part of Valac's room
    Manager.mod_data["BloodlessModeMapLogic"]["m08TWR_019_1"] = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"]["m08TWR_019"])

def candle_logic():
    #Function similar to the Miriam logic but simplified for Bloodless mode
    previous_gate = []
    requirement_to_gate = {}
    #Filling list with all room names
    all_rooms = []
    for i in candle_room:
        ratio = room_to_ratio(i)
        for e in range(ratio):
            all_rooms.append(i)
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
        for i in candle_room:
            if not Manager.mod_data["BloodlessModeMapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"]) or i in previous_gate:
                #Get ratio
                ratio = room_to_ratio(i)
                for e in range(ratio):
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
    for i in previous_gate:
        if i in nearest_gate:
            return True
    return False

def room_to_ratio(room):
    #Increasing chances of late rooms
    #Otherwise early game areas are more likely to have everything
    ratio = 1
    gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][room]["NearestGate"])
    while gate_list:
        nearest_gate = random.choice(gate_list)
        for i in Manager.mod_data["BloodlessModeMapLogic"]:
            if i == nearest_gate:
                ratio *= 2
                gate_list = copy.deepcopy(Manager.mod_data["BloodlessModeMapLogic"][i]["NearestGate"])
                break
    return ratio

def logic_choice(chosen_item, room_list):
    #Removing key from list
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)
    #Choosing room to place item in
    while True:
        chosen_room = random.choice(room_list)
        if not chosen_room in list(key_ability_to_location.values()):
            if chosen_room in room_to_requirement:
                for i in room_to_requirement[chosen_room]:
                    if i in key_ability_to_location:
                        key_ability_to_location[chosen_item] = chosen_room
                        break
            else:
                key_ability_to_location[chosen_item] = chosen_room
                break

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
        Manager.search_and_replace_string(Manager.remove_inst(bloodless_datatable[i]) + "_Gimmick", "BP_DM_BloodlessAbilityGimmick_C", "UnlockAbilityType", "EPBBloodlessAbilityType::" + candle_to_room_invert[bloodless_datatable[i]], "EPBBloodlessAbilityType::" + i)

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
        log["Key"][Manager.translation["Bloodless"][Manager.remove_inst(i)]] = []
    for i in bloodless_datatable:
        log["Key"][Manager.translation["Bloodless"][Manager.remove_inst(i)]] = []
    for i in bloodless_datatable:
        log["Key"][Manager.translation["Bloodless"][Manager.remove_inst(i)]].append(Manager.remove_inst(bloodless_datatable[i]))
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
        log_string += "  " + Manager.translation["Bloodless"][Manager.remove_inst(i)] + ": " + bloodless_datatable[i] + "\n"
    for i in bloodless_datatable:
        if i in key_order:
            continue
        if "_UP_" in i:
            break
        log_string += "  " + Manager.translation["Bloodless"][Manager.remove_inst(i)] + ": " + bloodless_datatable[i] + "\n"
    return log_string