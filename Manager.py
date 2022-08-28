import os
import clr
import shutil
import json
import math
import glob
import random
import struct
import sys
import colorsys
import copy
import filecmp
from enum import Enum
from collections import OrderedDict

#Open file information
with open("Data\\FileToPath.json", "r", encoding="utf8") as file_reader:
    file_to_path = json.load(file_reader)
file_to_type = {}
for i in file_to_path:
    if "DataTable" in file_to_path[i]:
        file_to_type[i] = "DataTable"
    elif "Level" in file_to_path[i]:
        file_to_type[i] = "Level"
    elif "StringTable" in file_to_path[i]:
        file_to_type[i] = "StringTable"
    elif "Material" in file_to_path[i]:
        file_to_type[i] = "Material"
    elif "Texture" in file_to_path[i] or "UI" in file_to_path[i] and not "StartupSelecter" in file_to_path[i] and not "Title" in file_to_path[i]:
        file_to_type[i] = "Texture"
    elif "Sound" in file_to_path[i]:
        file_to_type[i] = "Sound"
    else:
        file_to_type[i] = "Blueprint"
load_types = ["DataTable", "Level", "StringTable", "Blueprint", "Material"]
simplify_types = ["DataTable", "StringTable"]

mod_dir = "Tools\\UnrealPak\\Mod\\BloodstainedRotN\\Content"
asset_dir = "Game"

#Open UAssetAPI module
sys.path.append(os.path.abspath("Tools\\UAssetAPI"))
clr.AddReference("UAssetAPI")
clr.AddReference("UAssetSnippet")

from UAssetAPI import *
from UAssetAPI.FieldTypes import *
from UAssetAPI.JSON import *
from UAssetAPI.Kismet import *
from UAssetAPI.Kismet.Bytecode import *
from UAssetAPI.Kismet.Bytecode.Expressions import *
from UAssetAPI.PropertyTypes import *
from UAssetAPI.PropertyTypes.Objects import *
from UAssetAPI.PropertyTypes.Structs import *
from UAssetAPI.UnrealTypes import *
from UAssetAPI.Unversioned import *
from UAssetSnippet import *

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
    global actor_to_properties
    actor_to_properties = {
        "PBEasyTreasureBox_BP_C": {
            "Room": "m01SIP_002",
            "Index": 63
        },
        "PBEasyTreasureBox_BP_C(Gold)": {
            "Room": "m08TWR_019",
            "Index": 989
        },
        "PBPureMiriamTreasureBox_BP_C": {
            "Room": "m01SIP_003",
            "Index": 134
        },
        "HPMaxUp_C": {
            "Room": "m04GDN_002",
            "Index": 16
        },
        "MPMaxUp_C": {
            "Room": "m01SIP_025",
            "Index": 16
        },
        "BulletMaxUp_C": {
            "Room": "m01SIP_024",
            "Index": 2
        },
        "PBBossDoor_BP_C": {
            "Room": "m15JPN_015",
            "Index": 34
        },
        "PBBakkerDoor_BP_C": {
            "Room": "m15JPN_011",
            "Index": 80
        },
        "BP_AreaDoor_C(Left)": {
            "Room": "m11UGD_014",
            "Index": 1
        },
        "BP_AreaDoor_C(Right)": {
            "Room": "m04GDN_016",
            "Index": 1
        },
        "ReadableBookShelf_C": {
            "Room": "m01SIP_005",
            "Index": 163
        },
        "BP_SwitchDoor_C": {
            "Room": "m11UGD_015",
            "Index": 3
        },
        "ToriiWarp_BP_C": {
            "Room": "m07LIB_006",
            "Index": 142
        },
        "B_COM_DamegeWall_1_C": {
            "Room": "m03ENT_000",
            "Index": 0
        },
        "BP_DM_BaseLantern_ShardChild2_C": {
            "Room": "m05SAN_000",
            "Index": 16
        },
        "BP_DM_BloodlessAbilityGimmick_C": {
            "Room": "m01SIP_000",
            "Index": 7
        }
    }
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
        "m18ICE_017"
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
    global rotating_rooms
    rotating_rooms = [
        "m02VIL_008",
        "m02VIL_011",
        "m08TWR_017",
        "m08TWR_018",
        "m08TWR_019",
        "m09TRN_001",
        "m12SND_025",
        "m12SND_026",
        "m12SND_027"
    ]
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
        "LIB_000_0_2_TOP":          "LIB_005_StepSwitch",
        "LIB_005_0_0_BOTTOM":       "LIB_005_StepSwitch",
        "LIB_023_0_2_RIGHT":        "LIB_023_StepSwitch",
        "LIB_029_1_1_TOP":          "LIB_029_DestructibleCeil",
        "LIB_032_0_1_TOP":          "LIB_032_StepSwitch",
        "LIB_041_0_0_BOTTOM":       "LIB_032_StepSwitch",
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
        "TWR_017_3_0_RIGHT",
        "SND_025_0_0_LEFT",
        "SND_026_0_0_LEFT",
        "SND_027_0_0_LEFT"
    ]
    global special_doors
    special_doors = [
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
        "UGD_021_0_0_LEFT",
        "UGD_029_0_1_LEFT",
        "UGD_056_0_3_RIGHT",
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
        "m18ICE_019": "N1009_Enemy"
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
    global map_doors
    map_doors = {}
    global custom_actor_prefix
    custom_actor_prefix = "TR_"
    global datatable
    datatable = {}
    global original_datatable
    original_datatable = {}
    global stringtable
    stringtable = {}
    global key_items
    key_items = [
        "Swordsman",
        "Silverbromide",
        "BreastplateofAguilar",
        "Keyofbacker1",
        "Keyofbacker2",
        "Keyofbacker3",
        "Keyofbacker4",
        "MonarchCrown",
        "Certificationboard"
    ]
    global bit_weapons
    bit_weapons = [
        "CoolShoesOfMrNarita",
        "IceSlewShoes",
        "PoisonSpikeShoes",
        "CrystalSword",
        "ShieldWeapon",
        "XrossBrade",
        "BradeOfEU",
        "LightSaber",
        "JodoSwordLight",
        "SpearCutDownAside",
        "StickOfMagiGirl",
        "DeathBringer",
        "SacredSword",
        "ChargeWideEnd",
        "DrillWideEnd",
        "PetrifactionSword",
        "IcePillarSpear",
        "LoveOfFairyDragon",
        "WhipsOfLightDarkness",
        "TrustMusket"
    ]
    global material_to_offset
    material_to_offset = {
        "MI_N1001_Body": [
            0x110E,
            0x113B,
            0x1175,
            0x11D5,
            0x8BDD,
            0x8C0A,
            0x8C44,
            0x8CA4
        ],
        "MI_N1001_Crystal": [
            0x1CC9,
            0x1CF6,
            0x1D30,
            0x1D90,
            0x1DF6,
            0x1E23,
            0x1E5D,
            0x1EBD,
            0x1A0CE,
            0x1A0FB,
            0x1A135,
            0x1A195,
            0x1A1FB,
            0x1A228,
            0x1A262,
            0x1A2C2
        ],
        "MI_N1001_Eye1": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D1,
            0x86FE,
            0x8738,
            0x8798
        ],
        "MI_N1001_Eye2": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D2,
            0x86FF,
            0x8739,
            0x8799
        ],
        "MI_N1001_Face": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x85A1,
            0x85CE,
            0x8608,
            0x8668
        ],
        "MI_N1001_Hair": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D1,
            0x86FE,
            0x8738,
            0x8798
        ],
        "MI_N1001_Mouth": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D2,
            0x86FF,
            0x8739,
            0x8799
        ],
        "MI_N1001_tongue": [
            0x1ABD,
            0x1AEA,
            0x1B24,
            0x1B84,
            0x13A24,
            0x13A51,
            0x13A8B,
            0x13AEB
        ],
        "MI_N2012": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_Sharded": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_Sword": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_glass": [
            0x2185,
            0x250B,
            0x25D4,
            0x2601,
            0x263B,
            0x266A,
            0x2697,
            0x26D1,
            0x18879,
            0x18BFF,
            0x18CC8,
            0x18CF5,
            0x18D2F,
            0x18D5E,
            0x18D8B,
            0x18DC5
        ],
        "MI_N2004_body": [
            0x1B4E,
            0x1ED4,
            0x1F9D,
            0x1FCA,
            0x2004,
            0x2033,
            0x2060,
            0x209A,
            0x10E2B,
            0x111B1,
            0x1127A,
            0x112A7,
            0x112E1,
            0x11310,
            0x1133D,
            0x11377
        ],
        "M_Mbs004_all_Inst": [
            0x2185,
            0x250B,
            0x25D4,
            0x2601,
            0x263B,
            0x266A,
            0x2697,
            0x26D1,
            0x1887A,
            0x18C00,
            0x18CC9,
            0x18CF6,
            0x18D30,
            0x18D5F,
            0x18D8C,
            0x18DC6
        ]
    }

def load_game_data():
    global game_data
    game_data = {}
    global data_struct
    data_struct = {}
    for i in file_to_type:
        if file_to_type[i] in load_types:
            #Load all game data in one dict
            if file_to_type[i] == "Level":
                extension = ".umap"
            else:
                extension = ".uasset"
            game_data[i] = UAsset(asset_dir + "\\" + file_to_path[i] + "\\" + i.split("(")[0] + extension, UE4Version.VER_UE4_22)
            #Store struct data types for later on
            if file_to_type[i] == "DataTable":
                for e in game_data[i].Exports[0].Table.Data:
                    for o in e.Value:
                        if str(o.PropertyType) == "ArrayProperty":
                            if str(o.ArrayType) == "StructProperty":
                                for u in o.Value:
                                    data_struct[str(u.Name)] = u
    
def load_mod_data():
    global mod_data
    mod_data = {}
    for i in os.listdir("Data\\Dictionary"):
        name, extension = os.path.splitext(i)
        with open("Data\\Dictionary\\" + i, "r", encoding="utf8") as file_reader:
            mod_data[name] = json.load(file_reader)

