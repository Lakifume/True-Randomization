import json
import math
import random
import re
import os
import shutil
from random import randrange

#Keys

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
    "ICE": "m18"
}
special_chest_to_room = {
    "PotionMaterial": "m02VIL_005",
    "Qu07_Last": "m02VIL_003",
    "Swordsman": "m15JPN_016",
    "Treasurebox_PureMiriam_Hair": "m01SIP_003",
    "Treasurebox_PureMiriam_Tiare": "m10BIG_011",
    "Treasurebox_PureMiriam_Dress": "m08TWR_019",
    "Treasurebox_PureMiriam_Sword": "m08TWR_016",
    "N3106_1ST_Treasure": "m88BKR_004",
    "N3106_2ND_Treasure": "m88BKR_004"
}
room_to_special_chest = {
    "m02VIL_005": "PotionMaterial",
    "m02VIL_003": "Qu07_Last",
    "m15JPN_016": "Swordsman",
    "m01SIP_003": "Treasurebox_PureMiriam_Hair",
    "m10BIG_011": "Treasurebox_PureMiriam_Tiare",
    "m08TWR_019": "Treasurebox_PureMiriam_Dress",
    "m08TWR_016": "Treasurebox_PureMiriam_Sword",
    "m88BKR_004": "N3106_1ST_Treasure",
    "m88BKR_004": "N3106_2ND_Treasure"
}
all_keys = [
    "Doublejump",
    "HighJump",
    "Invert",
    "Deepsinker",
    "Dimensionshift",
    "Reflectionray",
    "Aquastream",
    "Bloodsteel",
    "Swordsman",
    "Silverbromide",
    "BreastplateofAguilar",
    "Keyofbacker1",
    "Keyofbacker2",
    "Keyofbacker3",
    "Keyofbacker4"
]
placed_keys = []
key_items = [
    "Swordsman",
    "Silverbromide",
    "BreastplateofAguilar",
    "Keyofbacker1",
    "Keyofbacker2",
    "Keyofbacker3",
    "Keyofbacker4"
]
key_shards = [
    "Doublejump",
    "HighJump",
    "Invert",
    "Deepsinker",
    "Dimensionshift",
    "Reflectionray",
    "Aquastream",
    "Bloodsteel"
]
key_items_location = [
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]
key_shards_location = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]
ordered_key_shards_location = []
previous_gate = []
previous_room = []
all_rooms = []
requirement = []
requirement_to_gate = {
    "Doublejump": [],
    "HighJump": [],
    "Invert": [],
    "Deepsinker": [],
    "Dimensionshift": [],
    "Reflectionray": [],
    "Aquastream": [],
    "Bloodsteel": [],
    "Swordsman": [],
    "Silverbromide": [],
    "BreastplateofAguilar": [],
    "Keyofbacker1": [],
    "Keyofbacker2": [],
    "Keyofbacker3": [],
    "Keyofbacker4": []
}

#Pool

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

#Shop

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

