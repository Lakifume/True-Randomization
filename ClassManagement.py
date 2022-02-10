import os
import shutil
import json
from enum import Enum
from collections import OrderedDict

class Direction(Enum):
    LEFT         = 0x0001
    BOTTOM       = 0x0002
    RIGHT        = 0x0004
    TOP          = 0x0008
    LEFT_BOTTOM  = 0x0010
    RIGHT_BOTTOM = 0x0020
    LEFT_TOP     = 0x0040
    RIGHT_TOP    = 0x0080
    TOP_LEFT     = 0x0100
    TOP_RIGHT    = 0x0200
    BOTTOM_RIGHT = 0x0400
    BOTTOM_LEFT  = 0x0800

OppositeDirection = {
    Direction.LEFT:         Direction.RIGHT,
    Direction.BOTTOM:       Direction.TOP,
    Direction.RIGHT:        Direction.LEFT,
    Direction.TOP:          Direction.BOTTOM,
    Direction.LEFT_BOTTOM:  Direction.RIGHT_BOTTOM,
    Direction.RIGHT_BOTTOM: Direction.LEFT_BOTTOM,
    Direction.LEFT_TOP:     Direction.RIGHT_TOP,
    Direction.RIGHT_TOP:    Direction.LEFT_TOP,
    Direction.TOP_LEFT:     Direction.BOTTOM_LEFT,
    Direction.TOP_RIGHT:    Direction.BOTTOM_RIGHT,
    Direction.BOTTOM_RIGHT: Direction.TOP_RIGHT,
    Direction.BOTTOM_LEFT:  Direction.TOP_LEFT,
}

class Door:
    def __init__(self, x_block, z_block, direction_part, breakable):
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        self.breakable = breakable

used_doors = []

def open_content():
    global armor_content
    with open("Serializer\\Json\\PB_DT_ArmorMaster.json", "r") as file_reader:
        armor_content = json.load(file_reader)
    
    global ballistic_content
    with open("Serializer\\Json\\PB_DT_BallisticMaster.json", "r") as file_reader:
        ballistic_content = json.load(file_reader)
    
    global book_content
    with open("Serializer\\Json\\PB_DT_BookMaster.json", "r") as file_reader:
        book_content = json.load(file_reader)
    
    global attack_content
    with open("Serializer\\Json\\PB_DT_BRVAttackDamage.json", "r") as file_reader:
        attack_content = json.load(file_reader)
    
    global bullet_content
    with open("Serializer\\Json\\PB_DT_BulletMaster.json", "r") as file_reader:
        bullet_content = json.load(file_reader)
    
    global character_content
    with open("Serializer\\Json\\PB_DT_CharacterParameterMaster.json", "r") as file_reader:
        character_content = json.load(file_reader)
    
    global collision_content
    with open("Serializer\\Json\\PB_DT_CollisionMaster.json", "r") as file_reader:
        collision_content = json.load(file_reader)
    
    global coordinate_content
    with open("Serializer\\Json\\PB_DT_CoordinateParameter.json", "r") as file_reader:
        coordinate_content = json.load(file_reader)
    
    global craft_content
    with open("Serializer\\Json\\PB_DT_CraftMaster.json", "r") as file_reader:
        craft_content = json.load(file_reader)
    
    global damage_content
    with open("Serializer\\Json\\PB_DT_DamageMaster.json", "r") as file_reader:
        damage_content = json.load(file_reader)
    
    global dialogue_content
    with open("Serializer\\Json\\PB_DT_DialogueTableItems.json", "r") as file_reader:
        dialogue_content = json.load(file_reader)
    
    global drop_content
    with open("Serializer\\Json\\PB_DT_DropRateMaster.json", "r") as file_reader:
        drop_content = json.load(file_reader)
    
    global item_content
    with open("Serializer\\Json\\PB_DT_ItemMaster.json", "r") as file_reader:
        item_content = json.load(file_reader)
    
    global quest_content
    with open("Serializer\\Json\\PB_DT_QuestMaster.json", "r") as file_reader:
        quest_content = json.load(file_reader)
    
    global shard_content
    with open("Serializer\\Json\\PB_DT_ShardMaster.json", "r") as file_reader:
        shard_content = json.load(file_reader)
    
    global effect_content
    with open("Serializer\\Json\\PB_DT_SpecialEffectDefinitionMaster.json", "r") as file_reader:
        effect_content = json.load(file_reader)
    
    global weapon_content
    with open("Serializer\\Json\\PB_DT_WeaponMaster.json", "r") as file_reader:
        weapon_content = json.load(file_reader)
    
    global master_content
    with open("Serializer\\Json\\PBMasterStringTable.json", "r") as file_reader:
        master_content = json.load(file_reader)
    
    global scenario_content
    with open("Serializer\\Json\\PBScenarioStringTable.json", "r") as file_reader:
        scenario_content = json.load(file_reader)
    
    global system_content
    with open("Serializer\\Json\\PBSystemStringTable.json", "r") as file_reader:
        system_content = json.load(file_reader)
    
    global room_content
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json", "r") as file_reader:
        room_content = json.load(file_reader)
    debug("ClassManagement.open_content()")
    
