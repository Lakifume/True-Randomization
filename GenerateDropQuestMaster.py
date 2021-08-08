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
chest_index = []
enemy_index = []
quest_index = []
enemy_req_number = []
enemy_req_index = []
coin = [1, 5, 10, 50, 100, 500, 1000]
odd = [1, 1, 0]
shard_list = []
chest_skip_list = [
    "Treasurebox_SAN021(2)",
    "Treasurebox_KNG017(3)",
    "Treasurebox_KNG020(2)",
    "Treasurebox_TWR019(2)",
    "Treasurebox_TWR019(3)",
    "Treasurebox_BIG006(3)",
    "Treasurebox_ICE013(2)",
    "Treasurebox_BRM_A_FIRST",
    "Treasurebox_BRM_B_FIRST",
    "Treasurebox_BRM_A",
    "Treasurebox_BRM_B",
    "Treasurebox_OfflineChaos_A",
    "Treasurebox_OfflineChaos_B",
    "Treasurebox_OnlineChaos_A",
    "Treasurebox_OnlineChaos_B",
    "Wall_RVA011(2)"
]
enemy_skip_list = [
    "N1003_Shard",
    "N2001_Shard",
    "N2013_Shard"
]
log = []

#Content
with open("Data\\DropRateMaster\\Content\\PB_DT_DropRateMaster.json", "r") as file_reader:
    item_content = json.load(file_reader)

with open("Data\\QuestMaster\\Content\\PB_DT_QuestMaster.json", "r") as file_reader:
    quest_content = json.load(file_reader)

with open("Data\\ScenarioStringTable\\Content\\PBScenarioStringTable.json", "r") as file_reader:
    string_content = json.load(file_reader)

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
    translation = json.load(file_reader)

max_ratio = 0
for i in chest_data:
    if i["Value"]["IsUnique"]:
        i["Value"]["ItemPool"] = list(dict.fromkeys(i["Value"]["ItemPool"]))
    if i["Value"]["Ratio"] > max_ratio:
        max_ratio = i["Value"]["Ratio"]

for i in chest_data:
    for e in range(i["Value"]["Ratio"]):
        chest_type.append(i["Key"])
        if i["Value"]["ChestColor"] == "EChestColor::Green":
            green_chest_type.append(i["Key"])
        if i["Value"]["ChestColor"] == "EChestColor::Blue":
            blue_chest_type.append(i["Key"])
    if i == chest_data[9]:
        for e in range(abs(math.floor(i["Value"]["Ratio"]/4) - (max_ratio + 1))):
            if i["Value"]["InQuest"]:
                quest_type.append(i["Key"])
    else:
        for e in range(abs(i["Value"]["Ratio"] - (max_ratio + 1))):
            if i["Value"]["InQuest"]:
                quest_type.append(i["Key"])

for i in enemy_data:
    enemy_type.append(i["Key"])

i = 37
while i <= 499:
    if item_content[i]["Key"] in chest_skip_list or item_content[i]["Value"]["ItemType"] == "EItemType::Upgrade":
        i += 1
        continue
    chest_index.append(i)
    i += 1
random.shuffle(chest_index)

i = 513
while i <= 626:
    if item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Value"]["ShardRate"] == 100.0 and item_content[i]["Value"]["RareItemId"] == "None" and item_content[i]["Value"]["CommonItemId"] == "None" and item_content[i]["Value"]["RareIngredientId"] == "None" and item_content[i]["Value"]["CommonIngredientId"] == "None":
        i += 1
        continue
    enemy_index.append(i)
    i += 1
random.shuffle(enemy_index)

for i in range(len(quest_content)):
    quest_index.append(i)
random.shuffle(quest_index)

i = 500
while i <= 626:
    if item_content[i]["Key"][0:5] == item_content[i-1]["Key"][0:5] or item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Key"] in enemy_skip_list:
        i += 1
        continue
    shard_list.append(item_content[i]["Value"]["ShardId"])
    i += 1

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

