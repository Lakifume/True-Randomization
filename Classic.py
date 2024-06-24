from System import *
import Manager
import Utility
import Room

def init():
    global item_to_level
    item_to_level = {
        "ItemCommonMoneyMedium":       "Stage_00",
        "ItemCommonMoneySmall":        "Stage_00",
        "ItemCommonMPLarge":           "Stage_00",
        "ItemCommonMPSmall":           "Stage_00",
        "ItemCommonWeaponDagger":      "Stage_00",
        "ItemCommonMagicKillAll":      "Stage_01",
        "ItemCommonMoneyLarge":        "Stage_01",
        "ItemCommonPotionInvisible":   "Stage_01",
        "ItemCommonWeaponBoneArc":     "Stage_01",
        "ItemCommonWeaponRuinousRood": "Stage_01",
        "ItemCommonWeaponUnholyFire":  "Stage_01",
        "ItemCommonMagicTimeShard":    "Stage_02",
        "ItemSecretCrown":             "Stage_02",
        "ItemSecretGoblet":            "Stage_03",
        "ItemSpecialExtraLife":        "Stage_03",
        "ItemTreasureChest":           "Stage_04",
        "ItemSecretLuckyCat":          "Stage_5A",
        "ItemSpecialFood":             "Stage_5B"
    }
    global key_item_to_location
    key_item_to_location = {}
    global location_to_item
    location_to_item = {}
    global item_to_type
    item_to_type = {}
    for type in constant["Classic2Pool"]:
        for item in constant["Classic2Pool"][type]:
            item_to_type[item] = type
    global key_items
    key_items = []
    key_items.extend(constant["Classic2Pool"]["KeyItem"])
    key_items.extend(constant["Classic2Pool"]["AbilityShard"])
    key_items.extend(constant["Classic2Pool"]["PassiveShard"])
    global overworld_types
    overworld_types = [
        "AttackShard",
        "AttackShard",
        "Consumable",
        "Consumable",
        "Consumable",
        "Consumable",
        "Consumable",
        "ShopItem",
        "ShopItem",
        "ShopItem"
    ]
    global current_available_checks
    current_available_checks = []
    global previous_available_checks
    previous_available_checks = []
    global all_available_checks
    all_available_checks = []
    global check_to_requirement
    check_to_requirement = {}
    global check_to_chest_class
    check_to_chest_class = {}
    global chest_to_level
    chest_to_level = {
        "BP_PBC2_ItemChest_HPRestore_C":          "Classic2_Region9_Dungeon5_Design",
        "BP_PBC2_ItemChest_HPUpgrade_4_C":        "Classic2_Region8_Map10b_Design",
        "BP_PBC2_ItemChest_KeyItem_DevilsRing_C": "Classic2_Region7_Map19_Design",
        "BP_PBC2_ItemChest_KeyItem_FancyBag_C":   "Classic2_Region4_Map10a_Design",
        "BP_PBC2_ItemChest_KeyItem_Omurice_C":    "Classic2_Region3_Map06a_Design",
        "BP_PBC2_ItemChest_MPUpgrade_7_C":        "Classic2_Region5_Dungeon3_Sand_Design",
        "BP_PBC2ItemChest_PlunderersRing_C":      "Classic2_Region1_Town01_Design",
        "BP_PBC2ItemChest_Waystone_C":            "Classic2_Region4_Town03_Design"
    }
    global linked_checks
    linked_checks = {
        "Region5_Map13_Alt_Design_19":         "Region5_Map13_Design_9",
        "Region5_Map13_Alt_Design_33":         "Region5_Map13_Design_23",
        "Region5_Dungeon3_Water_Design_165":   "Region5_Dungeon3_Sand_Design_56",
        "Region5_Dungeon3_Water_Design_210":   "Region5_Dungeon3_Sand_Design_86",
        "Region5_Dungeon3_Water_EnemyDay_153": "Region5_Dungeon3_Sand_EnemyDay_142"
    }
    global boss_chest_location
    boss_chest_location = {
        "Region3_Dungeon1_Design_85":          (-2080, 0,  5340),
        "Region4_Dungeon2_Design_112":         ( 6720, 0, 11420),
        "Region5_Dungeon3_Sand_EnemyDay_142":  (17600, 0,  2460),
        "Region5_Dungeon3_Water_EnemyDay_153": (17600, 0,  2460),
        "Region9_Dungeon5_Design_168":         (-9800, 0,  -900)
    }
    global shop_capacity
    shop_capacity = 10
    global valid_shops
    valid_shops = ["GK1", "GK2", "GK3", "GK5", "T1", "T2", "T3", "T4", "T5", "H1", "H2", "H3", "H4", "H5", "FM1", "FM2", "FM3", "IGA"]
    global item_to_shop_id
    item_to_shop_id = {
        "HEALTHRESTORE":  "HEALTH_RESTORE",
        "MANARESTORE":    "MANA_RESTORE",
        "OFUDACHARM":     "OFUDA_CHARM",
        "PLUNDERERSRING": "PLUNDERERS_RING",
        "EYEOFHORUS":     "EYE_OF_HORUS",
        "BONEARC":        "SHARD_BONE",
        "UNHOLYFIRE":     "SHARD_FIRE",
        "RUINOUSROOD":    "SHARD_ROOD",
        "TIMESHARD":      "SHARD_TIME"
    }
    global shop_skip
    shop_skip = [
        "COIN_CONVERSION",
        "WAYSTONE"
    ]
    global dialogue_key_notes
    dialogue_key_notes = [
        "spoken by dominique",
        "iga merchant",
        "special merchant",
        "merchant dialogue",
        "secret stock",
        "liber logaeth",
        "conversion dialogue",
        "town dialogue"
    ]
    global area_to_id
    area_to_id = {
        "Town01":       "C2_areaname_town01a",
        "Map13":        "C2_areaname_map13_sand",
        "DungeonFinal": "C2_areaname_finaldungeon_revealed"
    }