chest_unused_list = [
    "HPRecover",
    "SPEED",
    "Peanut",
    "Lantern",
    "TestIngredients",
    "Tresurebox_SAN000_01",
    "Tresurebox_SAN000_02",
    "Tresurebox_SAN_Tunic",
    "Tresurebox_SAN003_02",
    "Tresurebox_SAN003_03",
    "Tresurebox_SAN003_04",
    "Tresurebox_SAN016_01",
    "Tresurebox_SAN016_02",
    "Tresurebox_SAN017_01",
    "Tresurebox_SAN019_01",
    "Tresurebox_SAN_Spear",
    "Tresurebox_SAN_Shoes",
    "Tresurebox_SAN_Awhip",
    "Tresurebox_SAN_Dull",
    "Tresurebox_SAN_Claymore",
    "Tresurebox_SAN_Headband",
    "Tresurebox_SAN_Morgenstern",
    "Tresurebox_SAN_Baselard",
    "Tresurebox_SAN_High_Potion(2)",
    "Tresurebox_SAN_High_Potion(3)",
    "Tresurebox_SAN_High_Potion(4)",
    "Tresurebox_SAN_High_Ether(2)",
    "Tresurebox_SAN_High_Ether(3)",
    "Tresurebox_SAN_High_Ether(4)",
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
    "Treasurebox_OnlineChaos_B",
    "Wall_RVA003(2)",
    "Treasurebox_JRN001(2)",
    "Treasurebox_JRN001(3)",
    "Treasurebox_JRN001(4)",
    "Treasurebox_JRN002(2)"
]
enemy_skip_list = [
    "N1003",
    "N2001",
    "N2013"
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

with open("Data\\ShardMaster\\Content\\PB_DT_ShardMaster.json", "r") as file_reader:
    shard_content = json.load(file_reader)

#Data
with open("MapEdit\\Data\\RoomMaster\\Content\\PB_DT_RoomMaster.logic", "r") as file_reader:
    logic_data = json.load(file_reader)

with open("Data\\DropRateMaster\\EnemyLocation.json", "r") as file_reader:
    enemy_location = json.load(file_reader)

with open("Data\\DropRateMaster\\Chest.json", "r") as file_reader:
    chest_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Enemy.json", "r") as file_reader:
    enemy_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Shard.json", "r") as file_reader:
    shard_data = json.load(file_reader)

with open("Data\\QuestMaster\\Requirements.json", "r") as file_reader:
    item_req_data = json.load(file_reader)

with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    item_translation = json.load(file_reader)

with open("Data\\CharacterParameterMaster\\Translation.json", "r") as file_reader:
    enemy_translation = json.load(file_reader)

with open("Data\\ShardMaster\\Translation.json", "r") as file_reader:
    shard_translation = json.load(file_reader)

with open("Data\\DropRateMaster\\Seed.json", "r") as file_reader:
    seed = json.load(file_reader)

#FillingLootTypes
for i in chest_data:
    for e in range(i["Value"]["ChestRatio"]):
        chest_type.append(i["Key"])
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
    chest_index.append(i)
    i += 1
random.shuffle(chest_index)

#CollectingEnemyIndexes
i = 513
while i <= 626:
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

def unused_room_check(path):
    room_unused_list = []
    with open(path, "r") as file_reader:
        map_content = json.load(file_reader)
    for i in map_content:
        if not i["Value"]["AdjacentRoomName"] and not i["Key"] == "m09TRN_002":
            room_unused_list.append(i["Key"])
    for i in item_content:
        if chest_to_room(i["Key"]) in room_unused_list:
            chest_unused_list.append(i["Key"])

def load_custom_logic(path):
    global logic_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".logic"):
        with open(name + ".logic", "r") as file_reader:
            logic_data = json.load(file_reader)

def hard_enemy_logic():
    for i in enemy_location:
        for e in i["Value"]["HardModeRooms"]:
            i["Value"]["NormalModeRooms"].append(e)

def remove_infinite():
    #ByDefault
    item_content[69]["Value"]["RareItemId"] = "None"
    item_content[69]["Value"]["RareItemQuantity"] = 0
    item_content[69]["Value"]["RareItemRate"] = 0.0
    item_content[69]["Value"]["CoinType"] = "EDropCoin::D2000"
    item_content[69]["Value"]["CoinOverride"] = 10000
    item_content[69]["Value"]["CoinRate"] = 100.0
    quest_content[55]["Value"]["RewardItem01"] = "Medal019"
    quest_content[55]["Value"]["RewardNum01"] = 1
    #FromPool
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