def zangetsu_drops():
    for i in item_content:
        if i["Value"]["ItemType"] == "EItemType::Upgrade":
            i["Value"]["RareItemId"] = "None"
            i["Value"]["RareItemQuantity"] = 0
            i["Value"]["RareItemRate"] = 0.0
            i["Value"]["ItemType"] = "EItemType::None"

def chaos_key():
    item_content[11]["Value"]["ItemType"] = "EItemType::Weapon"
    item_content[157]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])
    item_content[194]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])
    item_content[195]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])
    item_content[234]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])
    item_content[418]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])
    item_content[445]["Value"]["ItemType"] = "EItemType::" + random.choice(["Accessory", "Body", "Head", "Recipe", "Scarf"])

def chaos_shard():
    i = 500
    while i <= 626:
        if item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Key"] in enemy_skip_list:
            i += 1
            continue
        if item_content[i]["Key"][0:5] == item_content[i-1]["Key"][0:5]:
            item_content[i]["Value"]["ShardId"] = item_content[i-1]["Value"]["ShardId"]
        else:
            shard = random.choice(shard_list)
            shard_list.remove(shard)
            item_content[i]["Value"]["ShardId"] = shard
        i += 1

def rand_pool():
    #JohannesMats
    patch_chest_entry(random.choice(blue_chest_type), 7)
    #FinalReward
    patch_chest_entry(random.choice(green_chest_type), 10)
    #StartChest
    patch_chest_entry(chest_data[12]["Key"], 36)
    #ItemPool
    for i in chest_index:
        item_type = random.choice(chest_type)
        if "Treasurebox" in item_content[i]["Key"]:
            if not item_content[i]["Value"]["AreaChangeTreasureFlag"]:
                while item_type == chest_data[8]["Key"]:
                    item_type = random.choice(chest_type)
            if item_content[i]["Value"]["ItemType"] == "EItemType::Bullet" or item_content[i]["Value"]["ItemType"] == "EItemType::Coin" or item_content[i]["Value"]["ItemType"] == "EItemType::Consumable" or item_content[i]["Value"]["AreaChangeTreasureFlag"]:
                while item_type == chest_data[9]["Key"]:
                    item_type = random.choice(chest_type)
        patch_chest_entry(item_type, i)
    #VolcanoWall
    patch_chest_entry(chest_data[3]["Key"], 493)
    #EnemyPool
    for i in enemy_index:
        if item_content[i]["Key"][0:5] == "N3090" or item_content[i]["Key"][0:5] == "N3099":
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateLow"])
        elif item_content[i]["Value"]["ShardRate"] != 100.0:
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateNormal"])
        if item_content[i]["Key"][0:5] != item_content[i-1]["Key"][0:5]:
            patch_enemy_entry(random.choice(enemy_type), i)
    for i in enemy_index:
        if item_content[i]["Key"][0:5] == item_content[i-1]["Key"][0:5]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Accessory"
        if chest_data[0]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[1]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Body"
        if chest_data[1]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[2]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Bullet"
        if chest_data[2]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[3]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Coin"
        if chest_data[3]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(item_content[i]["Value"]["CoinOverride"])
    if item_type == chest_data[4]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
        if chest_data[4]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["CommonItemId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
    if item_type == chest_data[5]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Consumable"
        if chest_data[5]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[6]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Head"
        if chest_data[6]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[7]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Consumable"
        if chest_data[7]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[8]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
        if chest_data[8]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[9]["Key"]:
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Recipe"
        if chest_data[9]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[10]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], chest_data[10]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[10]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[10]["Value"]["ItemRate"])
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Scarf"
        if chest_data[10]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    if item_type == chest_data[11]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[11]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[11]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[11]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[11]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonItemQuantity"] = random.choice(chest_data[11]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonRate"] = random.choice(chest_data[11]["Value"]["ItemRate"])
        item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[11]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(chest_data[11]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareIngredientRate"] = random.choice(chest_data[11]["Value"]["ItemRate"])
        item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[11]["Value"]["ItemPool"], False, item_type)
        item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(chest_data[11]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["CommonIngredientRate"] = random.choice(chest_data[11]["Value"]["ItemRate"])
        item_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        item_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(item_content[i]["Value"]["CoinOverride"])
        item_content[i]["Value"]["CoinRate"] = 0.0
        item_content[i]["Value"]["AreaChangeTreasureFlag"] = True
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
        if chest_data[11]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["CommonItemId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
    if item_type == chest_data[12]["Key"]:
        item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[12]["Value"]["ItemPool"], chest_data[12]["Value"]["IsUnique"], item_type)
        item_content[i]["Value"]["RareItemQuantity"] = random.choice(chest_data[12]["Value"]["ItemQuantity"])
        item_content[i]["Value"]["RareItemRate"] = random.choice(chest_data[12]["Value"]["ItemRate"])
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
        item_content[i]["Value"]["ItemType"] = "EItemType::Weapon"
        if chest_data[12]["Value"]["IsUnique"]:
            log[0]["Value"][item_type].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
    
def patch_enemy_entry(item_type, i):
    if item_type == enemy_data[0]["Key"]:
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[0]["Value"]["ItemRate"])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[11]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[11]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[1]["Value"]["ItemRate"])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[2]["Value"]["ItemRate"])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[0]["Value"]["ItemRate"])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
    if item_type == enemy_data[1]["Key"]:
        if random.choice(odd) == 1 and chest_data[11]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[11]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[1]["Value"]["ItemRate"])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[2]["Value"]["ItemRate"])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[0]["Value"]["ItemRate"])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[11]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[11]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[1]["Value"]["ItemRate"])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
    if item_type == enemy_data[2]["Key"]:
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[2]["Value"]["ItemRate"])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareItemId"]])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[0]["Value"]["ItemRate"])
            if enemy_data[0]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[0]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonItemId"]])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[11]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[11]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[1]["Value"]["ItemRate"])
            if enemy_data[1]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[1]["Key"]].append(translation["Value"][item_content[i]["Value"]["RareIngredientId"]])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[2]["Value"]["ItemRate"])
            if enemy_data[2]["Value"]["IsUnique"]:
                log[1]["Value"][enemy_data[2]["Key"]].append(translation["Value"][item_content[i]["Value"]["CommonIngredientId"]])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
        item_content[i]["Value"]["ItemType"] = "EItemType::CraftingMats"
    
