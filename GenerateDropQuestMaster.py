import json
import math
import random
import re
import os
import shutil
from random import randrange

chest_type = []
green_chest_type = []
blue_chest_type = []
enemy_type = []
quest_type = []

item_type_list = []

chest_index = []
enemy_index = []
quest_index = []

enemy_req_number = []
enemy_req_index = []

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

base = []
ten = []
hundred = []
thousand = []

coin = [1, 5, 10, 50, 100, 500, 1000]
odd = [1, 1, 0]

chest_skip_list = [
    "Treasurebox_SAN021(2)",
    "Treasurebox_KNG017(3)",
    "Treasurebox_TWR019(2)",
    "Treasurebox_TWR019(3)",
    "Treasurebox_BIG006(3)",
    "Treasurebox_ICE013(2)",
    "Wall_RVA011(2)"
]
chest_unused_list = [
    "Treasurebox_SIP014(3)",
    "Treasurebox_SIP021(2)",
    "Treasurebox_ENT008(2)",
    "Treasurebox_ENT011(3)",
    "Treasurebox_ENT012(2)",
    "Treasurebox_ENT015(2)",
    "Treasurebox_SAN000(2)",
    "Treasurebox_SAN000(3)",
    "Treasurebox_SAN005(4)",
    "Treasurebox_SAN005(5)",
    "Treasurebox_SAN009(4)",
    "Treasurebox_SAN015(2)",
    "Treasurebox_SAN017(3)",
    "Treasurebox_TWR000(3)",
    "Treasurebox_TWR000(4)",
    "Treasurebox_TWR006(3)",
    "Treasurebox_TWR013(3)",
    "Treasurebox_TWR015(2)",
    "Treasurebox_TWR019(4)",
    "Treasurebox_LIB001(3)",
    "Treasurebox_LIB013(2)",
    "Treasurebox_LIB018(2)",
    "Treasurebox_LIB041(2)",
    "Treasurebox_LIB042(2)",
    "Treasurebox_KNG005(2)",
    "Treasurebox_KNG018(2)",
    "Treasurebox_KNG020(2)",
    "Treasurebox_KNG021(3)",
    "Treasurebox_KNG021(4)",
    "Treasurebox_UGD002(2)",
    "Treasurebox_UGD008(2)",
    "Treasurebox_UGD012(2)",
    "Treasurebox_UGD013(2)",
    "Treasurebox_UGD013(3)",
    "Treasurebox_UGD014(2)",
    "Treasurebox_UGD015(2)",
    "Treasurebox_UGD016(2)",
    "Treasurebox_UGD017(2)",
    "Treasurebox_UGD018(2)",
    "Treasurebox_UGD019(2)",
    "Treasurebox_UGD020(2)",
    "Treasurebox_UGD022(2)",
    "Treasurebox_UGD023(2)",
    "Treasurebox_UGD026(2)",
    "Treasurebox_UGD028(2)",
    "Treasurebox_UGD029(2)",
    "Treasurebox_UGD032(2)",
    "Treasurebox_UGD033(2)",
    "Treasurebox_UGD034(2)",
    "Treasurebox_UGD035(2)",
    "Treasurebox_UGD037(2)",
    "Treasurebox_UGD039(2)",
    "Treasurebox_UGD043(2)",
    "Treasurebox_UGD045(2)",
    "Treasurebox_UGD047(2)",
    "Treasurebox_UGD048(3)",
    "Treasurebox_UGD049(2)",
    "Treasurebox_UGD055(2)",
    "Treasurebox_UGD057(2)",
    "Treasurebox_SND000(2)",
    "Treasurebox_SND001(2)",
    "Treasurebox_SND005(2)",
    "Treasurebox_SND007(2)",
    "Treasurebox_SND011(2)",
    "Treasurebox_SND012(2)",
    "Treasurebox_SND014(2)",
    "Treasurebox_SND021(2)",
    "Treasurebox_SND022(2)",
    "Treasurebox_SND023(2)",
    "Treasurebox_SND026(2)",
    "Treasurebox_SND027(2)",
    "Treasurebox_ARC001(2)",
    "Treasurebox_ARC005(2)",
    "Treasurebox_TAR000(2)",
    "Treasurebox_TAR003(2)",
    "Treasurebox_TAR004(2)",
    "Treasurebox_TAR005(2)",
    "Treasurebox_TAR008(2)",
    "Treasurebox_TAR009(2)",
    "Treasurebox_JPN000(2)",
    "Treasurebox_JPN001(2)",
    "Treasurebox_JPN003(2)",
    "Treasurebox_JPN003(3)",
    "Treasurebox_JPN006(2)",
    "Treasurebox_JPN007(2)",
    "Treasurebox_JPN008(2)",
    "Treasurebox_JPN011(2)",
    "Treasurebox_JPN012(2)",
    "Treasurebox_JPN014(2)",
    "Treasurebox_JPN016(2)",
    "Treasurebox_JPN019(2)",
    "Treasurebox_RVA000(2)",
    "Treasurebox_RVA003(2)",
    "Treasurebox_RVA003(3)",
    "Treasurebox_RVA005(2)",
    "Treasurebox_RVA005(3)",
    "Treasurebox_RVA007(2)",
    "Treasurebox_RVA008(2)",
    "Treasurebox_RVA009(2)",
    "Treasurebox_RVA013(2)",
    "Treasurebox_RVA014(2)",
    "Treasurebox_BRM_A_FIRST",
    "Treasurebox_BRM_B_FIRST",
    "Treasurebox_BRM_A",
    "Treasurebox_BRM_B",
    "Treasurebox_OfflineChaos_A",
    "Treasurebox_OfflineChaos_B",
    "Treasurebox_OnlineChaos_A",
    "Treasurebox_OnlineChaos_B"
]
room_unused_list = []
enemy_skip_list = [
    "N1003_Shard",
    "N2001_Shard",
    "N2013_Shard"
]
shop_skip_list = [
    "Waystone",
    "DiscountCard",
    "MonarchCrown"
]