def key_logic():
    #FillingListWithAllRoomNames
    for i in logic_data:
        all_rooms.append(i["Key"])
    #StartLogic
    while all_keys:
        #Reset
        requirement.clear()
        for i in key_items:
            requirement_to_gate[i].clear()
        for i in key_shards:
            requirement_to_gate[i].clear()
        previous_room.clear()
        #GatheringUpcomingGateRequirements
        for i in logic_data:
            if i["Value"]["GateRoom"] and previous_in_nearest(previous_gate, i["Value"]["NearestGate"]) and not i["Key"] in previous_gate:
                for e in key_items:
                    if i["Value"][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i["Key"])
                for e in key_shards:
                    if i["Value"][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i["Key"])
        #CheckIfRequirementIsntAlreadySatisfied
        check = False
        for i in placed_keys:
            if i in requirement:
                for e in requirement_to_gate[i]:
                    previous_gate.append(e)
                    check = True
        if check:
            continue
        #GatheringRoomsAvailableBeforeGate
        for i in logic_data:
            if not i["Value"]["GateRoom"] and previous_in_nearest(previous_gate, i["Value"]["NearestGate"]) or i["Key"] in previous_gate:
                #IncreasingChancesOfLateRooms
                gate_count = 0
                gate_list = i["Value"]["NearestGate"]
                while gate_list:
                    nearest_gate = gate_list[0]
                    for e in logic_data:
                        if e["Key"] == nearest_gate:
                            gate_count += 1
                            gate_list = e["Value"]["NearestGate"]
                            break
                for e in range((gate_count + 1)**3):
                    previous_room.append(i["Key"])
        #ChoosingKeyItemBasedOnRequirements
        chosen_item = random.choice(all_keys)
        if requirement:
            while chosen_item not in requirement:
                chosen_item = random.choice(all_keys)
            logic_choice(chosen_item, previous_room)
        else:
            logic_choice(chosen_item, all_rooms)
        #UpdatePreviousGate
        for i in requirement_to_gate[chosen_item]:
            previous_gate.append(i)
    #AppendInfoToLogs
    room_to_chest()
    room_to_enemy()
    fill_log()

def previous_in_nearest(previous_gate, nearest_gate):
    if not nearest_gate:
        return True
    else:
        for i in previous_gate:
            if i in nearest_gate:
                return True
    return False

def chest_to_room(chest):
    try:
        return room_to_area[chest.split("_")[1].split("(")[0][:3]] + chest.split("_")[1].split("(")[0][:3] + "_" + chest.split("_")[1].split("(")[0][3:]
    except KeyError:
        try:
            return special_chest_to_room[chest]
        except KeyError:
            return None
    except IndexError:
        try:
            return special_chest_to_room[chest]
        except KeyError:
            return None

def enemy_to_room(enemy):
    for i in enemy_location:
        if i["Key"] == enemy:
            return i["Value"]["NormalModeRooms"]
    
def logic_choice(chosen_item, room_list):
    #RemovingKeyFromList
    while chosen_item in all_keys:
        all_keys.remove(chosen_item)
    #ChoosingRoomToPlaceItemIn
    check = False
    while check == False:
        chosen_room = random.choice(room_list)
        if chosen_room in key_items_location or chosen_room in key_shards_location or chosen_room == "m01SIP_000":
            continue
        #CheckingIfRoomHasChest
        if chosen_item in key_items:
            check = room_chest_check(chosen_room)
        #CheckingIfRoomHasEnemy
        if chosen_item in key_shards:
            check = room_enemy_check(chosen_room)
    #UpdatingKeyItemLocation
    for i in range(len(key_items)):
        if key_items[i] == chosen_item:
            key_items_location[i] = chosen_room
    #UpdatingKeyShardLocation
    for i in range(len(key_shards)):
        if key_shards[i] == chosen_item:
            key_shards_location[i] = chosen_room
    #StoringKeyShardChoiceOrder
    if chosen_item in key_shards:
        ordered_key_shards_location.append(chosen_room)
    placed_keys.append(chosen_item)

def room_chest_check(room):
    for i in item_content:
        #CheckingIfChestIsntUnused
        if i["Key"] not in chest_unused_list:
            #CheckingIfChestCorrespondsToRoom
            if chest_to_room(i["Key"]) == room:
                return True
    return False

def room_enemy_check(room):
    for i in enemy_location:
        #CheckingIfEnemyHasShardSlotAndIsInRoom
        if not i["Key"] in enemy_skip_list and i["Value"]["HasShard"] and room in i["Value"]["NormalModeRooms"]:
            #CheckingIfEnemyIsntInAlreadyAssignedRoom
            check = True
            for e in key_shards_location:
                if e in i["Value"]["NormalModeRooms"]:
                    check = False
            if check:
                return True
    return False

