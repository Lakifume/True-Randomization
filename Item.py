import Manager
import Utility
import random
import os
import copy
from enum import Enum

class CheckType(Enum):
    Door  = 0
    Chest = 1
    Enemy = 2

def init():
    #Declare variables
    global used_chests
    used_chests = [
        "PotionMaterial",
        "Qu07_Last",
        "Swordsman",
        "Treasurebox_SIP000_Tutorial",
        "Treasurebox_SIP002_1",
        "Treasurebox_SIP003_1",
        "Treasurebox_SIP004_1",
        "Treasurebox_SIP005_1",
        "Treasurebox_SIP005_2",
        "Treasurebox_SIP006_1",
        "Treasurebox_SIP007_1",
        "Treasurebox_SIP007_2",
        "Treasurebox_SIP009_1",
        "Treasurebox_SIP011_1",
        "Treasurebox_SIP011_2",
        "Treasurebox_SIP011_3",
        "Treasurebox_SIP011_4",
        "Treasurebox_SIP012_1",
        "Treasurebox_SIP013_1",
        "Treasurebox_SIP014_1",
        "Treasurebox_SIP015_1",
        "Treasurebox_SIP016_1",
        "Treasurebox_SIP017_1",
        "Treasurebox_SIP018_1",
        "Treasurebox_SIP019_1",
        "Treasurebox_SIP020_1",
        "Treasurebox_SIP021_2",
        "Treasurebox_SIP024_1",
        "Treasurebox_SIP024_2",
        "Treasurebox_SIP025_1",
        "Treasurebox_SIP025_2",
        "Treasurebox_SIP026_1",
        "Treasurebox_VIL001_1",
        "Treasurebox_VIL003_1",
        "Treasurebox_VIL005_1",
        "Treasurebox_VIL006_1",
        "Treasurebox_VIL006_2",
        "Treasurebox_VIL006_3",
        "Treasurebox_VIL006_4",
        "Treasurebox_VIL007_1",
        "Treasurebox_VIL008_1",
        "Treasurebox_VIL008_2",
        "Treasurebox_VIL010_1",
        "Treasurebox_ENT002_1",
        "Treasurebox_ENT002_2",
        "Treasurebox_ENT002_3",
        "Treasurebox_ENT004_1",
        "Treasurebox_ENT005_1",
        "Treasurebox_ENT005_2",
        "Treasurebox_ENT007_1",
        "Treasurebox_ENT007_2",
        "Treasurebox_ENT007_3",
        "Treasurebox_ENT009_1",
        "Treasurebox_ENT011_1",
        "Treasurebox_ENT014_1",
        "Treasurebox_ENT014_2",
        "Treasurebox_ENT014_3",
        "Treasurebox_ENT018_1",
        "Treasurebox_ENT018_2",
        "Treasurebox_ENT020_1",
        "Treasurebox_ENT020_2",
        "Treasurebox_ENT021_1",
        "Treasurebox_ENT022_1",
        "Treasurebox_ENT024_1",
        "Treasurebox_ENT024_2",
        "Treasurebox_ENT024_3",
        "Treasurebox_GDN002_1",
        "Treasurebox_GDN004_1",
        "Treasurebox_GDN006_1",
        "Treasurebox_GDN006_2",
        "Treasurebox_GDN006_3",
        "Treasurebox_GDN006_4",
        "Treasurebox_GDN006_5",
        "Treasurebox_GDN007_1",
        "Treasurebox_GDN009_1",
        "Treasurebox_GDN009_2",
        "Treasurebox_GDN010_1",
        "Treasurebox_GDN012_1",
        "Treasurebox_GDN012_2",
        "Treasurebox_GDN013_1",
        "Treasurebox_GDN013_2",
        "Treasurebox_GDN013_3",
        "Treasurebox_GDN013_4",
        "Treasurebox_GDN014_1",
        "Treasurebox_SAN003_1",
        "Treasurebox_SAN003_2",
        "Treasurebox_SAN003_3",
        "Treasurebox_SAN003_4",
        "Treasurebox_SAN003_5",
        "Treasurebox_SAN003_6",
        "Treasurebox_SAN003_7",
        "Treasurebox_SAN003_8",
        "Treasurebox_SAN005_1",
        "Treasurebox_SAN005_2",
        "Treasurebox_SAN009_1",
        "Treasurebox_SAN009_2",
        "Treasurebox_SAN013_1",
        "Treasurebox_SAN013_2",
        "Treasurebox_SAN014_1",
        "Treasurebox_SAN015_2",
        "Treasurebox_SAN015_3",
        "Treasurebox_SAN016_1",
        "Treasurebox_SAN016_2",
        "Treasurebox_SAN016_3",
        "Treasurebox_SAN016_4",
        "Treasurebox_SAN016_5",
        "Treasurebox_SAN017_1",
        "Treasurebox_SAN019_1",
        "Treasurebox_SAN019_2",
        "Treasurebox_SAN019_3",
        "Treasurebox_SAN020_1",
        "Treasurebox_SAN021_1",
        "Treasurebox_SAN021_2",
        "Treasurebox_SAN021_3",
        "Treasurebox_SAN021_4",
        "Treasurebox_SAN021_5",
        "Treasurebox_SAN024_1",
        "Treasurebox_TWR000_1",
        "Treasurebox_TWR003_1",
        "Treasurebox_TWR004_1",
        "Treasurebox_TWR005_1",
        "Treasurebox_TWR006_1",
        "Treasurebox_TWR008_1",
        "Treasurebox_TWR009_1",
        "Treasurebox_TWR010_1",
        "Treasurebox_TWR012_1",
        "Treasurebox_TWR013_1",
        "Treasurebox_TWR016_1",
        "Treasurebox_TWR017_1",
        "Treasurebox_TWR017_2",
        "Treasurebox_TWR017_3",
        "Treasurebox_TWR017_4",
        "Treasurebox_TWR017_5",
        "Treasurebox_TWR017_6",
        "Treasurebox_TWR017_7",
        "Treasurebox_TWR018_1",
        "Treasurebox_TWR018_2",
        "Treasurebox_TWR018_3",
        "Treasurebox_TWR018_4",
        "Treasurebox_TWR018_5",
        "Treasurebox_TWR018_6",
        "Treasurebox_TWR018_7",
        "Treasurebox_TWR018_8",
        "Treasurebox_TWR019_1",
        "Treasurebox_TWR019_2",
        "Treasurebox_TWR019_4",
        "Treasurebox_LIB001_1",
        "Treasurebox_LIB002_1",
        "Treasurebox_LIB007_1",
        "Treasurebox_LIB009_1",
        "Treasurebox_LIB009_2",
        "Treasurebox_LIB011_1",
        "Treasurebox_LIB012_1",
        "Treasurebox_LIB017_1",
        "Treasurebox_LIB019_1",
        "Treasurebox_LIB022_1",
        "Treasurebox_LIB030_1",
        "Treasurebox_LIB032_1",
        "Treasurebox_LIB033_1",
        "Treasurebox_LIB040_1",
        "Treasurebox_LIB043_1",
        "Treasurebox_TRN002_1",
        "Treasurebox_TRN002_2",
        "Treasurebox_TRN002_3",
        "Treasurebox_TRN002_4",
        "Treasurebox_TRN002_5",
        "Treasurebox_KNG002_1",
        "Treasurebox_KNG002_2",
        "Treasurebox_KNG003_1",
        "Treasurebox_KNG006_1",
        "Treasurebox_KNG010_1",
        "Treasurebox_KNG011_1",
        "Treasurebox_KNG012_1",
        "Treasurebox_KNG012_2",
        "Treasurebox_KNG016_1",
        "Treasurebox_KNG017_1",
        "Treasurebox_KNG017_2",
        "Treasurebox_KNG017_3",
        "Treasurebox_KNG017_4",
        "Treasurebox_KNG017_5",
        "Treasurebox_KNG018_2",
        "Treasurebox_KNG018_3",
        "Treasurebox_KNG018_4",
        "Treasurebox_KNG021_1",
        "Treasurebox_KNG022_1",
        "Treasurebox_UGD001_1",
        "Treasurebox_UGD003_1",
        "Treasurebox_UGD003_2",
        "Treasurebox_UGD003_3",
        "Treasurebox_UGD003_4",
        "Treasurebox_UGD005_1",
        "Treasurebox_UGD005_2",
        "Treasurebox_UGD007_1",
        "Treasurebox_UGD009_1",
        "Treasurebox_UGD009_2",
        "Treasurebox_UGD009_3",
        "Treasurebox_UGD009_4",
        "Treasurebox_UGD010_1",
        "Treasurebox_UGD011_1",
        "Treasurebox_UGD021_1",
        "Treasurebox_UGD024_1",
        "Treasurebox_UGD024_2",
        "Treasurebox_UGD024_3",
        "Treasurebox_UGD025_1",
        "Treasurebox_UGD025_2",
        "Treasurebox_UGD025_3",
        "Treasurebox_UGD027_1",
        "Treasurebox_UGD030_1",
        "Treasurebox_UGD031_1",
        "Treasurebox_UGD031_2",
        "Treasurebox_UGD036_1",
        "Treasurebox_UGD036_2",
        "Treasurebox_UGD038_1",
        "Treasurebox_UGD040_1",
        "Treasurebox_UGD041_1",
        "Treasurebox_UGD042_1",
        "Treasurebox_UGD044_1",
        "Treasurebox_UGD044_2",
        "Treasurebox_UGD046_1",
        "Treasurebox_UGD046_2",
        "Treasurebox_UGD047_2",
        "Treasurebox_UGD048_1",
        "Treasurebox_UGD050_1",
        "Treasurebox_UGD051_1",
        "Treasurebox_UGD052_1",
        "Treasurebox_UGD052_2",
        "Treasurebox_UGD053_1",
        "Treasurebox_UGD054_1",
        "Treasurebox_UGD056_1",
        "Treasurebox_SND002_1",
        "Treasurebox_SND003_1",
        "Treasurebox_SND004_1",
        "Treasurebox_SND006_1",
        "Treasurebox_SND008_1",
        "Treasurebox_SND008_2",
        "Treasurebox_SND009_1",
        "Treasurebox_SND010_1",
        "Treasurebox_SND010_2",
        "Treasurebox_SND013_1",
        "Treasurebox_SND015_1",
        "Treasurebox_SND016_1",
        "Treasurebox_SND017_1",
        "Treasurebox_SND018_1",
        "Treasurebox_SND019_1",
        "Treasurebox_SND020_1",
        "Treasurebox_SND024_1",
        "Treasurebox_SND025_1",
        "Treasurebox_ARC000_1",
        "Treasurebox_ARC002_1",
        "Treasurebox_ARC003_1",
        "Treasurebox_ARC004_1",
        "Treasurebox_ARC006_1",
        "Treasurebox_ARC006_2",
        "Treasurebox_ARC007_1",
        "Treasurebox_ARC007_2",
        "Treasurebox_TAR001_1",
        "Treasurebox_TAR002_1",
        "Treasurebox_TAR006_1",
        "Treasurebox_TAR007_1",
        "Treasurebox_TAR010_1",
        "Treasurebox_JPN002_1",
        "Treasurebox_JPN002_2",
        "Treasurebox_JPN004_1",
        "Treasurebox_JPN005_1",
        "Treasurebox_JPN009_1",
        "Treasurebox_JPN010_1",
        "Treasurebox_JPN010_2",
        "Treasurebox_JPN013_1",
        "Treasurebox_JPN015_1",
        "Treasurebox_JPN017_1",
        "Treasurebox_JPN018_1",
        "Treasurebox_RVA001_1",
        "Treasurebox_RVA001_2",
        "Treasurebox_RVA002_1",
        "Treasurebox_RVA004_1",
        "Treasurebox_RVA006_1",
        "Treasurebox_RVA010_1",
        "Treasurebox_RVA011_1",
        "Treasurebox_RVA011_2",
        "Treasurebox_RVA012_1",
        "Treasurebox_RVA015_1",
        "Treasurebox_BIG002_1",
        "Treasurebox_BIG005_1",
        "Treasurebox_BIG006_1",
        "Treasurebox_BIG006_2",
        "Treasurebox_BIG006_3",
        "Treasurebox_BIG006_4",
        "Treasurebox_BIG006_5",
        "Treasurebox_BIG006_6",
        "Treasurebox_BIG007_1",
        "Treasurebox_BIG008_1",
        "Treasurebox_BIG010_1",
        "Treasurebox_BIG011_1",
        "Treasurebox_BIG012_1",
        "Treasurebox_BIG012_2",
        "Treasurebox_BIG012_3",
        "Treasurebox_BIG013_1",
        "Treasurebox_BIG014_1",
        "Treasurebox_BIG016_1",
        "Treasurebox_BIG016_2",
        "Treasurebox_BIG016_3",
        "Treasurebox_ICE001_1",
        "Treasurebox_ICE001_2",
        "Treasurebox_ICE002_1",
        "Treasurebox_ICE003_1",
        "Treasurebox_ICE003_2",
        "Treasurebox_ICE006_1",
        "Treasurebox_ICE008_1",
        "Treasurebox_ICE008_2",
        "Treasurebox_ICE010_1",
        "Treasurebox_ICE011_1",
        "Treasurebox_ICE013_1",
        "Treasurebox_ICE014_1",
        "Treasurebox_PureMiriam_Hair",
        "Treasurebox_PureMiriam_Tiare",
        "Treasurebox_PureMiriam_Dress",
        "Treasurebox_PureMiriam_Sword",
        "Wall_SIP004_1",
        "Wall_SIP009_1",
        "Wall_SIP014_1",
        "Wall_SIP016_1",
        "Wall_ENT002_1",
        "Wall_ENT012_1",
        "Wall_GDN006_1",
        "Wall_SAN000_1",
        "Wall_SAN005_1",
        "Wall_SAN019_1",
        "Wall_KNG000_1",
        "Wall_KNG007_1",
        "Wall_LIB004_1",
        "Wall_LIB019_1",
        "Wall_LIB025_1",
        "Wall_TWR006_1",
        "Wall_TWR013_1",
        "Wall_TWR016_1",
        "Wall_TRN005_1",
        "Wall_UGD000_1",
        "Wall_UGD003_1",
        "Wall_UGD006_1",
        "Wall_UGD012_1",
        "Wall_UGD020_1",
        "Wall_UGD031_1",
        "Wall_UGD037_1",
        "Wall_UGD046_1",
        "Wall_UGD056_1",
        "Wall_SND001_1",
        "Wall_SND019_1",
        "Wall_TAR007_1",
        "Wall_JPN011_1",
        "Wall_JPN013_1",
        "Wall_RVA011_1",
        "Wall_BIG002_1",
        "Wall_BIG012_1",
        "Wall_BIG016_1",
        "Wall_ICE003_1",
        "Wall_ICE010_1",
        "Wall_ICE017_1",
        "N3106_1ST_Treasure",
        "N3106_2ND_Treasure",
        "Treasurebox_JRN001_1",
        "Treasurebox_JRN001_2",
        "Treasurebox_JRN001_3",
        "Treasurebox_JRN002_1",
        "Treasurebox_JRN004_1"
    ]
    global room_to_area
    room_to_area = {
        "SIP": "m01",
        "VIL": "m02",
        "ENT": "m03",
        "GDN": "m04",
        "SAN": "m05",
        "KNG": "m06",
        "LIB": "m07",
        "TWR": "m08",
        "TRN": "m09",
        "BIG": "m10",
        "UGD": "m11",
        "SND": "m12",
        "ARC": "m13",
        "TAR": "m14",
        "JPN": "m15",
        "RVA": "m17",
        "ICE": "m18",
        "K2C": "m19",
        "JRN": "m20",
        "EBT": "m51",
        "LBP": "m77",
        "BKR": "m88"
    }
    global keyless_chests
    keyless_chests = [
        "Treasurebox_SIP000_Tutorial",
        "Treasurebox_SIP020_1",
        "Treasurebox_VIL005_1",
        "N3106_1ST_Treasure",
        "N3106_2ND_Treasure"
    ]
    global special_chest_to_room
    special_chest_to_room = {
        "PotionMaterial":               "m02VIL_005",
        "Qu07_Last":                    "m02VIL_003",
        "Swordsman":                    "m15JPN_016",
        "Treasurebox_PureMiriam_Hair":  "m01SIP_003",
        "Treasurebox_PureMiriam_Tiare": "m10BIG_011",
        "Treasurebox_PureMiriam_Dress": "m08TWR_019",
        "Treasurebox_PureMiriam_Sword": "m08TWR_016",
        "N3106_1ST_Treasure":           "m88BKR_004",
        "N3106_2ND_Treasure":           "m88BKR_004"
    }
    global important_checks
    important_checks = [
        "Qu07_Last",
        "Swordsman",
        "Treasurebox_LIB011_1",
        "Treasurebox_TWR019_1",
        "Treasurebox_TWR019_2",
        "Treasurebox_KNG021_1",
        "Treasurebox_JRN004_1"
    ]
    global important_check_ratio
    important_check_ratio = 4
    global key_order
    key_order = []
    global key_items
    key_items = [
        "Swordsman",
        "Silverbromide",
        "BreastplateofAguilar",
        "Keyofbacker1",
        "Keyofbacker2",
        "Keyofbacker3",
        "Keyofbacker4",
        "MonarchCrown"
    ]
    global key_shards
    key_shards = {
        "Doublejump":     4,
        "HighJump":       2,
        "Invert":         3,
        "Deepsinker":     2,
        "Dimensionshift": 1,
        "Reflectionray":  3,
        "Aquastream":     4,
        "Demoniccapture": 4,
        "Bloodsteel":     4
    }
    global key_item_to_location
    key_item_to_location = {}
    global key_shard_to_location
    key_shard_to_location = {}
    global all_keys
    all_keys = key_items + list(key_shards)
    global difficulty
    difficulty = "Normal"
    global current_available_doors
    current_available_doors = ["SIP_000_START"]
    global current_available_chests
    current_available_chests = []
    global current_available_enemies
    current_available_enemies = []
    global all_available_doors
    all_available_doors = copy.deepcopy(current_available_doors)
    global all_available_chests
    all_available_chests = []
    global all_available_enemies
    all_available_enemies = []
    global check_to_requirement
    check_to_requirement = {}
    global special_check_to_door
    special_check_to_door = {}
    global macro_to_requirements
    macro_to_requirements = {
        "Height": ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Flight": ["HighJump", "Invert", "Dimensionshift"],
        "Water":  ["Invert", "Deepsinker", "Aquastream"]
    }
    global enemy_to_room
    enemy_to_room = {}
    #Pool
    global chest_type
    chest_type = []
    global green_chest_type
    green_chest_type = []
    global blue_chest_type
    blue_chest_type = []
    global enemy_type
    enemy_type = []
    global quest_type
    quest_type = []
    global coin_type
    coin_type = [1, 5, 10, 50, 100, 500, 1000]
    global area_pools
    area_pools = {}
    #Shop
    global default_shop_event
    default_shop_event = "Event_01_001_0000"
    global boss_shop_events
    boss_shop_events = [
        "Event_02_001_0000", #Vepar
        "Event_06_001_0000", #Zangetsu
        "Event_08_002_0000", #Glutton Train
        "Event_09_005_0000", #Bathin
        "Event_10_001_0000", #Gebel
        "Event_11_001_0000", #Alfred
        "Event_13_001_0000", #Ultimate Zangetsu
        "Event_15_001_0000", #Gremory
        "Event_20_001_0000", #Valefar
        "Event_24_001_0000"  #Bloodless
    ]
    global enemy_skip_list
    enemy_skip_list = [
        "N2001",
        "N2013"
    ]
    global shop_skip_list
    shop_skip_list = [
        "Potion",
        "Ether",
        "Waystone",
	    "SeedCorn",
	    "SeedRice",
	    "SeedPotato",
        "8BitCoin",
        "16BitCoin",
        "32BitCoin"
    ]
    global price_skip_list
    price_skip_list = [
        "Potion",
        "Ether",
        "Waystone"
    ]
    Manager.mod_data["ItemDrop"]["Potion"]["ShopRatio"]      -= 3
    Manager.mod_data["ItemDrop"]["CookingMat"]["ShopRatio"]  -= 3
    Manager.mod_data["ItemDrop"]["StandardMat"]["ShopRatio"] -= 3
    global gun_list
    gun_list = [
        "Musketon",
        "Branderbus",
        "Tanegasima",
        "Trador",
        "Carvalin",
        "Betelgeuse",
        "Ursula",
        "Adrastea",
        "TrustMusket",
        "TrustMusket2",
        "TrustMusket3"
    ]
    global shard_type_to_hsv
    shard_type_to_hsv = {
        "Skill":       (  0,   0, 100),
        "Trigger":     (  0, 100, 100),
        "Effective":   (230, 100,  80),
        "Directional": (270, 100, 100),
        "Enchant":     ( 60, 100, 100),
        "Familia":     (120, 100,  80)
    }
    #Filling loot types
    for entry in Manager.mod_data["ItemDrop"]:
        for odd in range(Manager.mod_data["ItemDrop"][entry]["ChestRatio"]):
            chest_type.append(entry)
            if Manager.mod_data["ItemDrop"][entry]["ChestColor"] == "Green":
                green_chest_type.append(entry)
            if Manager.mod_data["ItemDrop"][entry]["ChestColor"] == "Blue":
                blue_chest_type.append(entry)
        for odd in range(Manager.mod_data["ItemDrop"][entry]["QuestRatio"]):
            quest_type.append(entry)
    enemy_type = list(Manager.mod_data["EnemyDrop"])