log = []

#Content
with open("Data\\DropRateMaster\\Content\\PB_DT_DropRateMaster.json", "r") as file_reader:
    item_content = json.load(file_reader)

with open("Data\\QuestMaster\\Content\\PB_DT_QuestMaster.json", "r") as file_reader:
    quest_content = json.load(file_reader)

with open("Data\\ScenarioStringTable\\Content\\PBScenarioStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

with open("Data\\ItemMaster\\Content\\PB_DT_ItemMaster.json", "r") as file_reader:
    shop_content = json.load(file_reader)

#Data
with open("Data\\DropRateMaster\\Chest.json", "r") as file_reader:
    chest_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Enemy.json", "r") as file_reader:
    enemy_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Shard.json", "r") as file_reader:
    shard_data = json.load(file_reader)

with open("Data\\QuestMaster\\Requirements.json", "r") as file_reader:
    item_req_data = json.load(file_reader)

with open("Data\\QuestMaster\\EnemyLocationInfo.json", "r") as file_reader:
    enemy_req_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    item_translation = json.load(file_reader)

with open("Data\\CharacterParameterMaster\\Translation.json", "r") as file_reader:
    enemy_translation = json.load(file_reader)

with open("Data\\ShardMaster\\Color.json", "r") as file_reader:
    color = json.load(file_reader)

#FillingLootTypes
for i in chest_data:
    for e in range(i["Value"]["ChestRatio"]):
        chest_type.append(i["Key"])
        if i["Key"] != chest_data[11]["Key"]:
            item_type_list.append(i["Value"]["ChestName"])
        if i["Value"]["ChestColor"] == "EChestColor::Green":
            green_chest_type.append(i["Key"])
        if i["Value"]["ChestColor"] == "EChestColor::Blue":
            blue_chest_type.append(i["Key"])
    for e in range(i["Value"]["QuestRatio"]):
        quest_type.append(i["Key"])
for i in enemy_data:
    enemy_type.append(i["Key"])

#CollectingChestIndexes
i = 37
while i <= 499:
    if item_content[i]["Key"] in chest_skip_list or item_content[i]["Value"]["ItemType"] == "EItemType::Upgrade":
        i += 1
        continue
    chest_index.append(i)
    i += 1
random.shuffle(chest_index)

#CollectingEnemyIndexes
i = 513
while i <= 626:
    if item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Value"]["ShardRate"] == 100.0:
        i += 1
        continue
    enemy_index.append(i)
    i += 1
random.shuffle(enemy_index)

#CollectingQuestIndexes

for i in range(len(quest_content)):
    quest_index.append(i)
random.shuffle(quest_index)

#CreatingPriceList
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
base.append(100000)
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

#CollectingZeroPrices
for i in shop_content:
    if i["Value"]["buyPrice"] == 0:
        shop_skip_list.append(i["Key"])

#PreparingLog
log_data = {}
log_data["Key"] = "ChestPool"
log_data["Value"] = {}
for i in chest_data:
    log_data["Value"][i["Key"]] = []
log.append(log_data)
log_data = {}
log_data["Key"] = "EnemyPool"
log_data["Value"] = {}
for i in enemy_data:
    log_data["Value"][i["Key"]] = []
log.append(log_data)
log_data = {}
log_data["Key"] = "QuestPool"
log_data["Value"] = {}
for i in chest_data:
    log_data["Value"][i["Key"]] = []
log.append(log_data)
log_data = {}
log_data["Key"] = "ShopPool"
log_data["Value"] = {}
for i in chest_data:
    log_data["Value"][i["Key"]] = []
log.append(log_data)
log_data = {}
log_data["Key"] = "ShardPool"
log_data["Value"] = {}
log_data["Value"]["Red"] = []
log_data["Value"]["Blue"] = []
log_data["Value"]["Purple"] = []
log_data["Value"]["Yellow"] = []
log_data["Value"]["Green"] = []
log_data["Value"]["White"] = []
log.append(log_data)

def map_check(path):
    with open(path, "r") as file_reader:
        map_content = json.load(file_reader)
    for i in map_content:
        if not i["Value"]["AdjacentRoomName"] and not i["Key"] == "m09TRN_002" and not i["Value"]["OutOfMap"]:
            room_unused_list.append(i["Key"][3:].replace("_", ""))
    for i in chest_index:
        for e in room_unused_list:
            if e in item_content[i]["Key"]:
                item_content[i]["Value"]["RareItemId"] = "Medal019"
                item_content[i]["Value"]["RareItemQuantity"] = 1
                item_content[i]["Value"]["RareItemRate"] = 100
                item_content[i]["Value"]["CommonItemId"] = "None"
                item_content[i]["Value"]["CommonItemQuantity"] = 0
                item_content[i]["Value"]["CommonRate"] = 0.0
                item_content[i]["Value"]["RareIngredientId"] = "None"
                item_content[i]["Value"]["RareIngredientQuantity"] = 0
                item_content[i]["Value"]["RareIngredientRate"] = 0.0
                item_content[i]["Value"]["CommonIngredientId"] = "None"
                item_content[i]["Value"]["CommonIngredientQuantity"] = 0
                item_content[i]["Value"]["CommonIngredientRate"] = 0.0
                item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
                item_content[i]["Value"]["CoinOverride"] = 0
                item_content[i]["Value"]["CoinRate"] = 0.0
                item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
                item_content[i]["Value"]["ItemType"] = "EItemType::Unused"

def completion_chest_check():
    item_content[69]["Value"]["RareItemId"] = "Medal019"
    item_content[69]["Value"]["ItemType"] = "EItemType::Unused"

def remove_infinite():
    while "Gebelsglasses" in chest_data[0]["Value"]["ItemPool"]:
        chest_data[0]["Value"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in item_req_data[0]["Value"]["ItemPool"]:
        item_req_data[0]["Value"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in chest_data[6]["Value"]["ItemPool"]:
        chest_data[6]["Value"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in item_req_data[0]["Value"]["ItemPool"]:
        item_req_data[0]["Value"]["ItemPool"].remove("Recyclehat")

def give_shortcut():
    item_content[6]["Value"]["RareItemId"] = "Shortcut"
    item_content[6]["Value"]["RareItemQuantity"] = 7
    item_content[6]["Value"]["RareItemRate"] = 100.0

def give_eye():
    item_content[6]["Value"]["CommonItemId"] = "SkilledDetectiveeye"
    item_content[6]["Value"]["CommonItemQuantity"] = 1
    item_content[6]["Value"]["CommonRate"] = 100.0

def give_map_help(item):
    item_content[6]["Value"]["RareIngredientId"] = item
    item_content[6]["Value"]["RareIngredientQuantity"] = 1
    item_content[6]["Value"]["RareIngredientRate"] = 100.0

def chaos_key():
    item_content[11]["Value"]["ItemType"] = chest_data[11]["Value"]["ChestName"]
    item_content[157]["Value"]["ItemType"] = random.choice(item_type_list)
    item_content[194]["Value"]["ItemType"] = random.choice(item_type_list)
    item_content[195]["Value"]["ItemType"] = random.choice(item_type_list)
    item_content[234]["Value"]["ItemType"] = random.choice(item_type_list)
    item_content[418]["Value"]["ItemType"] = random.choice(item_type_list)
    item_content[445]["Value"]["ItemType"] = random.choice(item_type_list)

def chaos_shard():
    i = 500
    while i <= 626:
        if item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Key"] in enemy_skip_list:
            i += 1
            continue
        if item_content[i]["Key"].split("_")[0] == item_content[i-1]["Key"].split("_")[0]:
            item_content[i]["Value"]["ShardId"] = item_content[i-1]["Value"]["ShardId"]
        else:
            item_content[i]["Value"]["ShardId"] = any_pick(shard_data["Value"]["ItemPool"], True, "None")
        i += 1

def rand_item_pool():
    #JohannesMats
    patch_chest_entry(random.choice(blue_chest_type), 7)
    #FinalReward
    patch_chest_entry(random.choice(green_chest_type), 10)
    #StartChest
    patch_chest_entry(chest_data[11]["Key"], 36)
    #ItemPool
    for i in chest_index:
        #UnusedCheck
        if item_content[i]["Value"]["ItemType"] == "EItemType::Unused":
            continue
        #Patch
        patch_chest_entry(random.choice(chest_type), i)
    #VolcanoWallFix
    patch_chest_entry(chest_data[3]["Key"], 493)
    #EnemyPool
    for i in enemy_index:
        #DullaHeadCheck
        if item_content[i]["Key"].split("_")[0] == "N3090" or item_content[i]["Key"].split("_")[0] == "N3099":
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateLow"])
        elif item_content[i]["Value"]["ShardRate"] != 100.0:
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateNormal"])
        #DullaHeadCheck
        if item_content[i]["Key"].split("_")[0] == "N3090" or item_content[i]["Key"].split("_")[0] == "N3099":
            patch_enemy_entry(random.choice(enemy_type), "ItemRateLow", i)
        elif item_content[i]["Key"].split("_")[0] != item_content[i-1]["Key"].split("_")[0]:
            patch_enemy_entry(random.choice(enemy_type), "ItemRateNormal", i)
    #DuplicateCheck
    for i in enemy_index:
        if item_content[i]["Key"].split("_")[0] == item_content[i-1]["Key"].split("_")[0]:
            item_content[i]["Value"]["RareItemId"] = item_content[i-1]["Value"]["RareItemId"]
            item_content[i]["Value"]["RareItemQuantity"] = item_content[i-1]["Value"]["RareItemQuantity"]
            item_content[i]["Value"]["RareItemRate"] = item_content[i-1]["Value"]["RareItemRate"]
            item_content[i]["Value"]["CommonItemId"] = item_content[i-1]["Value"]["CommonItemId"]
            item_content[i]["Value"]["CommonItemQuantity"] = item_content[i-1]["Value"]["CommonItemQuantity"]
            item_content[i]["Value"]["CommonRate"] = item_content[i-1]["Value"]["CommonRate"]
            item_content[i]["Value"]["RareIngredientId"] = item_content[i-1]["Value"]["RareIngredientId"]
            item_content[i]["Value"]["RareIngredientQuantity"] = item_content[i-1]["Value"]["RareIngredientQuantity"]
            item_content[i]["Value"]["RareIngredientRate"] = item_content[i-1]["Value"]["RareIngredientRate"]
            item_content[i]["Value"]["CommonIngredientId"] = item_content[i-1]["Value"]["CommonIngredientId"]
            item_content[i]["Value"]["CommonIngredientQuantity"] = item_content[i-1]["Value"]["CommonIngredientQuantity"]
            item_content[i]["Value"]["CommonIngredientRate"] = item_content[i-1]["Value"]["CommonIngredientRate"]
            item_content[i]["Value"]["ItemType"] = item_content[i-1]["Value"]["ItemType"]
    #CarpenterChest1
    patch_chest_entry(random.choice(green_chest_type), 621)
    #CarpenterChest2
    patch_chest_entry(random.choice(green_chest_type), 622)
    #ShardColor
    i = 500
    while i <= 630:
        if item_content[i]["Key"].split("_")[0] == item_content[i-1]["Key"].split("_")[0] or item_content[i]["Value"]["ShardRate"] == 0.0:
            i += 1
            continue
        log[4]["Value"][color["Value"][item_content[i]["Value"]["ShardId"]].split("::")[-1]].append(enemy_translation["Value"][item_content[i]["Key"].split("_")[0]])
        i += 1

def patch_chest_entry(item_type, i):
    if item_type == chest_data[0]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[0]["Value"]["ItemPool"], chest_data[0]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[0]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[0]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[0]["Value"]["ChestName"]
        if chest_data[0]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[1]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[1]["Value"]["ItemPool"], chest_data[1]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[1]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[1]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[1]["Value"]["ChestName"]
        if chest_data[1]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[2]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[2]["Value"]["ItemPool"], chest_data[2]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[2]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[2]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[2]["Value"]["ChestName"]
        if chest_data[2]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[3]["Key"]:
        item_content[i]["Value"]["RareItemId"] = "None"
        item_content[i]["Value"]["RareItemQuantity"] = 0
        item_content[i]["Value"]["RareItemRate"] = 0.0
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinOverride"] = any_pick(chest_data[3]["Value"]["ItemPool"], chest_data[3]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["CoinType"] = "EDropCoin::D2000"
        item_content[i]["Value"]["CoinRate"] = random.choice(chest_data[3]["Value"]["ItemRate"])
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[3]["Value"]["ChestName"]
        if chest_data[3]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_content[i]["Value"]["CoinOverride"])
    elif item_type == chest_data[4]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[4]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[4]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonItemQuantity"] = random.choice(chest_data[4]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonRate"] = random.choice(chest_data[4]["Value"]["ItemRate"])
        item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(chest_data[4]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareIngredientRate"] = random.choice(chest_data[4]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(chest_data[4]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonIngredientRate"] = random.choice(chest_data[4]["Value"]["ItemRate"])
        item_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        item_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(item_content[i]["Value"]["CoinOverride"])
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = True
        item_content[i]["Value"]["ItemType"] = chest_data[4]["Value"]["ChestName"]
        if chest_data[4]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["CommonItemId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
    elif item_type == chest_data[5]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[5]["Value"]["ItemPool"], chest_data[5]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[5]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[5]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[5]["Value"]["ChestName"]
        if chest_data[5]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[6]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[6]["Value"]["ItemPool"], chest_data[6]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[6]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[6]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[6]["Value"]["ChestName"]
        if chest_data[6]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[7]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[7]["Value"]["ItemPool"], chest_data[7]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[7]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[7]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[7]["Value"]["ChestName"]
        if chest_data[7]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[8]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[8]["Value"]["ItemPool"], chest_data[8]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[8]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[8]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[8]["Value"]["ChestName"]
        if chest_data[8]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[9]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[9]["Value"]["ItemPool"], chest_data[9]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[9]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[9]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[9]["Value"]["ChestName"]
        if chest_data[9]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    elif item_type == chest_data[10]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[10]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[10]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonItemQuantity"] = random.choice(chest_data[10]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonRate"] = random.choice(chest_data[10]["Value"]["ItemRate"])
        item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(chest_data[10]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareIngredientRate"] = random.choice(chest_data[10]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(chest_data[10]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonIngredientRate"] = random.choice(chest_data[10]["Value"]["ItemRate"])
        item_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        item_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(item_content[i]["Value"]["CoinOverride"])
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = True
        item_content[i]["Value"]["ItemType"] = chest_data[10]["Value"]["ChestName"]
        if chest_data[10]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["CommonItemId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
    elif item_type == chest_data[11]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[11]["Value"]["ItemPool"], chest_data[11]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[11]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[11]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = "None"
        item_content[i]["Value"]["CommonItemQuantity"] = 0
        item_content[i]["Value"]["CommonRate"] = 0.0
        item_content[i]["Value"]["RareIngredientId"] = "None"
        item_content[i]["Value"]["RareIngredientQuantity"] = 0
        item_content[i]["Value"]["RareIngredientRate"] = 0.0
        item_content[i]["Value"]["CommonIngredientId"] = "None"
        item_content[i]["Value"]["CommonIngredientQuantity"] = 0
        item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        item_content[i]["Value"]["CoinOverride"] = 0
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = False
        item_content[i]["Value"]["ItemType"] = chest_data[11]["Value"]["ChestName"]
        if chest_data[11]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
    
def patch_enemy_entry(item_type, item_rate, i):
    if item_type == enemy_data[0]["Key"]:
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[0]["Value"][item_rate])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[1]["Value"][item_rate])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[2]["Value"][item_rate])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[0]["Value"][item_rate])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = enemy_data[0]["Value"]["ChestName"]
    elif item_type == enemy_data[1]["Key"]:
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[1]["Value"][item_rate])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[2]["Value"][item_rate])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[0]["Value"][item_rate])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[1]["Value"][item_rate])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = enemy_data[1]["Value"]["ChestName"]
    elif item_type == enemy_data[2]["Key"]:
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[2]["Value"][item_rate])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[0]["Value"][item_rate])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[1]["Value"][item_rate])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[2]["Value"][item_rate])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(item_translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = enemy_data[2]["Value"]["ChestName"]
    
def all_quest():
    for i in range(56):
        quest_content[i]["Value"]["NeedQuestID"] = "None"
        quest_content[i]["Value"]["NeedAreaID"] = "None"
        quest_content[i]["Value"]["NeedItemID"] = "None"
        quest_content[i]["Value"]["NeedBossID"] = "None"

def quest_req(hard, custom_map):
    #EnemyQuests
    i = 0
    while i < len(enemy_req_data):
        enemy_req_number.append(i)
        i += 1
    for i in range(20):
        enemy_req_index.append(any_pick(enemy_req_number, True, "None"))
    enemy_req_index.sort()
    enemy_req_index.pop()
    enemy_req_index.append(len(enemy_req_data)-1)
    for i in range(20):
        quest_content[i]["Value"]["Enemy01"] = enemy_req_data[enemy_req_index[i]]["Key"]
        quest_content[i]["Value"]["EnemyNum01"] = len(enemy_req_data[enemy_req_index[i]]["Value"]["NormalModeRooms"])
        if hard:
            quest_content[i]["Value"]["EnemyNum01"] += len(enemy_req_data[enemy_req_index[i]]["Value"]["HardModeRooms"])
        enemy_room = ""
        for e in enemy_req_data[enemy_req_index[i]]["Value"]["NormalModeRooms"]:
            enemy_room += e + ","
        if hard:
            for e in enemy_req_data[enemy_req_index[i]]["Value"]["HardModeRooms"]:
                enemy_room += e + ","
        quest_content[i]["Value"]["EnemySpawnLocations"] = enemy_room[:-1]
    #Memento Quests
    i = 20
    while i <= 34:
        quest_content[i]["Value"]["Item01"] = any_pick(item_req_data[0]["Value"]["ItemPool"], True, "None")
        i += 1
    #Catering Quests
    i = 35
    while i <= 55:
        quest_content[i]["Value"]["Item01"] = any_pick(item_req_data[1]["Value"]["ItemPool"], True, "None")
        i += 1

def no_quest_icon():
    for i in range(20):
        quest_content[i]["Value"]["EnemySpawnLocations"] = "none"

def rand_quest_pool():
    invert_ratio()
    for i in quest_index:
        item_type = random.choice(quest_type)
        if item_type == chest_data[0]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[0]["Value"]["ItemPool"], chest_data[0]["Value"]["IsUnique"], item_type)
            if chest_data[0]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[0]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[1]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[1]["Value"]["ItemPool"], chest_data[1]["Value"]["IsUnique"], item_type)
            if chest_data[1]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[1]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[2]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[2]["Value"]["ItemPool"], chest_data[2]["Value"]["IsUnique"], item_type)
            if chest_data[2]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[2]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[3]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = "Money"
            quest_content[i]["Value"]["RewardNum01"] = any_pick(chest_data[3]["Value"]["ItemPool"], chest_data[3]["Value"]["IsUnique"], item_type)
        elif item_type == chest_data[4]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[4]["Value"]["ItemPool"], chest_data[4]["Value"]["IsUnique"], item_type)
            if chest_data[4]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[4]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[5]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[5]["Value"]["ItemPool"], chest_data[5]["Value"]["IsUnique"], item_type)
            if chest_data[5]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[5]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[6]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[6]["Value"]["ItemPool"], chest_data[6]["Value"]["IsUnique"], item_type)
            if chest_data[6]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[6]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[7]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[7]["Value"]["ItemPool"], chest_data[7]["Value"]["IsUnique"], item_type)
            if chest_data[7]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[7]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[8]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[8]["Value"]["ItemPool"], chest_data[8]["Value"]["IsUnique"], item_type)
            if chest_data[8]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[8]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[9]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[9]["Value"]["ItemPool"], chest_data[9]["Value"]["IsUnique"], item_type)
            if chest_data[9]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[9]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[10]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[10]["Value"]["ItemPool"], chest_data[10]["Value"]["IsUnique"], item_type)
            if chest_data[10]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[10]["Value"]["ItemQuantity"]) * 3
        elif item_type == chest_data[11]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[11]["Value"]["ItemPool"], chest_data[11]["Value"]["IsUnique"], item_type)
            if chest_data[11]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[11]["Value"]["ItemQuantity"]) * 3
        log[2]["Value"][item_type].append(item_translation["Value"][quest_content[i]["Value"]["RewardItem01"]])