def load_map(path):
    #Load map related files
    if not path:
        path = "MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json"
    with open(path, "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    if "PB_DT_RoomMaster" in datatable:
        for i in json_file["MapData"]:
            if not i in datatable["PB_DT_RoomMaster"]:
                area_save_room = json_file["MapData"][i]["AreaID"].split("::")[-1] + "_1000"
                datatable["PB_DT_RoomMaster"][i] = copy.deepcopy(datatable["PB_DT_RoomMaster"][area_save_room])
                datatable["PB_DT_RoomMaster"][i]["LevelName"] = i
                add_room_file(i)
            for e in json_file["MapData"][i]:
                datatable["PB_DT_RoomMaster"][i][e] = json_file["MapData"][i][e]
    else:
        datatable["PB_DT_RoomMaster"] = json_file["MapData"]
    mod_data["MapLogic"] = json_file["KeyLogic"]
    mod_data["BloodlessModeMapLogic"] = copy.deepcopy(mod_data["MapLogic"])
    mod_data["MapOrder"] = json_file["AreaOrder"]
    mod_data["OriginalMapOrder"] = [
      "m01SIP",
      "m02VIL",
      "m03ENT",
      "m04GDN",
      "m05SAN",
      "m08TWR",
      "m07LIB",
      "m09TRN",
      "m13ARC",
      "m06KNG",
      "m11UGD",
      "m12SND",
      "m14TAR",
      "m17RVA",
      "m15JPN",
      "m10BIG",
      "m18ICE"
    ]
    mod_data["BloodlessModeMapOrder"] = ["m05SAN"]
    mod_data["BloodlessModeOriginalMapOrder"] = [
      "m05SAN",
      "m03ENT",
      "m02VIL",
      "m01SIP",
      "m04GDN",
      "m08TWR",
      "m07LIB",
      "m09TRN",
      "m13ARC",
      "m06KNG",
      "m11UGD",
      "m12SND",
      "m14TAR",
      "m17RVA",
      "m15JPN",
      "m10BIG",
      "m18ICE"
    ]

def get_map_info():
    #Keep track of every door connection for multi purpose
    for i in datatable["PB_DT_RoomMaster"]:
        map_connections[i] = {}
        doors = convert_flag_to_door(i, datatable["PB_DT_RoomMaster"][i]["DoorFlag"], datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"])
        for e in doors:
            door_string = "_".join([e.room[3:], str(e.x_block), str(e.z_block), str(e.direction_part).split(".")[-1]])
            map_doors[door_string] = e
            map_connections[i][door_string] = []
    for i in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][i]["Unused"]:
            continue
        for e in datatable["PB_DT_RoomMaster"]:
            if datatable["PB_DT_RoomMaster"][e]["Unused"]:
                continue
            if datatable["PB_DT_RoomMaster"][i]["OutOfMap"] != datatable["PB_DT_RoomMaster"][e]["OutOfMap"]:
                continue
            is_adjacent(i, e)

def randomizer_events():
    #Some events need to be triggered by default to avoid conflicts or tedium
    #Galleon cannon wall
    datatable["PB_DT_GimmickFlagMaster"]["SIP_008_BreakWallCannon"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    #Librarian easter egg
    datatable["PB_DT_GimmickFlagMaster"]["LIB_009_PushUpOD_Second"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["LIB_009_PushUpOD_First"]["Id"]
    #Tower cutscene/garden red moon removal
    datatable["PB_DT_EventFlagMaster"]["Event_07_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
    datatable["PB_DT_EventFlagMaster"]["Event_19_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]

def fix_custom_map():
    #Trigger a few events by default
    datatable["PB_DT_GimmickFlagMaster"]["ENT_000_FallStatue"]["Id"]       = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["ENT_007_ZangetuJump"]["Id"]      = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["KNG_015_DestructibleRoof"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["LIB_029_DestructibleCeil"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    datatable["PB_DT_GimmickFlagMaster"]["TRN_002_LeverDoor"]["Id"]        = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    if not "SIP_006_0_2_RIGHT" in map_connections["m01SIP_017"]["SIP_017_0_0_LEFT"]:
        datatable["PB_DT_GimmickFlagMaster"]["SIP_017_BreakWallCannon"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    #Remove the few forced transitions that aren't necessary at all
    for i in ["m04GDN_006", "m06KNG_013", "m07LIB_036", "m15JPN_011", "m88BKR_001", "m88BKR_002", "m88BKR_003", "m88BKR_004"]:
        remove_level_class(i + "_RV", "RoomChange_C")
    #Make Bathin's room enterable from the left
    bathin_left_entrance_fix()
    #The two underground rooms with very specific shapes only display properly based on their Y position below the origin
    #Start by resetting their no traverse list as if they were above 0
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaWidthSize"]*2
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaWidthSize"]*3
    #Then shift those lists if the rooms are below 0
    if datatable["PB_DT_RoomMaster"]["m11UGD_013"]["OffsetZ"] < 0:
        multiplier = abs(int(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["OffsetZ"]/7.2)) - 1
        if multiplier > datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaHeightSize"] - 1:
            multiplier = datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaHeightSize"] - 1
        for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"])):
            datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"][i] -= datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaWidthSize"]*multiplier
    if datatable["PB_DT_RoomMaster"]["m11UGD_031"]["OffsetZ"] < 0:
        multiplier = abs(int(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["OffsetZ"]/7.2)) - 1
        if multiplier > datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaHeightSize"] - 1:
            multiplier = datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaHeightSize"] - 1
        for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"])):
            datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"][i] -= datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaWidthSize"]*multiplier
    #Each area has limitations as to where it can be displayed on the canvas
    #Change area IDs based on their X positions so that everything is always displayed
    for i in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][i]["OffsetX"] < 214.2:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m01SIP"
        elif datatable["PB_DT_RoomMaster"][i]["OffsetX"] + datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"]*12.6 > 1108.8:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m13ARC"
        else:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m03ENT"

def complex_to_simple():
    #The uasset data is inconvenient to access and would take up too much text space in the code
    #Convert them to a simplified dictionary that is similar to Serializer's outputs
    for i in file_to_type:
        if file_to_type[i] in simplify_types:
            if file_to_type[i] == "DataTable":
                datatable[i] = {}
                for e in game_data[i].Exports[0].Table.Data:
                    datatable[i][str(e.Name)] = {}
                    for o in e.Value:
                        datatable[i][str(e.Name)][str(o.Name)] = read_datatable(o)
                original_datatable[i] = copy.deepcopy(datatable[i])
            elif file_to_type[i] == "StringTable":
                stringtable[i] = {}
                for e in game_data[i].Exports[0].Table:
                    stringtable[i][str(e.Key)] = str(e.Value)

def simple_to_complex():
    #Convert the simplified datatables back to their complex versions
    for i in file_to_type:
        if file_to_type[i] in simplify_types:
            if file_to_type[i] == "DataTable":
                ecount = 0
                for e in datatable[i]:
                    ocount = 0
                    #If the datatables had entries added then add an entry slot in the uasset too
                    if ecount >= game_data[i].Exports[0].Table.Data.Count:
                        append_datatable_entry(i, e)
                    for o in datatable[i][e]:
                        #The unused field in room master is only used by the mod, not by the game
                        if i == "PB_DT_RoomMaster" and o == "Unused":
                            ocount += 1
                            continue
                        #Only patch the value if it is different from the original, saves a lot of load time
                        if e in original_datatable[i]:
                            if datatable[i][e][o] == original_datatable[i][e][o]:
                                ocount += 1
                                continue
                        patch_datatable(i, ecount, ocount, datatable[i][e][o])
                        ocount += 1
                    ecount += 1
            elif file_to_type[i] == "StringTable":
                game_data[i].Exports[0].Table.Clear()
                for e in stringtable[i]:
                    game_data[i].Exports[0].Table.Add(FString(e), FString(stringtable[i][e]))

def read_datatable(struct):
    #Read a uasset variable as a python variable
    type = str(struct.PropertyType)
    if type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        value = []
        for i in struct.Value:
            if sub_type == "ByteProperty":
                sub_value = str(i.EnumValue)
            elif sub_type == "FloatProperty":
                sub_value = round(i.Value, 3)
            elif sub_type in ["EnumProperty", "NameProperty", "SoftObjectProperty", "StrProperty", "TextProperty"] and struct.Value:
                sub_value = str(i.Value)
            elif sub_type == "StructProperty":
                sub_value = {}
                for e in i.Value:
                    sub_sub_type = str(e.PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_sub_value = str(e.EnumValue)
                    elif sub_sub_type == "FloatProperty":
                        sub_sub_value = round(e.Value, 3)
                    elif sub_sub_type in ["EnumProperty", "NameProperty", "StrProperty"]:
                        sub_sub_value = str(e.Value)
                    else:
                        sub_sub_value = e.Value
                    sub_value[str(e.Name)] = sub_sub_value
            else:
                sub_value = i.Value
            value.append(sub_value)
    elif type == "ByteProperty":
        value = str(struct.EnumValue)
    elif type == "FloatProperty":
        value = round(struct.Value, 3)
    elif type in ["EnumProperty", "NameProperty", "SoftObjectProperty", "StrProperty"] and struct.Value:
        value = str(struct.Value)
    elif type == "TextProperty":
        value = str(struct.CultureInvariantString)
    else:
        value = struct.Value
    return value

def patch_datatable(file, entry, data, value):
    #Patch a python variable over a uasset's variable
    struct = game_data[file].Exports[0].Table.Data[entry].Value[data]
    type = str(struct.PropertyType)
    if type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        new_list = []
        for i in value:
            if sub_type == "BoolProperty":
                sub_struct = BoolPropertyData()
                sub_struct.Value = i
            elif sub_type == "ByteProperty":
                sub_struct = BytePropertyData()
                sub_struct.ByteType = BytePropertyType.FName
                sub_struct.EnumValue = FName.FromString(game_data[file], i)
            elif sub_type == "EnumProperty":
                sub_struct = EnumPropertyData()
                sub_struct.Value = FName.FromString(game_data[file], i)
            elif sub_type == "FloatProperty":
                sub_struct = FloatPropertyData()
                sub_struct.Value = i
            elif sub_type == "IntProperty":
                sub_struct = IntPropertyData()
                sub_struct.Value = i
            elif sub_type == "NameProperty":
                sub_struct = NamePropertyData()
                sub_struct.Value = FName.FromString(game_data[file], i)
            elif sub_type == "SoftObjectProperty":
                sub_struct = SoftObjectPropertyData()
                sub_struct.Value = FName.FromString(game_data[file], i)
            elif sub_type == "StrProperty":
                sub_struct = StrPropertyData()
                sub_struct.Value = FString(i)
            elif sub_type == "StructProperty":
                sub_struct = data_struct[str(struct.Name)].Clone()
                count = 0
                for e in i:
                    sub_sub_type = str(sub_struct.Value[count].PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_struct.Value[count].EnumValue = FName.FromString(game_data[file], i[e])
                    elif sub_sub_type in ["NameProperty", "EnumProperty"]:
                        sub_struct.Value[count].Value = FName.FromString(game_data[file], i[e])
                    elif sub_sub_type == "StrProperty":
                        sub_struct.Value[count].Value = FString(i[e])
                    else:
                        sub_struct.Value[count].Value = i[e]
                    count += 1
            elif sub_type == "TextProperty":
                sub_struct = TextPropertyData()
                sub_struct.CultureInvariantString = FString(i)
            new_list.append(sub_struct)
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = new_list
    elif type == "ByteProperty":
        game_data[file].Exports[0].Table.Data[entry].Value[data].EnumValue = FName.FromString(game_data[file], value)
    elif type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FName.FromString(game_data[file], value)
    elif type == "StrProperty" and value:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FString(value)
    elif type == "TextProperty" and value:
        game_data[file].Exports[0].Table.Data[entry].Value[data].CultureInvariantString = FString(value)
    else:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = value

def append_datatable_entry(file, entry):
    #Append a new datatable entry to the end to be edited later on
    new_entry = game_data[file].Exports[0].Table.Data[0].Clone()
    new_entry.Name = FName.FromString(game_data[file], entry)
    game_data[file].Exports[0].Table.Data.Add(new_entry)

def apply_tweaks():
    #Make levels identical in all modes
    #This needs to be done before applying the json tweaks so that exceptions can be patched over
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(i)["Enemy"]:
            continue
        datatable["PB_DT_CharacterParameterMaster"][i]["HardEnemyLevel"]                       = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["NightmareEnemyLevel"]                  = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeDefaultEnemyLevel"]       = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeHardEnemyLevel"]          = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeNightmareEnemyLevel"]     = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyHPOverride"]         = 0.0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyExperienceOverride"] = 0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyStrIntMultiplier"]   = 1.0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyConMndMultiplier"]   = 1.0
    #Apply manual tweaks defined in the json
    for i in mod_data["DefaultTweak"]:
        for e in mod_data["DefaultTweak"][i]:
            for o in mod_data["DefaultTweak"][i][e]:
                datatable[i][e][o] = mod_data["DefaultTweak"][i][e][o]
    #Loop through all enemies
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(i)["Enemy"]:
            continue
        if is_enemy(i)["Boss"]:
            #Make boss health scale with level
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*(99/datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]))
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]/5)*5
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP99Enemy"] = datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]
            #Make experience a portion of health
            if i[0:5] in ["N3106", "N3107", "N3108"]:
                multiplier = 1
            else:
                multiplier = (4/3)
            if datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = int(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*multiplier)
                datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = int(datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"]/100) + 2
            #Expand expertise point range that scales with level
            #In vanilla the range is too small and barely makes a difference
            if datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 15
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
            #Set stone type
            #Some regular enemies are originally set to the boss stone type which doesn't work well when petrified
            datatable["PB_DT_CharacterParameterMaster"][i]["StoneType"] = "EPBStoneType::Boss"
        else:
            if datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = int(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*(2/3))
                datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = int(datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"]/100) + 2
            if datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 10
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
            datatable["PB_DT_CharacterParameterMaster"][i]["StoneType"] = "EPBStoneType::Mob"
        #Make level 1 health based off of level 99 health
        datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"] = int(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]/100) + 2.0
        datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP"] = datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"]
        #Give all enemies a luck stat which reduces the chances of critting them
        #Originally only Gebel, Valefar and OD have one
        if datatable["PB_DT_CharacterParameterMaster"][i]["LUC"] == 0 and i != "N1008":
            datatable["PB_DT_CharacterParameterMaster"][i]["LUC"]        = 5.0
            datatable["PB_DT_CharacterParameterMaster"][i]["LUC99Enemy"] = 50.0
        #Allow Zangetsu to chain grab everyone
        #Whether he can grab or not is entirely based on the enemy's stone resistance
        #As long as it's not 100% resist the chain grab will connect so cap stone resistance at 99.9%
        if datatable["PB_DT_CharacterParameterMaster"][i]["STO"] >= 100.0:
            datatable["PB_DT_CharacterParameterMaster"][i]["STO"] = 99.9
    #Make up for the increased expertise range
    for i in datatable["PB_DT_ArtsCommandMaster"]:
        datatable["PB_DT_ArtsCommandMaster"][i]["Expertise"] = int(datatable["PB_DT_ArtsCommandMaster"][i]["Expertise"]*2.5)
    #Lock 8 bit weapons behind recipes so that they aren't always easily accessible
    for i in datatable["PB_DT_CraftMaster"]:
        if i in bit_weapons:
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe018"
        elif i[:-1] in bit_weapons and i[-1] == "2":
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe019"
        elif i[:-1] in bit_weapons and i[-1] == "3":
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe020"
    #Remove the minimal damage addition on attacks
    for i in datatable["PB_DT_DamageMaster"]:
        if i == "N3108_SUICIDE":
            datatable["PB_DT_DamageMaster"][i]["SA_Correction"]  = 0.0
            datatable["PB_DT_DamageMaster"][i]["STR_Correction"] = 0.0
            datatable["PB_DT_DamageMaster"][i]["INT_Correction"] = 0.0
            datatable["PB_DT_DamageMaster"][i]["FixedDamage"]    = 7777.0
        else:
            datatable["PB_DT_DamageMaster"][i]["FixedDamage"] = 0.0
    #Loop through drops
    for i in datatable["PB_DT_DropRateMaster"]:
        #Increase default drop rates
        if datatable["PB_DT_DropRateMaster"][i]["AreaChangeTreasureFlag"]:
            drop_rate = mod_data["ItemDrop"]["StandardMat"]["ItemRate"]
        else:
            drop_rate = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]
        #Keep dulla head drops relatively low due to their spawn frequency
        if i.split("_")[0] in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["ShardRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        for e in ["RareItemRate", "CommonRate", "RareIngredientRate", "CommonIngredientRate"]:
            if 0.0 < datatable["PB_DT_DropRateMaster"][i][e] < 100.0:
                datatable["PB_DT_DropRateMaster"][i][e] = drop_rate*drop_rate_multiplier
        #Make coin type match the amount
        if datatable["PB_DT_DropRateMaster"][i]["CoinOverride"] > 0:
            datatable["PB_DT_DropRateMaster"][i]["CoinType"] = "EDropCoin::D" + str(datatable["PB_DT_DropRateMaster"][i]["CoinOverride"])
    #Loop through all items
    for i in datatable["PB_DT_ItemMaster"]:
        #Remove dishes from shop to prevent heal spam
        #In vanilla you can easily stock up on an infinite amount of them which breaks the game completely
        #This change also makes regular potions more viable now
        if i in mod_data["ItemDrop"]["Dish"]["ItemPool"]:
            datatable["PB_DT_ItemMaster"][i]["max"]       = 1
            datatable["PB_DT_ItemMaster"][i]["buyPrice"]  = 0
            datatable["PB_DT_ItemMaster"][i]["sellPrice"] = 0
        #Update icon pointer of 8 bit weapons for the new icons
        #The icon texture was edited so that all new icons are evenly shifted from the original ones
        if i[:-1] in bit_weapons and i[-1] == "2":
            datatable["PB_DT_ItemMaster"][i]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][i]["IconPath"]) + 204)
        elif i[:-1] in bit_weapons and i[-1] == "3":
            datatable["PB_DT_ItemMaster"][i]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][i]["IconPath"]) + 338)
    #Loop through all shards
    for i in datatable["PB_DT_ShardMaster"]:
        #Make all shard colors match their type
        datatable["PB_DT_ShardMaster"][i]["ShardColorOverride"] = "EShardColor::None"
        #Make all shards ignore standstill
        datatable["PB_DT_ShardMaster"][i]["IsStopByAccelWorld"] = False
    #Rename the second Zangetsu boss so that he isn't confused with the first
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N1011_STRONG"] = mod_data["EnemyTranslation"]["N1011_STRONG"]
    #Update Jinrai cost description
    stringtable["PBMasterStringTable"]["ARTS_TXT_017_00"] += str(datatable["PB_DT_ArtsCommandMaster"]["JSword_GodSpeed1"]["CostMP"])
    #Slightly change Igniculus' descriptions to match other familiar's
    stringtable["PBMasterStringTable"]["SHARD_EFFECT_TXT_FamiliaIgniculus"] = stringtable["PBMasterStringTable"]["SHARD_EFFECT_TXT_FamiliaArcher"]
    stringtable["PBMasterStringTable"]["SHARD_NAME_FamiliaIgniculus"] = "Familiar: Igniculus"
    #Add DLCs to the enemy archives
    add_enemy_to_archive("N2016", ["SYS_SEN_AreaName021"], None, "N2015")
    add_enemy_to_archive("N2017", [], None, "N2008")
    #Give the new dullahammer a unique name and look
    datatable["PB_DT_CharacterParameterMaster"]["N3127"]["NameStrKey"] = "ENEMY_NAME_N3127"
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N3127"] = mod_data["EnemyTranslation"]["N3127"]
    change_material_hsv("MI_N3127_Eye", "EmissiveColor" , (215, 100, 100))
    change_material_hsv("MI_N3127_Eye", "HighlightColor", (215,  65, 100))
    #Give Guardian his own shard drop
    datatable["PB_DT_CharacterMaster"]["N2017"]["ItemDrop"] = "N2017_Shard"
    datatable["PB_DT_DropRateMaster"]["N2017_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Deepsinker_Shard"])
    datatable["PB_DT_DropRateMaster"]["N2017_Shard"]["ShardId"] = "TissRosain"
    datatable["PB_DT_CraftMaster"]["TissRosain"]["OpenKeyRecipeID"] = "Medal019"
    #Rebalance boss rush mode a bit
    #Remove all consumables from inventory
    for i in game_data["PBExtraModeInfo_BP"].Exports[1].Data[7].Value:
        i.Value[1].Value = 0
    #Start both stages at level 50
    for i in range(8, 14):
        game_data["PBExtraModeInfo_BP"].Exports[1].Data[i].Value = 50
    #Give all bosses level 66
    for i in game_data["PBExtraModeInfo_BP"].Exports[1].Data[14].Value:
        i.Value.Value = 66
    #Make the second train gate a regular gate rather than a debug
    game_data["m09TRN_004_Gimmick"].Exports[257].Data[18].Value = False
    #Give the lever door in upper cathedral its own gimmick flag instead of being shared with the hall one
    game_data["m05SAN_017_Gimmick"].Exports[1].Data[7].Value = FName(game_data["m05SAN_017_Gimmick"], "SAN_017_LockDoor")
    datatable["PB_DT_GimmickFlagMaster"]["SAN_017_LockDoor"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["SAN_017_LockDoor"]["Id"] = 186
    #Add the missing gate warps for the extra characters
    #That way impassable gates are no longer a problem
    add_extra_mode_warp("m04GDN_013_Gimmick", FVector(2460, 0, 2100), FRotator(180,   0,   0), FVector(3080, 0, 1800), FRotator(  0,   0,   0))
    add_extra_mode_warp("m05SAN_003_Gimmick", FVector( 220, 0, 5940), FRotator(  0,   0, 180), FVector(2300, 0, 6000), FRotator(  0, 180,   0))
    add_extra_mode_warp("m05SAN_003_Gimmick", FVector(1400, 0,  900), FRotator(180,   0,   0), FVector(1400, 0,   60), FRotator(  0,   0,   0))
    add_extra_mode_warp("m07LIB_008_Gimmick", FVector(1200, 0,  960), FRotator(  0,   0,   0), FVector( 840, 0, 1380), FRotator(180,   0,   0))
    add_extra_mode_warp("m07LIB_012_Gimmick", FVector(1080, 0,  480), FRotator(  0, 180,   0), FVector( 940, 0,  180), FRotator(  0,   0,   0))
    add_extra_mode_warp("m07LIB_014_Gimmick", FVector( 540, 0,  450), FRotator(-90, 180,   0), FVector(1080, 0,  240), FRotator(  0,   0,   0))
    add_extra_mode_warp("m07LIB_022_Gimmick", FVector( 420, 0,  720), FRotator(180,   0,   0), FVector( 520, 0,  600), FRotator(  0,   0,   0))
    add_extra_mode_warp("m07LIB_035_Gimmick", FVector( 420, 0, 1520), FRotator(-90, 180,   0), FVector( 540, 0, 1680), FRotator( 90, 180,   0))
    add_extra_mode_warp("m08TWR_016_Gimmick", FVector( 600, 0,  240), FRotator(  0, 180,   0), FVector( 600, 0, -180), FRotator(  0,   0,   0))
    add_extra_mode_warp("m11UGD_025_Gimmick", FVector(1745, 0,  565), FRotator(  0, 180,   0), FVector(2205, 0,  630), FRotator(  0,   0,   0))
    add_extra_mode_warp("m11UGD_056_Gimmick", FVector( 880, 0, 2220), FRotator(180,   0,   0), FVector(1050, 0, 2400), FRotator(  0,   0,   0))
    add_extra_mode_warp("m11UGD_056_Gimmick", FVector( 600, 0, 1300), FRotator(-90, 180,   0), FVector( 660, 0, 1500), FRotator( 90, 180,   0))
    add_extra_mode_warp("m12SND_006_Gimmick", FVector( 660, 0,   60), FRotator(  0,   0,   0), FVector( 420, 0,   60), FRotator(  0, 180,   0))
    add_extra_mode_warp("m13ARC_006_Gimmick", FVector( 600, 0,  960), FRotator(  0,   0,   0), FVector( 420, 0,  960), FRotator(  0, 180,   0))
    add_extra_mode_warp("m15JPN_002_Gimmick", FVector(1740, 0, 1260), FRotator(180,   0,   0), FVector(1180, 0,   75), FRotator(  0,   0,   0))
    add_extra_mode_warp("m17RVA_001_Gimmick", FVector( 800, 0, 2080), FRotator(  0,   0, 180), FVector( 540, 0, 1800), FRotator(  0, 180,   0))
    add_extra_mode_warp("m17RVA_011_Gimmick", FVector(1900, 0, 2080), FRotator(180,   0,   0), FVector(2140, 0, 2080), FRotator(  0,   0, 180))
    add_extra_mode_warp("m18ICE_008_Gimmick", FVector(1745, 0,  565), FRotator(  0, 180,   0), FVector(2205, 0,  630), FRotator(  0,   0,   0))
    #Add the missing Bloodless candle that was accidentally removed in a recent game update
    add_level_actor("m07LIB_009_Gimmick", "BP_DM_BloodlessAbilityGimmick_C", FVector(720, -120, 1035), FRotator(0, 0, 0), FVector(1, 1, 1), {"UnlockAbilityType": FName(game_data["m07LIB_009_Gimmick"], "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP_5")})
    #Due to Focalor being scrapped the devs put aqua stream on a regular enemy instead but this can cause first playthroughs to miss out on the shard
    #Add a shard candle for it so that it becomes a guaranteed
    add_level_actor("m11UGD_015_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", FVector(720, -60, 390), FRotator(0, 0, 0), FVector(1, 1, 1), {"ShardID": FName(game_data["m11UGD_015_Gimmick"], "Aquastream"), "GimmickFlag": FName(game_data["m11UGD_015_Gimmick"], "AquastreamLantarn001")})
    datatable["PB_DT_GimmickFlagMaster"]["AquastreamLantarn001"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["AquastreamLantarn001"]["Id"] = 187
    datatable["PB_DT_DropRateMaster"]["Aquastream_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Deepsinker_Shard"])
    datatable["PB_DT_DropRateMaster"]["Aquastream_Shard"]["ShardId"] = "Aquastream"
    #Add a shard candle for Igniculus in Celeste's room
    #That way Celeste key becomes relevant and Igniculus can be obtained in story mode
    add_level_actor("m88BKR_003_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", FVector(660, -120, 315), FRotator(0, 0, 0), FVector(1, 1, 1), {"ShardID": FName(game_data["m88BKR_003_Gimmick"], "FamiliaIgniculus"), "GimmickFlag": FName(game_data["m88BKR_003_Gimmick"], "IgniculusLantarn001")})
    datatable["PB_DT_GimmickFlagMaster"]["IgniculusLantarn001"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["IgniculusLantarn001"]["Id"] = 188
    datatable["PB_DT_DropRateMaster"]["FamiliaIgniculus_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["FamiliaArcher_Shard"])
    datatable["PB_DT_DropRateMaster"]["FamiliaIgniculus_Shard"]["ShardId"] = "FamiliaIgniculus"
    #The HavePatchPureMiriam gimmick flag triggers as soon as a Pure Miriam chest is loaded in a room
    #So place one in the first ship room for this flag to trigger as soon as the game starts
    add_level_actor("m01SIP_000_Gimmick", "PBPureMiriamTreasureBox_BP_C", FVector(-999, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1), {"DropItemID": FName(game_data["m01SIP_000_Gimmick"], "AAAA_Shard"), "ItemID": FName(game_data["m01SIP_000_Gimmick"], "AAAA_Shard")})
    #Remove the Dullhammer in the first galleon room on hard to prevent rough starts
    #That way you can at least save once before the game truly starts
    remove_level_class("m01SIP_001_Enemy_Hard", "Chr_N3015_C")
    mod_data["EnemyLocation"]["N3015"]["HardModeRooms"].remove("m01SIP_001")
    #Also remove the bone mortes from that one crowded room in galleon
    remove_level_class("m01SIP_014_Enemy_Hard", "Chr_N3004_C")
    mod_data["EnemyLocation"]["N3004"]["HardModeRooms"].remove("m01SIP_014")
    #Remove the iron maidens that were added by the devs in an update in the tall entrance shaft
    #This is to simplify the logic a bit as we have no control over the Craftwork shard placement
    #To compensate for this the cooldown on spike damage was reduced, making it less likely for the player to tank through
    remove_level_class("m03ENT_000_Gimmick", "BP_IronMaiden_C")
    #Add more spikes in return
    add_level_actor("m03ENT_000_Gimmick", "B_COM_DamegeWall_1_C", FVector(420, 120, 7140), FRotator(0, 0, 0), FVector(1, 1,  1), {})
    add_level_actor("m03ENT_000_Gimmick", "B_COM_DamegeWall_1_C", FVector(  0, 120, 7380), FRotator(0, 0, 0), FVector(1, 1, -1), {})
    add_level_actor("m03ENT_000_Gimmick", "B_COM_DamegeWall_1_C", FVector(420, 120, 7860), FRotator(0, 0, 0), FVector(1, 1,  1), {})
    add_level_actor("m03ENT_000_Gimmick", "B_COM_DamegeWall_1_C", FVector(420, 120, 8760), FRotator(0, 0, 0), FVector(1, 1, -1), {})
    add_level_actor("m03ENT_000_Gimmick", "B_COM_DamegeWall_1_C", FVector(  0, 120, 9240), FRotator(0, 0, 0), FVector(1, 1,  1), {})
    #With this mod vanilla rando is pointless and obselete so remove its widget
    remove_vanilla_rando()
    #Store original enemy stats for convenience
    global original_enemy_stats
    original_enemy_stats = {}
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        original_enemy_stats[i] = {}
        original_enemy_stats[i]["Level"] = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        original_enemy_stats[i]["POI"] = datatable["PB_DT_CharacterParameterMaster"][i]["POI"]
        original_enemy_stats[i]["CUR"] = datatable["PB_DT_CharacterParameterMaster"][i]["CUR"]
        original_enemy_stats[i]["STO"] = datatable["PB_DT_CharacterParameterMaster"][i]["STO"]
        original_enemy_stats[i]["SLO"] = datatable["PB_DT_CharacterParameterMaster"][i]["SLO"]

def search_and_replace_string(filename, class_name, data, old_value, new_value):
    #Search for a specific piece of data to change in a level file and swap it
    for i in game_data[filename].Exports:
        if class_name == str(game_data[filename].Imports[abs(int(str(i.ClassIndex))) - 1].ObjectName):
            for e in i.Data:
                if str(e.Name) == data and str(e.Value) == old_value:
                    e.Value = FName.FromString(game_data[filename], new_value)

def change_lip_pointer(event, event_replacement):
    #Simply swap the file's name in the name map and save as the new name
    event = "en_" + event + "_LIP"
    event_replacement = "en_" + event_replacement + "_LIP"
    
    if event_replacement + ".uasset" in os.listdir("Data\\LipSync"):
        event_replacement_data = UAsset("Data\\LipSync\\" + event_replacement + ".uasset", UE4Version(517))
        index = event_replacement_data.SearchNameReference(FString(event_replacement))
        event_replacement_data.SetNameReference(index, FString(event))
        index = event_replacement_data.SearchNameReference(FString("/Game/Core/UI/Dialog/Data/LipSync/" + event_replacement))
        event_replacement_data.SetNameReference(index, FString("/Game/Core/UI/Dialog/Data/LipSync/" + event))
        event_replacement_data.Write(mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + event + ".uasset")
    elif event + ".uasset" in os.listdir("Data\\LipSync"):
        event_data = UAsset("Data\\LipSync\\" + event + ".uasset", UE4Version(517))
        for i in event_data.Exports:
            if str(i.ObjectName) == event:
                i.Data.Clear()
        event_data.Write(mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + event + ".uasset")

def change_portrait_pointer(portrait, portrait_replacement):
    #Simply swap the file's name in the name map and save as the new name
    portrait_replacement_data = UAsset(asset_dir + "\\" + file_to_path[portrait_replacement] + "\\" + portrait_replacement + ".uasset", UE4Version(517))
    index = portrait_replacement_data.SearchNameReference(FString(portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString(portrait))
    index = portrait_replacement_data.SearchNameReference(FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait))
    portrait_replacement_data.Write(mod_dir + "\\" + file_to_path[portrait] + "\\" + portrait + ".uasset")

def add_room_file(room):
    area_path = "ACT" + room[1:3] + "_" + room[3:6]
    new_file = UAsset(asset_dir + "\\" + file_to_path["m01SIP_1000_RV"] + "\\m01SIP_1000_RV.umap", UE4Version(517))
    index = new_file.SearchNameReference(FString("m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString(room + "_RV"))
    index = new_file.SearchNameReference(FString("/Game/Core/Environment/ACT01_SIP/Level/m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString("/Game/Core/Environment/" + area_path + "/Level/" + room + "_RV"))
    new_file.Exports[5].Data[1].Value = FName.FromString(new_file, room)
    new_file.Write(mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")

def add_starting_pickup(drop_id):
    #Overlay an upgrade on top of Miriam's starting position to instantly get its content when starting a game
    add_level_actor("m01SIP_000_Gimmick", "HPMaxUp_C", FVector(817, 100, 146), FRotator(0, 0, 0), FVector(1, 1, 1), {"DropRateID": FName.FromString(game_data["m01SIP_000_Gimmick"], drop_id)})

def update_descriptions():
    #Add magical stats to descriptions
    for i in datatable["PB_DT_ArmorMaster"]:
        if not "ITEM_EXPLAIN_" + i in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_ArmorMaster"][i]["MagicAttack"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff8000\">mATK " + str(datatable["PB_DT_ArmorMaster"][i]["MagicAttack"]) + "</>")
        if datatable["PB_DT_ArmorMaster"][i]["MagicDefense"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff00ff\">mDEF " + str(datatable["PB_DT_ArmorMaster"][i]["MagicDefense"]) + "</>")
    #Add restoration amount to descriptions
    for i in datatable["PB_DT_SpecialEffectDefinitionMaster"]:
        if not "ITEM_EXPLAIN_" + i in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeHP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00ff00\">HP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeMP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00bfff\">MP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
    #Add Shovel Armor's attack stat to its description
    append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_Shovelarmorsarmor", "<span color=\"#ff0000\">wATK " + str(int(datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"])) + "</>")

def update_map_doors():
    #Place doors next to their corresponding transitions if the adjacent room is of a special type
    #Do this even for the default map as some rooms are missing boss doors
    #Boss doors
    #Remove originals
    for i in boss_door_rooms:
        if i in room_to_gimmick:
            filename = room_to_gimmick[i]
        else:
            filename = i + "_Gimmick"
        remove_level_class(filename, "PBBossDoor_BP_C")
    #Add new
    for i in room_to_boss:
        for e in map_connections[i]:
            for o in map_connections[i][e]:
                if o in door_skip:
                    continue
                if map_doors[o].room in room_to_boss:
                    continue
                if map_doors[o].room in room_to_backer:
                    continue
                if not map_doors[o].room in mod_data["MapLogic"]:
                    continue
                if map_doors[o].room in room_to_gimmick:
                    filename = room_to_gimmick[map_doors[o].room]
                else:
                    filename = map_doors[o].room + "_Gimmick"
                location = FVector(0, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"] = FName.FromString(game_data[filename], room_to_boss[i])
                if map_doors[o].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    properties["IsRight"] = False
                    if o in special_doors:
                        rotation.Yaw += 15
                if map_doors[o].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[o].room]["AreaWidthSize"]*1260
                    properties["IsRight"] = True
                    if o in special_doors:
                        rotation.Yaw -= 15
                location.Z = map_doors[o].z_block*720 + 240.0
                if map_doors[o].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[o].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                add_level_actor(filename, "PBBossDoor_BP_C", location, rotation, scale, properties)
                #If the door is a breakable wall we don't want the boss door to overlay it, so break it by default
                if o in wall_to_gimmick_flag:
                    datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[o]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if o == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Backer doors
    #Remove originals
    for i in backer_door_rooms:
        if i in room_to_gimmick:
            filename = room_to_gimmick[i]
        else:
            filename = i + "_Gimmick"
        for e in range(len(game_data[filename].Exports)):
            class_name = str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[e].ClassIndex))) - 1].ObjectName)
            if class_name == "PBBakkerDoor_BP_C":
                for o in game_data[filename].Exports[e].Data:
                    if str(o.Name) == "RootComponent":
                        root_index = int(str(o.Value)) - 1
                game_data[filename].Exports[root_index].Data[0].Value[0].Value = FVector(-999, 0, 0)
    #Add new
    for i in room_to_backer:
        for e in map_connections[i]:
            for o in map_connections[i][e]:
                if o in door_skip:
                    continue
                if map_doors[o].room in room_to_boss:
                    continue
                if map_doors[o].room in room_to_backer:
                    continue
                if not map_doors[o].room in mod_data["MapLogic"]:
                    continue
                if map_doors[o].room in room_to_gimmick:
                    filename = room_to_gimmick[map_doors[o].room]
                else:
                    filename = map_doors[o].room + "_Gimmick"
                location = FVector(0, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"]     = FName.FromString(game_data[filename], room_to_backer[i][0])
                properties["KeyItemID"]  = FName.FromString(game_data[filename], "Keyofbacker" + str(room_to_backer[i][1]))
                properties["TutorialID"] = FName.FromString(game_data[filename], "KeyDoor" + "{:02x}".format(room_to_backer[i][1]))
                if room_to_backer[i][0] == "None":
                    properties["IsMusicBoxRoom"] =  True
                if map_doors[o].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    if o in special_doors:
                        rotation.Yaw += 15
                if map_doors[o].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[o].room]["AreaWidthSize"]*1260
                    if o in special_doors:
                        rotation.Yaw -= 15
                location.Z = map_doors[o].z_block*720 + 240.0
                if map_doors[o].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[o].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                actor_index = len(game_data[filename].Exports)
                add_level_actor(filename, "PBBakkerDoor_BP_C", location, rotation, scale, properties)
                #Fix a snippet issue causing a crash
                open_timeline_index = int(str(game_data[filename].Exports[actor_index].Data[3].Value)) - 1
                close_timeline_index = int(str(game_data[filename].Exports[actor_index].Data[2].Value)) - 1
                open_curve_float_index = abs(int(str(game_data[filename].Exports[open_timeline_index].Data[0].Value[1].Value[0].Value[0].Value))) - 1
                close_curve_float_index = abs(int(str(game_data[filename].Exports[close_timeline_index].Data[0].Value[1].Value[0].Value[0].Value))) - 1
                game_data[filename].Imports[open_curve_float_index].ObjectName = FName.FromString(game_data[filename], "CurveFloat_0")
                game_data[filename].Imports[close_curve_float_index].ObjectName = FName.FromString(game_data[filename], "CurveFloat_0_1")
                #If the door is a breakable wall we don't want the backer door to overlay it, so break it by default
                if o in wall_to_gimmick_flag:
                    datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[o]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if o == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Area doors
    #Remove originals
    for i in area_door_rooms:
        if i in room_to_gimmick:
            filename = room_to_gimmick[i]
        else:
            filename = i + "_Gimmick"
        remove_level_class(filename, "BP_AreaDoor_C")
    #Add new
    doors_done = []
    for i in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][i]["RoomType"] != "ERoomType::Load" or i == "m03ENT_1200":
            continue
        for e in map_connections[i]:
            for o in map_connections[i][e]:
                if o in doors_done:
                    continue
                if o in door_skip:
                    continue
                if o in special_doors:
                    continue
                if map_doors[o].room in room_to_boss:
                    continue
                if map_doors[o].room in room_to_backer:
                    continue
                if not map_doors[o].room in mod_data["MapLogic"]:
                    continue
                #If the door is too close to a cutscene disable the event to prevent softlocks
                if map_doors[o].room == "m03ENT_006":
                    datatable["PB_DT_EventFlagMaster"]["Event_05_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if o == "ARC_001_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_09_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if o == "TAR_000_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_12_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                #If the entrance has very little floor shift the door closer to the transition to prevent softlocks
                if o in floorless_doors:
                    x_offset = -20
                else:
                    x_offset = 40
                if map_doors[o].room in room_to_gimmick:
                    filename = room_to_gimmick[map_doors[o].room]
                else:
                    filename = map_doors[o].room + "_Gimmick"
                location = FVector(x_offset, -180, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                properties = {}
                properties["IsInvertingOpen"] = False
                if map_doors[o].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    class_name = "BP_AreaDoor_C(Left)"
                if map_doors[o].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[o].room]["AreaWidthSize"]*1260 - x_offset
                    class_name = "BP_AreaDoor_C(Right)"
                location.Z = map_doors[o].z_block*720 + 240.0
                if map_doors[o].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[o].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                add_level_actor(filename, class_name, location, rotation, scale, properties)
                #If the door is a breakable wall we don't want the area door to overlay it, so break it by default
                if o in wall_to_gimmick_flag:
                    datatable["PB_DT_GimmickFlagMaster"][wall_to_gimmick_flag[o]]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if o == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
                #Since transition rooms are double make sure that a door only gets added once
                doors_done.append(o)

def update_map_indicators():
    #Place a bookshelf in front of every save and warp point to make map traversal easier
    #Only do it for custom maps as the default map already has bookshelves with text
    #Remove originals
    for i in bookshelf_rooms:
        if i in room_to_gimmick:
            filename = room_to_gimmick[i]
        else:
            filename = i + "_Gimmick"
        remove_level_class(filename, "ReadableBookShelf_C")
    #Add new
    doors_done = []
    for i in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][i]["RoomType"] != "ERoomType::Save" and datatable["PB_DT_RoomMaster"][i]["RoomType"] != "ERoomType::Warp":
            continue
        for e in map_connections[i]:
            for o in map_connections[i][e]:
                if o in door_skip:
                    continue
                if map_doors[o].room in room_to_boss:
                    continue
                if map_doors[o].room in room_to_backer:
                    continue
                if not map_doors[o].room in mod_data["MapLogic"]:
                    continue
                if o in ["VIL_005_0_0_RIGHT", "VIL_006_0_1_LEFT"]:
                    continue
                if map_doors[o].room in room_to_gimmick:
                    filename = room_to_gimmick[map_doors[o].room]
                else:
                    filename = map_doors[o].room + "_Gimmick"
                location = FVector(-80, -120, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                properties = {}
                properties["DiaryID"] = FName.FromString(game_data[filename], "None")
                if map_doors[o].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -30
                if map_doors[o].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[o].room]["AreaWidthSize"]*1260 - 50
                    rotation.Yaw = 30
                location.Z = map_doors[o].z_block*720 + 240.0
                if map_doors[o].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[o].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                    location.Z += 180.0
                add_level_actor(filename, "ReadableBookShelf_C", location, rotation, scale, properties)
                #Remove the magic door in that one galleon room so that it never overlays with anything
                if o == "SIP_002_0_0_RIGHT":
                    remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")
    #Fill empty entrances with an impassable door to prevent softlocks
    #Add new
    door_height = 240
    door_width = 44
    for i in map_connections:
        for e in map_connections[i]:
            if map_connections[i][e] and map_connections[i][e] != "m03ENT_1200":
                continue
            if e in door_skip:
                continue
            if i in room_to_boss:
                continue
            if i in room_to_backer:
                continue
            if not i in mod_data["MapLogic"]:
                continue
            if i in room_to_gimmick:
                filename = room_to_gimmick[i]
            else:
                filename = i + "_Gimmick"
            location = FVector(0, -360, 0)
            rotation = FRotator(0, 0, 0)
            scale    = FVector(1, 1, 1)
           #Global direction
            if map_doors[e].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                location.X = -18
                location.Z = map_doors[e].z_block*720 + door_height
                lever_offset = -160
                if e in special_doors:
                    rotation.Yaw += 20
            if map_doors[e].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                location.X = datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"]*1260 + 18
                location.Z = map_doors[e].z_block*720 + door_height
                lever_offset = 160
                if e in special_doors:
                    rotation.Yaw -= 20
            if map_doors[e].direction_part in [Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT]:
                location.X = map_doors[e].x_block*1260 + 510.0
                location.Z = datatable["PB_DT_RoomMaster"][i]["AreaHeightSize"]*720 - 5
                rotation.Pitch = -90
                lever_offset = -160
            if map_doors[e].direction_part in [Direction.BOTTOM, Direction.BOTTOM_LEFT, Direction.BOTTOM_RIGHT]:
                location.X = map_doors[e].x_block*1260 + 510.0
                location.Z = 5
                rotation.Pitch = -90
                lever_offset = 160
            #Sub direction
            if map_doors[e].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                if datatable["PB_DT_RoomMaster"][i]["AreaID"] == "EAreaID::m10BIG":
                    location.Z -= door_height
                elif "_".join([i[3:], str(map_doors[e].x_block), str(map_doors[e].z_block), str(map_doors[e].direction_part).split(".")[-1].split("_")[0]]) in map_connections[i]:
                    location.Z -= door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    location.Z -= door_height*scale.Z - door_height
                else:
                    location.Z += 180
            if map_doors[e].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                if datatable["PB_DT_RoomMaster"][i]["AreaID"] == "EAreaID::m10BIG":
                    location.Z += door_height
                elif "_".join([i[3:], str(map_doors[e].x_block), str(map_doors[e].z_block), str(map_doors[e].direction_part).split(".")[-1].split("_")[0]]) in map_connections[i]:
                    location.Z += door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    if map_doors[e].direction_part == Direction.LEFT_TOP:
                        location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    else:
                        location.X += (door_width*scale.Z - door_width)/2 - door_width
                else:
                    location.Z += 180
            if map_doors[e].direction_part in [Direction.TOP_LEFT, Direction.BOTTOM_LEFT]:
                if datatable["PB_DT_RoomMaster"][i]["AreaID"] == "EAreaID::m10BIG":
                    location.X -= 510
                else:
                    location.X -= 370
            if map_doors[e].direction_part in [Direction.TOP_RIGHT, Direction.BOTTOM_RIGHT]:
                if datatable["PB_DT_RoomMaster"][i]["AreaID"] == "EAreaID::m10BIG":
                    location.X += 510
                else:
                    location.X += 370
            lever_index = len(game_data[filename].Exports) + 1
            add_level_actor(filename, "BP_SwitchDoor_C", location, rotation, scale, {"GimmickFlag": FName.FromString(game_data[filename], "None")})
            game_data[filename].Exports[lever_index].Data[2].Value[0].Value = FVector(lever_offset, 360, 0)
            #Remove the magic door in that one galleon room so that it never overlays with anything
            if e == "SIP_002_0_0_RIGHT":
                remove_level_class("m01SIP_002_Gimmick", "BP_MagicDoor_C")

def update_room_containers(room):
    #Don't change the containers for starting items
    if room == "m01SIP_000":
        return
    if room in room_to_gimmick:
        filename = room_to_gimmick[room]
    else:
        filename = room + "_Gimmick"
    room_width = datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260
    for i in range(len(game_data[filename].Exports)):
        old_class_name = str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[i].ClassIndex))) - 1].ObjectName)
        #Check if it is a golden chest
        if old_class_name == "PBEasyTreasureBox_BP_C" and str(game_data[filename].Exports[i].Data[4].Name) == "IsAutoMaterial":
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
            for e in game_data[filename].Exports[i].Data:
                if str(e.Name) in ["DropItemID", "DropRateID"]:
                    drop_id = str(e.Value)
                if str(e.Name) == "IsRandomizerSafetyChest":
                    safety_chest = e.Value
                if str(e.Name) == "OptionalGimmickID":
                    gimmick_id = str(e.Value)
                if str(e.Name) == "RootComponent":
                    root_index = int(str(e.Value)) - 1
                    for o in game_data[filename].Exports[root_index].Data:
                        if str(o.Name) == "RelativeLocation":
                            location = o.Value[0].Value
                        if str(o.Name) == "RelativeRotation":
                            rotation = o.Value[0].Value
                        if str(o.Name) == "RelativeScale3D":
                            scale    = o.Value[0].Value
            if not drop_id in datatable["PB_DT_DropRateMaster"]:
                continue
            if safety_chest:
                continue
            if datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxHPUP":
                new_class_name = "HPMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxMPUP":
                new_class_name = "MPMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] == "MaxBulletUP":
                new_class_name = "BulletMaxUp_C"
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] in key_items:
                new_class_name = "PBEasyTreasureBox_BP_C(Gold)"
            else:
                new_class_name = "PBEasyTreasureBox_BP_C"
            #Check if container mismatches item type
            if old_class_name == new_class_name:
                continue
            #Correct container transform when necessary
            #The upgrades up the castle bridge are on the wrong plane
            if room == "m02VIL_008":
                location.X -= 50
            #If the room is a rotating 3d one then use the forward vector to shift position
            elif room in rotating_rooms:
                forward_vector = (math.cos(math.radians(rotation.Pitch))*math.sin(math.radians(rotation.Yaw))*(-1), math.cos(math.radians(rotation.Pitch))*math.cos(math.radians(rotation.Yaw)))
                if "PBEasyTreasureBox_BP_C" in new_class_name and old_class_name in ["HPMaxUp_C", "MPMaxUp_C", "BulletMaxUp_C"]:
                    location.X -= forward_vector[0]*120
                    location.Y -= forward_vector[1]*120
                if new_class_name in ["HPMaxUp_C", "MPMaxUp_C", "BulletMaxUp_C"] and "PBEasyTreasureBox_BP_C" in old_class_name:
                    location.X += forward_vector[0]*120
                    location.Y += forward_vector[1]*120
            #Otherwise give the container a set transform
            else:
                if "PBEasyTreasureBox_BP_C" in new_class_name and old_class_name in ["HPMaxUp_C", "MPMaxUp_C", "BulletMaxUp_C"]:
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
                    elif drop_id == "Treasurebox_SAN003_5":
                        location.Z = 6600
                    elif drop_id == "Treasurebox_SAN019_3":
                        location.Z = 120
                    elif drop_id == "Treasurebox_SAN021_4":
                        location.Z = 420
                if new_class_name in ["HPMaxUp_C", "MPMaxUp_C", "BulletMaxUp_C"] and "PBEasyTreasureBox_BP_C" in old_class_name:
                    #If it used to be the chest under the bridge move it to Benjamin's room for the extra characters
                    if drop_id == "Treasurebox_JPN002_1":
                        location.X = 1860
                        location.Z = 60
                    location.Y = 0
                    rotation.Yaw = 0
            properties = {}
            if "PBEasyTreasureBox_BP_C" in new_class_name:
                properties["DropItemID"]   = FName.FromString(game_data[filename], drop_id)
                properties["ItemID"]       = FName.FromString(game_data[filename], drop_id)
                properties["TreasureFlag"] = FName.FromString(game_data[filename], "EGameTreasureFlag::" + remove_inst(drop_id))
                if gimmick_id:
                    properties["OptionalGimmickID"] = FName.FromString(game_data[filename], gimmick_id)
            else:
                properties["DropRateID"]   = FName.FromString(game_data[filename], drop_id)
            #Removing chests like any other actor currently causes crashes so instead move the original way offscreen
            #Hopefully this is only temporary
            if "PBEasyTreasureBox_BP_C":
                for e in game_data[filename].Exports[i].Data:
                    if str(e.Name) in ["DropItemID", "ItemID"]:
                        e.Value = FName.FromString(game_data[filename], "AAAA_Shard")
                game_data[filename].Exports[root_index].Data[0].Value[0].Value = FVector(-999, 0, 0)
            else:
                remove_level_actor(filename, i)
            #One of the Journey rooms has a faulty persistent level export in its gimmick file, so add in its bg file instead
            if room == "m20JRN_002":
                filename = "m20JRN_002_BG"
            add_level_actor(filename, new_class_name, location, rotation, scale, properties)

