import Manager
import math
import random
import os
import copy

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
        "JRN": "m20"
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
    global chest_to_requirement
    chest_to_requirement = {
        "Treasurebox_PureMiriam_Hair":  ["HighJump", "Invert"],
        "Treasurebox_SIP014_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Wall_SIP014_1":                ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_VIL006_4":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_GDN006_1":         ["Dimensionshift"],
        "Treasurebox_GDN013_1":         ["Invert", "Dimensionshift"],
        "Treasurebox_SAN003_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN003_8":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN015_2":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN015_3":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN016_3":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN016_4":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN019_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN019_2":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN021_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_SAN021_5":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_KNG018_4":         ["HighJump", "Invert", "Dimensionshift"],
        "Treasurebox_KNG021_1":         ["Doublejump"],
        "Treasurebox_LIB009_1":         ["HighJump", "Invert"],
        "Treasurebox_LIB009_2":         ["HighJump", "Invert"],
        "Treasurebox_LIB012_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_LIB022_1":         ["Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_TWR005_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_TWR018_2":         ["Doublejump", "HighJump", "Invert"],
        "Treasurebox_TWR018_6":         ["Doublejump", "HighJump", "Invert"],
        "Treasurebox_PureMiriam_Sword": ["Dimensionshift"],
        "Treasurebox_PureMiriam_Dress": ["HighJump", "Invert"],
        "Treasurebox_TRN002_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_TRN002_2":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_TRN002_3":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_BIG012_2":         ["HighJump", "Invert", "Dimensionshift"],
        "Treasurebox_UGD005_1":         ["Deepsinker"],
        "Treasurebox_UGD005_2":         ["Deepsinker"],
        "Treasurebox_UGD009_2":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_UGD021_1":         ["Deepsinker"],
        "Treasurebox_UGD024_1":         ["Deepsinker"],
        "Treasurebox_UGD024_2":         ["Deepsinker"],
        "Treasurebox_UGD024_3":         ["Deepsinker"],
        "Treasurebox_UGD025_1":         ["Deepsinker"],
        "Treasurebox_UGD025_2":         [["Deepsinker", "Dimensionshift", "Reflectionray"]],
        "Treasurebox_UGD025_3":         ["Deepsinker"],
        "Wall_UGD031_1":                ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_UGD036_1":         ["Deepsinker"],
        "Treasurebox_UGD040_1":         ["Deepsinker"],
        "Treasurebox_UGD042_1":         ["Deepsinker"],
        "Treasurebox_UGD044_1":         ["Deepsinker"],
        "Treasurebox_UGD044_2":         ["Deepsinker"],
        "Treasurebox_UGD046_2":         ["Deepsinker"],
        "Treasurebox_SND006_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_SND017_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_ARC006_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_TAR006_1":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_JPN002_1":         ["Dimensionshift"],
        "Treasurebox_RVA001_1":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_RVA001_2":         ["Dimensionshift", ["Invert", "Reflectionray"]],
        "Treasurebox_RVA011_1":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_RVA011_2":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_RVA012_1":         ["Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_ICE001_2":         ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_ICE008_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_JRN001_1":         ["Dimensionshift", "Reflectionray"],
        "Treasurebox_JRN001_2":         ["HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "Treasurebox_JRN001_3":         ["HighJump", "Invert", "Dimensionshift"]
    }
    global enemy_to_requirement
    enemy_to_requirement = {
        "N1008":      ["Invert", "Dimensionshift", "Reflectionray"],
        "N2006":      ["Doublejump", "HighJump", "Invert", "Dimensionshift", "Reflectionray"],
        "N2015":      ["Doublejump"],
        "Deepsinker": ["Doublejump", "HighJump", "Invert"]
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
    key_shards = [
        "Doublejump",
        "HighJump",
        "Invert",
        "Deepsinker",
        "Dimensionshift",
        "Reflectionray",
        "Aquastream",
        "Demoniccapture",
        "Bloodsteel"
    ]
    global key_item_to_location
    key_item_to_location = {}
    global key_shard_to_location
    key_shard_to_location = {}
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

def unused_room_check():
    #On custom maps certain rooms can end up unused and thus inaccessible
    #Remove them from the logic so that key items can never end up in there
    for i in list(Manager.mod_data["MapLogic"]):
        if Manager.datatable["PB_DT_RoomMaster"][i]["Unused"]:
            del Manager.mod_data["MapLogic"][i]

def extra_logic():
    #8 Bit Nightmare is always gonna be connected to Hall of Termination regardless of the map
    #So create its entry manually
    Manager.mod_data["MapLogic"]["m51EBT_000"] = {}
    Manager.mod_data["MapLogic"]["m51EBT_000"]["GateRoom"]             = False
    if Manager.mod_data["MapLogic"]["m06KNG_021"]["GateRoom"]:
        Manager.mod_data["MapLogic"]["m51EBT_000"]["NearestGate"]      = ["m06KNG_021"]
    else:
        Manager.mod_data["MapLogic"]["m51EBT_000"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["MapLogic"]["m06KNG_021"]["NearestGate"])
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Doublejump"]           = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["HighJump"]             = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Invert"]               = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Deepsinker"]           = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Dimensionshift"]       = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Reflectionray"]        = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Aquastream"]           = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Demoniccapture"]       = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Bloodsteel"]           = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Swordsman"]            = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Silverbromide"]        = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker1"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker2"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker3"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker4"]         = False
    #Add Crown of Creation to the logic manually
    for i in Manager.mod_data["MapLogic"]:
        Manager.mod_data["MapLogic"][i]["MonarchCrown"] = False
    #Kingdom 2 Crown is always connected to the train
    Manager.mod_data["MapLogic"]["m19K2C_000"] = {}
    Manager.mod_data["MapLogic"]["m19K2C_000"]["GateRoom"] = True
    if Manager.mod_data["MapLogic"]["m09TRN_002"]["GateRoom"]:
        Manager.mod_data["MapLogic"]["m19K2C_000"]["NearestGate"]      = ["m09TRN_002"]
    else:
        Manager.mod_data["MapLogic"]["m19K2C_000"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["MapLogic"]["m09TRN_002"]["NearestGate"])
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Doublejump"]           = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["HighJump"]             = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Invert"]               = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Deepsinker"]           = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Dimensionshift"]       = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Reflectionray"]        = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Aquastream"]           = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Demoniccapture"]       = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Bloodsteel"]           = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Swordsman"]            = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Silverbromide"]        = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker1"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker2"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker3"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker4"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["MonarchCrown"]         = True
    #Journey is always connected to the desert
    Manager.mod_data["MapLogic"]["m20JRN_000"] = {}
    Manager.mod_data["MapLogic"]["m20JRN_000"]["GateRoom"]             = True
    Manager.mod_data["MapLogic"]["m20JRN_000"]["NearestGate"]          = []
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Doublejump"]           = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["HighJump"]             = True
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Invert"]               = True
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Deepsinker"]           = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Dimensionshift"]       = True
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Reflectionray"]        = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Aquastream"]           = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Demoniccapture"]       = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Bloodsteel"]           = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Swordsman"]            = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Silverbromide"]        = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Keyofbacker1"]         = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Keyofbacker2"]         = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Keyofbacker3"]         = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["Keyofbacker4"]         = False
    Manager.mod_data["MapLogic"]["m20JRN_000"]["MonarchCrown"]         = False
    for i in range(4):
        room_name = "m20JRN_00" + str(i + 1)
        Manager.mod_data["MapLogic"][room_name] = {}
        Manager.mod_data["MapLogic"][room_name]["GateRoom"]             = False
        Manager.mod_data["MapLogic"][room_name]["NearestGate"]          = ["m20JRN_000"]
        Manager.mod_data["MapLogic"][room_name]["Doublejump"]           = False
        Manager.mod_data["MapLogic"][room_name]["HighJump"]             = False
        Manager.mod_data["MapLogic"][room_name]["Invert"]               = False
        Manager.mod_data["MapLogic"][room_name]["Deepsinker"]           = False
        Manager.mod_data["MapLogic"][room_name]["Dimensionshift"]       = False
        Manager.mod_data["MapLogic"][room_name]["Reflectionray"]        = False
        Manager.mod_data["MapLogic"][room_name]["Aquastream"]           = False
        Manager.mod_data["MapLogic"][room_name]["Demoniccapture"]       = False
        Manager.mod_data["MapLogic"][room_name]["Bloodsteel"]           = False
        Manager.mod_data["MapLogic"][room_name]["Swordsman"]            = False
        Manager.mod_data["MapLogic"][room_name]["Silverbromide"]        = False
        Manager.mod_data["MapLogic"][room_name]["BreastplateofAguilar"] = False
        Manager.mod_data["MapLogic"][room_name]["Keyofbacker1"]         = False
        Manager.mod_data["MapLogic"][room_name]["Keyofbacker2"]         = False
        Manager.mod_data["MapLogic"][room_name]["Keyofbacker3"]         = False
        Manager.mod_data["MapLogic"][room_name]["Keyofbacker4"]         = False
        Manager.mod_data["MapLogic"][room_name]["MonarchCrown"]         = False

