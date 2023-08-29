import os
import clr
import json
import math
import random
import struct
import sys
import colorsys
import copy
import filecmp
from enum import Enum
from collections import OrderedDict

class FileType(Enum):
    DataTable   = 0
    StringTable = 1
    Blueprint   = 2
    Level       = 3
    Material    = 4
    Texture     = 5
    Sound       = 6

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

def simplify_item_name(name):
    return name.replace("Familiar:", "").replace(" ", "").replace("'", "").replace("-", "").replace(".", "").replace("é", "e").replace("è", "e").replace("&", "and").lower()

#Open file information
with open("Data\\FileToPath.json", "r", encoding="utf8") as file_reader:
    file_to_path = json.load(file_reader)
translation = {}
for file in os.listdir("Data\\Translation"):
    name, extension = os.path.splitext(file)
    with open("Data\\Translation\\" + file, "r", encoding="utf8") as file_reader:
        translation[name] = json.load(file_reader)
start_item_translation = {}
for string in ["Item", "Shard"]:
    for entry in translation[string]:
        start_item_translation[simplify_item_name(translation[string][entry])] = entry

#Gather other information
file_to_type = {}
for file in file_to_path:
    if "DataTable" in file_to_path[file]:
        file_to_type[file] = FileType.DataTable
    elif "StringTable" in file_to_path[file]:
        file_to_type[file] = FileType.StringTable
    elif "Level" in file_to_path[file]:
        file_to_type[file] = FileType.Level
    elif "Material" in file_to_path[file]:
        file_to_type[file] = FileType.Material
    elif "Texture" in file_to_path[file] or "UI" in file_to_path[file] and not "StartupSelecter" in file_to_path[file] and not "Title" in file_to_path[file]:
        file_to_type[file] = FileType.Texture
    elif "Sound" in file_to_path[file]:
        file_to_type[file] = FileType.Sound
    else:
        file_to_type[file] = FileType.Blueprint
load_types = [FileType.DataTable, FileType.Level, FileType.StringTable, FileType.Blueprint, FileType.Material, FileType.Sound]
simplify_types = [FileType.DataTable, FileType.StringTable]

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

#test = UAsset("PB_DT_DropRateMaster.uasset", UE4Version.VER_UE4_22)
#test.AddNameReference(FString("FloatProperty"))
#test.Write("PB_DT_DropRateMaster2.uasset")

def init():
    global classic_item_to_properties
    classic_item_to_properties = {
        "BP_PBC_ItemCommonMoneyMedium_C": {
            "Level": "Stage_00",
            "Index": [0, 9]
        },
        "BP_PBC_ItemCommonMoneySmall_C": {
            "Level": "Stage_00",
            "Index": [1, 10]
        },
        "BP_PBC_ItemCommonMPLarge_C": {
            "Level": "Stage_00",
            "Index": [2, 11]
        },
        "BP_PBC_ItemCommonMPSmall_C": {
            "Level": "Stage_00",
            "Index": [3, 12]
        },
        "BP_PBC_ItemCommonWeaponDagger_C": {
            "Level": "Stage_00",
            "Index": [4, 13]
        },
        "BP_PBC_ItemCommonMagicKillAll_C": {
            "Level": "Stage_01",
            "Index": [0, 28]
        },
        "BP_PBC_ItemCommonMoneyLarge_C": {
            "Level": "Stage_01",
            "Index": [1, 29]
        },
        "BP_PBC_ItemCommonPotionInvisible_C": {
            "Level": "Stage_01",
            "Index": [5, 33]
        },
        "BP_PBC_ItemCommonWeaponBoneArc_C": {
            "Level": "Stage_01",
            "Index": [6, 34]
        },
        "BP_PBC_ItemCommonWeaponRuinousRood_C": {
            "Level": "Stage_01",
            "Index": [8, 36]
        },
        "BP_PBC_ItemCommonWeaponUnholyFire_C": {
            "Level": "Stage_01",
            "Index": [9, 37]
        },
        "BP_PBC_ItemCommonMagicTimeShard_C": {
            "Level": "Stage_02",
            "Index": [9, 37]
        },
        "BP_PBC_ItemSecretCrown_C": {
            "Level": "Stage_02",
            "Index": [14, 46]
        },
        "BP_PBC_ItemSecretGoblet_C": {
            "Level": "Stage_03",
            "Index": [10, 39]
        },
        "BP_PBC_ItemSpecialExtraLife_C": {
            "Level": "Stage_03",
            "Index": [11, 40]
        },
        "BP_PBC_ItemTreasureChest_C": {
            "Level": "Stage_04",
            "Index": [11, 41]
        },
        "BP_PBC_ItemSecretLuckyCat_C": {
            "Level": "Stage_5A",
            "Index": [10, 43]
        },
        "BP_PBC_ItemSpecialFood_C": {
            "Level": "Stage_5B",
            "Index": [9, 33]
        }
    }
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
    global global_room_pickups
    global_room_pickups = []
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
    global string_entry_exceptions
    string_entry_exceptions = [
        "ITEM_EXPLAIN_RolledOmelette",
        "ITEM_EXPLAIN_DiamondBullets"
    ]
    global datatable_entry_index
    datatable_entry_index = {}
    global wheight_exponents
    wheight_exponents = [3, 1.8, 1.25]

def load_game_data():
    global game_data
    game_data = {}
    global data_struct
    data_struct = {}
    for file in file_to_type:
        if file_to_type[file] in load_types:
            #Load all game data in one dict
            if file_to_type[file] == FileType.Level:
                extension = ".umap"
            else:
                extension = ".uasset"
            game_data[file] = UAsset(asset_dir + "\\" + file_to_path[file] + "\\" + file.split("(")[0] + extension, UE4Version.VER_UE4_22)
            #Store struct data types for later on
            if file_to_type[file] == FileType.DataTable:
                for entry in game_data[file].Exports[0].Table.Data:
                    for data in entry.Value:
                        if str(data.PropertyType) == "ArrayProperty":
                            if str(data.ArrayType) == "StructProperty":
                                for struct in data.Value:
                                    data_struct[str(struct.Name)] = struct
    
def load_mod_data():
    global mod_data
    mod_data = {}
    for file in os.listdir("Data\\Constant"):
        name, extension = os.path.splitext(file)
        with open("Data\\Constant\\" + file, "r", encoding="utf8") as file_reader:
            mod_data[name] = json.load(file_reader)