def all_quest():
    for i in range(56):
        quest_content[i]["Value"]["NeedQuestID"] = "None"
        quest_content[i]["Value"]["NeedAreaID"] = "None"
        quest_content[i]["Value"]["NeedItemID"] = "None"
        quest_content[i]["Value"]["NeedBossID"] = "None"

def quest_req(normal, custom_map):
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
        enemy_room = ""
        for e in enemy_req_data[enemy_req_index[i]]["Value"]["NormalModeRooms"]:
            enemy_room += e + ","
        if not normal:
            for e in enemy_req_data[enemy_req_index[i]]["Value"]["HardModeRooms"]:
                enemy_room += e + ","
        enemy_room = enemy_room[:-1]
        quest_content[i]["Value"]["Enemy01"] = enemy_req_data[enemy_req_index[i]]["Key"]
        quest_content[i]["Value"]["EnemyNum01"] = len(enemy_req_data[enemy_req_index[i]]["Value"]["NormalModeRooms"])
        if not normal:
            quest_content[i]["Value"]["EnemyNum01"] += len(enemy_req_data[enemy_req_index[i]]["Value"]["HardModeRooms"])
        if custom_map:
            quest_content[i]["Value"]["EnemySpawnLocations"] = "none"
        else:
            quest_content[i]["Value"]["EnemySpawnLocations"] = enemy_room
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