def room_to_chest():
    for i in range(len(key_items)):
        #GatheringPossibleChestChoices
        possible_chests = []
        for e in item_content:
            if e["Key"] not in chest_unused_list:
                if key_items_location[i][3:].replace("_", "") in e["Key"]:
                    possible_chests.append(e["Key"])
                try:
                    if room_to_special_chest[key_items_location[i]] == e["Key"]:
                        possible_chests.append(e["Key"])
                except KeyError:
                    continue
        #PickingChest
        key_items_location[i] = random.choice(possible_chests)

def room_to_enemy():
    for i in range(len(key_shards)):
        #GatheringPossibleEnemyChoices
        possible_enemy = []
        for e in enemy_location:
            if not e["Key"] in enemy_skip_list and e["Value"]["HasShard"] and ordered_key_shards_location[i] in e["Value"]["NormalModeRooms"]:
                possible_enemy.append(e["Key"])
        #CheckingIfEnemyIsntAlreadyTaken
        chosen_enemy = random.choice(possible_enemy)
        while chosen_enemy in key_shards_location:
            chosen_enemy = random.choice(possible_enemy)
        #ConvertingShardAssignmentOrderToNormalOrder
        for e in range(len(key_shards_location)):
            if key_shards_location[e] == ordered_key_shards_location[i]:
                key_shards_location[e] = chosen_enemy

def fill_log():
    for i in range(len(key_items)):
        log_data = {}
        log_data["Key"] = item_translation["Value"][key_items[i]]
        log_data["Value"] = {}
        log_data["Value"]["Container"] = key_items_location[i]
        log_data["Value"]["RoomList"] = chest_to_room(key_items_location[i])
        log.append(log_data)
    for i in range(len(key_shards)):
        log_data = {}
        log_data["Key"] = shard_translation["Value"][key_shards[i]]
        log_data["Value"] = {}
        log_data["Value"]["Container"] = enemy_translation["Value"][key_shards_location[i]]
        log_data["Value"]["RoomList"] = enemy_to_room(key_shards_location[i])
        log.append(log_data)

def rand_key_placement():
    key_logic()
    #KeyItems
    for i in range(len(key_items)):
        patch_key_item_entry(key_items[i], key_items_location[i])
    #KeyShards
    for i in range(len(key_shards)):
        patch_key_shard_entry(key_shards[i], key_shards_location[i])

def rand_shard_placement():
    i = 500
    while i <= 629:
        if item_content[i]["Key"].split("_")[0] in key_shards_location or item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Key"].split("_")[0] in enemy_skip_list:
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
    #ZangetsuReward
    patch_chest_entry(random.choice(green_chest_type), 11)
    #StartChest
    patch_chest_entry(chest_data[12]["Key"], 36)
    #ItemPool
    for i in chest_index:
        #UnusedCheck
        if item_content[i]["Key"] in chest_unused_list:
            continue
        #Patch
        patch_chest_entry(random.choice(chest_type), i)
    #EnemyPool
    for i in enemy_index:
        #Mats
        if item_content[i]["Value"]["ShardRate"] == 0.0 or item_content[i]["Key"].split("_")[0] == item_content[i-1]["Key"].split("_")[0]:
            continue
        if item_content[i]["Key"].split("_")[0] == "N3090" or item_content[i]["Key"].split("_")[0] == "N3099":
            patch_enemy_entry(random.choice(enemy_type), "ItemRateLow", i)
        else:
            patch_enemy_entry(random.choice(enemy_type), "ItemRateNormal", i)
        #ShardRate
        if item_content[i]["Value"]["ShardRate"] == 100.0:
            continue
        if item_content[i]["Key"].split("_")[0] == "N3090" or item_content[i]["Key"].split("_")[0] == "N3099":
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateLow"])
        else:
            item_content[i]["Value"]["ShardRate"] = random.choice(shard_data["Value"]["ItemRateNormal"])
    #DuplicateCheck
    for i in enemy_index:
        if "Treasure" in item_content[i]["Key"]:
            continue
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
    #CarpenterChest1
    patch_chest_entry(random.choice(green_chest_type), 621)
    #CarpenterChest2
    patch_chest_entry(random.choice(green_chest_type), 622)