def update_map_connections():
    #The game map requires you to manually input a list of which rooms can be transitioned into from the current room
    #Doing this via the map editor would only add long load times upon saving a map so do it here instead
    #Fill same room field for rooms that are overlayed perfectly
    #Not sure if it serves any actual purpose in-game but it does help for the following adjacent room check
    for i in datatable["PB_DT_RoomMaster"]:
        datatable["PB_DT_RoomMaster"][i]["SameRoom"] = "None"
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            continue
        for e in datatable["PB_DT_RoomMaster"]:
            if datatable["PB_DT_RoomMaster"][e]["OutOfMap"]:
                continue
            if datatable["PB_DT_RoomMaster"][i]["OffsetX"] == datatable["PB_DT_RoomMaster"][e]["OffsetX"] and datatable["PB_DT_RoomMaster"][i]["OffsetZ"] == datatable["PB_DT_RoomMaster"][e]["OffsetZ"] and i != e:
                datatable["PB_DT_RoomMaster"][i]["SameRoom"] = e
                break
    #Fill adjacent room lists
    for i in datatable["PB_DT_RoomMaster"]:
        doors = []
        for e in map_connections[i]:
            if map_connections[i][e]:
                doors.append(map_doors[e])
        datatable["PB_DT_RoomMaster"][i]["DoorFlag"] = convert_door_to_flag(doors, datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"])
        adjacent = []
        for e in map_connections[i]:
            for o in map_connections[i][e]:
                #Transition rooms in Bloodstained come by pair, each belonging to an area
                #Make it so that an area is only connected to its corresponding transition rooms when possible
                #This avoids having the next area name tag show up within the transition
                #With the exception of standalone transitions with no fallbacks as well as the first entrance transition fallback
                if datatable["PB_DT_RoomMaster"][map_doors[o].room]["RoomType"] == "ERoomType::Load" and map_doors[o].room[0:6] != i[0:6] and datatable["PB_DT_RoomMaster"][map_doors[o].room]["SameRoom"] != "None" and map_doors[o].room != "m02VIL_1200" and datatable["PB_DT_RoomMaster"][map_doors[o].room]["SameRoom"] != "m03ENT_1200":
                    continue
                #The first entrance transition room is hardcoded to bring you back to the village regardless of its position on the canvas
                #Ignore that room and don't connect it to anything
                #Meanwhile the village version of that transition is always needed to trigger the curved effect of the following bridge room
                #So ignore any other transitions overlayed on top of it
                if datatable["PB_DT_RoomMaster"][map_doors[o].room]["SameRoom"] == "m02VIL_1200" or map_doors[o].room == "m03ENT_1200":
                    continue
                if not map_doors[o].room in adjacent:
                    adjacent.append(map_doors[o].room)
        datatable["PB_DT_RoomMaster"][i]["AdjacentRoomName"] = adjacent
    #Some rooms need specific setups
    #Connect Vepar room to its overlayed village counterpart
    datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"].append("m02VIL_000")
    #Some tower rooms are overlayed and need to be connected manually as the above script ignores all overlayed rooms
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
    #Fix bad ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"].append("m02VIL_099")
    #Fix good ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"].append("m02VIL_099")
    #Give overlayed rooms the same door flag as their counterparts
    datatable["PB_DT_RoomMaster"]["m01SIP_022"]["DoorFlag"] = datatable["PB_DT_RoomMaster"]["m02VIL_000"]["DoorFlag"]
    datatable["PB_DT_RoomMaster"]["m18ICE_020"]["DoorFlag"] = datatable["PB_DT_RoomMaster"]["m18ICE_019"]["DoorFlag"]

def bathin_left_entrance_fix():
    #If Bathin's intro event triggers when the player entered the room from the left they will be stuck in an endless walk cycle
    #To fix this add a special door to warp the player in the room's player start instead
    for i in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = map_doors[i].room
        area_path = "ACT" + room[1:3] + "_" + room[3:6]
        new_file = UAsset(asset_dir + "\\" + file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version(517))
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
        new_file.Exports[2].Data[0].Value[0].Value  = FVector(1260*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"], 0, 720*map_doors[i].z_block + 360)
        new_file.Exports[2].Data[1].Value[0].Value  = FRotator(0, 0, 0)
        new_file.Exports[8].Data[0].Value = FName.FromString(new_file, room[3:])
        new_file.Exports[8].Data[1].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[2].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[3].Value = FName.FromString(new_file, "m13ARC_005")
        new_file.Write(mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")
    #Get Bathin's adjacent room while prioritizing the same area
    for i in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = map_doors[i].room
        adjacent_room = room
        if datatable["PB_DT_RoomMaster"][room]["AreaID"] == datatable["PB_DT_RoomMaster"]["m13ARC_005"]["AreaID"]:
            break
    #Also add one more door in the boss room to have a proper transition
    room = "m13ARC_005"
    area_path = "ACT" + room[1:3] + "_" + room[3:6]
    new_file = UAsset(asset_dir + "\\" + file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version(517))
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
    new_file.Write(mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")

def remove_vanilla_rando():
    for i in [293, 294]:
        new_list = []
        count = 0
        for e in game_data["TitleExtraMenu"].Exports[i].Data[0].Value:
            if count != 2:
                new_list.append(e)
            count += 1
        game_data["TitleExtraMenu"].Exports[i].Data[0].Value = new_list
    stringtable["PBSystemStringTable"]["SYS_SEN_ModeRogueDungeon"] = "DELETED"
    stringtable["PBSystemStringTable"]["SYS_MSG_OpenRogueDungeonMode"] = "Story Mode completed."

def show_mod_stats(seed, mod_version):
    game_version = str(game_data["VersionNumber"].Exports[6].Data[0].CultureInvariantString)
    mod_stats = "Bloodstained " + game_version + "\r\nTrue Randomization v" + mod_version
    height = 0.4
    if seed:
        mod_stats += "\r\nSeed # " + seed
        height = 0.66
    for i in range(2):
        game_data["VersionNumber"].Exports[4 + i].Data[0].Value[2].Value[0].X = 19
        game_data["VersionNumber"].Exports[4 + i].Data[0].Value[2].Value[0].Y = height
        game_data["VersionNumber"].Exports[6 + i].Data[0].CultureInvariantString = FString(mod_stats)
        game_data["VersionNumber"].Exports[6 + i].Data[1].Value[2].Value = 16
        game_data["VersionNumber"].Exports[6 + i].Data[2].EnumValue = FName(game_data["VersionNumber"], "ETextJustify::Left")
        struct = struct = FloatPropertyData(FName(game_data["VersionNumber"], "LineHeightPercentage"))
        struct.Value = 0.6
        game_data["VersionNumber"].Exports[6 + i].Data.Add(struct)

def remove_difficulties(current):
    #Ensure that in game difficulty never mismatches the mod's
    new_list = []
    sub_struct = BytePropertyData()
    sub_struct.ByteType = BytePropertyType.FName
    sub_struct.EnumValue = FName(game_data["DifficultSelecter"], "EPBGameLevel::" + current)
    new_list = [sub_struct]
    game_data["DifficultSelecter"].Exports[2].Data[1].Value = new_list

def default_nightmare_cheatcode():
    #Set the nightmare cheatcode as the default name entry in case the user hasn't unlocked the higher difficulties yet
    game_data["EntryNameSetter"].Exports[110].Data[0].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[110].Data[1].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[111].Data[2].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[111].Data[3].CultureInvariantString = FString("NIGHTMARE")

def write_log(filename, log):
    with open("SpoilerLog\\" + filename + ".json", "w", encoding="utf8") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def write_files():
    #Dump all uasset objects to files
    for i in game_data:
        if file_to_type[i] == "Level":
            extension = ".umap"
        else:
            extension = ".uasset"
        game_data[i].Write(mod_dir + "\\" + file_to_path[i] + "\\" + i.split("(")[0] + extension)

def remove_unchanged():
    #Since uasset objects cannot be compared successfully we need to compare the files after they've been written
    #That way unchanged files get removed from the pak
    for i in file_to_path:
        remove = True
        for e in os.listdir(mod_dir + "\\" + file_to_path[i]):
            name, extension = os.path.splitext(e)
            if name == i:
                if not filecmp.cmp(mod_dir + "\\" + file_to_path[i] + "\\" + e, asset_dir + "\\" + file_to_path[i] + "\\" + e, shallow=False):
                    remove = False
        if remove:
            for e in os.listdir(mod_dir + "\\" + file_to_path[i]):
                name, extension = os.path.splitext(e)
                if name == i:
                    os.remove(mod_dir + "\\" + file_to_path[i] + "\\" + e)

def import_texture(filename):
    #Convert DDS to game assets dynamically instead of cooking them within Unreal Editor
    absolute_asset_dir   = os.path.abspath(asset_dir + "\\" + file_to_path[filename])
    absolute_texture_dir = os.path.abspath("Data\\Texture")
    absolute_mod_dir     = os.path.abspath(mod_dir + "\\" + file_to_path[filename])
    
    root = os.getcwd()
    os.chdir("Tools\\UE4 DDS Tools")
    os.system("cmd /c python\python.exe src\main.py \"" + absolute_asset_dir  + "\\" + filename + ".uasset\" \"" + absolute_texture_dir + "\\" + filename + ".dds\" --save_folder=\"" + absolute_mod_dir + "\" --mode=inject --version=4.22")
    os.chdir(root)
    
    #UE4 DDS Tools does not interrupt the program if a texture fails to convert so do it from here
    if not os.path.isfile(absolute_mod_dir + "\\" + filename + ".uasset"):
        raise FileNotFoundError(filename + ".dds failed to inject")

def import_music(filename):
    #Start by coppying all secondary music files to destination
    for i in os.listdir(asset_dir + "\\" + file_to_path[filename]):
        name, extension = os.path.splitext(i)
        if extension == ".awb":
            continue
        if name == filename:
            shutil.copyfile(asset_dir + "\\" + file_to_path[filename] + "\\" + i, mod_dir + "\\" + file_to_path[filename] + "\\" + i)
    #Append the HCA data to the AWB's header
    with open(asset_dir + "\\" + file_to_path[filename] + "\\" + filename + ".awb", "rb") as inputfile, open(mod_dir + "\\" + file_to_path[filename] + "\\" + filename + ".awb", "wb") as outfile:
        offset = inputfile.read().find(str.encode("HCA"))
        inputfile.seek(0)
        outfile.write(inputfile.read(offset))
        with open("Data\\Music\\" + filename + ".hca", "rb") as hca:
            outfile.write(hca.read())

def export_name_to_index(filename, export_name):
    count = 0
    for i in game_data[filename].Exports:
        if str(i.ObjectName) == export_name:
            return count
        count += 1
    raise "Export not found"

def add_level_actor(filename, actor_class, location, rotation, scale, properties):
    actor_index = len(game_data[filename].Exports)
    #Name the new actor based on the class
    short_class = actor_class.replace(")", "").split("(")[0]
    short_class = short_class.split("_")
    if short_class[-1] == "C":
        short_class.pop()
    short_class = "_".join(short_class)
    actor_name = custom_actor_prefix + short_class + "_" + str(actor_index + 1)
    snippet = UAssetSnippet(game_data[actor_to_properties[actor_class]["Room"] + "_Gimmick"], actor_to_properties[actor_class]["Index"])
    snippet.AddToUAsset(game_data[filename], actor_name)
    #Change class parameters
    for i in game_data[filename].Exports[actor_index].Data:
        if str(i.Name) in properties:
            if str(i.PropertyType) == "ByteProperty":
                i.EnumValue = properties[str(i.Name)]
            else:
                i.Value = properties[str(i.Name)]
            del properties[str(i.Name)]
        if str(i.Name) == "ActorLabel":
            i.Value = FString(remove_inst(actor_name))
        if str(i.Name) == "RootComponent":
            root_index = int(str(i.Value)) - 1
            game_data[filename].Exports[root_index].Data.Clear()
            if location.X != 0 or location.Y != 0 or location.Z != 0:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeLocation"), FName.FromString(game_data[filename], "Vector"))
                sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "RelativeLocation"))
                sub_struct.Value = location
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
            if rotation.Pitch != 0 or rotation.Yaw != 0 or rotation.Roll != 0:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeRotation"), FName.FromString(game_data[filename], "Rotator"))
                sub_struct = RotatorPropertyData(FName.FromString(game_data[filename], "RelativeRotation"))
                sub_struct.Value = rotation
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
            if scale.X != 1 or scale.Y != 1 or scale.Z != 1:
                struct = StructPropertyData(FName.FromString(game_data[filename], "RelativeScale3D"), FName.FromString(game_data[filename], "Vector"))
                sub_struct = VectorPropertyData(FName.FromString(game_data[filename], "RelativeScale3D"))
                sub_struct.Value = scale
                struct.Value.Add(sub_struct)
                game_data[filename].Exports[root_index].Data.Add(struct)
    #Add parameters that are missing
    for i in properties:
        if type(properties[i]) is bool:
            struct = BoolPropertyData(FName.FromString(game_data[filename], i))
            struct.Value = properties[i]
        elif "::" in str(properties[i]):
            struct = BytePropertyData(FName.FromString(game_data[filename], i))
            struct.ByteType = BytePropertyType.FName
            struct.EnumType = FName.FromString(game_data[filename], str(properties[i]).split("::")[0])
            struct.EnumValue = properties[i]
        else:
            struct = NamePropertyData(FName.FromString(game_data[filename], i))
            struct.Value = properties[i]
        game_data[filename].Exports[actor_index].Data.Add(struct)

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

def remove_level_actor(filename, index):
    #Remove actor at index
    if file_to_type[filename] != "Level":
        raise "Input is not a level file"
    level_index = export_name_to_index(filename, "PersistentLevel")
    game_data[filename].Exports[index].OuterIndex = FPackageIndex(0)
    game_data[filename].Exports[level_index].IndexData.Remove(index + 1)

def remove_level_class(filename, name):
    #Remove all actors of class
    if file_to_type[filename] != "Level":
        raise "Input is not a level file"
    level_index = export_name_to_index(filename, "PersistentLevel")
    for i in range(len(game_data[filename].Exports)):
        class_name = str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[i].ClassIndex))) - 1].ObjectName)
        if class_name == name:
            game_data[filename].Exports[i].OuterIndex = FPackageIndex(0)
            game_data[filename].Exports[level_index].IndexData.Remove(i + 1)