def req_string():
    string_content["Table"]["QST_Catering_Name01"] = item_translation["Value"][quest_content[35]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name02"] = item_translation["Value"][quest_content[50]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name03"] = item_translation["Value"][quest_content[51]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name04"] = item_translation["Value"][quest_content[42]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name05"] = item_translation["Value"][quest_content[41]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name06"] = item_translation["Value"][quest_content[39]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name07"] = item_translation["Value"][quest_content[44]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name08"] = item_translation["Value"][quest_content[38]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name09"] = item_translation["Value"][quest_content[52]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name10"] = item_translation["Value"][quest_content[45]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name11"] = item_translation["Value"][quest_content[40]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name12"] = item_translation["Value"][quest_content[49]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name13"] = item_translation["Value"][quest_content[46]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name14"] = item_translation["Value"][quest_content[37]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name15"] = item_translation["Value"][quest_content[53]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name16"] = item_translation["Value"][quest_content[47]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name17"] = item_translation["Value"][quest_content[36]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name18"] = item_translation["Value"][quest_content[54]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name19"] = item_translation["Value"][quest_content[43]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name20"] = item_translation["Value"][quest_content[48]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name21"] = item_translation["Value"][quest_content[55]["Value"]["Item01"]]

def hair_app_shop():
    i = 521
    while i <= 532:
        shop_content[i]["Value"]["buyPrice"] = 100
        shop_content[i]["Value"]["Producted"] = "Event_01_001_0000"
        i += 1