def load_map(path):
    #Load map related files
    if not path:
        path = "MapEdit\\Data\\PB_DT_RoomMaster.json"
    with open(path, "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    if "PB_DT_RoomMaster" in datatable:
        for room in json_file["MapData"]:
            if not room in datatable["PB_DT_RoomMaster"]:
                area_save_room = json_file["MapData"][room]["AreaID"].split("::")[-1] + "_1000"
                datatable["PB_DT_RoomMaster"][room] = copy.deepcopy(datatable["PB_DT_RoomMaster"][area_save_room])
                datatable["PB_DT_RoomMaster"][room]["LevelName"] = room
                add_room_file(room)
            for data in json_file["MapData"][room]:
                datatable["PB_DT_RoomMaster"][room][data] = json_file["MapData"][room][data]
    else:
        datatable["PB_DT_RoomMaster"] = json_file["MapData"]
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
    #Rooms with no traverse blocks only display properly based on their Y position below the origin
    #Shift those lists if the rooms are below 0
    for room in ["m08TWR_017", "m08TWR_018", "m08TWR_019", "m11UGD_013", "m11UGD_031"]:
        if datatable["PB_DT_RoomMaster"][room]["OffsetZ"] < 0:
            multiplier = abs(int(datatable["PB_DT_RoomMaster"][room]["OffsetZ"]/7.2)) - 1
            if multiplier > datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"] - 1:
                multiplier = datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"] - 1
            for index in range(len(datatable["PB_DT_RoomMaster"][room]["NoTraverse"])):
                datatable["PB_DT_RoomMaster"][room]["NoTraverse"][index] -= datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*multiplier

def get_map_info():
    #Keep track of every door connection for multi purpose
    for room in datatable["PB_DT_RoomMaster"]:
        map_connections[room] = {}
        doors = convert_flag_to_door(room, datatable["PB_DT_RoomMaster"][room]["DoorFlag"], datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"])
        for door in doors:
            door_string = "_".join([door.room[3:], str(door.x_block), str(door.z_block), door.direction_part.name])
            map_doors[door_string] = door
            map_connections[room][door_string] = []
    for room_1 in datatable["PB_DT_RoomMaster"]:
        for room_2 in datatable["PB_DT_RoomMaster"]:
            if datatable["PB_DT_RoomMaster"][room_1]["OutOfMap"] != datatable["PB_DT_RoomMaster"][room_2]["OutOfMap"]:
                continue
            is_room_adjacent(room_1, room_2)

def set_randomizer_events():
    #Some events need to be triggered by default to avoid conflicts or tedium
    #First ship door
    remove_level_class("m01SIP_000_Gimmick", "BP_EventDoor_C")
    #Librarian easter egg
    datatable["PB_DT_GimmickFlagMaster"]["LIB_009_PushUpOD_Second"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["LIB_009_PushUpOD_First"]["Id"]
    #Tower cutscene/garden red moon removal
    datatable["PB_DT_EventFlagMaster"]["Event_07_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
    datatable["PB_DT_EventFlagMaster"]["Event_19_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
    #Temporary Craftwork softlock workaround
    datatable["PB_DT_DropRateMaster"]["Safe_Demoniccapture"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Tresurebox_SAN000_01"])
    datatable["PB_DT_DropRateMaster"]["Safe_Demoniccapture"]["RareItemId"]       = "Demoniccapture"
    datatable["PB_DT_DropRateMaster"]["Safe_Demoniccapture"]["RareItemQuantity"] = 1
    datatable["PB_DT_DropRateMaster"]["Safe_Demoniccapture"]["RareItemRate"]     = 100.0
    add_global_room_pickup("m05SAN_012", "Safe_Demoniccapture")

def remove_fire_shard_requirement():
    #Break galleon cannon wall
    datatable["PB_DT_GimmickFlagMaster"]["SIP_008_BreakWallCannon"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]

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

def table_complex_to_simple():
    #The uasset data is inconvenient to access and would take up too much text space in the code
    #Convert them to a simplified dictionary that is similar to the old serializer's outputs
    for file in file_to_type:
        if file_to_type[file] in simplify_types:
            if file_to_type[file] == FileType.DataTable:
                datatable[file] = {}
                for entry in game_data[file].Exports[0].Table.Data:
                    datatable[file][str(entry.Name)] = {}
                    for data in entry.Value:
                        datatable[file][str(entry.Name)][str(data.Name)] = read_datatable_value(data)
                original_datatable[file] = copy.deepcopy(datatable[file])
                datatable_entry_index[file] = {}
            elif file_to_type[file] == FileType.StringTable:
                stringtable[file] = {}
                for entry in game_data[file].Exports[0].Table:
                    stringtable[file][str(entry.Key)] = str(entry.Value)

def table_simple_to_complex():
    #Convert the simplified datatables back to their complex versions
    for file in file_to_type:
        if file_to_type[file] in simplify_types:
            if file_to_type[file] == FileType.DataTable:
                entry_count = 0
                for entry in datatable[file]:
                    #If the datatables had entries added then add an entry slot in the uasset too
                    if entry_count >= game_data[file].Exports[0].Table.Data.Count:
                        append_datatable_entry(file, entry)
                    data_count = 0
                    for data in datatable[file][entry]:
                        #Only patch the value if it is different from the original, saves a lot of load time
                        if entry in original_datatable[file]:
                            if datatable[file][entry][data] == original_datatable[file][entry][data]:
                                data_count += 1
                                continue
                        patch_datatable_value(file, entry_count, data_count, datatable[file][entry][data])
                        data_count += 1
                    entry_count += 1
            elif file_to_type[file] == FileType.StringTable:
                game_data[file].Exports[0].Table.Clear()
                for entry in stringtable[file]:
                    game_data[file].Exports[0].Table.Add(FString(entry), FString(stringtable[file][entry]))

def read_datatable_value(struct):
    #Read a uasset variable as a python variable
    struct_type = str(struct.PropertyType)
    if struct_type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        value = []
        for element in struct.Value:
            if sub_type == "ByteProperty":
                sub_value = str(element.EnumValue)
            elif sub_type == "FloatProperty":
                sub_value = round(element.Value, 3)
            elif sub_type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
                sub_value = str(element.Value)
            elif sub_type == "StrProperty":
                if element.Value:
                    sub_value = str(element.Value)
                else:
                    sub_value = ""
            elif sub_type == "StructProperty":
                sub_value = {}
                for sub_element in element.Value:
                    sub_sub_type = str(sub_element.PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_sub_value = str(sub_element.EnumValue)
                    elif sub_sub_type == "FloatProperty":
                        sub_sub_value = round(sub_element.Value, 3)
                    elif sub_sub_type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
                        sub_sub_value = str(sub_element.Value)
                    elif sub_sub_type == "StrProperty":
                        if sub_element.Value:
                            sub_sub_value = str(sub_element.Value)
                        else:
                            sub_sub_value = ""
                    elif sub_sub_type == "TextProperty":
                        if sub_element.CultureInvariantString:
                            sub_sub_value = str(sub_element.CultureInvariantString)
                        else:
                            sub_sub_value = ""
                    else:
                        sub_sub_value = sub_element.Value
                    sub_value[str(sub_element.Name)] = sub_sub_value
            elif sub_type == "TextProperty":
                if element.CultureInvariantString:
                    sub_value = str(element.CultureInvariantString)
                else:
                    sub_value = ""
            else:
                sub_value = element.Value
            value.append(sub_value)
    elif struct_type == "ByteProperty":
        value = str(struct.EnumValue)
    elif struct_type == "FloatProperty":
        value = round(struct.Value, 3)
    elif struct_type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
        value = str(struct.Value)
    elif struct_type == "StrProperty":
        if struct.Value:
            value = str(struct.Value)
        else:
            value = ""
    elif struct_type == "TextProperty":
        if struct.CultureInvariantString:
            value = str(struct.CultureInvariantString)
        else:
            value = ""
    else:
        value = struct.Value
    return value

def patch_datatable_value(file, entry, data, value):
    #Patch a python variable over a uasset's variable
    struct = game_data[file].Exports[0].Table.Data[entry].Value[data]
    struct_type = str(struct.PropertyType)
    if struct_type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        new_list = []
        for element in value:
            if sub_type == "BoolProperty":
                sub_struct = BoolPropertyData()
                sub_struct.Value = element
            elif sub_type == "ByteProperty":
                sub_struct = BytePropertyData()
                sub_struct.ByteType = BytePropertyType.FName
                sub_struct.EnumValue = FName.FromString(game_data[file], element)
            elif sub_type == "EnumProperty":
                sub_struct = EnumPropertyData()
                sub_struct.Value = FName.FromString(game_data[file], element)
            elif sub_type == "FloatProperty":
                sub_struct = FloatPropertyData()
                sub_struct.Value = element
            elif sub_type == "IntProperty":
                sub_struct = IntPropertyData()
                sub_struct.Value = element
            elif sub_type == "NameProperty":
                sub_struct = NamePropertyData()
                sub_struct.Value = FName.FromString(game_data[file], element)
            elif sub_type == "SoftObjectProperty":
                sub_struct = SoftObjectPropertyData()
                sub_struct.Value = FName.FromString(game_data[file], element)
            elif sub_type == "StrProperty":
                sub_struct = StrPropertyData()
                if element:
                    sub_struct.Value = FString(element)
                else:
                    sub_struct.Value = None
            elif sub_type == "StructProperty":
                sub_struct = data_struct[str(struct.Name)].Clone()
                count = 0
                for sub_element in element:
                    sub_sub_type = str(sub_struct.Value[count].PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_struct.Value[count].EnumValue = FName.FromString(game_data[file], element[sub_element])
                    elif sub_sub_type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
                        sub_struct.Value[count].Value = FName.FromString(game_data[file], element[sub_element])
                    elif sub_sub_type == "StrProperty":
                        if element[sub_element]:
                            sub_struct.Value[count].Value = FString(element[sub_element])
                        else:
                            sub_struct.Value[count].Value = None
                    elif sub_sub_type == "TextProperty":
                        if element[sub_element]:
                            sub_struct.Value[count].CultureInvariantString = FString(element[sub_element])
                        else:
                            sub_struct.Value[count].CultureInvariantString = None
                    else:
                        sub_struct.Value[count].Value = element[sub_element]
                    count += 1
            elif sub_type == "TextProperty":
                sub_struct = TextPropertyData()
                if element:
                    sub_struct.CultureInvariantString = FString(element)
                else:
                    sub_struct.CultureInvariantString = None
            new_list.append(sub_struct)
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = new_list
    elif struct_type == "ByteProperty":
        game_data[file].Exports[0].Table.Data[entry].Value[data].EnumValue = FName.FromString(game_data[file], value)
    elif struct_type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FName.FromString(game_data[file], value)
    elif struct_type == "StrProperty":
        if value:
            game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FString(value)
        else:
            game_data[file].Exports[0].Table.Data[entry].Value[data].Value = None
    elif struct_type == "TextProperty":
        if value:
            game_data[file].Exports[0].Table.Data[entry].Value[data].CultureInvariantString = FString(value)
        else:
            game_data[file].Exports[0].Table.Data[entry].Value[data].CultureInvariantString = None
    else:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = value

def append_datatable_entry(file, entry):
    #Append a new datatable entry to the end to be edited later on
    new_entry = game_data[file].Exports[0].Table.Data[0].Clone()
    new_entry.Name = FName.FromString(game_data[file], entry)
    game_data[file].Exports[0].Table.Data.Add(new_entry)

def update_datatable_order():
    #Shift some datatable entry placements when necessary
    for file in datatable_entry_index:
        for entry_1 in datatable_entry_index[file]:
            old_index = list(datatable[file]).index(entry_1)
            new_index = datatable_entry_index[file][entry_1]
            current_entry = game_data[file].Exports[0].Table.Data[old_index].Clone()
            game_data[file].Exports[0].Table.Data.Remove(game_data[file].Exports[0].Table.Data[old_index])
            game_data[file].Exports[0].Table.Data.Insert(new_index, current_entry)
            #Update the other entry indexes for that same datatable
            for entry_2 in datatable_entry_index[file]:
                if new_index < old_index:
                    if new_index <= datatable_entry_index[file][entry_2] < old_index:
                        datatable_entry_index[file][entry_2] += 1
                elif new_index > old_index:
                    if new_index >= datatable_entry_index[file][entry_2] > old_index:
                        datatable_entry_index[file][entry_2] -= 1

def apply_default_tweaks():
    #Make levels identical in all modes
    #This needs to be done before applying the json tweaks so that exceptions can be patched over
    for entry in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(entry):
            continue
        datatable["PB_DT_CharacterParameterMaster"][entry]["HardEnemyLevel"]                       = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][entry]["NightmareEnemyLevel"]                  = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeDefaultEnemyLevel"]       = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeHardEnemyLevel"]          = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeNightmareEnemyLevel"]     = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeEnemyHPOverride"]         = 0.0
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeEnemyExperienceOverride"] = 0
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeEnemyStrIntMultiplier"]   = 1.0
        datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeEnemyConMndMultiplier"]   = 1.0
    #Apply manual tweaks defined in the json
    for file in mod_data["DefaultTweak"]:
        for entry in mod_data["DefaultTweak"][file]:
            for data in mod_data["DefaultTweak"][file][entry]:
                datatable[file][entry][data] = mod_data["DefaultTweak"][file][entry][data]
    #Loop through all enemies
    for entry in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(entry):
            continue
        if is_boss(entry):
            #Make boss health scale with level
            datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]*(99/datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]))
            datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]/5)*5
            datatable["PB_DT_CharacterParameterMaster"][entry]["MaxMP99Enemy"] = datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]
            #Make experience a portion of health
            if datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"] > 0:
                multiplier = (4/3)
                if entry[0:5] in mod_data["ExpModifier"]:
                    multiplier *= mod_data["ExpModifier"][entry[0:5]]
                datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"] = int(datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]*multiplier)
                datatable["PB_DT_CharacterParameterMaster"][entry]["Experience"]        = int(datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"]/100) + 2
            #Expand expertise point range that scales with level
            #In vanilla the range is too small and barely makes a difference
            if datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience99Enemy"] = 15
                datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience"]        = 1
            #Set stone type
            #Some regular enemies are originally set to the boss stone type which doesn't work well when petrified
            datatable["PB_DT_CharacterParameterMaster"][entry]["StoneType"] = "EPBStoneType::Boss"
        else:
            if datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"] > 0:
                multiplier = (2/3)
                if entry[0:5] in mod_data["ExpModifier"]:
                    multiplier *= mod_data["ExpModifier"][entry[0:5]]
                datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"] = int(datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]*multiplier)
                datatable["PB_DT_CharacterParameterMaster"][entry]["Experience"]        = int(datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"]/100) + 2
            if datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience99Enemy"] = 10
                datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience"]        = 1
            if entry != "N2008_BOSS":
                datatable["PB_DT_CharacterParameterMaster"][entry]["StoneType"] = "EPBStoneType::Mob"
        #Make level 1 health based off of level 99 health
        datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"] = int(datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]/100) + 2.0
        datatable["PB_DT_CharacterParameterMaster"][entry]["MaxMP"] = datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"]
        #Give all enemies a luck stat which reduces the chances of critting them
        #Originally only Gebel, Valefar and OD have one
        if datatable["PB_DT_CharacterParameterMaster"][entry]["LUC"] == 0 and entry != "N1008":
            datatable["PB_DT_CharacterParameterMaster"][entry]["LUC"]        = 5.0
            datatable["PB_DT_CharacterParameterMaster"][entry]["LUC99Enemy"] = 50.0
        #Allow Zangetsu to chain grab everyone
        #Whether he can grab or not is entirely based on the enemy's stone resistance
        #As long as it's not 100% resist the chain grab will connect so cap stone resistance at 99.99%
        if datatable["PB_DT_CharacterParameterMaster"][entry]["STO"] >= 100.0:
            datatable["PB_DT_CharacterParameterMaster"][entry]["STO"] = 99.99
    #Make up for the increased expertise range
    for entry in datatable["PB_DT_ArtsCommandMaster"]:
        datatable["PB_DT_ArtsCommandMaster"][entry]["Expertise"] = int(datatable["PB_DT_ArtsCommandMaster"][entry]["Expertise"]*2.5)
    #Lock 8 bit weapons behind recipes so that they aren't always easily accessible
    for entry in datatable["PB_DT_CraftMaster"]:
        if entry in bit_weapons:
            datatable["PB_DT_CraftMaster"][entry]["OpenKeyRecipeID"] = "ArmsRecipe018"
        elif entry[:-1] in bit_weapons and entry[-1] == "2":
            datatable["PB_DT_CraftMaster"][entry]["OpenKeyRecipeID"] = "ArmsRecipe019"
        elif entry[:-1] in bit_weapons and entry[-1] == "3":
            datatable["PB_DT_CraftMaster"][entry]["OpenKeyRecipeID"] = "ArmsRecipe020"
    #Remove the minimal damage addition on attacks
    for entry in datatable["PB_DT_DamageMaster"]:
        datatable["PB_DT_DamageMaster"][entry]["FixedDamage"] = 0.0
    #Loop through drops
    for entry in datatable["PB_DT_DropRateMaster"]:
        #Increase default drop rates
        if datatable["PB_DT_DropRateMaster"][entry]["AreaChangeTreasureFlag"]:
            drop_rate = mod_data["ItemDrop"]["StandardMat"]["ItemRate"]
        else:
            drop_rate = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]
        #Keep dulla head drops relatively low due to their spawn frequency
        if entry.split("_")[0] in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        if 0.0 < datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][entry]["ShardRate"] = mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        for data in ["RareItemRate", "CommonRate", "RareIngredientRate", "CommonIngredientRate"]:
            if 0.0 < datatable["PB_DT_DropRateMaster"][entry][data] < 100.0:
                datatable["PB_DT_DropRateMaster"][entry][data] = drop_rate*drop_rate_multiplier
        #Make coin type match the amount
        if datatable["PB_DT_DropRateMaster"][entry]["CoinOverride"] > 0:
            datatable["PB_DT_DropRateMaster"][entry]["CoinType"] = "EDropCoin::D" + str(datatable["PB_DT_DropRateMaster"][entry]["CoinOverride"])
    #Loop through all items
    for entry in datatable["PB_DT_ItemMaster"]:
        #Remove dishes from shop to prevent heal spam
        #In vanilla you can easily stock up on an infinite amount of them which breaks the game completely
        #This change also makes regular potions more viable now
        if entry in mod_data["ItemDrop"]["Dish"]["ItemPool"]:
            datatable["PB_DT_ItemMaster"][entry]["max"]       = 1
            datatable["PB_DT_ItemMaster"][entry]["buyPrice"]  = 0
            datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = 0
        #Update icon pointer of 8 bit weapons for the new icons
        #The icon texture was edited so that all new icons are evenly shifted from the original ones
        if entry[:-1] in bit_weapons and entry[-1] == "2":
            datatable["PB_DT_ItemMaster"][entry]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][entry]["IconPath"]) + 204)
        elif entry[:-1] in bit_weapons and entry[-1] == "3":
            datatable["PB_DT_ItemMaster"][entry]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][entry]["IconPath"]) + 338)
    #Loop through all shards
    for entry in datatable["PB_DT_ShardMaster"]:
        #Make all shard colors match their type
        datatable["PB_DT_ShardMaster"][entry]["ShardColorOverride"] = "EShardColor::None"
        #Make all shards ignore standstill
        datatable["PB_DT_ShardMaster"][entry]["IsStopByAccelWorld"] = False
    #Give magic attack if a weapon has an elemental attribute
    for entry in datatable["PB_DT_WeaponMaster"]:
        for data in ["FLA", "ICE", "LIG", "HOL", "DAR"]:
            if datatable["PB_DT_WeaponMaster"][entry][data]:
                datatable["PB_DT_WeaponMaster"][entry]["MagicAttack"] = datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"]
                break
    #Rebalance boss rush mode a bit
    #Remove all consumables from inventory
    for data in game_data["PBExtraModeInfo_BP"].Exports[1].Data[7].Value:
        data.Value[1].Value = 0
    #Start both stages at level 50
    for data in range(8, 14):
        game_data["PBExtraModeInfo_BP"].Exports[1].Data[data].Value = 50
    #Give all bosses level 66
    for data in game_data["PBExtraModeInfo_BP"].Exports[1].Data[14].Value:
        data.Value.Value = 66
    #Rename the second Zangetsu boss so that he isn't confused with the first
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N1011_STRONG"] = translation["Enemy"]["N1011_STRONG"]
    stringtable["PBMasterStringTable"]["ITEM_NAME_Medal013"]      = translation["Enemy"]["N1011_STRONG"] + " Medal"
    stringtable["PBMasterStringTable"]["ITEM_EXPLAIN_Medal013"]   = "Proof that you have triumphed over " + translation["Enemy"]["N1011_STRONG"] + "."
    #Update Jinrai cost description
    stringtable["PBMasterStringTable"]["ARTS_TXT_017_00"] += str(datatable["PB_DT_ArtsCommandMaster"]["JSword_GodSpeed1"]["CostMP"])
    #Slightly change Igniculus' descriptions to match other familiar's
    stringtable["PBMasterStringTable"]["SHARD_EFFECT_TXT_FamiliaIgniculus"] = stringtable["PBMasterStringTable"]["SHARD_EFFECT_TXT_FamiliaArcher"]
    stringtable["PBMasterStringTable"]["SHARD_NAME_FamiliaIgniculus"] = translation["Shard"]["FamiliaIgniculus"]
    #Fix the archive Doppleganger outfit color to match Miriam's
    index = game_data["M_Body06_06"].SearchNameReference(FString("/Game/Core/Character/P0000/Texture/Body/T_Body06_06_Color"))
    game_data["M_Body06_06"].SetNameReference(index, FString("/Game/Core/Character/P0000/Texture/Body/T_Body01_01_Color"))
    index = game_data["M_Body06_06"].SearchNameReference(FString("T_Body06_06_Color"))
    game_data["M_Body06_06"].SetNameReference(index, FString("T_Body01_01_Color"))
    #Add DLCs to the enemy archives
    add_enemy_to_archive(102, "N2016", [], None, "N2015")
    stringtable["PBMasterStringTable"]["ENEMY_EXPLAIN_N2016"] = "A giant monster that takes part on the most powerful Greed waves."
    add_enemy_to_archive(109, "N2017", [], None, "N2008")
    stringtable["PBMasterStringTable"]["ENEMY_EXPLAIN_N2017"] = "An instrument of the war fought over the magical cloth that powered the world."
    #Give the new dullahammer a unique name and look
    datatable["PB_DT_CharacterParameterMaster"]["N3127"]["NameStrKey"] = "ENEMY_NAME_N3127"
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N3127"] = translation["Enemy"]["N3127"]
    set_material_hsv("MI_N3127_Eye", "EmissiveColor" , (215, 100, 100))
    set_material_hsv("MI_N3127_Eye", "HighlightColor", (215,  65, 100))
    #Give Guardian his own shard drop
    datatable["PB_DT_CharacterMaster"]["N2017"]["ItemDrop"] = "N2017_Shard"
    datatable["PB_DT_DropRateMaster"]["N2017_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Deepsinker_Shard"])
    datatable["PB_DT_DropRateMaster"]["N2017_Shard"]["ShardId"] = "TissRosain"
    datatable["PB_DT_CraftMaster"]["TissRosain"]["OpenKeyRecipeID"] = "Medal019"
    #Make the second train gate a regular gate rather than a debug
    game_data["m09TRN_004_Gimmick"].Exports[257].Data[18].Value = False
    #Move the Alfred magical seal closer to the edge of the screen so that Dimension Shift cannot pass
    game_data["m12SND_023_Gimmick"].Exports[7].Data[0].Value[0].Value = FVector(1200, 0, 2520)
    #Give the lever door in upper cathedral its own gimmick flag instead of being shared with the hall one
    game_data["m05SAN_017_Gimmick"].Exports[1].Data[7].Value = FName.FromString(game_data["m05SAN_017_Gimmick"], "SAN_017_LockDoor")
    datatable["PB_DT_GimmickFlagMaster"]["SAN_017_LockDoor"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["SAN_017_LockDoor"]["Id"] = get_available_gimmick_flag()
    #Remove the breakable wall in m17RVA_003 that shares its drop id with the wall in m17RVA_011
    datatable["PB_DT_GimmickFlagMaster"]["RVA_003_ItemWall"]["Id"] = datatable["PB_DT_GimmickFlagMaster"]["HavePatchPureMiriam"]["Id"]
    #Add the missing gate warps for the extra characters
    #That way impassable obstacles are no longer a problem
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
    add_extra_mode_warp("m15JPN_002_Gimmick", FVector(1740, 0, 1260), FRotator(180,   0,   0), FVector(1200, 0,   75), FRotator(  0,   0,   0))
    add_extra_mode_warp("m17RVA_001_Gimmick", FVector( 800, 0, 2080), FRotator(  0,   0, 180), FVector( 540, 0, 1800), FRotator(  0, 180,   0))
    add_extra_mode_warp("m17RVA_011_Gimmick", FVector(1900, 0, 2080), FRotator(180,   0,   0), FVector(2140, 0, 2080), FRotator(  0,   0, 180))
    add_extra_mode_warp("m17RVA_012_Gimmick", FVector(2320, 0,  120), FRotator(  0, 180,   0), FVector(1640, 0,  120), FRotator(  0,   0,   0))
    add_extra_mode_warp("m18ICE_008_Gimmick", FVector(1745, 0,  565), FRotator(  0, 180,   0), FVector(2205, 0,  630), FRotator(  0,   0,   0))
    #Make the garden iron maiden disappear in extra modes
    struct = BoolPropertyData(FName.FromString(game_data["m04GDN_006_Gimmick"], "DeleteSpinoffCharacter"))
    struct.Value = True
    game_data["m04GDN_006_Gimmick"].Exports[6].Data.Add(struct)
    #Add the missing Bloodless candle that was accidentally removed in a recent game update
    add_level_actor("m07LIB_009_Gimmick", "BP_DM_BloodlessAbilityGimmick_C", FVector(720, -120, 1035), FRotator(0, 0, 0), FVector(1, 1, 1), {"UnlockAbilityType": FName.FromString(game_data["m07LIB_009_Gimmick"], "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP_5")})
    #Due to Focalor being scrapped the devs put aqua stream on a regular enemy instead but this can cause first playthroughs to miss out on the shard
    #Add a shard candle for it so that it becomes a guaranteed
    add_level_actor("m11UGD_019_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", FVector(1320, -60, 1845), FRotator(180, 0, 0), FVector(1, 1, 1), {"ShardID": FName.FromString(game_data["m11UGD_019_Gimmick"], "Aquastream"), "GimmickFlag": FName.FromString(game_data["m11UGD_019_Gimmick"], "AquastreamLantarn001")})
    datatable["PB_DT_GimmickFlagMaster"]["AquastreamLantarn001"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["AquastreamLantarn001"]["Id"] = get_available_gimmick_flag()
    datatable["PB_DT_DropRateMaster"]["Aquastream_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Deepsinker_Shard"])
    datatable["PB_DT_DropRateMaster"]["Aquastream_Shard"]["ShardId"] = "Aquastream"
    #Add a shard candle for Igniculus in Celeste's room
    #That way Celeste key becomes relevant and Igniculus can be obtained in story mode
    add_level_actor("m88BKR_003_Gimmick", "BP_DM_BaseLantern_ShardChild2_C", FVector(660, -120, 315), FRotator(0, 0, 0), FVector(1, 1, 1), {"ShardID": FName.FromString(game_data["m88BKR_003_Gimmick"], "FamiliaIgniculus"), "GimmickFlag": FName.FromString(game_data["m88BKR_003_Gimmick"], "IgniculusLantarn001")})
    datatable["PB_DT_GimmickFlagMaster"]["IgniculusLantarn001"] = {}
    datatable["PB_DT_GimmickFlagMaster"]["IgniculusLantarn001"]["Id"] = get_available_gimmick_flag()
    datatable["PB_DT_DropRateMaster"]["FamiliaIgniculus_Shard"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["FamiliaArcher_Shard"])
    datatable["PB_DT_DropRateMaster"]["FamiliaIgniculus_Shard"]["ShardId"] = "FamiliaIgniculus"
    datatable["PB_DT_ItemMaster"]["FamiliaIgniculus"]["NotListedInArchive"]     = False
    datatable["PB_DT_ItemMaster"]["FamiliaIgniculus"]["NotCountAsCompleteness"] = False
    #The HavePatchPureMiriam gimmick flag triggers as soon as a Pure Miriam chest is loaded in a room
    #So place one in the first ship room for this flag to trigger as soon as the game starts
    add_level_actor("m01SIP_000_Gimmick", "PBPureMiriamTreasureBox_BP_C", FVector(-999, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1), {"DropItemID": FName.FromString(game_data["m01SIP_000_Gimmick"], "AAAA_Shard"), "ItemID": FName.FromString(game_data["m01SIP_000_Gimmick"], "AAAA_Shard")})
    #Remove the Dullhammer in the first galleon room on hard to prevent rough starts
    #That way you can at least save once before the game truly starts
    remove_level_class("m01SIP_001_Enemy_Hard", "Chr_N3015_C")
    #Remove the morte spawner that isn't an actual enemy actor
    remove_level_class("m01SIP_011_Enemy", "PBCharacterGeneratorActor")
    #Remove the bone mortes from that one crowded room in galleon
    remove_level_class("m01SIP_014_Enemy_Hard", "Chr_N3004_C")
    #Remove the giant rat in Den, was most likely a dev mistake
    remove_level_class("m10BIG_008_Enemy", "Chr_N3051_C")
    #Remove the boss door duplicate in the room before Craftwork
    remove_level_class("m05SAN_011_BG", "PBBossDoor_BP_C")
    #Fix that one Water Leaper in desert that falls through the floor by shifting its position upwards
    game_data["m12SND_025_Enemy"].Exports[4].Data[4].Value[0].Value = FVector(-260, -700, 600)
    #Fix some of the giant cannon stacks clipping over each other
    game_data["m10BIG_008_Enemy"].Exports[17].Data[4].Value[0].Value     = FVector(2220, 0, 3505)
    game_data["m10BIG_008_Enemy_Hard"].Exports[0].Data[4].Value[0].Value = FVector(2220, 0, 3865)
    game_data["m10BIG_008_Enemy_Hard"].Exports[1].Data[4].Value[0].Value = FVector(2220, 0, 4225)
    game_data["m10BIG_008_Enemy"].Exports[18].Data[4].Value[0].Value     = FVector( 300, 0, 1345)
    game_data["m10BIG_008_Enemy_Hard"].Exports[2].Data[4].Value[0].Value = FVector( 300, 0, 1705)
    game_data["m10BIG_008_Enemy_Hard"].Exports[3].Data[4].Value[0].Value = FVector( 300, 0, 2065)
    game_data["m10BIG_008_Enemy"].Exports[19].Data[4].Value[0].Value     = FVector(2220, 0,  505)
    game_data["m10BIG_008_Enemy_Hard"].Exports[4].Data[4].Value[0].Value = FVector(2220, 0,  865)
    game_data["m10BIG_008_Enemy_Hard"].Exports[5].Data[4].Value[0].Value = FVector(2220, 0, 1225)
    game_data["m10BIG_013_Enemy"].Exports[5].Data[4].Value[0].Value      = FVector(1020, 0, 1585)
    game_data["m10BIG_013_Enemy_Hard"].Exports[0].Data[4].Value[0].Value = FVector(1020, 0, 1945)
    game_data["m10BIG_013_Enemy_Hard"].Exports[1].Data[4].Value[0].Value = FVector(1020, 0, 2305)
    game_data["m10BIG_013_Enemy"].Exports[6].Data[4].Value[0].Value      = FVector(2040, 0, 2005)
    game_data["m10BIG_013_Enemy_Hard"].Exports[2].Data[4].Value[0].Value = FVector(2040, 0, 2365)
    game_data["m10BIG_013_Enemy"].Exports[7].Data[4].Value[0].Value      = FVector( 300, 0, 1105)
    game_data["m10BIG_013_Enemy_Hard"].Exports[3].Data[4].Value[0].Value = FVector( 300, 0, 1465)
    game_data["m10BIG_013_Enemy_Hard"].Exports[4].Data[4].Value[0].Value = FVector( 360, 0, 2065)
    game_data["m10BIG_013_Enemy_Hard"].Exports[5].Data[4].Value[0].Value = FVector( 360, 0, 2425)
    #Remove the iron maidens that were added by the devs in an update in the tall entrance shaft
    remove_level_class("m03ENT_000_Gimmick", "BP_IronMaiden_C")
    #Add magic doors instead to truly prevent tanking through
    add_level_actor("m03ENT_000_Gimmick", "BP_MagicDoor_C", FVector(1260, -270, 7500), FRotator(  0, 0, 0), FVector(-1, 1, 1), {"CommonFlag": FName.FromString(game_data["m03ENT_000_Gimmick"], "EGameCommonFlag::None")})
    add_level_actor("m03ENT_000_Gimmick", "BP_MagicDoor_C", FVector(1260, -270, 9120), FRotator(180, 0, 0), FVector(-1, 1, 1), {"CommonFlag": FName.FromString(game_data["m03ENT_000_Gimmick"], "EGameCommonFlag::None")})
    #Change Dark Matter so that consuming it puts the player in OHKO mode until the next death
    datatable["PB_DT_SpecialEffectMaster"]["DarkMatter"]["LifeTime"] = -1
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatter"]["Type"]                     = "EPBSpecialEffect::None"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatter"]["ParameterName"]            = "None"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxHP"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["CurseTempDownMaxHP"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxHP"]["DefId"]       = "DarkMatterTempDownMaxHP"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxHP"]["Parameter01"] = 99.999
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxMP"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["CurseTempDownMaxMP"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxMP"]["DefId"]       = "DarkMatterTempDownMaxMP"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DarkMatterTempDownMaxMP"]["Parameter01"] = 99.999
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterHitPoint"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["CurseHitPoint"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterHitPoint"]["GroupId"] = "DarkMatter"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterHitPoint"]["DefId"]   = "DarkMatterTempDownMaxHP"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterMagicPoint"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["CurseMagicPoint"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterMagicPoint"]["GroupId"] = "DarkMatter"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DarkMatterMagicPoint"]["DefId"]   = "DarkMatterTempDownMaxMP"
    #Give primary stat debuffs their secondary stat too
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["Id"]      = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["Id"]      = "DEBUFF_RATE_INT_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_INT_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["Id"]      = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["Id"]      = "DEBUFF_RATE_MND_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_MND_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["DefId"]       = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["Type"]        = "EPBSpecialEffect::None"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["Parameter01"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["Parameter02"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["Parameter03"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["DefId"]       = "DEBUFF_RATE_INT_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["Parameter01"] = 14
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["DefId"]       = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["Type"]        = "EPBSpecialEffect::None"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["Parameter01"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["Parameter02"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["Parameter03"] = 0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]                = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["DefId"]       = "DEBUFF_RATE_MND_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["Parameter01"] = 15
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_ATK_WITH_EFFECT"]["DefId"]   = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_STR_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_INT_WITH_EFFECT"]["DefId"]   = "DEBUFF_RATE_INT_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_DEF_WITH_EFFECT"]["DefId"]   = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]            = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_CON_WITH_EFFECT"])
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["GroupId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    datatable["PB_DT_SpecialEffectGroupMaster"]["DEBUFF_RATE_MND_WITH_EFFECT"]["DefId"]   = "DEBUFF_RATE_MND_WITH_EFFECT"
    datatable["PB_DT_WeaponMaster"]["Swordbreaker"]["SpecialEffectId"]        = "DEBUFF_RATE_ATK_WITH_EFFECT"
    datatable["PB_DT_DamageMaster"]["P0000_Jsword_Kabuto"]["SpecialEffectId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    for suffix in ["", "_EX", "_EX2"]:
        datatable["PB_DT_DamageMaster"]["WeaponbaneRounds" + suffix]["SpecialEffectId"] = "DEBUFF_RATE_ATK_WITH_EFFECT"
        datatable["PB_DT_DamageMaster"]["ShieldbaneRounds" + suffix]["SpecialEffectId"] = "DEBUFF_RATE_DEF_WITH_EFFECT"
    #Add a special ring that buffs the katana parry techniques
    add_game_item(106, "MightyRing", "Accessory", "Ring", (2048, 3200), translation["Item"]["MightyRing"], "A symbol of great courage that amplifies the power of counterattacks.", 8080, False)
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt245"]                                                   = copy.deepcopy(datatable["PB_DT_EnchantParameterType"]["DUMMY"])
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt245"]["Type_5_BF08F4064B9CF244C30C7788588CFDF5"]        = "EPBEquipSpecialAttribute::BuffParryArt"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt245"]["EquipType_25_DEF1C32D420ACBA29D5AA0B5D0AE0D20"]  = "ECarriedCatalog::Accessory1"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt245"]["ItemID_31_461716F74C5895124D82E0B3CA33B6B3"]     = "MightyRing"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt245"]["EquipValue_28_5CFE97924D56254C9B62AF83698220FC"] = 1.5
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt246"]                                                   = copy.deepcopy(datatable["PB_DT_EnchantParameterType"]["DUMMY"])
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt246"]["Type_5_BF08F4064B9CF244C30C7788588CFDF5"]        = "EPBEquipSpecialAttribute::BuffParryArt"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt246"]["EquipType_25_DEF1C32D420ACBA29D5AA0B5D0AE0D20"]  = "ECarriedCatalog::Accessory2"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt246"]["ItemID_31_461716F74C5895124D82E0B3CA33B6B3"]     = "MightyRing"
    datatable["PB_DT_EnchantParameterType"]["BuffParryArt246"]["EquipValue_28_5CFE97924D56254C9B62AF83698220FC"] = 1.5
    datatable["PB_DT_ArmorMaster"]["MightyRing"]["MeleeDefense"] = 3
    datatable["PB_DT_ArmorMaster"]["MightyRing"]["DAG"]          = 5
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareItemId"]               = "MightyRing"
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareItemQuantity"]         = 1
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareItemRate"]             = 100.0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonItemId"]             = "None"
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonItemQuantity"]       = 0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonRate"]               = 0.0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareIngredientId"]         = "None"
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareIngredientQuantity"]   = 0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["RareIngredientRate"]       = 0.0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonIngredientId"]       = "None"
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonIngredientQuantity"] = 0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CommonIngredientRate"]     = 0.0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CoinType"]                 = "EDropCoin::None"
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["CoinOverride"]             = 0
    datatable["PB_DT_DropRateMaster"]["Treasurebox_BIG010_1"]["AreaChangeTreasureFlag"]   = False
    mod_data["ItemDrop"]["Accessory"]["ItemPool"].append("MightyRing")
    for num in range(4):
        mod_data["QuestRequirement"]["Memento"]["ItemPool"].append("MightyRing")
    #Add an invisibility cloak into the game
    add_game_item(151, "InvisibleCloak", "Armor", "None", (3840, 2944), translation["Item"]["InvisibleCloak"], "A magical mantle that renders anything it covers fully invisible.", 22500, False)
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["MeleeDefense"] = 11
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["MagicDefense"] = 52
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["HOL"]          = 5
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["DAR"]          = 5
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["INT"]          = 10
    datatable["PB_DT_ArmorMaster"]["InvisibleCloak"]["MND"]          = 8
    datatable["PB_DT_DropRateMaster"]["N3025_Shard"]["RareItemId"]       = "InvisibleCloak"
    datatable["PB_DT_DropRateMaster"]["N3025_Shard"]["RareItemQuantity"] = 1
    datatable["PB_DT_DropRateMaster"]["N3025_Shard"]["RareItemRate"]     = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]
    mod_data["ItemDrop"]["Armor"]["ItemPool"].append("InvisibleCloak")
    for num in range(5):
        mod_data["QuestRequirement"]["Memento"]["ItemPool"].append("InvisibleCloak")
    #Add staggering bullets into the game
    add_game_item(8, "RagdollBullet", "Bullet", "None", (3456, 128), translation["Item"]["RagdollBullet"], "Strange bullets that contort targets, leaving a lasting impact.", 0, True)
    datatable["PB_DT_AmmunitionMaster"]["RagdollBullet"]["MeleeAttack"] = 40
    datatable["PB_DT_CraftMaster"]["RagdollBullet"]["CraftValue"]       = 5
    datatable["PB_DT_CraftMaster"]["RagdollBullet"]["Ingredient2Id"]    = "Silver"
    datatable["PB_DT_CraftMaster"]["RagdollBullet"]["Ingredient3Id"]    = "HolyWater"
    datatable["PB_DT_CraftMaster"]["RagdollBullet"]["Ingredient3Total"] = 1
    datatable["PB_DT_CraftMaster"]["RagdollBullet"]["OpenKeyRecipeID"]  = "BalletRecipe002"
    for suffix in ["", "_EX", "_EX2"]:
        datatable["PB_DT_DamageMaster"]["RagdollBullet" + suffix]["SA_Attack"] = 9999
    for num in range(5):
        mod_data["ItemDrop"]["Bullet"]["ItemPool"].append("RagdollBullet")
    #Add a tonic that speeds up all of Miriam's movement for 10 seconds
    add_game_item(9, "TimeTonic", "Potion", "None", (3840, 0), translation["Item"]["TimeTonic"], "An ancient drink that grants the ability to view the world at a slower pace.", 2000, True)
    datatable["PB_DT_ItemMaster"]["TimeTonic"]["max"] = 5
    datatable["PB_DT_CraftMaster"]["TimeTonic"]["Ingredient1Id"] = "MonsterBirdTears"
    datatable["PB_DT_CraftMaster"]["TimeTonic"]["Ingredient2Id"] = "SeekerEye"
    datatable["PB_DT_CraftMaster"]["TimeTonic"]["Alkhahest"]     = 4
    datatable["PB_DT_ConsumableMaster"]["TimeTonic"]["IsAutoUse"] = False
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["TimeTonic"]["Type"]        = "EPBSpecialEffect::TimeRate"
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["TimeTonic"]["Parameter01"] = 1.5
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["TimeTonic"]["Parameter02"] = 1.0
    datatable["PB_DT_SpecialEffectDefinitionMaster"]["TimeTonic"]["Parameter03"] = 20.0
    datatable["PB_DT_SpecialEffectMaster"]["TimeTonic"]["LifeTime"] = 10.0
    for num in range(2):
        mod_data["ItemDrop"]["Potion"]["ItemPool"].append("TimeTonic")
    #With this mod vanilla rando is pointless and obselete so remove its widget
    remove_vanilla_rando()
    #Store original enemy stats for convenience
    global original_enemy_stats
    original_enemy_stats = {}
    for entry in datatable["PB_DT_CharacterParameterMaster"]:
        original_enemy_stats[entry] = {}
        original_enemy_stats[entry]["Level"] = datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        original_enemy_stats[entry]["POI"]   = datatable["PB_DT_CharacterParameterMaster"][entry]["POI"]
        original_enemy_stats[entry]["CUR"]   = datatable["PB_DT_CharacterParameterMaster"][entry]["CUR"]
        original_enemy_stats[entry]["STO"]   = datatable["PB_DT_CharacterParameterMaster"][entry]["STO"]
        original_enemy_stats[entry]["SLO"]   = datatable["PB_DT_CharacterParameterMaster"][entry]["SLO"]
    #Test
    #add_global_room_pickup("m05SAN_012", "TestDemoniccapture")
    #datatable["PB_DT_DropRateMaster"]["TestDemoniccapture"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Tresurebox_SAN000_01"])
    #datatable["PB_DT_DropRateMaster"]["TestDemoniccapture"]["RareItemId"]       = "Demoniccapture"
    #datatable["PB_DT_DropRateMaster"]["TestDemoniccapture"]["RareItemQuantity"] = 1
    #datatable["PB_DT_DropRateMaster"]["TestDemoniccapture"]["RareItemRate"]     = 100.0
    #datatable["PB_DT_DropRateMaster"]["N1003_Shard"]["ShardId"] = "AccelWorld"
    #add_global_room_pickup("m06KNG_020", "TestNeverSatisfied")
    #datatable["PB_DT_DropRateMaster"]["TestNeverSatisfied"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Tresurebox_SAN000_01"])
    #datatable["PB_DT_DropRateMaster"]["TestNeverSatisfied"]["RareItemId"]       = "NeverSatisfied"
    #datatable["PB_DT_DropRateMaster"]["TestNeverSatisfied"]["RareItemQuantity"] = 1
    #datatable["PB_DT_DropRateMaster"]["TestNeverSatisfied"]["RareItemRate"]     = 100.0
    #datatable["PB_DT_DropRateMaster"]["N2013_Shard"]["ShardId"] = "AccelWorld"
    #add_global_room_pickup("m09TRN_002", "TestHammerknuckle")
    #datatable["PB_DT_DropRateMaster"]["TestHammerknuckle"] = copy.deepcopy(datatable["PB_DT_DropRateMaster"]["Tresurebox_SAN000_01"])
    #datatable["PB_DT_DropRateMaster"]["TestHammerknuckle"]["RareItemId"]       = "Hammerknuckle"
    #datatable["PB_DT_DropRateMaster"]["TestHammerknuckle"]["RareItemQuantity"] = 1
    #datatable["PB_DT_DropRateMaster"]["TestHammerknuckle"]["RareItemRate"]     = 100.0
    #datatable["PB_DT_DropRateMaster"]["N2001_Shard"]["ShardId"] = "AccelWorld"