def change_material_hsv(filename, parameter, new_hsv):
    #Change a vector color in a material file
    #Here we use hsv as a base as it is easier to work with
    if file_to_type[filename] != "Material":
        raise "Input is not a material file"
    #Some color properties are not parsed by UAssetAPI and end up in extra data
    #Hex edit in that case
    if filename in material_to_offset:
        for i in material_to_offset[filename]:
            #Check if given offset is valid
            string = ""
            for e in range(12):
                string += "{:02x}".format(game_data[filename].Exports[0].Extras[i + e]).upper()
            if string != "0000000000000002FFFFFFFF":
                raise "Material offset invalid"
            #Get rgb
            rgb = []
            for e in range(3):
                list = []
                for o in range(4):
                    list.insert(0, "{:02x}".format(game_data[filename].Exports[0].Extras[i + 12 + e*4 + o]).upper())
                string = ""
                for o in list:
                    string += o
                rgb.append(struct.unpack("!f", bytes.fromhex(string))[0])
            #Convert
            hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            if new_hsv[0] < 0:
                new_hue = hsv[0]
            else:
                new_hue = new_hsv[0]/360
            if new_hsv[1] < 0:
                new_sat = hsv[1]
            else:
                new_sat = new_hsv[1]/100
            if new_hsv[2] < 0:
                new_val = hsv[2]
            else:
                new_val = new_hsv[2]/100
            rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
            #Write rgb
            for e in range(3):
                string = "{:08x}".format(struct.unpack("<I", struct.pack("<f", rgb[e]))[0]).upper()
                list = []
                for o in range(0, len(string), 2):
                    list.insert(0, string[o] + string[o + 1])
                for o in range(4):
                    game_data[filename].Exports[0].Extras[i + 12 + e*4 + o] = int(list[o], 16)
    #Otherwise change color through the exports
    else:
        for i in game_data[filename].Exports[0].Data:
            if str(i.Name) == "VectorParameterValues":
                for e in i.Value:
                    if str(e.Value[0].Value[0].Value) == parameter:
                        rgb = []
                        rgb.append(e.Value[1].Value[0].Value.R)
                        rgb.append(e.Value[1].Value[0].Value.G)
                        rgb.append(e.Value[1].Value[0].Value.B)
                        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                        if new_hsv[0] < 0:
                            new_hue = hsv[0]
                        else:
                            new_hue = new_hsv[0]/360
                        if new_hsv[1] < 0:
                            new_sat = hsv[1]
                        else:
                            new_sat = new_hsv[1]/100
                        if new_hsv[2] < 0:
                            new_val = hsv[2]
                        else:
                            new_val = new_hsv[2]/100
                        rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
                        e.Value[1].Value[0].Value.R = rgb[0]
                        e.Value[1].Value[0].Value.G = rgb[1]
                        e.Value[1].Value[0].Value.B = rgb[2]