def quest_reward():
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
    for i in quest_index:
        item_type = random.choice(quest_type)
        if item_type == chest_data[0]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[0]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[1]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[1]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[2]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[2]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = max(chest_data[2]["Value"]["ItemQuantity"]) * 3
        if item_type == chest_data[4]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[4]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = max(chest_data[4]["Value"]["ItemQuantity"]) * 3
        if item_type == chest_data[5]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[5]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[6]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[6]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[7]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[7]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = max(chest_data[7]["Value"]["ItemQuantity"]) * 3
        if item_type == chest_data[8]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[8]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[9]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[9]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[10]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[10]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        if item_type == chest_data[11]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[11]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = max(chest_data[11]["Value"]["ItemQuantity"]) * 3
        if item_type == chest_data[12]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[12]["Value"]["ItemPool"], True, item_type)
            quest_content[i]["Value"]["RewardNum01"] = 1
        log[2]["Value"][item_type].append(translation["Value"][quest_content[i]["Value"]["RewardItem01"]])

def req_string():
    string_content["Table"]["QST_Catering_Name01"] = translation["Value"][quest_content[35]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name02"] = translation["Value"][quest_content[50]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name03"] = translation["Value"][quest_content[51]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name04"] = translation["Value"][quest_content[42]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name05"] = translation["Value"][quest_content[41]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name06"] = translation["Value"][quest_content[39]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name07"] = translation["Value"][quest_content[44]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name08"] = translation["Value"][quest_content[38]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name09"] = translation["Value"][quest_content[52]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name10"] = translation["Value"][quest_content[45]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name11"] = translation["Value"][quest_content[40]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name12"] = translation["Value"][quest_content[49]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name13"] = translation["Value"][quest_content[46]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name14"] = translation["Value"][quest_content[37]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name15"] = translation["Value"][quest_content[53]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name16"] = translation["Value"][quest_content[47]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name17"] = translation["Value"][quest_content[36]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name18"] = translation["Value"][quest_content[54]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name19"] = translation["Value"][quest_content[43]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name20"] = translation["Value"][quest_content[48]["Value"]["Item01"]]
    string_content["Table"]["QST_Catering_Name21"] = translation["Value"][quest_content[55]["Value"]["Item01"]]

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

def write_drop(patched):
    if patched:
        with open("Serializer\\PB_DT_DropRateMaster.json", "w") as file_writer:
            file_writer.write(json.dumps(item_content, ensure_ascii=False, indent=2))
        root = os.getcwd()
        os.chdir("Serializer")
        os.system("cmd /c UAsset2Json.exe -tobin PB_DT_DropRateMaster.json")
        os.chdir(root)
        shutil.move("Serializer\\PB_DT_DropRateMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")
        os.remove("Serializer\\PB_DT_DropRateMaster.json")
    else:
        shutil.copyfile("Serializer\\PB_DT_DropRateMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")

def write_quest():
    with open("Serializer\\PB_DT_QuestMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(quest_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_QuestMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_QuestMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset")
    os.remove("Serializer\\PB_DT_QuestMaster.json")

def write_scenario():
    with open("Serializer\\PBScenarioStringTable.json", "w") as file_writer:
        file_writer.write(json.dumps(string_content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PBScenarioStringTable.json")
    os.chdir(root)
    shutil.move("Serializer\\PBScenarioStringTable.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset")
    os.remove("Serializer\\PBScenarioStringTable.json")

def reset_drop():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DropRateMaster.uasset")

def reset_quest():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_QuestMaster.uasset")

def reset_scenario():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBScenarioStringTable.uasset")

def write_drop_log():
    for i in chest_data:
        log[0]["Value"][i["Key"]] = list(dict.fromkeys(log[0]["Value"][i["Key"]]))
        log[0]["Value"][i["Key"]].sort()
        log[2]["Value"][i["Key"]] = list(dict.fromkeys(log[2]["Value"][i["Key"]]))
        log[2]["Value"][i["Key"]].sort()
    for i in enemy_data:
        log[1]["Value"][i["Key"]] = list(dict.fromkeys(log[1]["Value"][i["Key"]]))
        log[1]["Value"][i["Key"]].sort()
    with open("SpoilerLog\\Item.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def reset_drop_log():
    if os.path.isfile("SpoilerLog\\Item.json"):
        os.remove("SpoilerLog\\Item.json")