import Manager
import math
import random
import os
from collections import OrderedDict

def init():
    #Declare variables
    global chest_to_seed
    chest_to_seed = {
        "PotionMaterial": "Treasurebox_SIP000_Tutorial",
        "Qu07_Last": "Qu07_Last",
        "Swordsman": "Swordsman",
        "Treasurebox_SIP000_Tutorial": "Treasurebox_SIP011_4",
        "Treasurebox_SIP002_1": "Treasurebox_SIP005_2",
        "Treasurebox_SIP003_1": "Treasurebox_LIB009_1",
        "Treasurebox_SIP004_1": "Treasurebox_GDN006_5",
        "Treasurebox_SIP005_1": "Treasurebox_ENT002_1",
        "Treasurebox_SIP005_2": "Treasurebox_SIP002_1",
        "Treasurebox_SIP006_1": "Treasurebox_LIB022_1",
        "Treasurebox_SIP007_1": "Treasurebox_KNG017_1",
        "Treasurebox_SIP007_2": "Treasurebox_SIP011_3",
        "Treasurebox_SIP009_1": "Treasurebox_JPN011_1",
        "Treasurebox_SIP011_1": "Treasurebox_SIP014_1",
        "Treasurebox_SIP011_2": "Treasurebox_TWR015_1",
        "Treasurebox_SIP011_3": "Treasurebox_TWR000_3",
        "Treasurebox_SIP011_4": "PotionMaterial",
        "Treasurebox_SIP012_1": "Treasurebox_TAR007_1",
        "Treasurebox_SIP013_1": "Treasurebox_RVA001_2",
        "Treasurebox_SIP014_1": "Treasurebox_UGD051_1",
        "Treasurebox_SIP015_1": "Treasurebox_ARC000_1",
        "Treasurebox_SIP016_1": "Treasurebox_SAN024_1",
        "Treasurebox_SIP017_1": "Treasurebox_RVA011_2",
        "Treasurebox_SIP018_1": "Treasurebox_SIP016_1",
        "Treasurebox_SIP019_1": "Treasurebox_UGD025_1",
        "Treasurebox_SIP020_1": "Treasurebox_RVA015_1",
        "Treasurebox_SIP021_2": "Treasurebox_BIG011_1",
        "Treasurebox_SIP024_1": "Treasurebox_ENT014_2",
        "Treasurebox_SIP024_2": "Treasurebox_TWR009_1",
        "Treasurebox_SIP025_1": "Treasurebox_UGD009_4",
        "Treasurebox_SIP025_2": "Treasurebox_SAN015_2",
        "Treasurebox_SIP026_1": "Treasurebox_SAN005_1",
        "Treasurebox_VIL001_1": "Treasurebox_UGD044_2",
        "Treasurebox_VIL003_1": "Treasurebox_LIB009_2",
        "Treasurebox_VIL005_1": "Treasurebox_JPN018_1",
        "Treasurebox_VIL006_1": "Treasurebox_TWR017_5",
        "Treasurebox_VIL006_2": "Treasurebox_VIL006_2",
        "Treasurebox_VIL006_3": "Treasurebox_UGD044_1",
        "Treasurebox_VIL006_4": "Treasurebox_ENT020_2",
        "Treasurebox_VIL007_1": "Treasurebox_SAN003_1",
        "Treasurebox_VIL008_1": "Treasurebox_TRN002_3",
        "Treasurebox_VIL008_2": "Treasurebox_SAN003_5",
        "Treasurebox_VIL010_1": "Treasurebox_ENT015_1",
        "Treasurebox_ENT002_1": "Treasurebox_TWR019_2",
        "Treasurebox_ENT002_2": "Treasurebox_ENT018_1",
        "Treasurebox_ENT002_3": "Treasurebox_GDN012_1",
        "Treasurebox_ENT004_1": "Treasurebox_VIL001_1",
        "Treasurebox_ENT005_1": "Treasurebox_ENT005_1",
        "Treasurebox_ENT005_2": "Treasurebox_TWR018_8",
        "Treasurebox_ENT007_1": "Treasurebox_VIL008_2",
        "Treasurebox_ENT007_2": "Treasurebox_UGD052_1",
        "Treasurebox_ENT007_3": "Treasurebox_SIP007_1",
        "Treasurebox_ENT009_1": "Treasurebox_GDN004_1",
        "Treasurebox_ENT011_1": "Treasurebox_SAN009_2",
        "Treasurebox_ENT014_1": "Treasurebox_SAN003_3",
        "Treasurebox_ENT014_2": "Treasurebox_SAN016_5",
        "Treasurebox_ENT014_3": "Treasurebox_SND016_1",
        "Treasurebox_ENT018_1": "Treasurebox_SND011_1",
        "Treasurebox_ENT018_2": "Treasurebox_BIG002_1",
        "Treasurebox_ENT020_1": "Treasurebox_GDN006_1",
        "Treasurebox_ENT020_2": "Treasurebox_ARC004_1",
        "Treasurebox_ENT021_1": "Treasurebox_ARC006_2",
        "Treasurebox_ENT022_1": "Treasurebox_ENT020_1",
        "Treasurebox_ENT024_1": "Treasurebox_LIB032_1",
        "Treasurebox_ENT024_2": "Treasurebox_ARC007_2",
        "Treasurebox_ENT024_3": "Treasurebox_BIG012_1",
        "Treasurebox_GDN002_1": "Treasurebox_TWR019_4",
        "Treasurebox_GDN004_1": "Treasurebox_TRN002_4",
        "Treasurebox_GDN006_1": "Treasurebox_LIB040_1",
        "Treasurebox_GDN006_2": "Treasurebox_PureMiriam_Hair",
        "Treasurebox_GDN006_3": "Treasurebox_SAN019_3",
        "Treasurebox_GDN006_4": "Treasurebox_VIL008_1",
        "Treasurebox_GDN006_5": "Treasurebox_ICE003_1",
        "Treasurebox_GDN007_1": "Treasurebox_GDN007_1",
        "Treasurebox_GDN009_1": "Treasurebox_SAN017_1",
        "Treasurebox_GDN009_2": "Treasurebox_SIP025_2",
        "Treasurebox_GDN010_1": "Treasurebox_ICE006_1",
        "Treasurebox_GDN012_1": "Treasurebox_ENT004_1",
        "Treasurebox_GDN012_2": "Treasurebox_GDN009_2",
        "Treasurebox_GDN013_1": "Treasurebox_TWR004_1",
        "Treasurebox_GDN013_2": "Treasurebox_KNG002_1",
        "Treasurebox_GDN013_3": "Treasurebox_SAN021_4",
        "Treasurebox_GDN013_4": "Treasurebox_UGD038_1",
        "Treasurebox_GDN014_1": "Treasurebox_UGD049_1",
        "Treasurebox_SAN003_1": "Treasurebox_SIP011_1",
        "Treasurebox_SAN003_2": "Treasurebox_ARC003_1",
        "Treasurebox_SAN003_3": "Treasurebox_ENT008_1",
        "Treasurebox_SAN003_4": "Treasurebox_BIG006_5",
        "Treasurebox_SAN003_5": "Treasurebox_TWR019_3",
        "Treasurebox_SAN003_6": "Treasurebox_KNG018_3",
        "Treasurebox_SAN003_7": "Treasurebox_UGD033_1",
        "Treasurebox_SAN003_8": "Treasurebox_TWR018_7",
        "Treasurebox_SAN005_1": "Treasurebox_SND003_1",
        "Treasurebox_SAN005_2": "Treasurebox_SAN003_8",
        "Treasurebox_SAN009_1": "Treasurebox_TWR018_2",
        "Treasurebox_SAN009_2": "Treasurebox_UGD053_1",
        "Treasurebox_SAN013_1": "Treasurebox_ARC006_1",
        "Treasurebox_SAN013_2": "Treasurebox_ENT007_1",
        "Treasurebox_SAN014_1": "Treasurebox_SIP004_1",
        "Treasurebox_SAN015_2": "Treasurebox_SND008_2",
        "Treasurebox_SAN015_3": "Treasurebox_TRN002_1",
        "Treasurebox_SAN016_1": "Treasurebox_SND000_1",
        "Treasurebox_SAN016_2": "Treasurebox_UGD035_1",
        "Treasurebox_SAN016_3": "Treasurebox_RVA001_1",
        "Treasurebox_SAN016_4": "Treasurebox_SAN016_4",
        "Treasurebox_SAN016_5": "Treasurebox_SAN003_6",
        "Treasurebox_SAN017_1": "Treasurebox_ENT024_1",
        "Treasurebox_SAN019_1": "Treasurebox_JPN004_1",
        "Treasurebox_SAN019_2": "Treasurebox_SIP025_1",
        "Treasurebox_SAN019_3": "Treasurebox_SAN013_2",
        "Treasurebox_SAN020_1": "Treasurebox_SAN003_7",
        "Treasurebox_SAN021_1": "Treasurebox_ICE013_1",
        "Treasurebox_SAN021_2": "Treasurebox_SAN021_2",
        "Treasurebox_SAN021_3": "Treasurebox_GDN002_1",
        "Treasurebox_SAN021_4": "Treasurebox_GDN006_3",
        "Treasurebox_SAN021_5": "Treasurebox_KNG017_3",
        "Treasurebox_SAN024_1": "Treasurebox_SIP024_2",
        "Treasurebox_TWR000_1": "Treasurebox_RVA003_2",
        "Treasurebox_TWR003_1": "Treasurebox_ENT012_1",
        "Treasurebox_TWR004_1": "Treasurebox_GDN013_1",
        "Treasurebox_TWR005_1": "Treasurebox_LIB011_1",
        "Treasurebox_TWR006_1": "Treasurebox_UGD023_1",
        "Treasurebox_TWR008_1": "Treasurebox_BIG014_1",
        "Treasurebox_TWR009_1": "Treasurebox_SIP018_1",
        "Treasurebox_TWR010_1": "Treasurebox_KNG005_1",
        "Treasurebox_TWR012_1": "Treasurebox_UGD018_1",
        "Treasurebox_TWR013_1": "Treasurebox_ENT014_1",
        "Treasurebox_TWR016_1": "Treasurebox_SAN005_4",
        "Treasurebox_TWR017_1": "Treasurebox_KNG012_1",
        "Treasurebox_TWR017_2": "Treasurebox_BIG005_1",
        "Treasurebox_TWR017_3": "Treasurebox_ENT007_2",
        "Treasurebox_TWR017_4": "Treasurebox_RVA006_1",
        "Treasurebox_TWR017_5": "Treasurebox_LIB043_1",
        "Treasurebox_TWR017_6": "Treasurebox_SAN021_3",
        "Treasurebox_TWR017_7": "Treasurebox_TRN002_2",
        "Treasurebox_TWR018_1": "Treasurebox_GDN010_1",
        "Treasurebox_TWR018_2": "Treasurebox_UGD009_2",
        "Treasurebox_TWR018_3": "Treasurebox_SND018_1",
        "Treasurebox_TWR018_4": "Treasurebox_SAN003_2",
        "Treasurebox_TWR018_5": "Treasurebox_PureMiriam_Sword",
        "Treasurebox_TWR018_6": "Treasurebox_GDN009_1",
        "Treasurebox_TWR018_7": "Treasurebox_KNG018_2",
        "Treasurebox_TWR018_8": "Treasurebox_GDN013_3",
        "Treasurebox_TWR019_1": "Treasurebox_SAN021_1",
        "Treasurebox_TWR019_2": "Treasurebox_SAN014_1",
        "Treasurebox_TWR019_4": "Treasurebox_GDN012_2",
        "Treasurebox_LIB001_1": "Treasurebox_UGD047_1",
        "Treasurebox_LIB002_1": "Treasurebox_TWR017_4",
        "Treasurebox_LIB007_1": "Treasurebox_GDN014_1",
        "Treasurebox_LIB009_1": "Treasurebox_VIL006_1",
        "Treasurebox_LIB009_2": "Treasurebox_VIL003_1",
        "Treasurebox_LIB011_1": "Treasurebox_SIP006_1",
        "Treasurebox_LIB012_1": "Treasurebox_ICE003_2",
        "Treasurebox_LIB017_1": "Treasurebox_JPN000_1",
        "Treasurebox_LIB019_1": "Treasurebox_LIB002_1",
        "Treasurebox_LIB022_1": "Treasurebox_SIP026_1",
        "Treasurebox_LIB030_1": "Treasurebox_ARC005_1",
        "Treasurebox_LIB032_1": "Treasurebox_LIB019_1",
        "Treasurebox_LIB033_1": "Treasurebox_SAN009_3",
        "Treasurebox_LIB040_1": "Treasurebox_ENT022_1",
        "Treasurebox_LIB043_1": "Treasurebox_UGD010_1",
        "Treasurebox_TRN002_1": "Treasurebox_TWR017_7",
        "Treasurebox_TRN002_2": "Treasurebox_ENT024_2",
        "Treasurebox_TRN002_3": "Treasurebox_UGD003_3",
        "Treasurebox_TRN002_4": "Treasurebox_ENT007_3",
        "Treasurebox_TRN002_5": "Treasurebox_JPN010_2",
        "Treasurebox_KNG002_1": "Treasurebox_UGD040_1",
        "Treasurebox_KNG002_2": "Treasurebox_TWR008_1",
        "Treasurebox_KNG003_1": "Treasurebox_ENT002_2",
        "Treasurebox_KNG006_1": "Treasurebox_JPN001_1",
        "Treasurebox_KNG010_1": "Treasurebox_UGD012_1",
        "Treasurebox_KNG011_1": "Treasurebox_KNG018_4",
        "Treasurebox_KNG012_1": "Treasurebox_ENT009_1",
        "Treasurebox_KNG012_2": "Treasurebox_UGD009_1",
        "Treasurebox_KNG016_1": "Treasurebox_UGD048_1",
        "Treasurebox_KNG017_1": "Treasurebox_ICE008_1",
        "Treasurebox_KNG017_2": "Treasurebox_TWR019_1",
        "Treasurebox_KNG017_3": "Treasurebox_ENT002_3",
        "Treasurebox_KNG017_4": "Treasurebox_UGD003_2",
        "Treasurebox_KNG017_5": "Treasurebox_KNG017_5",
        "Treasurebox_KNG018_2": "Treasurebox_KNG018_1",
        "Treasurebox_KNG018_3": "Treasurebox_LIB012_1",
        "Treasurebox_KNG018_4": "Treasurebox_KNG002_2",
        "Treasurebox_KNG021_1": "Treasurebox_RVA005_2",
        "Treasurebox_KNG022_1": "Treasurebox_UGD050_1",
        "Treasurebox_UGD001_1": "Treasurebox_KNG016_1",
        "Treasurebox_UGD003_1": "Treasurebox_SND005_1",
        "Treasurebox_UGD003_2": "Treasurebox_VIL006_3",
        "Treasurebox_UGD003_3": "Treasurebox_KNG017_4",
        "Treasurebox_UGD003_4": "Treasurebox_SND001_1",
        "Treasurebox_UGD005_1": "Treasurebox_ICE014_1",
        "Treasurebox_UGD005_2": "Treasurebox_SND021_1",
        "Treasurebox_UGD007_1": "Treasurebox_GDN006_2",
        "Treasurebox_UGD009_1": "Treasurebox_LIB018_1",
        "Treasurebox_UGD009_2": "Treasurebox_ENT011_1",
        "Treasurebox_UGD009_3": "Treasurebox_UGD048_2",
        "Treasurebox_UGD009_4": "Treasurebox_SIP019_1",
        "Treasurebox_UGD010_1": "Treasurebox_SAN013_1",
        "Treasurebox_UGD011_1": "Treasurebox_UGD011_1",
        "Treasurebox_UGD021_1": "Treasurebox_BIG006_1",
        "Treasurebox_UGD024_1": "Treasurebox_UGD005_1",
        "Treasurebox_UGD024_2": "Treasurebox_UGD020_1",
        "Treasurebox_UGD024_3": "Treasurebox_UGD024_3",
        "Treasurebox_UGD025_1": "Treasurebox_BIG006_3",
        "Treasurebox_UGD025_2": "Treasurebox_RVA004_1",
        "Treasurebox_UGD025_3": "Treasurebox_UGD036_1",
        "Treasurebox_UGD027_1": "Treasurebox_UGD032_1",
        "Treasurebox_UGD030_1": "Treasurebox_SND019_1",
        "Treasurebox_UGD031_1": "Treasurebox_KNG022_1",
        "Treasurebox_UGD031_2": "Treasurebox_TWR017_3",
        "Treasurebox_UGD036_1": "Treasurebox_ICE011_1",
        "Treasurebox_UGD036_2": "Treasurebox_TWR018_1",
        "Treasurebox_UGD038_1": "Treasurebox_UGD045_1",
        "Treasurebox_UGD040_1": "Treasurebox_BIG010_1",
        "Treasurebox_UGD041_1": "Treasurebox_TAR009_1",
        "Treasurebox_UGD042_1": "Treasurebox_SND026_1",
        "Treasurebox_UGD044_1": "Treasurebox_UGD047_2",
        "Treasurebox_UGD044_2": "Treasurebox_TRN002_5",
        "Treasurebox_UGD046_1": "Treasurebox_UGD046_1",
        "Treasurebox_UGD046_2": "Treasurebox_ICE008_2",
        "Treasurebox_UGD047_2": "Treasurebox_KNG021_3",
        "Treasurebox_UGD048_1": "Treasurebox_SND008_1",
        "Treasurebox_UGD050_1": "Treasurebox_UGD025_2",
        "Treasurebox_UGD051_1": "Treasurebox_TWR017_1",
        "Treasurebox_UGD052_1": "Treasurebox_ENT011_2",
        "Treasurebox_UGD052_2": "Treasurebox_SND010_1",
        "Treasurebox_UGD053_1": "Treasurebox_JPN005_1",
        "Treasurebox_UGD054_1": "Treasurebox_JPN008_1",
        "Treasurebox_UGD056_1": "Treasurebox_JPN002_1",
        "Treasurebox_SND002_1": "Treasurebox_SAN005_3",
        "Treasurebox_SND003_1": "Treasurebox_TWR005_1",
        "Treasurebox_SND004_1": "Treasurebox_KNG021_1",
        "Treasurebox_SND006_1": "Treasurebox_UGD031_1",
        "Treasurebox_SND008_1": "Treasurebox_SAN019_1",
        "Treasurebox_SND008_2": "Treasurebox_KNG021_2",
        "Treasurebox_SND009_1": "Treasurebox_SIP009_1",
        "Treasurebox_SND010_1": "Treasurebox_SND014_1",
        "Treasurebox_SND010_2": "Treasurebox_TWR017_6",
        "Treasurebox_SND013_1": "Treasurebox_JPN003_1",
        "Treasurebox_SND015_1": "Treasurebox_RVA014_1",
        "Treasurebox_SND016_1": "Treasurebox_ENT021_1",
        "Treasurebox_SND017_1": "Treasurebox_TAR003_1",
        "Treasurebox_SND018_1": "Treasurebox_BIG016_1",
        "Treasurebox_SND019_1": "Treasurebox_ICE010_1",
        "Treasurebox_SND020_1": "Treasurebox_RVA009_1",
        "Treasurebox_SND024_1": "Treasurebox_UGD057_1",
        "Treasurebox_SND025_1": "Treasurebox_RVA003_1",
        "Treasurebox_ARC000_1": "Treasurebox_UGD026_1",
        "Treasurebox_ARC002_1": "Treasurebox_UGD019_1",
        "Treasurebox_ARC003_1": "Treasurebox_UGD007_1",
        "Treasurebox_ARC004_1": "Treasurebox_BIG012_3",
        "Treasurebox_ARC006_1": "Treasurebox_SND006_1",
        "Treasurebox_ARC006_2": "Treasurebox_SIP024_1",
        "Treasurebox_ARC007_1": "Treasurebox_SIP003_1",
        "Treasurebox_ARC007_2": "Treasurebox_ENT014_3",
        "Treasurebox_TAR001_1": "Treasurebox_TAR005_1",
        "Treasurebox_TAR002_1": "N3106_2ND_Treasure",
        "Treasurebox_TAR006_1": "Treasurebox_PureMiriam_Dress",
        "Treasurebox_TAR007_1": "Treasurebox_ICE001_2",
        "Treasurebox_TAR010_1": "Treasurebox_UGD015_1",
        "Treasurebox_JPN002_1": "Treasurebox_UGD056_1",
        "Treasurebox_JPN002_2": "Treasurebox_JPN002_2",
        "Treasurebox_JPN004_1": "Treasurebox_TWR018_4",
        "Treasurebox_JPN005_1": "Treasurebox_TWR018_6",
        "Treasurebox_JPN009_1": "Treasurebox_UGD001_1",
        "Treasurebox_JPN010_1": "Treasurebox_SIP015_1",
        "Treasurebox_JPN010_2": "Treasurebox_SAN021_5",
        "Treasurebox_JPN013_1": "N3106_1ST_Treasure",
        "Treasurebox_JPN015_1": "Treasurebox_SAN016_1",
        "Treasurebox_JPN017_1": "Treasurebox_VIL005_1",
        "Treasurebox_JPN018_1": "Treasurebox_ARC007_1",
        "Treasurebox_RVA001_1": "Treasurebox_ENT018_2",
        "Treasurebox_RVA001_2": "Treasurebox_SIP013_1",
        "Treasurebox_RVA002_1": "Treasurebox_UGD052_2",
        "Treasurebox_RVA004_1": "Treasurebox_JPN017_1",
        "Treasurebox_RVA006_1": "Treasurebox_JPN009_1",
        "Treasurebox_RVA010_1": "Treasurebox_UGD037_1",
        "Treasurebox_RVA011_1": "Treasurebox_RVA011_1",
        "Treasurebox_RVA011_2": "Treasurebox_VIL010_1",
        "Treasurebox_RVA012_1": "Treasurebox_SND027_1",
        "Treasurebox_RVA015_1": "Treasurebox_TWR003_1",
        "Treasurebox_BIG002_1": "Treasurebox_UGD022_1",
        "Treasurebox_BIG005_1": "Treasurebox_LIB042_1",
        "Treasurebox_BIG006_1": "Treasurebox_SND009_1",
        "Treasurebox_BIG006_2": "Treasurebox_KNG017_2",
        "Treasurebox_BIG006_3": "Treasurebox_SAN019_2",
        "Treasurebox_BIG006_4": "Treasurebox_BIG008_1",
        "Treasurebox_BIG006_5": "Treasurebox_SAN005_2",
        "Treasurebox_BIG006_6": "Treasurebox_ENT005_2",
        "Treasurebox_BIG007_1": "Treasurebox_SND012_1",
        "Treasurebox_BIG008_1": "Treasurebox_BIG006_4",
        "Treasurebox_BIG010_1": "Treasurebox_UGD029_1",
        "Treasurebox_BIG011_1": "Treasurebox_SIP021_2",
        "Treasurebox_BIG012_1": "Treasurebox_SIP017_1",
        "Treasurebox_BIG012_2": "Treasurebox_UGD039_1",
        "Treasurebox_BIG012_3": "Treasurebox_SND010_2",
        "Treasurebox_BIG013_1": "Treasurebox_KNG003_1",
        "Treasurebox_BIG014_1": "Treasurebox_KNG011_1",
        "Treasurebox_BIG016_1": "Treasurebox_JPN010_1",
        "Treasurebox_BIG016_2": "Treasurebox_TWR012_1",
        "Treasurebox_BIG016_3": "Treasurebox_GDN013_4",
        "Treasurebox_ICE001_1": "Treasurebox_TWR006_2",
        "Treasurebox_ICE001_2": "Treasurebox_UGD036_2",
        "Treasurebox_ICE002_1": "Treasurebox_SND007_1",
        "Treasurebox_ICE003_1": "Treasurebox_SIP005_1",
        "Treasurebox_ICE003_2": "Treasurebox_VIL006_4",
        "Treasurebox_ICE006_1": "Treasurebox_UGD016_1",
        "Treasurebox_ICE008_1": "Treasurebox_VIL007_1",
        "Treasurebox_ICE008_2": "Treasurebox_RVA005_1",
        "Treasurebox_ICE010_1": "Treasurebox_ENT024_3",
        "Treasurebox_ICE011_1": "Treasurebox_GDN013_2",
        "Treasurebox_ICE013_1": "Treasurebox_BIG006_2",
        "Treasurebox_ICE014_1": "Treasurebox_SND020_1",
        "Treasurebox_PureMiriam_Hair": "Treasurebox_SAN009_1",
        "Treasurebox_PureMiriam_Tiare": "Treasurebox_PureMiriam_Tiare",
        "Treasurebox_PureMiriam_Dress": "Treasurebox_TAR006_1",
        "Treasurebox_PureMiriam_Sword": "Treasurebox_SAN000_1",
        "Wall_SIP004_1": "Wall_BIG012_1",
        "Wall_SIP009_1": "Wall_LIB004_1",
        "Wall_SIP014_1": "Wall_UGD031_1",
        "Wall_SIP016_1": "Wall_ICE003_1",
        "Wall_ENT002_1": "Wall_TRN005_1",
        "Wall_ENT012_1": "Wall_TWR013_1",
        "Wall_GDN006_1": "Wall_GDN006_1",
        "Wall_SAN000_1": "Wall_UGD006_1",
        "Wall_SAN005_1": "Wall_RVA011_1",
        "Wall_SAN019_1": "Wall_LIB025_1",
        "Wall_KNG000_1": "Wall_SND001_1",
        "Wall_KNG007_1": "Wall_RVA003_1",
        "Wall_LIB004_1": "Wall_ICE010_1",
        "Wall_LIB019_1": "Wall_UGD012_1",
        "Wall_LIB025_1": "Wall_TWR006_1",
        "Wall_TWR006_1": "Wall_UGD020_1",
        "Wall_TWR013_1": "Wall_ENT012_1",
        "Wall_TWR016_1": "Wall_TWR016_1",
        "Wall_TRN005_1": "Wall_SIP009_1",
        "Wall_UGD000_1": "Wall_ENT002_1",
        "Wall_UGD003_1": "Wall_UGD003_1",
        "Wall_UGD006_1": "Wall_SND019_1",
        "Wall_UGD012_1": "Wall_SAN005_1",
        "Wall_UGD020_1": "Wall_BIG016_1",
        "Wall_UGD031_1": "Wall_SIP014_1",
        "Wall_UGD037_1": "Wall_ICE017_1",
        "Wall_UGD046_1": "Wall_TAR007_1",
        "Wall_UGD056_1": "Wall_UGD056_1",
        "Wall_SND001_1": "Wall_SAN019_1",
        "Wall_SND019_1": "Wall_KNG007_1",
        "Wall_TAR007_1": "Wall_UGD046_1",
        "Wall_JPN011_1": "Wall_KNG000_1",
        "Wall_JPN013_1": "Wall_JPN013_1",
        "Wall_RVA011_1": "Wall_SIP016_1",
        "Wall_BIG002_1": "Wall_BIG002_1",
        "Wall_BIG012_1": "Wall_UGD000_1",
        "Wall_BIG016_1": "Wall_JPN011_1",
        "Wall_ICE003_1": "Wall_LIB019_1",
        "Wall_ICE010_1": "Wall_SIP004_1",
        "Wall_ICE017_1": "Wall_SAN000_1",
        "N3106_1ST_Treasure": "Treasurebox_ARC002_1",
        "N3106_2ND_Treasure": "Treasurebox_KNG006_1"
    }
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
        "ICE": "m18"
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
    global room_to_special_chest
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
    global boss_rooms
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
        "m19K2C_000",
        "m51EBT_000",
        "m88BKR_001",
        "m88BKR_002",
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
        "Bloodsteel"
    ]
    global other_key
    other_key = [
        "ShipMap",
        "DiscountCard"
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
    global coin
    coin = [1, 5, 10, 50, 100, 500, 1000]
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
    #Skip lists
    #Bosses that softlock if they are given a different shard
    global enemy_skip_list
    enemy_skip_list = [
        "N1003",
        "N2001",
        "N2013"
    ]
    global shop_skip_list
    shop_skip_list = [
        "Waystone"
    ]
    global ship_skip_list
    ship_skip_list = [
        "m01SIP_022",
        "m01SIP_023"
    ]
    #Galleon
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
    global ship_chest_list
    ship_chest_list = [
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
        "Treasurebox_SIP015_1",
        "Treasurebox_SIP016_1",
        "Treasurebox_SIP017_1",
        "Treasurebox_SIP018_1",
        "Treasurebox_SIP019_1",
        "Treasurebox_SIP020_1",
        "Treasurebox_SIP021_2",
        "Treasurebox_SIP025_1",
        "Treasurebox_SIP025_2",
        "Wall_SIP004_1",
        "Wall_SIP009_1",
        "Wall_SIP016_1",
    ]
    global shard_type_to_hsv
    shard_type_to_hsv = {
        "Skill":       (  0,   0, 100),
        "Trigger":     (  0, 100, 100),
        "Effective":   (216, 100, 100),
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
    for i in Manager.dictionary["ItemDrop"]:
        for e in range(Manager.dictionary["ItemDrop"][i]["ChestRatio"]):
            chest_type.append(i)
            if Manager.dictionary["ItemDrop"][i]["ChestColor"] == "Green":
                green_chest_type.append(i)
            if Manager.dictionary["ItemDrop"][i]["ChestColor"] == "Blue":
                blue_chest_type.append(i)
        for e in range(Manager.dictionary["ItemDrop"][i]["QuestRatio"]):
            quest_type.append(i)
    for i in Manager.dictionary["EnemyDrop"]:
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
    for i in list(Manager.dictionary["MapLogic"]):
        if Manager.datatable["PB_DT_RoomMaster"][i]["Unused"]:
            del Manager.dictionary["MapLogic"][i]

def extra_logic():
    #8 Bit Nightmare is always gonna be connected to Hall of Termination regardless of map
    #So create its entry manually
    Manager.dictionary["MapLogic"]["m51EBT_000"] = {}
    Manager.dictionary["MapLogic"]["m51EBT_000"]["GateRoom"]             = False
    if Manager.dictionary["MapLogic"]["m06KNG_021"]["GateRoom"]:
        Manager.dictionary["MapLogic"]["m51EBT_000"]["NearestGate"]      = ["m06KNG_021"]
    else:
        Manager.dictionary["MapLogic"]["m51EBT_000"]["NearestGate"]      = list(Manager.dictionary["MapLogic"]["m06KNG_021"]["NearestGate"])
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Doublejump"]           = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["HighJump"]             = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Invert"]               = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Deepsinker"]           = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Dimensionshift"]       = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Reflectionray"]        = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Aquastream"]           = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Bloodsteel"]           = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Swordsman"]            = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Silverbromide"]        = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["BreastplateofAguilar"] = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Keyofbacker1"]         = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Keyofbacker2"]         = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Keyofbacker3"]         = False
    Manager.dictionary["MapLogic"]["m51EBT_000"]["Keyofbacker4"]         = False
    #Same goes for Kingdom 2 Crown's connection to the train
    #Also add Crown of Creation to the logic manually
    for i in Manager.dictionary["MapLogic"]:
        Manager.dictionary["MapLogic"][i]["MonarchCrown"] = False
    Manager.dictionary["MapLogic"]["m19K2C_000"] = {}
    Manager.dictionary["MapLogic"]["m19K2C_000"]["GateRoom"] = True
    if Manager.dictionary["MapLogic"]["m09TRN_002"]["GateRoom"]:
        Manager.dictionary["MapLogic"]["m19K2C_000"]["NearestGate"]      = ["m09TRN_002"]
    else:
        Manager.dictionary["MapLogic"]["m19K2C_000"]["NearestGate"]      = list(Manager.dictionary["MapLogic"]["m09TRN_002"]["NearestGate"])
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Doublejump"]           = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["HighJump"]             = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Invert"]               = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Deepsinker"]           = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Dimensionshift"]       = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Reflectionray"]        = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Aquastream"]           = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Bloodsteel"]           = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Swordsman"]            = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Silverbromide"]        = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["BreastplateofAguilar"] = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Keyofbacker1"]         = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Keyofbacker2"]         = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Keyofbacker3"]         = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["Keyofbacker4"]         = False
    Manager.dictionary["MapLogic"]["m19K2C_000"]["MonarchCrown"]         = True
    #Benjamin's last reward appears if you've completed all his quests which is not guaranteed to be possible early on
    #Gebel's Glasses chest only appears if you to get 1 copy of every shard
    #OD can only be fought if the Tome of Conquest was obtained
    #Make sure none of these are required
    if Manager.dictionary["MapLogic"]["m18ICE_019"]["GateRoom"]:
        Manager.dictionary["MapLogic"]["m02VIL_003"]["NearestGate"]      = ["m18ICE_019"]
        Manager.dictionary["MapLogic"]["m02VIL_005"]["NearestGate"]      = ["m18ICE_019"]
        Manager.dictionary["MapLogic"]["m18ICE_004"]["NearestGate"]      = ["m18ICE_019"]
    else:
        Manager.dictionary["MapLogic"]["m02VIL_003"]["NearestGate"]      = list(Manager.dictionary["MapLogic"]["m18ICE_019"]["NearestGate"])
        Manager.dictionary["MapLogic"]["m02VIL_005"]["NearestGate"]      = list(Manager.dictionary["MapLogic"]["m18ICE_019"]["NearestGate"])
        Manager.dictionary["MapLogic"]["m18ICE_004"]["NearestGate"]      = list(Manager.dictionary["MapLogic"]["m18ICE_019"]["NearestGate"])