def hard_enemy_logic():
    #On hard mode some rooms have extra enemies so update the location info
    for i in Manager.mod_data["EnemyLocation"]:
        Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"].extend(Manager.mod_data["EnemyLocation"][i]["HardModeRooms"])
    #Dulla heads can also be replaced with maledictions so adapt for that
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m07LIB_029")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_005")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_013")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m11UGD_013")
    #Some of Ultimate Zangetsu's new attacks need some movement to be avoided
    chest_to_requirement["Swordsman"] = ["Doublejump", "Invert", "Dimensionshift"]

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

def key_logic():
    #Place all key items with logic so that the game is always beatable
    #The strategy used here is similar to the one implemented in vanilla where it reads from a room check file and loops through all the rooms based on that
    #The logic starts in all rooms that have no requirements until a gate is reached to determine which key item to place and so on
    #Since this has to adapt to different map layouts we cannot get away with using any "cheats" that are specific to the default map
    previous_gate = []
    requirement_to_gate = {}
    #Filling list with all room names
    all_rooms = []
    for i in Manager.mod_data["MapLogic"]:
        ratio = room_to_ratio(i)
        for e in range(ratio):
            all_rooms.append(i)
    #Loop through all keys until they've all been assigned
    while all_keys:
        #Reset lists and dicts
        requirement = []
        for i in key_items:
            requirement_to_gate[i] = []
        for i in key_shards:
            requirement_to_gate[i] = []
        previous_room = []
        #Gathering upcoming gate requirements
        for i in Manager.mod_data["MapLogic"]:
            if Manager.mod_data["MapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.mod_data["MapLogic"][i]["NearestGate"]) and not i in previous_gate:
                #If Zangetsuto gate then check if garden portal and Gebel room are accessible
                if Manager.mod_data["MapLogic"][i]["Swordsman"] and not zangetsuto_gate_avaliable(previous_gate):
                    continue
                #If Journey area then check if desert room and post portal are accessible
                if i == "m20JRN_000" and not journey_area_available(previous_gate):
                    continue
                for e in key_items:
                    if Manager.mod_data["MapLogic"][i][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
                for e in key_shards:
                    if Manager.mod_data["MapLogic"][i][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
        #Check if requirement isnt already satisfied
        check = False
        for i in key_item_to_location:
            if i in requirement:
                check = True
                previous_gate.extend(requirement_to_gate[i])
        for i in key_shard_to_location:
            if i in requirement:
                check = True
                previous_gate.extend(requirement_to_gate[i])
        if check:
            continue
        #Gathering rooms available before gate
        for i in Manager.mod_data["MapLogic"]:
            if not Manager.mod_data["MapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.mod_data["MapLogic"][i]["NearestGate"]) or i in previous_gate:
                #If it's OD's room then don't unlock it until all requirements are lifted
                if i == "m18ICE_004":
                    continue
                #Get ratio
                ratio = room_to_ratio(i)
                for e in range(ratio):
                    previous_room.append(i)
        #Choosing key item based on requirements
        chosen_item = random.choice(all_keys)
        if requirement:
            while chosen_item not in requirement:
                chosen_item = random.choice(all_keys)
            logic_choice(chosen_item, previous_room)
        else:
            logic_choice(chosen_item, all_rooms)
        #Update previous gate
        previous_gate.extend(requirement_to_gate[chosen_item])

def zangetsuto_gate_avaliable(previous_gate):
    if Manager.mod_data["MapLogic"]["m04GDN_001"]["GateRoom"]:
        nearest_gate_1 = ["m04GDN_001"]
    else:
        nearest_gate_1 = copy.deepcopy(Manager.mod_data["MapLogic"]["m04GDN_001"]["NearestGate"])
    if Manager.mod_data["MapLogic"]["m06KNG_020"]["GateRoom"]:
        nearest_gate_2 = ["m06KNG_020"]
    else:
        nearest_gate_2 = copy.deepcopy(Manager.mod_data["MapLogic"]["m06KNG_020"]["NearestGate"])
    if previous_in_nearest(previous_gate, nearest_gate_1) and previous_in_nearest(previous_gate, nearest_gate_2):
        return True
    return False

def journey_area_available(previous_gate):
    if Manager.mod_data["MapLogic"]["m10BIG_000"]["GateRoom"]:
        nearest_gate_1 = ["m10BIG_000"]
    else:
        nearest_gate_1 = copy.deepcopy(Manager.mod_data["MapLogic"]["m10BIG_000"]["NearestGate"])
    if Manager.mod_data["MapLogic"]["m12SND_025"]["GateRoom"]:
        nearest_gate_2 = ["m12SND_025"]
    else:
        nearest_gate_2 = copy.deepcopy(Manager.mod_data["MapLogic"]["m12SND_025"]["NearestGate"])
    if previous_in_nearest(previous_gate, nearest_gate_1) and previous_in_nearest(previous_gate, nearest_gate_2):
        return True
    return False

def previous_in_nearest(previous_gate, nearest_gate):
    if not nearest_gate:
        return True
    for i in previous_gate:
        if i in nearest_gate:
            return True
    return False

def room_to_ratio(room):
    #Increasing chances of late rooms
    #Otherwise early game areas are more likely to have everything
    ratio = 1
    gate_list = copy.deepcopy(Manager.mod_data["MapLogic"][room]["NearestGate"])
    while gate_list:
        nearest_gate = random.choice(gate_list)
        for i in Manager.mod_data["MapLogic"]:
            if i == nearest_gate:
                ratio *= 2
                gate_list = copy.deepcopy(Manager.mod_data["MapLogic"][i]["NearestGate"])
                break
    #Increasing chances of boss rooms
    #Otherwise bosses and special enemies have low chances of being required
    if room in boss_rooms:
        ratio *= 10
    return ratio

def chest_to_room(chest):
    if chest in special_chest_to_room:
        return special_chest_to_room[chest]
    else:
        return room_to_area[chest.split("_")[1].split("(")[0][:3]] + chest.split("_")[1].split("(")[0][:3] + "_" + chest.split("_")[1].split("(")[0][3:]

def enemy_to_room(enemy):
    return Manager.mod_data["EnemyLocation"][enemy]["NormalModeRooms"]

def logic_choice(chosen_item, room_list):
    #Removing key from list
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)
    #Choosing room to place item in
    while True:
        chosen_room = random.choice(room_list)
        #Choosing container to place item in
        if chosen_item in key_items:
            chest_list = room_to_available_chests(chosen_room)
            if chest_list:
                key_item_to_location[chosen_item] = random.choice(chest_list)
                #If it is a boss room then remove it from the priority
                if chosen_room in boss_rooms:
                    boss_rooms.remove(chosen_room)
                break
        if chosen_item in key_shards:
            enemy_list = room_to_available_enemies(chosen_room)
            if enemy_list:
                key_shard_to_location[chosen_item] = random.choice(enemy_list)
                #Giant dulla heads and Dullahammer EX share their drop with their early game counterpart
                if key_shard_to_location[chosen_item] == "N3126":
                    key_shard_to_location[chosen_item] = "N3090"
                if key_shard_to_location[chosen_item] == "N3127":
                    key_shard_to_location[chosen_item] = "N3015"
                if chosen_room in boss_rooms:
                    boss_rooms.remove(chosen_room)
                break

def room_to_available_chests(room):
    chest_list = []
    for i in used_chests:
        if chest_to_room(i) == room and not i in list(key_item_to_location.values()) and not i in keyless_chests:
            #If it is a chest with a self-contained requirement then check if available
            if i in chest_to_requirement:
                check = None
                for e in chest_to_requirement[i]:
                    #AND
                    if type(e) is list:
                        check = True
                        for o in e:
                            if not o in key_shard_to_location:
                                check = False
                                break
                        if check:
                            break
                    #OR  
                    else:
                        check = False
                        if e in key_shard_to_location:
                            check = True
                            break
                if check:
                    for e in range(2):
                        chest_list.append(i)
            else:
                chest_list.append(i)
    return chest_list

def room_to_available_enemies(room):
    enemy_list = []
    for i in Manager.mod_data["EnemyLocation"]:
        if not i in enemy_skip_list and not i in list(key_shard_to_location.values()) and Manager.mod_data["EnemyLocation"][i]["HasShard"] and room in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
            #Check if it is a boss that requires a certain movement ability to be realistically beatable
            if i in enemy_to_requirement:
                check = None
                for e in enemy_to_requirement[i]:
                    #AND
                    if type(e) is list:
                        check = True
                        for o in e:
                            if not o in key_shard_to_location:
                                check = False
                                break
                        if check:
                            break
                    #OR  
                    else:
                        check = False
                        if e in key_shard_to_location:
                            check = True
                            break
                if check:
                    for e in range(2):
                        enemy_list.append(i)
            else:
                #Increase chances of uncommon enemies
                #Otherwise shards tend to mostly end up on bats an whatnot
                for e in range(math.ceil(30/len(Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]))):
                    enemy_list.append(i)
    return enemy_list

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
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemyNum01"] = len(Manager.mod_data["EnemyLocation"][enemy]["NormalModeRooms"])
        enemy_room = ""
        for e in Manager.mod_data["EnemyLocation"][enemy]["NormalModeRooms"]:
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
            log["Key"][Manager.translation["Shard"][i]] = enemy_to_room(key_shard_to_location[i])
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