def search_and_replace_string(filename, class_name, data_name, old_value, new_value):
    #Search for a specific piece of data to change in a level file and swap it
    for export in game_data[filename].Exports:
        if class_name == str(game_data[filename].Imports[abs(int(str(export.ClassIndex))) - 1].ObjectName):
            for data in export.Data:
                if str(data.Name) == data_name and str(data.Value) == old_value:
                    data.Value = FName.FromString(game_data[filename], new_value)

def randomize_classic_mode_drops():
    #Convert the drop dictionary to a wheighted list
    classic_pool = []
    for item in mod_data["ClassicDrop"]:
        for num in range(mod_data["ClassicDrop"][item]):
            classic_pool.append(item)
    #Search for any instance of SpawnItemTypeClass and replace it with a random item
    for stage in ["Stage_00", "Stage_01", "Stage_02", "Stage_03", "Stage_04", "Stage_05A", "Stage_05B"]:
        filename = "Classic_" + stage + "_Objects"
        for export in game_data[filename].Exports:
            for data in export.Data:
                if str(data.Name) == "SpawnItemTypeClass":
                    if int(str(data.Value)) == 0:
                        item_name = "None"
                    else:
                        item_name = str(game_data[filename].Imports[abs(int(str(data.Value))) - 1].ObjectName).replace("BP_PBC_", "").replace("_C", "")
                    #Don't randomize the item if it isn't in the pool list
                    if not item_name in classic_pool:
                        continue
                    chosen = random.choice(classic_pool)
                    if chosen == "None":
                        data.Value = FPackageIndex(0)
                        break
                    else:
                        item_class = "BP_PBC_" + chosen + "_C"
                    #First check is the item is already in the level's imports
                    count = 0
                    found = False
                    for uimport in game_data[filename].Imports:
                        count -= 1
                        if str(uimport.ObjectName) == item_class:
                            data.Value = FPackageIndex(count)
                            found = True
                            break
                    if found:
                        break
                    #If not then add the import manually
                    new_import_index = len(game_data[filename].Imports)
                    old_import = game_data["Classic_" + classic_item_to_properties[item_class]["Level"] + "_Objects"].Imports[classic_item_to_properties[item_class]["Index"][0]]
                    package_index = abs(int(str(old_import.OuterIndex.Index))) - 1
                    new_import = Import(
                        FName.FromString(game_data[filename], str(old_import.ClassPackage)),
                        FName.FromString(game_data[filename], str(old_import.ClassName)),
                        FPackageIndex(-(new_import_index + 1 + 2)),
                        FName.FromString(game_data[filename], str(old_import.ObjectName))
                    )
                    game_data[filename].Imports.Add(new_import)
                    old_import = game_data["Classic_" + classic_item_to_properties[item_class]["Level"] + "_Objects"].Imports[classic_item_to_properties[item_class]["Index"][1]]
                    new_import = Import(
                        FName.FromString(game_data[filename], str(old_import.ClassPackage)),
                        FName.FromString(game_data[filename], str(old_import.ClassName)),
                        FPackageIndex(-(new_import_index + 1 + 2)),
                        FName.FromString(game_data[filename], str(old_import.ObjectName))
                    )
                    game_data[filename].Imports.Add(new_import)
                    old_import = game_data["Classic_" + classic_item_to_properties[item_class]["Level"] + "_Objects"].Imports[package_index]
                    new_import = Import(
                        FName.FromString(game_data[filename], str(old_import.ClassPackage)),
                        FName.FromString(game_data[filename], str(old_import.ClassName)),
                        FPackageIndex(0),
                        FName.FromString(game_data[filename], str(old_import.ObjectName))
                    )
                    game_data[filename].Imports.Add(new_import)
                    data.Value = FPackageIndex(-(new_import_index + 1))
                    break