def set_logic_complexity(complexity):
    global logic_complexity
    logic_complexity = (complexity - 1)/2

def set_shop_event_wheight(wheight):
    global shop_event_wheight
    shop_event_wheight = 0.2 * wheight

def set_shop_price_wheight(wheight):
    global shop_price_wheight
    shop_price_wheight = Manager.wheight_exponents[wheight - 1]

def fill_enemy_to_room():
    #Gather a list of rooms per enemy
    for enemy in Manager.mod_data["EnemyInfo"]:
        enemy_to_room[enemy] = []
    for room in Manager.mod_data["RoomRequirement"]:
        for door in Manager.mod_data["RoomRequirement"][room]:
            for check in Manager.mod_data["RoomRequirement"][room][door]:
                if is_valid_enemy_check(check)[1]:
                    enemy_id = Utility.split_enemy_profile(check)[0]
                    if not room in enemy_to_room[enemy_id]:
                        enemy_to_room[enemy_id].append(room)

def enemy_shard_to_room(enemy):
    if enemy in ["N3090", "N3126"]:
        return enemy_to_room["N3090"] + enemy_to_room["N3126"]
    if enemy in ["N3015", "N3127"]:
        return enemy_to_room["N3015"] + enemy_to_room["N3127"]
    return enemy_to_room[enemy]