def convert_flag_to_door(room_name, door_flag, room_width):
    #Function by LagoLunatic
    door_list = []
    for i in range(0, len(door_flag), 2):
        tile_index = door_flag[i]
        direction = door_flag[i+1]
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

def convert_door_to_adjacent_room(door):
    #Return a door's adjacent rooms, including the room that it belongs to
    if door in datatable["PB_DT_RoomMaster"]:
        return [door]
    adjacent = [map_doors[door].room]
    for i in map_connections[map_doors[door].room][door]:
        adjacent.append(map_doors[i].room)
    return adjacent

def is_adjacent(room_1, room_2):
    if left_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP)
    elif bottom_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_horizontal_check(room_1, room_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT)
    elif right_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP)
    elif top_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_horizontal_check(room_1, room_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT)

def left_check(room_1, room_2):
    return bool(room_2["OffsetX"] == round(room_1["OffsetX"] - 12.6 * room_2["AreaWidthSize"], 1) and round(room_1["OffsetZ"] - 7.2 * (room_2["AreaHeightSize"] - 1), 1) <= room_2["OffsetZ"] <= round(room_1["OffsetZ"] + 7.2 * (room_1["AreaHeightSize"] - 1), 1))

def bottom_check(room_1, room_2):
    return bool(round(room_1["OffsetX"] - 12.6 * (room_2["AreaWidthSize"] - 1), 1) <= room_2["OffsetX"] <= round(room_1["OffsetX"] + 12.6 * (room_1["AreaWidthSize"] - 1), 1) and room_2["OffsetZ"] == round(room_1["OffsetZ"] - 7.2 * room_2["AreaHeightSize"], 1))

