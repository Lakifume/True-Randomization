import Manager
import math
import random
import os
import copy
import json

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
    global keyless_chests
    keyless_chests = [
        "Qu07_Last",
        "Treasurebox_SIP000_Tutorial",
        "Treasurebox_SIP020_1",
        "Treasurebox_VIL005_1",
        "N3106_1ST_Treasure",
        "N3106_2ND_Treasure"
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
        "BKR": "m88"
    }
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
    global boss_rooms
    boss_rooms = [
        "m01SIP_022",
        "m05SAN_013",
        "m05SAN_023",
        "m06KNG_021",
        "m07LIB_011",
        "m08TWR_019",
        "m09TRN_002",
        "m10BIG_011",
        "m10BIG_015",
        "m12SND_026",
        "m13ARC_005",
        "m14TAR_004",
        "m15JPN_016",
        "m17RVA_008",
        "m18ICE_004",
        "m18ICE_018",
        "m19K2C_000",
        "m20JRN_003",
        "m20JRN_004",
        "m51EBT_000",
        "m88BKR_001",
        "m88BKR_002",
        "m88BKR_003",
        "m88BKR_004"
    ]
    global all_keys
    all_keys = []
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
    global difficulty
    difficulty = "Normal"
    global current_available_doors
    current_available_doors = ["SIP_000_START"]
    global current_available_chests
    current_available_chests = []
    global current_available_enemies
    current_available_enemies = []
    global all_available_doors
    all_available_doors = ["SIP_000_START"]
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
    global event_type
    event_type = [
        "Event_01_001_0000",
        "Event_01_001_0000",
        "Event_01_001_0000",
        "Event_01_001_0000",
        "Event_01_001_0000",
        "Event_01_001_0000",
        "Event_06_001_0000",
        "Event_08_002_0000",
        "Event_09_005_0000"
    ]
    global base
    base = []
    global ten
    ten = []
    global hundred
    hundred = []
    global thousand
    thousand = []
    global ten_thousand
    ten_thousand = []
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
    #Process variables
    for i in key_items:
        all_keys.append(i)
    for i in key_shards:
        all_keys.append(i)
    #Filling loot types
    for i in Manager.mod_data["ItemDrop"]:
        for e in range(Manager.mod_data["ItemDrop"][i]["ChestRatio"]):
            chest_type.append(i)
            if Manager.mod_data["ItemDrop"][i]["ChestColor"] == "Green":
                green_chest_type.append(i)
            if Manager.mod_data["ItemDrop"][i]["ChestColor"] == "Blue":
                blue_chest_type.append(i)
        for e in range(Manager.mod_data["ItemDrop"][i]["QuestRatio"]):
            quest_type.append(i)
    for i in Manager.mod_data["EnemyDrop"]:
        enemy_type.append(i)
    #Creating price lists
    i = 10
    while i <= 90:
        for e in range(10):
            base.append(i)
        i += 10
    i = 100
    while i <= 900:
        for e in range(10):
            base.append(i)
        i += 100
    i = 1000
    while i <= 9000:
        for e in range(10):
            base.append(i)
        i += 1000
    i = 10000
    while i <= 90000:
        for e in range(10):
            base.append(i)
        i += 10000
    i = 100000
    while i <= 900000:
        for e in range(10):
            base.append(i)
        i += 100000
    base.append(1000000)
    i = 0
    while i <= 90:
        ten.append(i)
        i += 10
    i = 0
    while i <= 900:
        hundred.append(i)
        i += 100
    i = 0
    while i <= 9000:
        thousand.append(i)
        i += 1000
    i = 0
    while i <= 90000:
        ten_thousand.append(i)
        i += 10000

def fill_enemy_to_room():
    for room in Manager.mod_data["RoomRequirement"]:
        for door in Manager.mod_data["RoomRequirement"][room]:
            for check in Manager.mod_data["RoomRequirement"][room][door]:
                is_valid_enemy = is_valid_enemy_check(check)
                if is_valid_enemy[1]:
                    if is_valid_enemy[0] in enemy_to_room:
                        enemy_to_room[is_valid_enemy[0]].append(room)
                    else:
                        enemy_to_room[is_valid_enemy[0]] = [room]
            break