def set_logic_complexity(complexity):
    global logic_complexity
    logic_complexity = (complexity - 1)/2

def set_shop_price_weight(weight):
    global shop_price_weight
    shop_price_weight = Utility.weight_exponents[weight - 1]

def apply_default_tweaks():
    #Apply manual tweaks defined in the json
    for file in constant["Classic2Tweak"]:
        for entry in constant["Classic2Tweak"][file]:
            for data in constant["Classic2Tweak"][file][entry]:
                datatable[file][entry][data] = constant["Classic2Tweak"][file][entry][data]
    #Extend the kill zone in sandy Megido Wastes to cover the whole room to force getting True Sight first
    game_data["Classic2_Region5_Map13_Collision"].Exports[98].Data[1].Value[0].Value = FVector(9999, 1, 1)

def satisfies_requirement(requirement):
    check = True
    for req in requirement:
        #AND
        if type(req) is list:
            for subreq in req:
                check = subreq in key_item_to_location
                if not check:
                    break
            if check:
                break
        #OR  
        else:
            check = req in key_item_to_location
            if check:
                break
    return check

def randomize_candle_drops():
    #Convert the drop dictionary to a weighted list
    classic_pool = []
    for item in constant["ClassicDrop"]:
        for num in range(constant["ClassicDrop"][item]):
            classic_pool.append(item)
    #Search for any instance of SpawnItemTypeClass and replace it with a random item
    for stage in ["Stage_00", "Stage_01", "Stage_02", "Stage_03", "Stage_04", "Stage_05A", "Stage_05B"]:
        filename = f"Classic_{stage}_Objects"
        uasset = game_data[filename]
        for export in uasset.Exports:
            for data in export.Data:
                if str(data.Name) != "SpawnItemTypeClass":
                    continue
                class_name = Utility.get_object_class(uasset, data)
                if not class_name:
                    continue
                #Don't randomize the item if it isn't in the pool list
                if not class_name.split("_")[2] in classic_pool:
                    continue
                chosen_item = random.choice(classic_pool)
                source_asset = game_data[f"Classic_{item_to_level[chosen_item]}_Objects"]
                data.Value = Utility.copy_asset_import(chosen_item, source_asset, uasset)
                break