def no_card():
    shop_content[561]["Value"]["buyPrice"] = 0
    shop_content[561]["Value"]["sellPrice"] = 0

def rand_shop_pool():
    invert_ratio()
    for i in chest_data:
        for e in shop_skip_list:
            while e in i["Value"]["ItemPool"]:
                i["Value"]["ItemPool"].remove(e)
        events = []
        for e in range(i["Value"]["ShopRatio"]):
            events.append(random.choice(event_type))
        chosen = []
        for e in range(len(events)):
            if i["Value"]["ItemPool"]:
                chosen.append(any_pick(i["Value"]["ItemPool"], True, "None"))
        for e in shop_content:
            if e["Key"] in shop_skip_list:
                continue
            if e["Key"] in chosen:
                e["Value"]["Producted"] = random.choice(events)
                events.remove(e["Value"]["Producted"])
            elif e["Value"]["ItemType"] == i["Value"]["ShopName"]:
                e["Value"]["Producted"] = "None"
        for e in chosen:
            log[3]["Value"][i["Key"]].append(item_translation["Value"][e])

def rand_shop_price(scale):
    for i in shop_content:
        if i["Key"] in shop_skip_list:
            continue
        chosen = random.choice(base)
        if chosen != 100000:
            if chosen >= 100:
                chosen += random.choice(ten)
            if chosen >= 1000:
                chosen += random.choice(hundred)
            if chosen >= 10000:
                chosen += random.choice(thousand)
        i["Value"]["buyPrice"] = chosen
        if not scale:
            chosen = random.choice(base)
            if chosen != 100000:
                if chosen >= 100:
                    chosen += random.choice(ten)
                if chosen >= 1000:
                    chosen += random.choice(hundred)
                if chosen >= 10000:
                    chosen += random.choice(thousand)
        i["Value"]["sellPrice"] = round(chosen/10)