def set_bigtoss_mode():
    #Greatly increase the knockback from enemy attacks and randomize the impulse angle
    enemy_attack_ranges = [
        range(302, 783),
        range(814, 835),
        range(848, 862)
    ]
    for index_range in enemy_attack_ranges:
        for index in index_range:
            entry = list(datatable["PB_DT_DamageMaster"])[index]
            if "P000" in entry or "P000" in datatable["PB_DT_DamageMaster"][entry]["GroupId"]:
                continue
            if "FAMILIA" in entry or "FAMILIA" in datatable["PB_DT_DamageMaster"][entry]["GroupId"]:
                continue
            if entry.split("_")[-1] == "BRV" or datatable["PB_DT_DamageMaster"][entry]["GroupId"].split("_")[-1] == "BRV":
                continue
            datatable["PB_DT_DamageMaster"][entry]["KnockBackDistance"] += 20.0
            datatable["PB_DT_DamageMaster"][entry]["KnockBackLimitAngleMin"] = float(random.randint(-180, 180))
            datatable["PB_DT_DamageMaster"][entry]["KnockBackLimitAngleMax"] = float(random.randint(-180, 180))

def update_lip_pointer(event, event_replacement, prefix):
    #Simply swap the file's name in the name map and save as the new name
    event = prefix + "_" + event + "_LIP"
    event_replacement = prefix + "_" + event_replacement + "_LIP"
    
    if event_replacement + ".uasset" in os.listdir("Data\\LipSync"):
        event_replacement_data = UAsset("Data\\LipSync\\" + event_replacement + ".uasset", UE4Version.VER_UE4_22)
        index = event_replacement_data.SearchNameReference(FString(event_replacement))
        event_replacement_data.SetNameReference(index, FString(event))
        index = event_replacement_data.SearchNameReference(FString("/Game/Core/UI/Dialog/Data/LipSync/" + event_replacement))
        event_replacement_data.SetNameReference(index, FString("/Game/Core/UI/Dialog/Data/LipSync/" + event))
        event_replacement_data.Write(mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + event + ".uasset")
    elif event + ".uasset" in os.listdir("Data\\LipSync"):
        event_data = UAsset("Data\\LipSync\\" + event + ".uasset", UE4Version.VER_UE4_22)
        for export in event_data.Exports:
            if str(export.ObjectName) == event:
                export.Data.Clear()
        event_data.Write(mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + event + ".uasset")