def process_key_logic():
    move_through_checks()
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
            #Choose requirement and key item
            chosen_requirement = random.choice(chosen_requirement_list)
            if type(chosen_requirement) is list:
                random.shuffle(chosen_requirement)
                for item in chosen_requirement:
                    if satisfies_requirement([item]):
                        continue
                    place_next_key(item)
            else:
                place_next_key(chosen_requirement)
        #Place last unecessary keys
        elif key_items:
            place_next_key(random.choice(key_items))
        #Stop when all keys are placed and all doors are explored
        else:
            break

def move_through_checks():
    for check, requirement in constant["Classic2Requirement"].items():
        accessible = satisfies_requirement(requirement)
        if accessible:
            if check in check_to_requirement:
                del check_to_requirement[check]
        if check in all_available_checks:
            continue
        if accessible:
            current_available_checks.append(check)
            all_available_checks.append(check)
        else:
            check_to_requirement[check] = requirement

def reset_available_checks():
    previous_available_checks.clear()
    previous_available_checks.extend(current_available_checks)
    current_available_checks.clear()

def place_next_key(chosen_item):
    if random.random() < logic_complexity:
        try:
            chosen_check = pick_key_check(current_available_checks)
        except IndexError:
            try:
                chosen_check = pick_key_check(previous_available_checks)
            except IndexError:
                chosen_check = pick_key_check(all_available_checks)
    elif random.random() < logic_complexity:
        try:
            chosen_check = pick_key_check(previous_available_checks)
        except IndexError:
            chosen_check = pick_key_check(all_available_checks)
    else:
        chosen_check = pick_key_check(all_available_checks)
    key_item_to_location[chosen_item] = chosen_check
    key_items.remove(chosen_item)
    #Analyse the game again
    reset_available_checks()
    move_through_checks()

def pick_key_check(available_checks):
    possible_checks = []
    for check in available_checks:
        if not check in list(key_item_to_location.values()):
            possible_checks.append(check)
    return random.choice(possible_checks)