def hard_logic():
    #room_req = {}
    #for i in Manager.mod_data["MapLogic"]:
    #    room_req[i] = {}
    #    struct = {}
    #    for e in Manager.map_connections[i]:
    #        struct[e] = []
    #    for e in used_chests:
    #        if chest_to_room(e) == i:
    #            struct[e] = []
    #            if e in chest_to_requirement:
    #                struct[e] = chest_to_requirement[e]
    #    for e in Manager.mod_data["EnemyLocation"]:
    #        if i in Manager.mod_data["EnemyLocation"][e]["NormalModeRooms"]:
    #            struct[e] = []
    #        elif i in Manager.mod_data["EnemyLocation"][e]["HardModeRooms"]:
    #            struct[e + "_Hard"] = []
    #    for e in Manager.map_connections[i]:
    #        struct2 = copy.deepcopy(struct)
    #        del struct2[e]
    #        room_req[i][e] = struct2
    #with open("RoomRequirement.json", "w", encoding="utf8") as file_writer:
    #    file_writer.write(json.dumps(room_req, ensure_ascii=False, indent=2))
    global difficulty
    difficulty = "Hard"

def remove_infinite():
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

def give_extra(item):
    entry = "Start_" + item
    #Determine quantity based on item type
    quantity = None
    for i in ["Item", "Enemy"]:
        for e in Manager.mod_data[i + "Drop"]:
            if item in Manager.mod_data[i + "Drop"][e]["ItemPool"]:
                quantity = Manager.mod_data[i + "Drop"][e]["ItemHighQuantity"]
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

def no_shard_craft():
    #If shards are randomized then disable the possiblity to manually craft shards so that they aren't always available
    #This is because there is currently no way to randomize which shards are craftable
    for i in Manager.datatable["PB_DT_CraftMaster"]:
        if Manager.datatable["PB_DT_CraftMaster"][i]["Type"] == "ECraftType::Craft" and Manager.datatable["PB_DT_CraftMaster"][i]["CraftItemId"] in Manager.datatable["PB_DT_ShardMaster"]:
            Manager.datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "Medal019"

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
    assessed_den_portal = False
    assessed_journey_area = False
    while all_keys:
        #Move through rooms
        for door in copy.deepcopy(current_available_doors):
            current_available_doors.remove(door)
            room = get_door_room(door)
            if room in Manager.mod_data["RoomRequirement"]:
                for check, requirement in Manager.mod_data["RoomRequirement"][get_door_room(door)][door].items():
                    #Don't automatically unlock certain checks
                    if check in ["TO_BIG_000_START", "TO_JRN_000_START"]:
                        if check in special_check_to_door:
                            special_check_to_door[check].append(door)
                        else:
                            special_check_to_door[check] = [door]
                        continue
                    analyse_check(check, requirement)
            else:
                for subdoor in Manager.map_connections[room]:
                    if subdoor == door:
                        continue
                    analyse_check(subdoor, [])
        #Keep going until stuck
        if current_available_doors:
            print(current_available_doors)
            continue
        #Check special requirements
        if den_portal_available() and not assessed_den_portal:
            assessed_den_portal = True
            for door in special_check_to_door["TO_BIG_000_START"]:
                analyse_check("TO_BIG_000_START", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["TO_BIG_000_START"])
        if journey_area_available() and not assessed_journey_area:
            assessed_journey_area = True
            for door in special_check_to_door["TO_JRN_000_START"]:
                analyse_check("TO_JRN_000_START", Manager.mod_data["RoomRequirement"][get_door_room(door)][door]["TO_JRN_000_START"])
        if current_available_doors:
            print(current_available_doors)
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
            #Choose requirement
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
                requirement = check_to_requirement[check]
                analyse_check(check, requirement)
        #Place last unecessary keys
        else:
            place_next_key(random.choice(all_keys))

def analyse_check(check, requirement):
    is_valid_enemy = is_valid_enemy_check(check)
    if is_valid_enemy[0] and not is_valid_enemy[1]:
        return
    accessible = satisfies_requirement(requirement)
    if accessible:
        #Chest
        if check in used_chests:
            if not check in all_available_chests:
                current_available_chests.append(check)
                all_available_chests.append(check)
        #Enemy
        elif is_valid_enemy[0]:
            if not is_valid_enemy[0] in all_available_enemies:
                current_available_enemies.append(is_valid_enemy[0])
                all_available_enemies.append(is_valid_enemy[0])
        #Door
        else:
            if not check in all_available_doors:
                all_available_doors.append(check)
                destination = get_door_destination(check)
                if destination and not destination in all_available_doors:
                    current_available_doors.append(destination)
                    all_available_doors.append(destination)
        if check in check_to_requirement:
            del check_to_requirement[check]
    else:
        if check in keyless_chests:
            return
        if check in check_to_requirement:
            check_to_requirement[check].extend(requirement)
            check_to_requirement[check] = remove_duplicates(check_to_requirement[check])
        else:
            check_to_requirement[check] = requirement