def hard_enemy_logic():
    #On hard mode some rooms have extra enemies so update the location info
    for i in Manager.dictionary["EnemyLocation"]:
        for e in Manager.dictionary["EnemyLocation"][i]["HardModeRooms"]:
            Manager.dictionary["EnemyLocation"][i]["NormalModeRooms"].append(e)
    #Dulla heads can also be replaced with maledictions so adapt for that
    Manager.dictionary["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m07LIB_029")
    Manager.dictionary["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_005")
    Manager.dictionary["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_013")
    Manager.dictionary["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m11UGD_013")

def story_chest():
    #While not meant for story mode adapt the chest pointers if the player wants to mess around
    for i in chest_to_seed:
        chest_to_seed[i] = i
    #Also don't randomize the starting shards that are immediately required in that mode
    enemy_skip_list.append("N3006")
    enemy_skip_list.append("N3005")

def remove_infinite():
    #These specific gears grant the player an infinite source of something which generally ends up defining the meta and dominating runs
    #If the player is up for variety and challenge remove those from the pool so that they can never be found
    while "Gebelsglasses" in Manager.dictionary["ItemDrop"]["Accessory"]["ItemPool"]:
        Manager.dictionary["ItemDrop"]["Accessory"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in Manager.dictionary["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.dictionary["QuestRequirement"]["Memento"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in Manager.dictionary["ItemDrop"]["Headgear"]["ItemPool"]:
        Manager.dictionary["ItemDrop"]["Headgear"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in Manager.dictionary["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.dictionary["QuestRequirement"]["Memento"]["ItemPool"].remove("Recyclehat")

def give_shortcut():
    #Start the player with all shortcut slots since it is a quality of life more than an ability
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemId"] = "Shortcut"
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemQuantity"] = 7
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemRate"] = 100.0
    while "Shortcut" in Manager.dictionary["ShardDrop"]["ItemPool"]:
        Manager.dictionary["ShardDrop"]["ItemPool"].remove("Shortcut")
    
def give_eye():
    #Start the player with Detective's Eye so that missing breakable walls isn't an issue
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonItemId"] = "SkilledDetectiveeye"
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonItemQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonRate"] = 100.0
    while "Detectiveeye" in Manager.dictionary["ShardDrop"]["ItemPool"]:
        Manager.dictionary["ShardDrop"]["ItemPool"].remove("Detectiveeye")

def give_extra(shard):
    #Start the player with a specific shard by putting it in the Village Key container
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientId"] = shard
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientRate"] = 100.0
    while shard in Manager.dictionary["ShardDrop"]["ItemPool"]:
        Manager.dictionary["ShardDrop"]["ItemPool"].remove(shard)

def no_shard_craft():
    #If shards are randomized then disable the possiblity to manually craft shards so that they aren't always available
    Manager.datatable["PB_DT_CraftMaster"]["HighJump"]["OpenKeyRecipeID"] = "Medal019"
    for i in Manager.datatable["PB_DT_CraftMaster"]:
        if Manager.datatable["PB_DT_CraftMaster"][i]["Type"] == "ECraftType::Craft" and Manager.datatable["PB_DT_CraftMaster"][i]["CraftItemId"] in Manager.dictionary["ShardDrop"]["ItemPool"]:
            Manager.datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "Medal019"

def deseema_fix():
    #If item are not randomized then quickly fix the aqua stream progression logic by giving Deseema increased drop chances
    Manager.datatable["PB_DT_DropRateMaster"]["N3022_Shard"]["DropSpecialFlags"] = "EDropSpecialFlag::DropShardOnce"
    Manager.datatable["PB_DT_DropRateMaster"]["N3022_Shard"]["ShardRate"]        = Manager.dictionary["ShardDrop"]["ItemRate"]*3

def key_logic():
    #Place all key items with logic so that the game is always beatable
    #The startegy used here is similar to the one implemented in vanilla where it reads from a room check file and loops through all the rooms based on that
    #The logic starts in all rooms that have no requirements until a gate is reached to determine which key item to place and so on
    #Since this has to adapt to different map layouts we cannot get away with using any "cheats" that are specific to the default map
    previous_gate = []
    previous_room = []
    all_rooms = []
    requirement = []
    requirement_to_gate = {}
    #Filling list with all room names
    all_rooms = list(Manager.dictionary["MapLogic"])
    #Filling requirement dictionary
    for i in key_items:
        requirement_to_gate[i] = []
    for i in key_shards:
        requirement_to_gate[i] = []
    #Loop through all keys until they've all been assigned
    while all_keys:
        #Reset lists and dicts
        requirement.clear()
        for i in key_items:
            requirement_to_gate[i].clear()
        for i in key_shards:
            requirement_to_gate[i].clear()
        previous_room.clear()
        #Gathering upcoming gate requirements
        for i in Manager.dictionary["MapLogic"]:
            if Manager.dictionary["MapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.dictionary["MapLogic"][i]["NearestGate"]) and not i in previous_gate:
                for e in key_items:
                    if Manager.dictionary["MapLogic"][i][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
                for e in key_shards:
                    if Manager.dictionary["MapLogic"][i][e]:
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
        for i in Manager.dictionary["MapLogic"]:
            if not Manager.dictionary["MapLogic"][i]["GateRoom"] and previous_in_nearest(previous_gate, Manager.dictionary["MapLogic"][i]["NearestGate"]) or i in previous_gate:
                #Increasing chances of late rooms
                #Otherwise early game areas are more likely to have everything
                gate_count = 1
                gate_list = list(Manager.dictionary["MapLogic"][i]["NearestGate"])
                while gate_list:
                    nearest_gate = random.choice(gate_list)
                    for e in Manager.dictionary["MapLogic"]:
                        if e == nearest_gate:
                            gate_count += 1
                            gate_list = list(Manager.dictionary["MapLogic"][e]["NearestGate"])
                            break
                #Making multplier more extreme with exponent
                gate_count = round(gate_count**1.5)
                #Increasing chances of boss rooms
                #Otherwise bosses and special enemies have low chances of being required
                if i in boss_rooms:
                    gate_count *= 6
                for e in range(gate_count):
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
    #Convert
    room_to_chest()
    room_to_enemy()

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
    return Manager.dictionary["EnemyLocation"][enemy]["NormalModeRooms"]

def logic_choice(chosen_item, room_list):
    #Removing key from list
    all_keys.remove(chosen_item)
    key_order.append(chosen_item)
    #Choosing room to place item in
    check = False
    while not check:
        chosen_room = random.choice(room_list)
        if chosen_room in list(key_item_to_location.values()) or chosen_room in list(key_shard_to_location.values()) or chosen_room == "m01SIP_000":
            continue
        #Checking if room has chest
        if chosen_item in key_items:
            check = room_chest_check(chosen_room)
        #Checking if room has enemy
        if chosen_item in key_shards:
            check = room_enemy_check(chosen_room)
    #Updating key location
    if chosen_item in key_items:
        key_item_to_location[chosen_item] = chosen_room
    if chosen_item in key_shards:
        key_shard_to_location[chosen_item] = chosen_room

def room_chest_check(room):
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        #Checking chest isn't unused
        if i in chest_to_seed:
            #Checking if chest corresponds to room
            if chest_to_room(i) == room:
                return True
    return False

def room_enemy_check(room):
    for i in Manager.dictionary["EnemyLocation"]:
        #Checking if enemy weilds a shard and is in room
        if not i in enemy_skip_list and Manager.dictionary["EnemyLocation"][i]["HasShard"] and room in Manager.dictionary["EnemyLocation"][i]["NormalModeRooms"]:
            #Checking if enemy isn't in an already assigned room
            for e in key_shard_to_location:
                if key_shard_to_location[e] in Manager.dictionary["EnemyLocation"][i]["NormalModeRooms"]:
                    return False
            return True
    return False

def room_to_chest():
    for i in key_item_to_location:
        #Gathering possible chest choices for room
        possible_chests = []
        for e in Manager.datatable["PB_DT_DropRateMaster"]:
            if e in chest_to_seed:
                if key_item_to_location[i][3:].replace("_", "") in e:
                    possible_chests.append(e)
                try:
                    if e in room_to_special_chest[key_item_to_location[i]]:
                        possible_chests.append(e)
                except KeyError:
                    continue
        #Picking chest
        key_item_to_location[i] = random.choice(possible_chests)

def room_to_enemy():
    for i in key_shard_to_location:
        #Gathering possible enemy choices for room
        possible_enemy = []
        for e in Manager.dictionary["EnemyLocation"]:
            if not e in enemy_skip_list and Manager.dictionary["EnemyLocation"][e]["HasShard"] and key_shard_to_location[i] in Manager.dictionary["EnemyLocation"][e]["NormalModeRooms"]:
                #Increasing chances of uncommon enemies
                #Otherwise shards tend to mostly end up on bats an whatnot
                for o in range(math.ceil(36/len(Manager.dictionary["EnemyLocation"][e]["NormalModeRooms"]))):
                    possible_enemy.append(e)
        #Checking if enemy isn't already taken
        chosen_enemy = random.choice(possible_enemy)
        while chosen_enemy in list(key_shard_to_location.values()):
            chosen_enemy = random.choice(possible_enemy)
        #Changing
        key_shard_to_location[i] = chosen_enemy

def rand_overworld_key():
    key_logic()
    #Key items
    for i in key_items:
        patch_key_item_entry(i, key_item_to_location[i])
    #Key shards
    for i in key_shards:
        patch_key_shard_entry(i, key_shard_to_location[i])
    #Other keys
    for i in other_key:
        patch_key_item_entry(i, random.choice(list(chest_to_seed)))

def rand_ship_waystone():
    #On random enemy levels or resistances Vepar can potentially become an impassable blockade
    #To ensure that the player can always move forward randomly place a waystone on the ship
    #Check abilities present on the galleon
    for i in key_shard_to_location:
        for e in Manager.dictionary["EnemyLocation"][key_shard_to_location[i]]["NormalModeRooms"]:
            if "m01SIP" in e and e not in ship_skip_list:
                if i in ["Doublejump", "Dimensionshift", "Reflectionray"]:
                    ship_height()
                if i in ["HighJump", "Invert"]:
                    ship_flight()
    #Choose chest
    chosen_chest = random.choice(ship_chest_list)
    while chosen_chest not in chest_to_seed:
        chosen_chest = random.choice(ship_chest_list)
    patch_key_item_entry("Waystone", chosen_chest)

def ship_height():
    #When Miriam has higher jump on galleon
    if "Treasurebox_SIP014_1" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP014_1")
    if "Treasurebox_SIP024_1" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP024_1")
    if "Treasurebox_SIP024_2" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP024_2")
    if "Treasurebox_SIP026_1" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_SIP026_1")
    if "Wall_SIP014_1" not in ship_chest_list:
        ship_chest_list.append("Wall_SIP014_1")
    while "m01SIP_023" in ship_skip_list:
        ship_skip_list.remove("m01SIP_023")

def ship_flight():
    #When Miriam has flight on the galleon
    if "Treasurebox_PureMiriam_Hair" not in ship_chest_list:
        ship_chest_list.append("Treasurebox_PureMiriam_Hair")

def rand_overworld_shard():
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        #Check if the entry should be skipped
        id = i.split("_")
        if not id[0] in Manager.dictionary["EnemyLocation"]:
            continue
        if not Manager.dictionary["EnemyLocation"][id[0]]["HasShard"]:
            continue
        if id[1] == "Treasure":
            continue
        if id[0] in enemy_skip_list:
            continue
        if id[0] in list(key_shard_to_location.values()):
            continue
        #Reduce dulla head drop rate
        if id[0] in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        #Assign shard
        if i == id[0] + "_Shard":
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = any_pick(Manager.dictionary["ShardDrop"]["ItemPool"], True, "None")
            if Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.dictionary["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        else:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"]   = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["ShardId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["ShardRate"]

def rand_overworld_pool():
    #Start chest
    patch_start_chest_entry()
    #Johannes mats
    patch_chest_entry(random.choice(blue_chest_type), "PotionMaterial", True)
    #Final Benjamin reward
    patch_chest_entry(random.choice(green_chest_type), "Qu07_Last", True)
    #Ultimate Zangetsu reward
    patch_chest_entry(random.choice(green_chest_type), "Swordsman", True)
    #Carpenter's first chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_1ST_Treasure", True)
    #Carpenter's second chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_2ND_Treasure", True)
    #Item pool
    for i in chest_to_seed:
        patch_chest_entry(random.choice(chest_type), i, False)
    #Enemy pool
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        id = i.split("_")
        if not id[0] in Manager.dictionary["EnemyLocation"]:
            continue
        if not Manager.dictionary["EnemyLocation"][id[0]]["HasShard"]:
            continue
        if "Treasure" in id:
            continue
        if Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["CommonRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] == 0.0 and Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] == 0.0:
            continue
        #Reduce dulla head drop rate
        if id[0] in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        #Assign drops
        if i == id[0] + "_Shard":
            patch_enemy_entry(random.choice(enemy_type), drop_rate_multiplier, i)
        else:
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"]               = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemQuantity"]         = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemRate"]             = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareItemRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonItemId"]             = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonItemId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonItemQuantity"]       = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonRate"]               = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientId"]         = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientQuantity"]   = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"]       = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["RareIngredientRate"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientId"]       = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonIngredientId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientQuantity"] = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonIngredientQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"]     = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["CommonIngredientRate"]

def patch_key_item_entry(item, container):
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = item
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = 100.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = False
    del chest_to_seed[container]
    
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
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.dictionary["ShardDrop"]["ItemRate"]*3*drop_rate_multiplier
        elif i.split("_")[0] == enemy:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = 0.0

def patch_start_chest_entry():
    #Randomize the very first chest so that it is always a weapon
    container = "Treasurebox_SIP000_Tutorial"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.dictionary["ItemDrop"]["Weapon"]["ItemPool"], Manager.dictionary["ItemDrop"]["Weapon"]["IsUnique"], "Weapon")
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.dictionary["ItemDrop"]["Weapon"]["ItemQuantity"]
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.dictionary["ItemDrop"]["Weapon"]["ItemRate"]
    #Give extra bullets if the starting weapon is a gun
    if Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] in gun_list:
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = any_pick(Manager.dictionary["ItemDrop"]["Bullet"]["ItemPool"], Manager.dictionary["ItemDrop"]["Bullet"]["IsUnique"], "Bullet")
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = Manager.dictionary["ItemDrop"]["Bullet"]["ItemQuantity"]*3
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = Manager.dictionary["ItemDrop"]["Bullet"]["ItemRate"]
    else:
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = "None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::None"
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = 0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = 0.0
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = False
    del chest_to_seed[container]

