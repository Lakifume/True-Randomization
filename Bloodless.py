from System import *
import Item
import Room
import Utility

class CheckType(Enum):
    Door   = 0
    Candle = 1
    Boss   = 2

def init():
    global candle_to_ability
    candle_to_ability = {
        "Candle_SND026_1": "BLD_ABILITY_HIGH_JUMP",
        "Candle_UGD015_1": "BLD_ABILITY_WATER_PROTECT",
        "Candle_TWR019_1": "BLD_ABILITY_BLOOD_STEAL",
        "Candle_TAR002_1": "BLD_ABILITY_SOUL_STEAL",
        "Candle_SIP000_1": "BLD_ABILITY_FLOATING_UP",
        "Candle_SAN011_1": "BLD_ABILITY_UMBRELLA_CHARGE",
        "Candle_VIL004_1": "BLD_ABILITY_GUILLOTINE_UMBRELLA",
        "Candle_LIB030_1": "BLD_ABILITY_UMBRELLA_TOSS",
        "Candle_SAN016_1": "BLD_ABILITY_SCARLET_THRUST",
        "Candle_EBT000_1": "BLD_ABILITY_SCARLET_THRUST_2",
        "Candle_UGD048_1": "BLD_ABILITY_BLOOD_PILLAR",
        "Candle_RVA007_1": "BLD_ABILITY_BLOOD_PILLAR_2",
        "Candle_ARC006_1": "BLD_ABILITY_SCARLET_CYCLONE",
        "Candle_JPN005_1": "BLD_ABILITY_BLOOD_RAIN",
        "Candle_LIB042_1": "BLD_ABILITY_STR_UP_1",
        "Candle_UGD050_1": "BLD_ABILITY_STR_UP_2",
        "Candle_ENT024_1": "BLD_ABILITY_STR_UP_3",
        "Candle_RVA015_1": "BLD_ABILITY_STR_UP_4",
        "Candle_SIP007_1": "BLD_ABILITY_STR_UP_5",
        "Candle_SAN021_1": "BLD_ABILITY_STR_UP_6",
        "Candle_BKR001_1": "BLD_ABILITY_STR_UP_7",
        "Candle_BIG015_1": "BLD_ABILITY_STR_UP_8",
        "Candle_SAN006_1": "BLD_ABILITY_INT_UP_1",
        "Candle_UGD030_1": "BLD_ABILITY_INT_UP_2",
        "Candle_TWR019_2": "BLD_ABILITY_INT_UP_3",
        "Candle_TAR006_1": "BLD_ABILITY_INT_UP_4",
        "Candle_LIB009_1": "BLD_ABILITY_INT_UP_5",
        "Candle_UGD051_1": "BLD_ABILITY_INT_UP_6",
        "Candle_BKR004_1": "BLD_ABILITY_INT_UP_7",
        "Candle_BIG014_1": "BLD_ABILITY_INT_UP_8",
        "Candle_SAN014_1": "BLD_ABILITY_CON_UP_1",
        "Candle_KNG022_1": "BLD_ABILITY_CON_UP_2",
        "Candle_GDN004_1": "BLD_ABILITY_CON_UP_3",
        "Candle_RVA004_1": "BLD_ABILITY_CON_UP_4",
        "Candle_JPN017_1": "BLD_ABILITY_CON_UP_5",
        "Candle_SIP026_1": "BLD_ABILITY_CON_UP_6",
        "Candle_LIB040_1": "BLD_ABILITY_CON_UP_7",
        "Candle_BIG002_1": "BLD_ABILITY_CON_UP_8",
        "Candle_VIL005_1": "BLD_ABILITY_MND_UP_1",
        "Candle_LIB041_1": "BLD_ABILITY_MND_UP_2",
        "Candle_JPN018_1": "BLD_ABILITY_MND_UP_3",
        "Candle_SND003_1": "BLD_ABILITY_MND_UP_4",
        "Candle_UGD010_1": "BLD_ABILITY_MND_UP_5",
        "Candle_SAN003_1": "BLD_ABILITY_MND_UP_6",
        "Candle_BKR003_1": "BLD_ABILITY_MND_UP_7",
        "Candle_BIG010_1": "BLD_ABILITY_MND_UP_8",
        "Candle_UGD049_1": "BLD_ABILITY_LCK_UP_1",
        "Candle_BKR002_1": "BLD_ABILITY_LCK_UP_2",
        "Candle_UGD038_1": "BLD_ABILITY_LCK_UP_3",
        "Candle_LIB012_1": "BLD_ABILITY_MP_REGEN_UP_1",
        "Candle_TWR018_1": "BLD_ABILITY_MP_REGEN_UP_2",
        "Candle_SND024_1": "BLD_ABILITY_MP_REGEN_UP_3"
    }
    global boss_requirements
    boss_requirements = [
        "N1001",
        "N1011",
        "N1003",
        "N2004",
        "N1005",
        "N2001",
        "N1006",
        "N2008_BOSS",
        "N1012",
        "N2014",
        "N2007",
        "N2006",
        "N1011_STRONG"
    ]
    global key_abilities
    key_abilities = {
        "BLD_ABILITY_HIGH_JUMP":     1,
        "BLD_ABILITY_WATER_PROTECT": 1,
        "BLD_ABILITY_BLOOD_STEAL":   3,
        "BLD_ABILITY_FLOATING_UP":   3
    }
    global ability_to_location
    ability_to_location = {}
    global key_ability_to_location
    key_ability_to_location = {}
    global all_keys
    all_keys = list(key_abilities)
    global all_candles
    all_candles = list(candle_to_ability)
    global all_abilities
    all_abilities = list(candle_to_ability.values())
    #Logic
    global previous_available_candles
    previous_available_candles = []
    global current_available_doors
    current_available_doors = ["SAN_023_START"]
    global current_available_candles
    current_available_candles = []
    global current_available_bosses
    current_available_bosses = []
    global all_available_doors
    all_available_doors = []
    global all_available_candles
    all_available_candles = []
    global all_available_bosses
    all_available_bosses = []
    global check_to_requirement
    check_to_requirement = {}
    global special_check_to_door
    special_check_to_door = {}
    global special_check_to_requirement
    special_check_to_requirement = {
        "TO_BIG_000_START":  den_portal_available,
        "ICE_015_0_0_LEFT":  wall_room_available,
        "ICE_015_1_0_RIGHT": wall_room_available
    }