def is_valid_enemy_check(check):
    enemy_profile = Manager.split_enemy_profile(check)
    if enemy_profile[0] in Manager.mod_data["EnemyLocation"]:
        enemy_id = enemy_profile[0]
    else:
        enemy_id = None
    is_valid = enemy_id and (not enemy_profile[1] or enemy_profile[1] == difficulty)
    return (enemy_id, is_valid)

def get_requirement_wheight(requirement):
    if type(requirement) is list:
        return 1
    elif requirement in key_shards:
        return key_shards[requirement]
    else:
        return 4

def place_next_key(chosen_item):
    if chosen_item in key_items:
        try:
            chosen_chest = pick_key_chest(current_available_chests)
        except IndexError:
            chosen_chest = pick_key_chest(all_available_chests)
        key_item_to_location[chosen_item] = chosen_chest
    if chosen_item in key_shards:
        try:
            chosen_enemy = pick_key_enemy(current_available_enemies)random.randint(1, 99)
        except IndexError:
            chosen_enemy = pick_key_enemy(all_available_enemies)
        key_shard_to_location[chosen_item] = chosen_enemy
    print(chosen_item)
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)

def pick_key_chest(available_chests):
    possible_chests = []
    for chest in available_chests:
        if not chest in list(key_item_to_location.values()) and not chest in keyless_chests:
            possible_chests.append(chest)
    return random.choice(possible_chests)

def pick_key_enemy(available_enemies):
    possible_enemies = []
    for enemy in available_enemies:
        if not enemy in list(key_shard_to_location.values()) and not enemy in enemy_skip_list and Manager.mod_data["EnemyLocation"][enemy]["HasShard"]:
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
    return ("GDN_001_0_0_LEFT" in all_available_doors or "GDN_001_1_0_RIGHT" in all_available_doors) and "N1012" in all_available_enemies

def journey_area_available():
    return "SND_025_0_0_LEFT" in all_available_doors and "BIG_000_START" in all_available_doors

def chest_to_room(chest):
    if chest in special_chest_to_room:
        return special_chest_to_room[chest]
    else:
        return room_to_area[chest.split("_")[1][:3]] + chest.split("_")[1][:3] + "_" + chest.split("_")[1][3:]

def rand_overworld_key():
    key_logic()
    #Key items
    for i in key_items:
        patch_key_item_entry(i, key_item_to_location[i])
    #Key shards
    for i in key_shards:
        patch_key_shard_entry(i, key_shard_to_location[i])

def rand_overworld_shard():
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        #Check if the entry should be skipped
        if "Treasure" in i:
            continue
        enemy_id = i.split("_")[0]
        if not enemy_id in Manager.mod_data["EnemyLocation"]:
            continue
        if not Manager.mod_data["EnemyLocation"][enemy_id]["HasShard"]:
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
        if i == enemy_id + "_Shard":
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = any_pick(Manager.mod_data["ShardDrop"]["ItemPool"], True, "None")
            if Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        else:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"]   = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardRate"]

def rand_overworld_pool(waystone):
    create_area_pools()
    #Start chest
    patch_start_chest_entry()
    #Vepar chest
    if waystone:
        patch_key_item_entry("Waystone", "Treasurebox_SIP020_1")
    else:
        patch_key_item_entry("Potion", "Treasurebox_SIP020_1")
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
    for i in range(30):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxHPUP", chosen)
    for i in range(30):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxMPUP", chosen)
    for i in range(24):
        chosen = random.choice(used_chests)
        while "JRN" in chosen:
            chosen = random.choice(used_chests)
        patch_key_item_entry("MaxBulletUP", chosen)
    #Item pool
    chest_pool = copy.deepcopy(used_chests)
    random.shuffle(chest_pool)
    for i in chest_pool:
        patch_chest_entry(random.choice(chest_type), i)
    #Enemy pool
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        if "Treasure" in i:
            continue
        enemy_id = i.split("_")[0]
        if not enemy_id in Manager.mod_data["EnemyLocation"]:
            continue
        if not Manager.mod_data["EnemyLocation"][enemy_id]["HasShard"]:
            continue
        if Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["CommonRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] == 0.0:
            continue
        #Reduce dulla head drop rate
        if enemy_id in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        #Assign drops
        if i == enemy_id + "_Shard":
            patch_enemy_entry(random.choice(enemy_type), drop_rate_multiplier, i)
        else:
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"]               = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemQuantity"]         = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemRate"]             = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareItemRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonItemId"]             = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonItemQuantity"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonRate"]               = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientId"]         = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientQuantity"]   = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["RareIngredientRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientId"]       = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientQuantity"] = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"]     = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["CommonIngredientRate"]