def patch_chest_entry(item_type, container, remove):
    #Randomize chest items based on item types
    if not container in chest_to_seed:
        return
    if Manager.dictionary["ItemDrop"][item_type]["ChestColor"] == "Blue":
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = random.choice(coin)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::D" + str(Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"])
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = True
    elif Manager.dictionary["ItemDrop"][item_type]["ChestColor"] == "Red":
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], Manager.dictionary["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::D2000"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = False
    else:
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], Manager.dictionary["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.dictionary["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = "None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::None"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = 0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = False
    if remove:
        del chest_to_seed[container]
    
def patch_enemy_entry(item_type, item_rate, container):
    #Randomize enemy drops in a varied fashion while slightly favouring one item type
    #Also randomize the amount of drops so that it isn't always 4 per enemy
    if item_type == "CookingMat":
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = 0.0
    elif item_type == "StandardMat":
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = 0.0
    elif item_type == "EnemyMat":
        if random.randint(1, 3) > 1 and Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.dictionary["ItemDrop"]["CookingMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.dictionary["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.dictionary["ItemDrop"]["StandardMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.dictionary["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = 0.0
        if random.randint(1, 3) > 1 and Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.dictionary["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        else:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = 0
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = 0.0

def unlock_all_quest():
    #Make all quests available from the start
    #Note that picking a memento or catering quest commits you to that quest until you complete it
    for i in range(20):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedAreaID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedItemID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["NeedBossID"] = "None"
    for i in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedAreaID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedItemID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["NeedBossID"] = "None"
    for i in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedQuestID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedAreaID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedItemID"] = "None"
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["NeedBossID"] = "None"

def rand_quest_requirement():
    #Enemy quests
    all_enemies = list(Manager.dictionary["EnemyLocation"])
    enemy_requirement = []
    for i in range(19):
        chosen = any_pick(all_enemies, True, "None")
        #Don't pick IGA, Miriam, or shard candles
        while chosen[0] != "N" or chosen in ["N2013", "N0000"]:
            chosen = any_pick(all_enemies, True, "None")
        enemy_requirement.append(chosen)
    #Order them by level, appending bosses at the end
    level_to_enemy = {}
    level_to_boss  = {}
    index = 0
    for i in enemy_requirement:
        if Manager.is_enemy(i)["Boss"]:
            level_to_boss[Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]*100 + index] = i
        else:
            level_to_enemy[Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]*100 + index] = i
        index += 1
    level_to_enemy = OrderedDict(sorted(level_to_enemy.items()))
    level_to_boss  = OrderedDict(sorted(level_to_boss.items()))
    level_to_enemy.update(level_to_boss)
    #Update requirement
    for i in range(19):
        enemy = list(level_to_enemy.values())[i]
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["Enemy01"] = enemy
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemyNum01"] = len(Manager.dictionary["EnemyLocation"][enemy]["NormalModeRooms"])
        enemy_room = ""
        for e in Manager.dictionary["EnemyLocation"][enemy]["NormalModeRooms"]:
            enemy_room += e + ","
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Enemy" + "{:02d}".format(i + 1)]["EnemySpawnLocations"] = enemy_room[:-1]
    #Memento quests
    for i in range(15):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Memento" + "{:02d}".format(i + 1)]["Item01"] = any_pick(Manager.dictionary["QuestRequirement"]["Memento"]["ItemPool"], True, "None")
    #Catering quests
    for i in range(21):
        Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["Item01"] = any_pick(Manager.dictionary["QuestRequirement"]["Catering"]["ItemPool"], True, "None")

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
        if Manager.dictionary["ItemDrop"][item_type]["ChestColor"] == "Blue":
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], Manager.dictionary["ItemDrop"][item_type]["IsUnique"], item_type)
            if Manager.dictionary["ItemDrop"][item_type]["IsUnique"]:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = 1
            else:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]*9
        elif Manager.dictionary["ItemDrop"][item_type]["ChestColor"] == "Red":
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = "Money"
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], Manager.dictionary["ItemDrop"][item_type]["IsUnique"], item_type)
        else:
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = any_pick(Manager.dictionary["ItemDrop"][item_type]["ItemPool"], Manager.dictionary["ItemDrop"][item_type]["IsUnique"], item_type)
            if Manager.dictionary["ItemDrop"][item_type]["IsUnique"]:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = 1
            else:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.dictionary["ItemDrop"][item_type]["ItemQuantity"]*3
    invert_ratio()