def set_hard_mode():
    global difficulty
    difficulty = "Hard"

def remove_infinite_items():
    #These specific gears grant the player an infinite source of something which generally ends up defining the meta and dominating runs
    #If the player is up for variety and challenge remove those from the pool so that they can never be found
    while "Gebelsglasses" in Manager.mod_data["ItemDrop"]["Accessory"]["ItemPool"]:
        Manager.mod_data["ItemDrop"]["Accessory"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in Manager.mod_data["ItemDrop"]["Headgear"]["ItemPool"]:
        Manager.mod_data["ItemDrop"]["Headgear"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"].remove("Recyclehat")

def add_starting_item(item):
    entry = "Start_" + item
    #Determine quantity based on item type
    quantity = None
    for string in ["Item", "Enemy"]:
        for data in Manager.mod_data[string + "Drop"]:
            if item in Manager.mod_data[string + "Drop"][data]["ItemPool"]:
                quantity = Manager.mod_data[string + "Drop"][data]["ItemHighQuantity"]
    if not quantity:
        if item == "Shortcut":
            quantity = 7
        else:
            quantity = 1
    Manager.datatable["PB_DT_DropRateMaster"][entry] = copy.deepcopy(Manager.datatable["PB_DT_DropRateMaster"]["Tresurebox_SAN000_01"])
    Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemId"]       = item
    Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemQuantity"] = quantity
    Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemRate"]     = 100.0
    Manager.add_global_room_pickup("m01SIP_000", entry)

def disable_shard_crafting():
    #If shards are randomized then disable the possiblity to manually craft shards so that they aren't always available
    #This is because there is currently no way to randomize which shards are craftable
    for entry in Manager.datatable["PB_DT_CraftMaster"]:
        if Manager.datatable["PB_DT_CraftMaster"][entry]["Type"] == "ECraftType::Craft" and Manager.datatable["PB_DT_CraftMaster"][entry]["CraftItemId"] in Manager.datatable["PB_DT_ShardMaster"]:
            Manager.datatable["PB_DT_CraftMaster"][entry]["OpenKeyRecipeID"] = "Medal019"

def satisfies_requirement(requirement):
    check = True
    for req in requirement:
        #AND
        if type(req) is list:
            for subreq in req:
                check = check_requirement(subreq)
                if not check:
                    break
            if check:
                break
        #OR  
        else:
            check = check_requirement(req)
            if check:
                break
    return check

def check_requirement(requirement):
    if requirement in macro_to_requirements:
        return satisfies_requirement(macro_to_requirements[requirement])
    else:
        return requirement in key_order

def key_logic():
    #Logic that adapts to any map layout
    while True:
        #Move through rooms
        for door in copy.deepcopy(current_available_doors):
            current_available_doors.remove(door)
            room = get_door_room(door)
            if room in Manager.mod_data["RoomRequirement"]:
                for check, requirement in Manager.mod_data["RoomRequirement"][room][door].items():
                    #Don't automatically unlock certain checks
                    if check in ["TO_BIG_000_START", "TO_JRN_000_START", "Qu07_Last", "N2012"]:
                        if check in special_check_to_door:
                            special_check_to_door[check].append(door)
                        else:
                            special_check_to_door[check] = [door]
                        continue
                    analyse_check(check, requirement)
            #Saves/warps/transitions
            else:
                for subdoor in Manager.map_connections[room]:
                    if subdoor == door:
                        continue
                    analyse_check(subdoor, [])
        #Keep going until stuck
        if current_available_doors:
            continue
        #Check special requirements
        if "TO_BIG_000_START" in special_check_to_door and den_portal_available():
            for door in special_check_to_door["TO_BIG_000_START"]:
                analyse_check("TO_BIG_000_START", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["TO_BIG_000_START"])
            del special_check_to_door["TO_BIG_000_START"]
        if "TO_JRN_000_START" in special_check_to_door and journey_area_available():
            for door in special_check_to_door["TO_JRN_000_START"]:
                analyse_check("TO_JRN_000_START", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["TO_JRN_000_START"])
            del special_check_to_door["TO_JRN_000_START"]
        if "Qu07_Last" in special_check_to_door and last_benjamin_available():
            for door in special_check_to_door["Qu07_Last"]:
                analyse_check("Qu07_Last", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["Qu07_Last"])
            del special_check_to_door["Qu07_Last"]
        if "N2012" in special_check_to_door and orlok_dracule_available():
            for door in special_check_to_door["N2012"]:
                analyse_check("N2012", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["N2012"])
            del special_check_to_door["N2012"]
        #Keep going until stuck
        if current_available_doors:
            continue
        #Place key item
        if check_to_requirement:
            #Wheight checks
            requirement_list_list = []
            for check in check_to_requirement:
                requirement_list = check_to_requirement[check]
                if not requirement_list in requirement_list_list:
                    requirement_list_list.append(requirement_list)
            chosen_requirement_list = random.choice(requirement_list_list)
            #Wheight requirements
            requirement_list = []
            for requirement in chosen_requirement_list:
                for num in range(get_requirement_wheight(requirement)):
                    requirement_list.append(requirement)
            chosen_requirement = random.choice(requirement_list)
            #Choose requirement and key item
            if type(chosen_requirement) is list:
                for item in chosen_requirement:
                    if item in macro_to_requirements:
                        chosen_item = random.choice(macro_to_requirements[item])
                    else:
                        chosen_item = item
                    if chosen_item in all_keys:
                        place_next_key(chosen_item)
            else:
                if chosen_requirement in macro_to_requirements:
                    chosen_item = random.choice(macro_to_requirements[chosen_requirement])
                else:
                    chosen_item = chosen_requirement
                place_next_key(chosen_item)
            current_available_chests.clear()
            current_available_enemies.clear()
            #Check which obstacles were lifted
            for check in list(check_to_requirement):
                if not check in check_to_requirement:
                    continue
                requirement = check_to_requirement[check]
                analyse_check(check, requirement)
        #Place last unecessary keys
        elif all_keys:
            place_next_key(random.choice(all_keys))
            current_available_chests.clear()
            current_available_enemies.clear()
        #Stop when all keys are placed and all doors are explored
        else:
            break

def analyse_check(check, requirement):
    #If accessible try to remove it from requirement list no matter what
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
        case CheckType.Chest:
            if check in all_available_chests:
                return
        case CheckType.Enemy:
            if not is_valid_enemy_check(check)[1]:
                return
            enemy_id = Utility.split_enemy_profile(check)[0]
            if enemy_id in all_available_enemies:
                return
    #Set check as available
    if accessible:
        match check_type:
            case CheckType.Door:
                all_available_doors.append(check)
                destination = get_door_destination(check)
                if destination:
                    current_available_doors.append(destination)
                    all_available_doors.append(destination)
                    if destination in check_to_requirement:
                        del check_to_requirement[destination]
            case CheckType.Chest:
                current_available_chests.append(check)
                all_available_chests.append(check)
            case CheckType.Enemy:
                current_available_enemies.append(enemy_id)
                all_available_enemies.append(enemy_id)
    #Add to requirement list
    else:
        if check in check_to_requirement:
            check_to_requirement[check].extend(requirement)
            check_to_requirement[check] = remove_duplicates(check_to_requirement[check])
        else:
            check_to_requirement[check] = requirement

def get_check_type(check):
    if check in used_chests:
        return CheckType.Chest
    if is_valid_enemy_check(check)[0]:
        return CheckType.Enemy
    return CheckType.Door

def is_valid_enemy_check(check):
    enemy_profile = Utility.split_enemy_profile(check)
    is_enemy = enemy_profile[0] in Manager.mod_data["EnemyInfo"]
    is_valid = is_enemy and (not enemy_profile[1] or enemy_profile[1] == difficulty)
    return (is_enemy, is_valid)

def get_requirement_wheight(requirement):
    if type(requirement) is list:
        return 1
    elif requirement in key_shards:
        return key_shards[requirement]
    else:
        return 4

def place_next_key(chosen_item):
    #Item
    if chosen_item in key_items:
        try:
            if random.random() < (1 - 1/(1+len(current_available_chests)))*logic_complexity:
                chosen_chest = pick_key_chest(current_available_chests)
            else:
                chosen_chest = pick_key_chest(all_available_chests)
        except IndexError:
            chosen_chest = pick_key_chest(all_available_chests)
        key_item_to_location[chosen_item] = chosen_chest
    #Shard
    if chosen_item in key_shards:
        try:
            if random.random() < (1 - 1/(1+len(current_available_enemies)))*logic_complexity:
                chosen_enemy = pick_key_enemy(current_available_enemies)
            else:
                chosen_enemy = pick_key_enemy(all_available_enemies)
        except IndexError:
            chosen_enemy = pick_key_enemy(all_available_enemies)
        key_shard_to_location[chosen_item] = chosen_enemy
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)

def pick_key_chest(available_chests):
    possible_chests = []
    for chest in available_chests:
        if not chest in list(key_item_to_location.values()) and not chest in keyless_chests:
            odds = 1
            #Increase odds of important checks
            if chest in important_checks:
                odds *= important_check_ratio
            for num in range(odds):
                possible_chests.append(chest)
    return random.choice(possible_chests)

def pick_key_enemy(available_enemies):
    #Giant dulla heads and Dullahammer EX share their drop with their early game counterpart
    available_enemies = ["N3090" if item == "N3126" else item for item in available_enemies]
    available_enemies = ["N3015" if item == "N3127" else item for item in available_enemies]
    possible_enemies = []
    for enemy in available_enemies:
        if not enemy in list(key_shard_to_location.values()) and not enemy in enemy_skip_list and Manager.mod_data["EnemyInfo"][enemy]["HasShard"]:
            #Increase odds the more uncommon the enemy
            odds = important_check_ratio - min(len(enemy_shard_to_room(enemy)), important_check_ratio) + 1
            for num in range(odds):
                possible_enemies.append(enemy)
    return random.choice(possible_enemies)

def get_door_destination(door):
    if door in Manager.map_doors:
        if Manager.map_connections[Manager.map_doors[door].room][door]:
            return Manager.map_connections[Manager.map_doors[door].room][door][0]
        else:
            return None
    elif door.split("_")[0] == "TO":
        short_door = door.split("_")
        short_door.pop(0)
        return "_".join(short_door)
    else:
        return None

def get_door_room(door):
    short_door = door.split("_")
    return room_to_area[short_door[0]] + "_".join([short_door[0], short_door[1]])

def den_portal_available():
    return "N1012" in all_available_enemies

def journey_area_available():
    return "BIG_000_START" in all_available_doors

def last_benjamin_available():
    return "VIL_004_1_0_RIGHT_BOTTOM" in all_available_doors and "ENT_015_0_0_LEFT" in all_available_doors and "UGD_049_0_0_LEFT" in all_available_doors and "Treasurebox_JPN002_1" in all_available_chests

def orlok_dracule_available():
    return "N1009_Enemy" in all_available_enemies

def final_boss_available():
    return "N1013_Bael" in all_available_enemies

def chest_to_room(chest):
    if chest in special_chest_to_room:
        return special_chest_to_room[chest]
    else:
        return room_to_area[chest.split("_")[1][:3]] + chest.split("_")[1][:3] + "_" + chest.split("_")[1][3:]

def randomize_overworld_keys():
    key_logic()
    #Key items
    for item in key_items:
        patch_key_item_entry(item, key_item_to_location[item])
    #Key shards
    for item in key_shards:
        patch_key_shard_entry(item, key_shard_to_location[item])

def randomize_overworld_shards():
    for entry in Manager.datatable["PB_DT_DropRateMaster"]:
        #Check if the entry should be skipped
        if "Treasure" in entry:
            continue
        enemy_id = entry.split("_")[0]
        if not enemy_id in Manager.mod_data["EnemyInfo"]:
            continue
        if not Manager.mod_data["EnemyInfo"][enemy_id]["HasShard"]:
            continue
        if enemy_id in enemy_skip_list:
            continue
        if enemy_id in list(key_shard_to_location.values()):
            continue
        #Reduce dulla head drop rate
        if enemy_id in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        #Assign shard
        if entry == enemy_id + "_Shard":
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardId"] = pick_and_remove(Manager.mod_data["ShardDrop"]["ItemPool"], True, "None")
            if Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        else:
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardId"]   = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardRate"]