def right_check(room_1, room_2):
    return bool(room_2["OffsetX"] == round(room_1["OffsetX"] + 12.6 * room_1["AreaWidthSize"], 1) and round(room_1["OffsetZ"] - 7.2 * (room_2["AreaHeightSize"] - 1), 1) <= room_2["OffsetZ"] <= round(room_1["OffsetZ"] + 7.2 * (room_1["AreaHeightSize"] - 1), 1))

def top_check(room_1, room_2):
    return bool(round(room_1["OffsetX"] - 12.6 * (room_2["AreaWidthSize"] - 1), 1) <= room_2["OffsetX"] <= round(room_1["OffsetX"] + 12.6 * (room_1["AreaWidthSize"] - 1), 1) and room_2["OffsetZ"] == round(room_1["OffsetZ"] + 7.2 * room_1["AreaHeightSize"], 1))

def door_vertical_check(room_1, room_2, direction_1, direction_2, direction_3):
    for i in map_connections[room_1]:
        if map_doors[i].direction_part == direction_1:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_1] and map_doors[i].z_block == (map_doors[e].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][i].append(e)
        elif map_doors[i].direction_part == direction_2:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_2] and map_doors[i].z_block == (map_doors[e].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][i].append(e)
        elif map_doors[i].direction_part == direction_3:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_3] and map_doors[i].z_block == (map_doors[e].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][i].append(e)