def open_data():
    global enemy_drop_data
    with open("Data\\Constant\\EnemyDrop.json", "r") as file_reader:
        enemy_drop_data = json.load(file_reader)
    
    global enemy_location_data
    with open("Data\\Constant\\EnemyLocation.json", "r") as file_reader:
        enemy_location_data = json.load(file_reader)
    
    global item_drop_data
    with open("Data\\Constant\\ItemDrop.json", "r") as file_reader:
        item_drop_data = json.load(file_reader)
    
    global quest_requirement_data
    with open("Data\\Constant\\QuestRequirement.json", "r") as file_reader:
        quest_requirement_data = json.load(file_reader)
    
    global shard_base_data
    with open("Data\\Constant\\ShardBase.json", "r") as file_reader:
        shard_base_data = json.load(file_reader)
    
    global shard_drop_data
    with open("Data\\Constant\\ShardDrop.json", "r") as file_reader:
        shard_drop_data = json.load(file_reader)
    
    global shard_range_data
    with open("Data\\Constant\\ShardRange.json", "r") as file_reader:
        shard_range_data = json.load(file_reader)
    
    global logic_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.logic", "r") as file_reader:
        logic_data = json.load(file_reader)
    
    global order_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.order", "r") as file_reader:
        order_data = json.load(file_reader)
    
    global original_order_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.order", "r") as file_reader:
        original_order_data = json.load(file_reader)
    debug("ClassManagement.open_data()")
    
def open_translation():
    global bloodless_translation
    with open("Data\\Translation\\BloodlessTranslation.json", "r") as file_reader:
        bloodless_translation = json.load(file_reader)
    
    global enemy_translation
    with open("Data\\Translation\\EnemyTranslation.json", "r") as file_reader:
        enemy_translation = json.load(file_reader)
    
    global item_translation
    with open("Data\\Translation\\ItemTranslation.json", "r") as file_reader:
        item_translation = json.load(file_reader)
    
    global shard_translation
    with open("Data\\Translation\\ShardTranslation.json", "r") as file_reader:
        shard_translation = json.load(file_reader)
    debug("ClassManagement.open_translation()")

