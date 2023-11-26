from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Graphic
import Sound
import Bloodless
import Utility

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
    def __init__(self, room, x_block, z_block, direction_part, breakable):
        self.room = room
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        self.breakable = breakable

def init():
    global c_cat_actors
    c_cat_actors = [
        "PBEasyTreasureBox_BP_C",
        "PBEasyTreasureBox_BP_C(Gold)",
        "PBPureMiriamTreasureBox_BP_C",
        "PBBakkerDoor_BP_C",
        "Chr_N3016_C",
        "Chr_N3028_C",
        "Chr_N3066_C",
        "Chr_N3067_C",
        "Chr_N3124_C",
        "IncubatorGlass_BP_C"
    ]
    global room_to_gimmick
    room_to_gimmick = {
        "m01SIP_007": "m01SIP_007_BG",
        "m20JRN_003": "m20JRN_003_Setting",
        "m20JRN_004": "m20JRN_004_BG"
    }
    global boss_door_rooms
    boss_door_rooms = [
        "m03ENT_011",
        "m03ENT_014",
        "m05SAN_011",
        "m05SAN_022",
        "m07LIB_010",
        "m07LIB_037",
        "m07LIB_039",
        "m08TWR_019",
        "m13ARC_002",
        "m13ARC_006",
        "m14TAR_003",
        "m14TAR_005",
        "m15JPN_015",
        "m17RVA_007",
        "m17RVA_009",
        "m18ICE_002",
        "m18ICE_005",
        "m18ICE_010",
        "m18ICE_017",
        "m20JRN_002"
    ]
    global backer_door_rooms
    backer_door_rooms = [
        "m04GDN_006",
        "m06KNG_013",
        "m07LIB_036",
        "m15JPN_011"
    ]
    global area_door_rooms
    area_door_rooms = [
        "m02VIL_012",
        "m03ENT_000",
        "m03ENT_007",
        "m03ENT_008",
        "m03ENT_016",
        "m03ENT_018",
        "m03ENT_019",
        "m04GDN_000",
        "m04GDN_003",
        "m04GDN_015",
        "m04GDN_016",
        "m04GDN_017",
        "m05SAN_000",
        "m05SAN_001",
        "m05SAN_003",
        "m05SAN_010",
        "m05SAN_021",
        "m05SAN_024",
        "m06KNG_000",
        "m06KNG_008",
        "m07LIB_000",
        "m07LIB_021",
        "m07LIB_039",
        "m08TWR_003",
        "m08TWR_017",
        "m09TRN_000",
        "m09TRN_005",
        "m10BIG_018",
        "m11UGD_000",
        "m11UGD_014",
        "m11UGD_026",
        "m11UGD_033",
        "m11UGD_036",
        "m11UGD_046",
        "m11UGD_055",
        "m11UGD_057",
        "m12SND_000",
        "m12SND_011",
        "m13ARC_000",
        "m14TAR_000",
        "m14TAR_009",
        "m15JPN_000",
        "m15JPN_007",
        "m17RVA_000",
        "m17RVA_014",
        "m18ICE_000"
    ]
    global bookshelf_rooms
    bookshelf_rooms = [
        "m01SIP_005",
        "m01SIP_012",
        "m02VIL_007",
        "m03ENT_002",
        "m03ENT_004",
        "m03ENT_005",
        "m03ENT_011",
        "m03ENT_012",
        "m04GDN_005",
        "m04GDN_006",
        "m04GDN_011",
        "m05SAN_000",
        "m05SAN_003",
        "m05SAN_005",
        "m05SAN_009",
        "m05SAN_021",
        "m06KNG_003",
        "m06KNG_015",
        "m06KNG_018",
        "m07LIB_000",
        "m07LIB_010",
        "m07LIB_018",
        "m07LIB_036",
        "m08TWR_000",
        "m08TWR_003",
        "m08TWR_010",
        "m08TWR_014",
        "m09TRN_005",
        "m10BIG_009",
        "m11UGD_000",
        "m11UGD_006",
        "m11UGD_032",
        "m12SND_021",
        "m13ARC_002",
        "m13ARC_006",
        "m14TAR_001",
        "m15JPN_015",
        "m17RVA_007",
        "m18ICE_002"
    ]
    global rotating_room_to_center
    rotating_room_to_center = {
        "m02VIL_008": (2280, -2280),
        "m02VIL_011": (5218, -2310),
        "m08TWR_017": (2400,     0),
        "m08TWR_018": (2400,     0),
        "m08TWR_019": (2520,     0),
        "m09TRN_001": (2390, -2460),
        "m12SND_025": ( 120,  -450),
        "m12SND_026": ( 120,  -450),
        "m12SND_027": ( 120,  -450)
    }
    global wall_to_gimmick_flag
    wall_to_gimmick_flag = {
        "SIP_006_0_0_RIGHT_BOTTOM": "SIP_006_DestructibleWall",
        "SIP_006_0_2_RIGHT":        "SIP_017_BreakWallCannon",
        "SIP_017_0_0_LEFT":         "SIP_017_BreakWallCannon",
        "VIL_006_3_0_BOTTOM":       "VIL_006_HardFloor1F",
        "VIL_009_0_0_LEFT_BOTTOM":  "VIL_009_DestructibleWall",
        "ENT_018_0_0_BOTTOM":       "ENT_018_DestructibleFloor",
        "GDN_013_0_0_LEFT":         "GDN_013_DestructibleWall",
        "SAN_019_1_0_BOTTOM":       "SAN_019_DestructibleFloor",
        "KNG_013_0_0_LEFT":         "KNG_013_DestructibleWall",
        "KNG_015_0_2_TOP":          "KNG_015_DestructibleRoof",
        "KNG_017_0_0_LEFT":         "KNG_017_DestructibleWall",
        "LIB_029_1_1_TOP":          "LIB_029_DestructibleCeil",
        "UGD_003_1_3_RIGHT":        "UGD_003_DestructibleWall1",
        "UGD_003_1_0_RIGHT":        "UGD_003_DestructibleWall2",
        "UGD_042_1_0_RIGHT":        "UGD_042_DestructibleWall",
        "SND_002_0_0_LEFT":         "SND_002_DestructibleWall",
        "ARC_003_0_0_RIGHT":        "ARC_002_DestructibleWall",
        "ARC_006_0_0_BOTTOM":       "ARC_006_DestructibleFloor",
        "JPN_003_0_0_LEFT":         "JPN_003_DestructibleWall",
        "RVA_003_1_0_RIGHT":        "RVA_003_DestructibleWall",
        "RVA_014_0_0_RIGHT":        "RVA_014_DestructibleWall"
    }
    global door_skip
    door_skip = [
        "VIL_008_3_0_RIGHT",
        "VIL_008_3_0_BOTTOM_RIGHT",
        "VIL_011_5_0_RIGHT",
        "VIL_011_5_0_TOP_RIGHT",
        "SND_025_0_0_LEFT",
        "SND_026_0_0_LEFT",
        "SND_027_0_0_LEFT"
    ]
    global arched_doors
    arched_doors = [
        "GDN_009_0_0_LEFT",
        "GDN_009_0_1_LEFT",
        "GDN_009_2_0_RIGHT",
        "SAN_015_0_0_LEFT",
        "SAN_015_1_0_RIGHT",
        "SAN_017_0_0_LEFT",
        "SAN_017_1_0_RIGHT",
        "SAN_018_0_0_LEFT",
        "SAN_018_1_0_RIGHT",
        "SAN_020_0_0_LEFT",
        "SAN_020_1_0_RIGHT",
        "SAN_020_0_1_LEFT",
        "SAN_020_1_1_RIGHT"
    ]
    global floorless_doors
    floorless_doors = [
        "SIP_006_0_2_RIGHT",
        "SIP_017_0_0_LEFT",
        "VIL_006_0_1_LEFT",
        "GDN_006_0_0_LEFT",
        "GDN_013_0_0_LEFT",
        "SAN_009_0_1_LEFT",
        "SAN_009_1_1_RIGHT",
        "SAN_021_0_1_LEFT",
        "SAN_021_1_1_RIGHT",
        "KNG_010_1_1_RIGHT",
        "KNG_013_0_0_LEFT",
        "KNG_017_0_0_LEFT",
        "LIB_003_0_1_RIGHT",
        "LIB_023_0_0_LEFT",
        "LIB_023_0_0_RIGHT",
        "UGD_006_0_2_LEFT",
        "UGD_016_0_1_RIGHT",
        "UGD_019_0_2_LEFT",
        "UGD_019_1_2_RIGHT",
        "UGD_020_0_0_LEFT",
        "UGD_021_0_0_LEFT",
        "UGD_029_0_1_LEFT",
        "UGD_056_0_3_LEFT",
        "ARC_002_1_1_RIGHT",
        "ARC_003_0_0_RIGHT",
        "JPN_010_0_0_LEFT",
        "JPN_010_0_1_LEFT",
        "JPN_010_3_0_RIGHT",
        "JPN_011_0_0_RIGHT",
        "JPN_012_0_0_LEFT",
        "JPN_012_3_0_RIGHT",
        "JPN_014_0_0_LEFT",
        "JPN_014_3_0_RIGHT",
        "JPN_015_0_0_RIGHT",
        "JPN_015_0_1_LEFT",
        "JPN_015_0_1_RIGHT",
        "RVA_001_0_1_LEFT",
        "ICE_005_0_2_LEFT",
        "ICE_016_0_1_RIGHT"
    ]
    global open_transition_doors
    open_transition_doors = [
        "LIB_008_0_1_RIGHT",
        "UGD_019_1_0_RIGHT",
        "UGD_021_0_0_LEFT",
        "UGD_022_1_0_RIGHT",
        "UGD_023_0_0_LEFT",
        "UGD_023_1_0_RIGHT",
        "UGD_024_0_2_LEFT",
        "UGD_024_1_1_RIGHT",
        "UGD_025_0_1_LEFT",
        "UGD_042_0_0_LEFT",
        "UGD_042_1_0_RIGHT",
        "UGD_044_0_0_LEFT",
        "UGD_045_0_0_LEFT",
        "UGD_045_1_0_RIGHT",
        "UGD_046_1_0_RIGHT"
    ]
    global transitionless_doors
    transitionless_doors = [
        "KNG_013_0_0_RIGHT",
        "TWR_009_0_10_RIGHT"
    ]
    global room_to_boss
    room_to_boss = {
        "m03ENT_013": "N1011",
        "m05SAN_012": "N1003",
        "m07LIB_011": "N2004",
        "m13ARC_005": "N1006",
        "m07LIB_038": "N2008",
        "m05SAN_023": "N1002",
        "m14TAR_004": "N2007",
        "m17RVA_008": "N2006",
        "m15JPN_016": "N1011_STRONG",
        "m18ICE_004": "N2012",
        "m18ICE_018": "N1008",
        "m18ICE_019": "N1009_Enemy",
        "m20JRN_003": "N2017"
    }
    global room_to_backer
    room_to_backer = {
        "m88BKR_001": ("N3107", 2),
        "m88BKR_002": ("N3108", 3),
        "m88BKR_003": ( "None", 4),
        "m88BKR_004": ("N3106", 1)
    }
    global map_connections
    map_connections = {}
    global door_string_to_door
    door_string_to_door = {}
    global custom_actor_prefix
    custom_actor_prefix = "TR_"
    global global_room_pickups
    global_room_pickups = []