def set_logic_complexity(complexity):
    global logic_complexity
    logic_complexity = (complexity - 1)/2

def satisfies_requirement(requirement):
    check = True
    for req in requirement:
        check = req in key_ability_to_location
        if check:
            break
    return check

def process_key_logic():
    #Simplified version of the function from Item
    move_through_rooms()
    while True:
        #Place key item
        if check_to_requirement:
            #Weight checks
            requirement_list_list = []
            for check in check_to_requirement:
                requirement_list = check_to_requirement[check]
                if not requirement_list in requirement_list_list:
                    requirement_list_list.append(requirement_list)
            chosen_requirement_list = random.choice(requirement_list_list)
            #Weight requirements
            requirement_list = []
            for requirement in chosen_requirement_list:
                for num in range(key_abilities[requirement]):
                    requirement_list.append(requirement)
            chosen_requirement = random.choice(requirement_list)
            #Place item
            place_next_key(chosen_requirement)
        #Place last unecessary keys
        elif all_keys:
            place_next_key(random.choice(all_keys))
        #Stop when all keys are placed and all doors are explored
        else:
            break

def move_through_rooms():
    #Move through each door
    while True:
        for door in copy.deepcopy(current_available_doors):
            current_available_doors.remove(door)
            room = Item.get_door_room(door)
            if room in constant["BloodlessRequirement"]:
                for check, requirement in constant["BloodlessRequirement"][room][door].items():
                    #Don't automatically unlock certain checks
                    if check in special_check_to_requirement:
                        if not check in special_check_to_door:
                            special_check_to_door[check] = []
                        special_check_to_door[check].append(door)
                        continue
                    analyse_check(check, requirement)
            else:
                for subdoor in Room.map_connections[room]:
                    if subdoor == door:
                        continue
                    analyse_check(subdoor, [])
        #Keep going until stuck
        if current_available_doors:
            continue
        #Check special requirements
        for special_check in special_check_to_requirement:
            if special_check in special_check_to_door and special_check_to_requirement[special_check]():
                for door in special_check_to_door[special_check]:
                    analyse_check(special_check, constant["BloodlessRequirement"][Item.get_door_room(door)][door][special_check])
                del special_check_to_door[special_check]
        #Stop if no more doors are found
        if not current_available_doors:
            break