def create_area_pools():
    #Set up material pools per area for blue chests
    for i in room_to_area:
        area_id = room_to_area[i] + i
        area_pools[area_id] = {}
        for e in blue_chest_type:
            area_pools[area_id][e] = []
            for o in range(4):
                chosen = any_pick(Manager.mod_data["ItemDrop"][e]["ItemPool"], Manager.mod_data["ItemDrop"][e]["IsUnique"], e)
                while chosen in area_pools[area_id][e]:
                    chosen = any_pick(Manager.mod_data["ItemDrop"][e]["ItemPool"], Manager.mod_data["ItemDrop"][e]["IsUnique"], e)
                area_pools[area_id][e].append(chosen)

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
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        if i == enemy + "_Shard":
            Manager.datatable["PB_DT_DropRateMaster"][i]["DropSpecialFlags"] = "EDropSpecialFlag::DropShardOnce"
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = shard
            if Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*3*drop_rate_multiplier
        elif i.split("_")[0] == enemy:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = 0.0
    #If the key shard ends up in mutliple candles make them all disappear once one has been acquired
    if enemy == "Shortcut":
        for i in range(6):
            Manager.datatable["PB_DT_GimmickFlagMaster"]["ShortcutLantarn" + "{:03d}".format(i + 2)]["Id"] = Manager.datatable["PB_DT_GimmickFlagMaster"]["ShortcutLantarn001"]["Id"]
    if enemy == "FamiliaSilverKnight":
        for i in range(8):
            Manager.datatable["PB_DT_GimmickFlagMaster"]["FamilierLantarn" + "{:03d}".format(i + 2)]["Id"] = Manager.datatable["PB_DT_GimmickFlagMaster"]["FamilierLantarn001"]["Id"]

def patch_start_chest_entry():
    #Randomize the very first chest so that it is always a weapon
    container = "Treasurebox_SIP000_Tutorial"
    empty_drop_entry(container)
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["Weapon"]["ItemPool"], Manager.mod_data["ItemDrop"]["Weapon"]["IsUnique"], "Weapon")
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["ItemDrop"]["Weapon"]["ItemQuantity"]
    Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["ItemDrop"]["Weapon"]["ItemRate"]
    #Give extra bullets if the starting weapon is a gun
    if Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] in gun_list:
        Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["Bullet"]["ItemPool"], Manager.mod_data["ItemDrop"]["Bullet"]["IsUnique"], "Bullet")
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
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinOverride"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinType"]     = "EDropCoin::D2000"
        Manager.datatable["PB_DT_DropRateMaster"][container]["CoinRate"]     = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    else:
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    used_chests.remove(container)
    
def patch_enemy_entry(item_type, item_rate, container):
    #Randomize enemy drops in a varied fashion while slightly favouring one item type
    #Also randomize the amount of drops so that it isn't always 4 per enemy
    empty_drop_entry(container)
    if item_type == "CookingMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
    elif item_type == "StandardMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
    elif item_type == "EnemyMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"]       = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"]       = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"]         = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"]       = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"]     = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"]       = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"]     = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate

def unlock_all_quest():
    #Make all quests available from the start
    #Note that picking a memento or catering quest commits you to that quest until you complete it
    for i in range(20):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedBossID"]  = "None"
    for i in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedBossID"]  = "None"
    for i in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedAreaID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedItemID"]  = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedBossID"]  = "None"