def catering_quest_info():
    #Update catering quests descriptions so that it is possible to tell what Susie wants
    for i in range(21):
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Name" + "{:02d}".format(i + 1)]    = Manager.dictionary["ItemTranslation"][Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["Item01"]]
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Caption" + "{:02d}".format(i + 1)] = "She says she wants to eat until she explodes."

def all_hair_in_shop():
    #Add all hair apparents to the shop for 100G
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["buyPrice"]  = 100
    Manager.datatable["PB_DT_ItemMaster"]["Worldfashionfirstissue"]["Producted"] = "Event_01_001_0000"
    shop_skip_list.append("Worldfashionfirstissue")
    for i in range(11):
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(i + 2)]["buyPrice"]  = 100
        Manager.datatable["PB_DT_ItemMaster"]["WorldfashionNo" + "{:02d}".format(i + 2)]["Producted"] = "Event_01_001_0000"
        shop_skip_list.append("WorldfashionNo" + "{:02d}".format(i + 2))

def no_key_in_shop():
    #Remove all key items from shop
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["DiscountCard"]["sellPrice"] = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["buyPrice"]  = 0
    Manager.datatable["PB_DT_ItemMaster"]["MonarchCrown"]["sellPrice"] = 0

def rand_shop_pool():
    #Unchanged items are guaranteed so update the shop number
    for i in Manager.dictionary["ItemDrop"]:
        for e in shop_skip_list:
            if e in Manager.dictionary["ItemDrop"][i]["ItemPool"]:
                Manager.dictionary["ItemDrop"][i]["ShopRatio"] -= 1
    #Reset shop event
    for i in Manager.datatable["PB_DT_ItemMaster"]:
        if i in shop_skip_list:
            continue
        Manager.datatable["PB_DT_ItemMaster"][i]["Producted"] = "None"
    #Assign random events
    for i in Manager.dictionary["ItemDrop"]:
        for e in range(Manager.dictionary["ItemDrop"][i]["ShopRatio"]):
            if Manager.dictionary["ItemDrop"][i]["ItemPool"]:
                chosen = any_pick(Manager.dictionary["ItemDrop"][i]["ItemPool"], True, "None")
                while Manager.datatable["PB_DT_ItemMaster"][chosen]["buyPrice"] == 0 or chosen in shop_skip_list:
                    chosen = any_pick(Manager.dictionary["ItemDrop"][i]["ItemPool"], True, "None")
                Manager.datatable["PB_DT_ItemMaster"][chosen]["Producted"] = random.choice(event_type)