def get_map_info():
    #Keep track of every door connection for multi purpose
    for room in datatable["PB_DT_RoomMaster"]:
        map_connections[room] = {}
        doors = convert_flag_to_door(room, datatable["PB_DT_RoomMaster"][room]["DoorFlag"], datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"])
        for door in doors:
            door_string = "_".join([door.room[3:], str(door.x_block), str(door.z_block), door.direction_part.name])
            door_string_to_door[door_string] = door
            map_connections[room][door_string] = []
    for room_1 in datatable["PB_DT_RoomMaster"]:
        for room_2 in datatable["PB_DT_RoomMaster"]:
            is_room_adjacent(room_1, room_2)

def update_any_map():
    #Rooms with no traverse blocks only display properly based on their Y position below the origin
    #Shift those lists if the rooms are below 0
    for room in ["m08TWR_017", "m08TWR_018", "m08TWR_019", "m11UGD_013", "m11UGD_031"]:
        if datatable["PB_DT_RoomMaster"][room]["OffsetZ"] < 0:
            multiplier = abs(int(datatable["PB_DT_RoomMaster"][room]["OffsetZ"]/7.2)) - 1
            if multiplier > datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"] - 1:
                multiplier = datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"] - 1
            for index in range(len(datatable["PB_DT_RoomMaster"][room]["NoTraverse"])):
                datatable["PB_DT_RoomMaster"][room]["NoTraverse"][index] -= datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*multiplier

def update_custom_map():
    #Remove the village locked door
    remove_level_class("m02VIL_003_Gimmick", "BP_LookDoor_C")
    #Trigger a few events by default
    datatable["PB_DT_GimmickFlagMaster"]["SIP_017_BreakWallCannon"]["Id"]  = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["ENT_000_FallStatue"]["Id"]       = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["ENT_007_ZangetuJump"]["Id"]      = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["KNG_015_DestructibleRoof"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["LIB_029_DestructibleCeil"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["TRN_002_LeverDoor"]["Id"]        = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    #Remove the few forced transitions that aren't necessary at all
    for room in ["m04GDN_006", "m06KNG_013", "m07LIB_036", "m15JPN_011", "m88BKR_001", "m88BKR_002", "m88BKR_003", "m88BKR_004"]:
        remove_level_class(room + "_RV", "RoomChange_C")
    #Add a second lever to the right of the tower elevator so that it can be activated from either sides
    add_level_actor("m08TWR_009_Gimmick", "TWR009_ElevatorLever_BP_C", FVector(1110, 0, 11040), FRotator(0, 0, 0), FVector(1, 1, 1), {})
    #Make Bathin's room enterable from the left without softlocking the boss
    fix_bathin_left_entrance()
    #Each area has limitations as to where it can be displayed on the canvas
    #Change area IDs based on their X positions so that everything is always displayed
    for room in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][room]["OffsetX"] < 214.2:
            datatable["PB_DT_RoomMaster"][room]["AreaID"] = "EAreaID::m01SIP"
        elif datatable["PB_DT_RoomMaster"][room]["OffsetX"] + datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*12.6 > 1108.8:
            datatable["PB_DT_RoomMaster"][room]["AreaID"] = "EAreaID::m13ARC"
        else:
            datatable["PB_DT_RoomMaster"][room]["AreaID"] = "EAreaID::m03ENT"

def update_map_doors():
    #Place doors next to their corresponding transitions if the adjacent room is of a special type
    #Do this even for the default map as some rooms are missing boss doors
    #Boss doors
    #Remove originals
    for room in boss_door_rooms:
        remove_level_class(get_gimmick_filename(room), "PBBossDoor_BP_C")
    remove_level_class("m20JRN_004_Setting", "PBBossDoor_BP_C")
    #Add new
    for room in room_to_boss:
        for entrance in map_connections[room]:
            for exit in map_connections[room][entrance]:
                if cannot_add_actor_to_door(exit):
                    continue
                #One of the Journey rooms has a faulty persistent level export in its gimmick file, so add in its bg file instead
                if door_string_to_door[exit].room == "m20JRN_002":
                    filename = "m20JRN_002_BG"
                else:
                    filename = get_gimmick_filename(door_string_to_door[exit].room)
                #Offset the door for Journey
                if door_string_to_door[exit].room == "m20JRN_004":
                    x_offset = 180
                elif "m20JRN" in door_string_to_door[exit].room:
                    x_offset = -60
                else:
                    x_offset = 0
                location = FVector(x_offset, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"] = FName.FromString(game_data[filename], room_to_boss[room])
                if door_string_to_door[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    properties["IsRight"] = False
                    if exit in arched_doors:
                        rotation.Yaw += 15
                if door_string_to_door[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["AreaWidthSize"]*1260 - x_offset
                    properties["IsRight"] = True
                    if exit in arched_doors:
                        rotation.Yaw -= 15
                location.Z = door_string_to_door[exit].z_block*720 + 240.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                add_level_actor(filename, "PBBossDoor_BP_C", location, rotation, scale, properties)
                #If the door is a breakable wall we don't want the boss door to overlay it, so break it by default
                if exit in wall_to_gimmick_flag:
                    datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[exit]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if exit == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Backer doors
    #Remove originals
    for room in backer_door_rooms:
        remove_level_class(get_gimmick_filename(room), "PBBakkerDoor_BP_C")
    #Add new
    for room in room_to_backer:
        for entrance in map_connections[room]:
            for exit in map_connections[room][entrance]:
                if cannot_add_actor_to_door(exit):
                    continue
                filename = get_gimmick_filename(door_string_to_door[exit].room)
                location = FVector(0, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"]     = FName.FromString(game_data[filename], room_to_backer[room][0])
                properties["KeyItemID"]  = FName.FromString(game_data[filename], "Keyofbacker" + str(room_to_backer[room][1]))
                properties["TutorialID"] = FName.FromString(game_data[filename], "KeyDoor" + "{:02x}".format(room_to_backer[room][1]))
                if room_to_backer[room][0] == "None":
                    properties["IsMusicBoxRoom"] =  True
                if door_string_to_door[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    if exit in arched_doors:
                        rotation.Yaw += 15
                if door_string_to_door[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["AreaWidthSize"]*1260
                    if exit in arched_doors:
                        rotation.Yaw -= 15
                location.Z = door_string_to_door[exit].z_block*720 + 240.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                actor_index = len(game_data[filename].Exports)
                add_level_actor(filename, "PBBakkerDoor_BP_C", location, rotation, scale, properties)
                #If the door is a breakable wall we don't want the backer door to overlay it, so break it by default
                if exit in wall_to_gimmick_flag:
                    datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[exit]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if exit == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Area doors
    #Remove originals
    for room in area_door_rooms:
        remove_level_class(get_gimmick_filename(room), "BP_AreaDoor_C")
    #Add new
    doors_done = []
    for room in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][room]["RoomType"] != "ERoomType::Load" or room == "m03ENT_1200":
            continue
        for entrance in map_connections[room]:
            for exit in map_connections[room][entrance]:
                if cannot_add_actor_to_door(exit):
                    continue
                if exit in doors_done or exit in arched_doors or exit in transitionless_doors:
                    continue
                #If the door is too close to a cutscene disable the event to prevent softlocks
                if door_string_to_door[exit].room == "m03ENT_006":
                    datatable["PB_DT_EventFlagMaster"]["Event_05_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if exit == "ARC_001_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_09_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if exit == "TAR_000_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_12_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                filename = get_gimmick_filename(door_string_to_door[exit].room)
                x_offset = 40
                location = FVector(x_offset, -180, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                if door_string_to_door[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    class_name = "BP_AreaDoor_C(Left)"
                if door_string_to_door[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["AreaWidthSize"]*1260 - x_offset
                    class_name = "BP_AreaDoor_C(Right)"
                location.Z = door_string_to_door[exit].z_block*720 + 240.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                #If the door should remain open replace it with a regular event door
                if exit in open_transition_doors:
                    scale.Y = 1/3
                    if "Left" in class_name:
                        rotation.Yaw -= 90
                    if "Right" in class_name:
                        rotation.Yaw += 90
                    lever_index = len(game_data[filename].Exports) + 1
                    add_level_actor(filename, "BP_SwitchDoor_C", location, rotation, scale, {"GimmickFlag": FName.FromString(game_data[filename], "None")})
                    game_data[filename].Exports[lever_index].Data[2].Value[0].Value = FVector(0, -600, 0)
                else:
                    add_level_actor(filename, class_name, location, rotation, scale, {"IsInvertingOpen": False})
                    #If the door is a breakable wall we don't want the area door to overlay it, so break it by default
                    if exit in wall_to_gimmick_flag:
                        datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[exit]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                    #If the entrance has very little floor shift the door closer to the transition to prevent softlocks
                    if exit in floorless_doors:
                        platform_location = FVector(0, -250, location.Z - 20)
                        platform_rotation = FRotator(0, 0, 0)
                        platform_scale    = FVector(12/11, 1, 1)
                        if "Left" in class_name:
                            platform_location.X = location.X + 35
                        if "Right" in class_name:
                            platform_location.X = location.X - 35 - 120*12/11
                        add_level_actor(filename, "UGD_WeakPlatform_C", platform_location, platform_rotation, platform_scale, {"SecondsToDestroy": 9999.0})
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if exit == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
                #Since transition rooms are double make sure that a door only gets added once
                doors_done.append(exit)

def update_map_indicators():
    #Place a bookshelf in front of every save and warp point to make map traversal easier
    #Only do it for custom maps as the default map already has bookshelves with text
    #Remove originals
    for room in bookshelf_rooms:
        remove_level_class(get_gimmick_filename(room), "ReadableBookShelf_C")
    #Add new
    doors_done = []
    for room in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][room]["RoomType"] != "ERoomType::Save" and datatable["PB_DT_RoomMaster"][room]["RoomType"] != "ERoomType::Warp":
            continue
        for entrance in map_connections[room]:
            for exit in map_connections[room][entrance]:
                if cannot_add_actor_to_door(exit):
                    continue
                if exit in ["VIL_005_0_0_RIGHT", "VIL_006_0_1_LEFT"]:
                    continue
                filename = get_gimmick_filename(door_string_to_door[exit].room)
                location = FVector(-80, -120, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                properties = {}
                properties["DiaryID"] = FName.FromString(game_data[filename], "None")
                if door_string_to_door[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -30
                if door_string_to_door[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["AreaWidthSize"]*1260 - 50
                    rotation.Yaw = 30
                location.Z = door_string_to_door[exit].z_block*720 + 240.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if door_string_to_door[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                add_level_actor(filename, "ReadableBookShelf_C", location, rotation, scale, properties)
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if exit == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Fill empty entrances with an impassable door to prevent softlocks
    #Add new
    door_height = 240
    door_width = 44
    for room in map_connections:
        for door in map_connections[room]:
            if map_connections[room][door]:
                continue
            if cannot_add_actor_to_door(door):
                continue
            filename = get_gimmick_filename(room)
            location = FVector(0, -360, 0)
            rotation = FRotator(0, 0, 0)
            scale    = FVector(1, 1, 1)
            #Global direction
            if door_string_to_door[door].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                location.X = -18
                location.Z = door_string_to_door[door].z_block*720 + door_height
                lever_offset = -360
                if door in arched_doors:
                    rotation.Yaw += 20
            if door_string_to_door[door].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                location.X = datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260 + 18
                location.Z = door_string_to_door[door].z_block*720 + door_height
                lever_offset = 360
                if door in arched_doors:
                    rotation.Yaw -= 20
            if door_string_to_door[door].direction_part in [Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT]:
                location.X = door_string_to_door[door].x_block*1260 + 510.0
                location.Z = datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"]*720 - 5
                rotation.Pitch = -90
                lever_offset = -360
            if door_string_to_door[door].direction_part in [Direction.BOTTOM, Direction.BOTTOM_LEFT, Direction.BOTTOM_RIGHT]:
                location.X = door_string_to_door[door].x_block*1260 + 510.0
                location.Z = 5
                rotation.Pitch = -90
                lever_offset = 360
            #Sub direction
            if door_string_to_door[door].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                if "m10BIG" in room:
                    location.Z -= door_height
                elif "_".join([room[3:], str(door_string_to_door[door].x_block), str(door_string_to_door[door].z_block), door_string_to_door[door].direction_part.name.split("_")[0]]) in map_connections[room]:
                    location.Z -= door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    location.Z -= door_height*scale.Z - door_height
                else:
                    location.Z -= 180
            if door_string_to_door[door].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                if "m10BIG" in room:
                    location.Z += door_height
                elif "_".join([room[3:], str(door_string_to_door[door].x_block), str(door_string_to_door[door].z_block), door_string_to_door[door].direction_part.name.split("_")[0]]) in map_connections[room]:
                    location.Z += door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    if door_string_to_door[door].direction_part == Direction.LEFT_TOP:
                        location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    else:
                        location.X += (door_width*scale.Z - door_width)/2 - door_width
                else:
                    location.Z += 180
            if door_string_to_door[door].direction_part in [Direction.TOP_LEFT, Direction.BOTTOM_LEFT]:
                if "m10BIG" in room:
                    location.X -= 510
                else:
                    location.X -= 370
            if door_string_to_door[door].direction_part in [Direction.TOP_RIGHT, Direction.BOTTOM_RIGHT]:
                if "m10BIG" in room:
                    location.X += 510
                else:
                    location.X += 370
            lever_index = len(game_data[filename].Exports) + 1
            add_level_actor(filename, "BP_SwitchDoor_C", location, rotation, scale, {"GimmickFlag": FName.FromString(game_data[filename], "None")})
            game_data[filename].Exports[lever_index].Data[2].Value[0].Value = FVector(lever_offset, 360, 0)
            #Remove the magic door in that one galleon room so that it never overlays with anything
            if door == "SIP_002_0_0_RIGHT":
                remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")

def cannot_add_actor_to_door(door):
    room = door_string_to_door[door].room
    return door in door_skip or room in room_to_boss or room in room_to_backer or not room in constant["RoomRequirement"]

def update_room_containers(room):
    filename = get_gimmick_filename(room)
    if not filename in game_data:
        return
    room_width = datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260
    for export_index in range(len(game_data[filename].Exports)):
        old_class_name = str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[export_index].ClassIndex))) - 1].ObjectName)
        #Check if it is a golden chest
        if old_class_name == "PBEasyTreasureBox_BP_C" and str(game_data[filename].Exports[export_index].Data[4].Name) == "IsAutoMaterial":
            old_class_name = "PBEasyTreasureBox_BP_C(Gold)"
        #Pure miriam is considered a different class but honestly it's the same as regular chests
        if old_class_name == "PBPureMiriamTreasureBox_BP_C":
            old_class_name = "PBEasyTreasureBox_BP_C"
        if old_class_name in ["PBEasyTreasureBox_BP_C", "PBEasyTreasureBox_BP_C(Gold)", "HPMaxUp_C", "MPMaxUp_C", "BulletMaxUp_C"]:
            #Gather old actor properties
            location = FVector(0, 0, 0)
            rotation = FRotator(0, 0, 0)
            scale    = FVector(1, 1, 1)
            safety_chest = False
            gimmick_id = ""
            for data in game_data[filename].Exports[export_index].Data:
                if str(data.Name) in ["DropItemID", "DropRateID"]:
                    drop_id = str(data.Value)
                if str(data.Name) == "IsRandomizerSafetyChest":
                    safety_chest = data.Value
                if str(data.Name) == "OptionalGimmickID":
                    gimmick_id = str(data.Value)
                if str(data.Name) == "RootComponent":
                    root_index = int(str(data.Value)) - 1
                    for root_data in game_data[filename].Exports[root_index].Data:
                        if str(root_data.Name) == "RelativeLocation":
                            location = root_data.Value[0].Value
                        if str(root_data.Name) == "RelativeRotation":
                            rotation = root_data.Value[0].Value
                        if str(root_data.Name) == "RelativeScale3D":
                            scale    = root_data.Value[0].Value
            if not drop_id in datatable["PB_DT_DropRateMaster"]:
                continue
            if drop_id in global_room_pickups:
                continue
            if safety_chest:
                continue
            if datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxHPUP":
                new_class_name = "HPMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxMPUP":
                new_class_name = "MPMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxBulletUP":
                new_class_name = "BulletMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] in Item.key_items + ["Certificationboard"]:
                new_class_name = "PBEasyTreasureBox_BP_C(Gold)"
            else:
                new_class_name = "PBEasyTreasureBox_BP_C"
            #Check if container mismatches item type
            if old_class_name == new_class_name:
                continue
            #Some upgrades in rotating rooms are on the wrong plane
            if room == "m02VIL_008":
                location.X -= 50
            if drop_id == "Treasurebox_TWR017_6":
                location.X -= 100
            #Correct container transform when necessary
            if "TreasureBox" in new_class_name and "MaxUp" in old_class_name or "MaxUp" in new_class_name and "TreasureBox" in old_class_name:
                #If the room is a rotating 3d one then use the forward vector to shift position
                if room in rotating_room_to_center and drop_id != "Treasurebox_TWR019_2":
                    rotation.Yaw = -math.degrees(math.atan2(location.X - rotating_room_to_center[room][0], location.Y - rotating_room_to_center[room][1]))
                    forward_vector = (math.sin(math.radians(rotation.Yaw))*(-1), math.cos(math.radians(rotation.Yaw)))
                    if "TreasureBox" in new_class_name:
                        location.X -= forward_vector[0]*120
                        location.Y -= forward_vector[1]*120
                    if "MaxUp" in new_class_name:
                        if drop_id in ["Treasurebox_TWR017_5", "Treasurebox_SND025_1"]:
                            location.X += forward_vector[0]*60
                            location.Y += forward_vector[1]*60
                        else:
                            location.X += forward_vector[0]*120
                            location.Y += forward_vector[1]*120
                else:
                    if "TreasureBox" in new_class_name:
                        location.Y = -120
                        #Slightly rotate the chest to be facing the center of the room
                        if location.X < room_width*0.45:
                            rotation.Yaw = -30
                        elif location.X > room_width*0.55:
                            rotation.Yaw = 30
                        else:
                            rotation.Yaw = 0
                        #Drop chest down to the floor if it is in a bell
                        if drop_id == "Treasurebox_SAN003_4":
                            location.Z = 4080
                        if drop_id == "Treasurebox_SAN003_5":
                            location.Z = 6600
                        if drop_id == "Treasurebox_SAN019_3":
                            location.Z = 120
                        if drop_id == "Treasurebox_SAN021_4":
                            location.Z = 420
                    if "MaxUp" in new_class_name:
                        location.Y = 0
                        rotation.Yaw = 0
                        #If it used to be the chest under the bridge move it to Benjamin's room for the extra characters
                        if drop_id == "Treasurebox_JPN002_1":
                            location.X = 1860
                            location.Z = 60
            #Remove the old container
            remove_level_actor(filename, export_index)
            #One of the Journey rooms has a faulty persistent level export in its gimmick file, so add in its bg file instead
            if room == "m20JRN_002":
                filename = "m20JRN_002_BG"
            #Setup the actor properties
            properties = {}
            if "PBEasyTreasureBox_BP_C" in new_class_name:
                properties["DropItemID"]   = FName.FromString(game_data[filename], drop_id)
                properties["ItemID"]       = FName.FromString(game_data[filename], drop_id)
                properties["TreasureFlag"] = FName.FromString(game_data[filename], "EGameTreasureFlag::" + Utility.remove_inst_number(drop_id))
                if gimmick_id:
                    properties["OptionalGimmickID"] = FName.FromString(game_data[filename], gimmick_id)
            else:
                properties["DropRateID"]   = FName.FromString(game_data[filename], drop_id)
            add_level_actor(filename, new_class_name, location, rotation, scale, properties)

def update_map_connections():
    #The game map requires you to manually input a list of which rooms can be transitioned into from the current room
    #Doing this via the map editor would only add long load times upon saving a map so do it here instead
    #Fill same room field for rooms that are overlayed perfectly
    #Not sure if it serves any actual purpose in-game but it does help for the following adjacent room check
    for room_1 in datatable["PB_DT_RoomMaster"]:
        datatable["PB_DT_RoomMaster"][room_1]["SameRoom"] = "None"
        if datatable["PB_DT_RoomMaster"][room_1]["OutOfMap"]:
            continue
        for room_2 in datatable["PB_DT_RoomMaster"]:
            if datatable["PB_DT_RoomMaster"][room_2]["OutOfMap"]:
                continue
            if datatable["PB_DT_RoomMaster"][room_1]["OffsetX"] == datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] and datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"] == datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] and room_1 != room_2:
                datatable["PB_DT_RoomMaster"][room_1]["SameRoom"] = room_2
                break
    is_vanilla_start = datatable["PB_DT_RoomMaster"]["m03ENT_1200"]["SameRoom"] == "m02VIL_1200"
    #Fill adjacent room lists
    for room in datatable["PB_DT_RoomMaster"]:
        datatable["PB_DT_RoomMaster"][room]["AdjacentRoomName"].clear()
        open_doors = []
        for entrance in map_connections[room]:
            for exit in map_connections[room][entrance]:
                #Transition rooms in Bloodstained come by pair, each belonging to an area
                #Make it so that an area is only connected to its corresponding transition rooms when possible
                #This avoids having the next area name tag show up within the transition
                #With the exception of standalone transitions with no fallbacks as well as the first entrance transition fallback
                if datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["RoomType"] == "ERoomType::Load" and door_string_to_door[exit].room[0:6] != room[0:6] and datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["SameRoom"] != "None":
                    if is_vanilla_start or door_string_to_door[exit].room != "m02VIL_1200" and datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["SameRoom"] != "m03ENT_1200":
                        continue
                #The first entrance transition room is hardcoded to bring you back to the village regardless of its position on the canvas
                #Ignore that room and don't connect it to anything
                #Meanwhile the village version of that transition is always needed to trigger the curved effect of the following bridge room
                #So ignore any other transitions overlayed on top of it
                if not is_vanilla_start and (datatable["PB_DT_RoomMaster"][door_string_to_door[exit].room]["SameRoom"] == "m02VIL_1200" or door_string_to_door[exit].room == "m03ENT_1200"):
                    continue
                if not door_string_to_door[exit].room in datatable["PB_DT_RoomMaster"][room]["AdjacentRoomName"]:
                    datatable["PB_DT_RoomMaster"][room]["AdjacentRoomName"].append(door_string_to_door[exit].room)
            #Update door list
            if map_connections[room][entrance]:
                open_doors.append(door_string_to_door[entrance])
        datatable["PB_DT_RoomMaster"][room]["DoorFlag"] = convert_door_to_flag(open_doors, datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"])
    #Some rooms need specific setups
    #Vepar room
    datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"].append("m02VIL_000")
    #Tower rooms
    datatable["PB_DT_RoomMaster"]["m08TWR_000"]["AdjacentRoomName"].append("m08TWR_017")
    datatable["PB_DT_RoomMaster"]["m08TWR_005"]["AdjacentRoomName"].append("m08TWR_018")
    datatable["PB_DT_RoomMaster"]["m08TWR_006"]["AdjacentRoomName"].append("m08TWR_018")
    datatable["PB_DT_RoomMaster"]["m08TWR_016"]["AdjacentRoomName"].append("m08TWR_019")
    
    datatable["PB_DT_RoomMaster"]["m08TWR_017"]["AdjacentRoomName"].append("m08TWR_000")
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"].append("m08TWR_005")
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"].append("m08TWR_006")
    datatable["PB_DT_RoomMaster"]["m08TWR_019"]["AdjacentRoomName"].append("m08TWR_016")
    
    datatable["PB_DT_RoomMaster"]["m08TWR_000"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_000"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_005"]["DoorFlag"].append(4)
    datatable["PB_DT_RoomMaster"]["m08TWR_005"]["DoorFlag"].append(4)
    datatable["PB_DT_RoomMaster"]["m08TWR_006"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_006"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_016"]["DoorFlag"].insert(0, 4)
    datatable["PB_DT_RoomMaster"]["m08TWR_016"]["DoorFlag"].insert(0, 2)
    
    datatable["PB_DT_RoomMaster"]["m08TWR_017"]["DoorFlag"].append(18)
    datatable["PB_DT_RoomMaster"]["m08TWR_017"]["DoorFlag"].append(8)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(3)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(2)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(34)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(8)
    datatable["PB_DT_RoomMaster"]["m08TWR_019"]["DoorFlag"].append(39)
    datatable["PB_DT_RoomMaster"]["m08TWR_019"]["DoorFlag"].append(8)
    #Train rooms
    datatable["PB_DT_RoomMaster"]["m09TRN_001"]["AdjacentRoomName"].append("m09TRN_002")
    datatable["PB_DT_RoomMaster"]["m09TRN_002"]["AdjacentRoomName"].append("m09TRN_001")
    datatable["PB_DT_RoomMaster"]["m09TRN_002"]["AdjacentRoomName"].append("m09TRN_003")
    datatable["PB_DT_RoomMaster"]["m09TRN_003"]["AdjacentRoomName"].append("m09TRN_002")
    #Garden Den
    datatable["PB_DT_RoomMaster"]["m04GDN_001"]["AdjacentRoomName"].append("m10BIG_000")
    datatable["PB_DT_RoomMaster"]["m10BIG_000"]["AdjacentRoomName"].append("m04GDN_001")
    #Extra mode rooms
    datatable["PB_DT_RoomMaster"]["m53BRV_000"]["AdjacentRoomName"].append("m53BRV_001")
    datatable["PB_DT_RoomMaster"]["m53BRV_001"]["AdjacentRoomName"].append("m53BRV_002")
    datatable["PB_DT_RoomMaster"]["m53BRV_001"]["AdjacentRoomName"].append("m53BRV_022")
    datatable["PB_DT_RoomMaster"]["m53BRV_002"]["AdjacentRoomName"].append("m53BRV_003")
    datatable["PB_DT_RoomMaster"]["m53BRV_022"]["AdjacentRoomName"].append("m53BRV_003")
    datatable["PB_DT_RoomMaster"]["m53BRV_003"]["AdjacentRoomName"].append("m53BRV_004")
    datatable["PB_DT_RoomMaster"]["m53BRV_003"]["AdjacentRoomName"].append("m53BRV_024")
    datatable["PB_DT_RoomMaster"]["m53BRV_004"]["AdjacentRoomName"].append("m53BRV_005")
    datatable["PB_DT_RoomMaster"]["m53BRV_024"]["AdjacentRoomName"].append("m53BRV_005")
    datatable["PB_DT_RoomMaster"]["m53BRV_005"]["AdjacentRoomName"].append("m53BRV_026")
    datatable["PB_DT_RoomMaster"]["m53BRV_026"]["AdjacentRoomName"].append("m53BRV_101")
    datatable["PB_DT_RoomMaster"]["m53BRV_026"]["AdjacentRoomName"].append("m53BRV_121")
    
    datatable["PB_DT_RoomMaster"]["m50BRM_000"]["AdjacentRoomName"].append("m50BRM_001")
    datatable["PB_DT_RoomMaster"]["m50BRM_020"]["AdjacentRoomName"].append("m50BRM_001")
    datatable["PB_DT_RoomMaster"]["m50BRM_001"]["AdjacentRoomName"].append("m50BRM_002")
    datatable["PB_DT_RoomMaster"]["m50BRM_001"]["AdjacentRoomName"].append("m50BRM_022")
    datatable["PB_DT_RoomMaster"]["m50BRM_002"]["AdjacentRoomName"].append("m50BRM_003")
    datatable["PB_DT_RoomMaster"]["m50BRM_022"]["AdjacentRoomName"].append("m50BRM_003")
    datatable["PB_DT_RoomMaster"]["m50BRM_003"]["AdjacentRoomName"].append("m50BRM_004")
    datatable["PB_DT_RoomMaster"]["m50BRM_003"]["AdjacentRoomName"].append("m50BRM_024")
    datatable["PB_DT_RoomMaster"]["m50BRM_004"]["AdjacentRoomName"].append("m50BRM_005")
    datatable["PB_DT_RoomMaster"]["m50BRM_024"]["AdjacentRoomName"].append("m50BRM_005")
    datatable["PB_DT_RoomMaster"]["m50BRM_005"]["AdjacentRoomName"].append("m50BRM_006")
    datatable["PB_DT_RoomMaster"]["m50BRM_005"]["AdjacentRoomName"].append("m50BRM_026")
    datatable["PB_DT_RoomMaster"]["m50BRM_006"]["AdjacentRoomName"].append("m50BRM_007")
    datatable["PB_DT_RoomMaster"]["m50BRM_026"]["AdjacentRoomName"].append("m50BRM_007")
    datatable["PB_DT_RoomMaster"]["m50BRM_007"]["AdjacentRoomName"].append("m50BRM_008")
    datatable["PB_DT_RoomMaster"]["m50BRM_007"]["AdjacentRoomName"].append("m50BRM_028")
    datatable["PB_DT_RoomMaster"]["m50BRM_008"]["AdjacentRoomName"].append("m50BRM_009")
    datatable["PB_DT_RoomMaster"]["m50BRM_028"]["AdjacentRoomName"].append("m50BRM_009")
    datatable["PB_DT_RoomMaster"]["m50BRM_009"]["AdjacentRoomName"].append("m50BRM_101")
    datatable["PB_DT_RoomMaster"]["m50BRM_009"]["AdjacentRoomName"].append("m50BRM_121")
    
    datatable["PB_DT_RoomMaster"]["m50BRM_050"]["AdjacentRoomName"].append("m50BRM_051")
    datatable["PB_DT_RoomMaster"]["m50BRM_070"]["AdjacentRoomName"].append("m50BRM_051")
    datatable["PB_DT_RoomMaster"]["m50BRM_051"]["AdjacentRoomName"].append("m50BRM_052")
    datatable["PB_DT_RoomMaster"]["m50BRM_051"]["AdjacentRoomName"].append("m50BRM_072")
    datatable["PB_DT_RoomMaster"]["m50BRM_052"]["AdjacentRoomName"].append("m50BRM_053")
    datatable["PB_DT_RoomMaster"]["m50BRM_072"]["AdjacentRoomName"].append("m50BRM_053")
    datatable["PB_DT_RoomMaster"]["m50BRM_053"]["AdjacentRoomName"].append("m50BRM_054")
    datatable["PB_DT_RoomMaster"]["m50BRM_053"]["AdjacentRoomName"].append("m50BRM_074")
    datatable["PB_DT_RoomMaster"]["m50BRM_054"]["AdjacentRoomName"].append("m50BRM_055")
    datatable["PB_DT_RoomMaster"]["m50BRM_074"]["AdjacentRoomName"].append("m50BRM_055")
    datatable["PB_DT_RoomMaster"]["m50BRM_055"]["AdjacentRoomName"].append("m50BRM_056")
    datatable["PB_DT_RoomMaster"]["m50BRM_055"]["AdjacentRoomName"].append("m50BRM_076")
    datatable["PB_DT_RoomMaster"]["m50BRM_056"]["AdjacentRoomName"].append("m50BRM_057")
    datatable["PB_DT_RoomMaster"]["m50BRM_076"]["AdjacentRoomName"].append("m50BRM_057")
    datatable["PB_DT_RoomMaster"]["m50BRM_057"]["AdjacentRoomName"].append("m50BRM_058")
    datatable["PB_DT_RoomMaster"]["m50BRM_057"]["AdjacentRoomName"].append("m50BRM_078")
    datatable["PB_DT_RoomMaster"]["m50BRM_058"]["AdjacentRoomName"].append("m50BRM_059")
    datatable["PB_DT_RoomMaster"]["m50BRM_078"]["AdjacentRoomName"].append("m50BRM_059")
    datatable["PB_DT_RoomMaster"]["m50BRM_059"]["AdjacentRoomName"].append("m50BRM_151")
    datatable["PB_DT_RoomMaster"]["m50BRM_059"]["AdjacentRoomName"].append("m50BRM_171")
    #Give overlayed rooms the same door flag as their counterparts
    datatable["PB_DT_RoomMaster"]["m01SIP_022"]["DoorFlag"] = datatable["PB_DT_RoomMaster"]["m02VIL_000"]["DoorFlag"]
    datatable["PB_DT_RoomMaster"]["m18ICE_020"]["DoorFlag"] = datatable["PB_DT_RoomMaster"]["m18ICE_019"]["DoorFlag"]
    #Update out of map based on accessible rooms
    for room in datatable["PB_DT_RoomMaster"]:
        datatable["PB_DT_RoomMaster"][room]["OutOfMap"] = True
    current_rooms = ["m01SIP_000"]
    while current_rooms:
        for room in current_rooms:
            datatable["PB_DT_RoomMaster"][room]["OutOfMap"] = False
        current_rooms_copy = copy.deepcopy(current_rooms)
        for room_1 in current_rooms_copy:
            for room_2 in datatable["PB_DT_RoomMaster"][room_1]["AdjacentRoomName"]:
                if datatable["PB_DT_RoomMaster"][room_2]["OutOfMap"]:
                    current_rooms.append(room_2)
            current_rooms.remove(room_1)
        current_rooms = list(dict.fromkeys(current_rooms))
    #Fix bad ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"].append("m02VIL_099")
    #Fix good ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"].append("m02VIL_099")

def fix_bathin_left_entrance():
    #If Bathin's intro event triggers when the player entered the room from the left they will be stuck in an endless walk cycle
    #To fix this add a special door to warp the player in the room's player start instead
    for door in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = door_string_to_door[door].room
        area_path = "ACT" + room[1:3] + "_" + room[3:6]
        new_file = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version.VER_UE4_22)
        index = new_file.SearchNameReference(FString("m02VIL_012_RV"))
        new_file.SetNameReference(index, FString(room + "_RV"))
        index = new_file.SearchNameReference(FString("/Game/Core/Environment/ACT02_VIL/Level/m02VIL_012_RV"))
        new_file.SetNameReference(index, FString("/Game/Core/Environment/" + area_path + "/Level/" + room + "_RV"))
        new_file.Exports[9].Data[1].Value = FName.FromString(new_file, room)
        #Correct the room dimension settings
        new_file.Exports[0].Data[2].Value[0].Value  = FVector( 630*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"],   0, 360*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        new_file.Exports[0].Data[3].Value[0].Value  = FVector(1260*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"], 720, 720*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        new_file.Exports[12].Data[0].Value[0].Value = FVector(  21*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"],  12,  12*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        #Change the door's properties
        new_file.Exports[2].Data[0].Value[0].Value  = FVector(1260*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"], 0, 720*door_string_to_door[door].z_block + 360)
        new_file.Exports[2].Data[1].Value[0].Value  = FRotator(0, 0, 0)
        new_file.Exports[8].Data[0].Value = FName.FromString(new_file, room[3:])
        new_file.Exports[8].Data[1].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[2].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[3].Value = FName.FromString(new_file, "m13ARC_005")
        new_file.Write(Manager.mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")
    adjacent_room = None
    #Get Bathin's adjacent room while prioritizing the same area
    for door in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = door_string_to_door[door].room
        adjacent_room = room
        if datatable["PB_DT_RoomMaster"][room]["AreaID"] == datatable["PB_DT_RoomMaster"]["m13ARC_005"]["AreaID"]:
            break
    #Add one more door in the boss room to have a proper transition
    if adjacent_room:
        room = "m13ARC_005"
        area_path = "ACT" + room[1:3] + "_" + room[3:6]
        new_file = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version.VER_UE4_22)
        index = new_file.SearchNameReference(FString("m02VIL_012_RV"))
        new_file.SetNameReference(index, FString(room + "_RV"))
        index = new_file.SearchNameReference(FString("/Game/Core/Environment/ACT02_VIL/Level/m02VIL_012_RV"))
        new_file.SetNameReference(index, FString("/Game/Core/Environment/" + area_path + "/Level/" + room + "_RV"))
        new_file.Exports[9].Data[1].Value = FName.FromString(new_file, room)
        #Correct the room dimension settings
        new_file.Exports[0].Data[2].Value[0].Value  = FVector( 630*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"],   0, 360*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        new_file.Exports[0].Data[3].Value[0].Value  = FVector(1260*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"], 720, 720*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        new_file.Exports[12].Data[0].Value[0].Value = FVector(  21*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"],  12,  12*datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"])
        #Change the door's properties
        new_file.Exports[2].Data[0].Value[0].Value  = FVector(0, 0, 360)
        new_file.Exports[2].Data[1].Value[0].Value  = FRotator(0, 0, 0)
        new_file.Exports[8].Data[0].Value = FName.FromString(new_file, "ARC_005")
        new_file.Exports[8].Data[1].Value = FName.FromString(new_file, adjacent_room[3:])
        new_file.Exports[8].Data[2].Value = FName.FromString(new_file, adjacent_room[3:])
        new_file.Exports[8].Data[3].Value = FName.FromString(new_file, adjacent_room)
        new_file.Write(Manager.mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")

def add_global_room_pickup(room, drop_id):
    #Place an upgrade in a room at its origin
    room_width  = datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260
    room_height = datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"]*720
    filename = get_gimmick_filename(room)
    actor_index = len(game_data[filename].Exports)
    add_level_actor(filename, "HPMaxUp_C", FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1), {"DropRateID": FName.FromString(game_data[filename], drop_id)})
    #Enlarge its hitbox considerably so that entering the room from anywhere will collect it
    struct = StructPropertyData(FName.FromString(game_data[filename], "BoxExtent"), FName.FromString(game_data[filename], "Vector"))
    sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "BoxExtent"))
    sub_struct.Value = FVector((room_width + 120)*4, 50, (room_height + 120)*4)
    struct.Value.Add(sub_struct)
    game_data[filename].Exports[actor_index + 1].Data.Add(struct)
    #Keep it in mind to not update its container type
    global_room_pickups.append(drop_id)

def add_game_room(room):
    area_path = "ACT" + room[1:3] + "_" + room[3:6]
    new_file = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path["m01SIP_1000_RV"] + "\\m01SIP_1000_RV.umap", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString(room + "_RV"))
    index = new_file.SearchNameReference(FString("/Game/Core/Environment/ACT01_SIP/Level/m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString("/Game/Core/Environment/" + area_path + "/Level/" + room + "_RV"))
    new_file.Exports[5].Data[1].Value = FName.FromString(new_file, room)
    new_file.Write(Manager.mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")

def add_level_actor(filename, actor_class, location, rotation, scale, properties):
    actor_index = len(game_data[filename].Exports)
    #Name the new actor based on the class
    short_class = actor_class.replace(")", "").split("(")[0]
    short_class = short_class.split("_")
    if short_class[-1] == "C":
        short_class.pop()
    short_class = "_".join(short_class)
    actor_name = custom_actor_prefix + short_class
    snippet = UAssetSnippet(game_data[constant["ActorPointer"][actor_class]["File"]], constant["ActorPointer"][actor_class]["Index"])
    snippet.AddToUAsset(game_data[filename], actor_name)
    #Change class parameters
    for data in game_data[filename].Exports[actor_index].Data:
        if str(data.Name) in properties:
            if str(data.PropertyType) == "ByteProperty":
                data.EnumValue = properties[str(data.Name)]
            else:
                data.Value = properties[str(data.Name)]
            del properties[str(data.Name)]
        if str(data.Name) == "ActorLabel":
            data.Value = FString(Utility.remove_inst_number(actor_name))
        if str(data.Name) == "RootComponent":
            root_index = int(str(data.Value)) - 1
            game_data[filename].Exports[root_index].Data.Clear()
            if location.X != 0 or location.Y != 0 or location.Z != 0:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeLocation"), FName.FromString(game_data[filename], "Vector"))
                sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "RelativeLocation"))
                sub_struct.Value = FVector(location.X, location.Y, location.Z)
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
            if rotation.Pitch != 0 or rotation.Yaw != 0 or rotation.Roll != 0:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeRotation"), FName.FromString(game_data[filename], "Rotator"))
                sub_struct = RotatorPropertyData(FName.FromString(game_data[filename], "RelativeRotation"))
                sub_struct.Value = FRotator(rotation.Pitch, rotation.Yaw, rotation.Roll)
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
            if scale.X != 1 or scale.Y != 1 or scale.Z != 1:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeScale3D"), FName.FromString(game_data[filename], "Vector"))
                sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "RelativeScale3D"))
                sub_struct.Value = FVector(scale.X, scale.Y, scale.Z)
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
    #Add parameters that are missing
    for data in properties:
        if type(properties[data]) is bool:
            struct = BoolPropertyData(FName.FromString(game_data[filename], data))
            struct.Value = properties[data]
        elif type(properties[data]) is int:
            struct = IntPropertyData(FName.FromString(game_data[filename], data))
            struct.Value = properties[data]
        elif type(properties[data]) is float:
            struct = FloatPropertyData(FName.FromString(game_data[filename], data))
            struct.Value = properties[data]
        elif "::" in str(properties[data]):
            struct = BytePropertyData(FName.FromString(game_data[filename], data))
            struct.ByteType = BytePropertyType.FName
            struct.EnumType = FName.FromString(game_data[filename], str(properties[data]).split("::")[0])
            struct.EnumValue = properties[data]
        else:
            struct = NamePropertyData(FName.FromString(game_data[filename], data))
            struct.Value = properties[data]
        game_data[filename].AddNameReference(struct.PropertyType)
        game_data[filename].Exports[actor_index].Data.Add(struct)
    #Temporary Rocky fix
    if actor_class == "Chr_N3115_C":
        remove_level_actor(filename, actor_index + 59)
        game_data[filename].Exports[actor_index + 59].OuterIndex = FPackageIndex(actor_index + 43)

def add_extra_mode_warp(filename, warp_1_location, warp_1_rotation, warp_2_location, warp_2_rotation):
    warp_1_index = len(game_data[filename].Exports)
    add_level_actor(filename, "ToriiWarp_BP_C", warp_1_location, warp_1_rotation, FVector(1, 1, 1), {})
    warp_2_index = int(str(game_data[filename].Exports[warp_1_index].Data[12].Value)) - 1
    root_index = int(str(game_data[filename].Exports[warp_2_index].Data[14].Value)) - 1
    game_data[filename].Exports[root_index].Data.Clear()
    if warp_2_location.X != 0 or warp_2_location.Y != 0 or warp_2_location.Z != 0:
        struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeLocation"), FName.FromString(game_data[filename], "Vector"))
        sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "RelativeLocation"))
        sub_struct.Value = warp_2_location
        struct.Value.Add(sub_struct)
        game_data[filename].Exports[root_index].Data.Add(struct)
    if warp_2_rotation.Pitch != 0 or warp_2_rotation.Yaw != 0 or warp_2_rotation.Roll != 0:
        struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeRotation"), FName.FromString(game_data[filename], "Rotator"))
        sub_struct = RotatorPropertyData(FName.FromString(game_data[filename], "RelativeRotation"))
        sub_struct.Value = warp_2_rotation
        struct.Value.Add(sub_struct)
        game_data[filename].Exports[root_index].Data.Add(struct)
    warp_1_event_index = int(str(game_data[filename].Exports[warp_1_index].Data[3].Value)) - 1
    warp_2_event_index = int(str(game_data[filename].Exports[warp_2_index].Data[3].Value)) - 1
    game_data[filename].Exports[warp_1_event_index].Data[2].Value = game_data[filename].Exports[warp_1_index].ObjectName
    game_data[filename].Exports[warp_1_event_index].Data[3].Value = game_data[filename].Exports[warp_2_index].ObjectName
    game_data[filename].Exports[warp_2_event_index].Data[2].Value = game_data[filename].Exports[warp_2_index].ObjectName
    game_data[filename].Exports[warp_2_event_index].Data[3].Value = game_data[filename].Exports[warp_1_index].ObjectName

def remove_level_actor(filename, export_index):
    #Remove actor at index
    if Manager.file_to_type[filename] != Manager.FileType.Level:
        raise TypeError("Input is not a level file")
    class_name = str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[export_index].ClassIndex))) - 1].ObjectName)
    #If the actor makes use of a c_cat class removing it will crash the game
    if class_name in c_cat_actors or filename in ["m20JRN_002_Gimmick", "m20JRN_002_Enemy"]:
        for data in game_data[filename].Exports[export_index].Data:
            if str(data.Name) in ["DropItemID", "ItemID"] and "TreasureBox" in class_name:
                data.Value = FName.FromString(game_data[filename], "AAAA_Shard")
            if str(data.Name) == "RootComponent":
                root_index = int(str(data.Value)) - 1
        for data in game_data[filename].Exports[root_index].Data:
            #Scale giant dulla spawner to 0 to remove it
            if class_name == "N3126_Generator_C":
                if str(data.Name) == "RelativeScale3D":
                    data.Value[0].Value = FVector(0, 0, 0)
            #Otherwise move the actor off screen
            else:
                if str(data.Name) == "RelativeLocation":
                    data.Value[0].Value = FVector(-999, 0, 0)
    else:
        level_index = Utility.export_name_to_index(filename, "PersistentLevel")
        game_data[filename].Exports[export_index].OuterIndex = FPackageIndex(0)
        game_data[filename].Exports[level_index].IndexData.Remove(export_index + 1)
        game_data[filename].Exports[level_index].CreateBeforeSerializationDependencies.Remove(FPackageIndex(export_index + 1))