def rand_quest_requirement():
    #Enemy quests
    all_enemies = list(Manager.mod_data["EnemyLocation"])
    enemy_requirement = []
    for i in range(19):
        chosen = any_pick(all_enemies, True, "None")
        #Don't pick IGA, Miriam, or shard candles
        while chosen in ["N2013", "N0000"] or chosen in Manager.datatable["PB_DT_ShardMaster"]:
            chosen = any_pick(all_enemies, True, "None")
        enemy_requirement.append(chosen)
    #Order them by level, appending bosses at the end
    level_to_enemy = {}
    level_to_boss  = {}
    index = 0
    for i in enemy_requirement:
        if Manager.is_boss(i):
            level_to_boss[Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]*100 + index] = i
        else:
            level_to_enemy[Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]*100 + index] = i
        index += 1
    level_to_enemy = dict(sorted(level_to_enemy.items()))
    level_to_boss  = dict(sorted(level_to_boss.items()))
    level_to_enemy.update(level_to_boss)
    #Update requirement
    for i in range(19):
        enemy = list(level_to_enemy.values())[i]
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["Enemy01"] = enemy
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemyNum01"] = len(enemy_to_room[enemy])
        enemy_room = ""
        for e in enemy_to_room[enemy]:
            enemy_room += e + ","
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemySpawnLocations"] = enemy_room[:-1]
    #Memento quests
    for i in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["Item01"] = any_pick(Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"], True, "None")
    #Catering quests
    for i in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["Item01"] = any_pick(Manager.mod_data["QuestRequirement"]["Catering"]["ItemPool"], True, "None")

def no_enemy_quest_icon():
    #The icons for enemy quests are not dynamic with room placement so remove them for custom maps
    for i in range(20):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemySpawnLocations"] = "none"

def rand_quest_pool():
    #Randomize the rewards that quests give you
    #Quest rewards are meant to be higher tier than overworld items and come at greater quantities
    invert_ratio()
    for i in Manager.datatable["PB_DT_QuestMaster"]:
        item_type = random.choice(quest_type)
        if Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Blue":
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemHighQuantity"]
        elif Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Red":
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = "Money"
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        else:
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemHighQuantity"]
    invert_ratio()

def catering_quest_info():
    #Update catering quests descriptions so that it is possible to tell what Susie wants
    for i in range(21):
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Name" + "{:02d}".format(i + 1)]    = Manager.translation["Item"][Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["Item01"]]
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Caption" + "{:02d}".format(i + 1)] = "She says she wants to eat until she explodes."

def all_hair_in_shop():
    #Add all hair apparents to the shop for 100G
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["buyPrice"]  = 100
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["Producted"] = "Event_01_001_0000"
    shop_skip_list.append("Worldfashionfirstissue")
    price_skip_list.append("Worldfashionfirstissue")
    for i in range(11):
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(i + 2)]["buyPrice"]  = 100
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(i + 2)]["Producted"] = "Event_01_001_0000"
        shop_skip_list.append("WorldfashionNo" + "{:02d}".format(i + 2))
        price_skip_list.append("WorldfashionNo" + "{:02d}".format(i + 2))

def no_key_in_shop():
    #Remove all key items from shop
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["sellPrice"] = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["sellPrice"] = 0

def rand_shop_pool():
    #Reset shop event
    for i in Manager.datatable["PB_DT_ItemMaster"]:
        if i in shop_skip_list:
            continue
        Manager.datatable["PB_DT_ItemMaster"][i]["Producted"] = "None"
    #Assign random events
    for i in Manager.mod_data["ItemDrop"]:
        for e in range(Manager.mod_data["ItemDrop"][i]["ShopRatio"]):
            if Manager.mod_data["ItemDrop"][i]["ItemPool"]:
                chosen = any_pick(Manager.mod_data["ItemDrop"][i]["ItemPool"], True, "None")
                while Manager.datatable["PB_DT_ItemMaster"][chosen]["buyPrice"] == 0 or chosen in shop_skip_list:
                    chosen = any_pick(Manager.mod_data["ItemDrop"][i]["ItemPool"], True, "None")
                Manager.datatable["PB_DT_ItemMaster"][chosen]["Producted"] = random.choice(event_type)

def rand_shop_price(scale):
    price_range = Manager.create_weighted_list(100, 1, 10000, 1, 3)
    for i in Manager.datatable["PB_DT_ItemMaster"]:
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] == 0 or i in price_skip_list:
            continue
        #Buy
        buy_price = Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"]
        sell_ratio = Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"]/buy_price
        multiplier = random.choice(random.choice(price_range))/100
        Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = int(buy_price*multiplier)
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] > 10:
            Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = round(Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"]/10)*10
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] < 1:
            Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = 1
        #Sell
        if not scale:
            multiplier = random.choice(random.choice(price_range))/100
        Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] = int(buy_price*multiplier*sell_ratio)
        if Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] < 1:
            Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] = 1