def randomize_item_pool():
    process_key_logic()
    #Neutralize the first chest that will be used later for copying
    chest_info = constant["ActorPointer"]["BP_PBC2_ItemChest_Base_C"]
    neutralize_chest_export(game_data[chest_info["File"]], game_data[chest_info["File"]].Exports[chest_info["Index"]])
    #Assign items to every check
    for item, location in key_item_to_location.items():
        location_to_item[location] = item
    for check in constant["Classic2Requirement"]:
        if not check in location_to_item:
            location_to_item[check] = pick_next_item()
    for check in linked_checks:
        location_to_item[check] = location_to_item[linked_checks[check]]
    #Apply the changes in the assets
    available_chest_classes = list(chest_to_level)
    modified_chest_blueprints = []
    for check, item in location_to_item.items():
        split_check = check.split("_")
        export_index = int(split_check.pop()) - 1
        file_name = "Classic2_" + "_".join(split_check)
        uasset = game_data[file_name]
        export = uasset.Exports[export_index]
        class_name = Utility.get_export_class(uasset, export)
        if not class_name:
            continue
        #For a regular chest change the class to its parent and override its content
        if "ItemChest" in class_name:
            neutralize_chest_export(uasset, export)
            export.Data.Add(create_item_struct(uasset, item))
            if check == "Region5_Dungeon3_Water_Design_210":
                export.Data.Add(create_bool_struct(uasset, "m_shouldFall", False))
                uasset.Exports[export.Data[5].Value.Index - 1].Data[0].Value[0].Value = FVector(10200, 0, 2232)
        #For a wall drop edit its chest blueprint directly
        if "Breakable" in class_name:
            for data in export.Data:
                if str(data.Name) == "m_pPrimaryItemClass":
                    sub_class = Utility.get_object_class(uasset, data)
                    item_class_struct = data
                    break
            if check in linked_checks:
                sub_class = check_to_chest_class[linked_checks[check]]
            if not "ItemChest" in sub_class or sub_class in modified_chest_blueprints:
                if not check in linked_checks:
                    sub_class = available_chest_classes[0]
                    available_chest_classes.remove(sub_class)
                if sub_class in chest_to_level:
                    source_asset = game_data[chest_to_level[sub_class]]
                    item_class_struct.Value = Utility.copy_asset_import(sub_class, source_asset, uasset)
            modified_chest_blueprints.append(sub_class)
            check_to_chest_class[check] = sub_class
            class_split = sub_class.split("_")
            class_split.pop()
            file_name = "_".join(class_split)
            uasset = game_data[file_name]
            export = uasset.Exports[1]
            export.Data.Clear()
            export.Data.Add(create_item_struct(uasset, item))
        #For a hunter drop edit its chest blueprint directly
        if "HunterBattleTrigger" in class_name:
            for data in export.Data:
                if str(data.Name) == "m_pSpawnChestClass":
                    sub_class = Utility.get_object_class(uasset, data)
                    break
            class_split = sub_class.split("_")
            class_split.pop()
            file_name = "_".join(class_split)
            uasset = game_data[file_name]
            export = uasset.Exports[1]
            export.Data.Remove(export.Data[1])
            export.Data.Add(create_item_struct(uasset, item))
        #For a boss trigger remove its drop and place a chest in the boss room
        if "BossBattleTrigger" in class_name:
            for data in export.Data:
                if str(data.Name) == "m_shardAbility":
                    data.Value = FName.FromString(uasset, "EPBC2AbilityShard::NONE")
                if str(data.Name) == "m_shardPassive":
                    data.Value = FName.FromString(uasset, "EPBC2PassiveShard::NONE")
                if str(data.Name) == "m_freezePlayerMovementOnDefeat":
                    data.Value = False
            x_pos, y_pos, z_pos = boss_chest_location[check]
            location = FVector(x_pos, y_pos, z_pos)
            actor_index = len(uasset.Exports)
            Room.add_level_actor(file_name, "BP_PBC2_ItemChest_Base_C", location, FRotator(0, 0, 0), FVector(1, 1, 1), {})
            export = uasset.Exports[actor_index]
            neutralize_chest_export(uasset, export)
            if "Dungeon3" in check:
                export.Data.Add(create_bool_struct(uasset, "m_isInDungeon3", True))
            export.Data.Add(create_bool_struct(uasset, "m_shouldFall", False))
            export.Data.Add(create_item_struct(uasset, item))

def pick_next_item():
    item_type = random.choice(overworld_types)
    item_pool = constant["Classic2Pool"][item_type]
    chosen_item = random.choice(item_pool)
    if item_type != "Consumable":
        item_pool.remove(chosen_item)
    if not item_pool:
        while item_type in overworld_types:
            overworld_types.remove(item_type)
    return chosen_item

def create_item_struct(uasset, chosen_item):
    item_type = item_to_type[chosen_item]
    enum_type = f"EPBC2{item_type}"
    struct = EnumPropertyData()
    struct.Name = FName.FromString(uasset, f"m_{item_type[0].lower() + item_type[1:]}")
    struct.EnumType = FName.FromString(uasset, enum_type)
    struct.Value = FName.FromString(uasset, f"{enum_type}::{chosen_item}")
    return struct

def create_bool_struct(uasset, bool_name, enable):
    struct = BoolPropertyData()
    struct.Name = FName.FromString(uasset, bool_name)
    struct.Value = enable
    return struct