def remove_level_class(filename, class_name):
    #Remove all actors of class in a level
    for export_index in range(len(game_data[filename].Exports)):
        if str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[export_index].ClassIndex))) - 1].ObjectName) == class_name:
            remove_level_actor(filename, export_index)

def convert_flag_to_door(room_name, door_flag, room_width):
    #Function by LagoLunatic
    door_list = []
    for index in range(0, len(door_flag), 2):
        tile_index = door_flag[index]
        direction = door_flag[index+1]
        tile_index -= 1
        if room_width == 0:
            x_block = tile_index
            z_block = 0
        else:
            x_block = tile_index % room_width
            z_block = tile_index // room_width
        for direction_part in Direction:
            if (direction & direction_part.value) != 0:
                breakable = (direction & (direction_part.value << 16)) != 0
                door = Door(room_name, x_block, z_block, direction_part, breakable)
                door_list.append(door)
    return door_list

def convert_door_to_flag(door_list, room_width):
    #Function by LagoLunatic
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
        tile_index_in_room = z*room_width + x
        tile_index_in_room += 1
        door_flag.extend([tile_index_in_room, dir_flags])
    return door_flag

def is_room_adjacent(room_1, room_2):
    if datatable["PB_DT_RoomMaster"][room_1]["OutOfMap"] != datatable["PB_DT_RoomMaster"][room_2]["OutOfMap"]:
        return
    if left_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP)
    if bottom_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_horizontal_check(room_1, room_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT)
    if right_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP)
    if top_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_horizontal_check(room_1, room_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT)