def randomize_overworld_items():
    create_area_pools()
    #Start chest
    patch_start_chest_entry()
    #Skip Vepar chest
    used_chests.remove("Treasurebox_SIP020_1")
    #Johannes mats
    patch_chest_entry(random.choice(blue_chest_type), "PotionMaterial")
    #100% chest
    patch_chest_entry(random.choice(green_chest_type), "Treasurebox_VIL005_1")
    #8 bit nightmare chest
    patch_chest_entry(random.choice(green_chest_type), "Treasurebox_KNG021_1")
    #Final Benjamin reward
    patch_chest_entry(random.choice(green_chest_type), "Qu07_Last")
    #Ultimate Zangetsu reward
    patch_chest_entry(random.choice(green_chest_type), "Swordsman")
    #Carpenter's first chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_1ST_Treasure")
    #Carpenter's second chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_2ND_Treasure")
    #Journey's last chest
    patch_chest_entry(random.choice(green_chest_type), "Treasurebox_JRN004_1")
    #Upgrades
    #Don't put any upgrades in areas that extra character can't access
    for num in range(30):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxHPUP", chosen)
    for num in range(30):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxMPUP", chosen)
    for num in range(24):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxBulletUP", chosen)
    #Item pool
    chest_pool = copy.deepcopy(used_chests)
    random.shuffle(chest_pool)
    for chest in chest_pool:
        patch_chest_entry(random.choice(chest_type), chest)
    #Enemy pool
    for entry in Manager.datatable["PB_DT_DropRateMaster"]:
        if "Treasure" in entry:
            continue
        enemy_id = entry.split("_")[0]
        if not enemy_id in Manager.mod_data["EnemyInfo"]:
            continue
        if not Manager.mod_data["EnemyInfo"][enemy_id]["HasShard"]:
            continue
        if Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][entry]["RareIngredientRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonIngredientRate"] == 0.0:
            continue
        #Reduce dulla head drop rate
        if enemy_id in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        #Assign drops
        if entry == enemy_id + "_Shard":
            patch_enemy_entry(random.choice(enemy_type), drop_rate_multiplier, entry)
        else:
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemId"]               = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemQuantity"]         = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemRate"]             = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemRate"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonItemId"]             = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonItemQuantity"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonRate"]               = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonRate"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareIngredientId"]         = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareIngredientQuantity"]   = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareIngredientRate"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientRate"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonIngredientId"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonIngredientQuantity"] = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][entry]["CommonIngredientRate"]     = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientRate"]