def replace_silver_bromide():
    #Find Silver Bromide and replace it by the Passplate
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        if Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"] == "Silverbromide":
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"] = "Certificationboard"
    for i in Manager.datatable["PB_DT_QuestMaster"]:
        if Manager.datatable["PB_DT_QuestMaster"][i]["Item01"] == "Silverbromide":
            Manager.datatable["PB_DT_QuestMaster"][i]["Item01"] = "Certificationboard"

def update_drop_ids():
    #Make sure that every id number in dropratemaster is unique
    used_ids = []
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        drop_id = Manager.datatable["PB_DT_DropRateMaster"][i]["Id"]
        while drop_id in used_ids:
            drop_id += 1
        used_ids.append(drop_id)
        Manager.datatable["PB_DT_DropRateMaster"][i]["Id"] = drop_id

def update_container_types():
    for i in Manager.mod_data["MapLogic"]:
        Manager.update_room_containers(i)

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for i in Manager.file_to_path:
        if Manager.file_to_type[i] == "Material":
            enemy_id = Manager.file_to_path[i].split("\\")[-2]
            if Manager.is_boss(enemy_id) or enemy_id == "N2008":
                shard_name = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
                shard_type = Manager.datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
                shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
                Manager.change_material_hsv(i, "ShardColor", shard_hsv)

def update_shard_candles():
    #While candle shards have entries in DropRateMaster they are completely ignored by the game
    #Instead those are read directly from the level files so they need to be updated to reflect the new shard drops
    for i in ["Shortcut", "Deepsinker", "FamiliaSilverKnight", "Aquastream", "FamiliaIgniculus"]:
        for e in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
            Manager.search_and_replace_string(e + "_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", "ShardID", i, Manager.datatable["PB_DT_DropRateMaster"][i + "_Shard"]["ShardId"])

def any_pick(item_array, remove, item_type):
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
    for i in list:
        if not i in new_list:
            new_list.append(i)
    return new_list

def invert_ratio():
    #Complex function for inverting all item ratios in item drop dictionary
    for i in Manager.mod_data["ItemDrop"]:
        if Manager.mod_data["ItemDrop"][i]["IsUnique"]:
            continue
        ratio = []
        new_list = []
        duplicate = 1
        for e in range(len(Manager.mod_data["ItemDrop"][i]["ItemPool"]) - 1):
            previous = Manager.mod_data["ItemDrop"][i]["ItemPool"][e]
            current = Manager.mod_data["ItemDrop"][i]["ItemPool"][e + 1]
            if current == previous:
                duplicate += 1
            else:
                ratio.append(duplicate)
                duplicate = 1
            if e == len(Manager.mod_data["ItemDrop"][i]["ItemPool"]) - 2:
                ratio.append(duplicate)
            e += 1
        max_ratio = max(ratio)
        Manager.mod_data["ItemDrop"][i]["ItemPool"] = list(dict.fromkeys(Manager.mod_data["ItemDrop"][i]["ItemPool"]))
        for e in range(len(Manager.mod_data["ItemDrop"][i]["ItemPool"])):
            for o in range(abs(ratio[e] - (max_ratio + 1))):
                new_list.append(Manager.mod_data["ItemDrop"][i]["ItemPool"][e])
        Manager.mod_data["ItemDrop"][i]["ItemPool"] = new_list

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    name, extension = os.path.splitext(map)
    log = {}
    log["Seed"] = seed
    log["Map"]  = name.split("\\")[-1]
    log["Key"]  = {}
    for i in key_order:
        if i in key_items:
            log["Key"][Manager.translation["Item"][i]] = [chest_to_room(key_item_to_location[i])]
        if i in key_shards:
            log["Key"][Manager.translation["Shard"][i]] = enemy_to_room[key_shard_to_location[i]]
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
    for i in key_order:
        if i in key_items:
            log_string += "  " + Manager.translation["Item"][i] + ": " + key_item_to_location[i]
            log_string += "\n"
        if i in key_shards:
            log_string += "  " + Manager.translation["Shard"][i] + ": " + Manager.translation["Enemy"][key_shard_to_location[i]]
            if key_shard_to_location[i] in original_enemies:
                log_string += " (over " + Manager.translation["Enemy"][original_enemies[key_shard_to_location[i]]] + ")"
            log_string += "\n"
    return log_string