def patch_key_item_entry(item, chest):
    for i in range(len(item_content)):
        if item_content[i]["Key"] == chest:
            item_content[seed_convert(i)]["Value"]["RareItemId"] = item
            item_content[seed_convert(i)]["Value"]["RareItemQuantity"] = 1
            item_content[seed_convert(i)]["Value"]["RareItemRate"] = 100.0
            item_content[seed_convert(i)]["Value"]["CommonItemId"] = "None"
            item_content[seed_convert(i)]["Value"]["CommonItemQuantity"] = 0
            item_content[seed_convert(i)]["Value"]["CommonRate"] = 0.0
            item_content[seed_convert(i)]["Value"]["RareIngredientId"] = "None"
            item_content[seed_convert(i)]["Value"]["RareIngredientQuantity"] = 0
            item_content[seed_convert(i)]["Value"]["RareIngredientRate"] = 0.0
            item_content[seed_convert(i)]["Value"]["CommonIngredientId"] = "None"
            item_content[seed_convert(i)]["Value"]["CommonIngredientQuantity"] = 0
            item_content[seed_convert(i)]["Value"]["CommonIngredientRate"] = 0.0
            item_content[seed_convert(i)]["Value"]["CoinType"] = "EDropCoin::None"
            item_content[seed_convert(i)]["Value"]["CoinOverride"] = 0
            item_content[seed_convert(i)]["Value"]["CoinRate"] = 0.0
            item_content[seed_convert(i)]["Value"]["AreaChangeTreasureFlag"] = False
    
def patch_key_shard_entry(shard, enemy):
    for i in item_content:
        if i["Key"].split("_")[0] == enemy:
            i["Value"]["ShardId"] = shard

def patch_chest_entry(item_type, i):
    if item_content[i]["Key"] in key_items_location:
        return
    i = seed_convert(i)
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
    elif item_type == chest_data[12]["Key"]:
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
    