def add_pre_vepar_waystone():
    Manager.datatable["PB_DT_DropRateMaster"]["Treasurebox_SIP020_1"]["RareItemId"] = "Waystone"

def create_area_pools():
    #Set up material pools per area for blue chests
    for room_prefix in room_to_area:
        area_id = room_to_area[room_prefix] + room_prefix
        area_pools[area_id] = {}
        for item_type in blue_chest_type:
            area_pools[area_id][item_type] = []
            for num in range(4):
                chosen = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
                while chosen in area_pools[area_id][item_type]:
                    chosen = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
                area_pools[area_id][item_type].append(chosen)

def empty_drop_entry(container):
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CoinType"] = "EDropCoin::None"
    Manager.datatable["PB_DT_DropRateMaster"][container]["CoinOverride"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][container]["CoinRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][container]["AreaChangeTreasureFlag"] = False

def patch_key_item_entry(item, container):
    empty_drop_entry(container)
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = item
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = 100.0
    used_chests.remove(container)
    
def patch_key_shard_entry(shard, enemy):
    #Assign a key shard to an entry
    #Unlike regular shards those will be more likely to drop but can only be dropped once
    if enemy in ["N3090", "N3099"]:
        drop_rate_multiplier = 0.5
    else:
        drop_rate_multiplier = 1.0
    for entry in Manager.datatable["PB_DT_DropRateMaster"]:
        if entry == enemy + "_Shard":
            Manager.datatable["PB_DT_DropRateMaster"][entry]["DropSpecialFlags"] = "EDropSpecialFlag::DropShardOnce"
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardId"] = shard
            if Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*3*drop_rate_multiplier
        elif entry.split("_")[0] == enemy:
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] = 0.0
    #If the key shard ends up in mutliple candles make them all disappear once one has been acquired
    if enemy == "Shortcut":
        for index in range(6):
            Manager.datatable["PB_DT_GimmickFlagMaster"]["ShortcutLantarn" + "{:03d}".format(index + 2)]["Id"] = Manager.datatable["PB_DT_GimmickFlagMaster"]["ShortcutLantarn001"]["Id"]
    if enemy == "FamiliaSilverKnight":
        for index in range(8):
            Manager.datatable["PB_DT_GimmickFlagMaster"]["FamilierLantarn" + "{:03d}".format(index + 2)]["Id"] = Manager.datatable["PB_DT_GimmickFlagMaster"]["FamilierLantarn001"]["Id"]