def check_lifted_obstacles():
    for check in list(check_to_requirement):
        if not check in check_to_requirement:
            continue
        requirement = check_to_requirement[check]
        analyse_check(check, requirement)

def reset_available_checks():
    previous_available_candles.clear()
    previous_available_candles.extend(current_available_candles)
    current_available_candles.clear()
    current_available_bosses.clear()

def analyse_check(check, requirement):
    #If accessible remove it from the requirement list
    accessible = satisfies_requirement(requirement)
    if accessible:
        if check in check_to_requirement:
            del check_to_requirement[check]
    #Handle each check type differently
    check_type = get_check_type(check)
    match check_type:
        case CheckType.Door:
            if check in all_available_doors:
                return
        case CheckType.Candle:
            if check in all_available_candles:
                return
        case CheckType.Boss:
            if check in all_available_bosses:
                return
    #Set check as available
    if accessible:
        match check_type:
            case CheckType.Door:
                all_available_doors.append(check)
                destination = Item.get_door_destination(check)
                if destination:
                    current_available_doors.append(destination)
                    all_available_doors.append(destination)
                    if destination in check_to_requirement:
                        del check_to_requirement[destination]
            case CheckType.Candle:
                current_available_candles.append(check)
                all_available_candles.append(check)
            case CheckType.Boss:
                current_available_bosses.append(check)
                all_available_bosses.append(check)
    #Add to requirement list
    else:
        if check in check_to_requirement:
            add_requirement_to_check(check, requirement)
        else:
            check_to_requirement[check] = requirement

def add_requirement_to_check(check, requirement):
    old_list = check_to_requirement[check] + requirement
    new_list = []
    for req in old_list:
        to_add = not req in new_list
        if type(req) is list:
            for subreq in old_list:
                if subreq in req:
                    to_add = False
        if to_add:
            new_list.append(req)
    check_to_requirement[check] = new_list

def get_check_type(check):
    if check in all_candles:
        return CheckType.Candle
    if check in constant["EnemyInfo"] or check == "N2008_BOSS":
        return CheckType.Boss
    return CheckType.Door

def place_next_key(chosen_item):
    if random.random() < logic_complexity:
        try:
            chosen_candle = pick_key_candle(current_available_candles)
        except IndexError:
            try:
                chosen_candle = pick_key_candle(previous_available_candles)
            except IndexError:
                chosen_candle = pick_key_candle(all_available_candles)
    elif random.random() < logic_complexity:
        try:
            chosen_candle = pick_key_candle(previous_available_candles)
        except IndexError:
            chosen_candle = pick_key_candle(all_available_candles)
    else:
        chosen_candle = pick_key_candle(all_available_candles)
    key_ability_to_location[chosen_item] = chosen_candle
    all_keys.remove(chosen_item)
    #Analyse the game again
    reset_available_checks()
    check_lifted_obstacles()
    move_through_rooms()

def pick_key_candle(available_candle):
    possible_candle = []
    for candle in available_candle:
        if not candle in list(key_ability_to_location.values()):
            possible_candle.append(candle)
    return random.choice(possible_candle)