def neutralize_chest_export(uasset, export):
    old_class_index_index = export.SerializationBeforeCreateDependencies.index(export.ClassIndex)
    old_template_index_index = export.SerializationBeforeCreateDependencies.index(export.TemplateIndex)
    export.ClassIndex = FPackageIndex(uasset.SearchForImport(FName.FromString(uasset, "BP_PBC2_ItemChest_Base_C")))
    export.TemplateIndex = FPackageIndex(uasset.SearchForImport(FName.FromString(uasset, "Default__BP_PBC2_ItemChest_Base_C")))
    export.SerializationBeforeCreateDependencies[old_class_index_index] = export.ClassIndex
    export.SerializationBeforeCreateDependencies[old_template_index_index] = export.TemplateIndex
    for data_index in range(len(export.Data)):
        if str(export.Data[data_index].Name) == "BlueprintCreatedComponents":
            last_index = data_index + 1
    while len(export.Data) > last_index:
        export.Data.Remove(export.Data[last_index])

def randomize_shop_pool():
    #Start by resetting the shop
    for item in datatable["DT_PBC2_ShopData"]:
        if item in shop_skip:
            continue
        for shop in valid_shops:
            datatable["DT_PBC2_ShopData"][item][shop] = False
        datatable["DT_PBC2_ShopData"][item]["REQUIRE_ATK_SHARD_TO_SEE"] = "EPBC2AttackShard::NONE"
        datatable["DT_PBC2_ShopData"][item]["REQUIRE_KEY_ITEM_TO_SEE"] =  "EPBC2KeyItem::NONE"
        datatable["DT_PBC2_ShopData"][item]["COSTS_ATK_SHARD"] =          "EPBC2AttackShard::NONE"
        datatable["DT_PBC2_ShopData"][item]["COSTS_KEY_ITEM"] =           "EPBC2KeyItem::NONE"
    #Place the remaining unique items
    shop_quantity = {shop: 0 for shop in valid_shops}
    shop_types = list(dict.fromkeys(overworld_types))
    shop_types.remove("Consumable")
    shop_types.append("ShopOnly")
    for type in shop_types:
        for item in constant["Classic2Pool"][type]:
            item_shop_id = get_item_shop_id(item)
            chosen_shop = random.choice(valid_shops)
            #Don't give the IGA merchant holy water or he'll be unreachable
            while item == "UNHOLYFIRE" and chosen_shop == "IGA":
                chosen_shop = random.choice(valid_shops)
            datatable["DT_PBC2_ShopData"][item_shop_id][chosen_shop] = True
            shop_quantity[chosen_shop] += 1
            #Shop menus can't carry more than 10 items
            if shop_quantity[chosen_shop] >= shop_capacity:
                valid_shops.remove(chosen_shop)
    #Lock the last attack upgrade behind omurice to make it useful
    datatable["DT_PBC2_ShopData"]["ATK_UP_5"]["REQUIRE_KEY_ITEM_TO_SEE"] = "EPBC2KeyItem::OMURICE"
    datatable["DT_PBC2_ShopData"]["ATK_UP_5"]["COSTS_KEY_ITEM"] =          "EPBC2KeyItem::OMURICE"
    #End with extra consumables
    for shop in valid_shops:
        valid_items = []
        for item in constant["Classic2Pool"]["Consumable"]:
            item_shop_id = get_item_shop_id(item)
            if not item_shop_id in shop_skip:
                valid_items.append(item_shop_id)
        #Determine consumable amount by shop type
        shop_type = "".join([char for char in shop if not char.isdigit()])
        match shop_type:
            case "GK":
                minimum = 0
                maximum = 2
            case "T":
                minimum = 3
                maximum = 6
            case "FM":
                minimum = 2
                maximum = 3
            case "IGA":
                minimum = 3
                maximum = 3
            case _:
                minimum = 0
                maximum = 0
        minimum = min(minimum, shop_capacity - shop_quantity[shop])
        maximum = min(maximum, shop_capacity - shop_quantity[shop])
        item_quantity = random.randint(minimum, maximum)
        for num in range(item_quantity):
            chosen_item = random.choice(valid_items)
            valid_items.remove(chosen_item)
            datatable["DT_PBC2_ShopData"][chosen_item][shop] = True
            shop_quantity[shop] += 1