def left_room_check(room_1, room_2):
    return bool(room_2["OffsetX"] == round(room_1["OffsetX"] - 12.6 * room_2["AreaWidthSize"], 1) and round(room_1["OffsetZ"] - 7.2 * (room_2["AreaHeightSize"] - 1), 1) <= room_2["OffsetZ"] <= round(room_1["OffsetZ"] + 7.2 * (room_1["AreaHeightSize"] - 1), 1))

def bottom_room_check(room_1, room_2):
    return bool(round(room_1["OffsetX"] - 12.6 * (room_2["AreaWidthSize"] - 1), 1) <= room_2["OffsetX"] <= round(room_1["OffsetX"] + 12.6 * (room_1["AreaWidthSize"] - 1), 1) and room_2["OffsetZ"] == round(room_1["OffsetZ"] - 7.2 * room_2["AreaHeightSize"], 1))

def right_room_check(room_1, room_2):
    return bool(room_2["OffsetX"] == round(room_1["OffsetX"] + 12.6 * room_1["AreaWidthSize"], 1) and round(room_1["OffsetZ"] - 7.2 * (room_2["AreaHeightSize"] - 1), 1) <= room_2["OffsetZ"] <= round(room_1["OffsetZ"] + 7.2 * (room_1["AreaHeightSize"] - 1), 1))