def rand_shop_price(scale):
    price_list = Manager.create_weighted_list(100, 1, 10000, 1, 4)
    for i in Manager.datatable["PB_DT_ItemMaster"]:
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] == 0 or i in shop_skip_list:
            continue
        #Buy
        buy_price = Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"]
        sell_ratio = Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"]/buy_price
        multiplier = random.choice(price_list)/100
        Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = int(buy_price*multiplier)
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] > 10:
            Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = round(Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"]/10)*10
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] < 1:
            Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] = 1
        #Sell
        if not scale:
            multiplier = random.choice(price_list)/100
        Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] = int(buy_price*multiplier*sell_ratio)
        if Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] < 1:
            Manager.datatable["PB_DT_ItemMaster"][i]["sellPrice"] = 1

def replace_silver_bromide():
    #Find Silver Bromide and replace it by the Certification Board
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        if Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"] == "Silverbromide":
            Manager.datatable["PB_DT_DropRateMaster"][i]["RareItemId"] = "Certificationboard"

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for i in Manager.dictionary["BossToMaterial"]:
        shard_name = Manager.datatable["PB_DT_DropRateMaster"][i + "_Shard"]["ShardId"]
        shard_type = Manager.datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
        shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
        for e in Manager.dictionary["BossToMaterial"][i]:
            Manager.change_material_hsv(e, Manager.dictionary["BossToMaterial"][i][e], shard_hsv)

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
    for i in Manager.dictionary["ItemDrop"]:
        if Manager.dictionary["ItemDrop"][i]["IsUnique"]:
            continue
        ratio = []
        new_list = []
        duplicate = 1
        for e in range(len(Manager.dictionary["ItemDrop"][i]["ItemPool"]) - 1):
            previous = Manager.dictionary["ItemDrop"][i]["ItemPool"][e]
            current = Manager.dictionary["ItemDrop"][i]["ItemPool"][e + 1]
            if current == previous:
                duplicate += 1
            else:
                ratio.append(duplicate)
                duplicate = 1
            if e == len(Manager.dictionary["ItemDrop"][i]["ItemPool"]) - 2:
                ratio.append(duplicate)
            e += 1
        max_ratio = max(ratio)
        Manager.dictionary["ItemDrop"][i]["ItemPool"] = list(dict.fromkeys(Manager.dictionary["ItemDrop"][i]["ItemPool"]))
        for e in range(len(Manager.dictionary["ItemDrop"][i]["ItemPool"])):
            for o in range(abs(ratio[e] - (max_ratio + 1))):
                new_list.append(Manager.dictionary["ItemDrop"][i]["ItemPool"][e])
        Manager.dictionary["ItemDrop"][i]["ItemPool"] = new_list

def create_log(seed, map):
    #Log compatible with the map editor to show key item locations
    name, extension = os.path.splitext(map)
    log = {}
    log["Seed"] = seed
    log["Map"]  = name.split("\\")[-1]
    log["Key"]  = {}
    for i in key_order:
        if i in key_items:
            log["Key"][Manager.dictionary["ItemTranslation"][i]] = [chest_to_room(key_item_to_location[i])]
        if i in key_shards:
            log["Key"][Manager.dictionary["ShardTranslation"][i]] = enemy_to_room(key_shard_to_location[i])
    return log

def create_log_string(seed, map):
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
            log_string += "  " + Manager.dictionary["ItemTranslation"][i] + ": " + key_item_to_location[i] + "\n"
        if i in key_shards:
            log_string += "  " + Manager.dictionary["ShardTranslation"][i] + ": " + Manager.dictionary["EnemyTranslation"][key_shard_to_location[i]] + "\n"
    return log_string