def patch_enemy_entry(item_type, item_rate, i):
    if item_type == enemy_data[0]["Key"]:
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[0]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[1]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[2]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[0]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == enemy_data[1]["Key"]:
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[1]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[2]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[0]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[1]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == enemy_data[2]["Key"]:
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareItemId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareItemQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareItemRate"] = random.choice(enemy_data[2]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareItemId"] = "None"
            item_content[i]["Value"]["RareItemQuantity"] = 0
            item_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[4]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonItemId"] = any_pick(chest_data[4]["Value"]["ItemPool"], enemy_data[0]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonItemQuantity"] = random.choice(enemy_data[0]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonRate"] = random.choice(enemy_data[0]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonItemId"] = "None"
            item_content[i]["Value"]["CommonItemQuantity"] = 0
            item_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and chest_data[10]["Value"]["ItemPool"]:
            item_content[i]["Value"]["RareIngredientId"] = any_pick(chest_data[10]["Value"]["ItemPool"], enemy_data[1]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["RareIngredientQuantity"] = random.choice(enemy_data[1]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["RareIngredientRate"] = random.choice(enemy_data[1]["Value"][item_rate])
        else:
            item_content[i]["Value"]["RareIngredientId"] = "None"
            item_content[i]["Value"]["RareIngredientQuantity"] = 0
            item_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and enemy_data[2]["Value"]["ItemPool"]:
            item_content[i]["Value"]["CommonIngredientId"] = any_pick(enemy_data[2]["Value"]["ItemPool"], enemy_data[2]["Value"]["IsUnique"], item_type)
            item_content[i]["Value"]["CommonIngredientQuantity"] = random.choice(enemy_data[2]["Value"]["ItemQuantity"])
            item_content[i]["Value"]["CommonIngredientRate"] = random.choice(enemy_data[2]["Value"][item_rate])
        else:
            item_content[i]["Value"]["CommonIngredientId"] = "None"
            item_content[i]["Value"]["CommonIngredientQuantity"] = 0
            item_content[i]["Value"]["CommonIngredientRate"] = 0.0

def seed_convert(i):
    new_chest = seed["Value"][item_content[i]["Key"]]
    for e in range(len(item_content)):
        if item_content[e]["Key"] == new_chest:
            return e

def all_quest():
    for i in range(56):
        quest_content[i]["Value"]["NeedQuestID"] = "None"
        quest_content[i]["Value"]["NeedAreaID"] = "None"
        quest_content[i]["Value"]["NeedItemID"] = "None"
        quest_content[i]["Value"]["NeedBossID"] = "None"

def quest_req():
    #EnemyQuests
    for i in range(len(enemy_location)):
        if enemy_location[i]["Key"][0] != "N" or enemy_location[i]["Key"] == "N2013":
            continue
        enemy_req_number.append(i)
    for i in range(19):
        enemy_req_index.append(any_pick(enemy_req_number, True, "None"))
    enemy_req_index.sort()
    for i in range(19):
        quest_content[i]["Value"]["Enemy01"] = enemy_location[enemy_req_index[i]]["Key"]
        quest_content[i]["Value"]["EnemyNum01"] = len(enemy_location[enemy_req_index[i]]["Value"]["NormalModeRooms"])
        enemy_room = ""
        for e in enemy_location[enemy_req_index[i]]["Value"]["NormalModeRooms"]:
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
        elif item_type == chest_data[12]["Key"]:
            quest_content[i]["Value"]["RewardItem01"] = any_pick(chest_data[12]["Value"]["ItemPool"], chest_data[12]["Value"]["IsUnique"], item_type)
            if chest_data[12]["Value"]["IsUnique"]:
                quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                quest_content[i]["Value"]["RewardNum01"] = max(chest_data[12]["Value"]["ItemQuantity"]) * 3
    invert_ratio()

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

def no_card_shop():
    shop_content[561]["Value"]["buyPrice"] = 0
    shop_content[561]["Value"]["sellPrice"] = 0

def rand_shop_pool():
    for i in chest_data:
        for e in shop_skip_list:
            while e in i["Value"]["ItemPool"]:
                i["Value"]["ItemPool"].remove(e)
        events = []
        for e in range(i["Value"]["ShopRatio"]):
            events.append(random.choice(event_type))
        chosen = []
        for e in events:
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

def candle_process(shard, candle):
    for i in enemy_location:
        if i["Key"] == candle:
            filelist = i["Value"]["NormalModeRooms"]
    for i in shard_content:
        if i["Key"] == candle:
            candle_type = i["Value"]["ShardType"]
        if i["Key"] == shard:
            shard_type = i["Value"]["ShardType"]
    for i in filelist:
        file_name = i + "_Gimmick"
        #ReadJson
        with open("UAssetGUI\\Json\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
            content = json.load(file_reader)
        #PatchJson
        for e in content["Exports"]:
            try:
                if candle in e["Data"][45]["Value"]:
                    e["Data"][45]["Value"] = shard + "(0)"
            except TypeError:
                continue
            except IndexError:
                continue
        for e in range(len(content["NameMap"])):
            if content["NameMap"][e] == candle:
                content["NameMap"][e] = shard
            if content["NameMap"][e] == candle_type:
                content["NameMap"][e] = shard_type
        #WriteJson
        with open("UAssetGUI\\" + file_name + ".json", "w") as file_writer:
            file_writer.write(json.dumps(content))
        #CommandFromJson
        root = os.getcwd()
        os.chdir("UAssetGUI")
        os.system("cmd /c UAssetGUI.exe fromjson " + file_name + ".json " + file_name + ".umap")
        os.chdir(root)
        #Move
        shutil.move("UAssetGUI\\" + file_name + ".umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name + ".umap")
        #Delete
        os.remove("UAssetGUI\\" + file_name + ".json")

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

def write_patched_candle():
    print("mXXXXX_XXX_Gimmick.umap")
    i = 627
    while i <= 629:
        candle_process(item_content[i]["Value"]["ShardId"], item_content[i]["Key"].split("_")[0])
        i += 1
    print("Done")

def write_drop_log():
    with open("MapEdit\\Key\\KeyLocation.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))