def top_room_check(room_1, room_2):
    return bool(round(room_1["OffsetX"] - 12.6 * (room_2["AreaWidthSize"] - 1), 1) <= room_2["OffsetX"] <= round(room_1["OffsetX"] + 12.6 * (room_1["AreaWidthSize"] - 1), 1) and room_2["OffsetZ"] == round(room_1["OffsetZ"] + 7.2 * room_1["AreaHeightSize"], 1))

def door_vertical_check(room_1, room_2, direction_1, direction_2, direction_3):
    for door_1 in map_connections[room_1]:
        if door_string_to_door[door_1].direction_part == direction_1:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_1] and door_string_to_door[door_1].z_block == (door_string_to_door[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)
        if door_string_to_door[door_1].direction_part == direction_2:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_2] and door_string_to_door[door_1].z_block == (door_string_to_door[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)
        if door_string_to_door[door_1].direction_part == direction_3:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_3] and door_string_to_door[door_1].z_block == (door_string_to_door[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)

def door_horizontal_check(room_1, room_2, direction_1, direction_2, direction_3):
    for door_1 in map_connections[room_1]:
        if door_string_to_door[door_1].direction_part == direction_1:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_1] and door_string_to_door[door_1].x_block == (door_string_to_door[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)
        if door_string_to_door[door_1].direction_part == direction_2:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_2] and door_string_to_door[door_1].x_block == (door_string_to_door[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)
        if door_string_to_door[door_1].direction_part == direction_3:
            for door_2 in map_connections[room_2]:
                if door_string_to_door[door_2].direction_part == OppositeDirection[direction_3] and door_string_to_door[door_1].x_block == (door_string_to_door[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)

def get_gimmick_filename(room):
    if room in room_to_gimmick:
        return room_to_gimmick[room]
    return room + "_Gimmick"