def patch_start_chest_entry():
    #Randomize the very first chest so that it is always a weapon
    container = "Treasurebox_SIP000_Tutorial"
    empty_drop_entry(container)
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["Weapon"]["ItemPool"], Manager.mod_data["ItemDrop"]["Weapon"]["IsUnique"], "Weapon")
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["ItemDrop"]["Weapon"]["ItemQuantity"]
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["ItemDrop"]["Weapon"]["ItemRate"]
    #Give extra bullets if the starting weapon is a gun
    if Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] in gun_list:
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["Bullet"]["ItemPool"], Manager.mod_data["ItemDrop"]["Bullet"]["IsUnique"], "Bullet")
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["ItemDrop"]["Bullet"]["ItemHighQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["ItemDrop"]["Bullet"]["ItemRate"]
    used_chests.remove(container)

def patch_chest_entry(item_type, container):
    #Randomize chest items based on item types
    if not container in used_chests:
        return
    empty_drop_entry(container)
    if Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Blue":
        area_id = chest_to_room(container)[:6]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]               = area_pools[area_id][item_type][0]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"]         = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]             = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]             = area_pools[area_id][item_type][1]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"]       = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]               = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]         = area_pools[area_id][item_type][2]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"]   = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]       = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = area_pools[area_id][item_type][3]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinOverride"]             = random.choice(coin_type)
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinType"]                 = "EDropCoin::D" + str(Manager.datatable["PB_DT_DropRateMaster"][container]["CoinOverride"])
        Manager.datatable["PB_DT_DropRateMaster"][container]["AreaChangeTreasureFlag"]   = True
    elif Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Red":
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinOverride"] = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinType"]     = "EDropCoin::D2000"
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinRate"]     = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    else:
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    used_chests.remove(container)
    