def door_horizontal_check(room_1, room_2, direction_1, direction_2, direction_3):
    for i in map_connections[room_1]:
        if map_doors[i].direction_part == direction_1:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_1] and map_doors[i].x_block == (map_doors[e].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][i].append(e)
        elif map_doors[i].direction_part == direction_2:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_2] and map_doors[i].x_block == (map_doors[e].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][i].append(e)
        elif map_doors[i].direction_part == direction_3:
            for e in map_connections[room_2]:
                if map_doors[e].direction_part == OppositeDirection[direction_3] and map_doors[i].x_block == (map_doors[e].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][i].append(e)

def remove_inst(name):
    #Return a string without its instance number the same way Unreal does it
    name = name.split("_")
    if name[-1][0] != "0":
        try:
            int(name[-1])
            name.pop()
        except ValueError:
            pass
    return "_".join(name)

def is_enemy(character):
    #Check if input entry is an enemy and what type
    dict = {
        "Enemy":     False,
        "Boss":      False,
        "Main":      False,
        "Exception": False
    }
    if character in mod_data["EnemyLocation"]:
        dict["Enemy"] = True
        dict["Main"]  = True
    elif character[0:5] in mod_data["EnemyLocation"] and character != "N1001_Sip":
        dict["Enemy"] = True
    elif character[0:5] in ["N1009", "N1013"] or character == "N3125":
        dict["Enemy"]     = True
        dict["Exception"] = True
    if character in datatable["PB_DT_CharacterParameterMaster"]:
        if datatable["PB_DT_CharacterParameterMaster"][character]["IsBoss"] and character != "N2008_BOSS" or character[0:5] in ["N3106", "N3107", "N3108"]:
            dict["Boss"] = True
    return dict