def get_item_shop_id(item):
    if item in item_to_shop_id:
        return item_to_shop_id[item]
    if "Shard" in item_to_type[item]:
        return f"SHARD_{item}"
    return item

def randomize_shop_prices(scale):
    for entry in datatable["DT_PBC2_ShopData"]:
        if datatable["DT_PBC2_ShopData"][entry]["COIN_COST"] == 0 or entry in shop_skip:
            continue
        coin_price = datatable["DT_PBC2_ShopData"][entry]["COIN_COST"]
        rmnt_ratio = datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"]/coin_price
        #Coin
        multiplier = Utility.random_weighted(1.0, 0.2, 5.0, 0.01, shop_price_weight, False)
        datatable["DT_PBC2_ShopData"][entry]["COIN_COST"] = int(coin_price*multiplier)
        datatable["DT_PBC2_ShopData"][entry]["COIN_COST"] = max(datatable["DT_PBC2_ShopData"][entry]["COIN_COST"], 1)
        datatable["DT_PBC2_ShopData"][entry]["COIN_COST"] = round(datatable["DT_PBC2_ShopData"][entry]["COIN_COST"]/5)*5
        #Remnant
        if not scale:
            multiplier = Utility.random_weighted(1.0, 0.2, 5.0, 0.01, shop_price_weight, False)
        datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"] = int(coin_price*multiplier*rmnt_ratio)
        datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"] = max(datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"], 1)
        datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"] = round(datatable["DT_PBC2_ShopData"][entry]["RMNT_COST"]/5)*5

def randomize_dialogues():
    valid_dialogues = []
    dialogue_pool = []
    for entry in datatable["DT_PBC2_DialogData"]:
        for note in dialogue_key_notes:
            if note.lower() in datatable["DT_PBC2_DialogData"][entry]["Description"].lower():
                valid_dialogues.append(entry)
                dialogue_pool.append(entry)
                break
    for entry in datatable["DT_PBC2_DialogData"]:
        if not entry in valid_dialogues:
            continue
        chosen_entry = random.choice(dialogue_pool)
        dialogue_pool.remove(chosen_entry)
        for lang in datatable["DT_PBC2_DialogData"][entry]:
            if not lang in ["Type", "Description"]:
                datatable["DT_PBC2_DialogData"][entry][lang] = Manager.original_datatable["DT_PBC2_DialogData"][chosen_entry][lang]

def set_easy_mode():
    multiply_enemy_damage(0.5)
    multiply_enemy_health(2/3)
    game_data["BP_PBC2_Player_Dominique"].Exports[2].Data[168].Value[0].Value = FVector(0, 0, 0)

def set_hard_mode():
    multiply_enemy_damage(2.0)
    multiply_enemy_health(1.5)