def load_custom_map(path):
    global room_content
    with open(path, "r") as file_reader:
        room_content = json.load(file_reader)
    #UndergroundBigRoomsInitialFix
    for i in range(len(room_content[295]["Value"]["NoTraverse"])):
        room_content[295]["Value"]["NoTraverse"][i] += room_content[295]["Value"]["AreaWidthSize"]*2
    for i in range(len(room_content[313]["Value"]["NoTraverse"])):
        room_content[313]["Value"]["NoTraverse"][i] += room_content[313]["Value"]["AreaWidthSize"]*3
    #UndergroundBigRoomsNegativeOffset
    if room_content[295]["Value"]["OffsetZ"] < 0:
        multiplier = abs(int(room_content[295]["Value"]["OffsetZ"]/7.2)) - 1
        if multiplier > room_content[295]["Value"]["AreaHeightSize"] - 1:
            multiplier = room_content[295]["Value"]["AreaHeightSize"] - 1
        for i in range(len(room_content[295]["Value"]["NoTraverse"])):
            room_content[295]["Value"]["NoTraverse"][i] -= room_content[295]["Value"]["AreaWidthSize"]*multiplier
    if room_content[313]["Value"]["OffsetZ"] < 0:
        multiplier = abs(int(room_content[313]["Value"]["OffsetZ"]/7.2)) - 1
        if multiplier > room_content[313]["Value"]["AreaHeightSize"] - 1:
            multiplier = room_content[313]["Value"]["AreaHeightSize"] - 1
        for i in range(len(room_content[313]["Value"]["NoTraverse"])):
            room_content[313]["Value"]["NoTraverse"][i] -= room_content[313]["Value"]["AreaWidthSize"]*multiplier
    #GlobalMapDisplayFix
    for i in room_content:
        if i["Value"]["OffsetX"] < 214.2:
            i["Value"]["AreaID"] = "EAreaID::m01SIP"
        elif i["Value"]["OffsetX"] + i["Value"]["AreaWidthSize"]*12.6 > 1108.8:
            i["Value"]["AreaID"] = "EAreaID::m13ARC"
        else:
            i["Value"]["AreaID"] = "EAreaID::m03ENT"
    debug("ClassManagement.load_custom_map(" + path + ")")

def load_custom_logic(path):
    global logic_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".logic"):
        with open(name + ".logic", "r") as file_reader:
            logic_data = json.load(file_reader)
    debug("ClassManagement.load_custom_logic(" + path + ")")

def load_custom_order(path):
    global order_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".order"):
        with open(name + ".order", "r") as file_reader:
            order_data = json.load(file_reader)
    debug("ClassManagement.load_custom_order(" + path + ")")

def create_log(path):
    name, extension = os.path.splitext(path)
    global log
    log = name.split("\\")[-1]
    debug("ClassManagement.create_log(" + path + ")")