def any_pick(item_array, remove, item_type):
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

def invert_ratio():
    for i in chest_data:
        if i["Value"]["IsUnique"]:
            continue
        ratio = []
        new_list = []
        duplicate = 1
        for e in range(len(i["Value"]["ItemPool"]) - 1):
            previous = i["Value"]["ItemPool"][e]
            current = i["Value"]["ItemPool"][e + 1]
            if current == previous:
                duplicate += 1
            else:
                ratio.append(duplicate)
                duplicate = 1
            if e == len(i["Value"]["ItemPool"]) - 2:
                ratio.append(duplicate)
            e += 1
        max_ratio = max(ratio)
        i["Value"]["ItemPool"] = list(dict.fromkeys(i["Value"]["ItemPool"]))
        for e in range(len(i["Value"]["ItemPool"])):
            for o in range(abs(ratio[e] - (max_ratio + 1))):
                new_list.append(i["Value"]["ItemPool"][e])
        i["Value"]["ItemPool"] = new_list

def write_patched_drop():
    with open("Serializer\\PB_DT_DropRateMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(item_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_DropRateMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_DropRateMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")
    os.remove("Serializer\\PB_DT_DropRateMaster.json")

def write_drop():
    shutil.copyfile("Serializer\\PB_DT_DropRateMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")

