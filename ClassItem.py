import ClassManagement
import math
import random

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
    "m02VIL_005": ["PotionMaterial"],
    "m02VIL_003": ["Qu07_Last"],
    "m15JPN_016": ["Swordsman"],
    "m01SIP_003": ["Treasurebox_PureMiriam_Hair"],
    "m10BIG_011": ["Treasurebox_PureMiriam_Tiare"],
    "m08TWR_019": ["Treasurebox_PureMiriam_Dress"],
    "m08TWR_016": ["Treasurebox_PureMiriam_Sword"],
    "m88BKR_004": ["N3106_1ST_Treasure", "N3106_2ND_Treasure"]
}
boss_rooms= [
    "m01SIP_022",
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
    "m88BKR_001",
    "m88BKR_002",
    "m88BKR_004"
]

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
requirement_to_gate = {}

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

coin = [1, 5, 10, 50, 100, 500, 1000]
odd = [1, 1, 0]

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
ten_thousand = []

#Lists

chest_skip_list = [
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

#Galleon

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
ship_chest_list = [
    "Treasurebox_SIP002(2)",
    "Treasurebox_SIP003(2)",
    "Treasurebox_SIP004(2)",
    "Treasurebox_SIP005(2)",
    "Treasurebox_SIP005(3)",
    "Treasurebox_SIP006(2)",
    "Treasurebox_SIP007(2)",
    "Treasurebox_SIP007(3)",
    "Treasurebox_SIP009(2)",
    "Treasurebox_SIP011(2)",
    "Treasurebox_SIP011(3)",
    "Treasurebox_SIP011(4)",
    "Treasurebox_SIP011(5)",
    "Treasurebox_SIP012(2)",
    "Treasurebox_SIP013(2)",
    "Treasurebox_SIP015(2)",
    "Treasurebox_SIP016(2)",
    "Treasurebox_SIP017(2)",
    "Treasurebox_SIP018(2)",
    "Treasurebox_SIP019(2)",
    "Treasurebox_SIP020(2)",
    "Treasurebox_SIP021(3)",
    "Treasurebox_SIP025(2)",
    "Treasurebox_SIP025(3)",
    "Wall_SIP004(2)",
    "Wall_SIP009(2)",
    "Wall_SIP016(2)"
]
ship_skip_list = [
    "m01SIP_022",
    "m01SIP_023"
]

log = []

def init():
    #FillingLootTypes
    for i in ClassManagement.item_drop_data:
        for e in range(i["Value"]["ChestRatio"]):
            chest_type.append(i["Key"])
            if i["Value"]["ChestColor"] == "Green":
                green_chest_type.append(i["Key"])
            if i["Value"]["ChestColor"] == "Blue":
                blue_chest_type.append(i["Key"])
        for e in range(i["Value"]["QuestRatio"]):
            quest_type.append(i["Key"])
    for i in ClassManagement.enemy_drop_data:
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
    for i in range(len(ClassManagement.quest_content)):
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
    i = 100000
    while i <= 400000:
        base.append(i)
        i += 100000
    base.append(500000)
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
    
    #CollectingZeroPrices
    for i in ClassManagement.item_content:
        if i["Value"]["buyPrice"] == 0:
            shop_skip_list.append(i["Key"])
    ClassManagement.debug("ClassItem.init()")

def unused_room_check():
    room_unused_list = []
    for i in ClassManagement.room_content:
        if not i["Value"]["AdjacentRoomName"] and not i["Key"] == "m09TRN_002":
            room_unused_list.append(i["Key"])
    for i in ClassManagement.drop_content:
        if chest_to_room(i["Key"]) in room_unused_list:
            chest_skip_list.append(i["Key"])
    ClassManagement.debug("ClassItem.unused_room_check()")

def extra_logic_safety():
    #Benjamin
    ClassManagement.logic_data[30]["Value"]["NearestGate"] = ClassManagement.logic_data[382]["Value"]["NearestGate"]
    #100%Chest
    ClassManagement.logic_data[32]["Value"]["NearestGate"] = ClassManagement.logic_data[382]["Value"]["NearestGate"]
    #OD
    if ClassManagement.book_content[21]["Value"]["RoomTraverseThreshold"] > 80:
        ClassManagement.logic_data[367]["Value"]["NearestGate"] = ClassManagement.logic_data[382]["Value"]["NearestGate"]
    ClassManagement.debug("ClassItem.extra_logic_safety()")

def hard_enemy_logic():
    for i in ClassManagement.enemy_location_data:
        for e in i["Value"]["HardModeRooms"]:
            i["Value"]["NormalModeRooms"].append(e)
        #DullaHeadFix
        if i["Key"] == "N3090":
            i["Value"]["NormalModeRooms"].remove("m07LIB_029")
            i["Value"]["NormalModeRooms"].remove("m08TWR_005")
            i["Value"]["NormalModeRooms"].remove("m08TWR_013")
            i["Value"]["NormalModeRooms"].remove("m11UGD_013")
    ClassManagement.debug("ClassItem.hard_enemy_logic()")

def remove_infinite():
    while "Gebelsglasses" in ClassManagement.item_drop_data[0]["Value"]["ItemPool"]:
        ClassManagement.item_drop_data[0]["Value"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in ClassManagement.quest_requirement_data[0]["Value"]["ItemPool"]:
        ClassManagement.quest_requirement_data[0]["Value"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in ClassManagement.item_drop_data[6]["Value"]["ItemPool"]:
        ClassManagement.item_drop_data[6]["Value"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in ClassManagement.quest_requirement_data[0]["Value"]["ItemPool"]:
        ClassManagement.quest_requirement_data[0]["Value"]["ItemPool"].remove("Recyclehat")
    ClassManagement.debug("ClassItem.remove_infinite()")

def give_shortcut():
    ClassManagement.drop_content[6]["Value"]["RareItemId"] = "Shortcut"
    ClassManagement.drop_content[6]["Value"]["RareItemQuantity"] = 7
    ClassManagement.drop_content[6]["Value"]["RareItemRate"] = 100.0
    while "Shortcut" in ClassManagement.shard_drop_data["Value"]["ItemPool"]:
        ClassManagement.shard_drop_data["Value"]["ItemPool"].remove("Shortcut")
    ClassManagement.debug("ClassItem.give_shortcut()")
    
def give_eye():
    ClassManagement.drop_content[6]["Value"]["CommonItemId"] = "SkilledDetectiveeye"
    ClassManagement.drop_content[6]["Value"]["CommonItemQuantity"] = 1
    ClassManagement.drop_content[6]["Value"]["CommonRate"] = 100.0
    while "Detectiveeye" in ClassManagement.shard_drop_data["Value"]["ItemPool"]:
        ClassManagement.shard_drop_data["Value"]["ItemPool"].remove("Detectiveeye")
    ClassManagement.debug("ClassItem.give_eye()")

def give_extra(shard):
    ClassManagement.drop_content[6]["Value"]["RareIngredientId"] = shard
    ClassManagement.drop_content[6]["Value"]["RareIngredientQuantity"] = 1
    ClassManagement.drop_content[6]["Value"]["RareIngredientRate"] = 100.0
    if shard in key_shards:
        key_shards.remove(shard)
        key_shards_location.pop()
        all_keys.remove(shard)
        for i in ClassManagement.logic_data:
            if i["Value"][shard]:
                i["Value"]["GateRoom"] = False
                for e in ClassManagement.logic_data:
                    if i["Key"] in e["Value"]["NearestGate"]:
                        e["Value"]["NearestGate"] = i["Value"]["NearestGate"]
    else:
        while shard in ClassManagement.shard_drop_data["Value"]["ItemPool"]:
            ClassManagement.shard_drop_data["Value"]["ItemPool"].remove(shard)
    ClassManagement.debug("ClassItem.give_extra(" + shard + ")")

def no_shard_craft():
    i = 345
    while i <= 356:
        ClassManagement.craft_content[i]["Value"]["OpenKeyRecipeID"] = "Medal019"
        i += 1
    ClassManagement.debug("ClassItem.no_shard_craft()")

def key_logic():
    #FillingListWithAllRoomNames
    for i in ClassManagement.logic_data:
        all_rooms.append(i["Key"])
    #FillingRequirementDictionary
    for i in key_items:
        requirement_to_gate[i] = []
    for i in key_shards:
        requirement_to_gate[i] = []
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
        for i in ClassManagement.logic_data:
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
                check = True
                for e in requirement_to_gate[i]:
                    previous_gate.append(e)
        if check:
            continue
        #GatheringRoomsAvailableBeforeGate
        for i in ClassManagement.logic_data:
            if not i["Value"]["GateRoom"] and previous_in_nearest(previous_gate, i["Value"]["NearestGate"]) or i["Key"] in previous_gate:
                #IncreasingChancesOfLateRooms
                gate_count = 1
                gate_list = i["Value"]["NearestGate"]
                while gate_list:
                    nearest_gate = random.choice(gate_list)
                    for e in ClassManagement.logic_data:
                        if e["Key"] == nearest_gate:
                            gate_count += 1
                            gate_list = e["Value"]["NearestGate"]
                            break
                #IncreasingChancesOfBossRooms
                if i["Key"] in boss_rooms:
                    gate_count *= 6
                for e in range(gate_count):
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
    for i in ClassManagement.enemy_location_data:
        if i["Key"] == enemy:
            return i["Value"]["NormalModeRooms"]
    
def logic_choice(chosen_item, room_list):
    #RemovingKeyFromList
    while chosen_item in all_keys:
        all_keys.remove(chosen_item)
    #ChoosingRoomToPlaceItemIn
    check = False
    while not check:
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
    for i in ClassManagement.drop_content:
        #CheckingIfChestIsntUnused
        if i["Key"] not in chest_skip_list:
            #CheckingIfChestCorrespondsToRoom
            if chest_to_room(i["Key"]) == room:
                return True
    return False

def room_enemy_check(room):
    for i in ClassManagement.enemy_location_data:
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
        for e in ClassManagement.drop_content:
            if e["Key"] not in chest_skip_list:
                if key_items_location[i][3:].replace("_", "") in e["Key"]:
                    possible_chests.append(e["Key"])
                try:
                    if e["Key"] in room_to_special_chest[key_items_location[i]]:
                        possible_chests.append(e["Key"])
                except KeyError:
                    continue
        #PickingChest
        key_items_location[i] = random.choice(possible_chests)

def room_to_enemy():
    for i in range(len(key_shards)):
        #GatheringPossibleEnemyChoices
        possible_enemy = []
        for e in ClassManagement.enemy_location_data:
            if not e["Key"] in enemy_skip_list and e["Value"]["HasShard"] and ordered_key_shards_location[i] in e["Value"]["NormalModeRooms"]:
                #IncreasingChancesOfUncommonEnemies
                for o in range(math.ceil(36/len(e["Value"]["NormalModeRooms"]))):
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
        log_data["Key"] = ClassManagement.item_translation["Value"][key_items[i]]
        log_data["Value"] = {}
        log_data["Value"]["Container"] = key_items_location[i]
        log_data["Value"]["RoomList"] = chest_to_room(key_items_location[i])
        log.append(log_data)
    for i in range(len(key_shards)):
        log_data = {}
        log_data["Key"] = ClassManagement.shard_translation["Value"][key_shards[i]]
        log_data["Value"] = {}
        log_data["Value"]["Container"] = ClassManagement.enemy_translation["Value"][key_shards_location[i]]
        log_data["Value"]["RoomList"] = enemy_to_room(key_shards_location[i])
        log.append(log_data)

def rand_overworld_key():
    key_logic()
    #KeyItems
    for i in range(len(key_items)):
        patch_key_item_entry(key_items[i], key_items_location[i])
    #KeyShards
    for i in ClassManagement.drop_content:
        i["Value"]["DropSpecialFlags"] = "EDropSpecialFlag::None"
    for i in range(len(key_shards)):
        patch_key_shard_entry(key_shards[i], key_shards_location[i])
    ClassManagement.debug("ClassItem.rand_overworld_key()")

def rand_ship_waystone():
    #CheckStartingKey
    if not "Doublejump" in key_shards or not "Dimensionshift" in key_shards or not "Reflectionray" in key_shards:
        ship_height()
    if not "HighJump" in key_shards or not "Invert" in key_shards:
        ship_flight()
    #CheckShardsOnShip
    for i in range(len(key_shards)):
        for e in ClassManagement.enemy_location_data:
            if e["Key"] == key_shards_location[i]:
                for o in e["Value"]["NormalModeRooms"]:
                    if "m01SIP" in o and o not in ship_skip_list:
                        if key_shards[i] == "Doublejump" or key_shards[i] == "Dimensionshift" or key_shards[i] == "Reflectionray":
                            ship_height()
                        if key_shards[i] == "HighJump" or key_shards[i] == "Invert":
                            ship_flight()
    #AssignChest
    chosen_chest = random.choice(ship_chest_list)
    while chosen_chest in chest_skip_list:
        chosen_chest = random.choice(ship_chest_list)
    patch_key_item_entry("Waystone", chosen_chest)
    ClassManagement.debug("ClassItem.rand_ship_waystone()")

def ship_height():
    if "Treasurebox_SIP014(2)" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP014(2)")
    if "Treasurebox_SIP024(2)" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP024(2)")
    if "Treasurebox_SIP024(3)" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP024(3)")
    if "Treasurebox_SIP026(2)" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP026(2)")
    if "Wall_SIP014(2)" not in ship_chest_list:
        ship_chest_list.append("Wall_SIP014(2)")
    while "m01SIP_023" in ship_skip_list:
        ship_skip_list.remove("m01SIP_023")

def ship_flight():
    if "Treasurebox_PureMiriam_Hair" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_PureMiriam_Hair")

def rand_overworld_shard():
    i = 500
    while i <= 629:
        if ClassManagement.drop_content[i]["Key"].split("_")[0] in key_shards_location or ClassManagement.drop_content[i]["Value"]["ShardRate"] == 0.0 or ClassManagement.drop_content[i]["Key"].split("_")[0] in enemy_skip_list:
            i += 1
            continue
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == ClassManagement.drop_content[i-1]["Key"].split("_")[0]:
            ClassManagement.drop_content[i]["Value"]["ShardId"] = ClassManagement.drop_content[i-1]["Value"]["ShardId"]
        else:
            ClassManagement.drop_content[i]["Value"]["ShardId"] = any_pick(ClassManagement.shard_drop_data["Value"]["ItemPool"], True, "None")
        i += 1
    ClassManagement.debug("ClassItem.rand_overworld_shard()")

def rand_overworld_pool():
    #JohannesMats
    patch_chest_entry(random.choice(blue_chest_type), 7)
    #FinalReward
    patch_chest_entry(random.choice(green_chest_type), 10)
    #ZangetsuReward
    patch_chest_entry(random.choice(green_chest_type), 11)
    #StartChest
    patch_start_chest_entry(36)
    #ItemPool
    for i in chest_index:
        #UnusedCheck
        if ClassManagement.drop_content[i]["Key"] in chest_skip_list:
            continue
        #Patch
        patch_chest_entry(random.choice(chest_type), i)
    #EnemyPool
    for i in enemy_index:
        #Mats
        if ClassManagement.drop_content[i]["Value"]["ShardRate"] == 0.0 or ClassManagement.drop_content[i]["Key"].split("_")[0] == ClassManagement.drop_content[i-1]["Key"].split("_")[0]:
            continue
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3090" or ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3099":
            patch_enemy_entry(random.choice(enemy_type), 0.5, i)
        else:
            patch_enemy_entry(random.choice(enemy_type), 1.0, i)
        #ShardRate
        if ClassManagement.drop_content[i]["Value"]["ShardRate"] == 100.0:
            continue
        ClassManagement.drop_content[i]["Value"]["ShardRate"] = ClassManagement.shard_drop_data["Value"]["ItemRate"]
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3090" or ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3099":
            ClassManagement.drop_content[i]["Value"]["ShardRate"] /= 2
        if ClassManagement.drop_content[i]["Value"]["DropSpecialFlags"] == "EDropSpecialFlag::DropShardOnce":
            ClassManagement.drop_content[i]["Value"]["ShardRate"] *= 3
    #FireCannonShardFix
    ClassManagement.drop_content[516]["Value"]["ShardRate"] = ClassManagement.drop_content[515]["Value"]["ShardRate"]
    #DuplicateCheck
    for i in enemy_index:
        if "Treasure" in ClassManagement.drop_content[i]["Key"]:
            continue
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == ClassManagement.drop_content[i-1]["Key"].split("_")[0]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = ClassManagement.drop_content[i-1]["Value"]["RareItemId"]
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.drop_content[i-1]["Value"]["RareItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.drop_content[i-1]["Value"]["RareItemRate"]
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = ClassManagement.drop_content[i-1]["Value"]["CommonItemId"]
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.drop_content[i-1]["Value"]["CommonItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.drop_content[i-1]["Value"]["CommonRate"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = ClassManagement.drop_content[i-1]["Value"]["RareIngredientId"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.drop_content[i-1]["Value"]["RareIngredientQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.drop_content[i-1]["Value"]["RareIngredientRate"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = ClassManagement.drop_content[i-1]["Value"]["CommonIngredientId"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.drop_content[i-1]["Value"]["CommonIngredientQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.drop_content[i-1]["Value"]["CommonIngredientRate"]
    #CarpenterChest1
    patch_chest_entry(random.choice(green_chest_type), 621)
    #CarpenterChest2
    patch_chest_entry(random.choice(green_chest_type), 622)
    ClassManagement.debug("ClassItem.rand_overworld_pool()")

def patch_key_item_entry(item, chest):
    for i in range(len(ClassManagement.drop_content)):
        if ClassManagement.drop_content[i]["Key"] == chest:
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareItemId"] = item
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareItemQuantity"] = 1
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareItemRate"] = 100.0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonRate"] = 0.0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["RareIngredientRate"] = 0.0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CommonIngredientRate"] = 0.0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CoinType"] = "EDropCoin::None"
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CoinOverride"] = 0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["CoinRate"] = 0.0
            ClassManagement.drop_content[seed_convert(i)]["Value"]["AreaChangeTreasureFlag"] = False
    chest_skip_list.append(chest)
    
def patch_key_shard_entry(shard, enemy):
    for i in range(len(ClassManagement.drop_content)):
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == enemy:
            if ClassManagement.drop_content[i]["Key"].split("_")[0] == ClassManagement.drop_content[i-1]["Key"].split("_")[0]:
                ClassManagement.drop_content[i]["Value"]["ShardId"] = "None"
                ClassManagement.drop_content[i]["Value"]["ShardRate"] = 0.0
            else:
                ClassManagement.drop_content[i]["Value"]["DropSpecialFlags"] = "EDropSpecialFlag::DropShardOnce"
                ClassManagement.drop_content[i]["Value"]["ShardId"] = shard

def patch_start_chest_entry(i):
    i = seed_convert(i)
    ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[12]["Value"]["ItemPool"], ClassManagement.item_drop_data[12]["Value"]["IsUnique"], ClassManagement.item_drop_data[12]["Key"])
    ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[12]["Value"]["ItemQuantity"]
    ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[12]["Value"]["ItemRate"]
    if ClassManagement.drop_content[i]["Value"]["RareItemId"] in gun_list:
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[2]["Value"]["ItemPool"], ClassManagement.item_drop_data[2]["Value"]["IsUnique"], ClassManagement.item_drop_data[2]["Key"])
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.item_drop_data[2]["Value"]["ItemQuantity"]*3
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.item_drop_data[2]["Value"]["ItemRate"]
    else:
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
    ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
    ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
    ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
    ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
    ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
    ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
    ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
    ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
    ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
    ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False

def patch_chest_entry(item_type, i):
    if ClassManagement.drop_content[i]["Key"] in chest_skip_list:
        return
    i = seed_convert(i)
    if item_type == ClassManagement.item_drop_data[0]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[0]["Value"]["ItemPool"], ClassManagement.item_drop_data[0]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[0]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[0]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[1]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[1]["Value"]["ItemPool"], ClassManagement.item_drop_data[1]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[1]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[1]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[2]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[2]["Value"]["ItemPool"], ClassManagement.item_drop_data[2]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[2]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[2]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[3]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = any_pick(ClassManagement.item_drop_data[3]["Value"]["ItemPool"], ClassManagement.item_drop_data[3]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::D2000"
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = ClassManagement.item_drop_data[3]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[4]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[4]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[4]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.item_drop_data[4]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.item_drop_data[4]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.item_drop_data[4]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.item_drop_data[4]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.item_drop_data[4]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.item_drop_data[4]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(ClassManagement.drop_content[i]["Value"]["CoinOverride"])
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = True
    elif item_type == ClassManagement.item_drop_data[5]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[5]["Value"]["ItemPool"], ClassManagement.item_drop_data[5]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[5]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[5]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[6]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[6]["Value"]["ItemPool"], ClassManagement.item_drop_data[6]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[6]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[6]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[7]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[7]["Value"]["ItemPool"], ClassManagement.item_drop_data[7]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[7]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[7]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[8]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[8]["Value"]["ItemPool"], ClassManagement.item_drop_data[8]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[8]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[8]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[9]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[9]["Value"]["ItemPool"], ClassManagement.item_drop_data[9]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[9]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[9]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[10]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[10]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[10]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.item_drop_data[10]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.item_drop_data[10]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.item_drop_data[10]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.item_drop_data[10]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.item_drop_data[10]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.item_drop_data[10]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(ClassManagement.drop_content[i]["Value"]["CoinOverride"])
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = True
    elif item_type == ClassManagement.item_drop_data[11]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[11]["Value"]["ItemPool"], ClassManagement.item_drop_data[11]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[11]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[11]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    elif item_type == ClassManagement.item_drop_data[12]["Key"]:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[12]["Value"]["ItemPool"], ClassManagement.item_drop_data[12]["Value"]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[12]["Value"]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[12]["Value"]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::None"
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = 0
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    
def patch_enemy_entry(item_type, item_rate, i):
    if item_type == ClassManagement.enemy_drop_data[0]["Key"]:
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[4]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[0]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[10]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[1]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[2]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[4]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[0]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == ClassManagement.enemy_drop_data[1]["Key"]:
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[10]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[1]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[2]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[4]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[0]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[10]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[1]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == ClassManagement.enemy_drop_data[2]["Key"]:
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[2]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[4]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[0]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data[0]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data[10]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[1]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data[1]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.enemy_drop_data[2]["Value"]["ItemPool"], ClassManagement.enemy_drop_data[2]["Value"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data[2]["Value"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0

def seed_convert(i):
    new_chest = ClassManagement.seed_conversion_data["Value"][ClassManagement.drop_content[i]["Key"]]
    for e in range(len(ClassManagement.drop_content)):
        if ClassManagement.drop_content[e]["Key"] == new_chest:
            return e

def unlock_all_quest():
    for i in range(56):
        ClassManagement.quest_content[i]["Value"]["NeedQuestID"] = "None"
        ClassManagement.quest_content[i]["Value"]["NeedAreaID"] = "None"
        ClassManagement.quest_content[i]["Value"]["NeedItemID"] = "None"
        ClassManagement.quest_content[i]["Value"]["NeedBossID"] = "None"
    ClassManagement.debug("ClassItem.unlock_all_quest()")

def rand_quest_requirement():
    #EnemyQuests
    for i in range(len(ClassManagement.enemy_location_data)):
        if ClassManagement.enemy_location_data[i]["Key"][0] != "N" or ClassManagement.enemy_location_data[i]["Key"] == "N2013":
            continue
        enemy_req_number.append(i)
    for i in range(19):
        enemy_req_index.append(any_pick(enemy_req_number, True, "None"))
    enemy_req_index.sort()
    for i in range(19):
        ClassManagement.quest_content[i]["Value"]["Enemy01"] = ClassManagement.enemy_location_data[enemy_req_index[i]]["Key"]
        ClassManagement.quest_content[i]["Value"]["EnemyNum01"] = len(ClassManagement.enemy_location_data[enemy_req_index[i]]["Value"]["NormalModeRooms"])
        enemy_room = ""
        for e in ClassManagement.enemy_location_data[enemy_req_index[i]]["Value"]["NormalModeRooms"]:
            enemy_room += e + ","
        ClassManagement.quest_content[i]["Value"]["EnemySpawnLocations"] = enemy_room[:-1]
    #MementoQuests
    i = 20
    while i <= 34:
        ClassManagement.quest_content[i]["Value"]["Item01"] = any_pick(ClassManagement.quest_requirement_data[0]["Value"]["ItemPool"], True, "None")
        i += 1
    #CateringQuests
    i = 35
    while i <= 55:
        ClassManagement.quest_content[i]["Value"]["Item01"] = any_pick(ClassManagement.quest_requirement_data[1]["Value"]["ItemPool"], True, "None")
        i += 1
    ClassManagement.debug("ClassItem.rand_quest_requirement()")

def no_enemy_quest_icon():
    for i in range(20):
        ClassManagement.quest_content[i]["Value"]["EnemySpawnLocations"] = "none"
    ClassManagement.debug("ClassItem.no_enemy_quest_icon()")

def rand_quest_pool():
    invert_ratio()
    for i in quest_index:
        item_type = random.choice(quest_type)
        if item_type == ClassManagement.item_drop_data[0]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[0]["Value"]["ItemPool"], ClassManagement.item_drop_data[0]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[0]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[0]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[1]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[1]["Value"]["ItemPool"], ClassManagement.item_drop_data[1]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[1]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[1]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[2]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[2]["Value"]["ItemPool"], ClassManagement.item_drop_data[2]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[2]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[2]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[3]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = "Money"
            ClassManagement.quest_content[i]["Value"]["RewardNum01"] = any_pick(ClassManagement.item_drop_data[3]["Value"]["ItemPool"], ClassManagement.item_drop_data[3]["Value"]["IsUnique"], item_type)
        elif item_type == ClassManagement.item_drop_data[4]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[4]["Value"]["ItemPool"], ClassManagement.item_drop_data[4]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[4]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[4]["Value"]["ItemQuantity"]*9
        elif item_type == ClassManagement.item_drop_data[5]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[5]["Value"]["ItemPool"], ClassManagement.item_drop_data[5]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[5]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[5]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[6]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[6]["Value"]["ItemPool"], ClassManagement.item_drop_data[6]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[6]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[6]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[7]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[7]["Value"]["ItemPool"], ClassManagement.item_drop_data[7]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[7]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[7]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[8]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[8]["Value"]["ItemPool"], ClassManagement.item_drop_data[8]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[8]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[8]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[9]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[9]["Value"]["ItemPool"], ClassManagement.item_drop_data[9]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[9]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[9]["Value"]["ItemQuantity"]*3
        elif item_type == ClassManagement.item_drop_data[10]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[10]["Value"]["ItemPool"], ClassManagement.item_drop_data[10]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[10]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[10]["Value"]["ItemQuantity"]*9
        elif item_type == ClassManagement.item_drop_data[12]["Key"]:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[12]["Value"]["ItemPool"], ClassManagement.item_drop_data[12]["Value"]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[12]["Value"]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[12]["Value"]["ItemQuantity"]*3
    invert_ratio()
    ClassManagement.debug("ClassItem.rand_quest_pool()")

def catering_quest_info():
    ClassManagement.scenario_content["Table"]["QST_Catering_Name01"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[35]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name02"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[50]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name03"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[51]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name04"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[42]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name05"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[41]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name06"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[39]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name07"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[44]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name08"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[38]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name09"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[52]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name10"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[45]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name11"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[40]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name12"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[49]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name13"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[46]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name14"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[37]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name15"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[53]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name16"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[47]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name17"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[36]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name18"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[54]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name19"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[43]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name20"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[48]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name21"] = ClassManagement.item_translation["Value"][ClassManagement.quest_content[55]["Value"]["Item01"]]
    ClassManagement.debug("ClassItem.catering_quest_info()")

def all_hair_in_shop():
    i = 521
    while i <= 532:
        ClassManagement.item_content[i]["Value"]["buyPrice"] = 100
        ClassManagement.item_content[i]["Value"]["Producted"] = "Event_01_001_0000"
        i += 1
    ClassManagement.debug("ClassItem.all_hair_in_shop()")

def no_card_in_shop():
    ClassManagement.item_content[561]["Value"]["buyPrice"] = 0
    ClassManagement.item_content[561]["Value"]["sellPrice"] = 0
    ClassManagement.debug("ClassItem.no_card_in_shop()")

def rand_shop_pool():
    for i in ClassManagement.item_drop_data:
        for e in shop_skip_list:
            while e in i["Value"]["ItemPool"]:
                i["Value"]["ItemPool"].remove(e)
        chosen = []
        for e in range(i["Value"]["ShopRatio"]):
            if i["Value"]["ItemPool"]:
                chosen.append(any_pick(i["Value"]["ItemPool"], True, "None"))
        for e in ClassManagement.item_content:
            if e["Key"] in shop_skip_list:
                continue
            if e["Key"] in chosen:
                e["Value"]["Producted"] = random.choice(event_type)
            elif e["Value"]["ItemType"] == i["Value"]["ShopName"]:
                e["Value"]["Producted"] = "None"
    ClassManagement.debug("ClassItem.rand_shop_pool()")

def rand_shop_price(scale):
    for i in ClassManagement.item_content:
        if i["Key"] in shop_skip_list:
            continue
        chosen = random.choice(base)
        if chosen < 500000:
            if chosen >= 100:
                chosen += random.choice(ten)
            if chosen >= 1000:
                chosen += random.choice(hundred)
            if chosen >= 10000:
                chosen += random.choice(thousand)
            if chosen >= 100000:
                chosen += random.choice(ten_thousand)
        i["Value"]["buyPrice"] = chosen
        if not scale:
            chosen = random.choice(base)
            if chosen < 500000:
                if chosen >= 100:
                    chosen += random.choice(ten)
                if chosen >= 1000:
                    chosen += random.choice(hundred)
                if chosen >= 10000:
                    chosen += random.choice(thousand)
                if chosen >= 100000:
                    chosen += random.choice(ten_thousand)
        if i["Value"]["ItemType"] == "ECarriedCatalog::Ingredient" or i["Value"]["ItemType"] == "ECarriedCatalog::FoodStuff" or i["Value"]["ItemType"] == "ECarriedCatalog::Seed":
            i["Value"]["sellPrice"] = 0
        else:
            i["Value"]["sellPrice"] = round(chosen/10)
    ClassManagement.debug("ClassItem.rand_shop_price(" + str(scale) + ")")

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
    for i in ClassManagement.item_drop_data:
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

def get_log():
    return log