def den_portal_available():
    for boss in boss_requirements:
        if not boss in all_available_bosses:
            return False
    return True

def wall_room_available():
    return "N1008" in all_available_bosses

def final_boss_available():
    return "N1013_Bael" in all_available_bosses

def randomize_bloodless_candles():
    process_key_logic()
    #Key abilities
    for item in key_ability_to_location:
        ability_to_location[item] = key_ability_to_location[item]
        all_candles.remove(key_ability_to_location[item])
        all_abilities.remove(item)
    #Remaining abilities
    for item in all_abilities:
        chosen_room = pick_and_remove(all_candles)
        ability_to_location[item] = chosen_room

def update_shard_candles():
    #All of Bloodless' abilities are stored inside of shard candles
    #Just like for Miriam those are defined inside of the level files
    for item in ability_to_location:
        file_name = f"{Item.chest_to_room(ability_to_location[item])}_Gimmick"
        class_name = "BP_DM_BloodlessAbilityGimmick_C"
        data_name = "UnlockAbilityType"
        old_value = f"EPBBloodlessAbilityType::{candle_to_ability[ability_to_location[item]]}"
        new_value = f"EPBBloodlessAbilityType::{item}"
        Utility.search_and_replace_string(file_name, class_name, data_name, old_value, new_value)

def increase_starting_stats():
    #Give Bloodless 4 of each stat to start with
    for stat in ["STR", "INT", "CON", "MND"]:
        for index in range(4):
            datatable["PB_DT_BloodlessAbilityData"][f"BLD_ABILITY_{stat}_UP_{index + 1}"]["IsUnlockedByDefault"] = True

def remove_gremory_cutscene():
    #Remove the new cutscene when entering the Gremory fight since it causes a softlock on custom maps
    datatable["PB_DT_EventFlagMaster"]["Event_15_001_0000"]["Id"]          = datatable["PB_DT_EventFlagMaster"]["Event_24_001_0000"]["Id"]
    datatable["PB_DT_EventFlagMaster"]["Event_15_geki_End"]["Id"]          = datatable["PB_DT_EventFlagMaster"]["Event_24_001_0000"]["Id"]
    datatable["PB_DT_EventFlagMaster"]["Event_15_Cine_End"]["Id"]          = datatable["PB_DT_EventFlagMaster"]["Event_24_001_0000"]["Id"]
    datatable["PB_DT_EventFlagMaster"]["Event_15_N1008_BattleStart"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_24_001_0000"]["Id"]
    datatable["PB_DT_RoomMaster"]["m18ICE_018"]["BgmID"] = "BGM_BOSS_B"

def pick_and_remove(array):
    item = random.choice(array)
    array.remove(item)
    return item

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    file_name = os.path.split(os.path.splitext(map)[0])[-1]
    log = {}
    log["Seed"] = seed
    log["Map"]  = file_name
    log["Key"]  = {}
    for item in ability_to_location:
        item_name = translation["Bloodless"][Utility.remove_inst_number(item)]
        if not item_name in log["Key"]:
            log["Key"][item_name] = []
        log["Key"][item_name].append(Item.chest_to_room(ability_to_location[item]))
    log["Beatable"] = final_boss_available()
    return log

def create_log_string(seed, map):
    #Log string for quickly showing answer to a seed
    file_name = os.path.split(os.path.splitext(map)[0])[-1]
    map_name = file_name if file_name else "Default"
    log_string = ""
    log_string += f"Seed: {seed}\n"
    log_string += f"Map: {map_name}\n"
    log_string += "Key:\n"
    for item in ability_to_location:
        if "_UP_" in item:
            break
        item_name = translation["Bloodless"][Utility.remove_inst_number(item)]
        log_string += f"  {item_name}: {ability_to_location[item]}"
        log_string += "\n"
    log_string += "Beatable: "
    log_string += "Yes" if final_boss_available() else "No"
    return log_string