def write_log(filename, filepath, log, ascii):
    with open(filepath + "\\" + filename + ".json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=ascii, indent=2))
    debug("ClassManagement.write_log(" + filename + ", " + filepath + ", " + "[log]" + ", " + str(ascii) + ")")

def write_json(filename, filepath, content, ascii):
    with open("Serializer\\" + filename + ".json", "w") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=ascii, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    if filename == "PB_DT_RoomMaster":
        os.system("cmd /c UAsset2Json.exe -tobin -force " + filename + ".json")
    else:
        os.system("cmd /c UAsset2Json.exe -tobin " + filename + ".json")
    os.chdir(root)
    shutil.move("Serializer\\" + filename + ".bin", "UnrealPak\\Mod\\BloodstainedRotN\\" + filepath + "\\" + filename + ".uasset")
    os.remove("Serializer\\" + filename + ".json")
    debug("ClassManagement.write_patched_json(" + filename + ", " + filepath + ", [content], " + str(ascii) + ")")

def write_miriam_candle():
    print("mXXXXX_XXX_Gimmick.umap")
    i = 627
    while i <= 629:
        candle_process(drop_content[i]["Value"]["ShardId"], drop_content[i]["Key"].split("_")[0])
        i += 1
    print("Done")
    debug("ClassManagement.write_miriam_candle()")

def write_bloodless_candle(datatable):
    #Start
    print("mXXXXX_XXX_Gimmick.umap")
    tower_check = 0
    for i in datatable:
        #RoomToFile
        file_name = datatable[i].replace(")", "").split("(")[0] + "_Gimmick"
        #TowerCheck
        if datatable[i] == "m08TWR_019":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_BLOOD_STEAL"
        elif datatable[i] == "m08TWR_019(2)":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP"
        else:
            search = "EPBBloodlessAbilityType::"
        #ReadJson
        if "m08TWR_019" in file_name and tower_check == 1:
            with open("UAssetGUI\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        else:
            with open("UAssetGUI\\Json\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        #PatchJson
        for e in content["Exports"]:
            try:
                if search in e["Data"][1]["Value"]:
                    e["Data"][1]["Value"] = "EPBBloodlessAbilityType::" + i
            except TypeError:
                continue
            except IndexError:
                continue
        for e in range(len(content["NameMap"])):
            if search in content["NameMap"][e]:
                content["NameMap"][e] = "EPBBloodlessAbilityType::" + i[:-3]
        #WriteJson
        with open("UAssetGUI\\" + file_name + ".json", "w") as file_writer:
            file_writer.write(json.dumps(content))
        #UAssetGUI
        if not ("m08TWR_019" in file_name and tower_check == 0):
            #CommandFromJson
            root = os.getcwd()
            os.chdir("UAssetGUI")
            os.system("cmd /c UAssetGUI.exe fromjson " + file_name + ".json " + file_name + ".umap")
            os.chdir(root)
            #Move
            shutil.move("UAssetGUI\\" + file_name + ".umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name + ".umap")
            #Delete
            os.remove("UAssetGUI\\" + file_name + ".json")
        #TowerCheck
        if "m08TWR_019" in file_name:
            tower_check += 1
    #Done
    print("Done")
    debug("ClassManagement.write_bloodless_candle([datatable])")

def candle_process(shard, candle):
    for i in shard_content:
        if i["Key"] == candle:
            candle_type = i["Value"]["ShardType"]
        if i["Key"] == shard:
            shard_type = i["Value"]["ShardType"]
    for i in enemy_location_data[candle]["NormalModeRooms"]:
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

def convert_umap_to_json():
    for i in os.listdir("UAssetGUI\\Umap"):
        shutil.copyfile("UAssetGUI\\Umap\\" + i, "UAssetGUI\\" + i)
        
        root = os.getcwd()
        os.chdir("UAssetGUI")
        os.system("cmd /c UAssetGUI.exe tojson " + i + " " + i[:-5] + ".json 514")
        os.chdir(root)
        
        shutil.move("UAssetGUI\\" + i[:-5] + ".json", "UAssetGUI\\Json\\" + i[:-5] + ".json")
        os.remove("UAssetGUI\\" + i)

def copy_file(filename, extension, source, destination):
    shutil.copyfile(source + "\\" + filename + "." + extension, "UnrealPak\\Mod\\BloodstainedRotN\\" + destination + "\\" + filename + "." + extension)
    debug("ClassManagement.copy_file(" + filename + ", " + extension + ", " + source + ", " + destination + ")")

def convert_flag_to_door(door_flag, width):
    door_list = []
    for i in range(0, len(door_flag), 2):
        tile_index = door_flag[i]
        direction = door_flag[i+1]
        tile_index -= 1
        if width == 0:
            x_block = tile_index
            z_block = 0
        else:
            x_block = tile_index % width
            z_block = tile_index // width
        for direction_part in Direction:
            if (direction & direction_part.value) != 0:
                breakable = (direction & (direction_part.value << 16)) != 0
                door = Door(x_block, z_block, direction_part, breakable)
                door_list.append(door)
    return door_list

def convert_door_to_flag(door_list, width):
    door_flags_by_coords = OrderedDict()
    for door in door_list:
        coords = (door.x_block, door.z_block)
        if coords not in door_flags_by_coords:
            door_flags_by_coords[coords] = 0
            
        door_flags_by_coords[coords] |= door.direction_part.value
        if door.breakable:
            door_flags_by_coords[coords] |= (door.direction_part.value << 16)
        
    door_flag = []
    for (x, z), dir_flags in door_flags_by_coords.items():
        tile_index_in_room = z*width + x
        tile_index_in_room += 1
        door_flag += [tile_index_in_room, dir_flags]
    return door_flag

def room_final():
    global room_content
    #SameCheck
    for i in room_content:
        if i["Value"]["OutOfMap"]:
            continue
        for e in room_content:
            if e["Value"]["OutOfMap"]:
                continue
            #SameRoom
            if i["Value"]["OffsetX"] == e["Value"]["OffsetX"] and i["Value"]["OffsetZ"] == e["Value"]["OffsetZ"] and i["Key"] != e["Key"]:
                i["Value"]["SameRoom"] = e["Key"]
                break;
            else:
                i["Value"]["SameRoom"] = "None"
    #AdjacentCheck
    for i in room_content:
        i["Value"]["AdjacentRoomName"].clear()
        used_doors.clear()
        if i["Value"]["WarpPositionX"] == -1.0:
            i["Value"]["DoorFlag"].clear()
            continue
        door_1 = convert_flag_to_door(i["Value"]["DoorFlag"], i["Value"]["AreaWidthSize"])
        for e in room_content:
            if i["Value"]["OutOfMap"] != e["Value"]["OutOfMap"] or e["Value"]["WarpPositionX"] == -1.0:
                continue
            door_2 = convert_flag_to_door(e["Value"]["DoorFlag"], e["Value"]["AreaWidthSize"])
            #AdjacentRoom
            check = False
            if left_check(i, e):
                if i["Value"]["OutOfMap"]:
                    check = True
                else:
                    check = door_vertical_check(door_1, door_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP, i["Value"]["OffsetZ"], e["Value"]["OffsetZ"])
            elif bottom_check(i, e):
                if i["Value"]["OutOfMap"]:
                    check = True
                else:
                    check = door_horizontal_check(door_1, door_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT, i["Value"]["OffsetX"], e["Value"]["OffsetX"])
            elif right_check(i, e):
                if i["Value"]["OutOfMap"]:
                    check = True
                else:
                    check = door_vertical_check(door_1, door_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP, i["Value"]["OffsetZ"], e["Value"]["OffsetZ"])
            elif top_check(i, e):
                if i["Value"]["OutOfMap"]:
                    check = True
                else:
                    check = door_horizontal_check(door_1, door_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT, i["Value"]["OffsetX"], e["Value"]["OffsetX"])
            if check:
                #TransitionFix
                if not (e["Value"]["RoomType"] == "ERoomType::Load" and e["Key"][0:6] != i["Key"][0:6] and e["Value"]["SameRoom"] != "None" and e["Key"] != "m02VIL(1201)" and e["Value"]["SameRoom"] != "m03ENT(1201)"):
                    #VillageTransitionFix
                    if e["Value"]["SameRoom"] != "m02VIL(1201)" and e["Key"] != "m03ENT(1201)":
                        i["Value"]["AdjacentRoomName"].append(e["Key"])
        for e in list(door_1):
            if not e in used_doors:
                door_1.remove(e)
        i["Value"]["DoorFlag"] = convert_door_to_flag(door_1, i["Value"]["AreaWidthSize"])
    #VeparFix
    if "m02VIL_001" in room_content[22]["Value"]["AdjacentRoomName"]:
        room_content[22]["Value"]["AdjacentRoomName"].remove("m02VIL_001")
    if "m01SIP_022" in room_content[32]["Value"]["AdjacentRoomName"]:
        room_content[32]["Value"]["AdjacentRoomName"].remove("m01SIP_022")
    if not "m02VIL_000" in room_content[22]["Value"]["AdjacentRoomName"]:
        room_content[22]["Value"]["AdjacentRoomName"].append("m02VIL_000")
    #TowerFix
    if not "m08TWR_017" in room_content[227]["Value"]["AdjacentRoomName"]:
        room_content[227]["Value"]["AdjacentRoomName"].append("m08TWR_017")
    if not "m08TWR_018" in room_content[232]["Value"]["AdjacentRoomName"]:
        room_content[232]["Value"]["AdjacentRoomName"].append("m08TWR_018")
    if not "m08TWR_018" in room_content[233]["Value"]["AdjacentRoomName"]:
        room_content[233]["Value"]["AdjacentRoomName"].append("m08TWR_018")
    if not "m08TWR_019" in room_content[243]["Value"]["AdjacentRoomName"]:
        room_content[243]["Value"]["AdjacentRoomName"].append("m08TWR_019")
    
    if not "m08TWR_000" in room_content[244]["Value"]["AdjacentRoomName"]:
        room_content[244]["Value"]["AdjacentRoomName"].append("m08TWR_000")
    if not "m08TWR_005" in room_content[245]["Value"]["AdjacentRoomName"]:
        room_content[245]["Value"]["AdjacentRoomName"].append("m08TWR_005")
    if not "m08TWR_006" in room_content[245]["Value"]["AdjacentRoomName"]:
        room_content[245]["Value"]["AdjacentRoomName"].append("m08TWR_006")
    if not "m08TWR_016" in room_content[246]["Value"]["AdjacentRoomName"]:
        room_content[246]["Value"]["AdjacentRoomName"].append("m08TWR_016")
    
    room_content[227]["Value"]["DoorFlag"].insert(0, 1)
    room_content[227]["Value"]["DoorFlag"].insert(0, 1)
    room_content[232]["Value"]["DoorFlag"].append(4)
    room_content[232]["Value"]["DoorFlag"].append(4)
    room_content[233]["Value"]["DoorFlag"].insert(0, 1)
    room_content[233]["Value"]["DoorFlag"].insert(0, 1)
    room_content[243]["Value"]["DoorFlag"].insert(0, 4)
    room_content[243]["Value"]["DoorFlag"].insert(0, 2)
    
    room_content[244]["Value"]["DoorFlag"].append(18)
    room_content[244]["Value"]["DoorFlag"].append(8)
    room_content[245]["Value"]["DoorFlag"].append(3)
    room_content[245]["Value"]["DoorFlag"].append(2)
    room_content[245]["Value"]["DoorFlag"].append(34)
    room_content[245]["Value"]["DoorFlag"].append(8)
    room_content[246]["Value"]["DoorFlag"].append(39)
    room_content[246]["Value"]["DoorFlag"].append(8)
    #GebelFix
    if not "m02VIL_099" in room_content[166]["Value"]["AdjacentRoomName"]:
        room_content[166]["Value"]["AdjacentRoomName"].append("m02VIL_099")
    #BaelFix
    if not "m02VIL_099" in room_content[475]["Value"]["AdjacentRoomName"]:
        room_content[475]["Value"]["AdjacentRoomName"].append("m02VIL_099")
    #ICE_020Fix
    room_content[480]["Value"]["DoorFlag"] = [2, 4]

def left_check(i, e):
    return bool(e["Value"]["OffsetX"] == round(i["Value"]["OffsetX"] - 12.6 * e["Value"]["AreaWidthSize"], 1) and round(i["Value"]["OffsetZ"] - 7.2 * (e["Value"]["AreaHeightSize"] - 1), 1) <= e["Value"]["OffsetZ"] <= round(i["Value"]["OffsetZ"] + 7.2 * (i["Value"]["AreaHeightSize"] - 1), 1))

def bottom_check(i, e):
    return bool(round(i["Value"]["OffsetX"] - 12.6 * (e["Value"]["AreaWidthSize"] - 1), 1) <= e["Value"]["OffsetX"] <= round(i["Value"]["OffsetX"] + 12.6 * (i["Value"]["AreaWidthSize"] - 1), 1) and e["Value"]["OffsetZ"] == round(i["Value"]["OffsetZ"] - 7.2 * e["Value"]["AreaHeightSize"], 1))

def right_check(i, e):
    return bool(e["Value"]["OffsetX"] == round(i["Value"]["OffsetX"] + 12.6 * i["Value"]["AreaWidthSize"], 1) and round(i["Value"]["OffsetZ"] - 7.2 * (e["Value"]["AreaHeightSize"] - 1), 1) <= e["Value"]["OffsetZ"] <= round(i["Value"]["OffsetZ"] + 7.2 * (i["Value"]["AreaHeightSize"] - 1), 1))

def top_check(i, e):
    return bool(round(i["Value"]["OffsetX"] - 12.6 * (e["Value"]["AreaWidthSize"] - 1), 1) <= e["Value"]["OffsetX"] <= round(i["Value"]["OffsetX"] + 12.6 * (i["Value"]["AreaWidthSize"] - 1), 1) and e["Value"]["OffsetZ"] == round(i["Value"]["OffsetZ"] + 7.2 * i["Value"]["AreaHeightSize"], 1))

def door_vertical_check(door_1, door_2, direction_1, direction_2, direction_3, offset_1, offset_2):
    check = False
    for i in door_1:
        if i.direction_part == direction_1:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_1] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_2:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_2] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_3:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_3] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
    return check

def door_horizontal_check(door_1, door_2, direction_1, direction_2, direction_3, offset_1, offset_2):
    check = False
    for i in door_1:
        if i.direction_part == direction_1:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_1] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_2:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_2] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_3:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_3] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
    return check

def debug(line):
    with open("SpoilerLog\\~debug.txt", "a") as file:
        file.write(line + "\n")