def create_weighted_list(value, minimum, maximum, step, deviation):
    #Create a list in a range with higher odds around a specific value
    list = []
    for i in [(minimum, value + 1), (value, maximum + 1)]:
        sublist = []
        distance = abs(i[0]-i[1])
        new_deviation = round(deviation*(distance/(maximum-minimum)))*2
        for e in range(i[0], i[1]):
            if e % step == 0:
                difference = abs(e-value)
                for o in range(2**(abs(math.ceil(difference*new_deviation/distance)-new_deviation))):
                    sublist.append(e)
        list.append(sublist)
    return list

def random_weighted(value, minimum, maximum, step, deviation):
    return random.choice(random.choice(create_weighted_list(value, minimum, maximum, step, deviation)))

def add_enemy_to_archive(enemy_id, area_ids, package_path, copy_from):
    last_id = int(list(datatable["PB_DT_ArchiveEnemyMaster"])[-1].split("_")[-1])
    entry_id = "Enemy_" + "{:03d}".format(last_id + 1)
    for i in datatable["PB_DT_ArchiveEnemyMaster"]:
        if datatable["PB_DT_ArchiveEnemyMaster"][i]["UniqueID"] == copy_from:
            new_entry = copy.deepcopy(datatable["PB_DT_ArchiveEnemyMaster"][i])
            break
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id] = new_entry
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["UniqueID"] = enemy_id
    for i in range(len(area_ids)):
        datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["Area" + str(i + 1)] = area_ids[i]
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["AreaInputPath"] = package_path

def append_string_entry(file, entry, text):
    #Make sure the text never exceeds two lines
    if "\r\n" in stringtable[file][entry] or len(stringtable[file][entry]) > 60 or entry == "ITEM_EXPLAIN_RolledOmelette":
        prefix = " "
    else:
        prefix = "\r\n"
    stringtable[file][entry] += prefix + text