def write_patched_quest():
    with open("Serializer\\PB_DT_QuestMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(quest_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_QuestMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_QuestMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset")
    os.remove("Serializer\\PB_DT_QuestMaster.json")

def write_patched_scenario():
    with open("Serializer\\PBScenarioStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBScenarioStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBScenarioStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset")
    os.remove("Serializer\\PBScenarioStringTable.json")

def write_patched_item():
    with open("Serializer\\PB_DT_ItemMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(shop_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ItemMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ItemMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")
    os.remove("Serializer\\PB_DT_ItemMaster.json")

def write_item():
    shutil.copyfile("Serializer\\PB_DT_ItemMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")

def reset_drop():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")

def reset_quest():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset")

def reset_scenario():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset")

def reset_item():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")

def write_drop_log():
    for i in chest_data:
        log[0]["Value"][i["Key"]] = list(dict.fromkeys(log[0]["Value"][i["Key"]]))
        log[0]["Value"][i["Key"]].sort()
        log[2]["Value"][i["Key"]] = list(dict.fromkeys(log[2]["Value"][i["Key"]]))
        log[2]["Value"][i["Key"]].sort()
        log[3]["Value"][i["Key"]] = list(dict.fromkeys(log[3]["Value"][i["Key"]]))
        log[3]["Value"][i["Key"]].sort()
    for i in enemy_data:
        log[1]["Value"][i["Key"]] = list(dict.fromkeys(log[1]["Value"][i["Key"]]))
        log[1]["Value"][i["Key"]].sort()
    log[4]["Value"]["Red"].sort()
    log[4]["Value"]["Blue"].sort()
    log[4]["Value"]["Purple"].sort()
    log[4]["Value"]["Yellow"].sort()
    log[4]["Value"]["Green"].sort()
    log[4]["Value"]["White"].sort()
    with open("SpoilerLog\\Item.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def reset_drop_log():
    if os.path.isfile("SpoilerLog\\Item.json"):
        os.remove("SpoilerLog\\Item.json")