def multiply_enemy_damage(multiplier):
    for entry in datatable["DT_PBC2_EnemyData"]:
        datatable["DT_PBC2_EnemyData"][entry]["C_ATK"] = round(datatable["DT_PBC2_EnemyData"][entry]["C_ATK"]*multiplier)
        datatable["DT_PBC2_EnemyData"][entry]["ATK1"]  = round(datatable["DT_PBC2_EnemyData"][entry]["ATK1"]*multiplier)
        datatable["DT_PBC2_EnemyData"][entry]["ATK2"]  = round(datatable["DT_PBC2_EnemyData"][entry]["ATK2"]*multiplier)
        datatable["DT_PBC2_EnemyData"][entry]["ATK3"]  = round(datatable["DT_PBC2_EnemyData"][entry]["ATK3"]*multiplier)
    for entry in datatable["DT_PBC2_HunterData"]:
        datatable["DT_PBC2_HunterData"][entry]["C_ATK"] = round(datatable["DT_PBC2_HunterData"][entry]["C_ATK"]*multiplier)
        datatable["DT_PBC2_HunterData"][entry]["ATK1"]  = round(datatable["DT_PBC2_HunterData"][entry]["ATK1"]*multiplier)
        datatable["DT_PBC2_HunterData"][entry]["ATK2"]  = round(datatable["DT_PBC2_HunterData"][entry]["ATK2"]*multiplier)
        datatable["DT_PBC2_HunterData"][entry]["ATK3"]  = round(datatable["DT_PBC2_HunterData"][entry]["ATK3"]*multiplier)
    for entry in datatable["DT_PBC2_BossData"]:
        datatable["DT_PBC2_BossData"][entry]["C_ATK"] = round(datatable["DT_PBC2_BossData"][entry]["C_ATK"]*multiplier)
        datatable["DT_PBC2_BossData"][entry]["ATK1"]  = round(datatable["DT_PBC2_BossData"][entry]["ATK1"]*multiplier)
        datatable["DT_PBC2_BossData"][entry]["ATK2"]  = round(datatable["DT_PBC2_BossData"][entry]["ATK2"]*multiplier)
        datatable["DT_PBC2_BossData"][entry]["ATK3"]  = round(datatable["DT_PBC2_BossData"][entry]["ATK3"]*multiplier)
    for entry in datatable["DT_PBC2_ProjectileData"]:
        if datatable["DT_PBC2_ProjectileData"][entry]["PlayerProjectile"]:
            continue
        datatable["DT_PBC2_ProjectileData"][entry]["Atk"]      = round(datatable["DT_PBC2_ProjectileData"][entry]["Atk"]*multiplier)
        datatable["DT_PBC2_ProjectileData"][entry]["Atk_Ext"]  = round(datatable["DT_PBC2_ProjectileData"][entry]["Atk_Ext"]*multiplier)
    for suffix in ["1_Unit_Wide", "Fortress_01", "Fortress_02", "Nature_01", "Nature_02"]:
        game_data[f"BP_PBC2_Spikes_{suffix}"].Exports[1].Data[3].Value *= multiplier
    game_data["BP_PBC2_Player_Dominique"].Exports[2].Data[258].Value *= multiplier

def multiply_enemy_health(multiplier):
    for entry in datatable["DT_PBC2_EnemyData"]:
        datatable["DT_PBC2_EnemyData"][entry]["HP_DAY"]   = round(datatable["DT_PBC2_EnemyData"][entry]["HP_DAY"]*multiplier)
        datatable["DT_PBC2_EnemyData"][entry]["HP_NIGHT"] = round(datatable["DT_PBC2_EnemyData"][entry]["HP_NIGHT"]*multiplier)
    for entry in datatable["DT_PBC2_HunterData"]:
        datatable["DT_PBC2_HunterData"][entry]["HP"] = round(datatable["DT_PBC2_HunterData"][entry]["HP"]*multiplier)
    for entry in datatable["DT_PBC2_BossData"]:
        datatable["DT_PBC2_BossData"][entry]["HP"] = round(datatable["DT_PBC2_BossData"][entry]["HP"]*multiplier)

def create_log():
    log = {}
    for item, location in key_item_to_location.items():
        area_name = location.split("_")[1]
        if area_name in area_to_id:
            area_id = area_to_id[area_name]
        else:
            area_id = f"C2_areaname_{area_name.lower()}"
            if "dungeon" in area_id:
                area_id = f"{area_id[:-1]}0{area_id[-1:]}"
        log[item] = datatable["DT_PBC2_DialogData"][area_id]["English"]
    return log