def patch_enemy_entry(item_type, item_rate, container):
    #Randomize enemy drops in a varied fashion while slightly favouring one item type
    #Also randomize the amount of drops so that it isn't always 4 per enemy
    empty_drop_entry(container)
    if item_type == "CookingMat":
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = pick_and_remove(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
    elif item_type == "StandardMat":
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = pick_and_remove(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
    elif item_type == "EnemyMat":
        if random.random() < 2/3 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = pick_and_remove(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = pick_and_remove(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.random() < 2/3 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = pick_and_remove(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate

def unlock_all_quests():
    #Make all quests available from the start
    #Note that picking a memento or catering quest commits you to that quest until you complete it
    for index in range(20):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["NeedBossID"]  = "None"
    for index in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(index + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(index + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(index + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(index + 1)]["NeedBossID"]  = "None"
    for index in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["NeedBossID"]  = "None"

def randomize_quest_requirements():
    #Enemy quests
    all_enemies = list(Manager.mod_data["EnemyInfo"])
    enemy_requirement = []
    for num in range(19):
        chosen = pick_and_remove(all_enemies, True, "None")
        #Don't pick IGA, Miriam, or shard candles
        while chosen in ["N2013", "N0000"] or chosen in Manager.datatable["PB_DT_ShardMaster"]:
            chosen = pick_and_remove(all_enemies, True, "None")
        enemy_requirement.append(chosen)
    #Order them by level, appending bosses at the end
    level_to_enemy = {}
    level_to_boss  = {}
    index = 0
    for enemy in enemy_requirement:
        if Manager.is_boss(enemy):
            level_to_boss[Manager.datatable["PB_DT_CharacterParameterMaster"][enemy]["DefaultEnemyLevel"]*100 + index] = enemy
        else:
            level_to_enemy[Manager.datatable["PB_DT_CharacterParameterMaster"][enemy]["DefaultEnemyLevel"]*100 + index] = enemy
        index += 1
    level_to_enemy = dict(sorted(level_to_enemy.items()))
    level_to_boss  = dict(sorted(level_to_boss.items()))
    level_to_enemy.update(level_to_boss)
    #Update requirement
    for index in range(19):
        enemy = list(level_to_enemy.values())[index]
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["Enemy01"] = enemy
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["EnemyNum01"] = len(enemy_to_room[enemy])
        enemy_room_string = ""
        for room in enemy_to_room[enemy]:
            if not Manager.datatable["PB_DT_RoomMaster"][room]["OutOfMap"]:
                enemy_room_string += room + ","
        if enemy_room_string:
            Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["EnemySpawnLocations"] = enemy_room_string[:-1]
        else:
            Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["EnemySpawnLocations"] = "none"
    #Memento quests
    for index in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(index + 1)]["Item01"] = pick_and_remove(Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"], True, "None")
    #Catering quests
    for index in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["Item01"] = pick_and_remove(Manager.mod_data["QuestRequirement"]["Catering"]["ItemPool"], True, "None")

def remove_enemy_quest_icons():
    #The icons for enemy quests are not dynamic with room placement so remove them for custom maps
    for index in range(20):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(index + 1)]["EnemySpawnLocations"] = "none"

def randomize_quest_rewards():
    #Randomize the rewards that quests give you
    #Quest rewards are meant to be higher tier than overworld items and come at greater quantities
    invert_ratio()
    for entry in Manager.datatable["PB_DT_QuestMaster"]:
        item_type = random.choice(quest_type)
        if Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Blue":
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardItem01"] = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemHighQuantity"]
        elif Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Red":
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardItem01"] = "Money"
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardNum01"] = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        else:
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardItem01"] = pick_and_remove(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
            Manager.datatable["PB_DT_QuestMaster"][entry]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemHighQuantity"]
    invert_ratio()

def update_catering_quest_info():
    #Update catering quests descriptions so that it is possible to tell what Susie wants
    for index in range(21):
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Name" + "{:02d}".format(index + 1)]    = Manager.translation["Item"][Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(index + 1)]["Item01"]]
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Caption" + "{:02d}".format(index + 1)] = "She says she wants to eat until she explodes."

def add_all_hair_apparents_in_shop():
    #Add all hair apparents to the shop for 100G
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["buyPrice"]  = 100
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["Producted"] = "Event_01_001_0000"
    shop_skip_list.append("Worldfashionfirstissue")
    price_skip_list.append("Worldfashionfirstissue")
    for index in range(11):
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(index + 2)]["buyPrice"]  = 100
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(index + 2)]["Producted"] = "Event_01_001_0000"
        shop_skip_list.append("WorldfashionNo" + "{:02d}".format(index + 2))
        price_skip_list.append("WorldfashionNo" + "{:02d}".format(index + 2))

def remove_all_keys_from_shop():
    #Remove all key items from shop
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["sellPrice"] = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["sellPrice"] = 0

def randomize_shop_items():
    #Reset shop event
    for entry in Manager.datatable["PB_DT_ItemMaster"]:
        if entry in shop_skip_list:
            continue
        Manager.datatable["PB_DT_ItemMaster"][entry]["Producted"] = "None"
    #Assign random events
    for entry in Manager.mod_data["ItemDrop"]:
        for num in range(Manager.mod_data["ItemDrop"][entry]["ShopRatio"]):
            if Manager.mod_data["ItemDrop"][entry]["ItemPool"]:
                chosen = pick_and_remove(Manager.mod_data["ItemDrop"][entry]["ItemPool"], True, "None")
                while Manager.datatable["PB_DT_ItemMaster"][chosen]["buyPrice"] == 0 or chosen in shop_skip_list:
                    chosen = pick_and_remove(Manager.mod_data["ItemDrop"][entry]["ItemPool"], True, "None")
                if random.random() < shop_event_wheight:
                    Manager.datatable["PB_DT_ItemMaster"][chosen]["Producted"] = random.choice(boss_shop_events)
                else:
                    Manager.datatable["PB_DT_ItemMaster"][chosen]["Producted"] = default_shop_event

def randomize_shop_prices(scale):
    for entry in Manager.datatable["PB_DT_ItemMaster"]:
        if Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"] == 0 or entry in price_skip_list:
            continue
        #Buy
        buy_price = Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"]
        sell_ratio = Manager.datatable["PB_DT_ItemMaster"][entry]["sellPrice"]/buy_price
        multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_wheight, False)
        Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = int(buy_price*multiplier)
        Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = max(Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"], 1)
        if Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"] > 10:
            Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = round(Manager.datatable["PB_DT_ItemMaster"][entry]["buyPrice"]/10)*10
        #Sell
        if not scale:
            multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_wheight, False)
        Manager.datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = int(buy_price*multiplier*sell_ratio)
        Manager.datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = max(Manager.datatable["PB_DT_ItemMaster"][entry]["sellPrice"], 1)

def replace_silver_bromide():
    #Find Silver Bromide and replace it by the Passplate
    for entry in Manager.datatable["PB_DT_DropRateMaster"]:
        if Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemId"] == "Silverbromide":
            Manager.datatable["PB_DT_DropRateMaster"][entry]["RareItemId"] = "Certificationboard"
    for entry in Manager.datatable["PB_DT_QuestMaster"]:
        if Manager.datatable["PB_DT_QuestMaster"][entry]["Item01"] == "Silverbromide":
            Manager.datatable["PB_DT_QuestMaster"][entry]["Item01"] = "Certificationboard"

def update_drop_ids():
    #Make sure that every id number in dropratemaster is unique
    used_ids = []
    for entry in Manager.datatable["PB_DT_DropRateMaster"]:
        drop_id = Manager.datatable["PB_DT_DropRateMaster"][entry]["Id"]
        while drop_id in used_ids:
            drop_id += 1
        used_ids.append(drop_id)
        Manager.datatable["PB_DT_DropRateMaster"][entry]["Id"] = drop_id

def update_container_types():
    for room in Manager.mod_data["RoomRequirement"]:
        Manager.update_room_containers(room)

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for file in Manager.file_to_path:
        if Manager.file_to_type[file] == Manager.FileType.Material:
            enemy_id = Manager.file_to_path[file].split("\\")[-2]
            if Manager.is_boss(enemy_id) or enemy_id == "N2008":
                shard_name = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
                shard_type = Manager.datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
                shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
                Manager.set_material_hsv(file, "ShardColor", shard_hsv)

def update_shard_candles():
    #While candle shards have entries in DropRateMaster they are completely ignored by the game
    #Instead those are read directly from the level files so they need to be updated to reflect the new shard drops
    for shard in ["Shortcut", "Deepsinker", "FamiliaSilverKnight", "Aquastream", "FamiliaIgniculus"]:
        for room in enemy_to_room[shard]:
            Manager.search_and_replace_string(room + "_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", "ShardID", shard, Manager.datatable["PB_DT_DropRateMaster"][shard + "_Shard"]["ShardId"])

def pick_and_remove(item_array, remove, item_type):
    #Function for picking and remove an item at random
    item = random.choice(item_array)
    if remove:
        if len(item_array) == 1:
            while item_type in chest_type:
                chest_type.remove(item_type)
            while item_type in blue_chest_type:
                blue_chest_type.remove(item_type)
            while item_type in green_chest_type:
                green_chest_type.remove(item_type)
            while item_type in enemy_type:
                enemy_type.remove(item_type)
            while item_type in quest_type:
                quest_type.remove(item_type)
        while item in item_array:
            item_array.remove(item)
    return item

def remove_duplicates(list):
    new_list = []
    for element in list:
        if not element in new_list:
            new_list.append(element)
    return new_list

def invert_ratio():
    #Complex function for inverting all item ratios in item drop dictionary
    for entry in Manager.mod_data["ItemDrop"]:
        if Manager.mod_data["ItemDrop"][entry]["IsUnique"]:
            continue
        ratio = []
        new_list = []
        duplicate = 1
        for index in range(len(Manager.mod_data["ItemDrop"][entry]["ItemPool"]) - 1):
            previous = Manager.mod_data["ItemDrop"][entry]["ItemPool"][index]
            current = Manager.mod_data["ItemDrop"][entry]["ItemPool"][index + 1]
            if current == previous:
                duplicate += 1
            else:
                ratio.append(duplicate)
                duplicate = 1
            if index == len(Manager.mod_data["ItemDrop"][entry]["ItemPool"]) - 2:
                ratio.append(duplicate)
            index += 1
        max_ratio = max(ratio)
        Manager.mod_data["ItemDrop"][entry]["ItemPool"] = list(dict.fromkeys(Manager.mod_data["ItemDrop"][entry]["ItemPool"]))
        for index in range(len(Manager.mod_data["ItemDrop"][entry]["ItemPool"])):
            for odd in range(abs(ratio[index] - (max_ratio + 1))):
                new_list.append(Manager.mod_data["ItemDrop"][entry]["ItemPool"][index])
        Manager.mod_data["ItemDrop"][entry]["ItemPool"] = new_list

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    name, extension = os.path.splitext(map)
    log = {}
    log["Seed"] = seed
    log["Map"]  = name.split("\\")[-1]
    log["Key"]  = {}
    for item in key_order:
        if item in key_items:
            log["Key"][Manager.translation["Item"][item]] = [chest_to_room(key_item_to_location[item])]
        if item in key_shards:
            log["Key"][Manager.translation["Shard"][item]] = enemy_shard_to_room(key_shard_to_location[item])
    log["Beatable"] = final_boss_available()
    return log

def create_log_string(seed, map, original_enemies):
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
    for item in key_order:
        if item in key_items:
            log_string += "  " + Manager.translation["Item"][item] + ": " + key_item_to_location[item]
        if item in key_shards:
            log_string += "  " + Manager.translation["Shard"][item] + ": " + Manager.translation["Enemy"][key_shard_to_location[item]]
            if key_shard_to_location[item] in original_enemies:
                log_string += " (over " + Manager.translation["Enemy"][original_enemies[key_shard_to_location[item]]] + ")"
        log_string += "\n"
    log_string += "Beatable: "
    if final_boss_available():
        log_string += "Yes"
    else:
        log_string += "No"
    return log_string