def update_portrait_pointer(portrait, portrait_replacement):
    #Simply swap the file's name in the name map and save as the new name
    portrait_replacement_data = UAsset(asset_dir + "\\" + file_to_path[portrait_replacement] + "\\" + portrait_replacement + ".uasset", UE4Version.VER_UE4_22)
    index = portrait_replacement_data.SearchNameReference(FString(portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString(portrait))
    index = portrait_replacement_data.SearchNameReference(FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait))
    portrait_replacement_data.Write(mod_dir + "\\" + file_to_path[portrait] + "\\" + portrait + ".uasset")

def update_item_descriptions():
    #Add magical stats to descriptions
    for entry in datatable["PB_DT_ArmorMaster"]:
        if not "ITEM_EXPLAIN_" + entry in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_ArmorMaster"][entry]["MagicAttack"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + entry, "<span color=\"#ff8000\">mATK " + str(datatable["PB_DT_ArmorMaster"][entry]["MagicAttack"]) + "</>")
        if datatable["PB_DT_ArmorMaster"][entry]["MagicDefense"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + entry, "<span color=\"#ff00ff\">mDEF " + str(datatable["PB_DT_ArmorMaster"][entry]["MagicDefense"]) + "</>")
    #Add restoration amount to descriptions
    for entry in datatable["PB_DT_SpecialEffectDefinitionMaster"]:
        if not "ITEM_EXPLAIN_" + entry in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][entry]["Type"] == "EPBSpecialEffect::ChangeHP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + entry, "<span color=\"#00ff00\">HP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][entry]["Parameter01"])) + "</>")
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][entry]["Type"] == "EPBSpecialEffect::ChangeMP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + entry, "<span color=\"#00bfff\">MP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][entry]["Parameter01"])) + "</>")
    for entry in datatable["PB_DT_AmmunitionMaster"]:
        if not "ITEM_EXPLAIN_" + entry in stringtable["PBMasterStringTable"]:
            continue
        append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + entry, "<span color=\"#ff0000\">ATK " + str(datatable["PB_DT_AmmunitionMaster"][entry]["MeleeAttack"]) + "</>")
    #Add Shovel Armor's attack stat to its description
    append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_Shovelarmorsarmor", "<span color=\"#ff0000\">wATK " + str(int(datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"])) + "</>")

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
                if map_doors[exit].room == "m20JRN_002":
                    filename = "m20JRN_002_BG"
                else:
                    filename = get_gimmick_filename(map_doors[exit].room)
                #Offset the door for Journey
                if map_doors[exit].room == "m20JRN_004":
                    x_offset = 180
                elif "m20JRN" in map_doors[exit].room:
                    x_offset = -60
                else:
                    x_offset = 0
                location = FVector(x_offset, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"] = FName.FromString(game_data[filename], room_to_boss[room])
                if map_doors[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    properties["IsRight"] = False
                    if exit in arched_doors:
                        rotation.Yaw += 15
                if map_doors[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[exit].room]["AreaWidthSize"]*1260 - x_offset
                    properties["IsRight"] = True
                    if exit in arched_doors:
                        rotation.Yaw -= 15
                location.Z = map_doors[exit].z_block*720 + 240.0
                if map_doors[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
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
                filename = get_gimmick_filename(map_doors[exit].room)
                location = FVector(0, 0, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 3, 1)
                properties = {}
                properties["BossID"]     = FName.FromString(game_data[filename], room_to_backer[room][0])
                properties["KeyItemID"]  = FName.FromString(game_data[filename], "Keyofbacker" + str(room_to_backer[room][1]))
                properties["TutorialID"] = FName.FromString(game_data[filename], "KeyDoor" + "{:02x}".format(room_to_backer[room][1]))
                if room_to_backer[room][0] == "None":
                    properties["IsMusicBoxRoom"] =  True
                if map_doors[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -180
                    if exit in arched_doors:
                        rotation.Yaw += 15
                if map_doors[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[exit].room]["AreaWidthSize"]*1260
                    if exit in arched_doors:
                        rotation.Yaw -= 15
                location.Z = map_doors[exit].z_block*720 + 240.0
                if map_doors[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
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
                if map_doors[exit].room == "m03ENT_006":
                    datatable["PB_DT_EventFlagMaster"]["Event_05_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if exit == "ARC_001_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_09_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                if exit == "TAR_000_0_0_LEFT":
                    datatable["PB_DT_EventFlagMaster"]["Event_12_001_0000"]["Id"] = datatable["PB_DT_EventFlagMaster"]["Event_01_001_0000"]["Id"]
                filename = get_gimmick_filename(map_doors[exit].room)
                x_offset = 40
                location = FVector(x_offset, -180, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                if map_doors[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    class_name = "BP_AreaDoor_C(Left)"
                if map_doors[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[exit].room]["AreaWidthSize"]*1260 - x_offset
                    class_name = "BP_AreaDoor_C(Right)"
                location.Z = map_doors[exit].z_block*720 + 240.0
                if map_doors[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
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
                filename = get_gimmick_filename(map_doors[exit].room)
                location = FVector(-80, -120, 0)
                rotation = FRotator(0, 0, 0)
                scale    = FVector(1, 1, 1)
                properties = {}
                properties["DiaryID"] = FName.FromString(game_data[filename], "None")
                if map_doors[exit].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                    rotation.Yaw = -30
                if map_doors[exit].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                    location.X = datatable["PB_DT_RoomMaster"][map_doors[exit].room]["AreaWidthSize"]*1260 - 50
                    rotation.Yaw = 30
                location.Z = map_doors[exit].z_block*720 + 240.0
                if map_doors[exit].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                    location.Z -= 180.0
                if map_doors[exit].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
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
            if map_doors[door].direction_part in [Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP]:
                location.X = -18
                location.Z = map_doors[door].z_block*720 + door_height
                lever_offset = -360
                if door in arched_doors:
                    rotation.Yaw += 20
            if map_doors[door].direction_part in [Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP]:
                location.X = datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260 + 18
                location.Z = map_doors[door].z_block*720 + door_height
                lever_offset = 360
                if door in arched_doors:
                    rotation.Yaw -= 20
            if map_doors[door].direction_part in [Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT]:
                location.X = map_doors[door].x_block*1260 + 510.0
                location.Z = datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"]*720 - 5
                rotation.Pitch = -90
                lever_offset = -360
            if map_doors[door].direction_part in [Direction.BOTTOM, Direction.BOTTOM_LEFT, Direction.BOTTOM_RIGHT]:
                location.X = map_doors[door].x_block*1260 + 510.0
                location.Z = 5
                rotation.Pitch = -90
                lever_offset = 360
            #Sub direction
            if map_doors[door].direction_part in [Direction.LEFT_BOTTOM, Direction.RIGHT_BOTTOM]:
                if "m10BIG" in room:
                    location.Z -= door_height
                elif "_".join([room[3:], str(map_doors[door].x_block), str(map_doors[door].z_block), map_doors[door].direction_part.name.split("_")[0]]) in map_connections[room]:
                    location.Z -= door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    location.Z -= door_height*scale.Z - door_height
                else:
                    location.Z -= 180
            if map_doors[door].direction_part in [Direction.LEFT_TOP, Direction.RIGHT_TOP]:
                if "m10BIG" in room:
                    location.Z += door_height
                elif "_".join([room[3:], str(map_doors[door].x_block), str(map_doors[door].z_block), map_doors[door].direction_part.name.split("_")[0]]) in map_connections[room]:
                    location.Z += door_height
                    scale.X = 4.25
                    scale.Z = 4.25
                    if map_doors[door].direction_part == Direction.LEFT_TOP:
                        location.X -= (door_width*scale.Z - door_width)/2 - door_width
                    else:
                        location.X += (door_width*scale.Z - door_width)/2 - door_width
                else:
                    location.Z += 180
            if map_doors[door].direction_part in [Direction.TOP_LEFT, Direction.BOTTOM_LEFT]:
                if "m10BIG" in room:
                    location.X -= 510
                else:
                    location.X -= 370
            if map_doors[door].direction_part in [Direction.TOP_RIGHT, Direction.BOTTOM_RIGHT]:
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
    room = map_doors[door].room
    return door in door_skip or room in room_to_boss or room in room_to_backer or not room in mod_data["RoomRequirement"]

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
            elif datatable["PB_DT_DropRateMaster"][drop_id]["RareItemId"] in key_items:
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
                properties["TreasureFlag"] = FName.FromString(game_data[filename], "EGameTreasureFlag::" + remove_inst_number(drop_id))
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
                if datatable["PB_DT_RoomMaster"][map_doors[exit].room]["RoomType"] == "ERoomType::Load" and map_doors[exit].room[0:6] != room[0:6] and datatable["PB_DT_RoomMaster"][map_doors[exit].room]["SameRoom"] != "None":
                    if is_vanilla_start or map_doors[exit].room != "m02VIL_1200" and datatable["PB_DT_RoomMaster"][map_doors[exit].room]["SameRoom"] != "m03ENT_1200":
                        continue
                #The first entrance transition room is hardcoded to bring you back to the village regardless of its position on the canvas
                #Ignore that room and don't connect it to anything
                #Meanwhile the village version of that transition is always needed to trigger the curved effect of the following bridge room
                #So ignore any other transitions overlayed on top of it
                if not is_vanilla_start and (datatable["PB_DT_RoomMaster"][map_doors[exit].room]["SameRoom"] == "m02VIL_1200" or map_doors[exit].room == "m03ENT_1200"):
                    continue
                if not map_doors[exit].room in datatable["PB_DT_RoomMaster"][room]["AdjacentRoomName"]:
                    datatable["PB_DT_RoomMaster"][room]["AdjacentRoomName"].append(map_doors[exit].room)
            #Update door list
            if map_connections[room][entrance]:
                open_doors.append(map_doors[entrance])
        if not open_doors and datatable["PB_DT_RoomMaster"][room]["DoorFlag"]:
            datatable["PB_DT_RoomMaster"][room]["OutOfMap"] = True
        datatable["PB_DT_RoomMaster"][room]["DoorFlag"] = convert_door_to_flag(open_doors, datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"])
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

def update_default_outfit_hsv(parameter_string):
    parameter_list = []
    for index in range(len(parameter_string)//4):
        parameter_list.append(parameter_string[index*4:index*4 + 4])
    for index in range(6):
        for parameter in parameter_list:
            datatable["PB_DT_HairSalonOldDefaults"]["Body_01_" + "{:02d}".format(index + 1)][parameter[0] + "1"] = int(parameter[1:4])

def fix_bathin_left_entrance():
    #If Bathin's intro event triggers when the player entered the room from the left they will be stuck in an endless walk cycle
    #To fix this add a special door to warp the player in the room's player start instead
    for door in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = map_doors[door].room
        area_path = "ACT" + room[1:3] + "_" + room[3:6]
        new_file = UAsset(asset_dir + "\\" + file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version.VER_UE4_22)
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
        new_file.Exports[2].Data[0].Value[0].Value  = FVector(1260*datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"], 0, 720*map_doors[door].z_block + 360)
        new_file.Exports[2].Data[1].Value[0].Value  = FRotator(0, 0, 0)
        new_file.Exports[8].Data[0].Value = FName.FromString(new_file, room[3:])
        new_file.Exports[8].Data[1].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[2].Value = FName.FromString(new_file, "dummy")
        new_file.Exports[8].Data[3].Value = FName.FromString(new_file, "m13ARC_005")
        new_file.Write(mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")
    adjacent_room = None
    #Get Bathin's adjacent room while prioritizing the same area
    for door in map_connections["m13ARC_005"]["ARC_005_0_0_LEFT"]:
        room = map_doors[door].room
        adjacent_room = room
        if datatable["PB_DT_RoomMaster"][room]["AreaID"] == datatable["PB_DT_RoomMaster"]["m13ARC_005"]["AreaID"]:
            break
    #Add one more door in the boss room to have a proper transition
    if adjacent_room:
        room = "m13ARC_005"
        area_path = "ACT" + room[1:3] + "_" + room[3:6]
        new_file = UAsset(asset_dir + "\\" + file_to_path["m02VIL_012_RV"] + "\\m02VIL_012_RV.umap", UE4Version.VER_UE4_22)
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
    for index in [293, 294]:
        new_list = []
        count = 0
        for data in game_data["TitleExtraMenu"].Exports[index].Data[0].Value:
            if count != 2:
                new_list.append(data)
            count += 1
        game_data["TitleExtraMenu"].Exports[index].Data[0].Value = new_list
    stringtable["PBSystemStringTable"]["SYS_SEN_ModeRogueDungeon"] = "DELETED"
    stringtable["PBSystemStringTable"]["SYS_MSG_OpenRogueDungeonMode"] = "Story Mode completed."

def show_mod_stats(seed, mod_version):
    game_version = str(game_data["VersionNumber"].Exports[6].Data[0].CultureInvariantString)
    mod_stats = "Bloodstained " + game_version + "\r\nTrue Randomization v" + mod_version
    height = 0.4
    if seed:
        mod_stats += "\r\nSeed # " + seed
        height = 0.66
    for num in range(2):
        game_data["VersionNumber"].Exports[4 + num].Data[0].Value[2].Value[0].X = 19
        game_data["VersionNumber"].Exports[4 + num].Data[0].Value[2].Value[0].Y = height
        game_data["VersionNumber"].Exports[6 + num].Data[0].CultureInvariantString = FString(mod_stats)
        game_data["VersionNumber"].Exports[6 + num].Data[1].Value[2].Value = 16
        game_data["VersionNumber"].Exports[6 + num].Data[2].EnumValue = FName.FromString(game_data["VersionNumber"], "ETextJustify::Left")
        struct = struct = FloatPropertyData(FName.FromString(game_data["VersionNumber"], "LineHeightPercentage"))
        struct.Value = 0.6
        game_data["VersionNumber"].Exports[6 + num].Data.Add(struct)

def set_single_difficulty(difficulty):
    #Ensure that in game difficulty never mismatches the mod's
    new_list = []
    sub_struct = BytePropertyData()
    sub_struct.ByteType = BytePropertyType.FName
    sub_struct.EnumValue = FName.FromString(game_data["DifficultSelecter"], "EPBGameLevel::" + difficulty)
    new_list = [sub_struct]
    game_data["DifficultSelecter"].Exports[2].Data[1].Value = new_list

def set_default_entry_name(name):
    #Change the default in-game file name
    game_data["EntryNameSetter"].Exports[110].Data[0].CultureInvariantString = FString(name)
    game_data["EntryNameSetter"].Exports[110].Data[1].CultureInvariantString = FString(name)
    game_data["EntryNameSetter"].Exports[111].Data[2].CultureInvariantString = FString(name)
    game_data["EntryNameSetter"].Exports[111].Data[3].CultureInvariantString = FString(name)

def write_log(filename, log):
    with open("SpoilerLog\\" + filename + ".json", "w", encoding="utf8") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def write_files():
    #Dump all uasset objects to files
    for file in game_data:
        if file_to_type[file] == FileType.Level:
            extension = ".umap"
        else:
            extension = ".uasset"
        game_data[file].Write(mod_dir + "\\" + file_to_path[file] + "\\" + file.split("(")[0] + extension)

def remove_unchanged_files():
    #Since uasset objects cannot be compared successfully we need to compare the files after they've been written
    #That way unchanged files get removed from the pak
    for file in file_to_path:
        remove = True
        for sub_file in os.listdir(mod_dir + "\\" + file_to_path[file]):
            name, extension = os.path.splitext(sub_file)
            if name == file:
                if not filecmp.cmp(mod_dir + "\\" + file_to_path[file] + "\\" + sub_file, asset_dir + "\\" + file_to_path[file] + "\\" + sub_file, shallow=False):
                    remove = False
        if remove:
            for sub_file in os.listdir(mod_dir + "\\" + file_to_path[file]):
                name, extension = os.path.splitext(sub_file)
                if name == file:
                    os.remove(mod_dir + "\\" + file_to_path[file] + "\\" + sub_file)

def import_mesh(filename):
    #Import a mesh file at the right location by reading it in the file
    new_file = UAsset("Data\\Mesh\\" + filename + ".uasset", UE4Version.VER_UE4_22)
    name_map = new_file.GetNameMapIndexList()
    filepath = None
    for name in name_map:
        if str(name)[0] == "/" and str(name).split("/")[-1] == filename:
            filepath = str(name)[6:][:-(len(filename)+1)].replace("/", "\\")
            break
    if not filepath:
        raise Exception("Failed to obtain filepath of asset " + filename)
    if not os.path.isdir(mod_dir + "\\" + filepath):
        os.makedirs(mod_dir + "\\" + filepath)
    new_file.Write(mod_dir + "\\" + filepath + "\\" + filename + ".uasset")

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
    sub_struct.Value = FVector(room_width*2 + 240, 50, room_height*2 + 240)
    struct.Value.Add(sub_struct)
    game_data[filename].Exports[actor_index + 1].Data.Add(struct)
    #Keep it in mind to not update its container type
    global_room_pickups.append(drop_id)

def add_room_file(room):
    area_path = "ACT" + room[1:3] + "_" + room[3:6]
    new_file = UAsset(asset_dir + "\\" + file_to_path["m01SIP_1000_RV"] + "\\m01SIP_1000_RV.umap", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString(room + "_RV"))
    index = new_file.SearchNameReference(FString("/Game/Core/Environment/ACT01_SIP/Level/m01SIP_1000_RV"))
    new_file.SetNameReference(index, FString("/Game/Core/Environment/" + area_path + "/Level/" + room + "_RV"))
    new_file.Exports[5].Data[1].Value = FName.FromString(new_file, room)
    new_file.Write(mod_dir + "\\Core\\Environment\\" + area_path + "\\Level\\" + room + "_RV.umap")

def add_game_item(index, item_id, item_type, item_subtype, icon_coord, name, description, price, craftable):
    #Add a completely new item slot into the game
    if item_id in datatable["PB_DT_ItemMaster"]:
        raise Exception("Item already exists.")
    #Edit ItemMaster
    icon_path                                                              = (icon_coord[1]//128)*32 + icon_coord[0]//128
    datatable["PB_DT_ItemMaster"][item_id]                                 = copy.deepcopy(datatable["PB_DT_ItemMaster"]["Potion"])
    datatable["PB_DT_ItemMaster"][item_id]["IconPath"]                     = str(icon_path)
    datatable["PB_DT_ItemMaster"][item_id]["NameStrKey"]                   = "ITEM_NAME_" + item_id
    datatable["PB_DT_ItemMaster"][item_id]["DescriptionStrKey"]            = "ITEM_EXPLAIN_" + item_id
    datatable["PB_DT_ItemMaster"][item_id]["buyPrice"]                     = price
    if 0 < price < 100:                                                    
        datatable["PB_DT_ItemMaster"][item_id]["sellPrice"]                = 1
    else:                                                                  
        datatable["PB_DT_ItemMaster"][item_id]["sellPrice"]                = price//10
    datatable["PB_DT_ItemMaster"][item_id]["Producted"]                    = "None"
    #Edit string entries                                                   
    stringtable["PBMasterStringTable"]["ITEM_NAME_" + item_id]             = name
    stringtable["PBMasterStringTable"]["ITEM_EXPLAIN_" + item_id]          = description
    #Edit case by case properties                                          
    if item_type == "Accessory":                                                
        datatable["PB_DT_ItemMaster"][item_id]["ItemType"]                 = "ECarriedCatalog::Accessory1"
        datatable["PB_DT_ItemMaster"][item_id]["max"]                      = 99
        datatable["PB_DT_ItemMaster"][item_id]["CarryToBossRushMode"]      = True
        datatable["PB_DT_ArmorMaster"][item_id]                            = copy.deepcopy(datatable["PB_DT_ArmorMaster"]["EmptyAccesory"])
        datatable["PB_DT_ArmorMaster"][item_id]["AttachPoint"]             = "EWeaponAttachPoint::None"
        datatable["PB_DT_ArmorMaster"][item_id]["Category"]                = item_subtype
        if craftable:
            datatable["PB_DT_CraftMaster"][item_id]                        = copy.deepcopy(datatable["PB_DT_CraftMaster"]["Ring"])
            datatable["PB_DT_CraftMaster"][item_id]["CraftItemId"]         = item_id
        datatable_entry_index["PB_DT_ArmorMaster"][item_id]                = index
    if item_type == "Armor":                                                  
        datatable["PB_DT_ItemMaster"][item_id]["ItemType"]                 = "ECarriedCatalog::Body"
        datatable["PB_DT_ItemMaster"][item_id]["max"]                      = 99
        datatable["PB_DT_ItemMaster"][item_id]["CarryToBossRushMode"]      = True
        datatable["PB_DT_ArmorMaster"][item_id]                            = copy.deepcopy(datatable["PB_DT_ArmorMaster"]["EmptyBody"])
        datatable["PB_DT_ArmorMaster"][item_id]["AttachPoint"]             = "EWeaponAttachPoint::None"
        datatable["PB_DT_ArmorMaster"][item_id]["Category"]                = item_subtype
        if craftable:
            datatable["PB_DT_CraftMaster"][item_id]                        = copy.deepcopy(datatable["PB_DT_CraftMaster"]["Tunic"])
            datatable["PB_DT_CraftMaster"][item_id]["CraftItemId"]         = item_id
        datatable_entry_index["PB_DT_ArmorMaster"][item_id]                = index
    if item_type == "Bullet":                                                 
        datatable["PB_DT_ItemMaster"][item_id]["ItemType"]                 = "ECarriedCatalog::Bullet"
        datatable["PB_DT_ItemMaster"][item_id]["max"]                      = 999
        datatable["PB_DT_ItemMaster"][item_id]["CarryToBossRushMode"]      = True
        datatable["PB_DT_AmmunitionMaster"][item_id]                       = copy.deepcopy(datatable["PB_DT_AmmunitionMaster"]["Softpoint"])
        datatable["PB_DT_AmmunitionMaster"][item_id]["BulletID"]           = item_id
        if craftable:
            datatable["PB_DT_CraftMaster"][item_id]                        = copy.deepcopy(datatable["PB_DT_CraftMaster"]["Softpoint"])
            datatable["PB_DT_CraftMaster"][item_id]["CraftItemId"]         = item_id
        if not item_id in datatable["PB_DT_BulletMaster"]:                 
            datatable["PB_DT_BulletMaster"][item_id]                       = copy.deepcopy(datatable["PB_DT_BulletMaster"]["Softpoint"])
            datatable["PB_DT_BulletMaster"][item_id]["DamageId"]           = item_id
        if not item_id in datatable["PB_DT_CollisionMaster"]:              
            datatable["PB_DT_CollisionMaster"][item_id]                    = copy.deepcopy(datatable["PB_DT_CollisionMaster"]["Softpoint"])
            datatable["PB_DT_CollisionMaster"][item_id + "_EX"]            = copy.deepcopy(datatable["PB_DT_CollisionMaster"]["Softpoint_EX"])
        if not item_id in datatable["PB_DT_DamageMaster"]:                 
            datatable["PB_DT_DamageMaster"][item_id]                       = copy.deepcopy(datatable["PB_DT_DamageMaster"]["Softpoint"])
            datatable["PB_DT_DamageMaster"][item_id + "_EX"]               = copy.deepcopy(datatable["PB_DT_DamageMaster"]["Softpoint_EX"])
            datatable["PB_DT_DamageMaster"][item_id + "_EX2"]              = copy.deepcopy(datatable["PB_DT_DamageMaster"]["Softpoint_EX2"])
        datatable_entry_index["PB_DT_AmmunitionMaster"][item_id]           = index
    if item_type == "Potion":                                                 
        datatable["PB_DT_ItemMaster"][item_id]["ItemType"]                 = "ECarriedCatalog::Potion"
        datatable["PB_DT_ItemMaster"][item_id]["max"]                      = 9
        datatable["PB_DT_ConsumableMaster"][item_id]                       = copy.deepcopy(datatable["PB_DT_ConsumableMaster"]["Potion"])
        datatable["PB_DT_ConsumableMaster"][item_id]["SpecialEffectId"]    = item_id
        datatable["PB_DT_SpecialEffectDefinitionMaster"][item_id]          = copy.deepcopy(datatable["PB_DT_SpecialEffectDefinitionMaster"]["Potion"])
        datatable["PB_DT_SpecialEffectDefinitionMaster"][item_id]["DefId"] = item_id
        datatable["PB_DT_SpecialEffectGroupMaster"][item_id]               = copy.deepcopy(datatable["PB_DT_SpecialEffectGroupMaster"]["Potion"])
        datatable["PB_DT_SpecialEffectGroupMaster"][item_id]["GroupId"]    = item_id
        datatable["PB_DT_SpecialEffectGroupMaster"][item_id]["DefId"]      = item_id
        datatable["PB_DT_SpecialEffectMaster"][item_id]                    = copy.deepcopy(datatable["PB_DT_SpecialEffectMaster"]["Potion"])
        datatable["PB_DT_SpecialEffectMaster"][item_id]["Id"]              = item_id
        datatable["PB_DT_SpecialEffectMaster"][item_id]["GroupId"]         = item_id
        if craftable:
            datatable["PB_DT_CraftMaster"][item_id]                        = copy.deepcopy(datatable["PB_DT_CraftMaster"]["Potion"])
            datatable["PB_DT_CraftMaster"][item_id]["CraftItemId"]         = item_id
        datatable_entry_index["PB_DT_ConsumableMaster"][item_id]           = index

def add_armor_reference(armor_id):
    #Give a specific armor its own graphical asset pointer when equipped
    datatable["PB_DT_ArmorMaster"][armor_id]["ReferencePath"] = "/Game/Core/Item/Body/BDBP_" + armor_id + ".BDBP_" + armor_id
    new_file = UAsset(asset_dir + "\\" + file_to_path["BDBP_BodyValkyrie"] + "\\BDBP_BodyValkyrie.uasset", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("BDBP_BodyValkyrie_C"))
    new_file.SetNameReference(index, FString("BDBP_" + armor_id + "_C"))
    index = new_file.SearchNameReference(FString("Default__BDBP_BodyValkyrie_C"))
    new_file.SetNameReference(index, FString("Default__BDBP_" + armor_id + "_C"))
    default_body_mat          = mod_data["ArmorReference"][armor_id]["DefaultBodyMat"]         + "." + mod_data["ArmorReference"][armor_id]["DefaultBodyMat"].split("/")[-1]
    chroma_body_mat           = mod_data["ArmorReference"][armor_id]["ChromaBodyMat"]          + "." + mod_data["ArmorReference"][armor_id]["ChromaBodyMat"].split("/")[-1]
    default_skin_mat          = mod_data["ArmorReference"][armor_id]["DefaultSkinMat"]         + "." + mod_data["ArmorReference"][armor_id]["DefaultSkinMat"].split("/")[-1]
    chroma_skin_mat           = mod_data["ArmorReference"][armor_id]["ChromaSkinMat"]          + "." + mod_data["ArmorReference"][armor_id]["ChromaSkinMat"].split("/")[-1]
    dialogue_default_skin_mat = mod_data["ArmorReference"][armor_id]["DialogueDefaultSkinMat"] + "." + mod_data["ArmorReference"][armor_id]["DialogueDefaultSkinMat"].split("/")[-1]
    dialogue_chroma_skin_mat  = mod_data["ArmorReference"][armor_id]["DialogueChromaSkinMat"]  + "." + mod_data["ArmorReference"][armor_id]["DialogueChromaSkinMat"].split("/")[-1]
    new_file.Imports[18].ObjectName            = FName.FromString(new_file, mod_data["ArmorReference"][armor_id]["Mesh"])
    new_file.Imports[27].ObjectName            = FName.FromString(new_file, mod_data["ArmorReference"][armor_id]["Mesh"].split("/")[-1])
    new_file.Exports[1].Data[0].Value[0].Value = FName.FromString(new_file, chroma_body_mat)
    new_file.Exports[1].Data[1].Value[0].Value = FName.FromString(new_file, default_body_mat)
    new_file.Exports[1].Data[2].Value          = FName.FromString(new_file, chroma_skin_mat)
    new_list = []
    sub_struct = SoftObjectPropertyData()
    sub_struct.Value                           = FName.FromString(new_file, default_skin_mat)
    new_list = [sub_struct]
    new_file.Exports[1].Data[3].Value          = new_list
    new_file.Exports[1].Data[4].Value          = FName.FromString(new_file, dialogue_chroma_skin_mat)
    new_file.Exports[1].Data[5].Value          = FName.FromString(new_file, dialogue_default_skin_mat)
    new_file.Exports[1].Data[7].Value          = False
    new_file.Exports[1].Data[8].Value          = 1
    new_file.Exports[1].Data[9].Value          = 0
    new_file.Write(mod_dir + "\\" + file_to_path["BDBP_BodyValkyrie"] + "\\BDBP_" + armor_id + ".uasset")

def add_music_file(filename):
    #Check if the filename is valid
    if len(filename.split("_")) != 2:
        raise TypeError("Invalid music name: " + filename)
    if len(filename.split("_")[0]) != 5 or len(filename.split("_")[-1]) != 3:
        raise TypeError("Invalid music name: " + filename)
    if filename[0:3] != "ACT":
        raise TypeError("Invalid music name: " + filename)
    try:
        int(filename[3:5])
    except ValueError:
        raise TypeError("Invalid music name: " + filename)
    #Copy the awb and import the new music in it
    filesize = None
    with open(asset_dir + "\\" + file_to_path["ACT50_BRM"] + "\\ACT50_BRM.awb", "rb") as inputfile, open(mod_dir + "\\" + file_to_path["ACT50_BRM"] + "\\" + filename + ".awb", "wb") as outfile:
        offset = inputfile.read().find(str.encode("HCA"))
        inputfile.seek(0)
        outfile.write(inputfile.read(offset))
        with open("Data\\Music\\" + filename + ".hca", "rb") as hca:
            outfile.write(hca.read())
        outfile.seek(0, os.SEEK_END)
        filesize = outfile.tell()
        outfile.seek(0x16)
        outfile.write(filesize.to_bytes(4, "little"))
    #Add the music pointer in soundmaster
    music_id = "BGM_m" + filename[3:5] + filename.split("_")[-1]
    datatable["PB_DT_SoundMaster"][music_id] = copy.deepcopy(datatable["PB_DT_SoundMaster"]["BGM_m50BRM"])
    datatable["PB_DT_SoundMaster"][music_id]["AssetPath"] = datatable["PB_DT_SoundMaster"][music_id]["AssetPath"].replace("BGM_m50BRM", music_id)
    #Copy the act file
    new_file = UAsset(asset_dir + "\\" + file_to_path["ACT50_BRM"] + "\\ACT50_BRM.uasset", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("ACT50_BRM"))
    new_file.SetNameReference(index, FString(filename))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/ACT50_BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + filename))
    new_file.Exports[0].Data[0].Value = FString(filename)
    string = "{:02x}".format(int.from_bytes(str.encode(filename), "big"))
    for num in range(int(len(string)/2)):
        new_file.Exports[0].Extras[0x662 + num] = int(string[num*2] + string[num*2 + 1], 16)
        new_file.Exports[0].Extras[0xE82 + num] = int(string[num*2] + string[num*2 + 1], 16)
    string = "{:02x}".format(int.from_bytes(str.encode(music_id), "big"))
    for num in range(int(len(string)/2)):
        new_file.Exports[0].Extras[0x7E1 + num] = int(string[num*2] + string[num*2 + 1], 16)
    string = "{:08x}".format(filesize)
    count = 0
    for num in range(int(len(string)/2) -1, -1, -1):
        new_file.Exports[0].Extras[0x1A32 + count] = int(string[num*2] + string[num*2 + 1], 16)
        count += 1
    new_file.Write(mod_dir + "\\" + file_to_path["ACT50_BRM"] + "\\" + filename + ".uasset")
    #Copy the bgm file
    new_file = UAsset(asset_dir + "\\" + file_to_path["BGM_m50BRM"] + "\\BGM_m50BRM.uasset", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("ACT50_BRM"))
    new_file.SetNameReference(index, FString(filename))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/ACT50_BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + filename))
    index = new_file.SearchNameReference(FString("BGM_m50BRM"))
    new_file.SetNameReference(index, FString(music_id))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/BGM_m50BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + music_id))
    new_file.Exports[0].Data[1].Value = FString(music_id)
    new_file.Exports[0].Data[2].Value = 300.0
    new_file.Write(mod_dir + "\\" + file_to_path["BGM_m50BRM"] + "\\" + music_id + ".uasset")

def add_level_actor(filename, actor_class, location, rotation, scale, properties):
    actor_index = len(game_data[filename].Exports)
    #Name the new actor based on the class
    short_class = actor_class.replace(")", "").split("(")[0]
    short_class = short_class.split("_")
    if short_class[-1] == "C":
        short_class.pop()
    short_class = "_".join(short_class)
    actor_name = custom_actor_prefix + short_class
    snippet = UAssetSnippet(game_data[mod_data["ActorPointer"][actor_class]["File"]], mod_data["ActorPointer"][actor_class]["Index"])
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
            data.Value = FString(remove_inst_number(actor_name))
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
    if file_to_type[filename] != FileType.Level:
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
        level_index = export_name_to_index(filename, "PersistentLevel")
        game_data[filename].Exports[export_index].OuterIndex = FPackageIndex(0)
        game_data[filename].Exports[level_index].IndexData.Remove(export_index + 1)
        game_data[filename].Exports[level_index].CreateBeforeSerializationDependencies.Remove(FPackageIndex(export_index + 1))

def remove_level_class(filename, class_name):
    #Remove all actors of class in a level
    for export_index in range(len(game_data[filename].Exports)):
        if str(game_data[filename].Imports[abs(int(str(game_data[filename].Exports[export_index].ClassIndex))) - 1].ObjectName) == class_name:
            remove_level_actor(filename, export_index)

def set_material_hsv(filename, parameter, new_hsv):
    #Change a vector color in a material file
    #Here we use hsv as a base as it is easier to work with
    if file_to_type[filename] != FileType.Material:
        raise TypeError("Input is not a material file")
    #Some color properties are not parsed by UAssetAPI and end up in extra data
    #Hex edit in that case
    if filename in material_to_offset:
        for offset in material_to_offset[filename]:
            #Check if given offset is valid
            string = ""
            for num in range(12):
                string += "{:02x}".format(game_data[filename].Exports[0].Extras[offset + num]).upper()
            if string != "0000000000000002FFFFFFFF":
                raise Exception("Material offset invalid")
            #Get rgb
            rgb = []
            for num in range(3):
                list = []
                for index in range(4):
                    list.insert(0, "{:02x}".format(game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index]).upper())
                string = ""
                for index in list:
                    string += index
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
            for num in range(3):
                string = "{:08x}".format(struct.unpack("<I", struct.pack("<f", rgb[num]))[0]).upper()
                list = []
                for index in range(0, len(string), 2):
                    list.insert(0, string[index] + string[index + 1])
                for index in range(4):
                    game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index] = int(list[index], 16)
    #Otherwise change color through the exports
    else:
        for data in game_data[filename].Exports[0].Data:
            if str(data.Name) == "VectorParameterValues":
                for sub_data in data.Value:
                    if str(sub_data.Value[0].Value[0].Value) == parameter:
                        rgb = []
                        rgb.append(sub_data.Value[1].Value[0].Value.R)
                        rgb.append(sub_data.Value[1].Value[0].Value.G)
                        rgb.append(sub_data.Value[1].Value[0].Value.B)
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
                        sub_data.Value[1].Value[0].Value.R = rgb[0]
                        sub_data.Value[1].Value[0].Value.G = rgb[1]
                        sub_data.Value[1].Value[0].Value.B = rgb[2]

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
    if left_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP)
    elif bottom_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_horizontal_check(room_1, room_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT)
    elif right_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
        door_vertical_check(room_1, room_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP)
    elif top_room_check(datatable["PB_DT_RoomMaster"][room_1], datatable["PB_DT_RoomMaster"][room_2]):
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
        if map_doors[door_1].direction_part == direction_1:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_1] and map_doors[door_1].z_block == (map_doors[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)
        elif map_doors[door_1].direction_part == direction_2:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_2] and map_doors[door_1].z_block == (map_doors[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)
        elif map_doors[door_1].direction_part == direction_3:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_3] and map_doors[door_1].z_block == (map_doors[door_2].z_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetZ"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetZ"])/7.2)):
                    map_connections[room_1][door_1].append(door_2)

def door_horizontal_check(room_1, room_2, direction_1, direction_2, direction_3):
    for door_1 in map_connections[room_1]:
        if map_doors[door_1].direction_part == direction_1:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_1] and map_doors[door_1].x_block == (map_doors[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)
        elif map_doors[door_1].direction_part == direction_2:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_2] and map_doors[door_1].x_block == (map_doors[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)
        elif map_doors[door_1].direction_part == direction_3:
            for door_2 in map_connections[room_2]:
                if map_doors[door_2].direction_part == OppositeDirection[direction_3] and map_doors[door_1].x_block == (map_doors[door_2].x_block + round((datatable["PB_DT_RoomMaster"][room_2]["OffsetX"] - datatable["PB_DT_RoomMaster"][room_1]["OffsetX"])/12.6)):
                    map_connections[room_1][door_1].append(door_2)

def remove_inst_number(name):
    #Return a string without its instance number the same way Unreal does it
    name = name.split("_")
    if name[-1][0] != "0":
        try:
            int(name[-1])
            name.pop()
        except ValueError:
            pass
    return "_".join(name)

def export_name_to_index(filename, export_name):
    count = 0
    for export in game_data[filename].Exports:
        if str(export.ObjectName) == export_name:
            return count
        count += 1
    raise Exception("Export not found")

def get_gimmick_filename(room):
    if room in room_to_gimmick:
        return room_to_gimmick[room]
    else:
        return room + "_Gimmick"

def is_enemy(character):
    if is_main_enemy(character):
        return True
    if character[0:5] in mod_data["EnemyInfo"]:
        return list(datatable["PB_DT_CharacterParameterMaster"]).index("P0007") < list(datatable["PB_DT_CharacterParameterMaster"]).index(character) < list(datatable["PB_DT_CharacterParameterMaster"]).index("SubChar")
    return is_final_boss(character)

def is_main_enemy(character):
    return character in mod_data["EnemyInfo"]

def is_boss(character):
    if is_enemy(character):
        return datatable["PB_DT_CharacterParameterMaster"][character]["IsBoss"] and character != "N2008_BOSS" or character[0:5] in ["N3106", "N3107", "N3108"]
    return False

def is_final_boss(character):
    return character[0:5] in ["N1009", "N1013"]

def add_enemy_to_archive(entry_index, enemy_id, area_ids, package_path, copy_from):
    last_id = int(list(datatable["PB_DT_ArchiveEnemyMaster"])[-1].split("_")[-1])
    entry_id = "Enemy_" + "{:03d}".format(last_id + 1)
    for entry in datatable["PB_DT_ArchiveEnemyMaster"]:
        if datatable["PB_DT_ArchiveEnemyMaster"][entry]["UniqueID"] == copy_from:
            new_entry = copy.deepcopy(datatable["PB_DT_ArchiveEnemyMaster"][entry])
            break
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id] = new_entry
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["UniqueID"] = enemy_id
    for index in range(4):
        datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["Area" + str(index + 1)] = "None"
    for index in range(len(area_ids)):
        datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["Area" + str(index + 1)] = area_ids[index]
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["AreaInputPath"] = package_path
    datatable_entry_index["PB_DT_ArchiveEnemyMaster"][entry_id] = entry_index

def append_string_entry(file, entry, text):
    #Make sure the text never exceeds two lines
    if "\r\n" in stringtable[file][entry] or len(stringtable[file][entry]) > 60 or entry in string_entry_exceptions:
        prefix = " "
    else:
        prefix = "\r\n"
    stringtable[file][entry] += prefix + text

def get_available_gimmick_flag():
    index = -1
    while abs(index) <= len(datatable["PB_DT_GimmickFlagMaster"]):
        dict = datatable["PB_DT_GimmickFlagMaster"][list(datatable["PB_DT_GimmickFlagMaster"])[index]]
        if "Id" in dict:
            return dict["Id"] + 1
        index -= 1
    return 1