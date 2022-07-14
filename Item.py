import Manager
import math
import random
import os
import copy
from collections import OrderedDict

def init():
    #Declare variables
    global chest_to_seed
    chest_to_seed = {
        "PotionMaterial": "Treasurebox_SIP000_Tutorial",
        "Qu07_Last": "Qu07_Last",
        "Swordsman": "Swordsman",
        "Treasurebox_SIP000_Tutorial": "Treasurebox_SIP011(4)",
        "Treasurebox_SIP002(1)": "Treasurebox_SIP005(2)",
        "Treasurebox_SIP003(1)": "Treasurebox_LIB009(1)",
        "Treasurebox_SIP004(1)": "Treasurebox_GDN006(5)",
        "Treasurebox_SIP005(1)": "Treasurebox_ENT002(1)",
        "Treasurebox_SIP005(2)": "Treasurebox_SIP002(1)",
        "Treasurebox_SIP006(1)": "Treasurebox_LIB022(1)",
        "Treasurebox_SIP007(1)": "Treasurebox_KNG017(1)",
        "Treasurebox_SIP007(2)": "Treasurebox_SIP011(3)",
        "Treasurebox_SIP009(1)": "Treasurebox_JPN011(1)",
        "Treasurebox_SIP011(1)": "Treasurebox_SIP014(1)",
        "Treasurebox_SIP011(2)": "Treasurebox_TWR015(1)",
        "Treasurebox_SIP011(3)": "Treasurebox_TWR000(3)",
        "Treasurebox_SIP011(4)": "PotionMaterial",
        "Treasurebox_SIP012(1)": "Treasurebox_TAR007(1)",
        "Treasurebox_SIP013(1)": "Treasurebox_RVA001(2)",
        "Treasurebox_SIP014(1)": "Treasurebox_UGD051(1)",
        "Treasurebox_SIP015(1)": "Treasurebox_ARC000(1)",
        "Treasurebox_SIP016(1)": "Treasurebox_SAN024(1)",
        "Treasurebox_SIP017(1)": "Treasurebox_RVA011(2)",
        "Treasurebox_SIP018(1)": "Treasurebox_SIP016(1)",
        "Treasurebox_SIP019(1)": "Treasurebox_UGD025(1)",
        "Treasurebox_SIP020(1)": "Treasurebox_RVA015(1)",
        "Treasurebox_SIP021(2)": "Treasurebox_BIG011(1)",
        "Treasurebox_SIP024(1)": "Treasurebox_ENT014(2)",
        "Treasurebox_SIP024(2)": "Treasurebox_TWR009(1)",
        "Treasurebox_SIP025(1)": "Treasurebox_UGD009(4)",
        "Treasurebox_SIP025(2)": "Treasurebox_SAN015(2)",
        "Treasurebox_SIP026(1)": "Treasurebox_SAN005(1)",
        "Treasurebox_VIL001(1)": "Treasurebox_UGD044(2)",
        "Treasurebox_VIL003(1)": "Treasurebox_LIB009(2)",
        "Treasurebox_VIL005(1)": "Treasurebox_JPN018(1)",
        "Treasurebox_VIL006(1)": "Treasurebox_TWR017(5)",
        "Treasurebox_VIL006(2)": "Treasurebox_VIL006(2)",
        "Treasurebox_VIL006(3)": "Treasurebox_UGD044(1)",
        "Treasurebox_VIL006(4)": "Treasurebox_ENT020(2)",
        "Treasurebox_VIL007(1)": "Treasurebox_SAN003(1)",
        "Treasurebox_VIL008(1)": "Treasurebox_TRN002(3)",
        "Treasurebox_VIL008(2)": "Treasurebox_SAN003(5)",
        "Treasurebox_VIL010(1)": "Treasurebox_ENT015(1)",
        "Treasurebox_ENT002(1)": "Treasurebox_TWR019(2)",
        "Treasurebox_ENT002(2)": "Treasurebox_ENT018(1)",
        "Treasurebox_ENT002(3)": "Treasurebox_GDN012(1)",
        "Treasurebox_ENT004(1)": "Treasurebox_VIL001(1)",
        "Treasurebox_ENT005(1)": "Treasurebox_ENT005(1)",
        "Treasurebox_ENT005(2)": "Treasurebox_TWR018(8)",
        "Treasurebox_ENT007(1)": "Treasurebox_VIL008(2)",
        "Treasurebox_ENT007(2)": "Treasurebox_UGD052(1)",
        "Treasurebox_ENT007(3)": "Treasurebox_SIP007(1)",
        "Treasurebox_ENT009(1)": "Treasurebox_GDN004(1)",
        "Treasurebox_ENT011(1)": "Treasurebox_SAN009(2)",
        "Treasurebox_ENT014(1)": "Treasurebox_SAN003(3)",
        "Treasurebox_ENT014(2)": "Treasurebox_SAN016(5)",
        "Treasurebox_ENT014(3)": "Treasurebox_SND016(1)",
        "Treasurebox_ENT018(1)": "Treasurebox_SND011(1)",
        "Treasurebox_ENT018(2)": "Treasurebox_BIG002(1)",
        "Treasurebox_ENT020(1)": "Treasurebox_GDN006(1)",
        "Treasurebox_ENT020(2)": "Treasurebox_ARC004(1)",
        "Treasurebox_ENT021(1)": "Treasurebox_ARC006(2)",
        "Treasurebox_ENT022(1)": "Treasurebox_ENT020(1)",
        "Treasurebox_ENT024(1)": "Treasurebox_LIB032(1)",
        "Treasurebox_ENT024(2)": "Treasurebox_ARC007(2)",
        "Treasurebox_ENT024(3)": "Treasurebox_BIG012(1)",
        "Treasurebox_GDN002(1)": "Treasurebox_TWR019(4)",
        "Treasurebox_GDN004(1)": "Treasurebox_TRN002(4)",
        "Treasurebox_GDN006(1)": "Treasurebox_LIB040(1)",
        "Treasurebox_GDN006(2)": "Treasurebox_PureMiriam_Hair",
        "Treasurebox_GDN006(3)": "Treasurebox_SAN019(3)",
        "Treasurebox_GDN006(4)": "Treasurebox_VIL008(1)",
        "Treasurebox_GDN006(5)": "Treasurebox_ICE003(1)",
        "Treasurebox_GDN007(1)": "Treasurebox_GDN007(1)",
        "Treasurebox_GDN009(1)": "Treasurebox_SAN017(1)",
        "Treasurebox_GDN009(2)": "Treasurebox_SIP025(2)",
        "Treasurebox_GDN010(1)": "Treasurebox_ICE006(1)",
        "Treasurebox_GDN012(1)": "Treasurebox_ENT004(1)",
        "Treasurebox_GDN012(2)": "Treasurebox_GDN009(2)",
        "Treasurebox_GDN013(1)": "Treasurebox_TWR004(1)",
        "Treasurebox_GDN013(2)": "Treasurebox_KNG002(1)",
        "Treasurebox_GDN013(3)": "Treasurebox_SAN021(4)",
        "Treasurebox_GDN013(4)": "Treasurebox_UGD038(1)",
        "Treasurebox_GDN014(1)": "Treasurebox_UGD049(1)",
        "Treasurebox_SAN003(1)": "Treasurebox_SIP011(1)",
        "Treasurebox_SAN003(2)": "Treasurebox_ARC003(1)",
        "Treasurebox_SAN003(3)": "Treasurebox_ENT008(1)",
        "Treasurebox_SAN003(4)": "Treasurebox_BIG006(5)",
        "Treasurebox_SAN003(5)": "Treasurebox_TWR019(3)",
        "Treasurebox_SAN003(6)": "Treasurebox_KNG018(3)",
        "Treasurebox_SAN003(7)": "Treasurebox_UGD033(1)",
        "Treasurebox_SAN003(8)": "Treasurebox_TWR018(7)",
        "Treasurebox_SAN005(1)": "Treasurebox_SND003(1)",
        "Treasurebox_SAN005(2)": "Treasurebox_SAN003(8)",
        "Treasurebox_SAN009(1)": "Treasurebox_TWR018(2)",
        "Treasurebox_SAN009(2)": "Treasurebox_UGD053(1)",
        "Treasurebox_SAN013(1)": "Treasurebox_ARC006(1)",
        "Treasurebox_SAN013(2)": "Treasurebox_ENT007(1)",
        "Treasurebox_SAN014(1)": "Treasurebox_SIP004(1)",
        "Treasurebox_SAN015(2)": "Treasurebox_SND008(2)",
        "Treasurebox_SAN015(3)": "Treasurebox_TRN002(1)",
        "Treasurebox_SAN016(1)": "Treasurebox_SND000(1)",
        "Treasurebox_SAN016(2)": "Treasurebox_UGD035(1)",
        "Treasurebox_SAN016(3)": "Treasurebox_RVA001(1)",
        "Treasurebox_SAN016(4)": "Treasurebox_SAN016(4)",
        "Treasurebox_SAN016(5)": "Treasurebox_SAN003(6)",
        "Treasurebox_SAN017(1)": "Treasurebox_ENT024(1)",
        "Treasurebox_SAN019(1)": "Treasurebox_JPN004(1)",
        "Treasurebox_SAN019(2)": "Treasurebox_SIP025(1)",
        "Treasurebox_SAN019(3)": "Treasurebox_SAN013(2)",
        "Treasurebox_SAN020(1)": "Treasurebox_SAN003(7)",
        "Treasurebox_SAN021(1)": "Treasurebox_ICE013(1)",
        "Treasurebox_SAN021(2)": "Treasurebox_SAN021(2)",
        "Treasurebox_SAN021(3)": "Treasurebox_GDN002(1)",
        "Treasurebox_SAN021(4)": "Treasurebox_GDN006(3)",
        "Treasurebox_SAN021(5)": "Treasurebox_KNG017(3)",
        "Treasurebox_SAN024(1)": "Treasurebox_SIP024(2)",
        "Treasurebox_TWR000(1)": "Treasurebox_RVA003(2)",
        "Treasurebox_TWR003(1)": "Treasurebox_ENT012(1)",
        "Treasurebox_TWR004(1)": "Treasurebox_GDN013(1)",
        "Treasurebox_TWR005(1)": "Treasurebox_LIB011(1)",
        "Treasurebox_TWR006(1)": "Treasurebox_UGD023(1)",
        "Treasurebox_TWR008(1)": "Treasurebox_BIG014(1)",
        "Treasurebox_TWR009(1)": "Treasurebox_SIP018(1)",
        "Treasurebox_TWR010(1)": "Treasurebox_KNG005(1)",
        "Treasurebox_TWR012(1)": "Treasurebox_UGD018(1)",
        "Treasurebox_TWR013(1)": "Treasurebox_ENT014(1)",
        "Treasurebox_TWR016(1)": "Treasurebox_SAN005(4)",
        "Treasurebox_TWR017(1)": "Treasurebox_KNG012(1)",
        "Treasurebox_TWR017(2)": "Treasurebox_BIG005(1)",
        "Treasurebox_TWR017(3)": "Treasurebox_ENT007(2)",
        "Treasurebox_TWR017(4)": "Treasurebox_RVA006(1)",
        "Treasurebox_TWR017(5)": "Treasurebox_LIB043(1)",
        "Treasurebox_TWR017(6)": "Treasurebox_SAN021(3)",
        "Treasurebox_TWR017(7)": "Treasurebox_TRN002(2)",
        "Treasurebox_TWR018(1)": "Treasurebox_GDN010(1)",
        "Treasurebox_TWR018(2)": "Treasurebox_UGD009(2)",
        "Treasurebox_TWR018(3)": "Treasurebox_SND018(1)",
        "Treasurebox_TWR018(4)": "Treasurebox_SAN003(2)",
        "Treasurebox_TWR018(5)": "Treasurebox_PureMiriam_Sword",
        "Treasurebox_TWR018(6)": "Treasurebox_GDN009(1)",
        "Treasurebox_TWR018(7)": "Treasurebox_KNG018(2)",
        "Treasurebox_TWR018(8)": "Treasurebox_GDN013(3)",
        "Treasurebox_TWR019(1)": "Treasurebox_SAN021(1)",
        "Treasurebox_TWR019(2)": "Treasurebox_SAN014(1)",
        "Treasurebox_TWR019(4)": "Treasurebox_GDN012(2)",
        "Treasurebox_LIB001(1)": "Treasurebox_UGD047(1)",
        "Treasurebox_LIB002(1)": "Treasurebox_TWR017(4)",
        "Treasurebox_LIB007(1)": "Treasurebox_GDN014(1)",
        "Treasurebox_LIB009(1)": "Treasurebox_VIL006(1)",
        "Treasurebox_LIB009(2)": "Treasurebox_VIL003(1)",
        "Treasurebox_LIB011(1)": "Treasurebox_SIP006(1)",
        "Treasurebox_LIB012(1)": "Treasurebox_ICE003(2)",
        "Treasurebox_LIB017(1)": "Treasurebox_JPN000(1)",
        "Treasurebox_LIB019(1)": "Treasurebox_LIB002(1)",
        "Treasurebox_LIB022(1)": "Treasurebox_SIP026(1)",
        "Treasurebox_LIB030(1)": "Treasurebox_ARC005(1)",
        "Treasurebox_LIB032(1)": "Treasurebox_LIB019(1)",
        "Treasurebox_LIB033(1)": "Treasurebox_SAN009(3)",
        "Treasurebox_LIB040(1)": "Treasurebox_ENT022(1)",
        "Treasurebox_LIB043(1)": "Treasurebox_UGD010(1)",
        "Treasurebox_TRN002(1)": "Treasurebox_TWR017(7)",
        "Treasurebox_TRN002(2)": "Treasurebox_ENT024(2)",
        "Treasurebox_TRN002(3)": "Treasurebox_UGD003(3)",
        "Treasurebox_TRN002(4)": "Treasurebox_ENT007(3)",
        "Treasurebox_TRN002(5)": "Treasurebox_JPN010(2)",
        "Treasurebox_KNG002(1)": "Treasurebox_UGD040(1)",
        "Treasurebox_KNG002(2)": "Treasurebox_TWR008(1)",
        "Treasurebox_KNG003(1)": "Treasurebox_ENT002(2)",
        "Treasurebox_KNG006(1)": "Treasurebox_JPN001(1)",
        "Treasurebox_KNG010(1)": "Treasurebox_UGD012(1)",
        "Treasurebox_KNG011(1)": "Treasurebox_KNG018(4)",
        "Treasurebox_KNG012(1)": "Treasurebox_ENT009(1)",
        "Treasurebox_KNG012(2)": "Treasurebox_UGD009(1)",
        "Treasurebox_KNG016(1)": "Treasurebox_UGD048(1)",
        "Treasurebox_KNG017(1)": "Treasurebox_ICE008(1)",
        "Treasurebox_KNG017(2)": "Treasurebox_TWR019(1)",
        "Treasurebox_KNG017(3)": "Treasurebox_ENT002(3)",
        "Treasurebox_KNG017(4)": "Treasurebox_UGD003(2)",
        "Treasurebox_KNG017(5)": "Treasurebox_KNG017(5)",
        "Treasurebox_KNG018(2)": "Treasurebox_KNG018(1)",
        "Treasurebox_KNG018(3)": "Treasurebox_LIB012(1)",
        "Treasurebox_KNG018(4)": "Treasurebox_KNG002(2)",
        "Treasurebox_KNG021(1)": "Treasurebox_RVA005(2)",
        "Treasurebox_KNG022(1)": "Treasurebox_UGD050(1)",
        "Treasurebox_UGD001(1)": "Treasurebox_KNG016(1)",
        "Treasurebox_UGD003(1)": "Treasurebox_SND005(1)",
        "Treasurebox_UGD003(2)": "Treasurebox_VIL006(3)",
        "Treasurebox_UGD003(3)": "Treasurebox_KNG017(4)",
        "Treasurebox_UGD003(4)": "Treasurebox_SND001(1)",
        "Treasurebox_UGD005(1)": "Treasurebox_ICE014(1)",
        "Treasurebox_UGD005(2)": "Treasurebox_SND021(1)",
        "Treasurebox_UGD007(1)": "Treasurebox_GDN006(2)",
        "Treasurebox_UGD009(1)": "Treasurebox_LIB018(1)",
        "Treasurebox_UGD009(2)": "Treasurebox_ENT011(1)",
        "Treasurebox_UGD009(3)": "Treasurebox_UGD048(2)",
        "Treasurebox_UGD009(4)": "Treasurebox_SIP019(1)",
        "Treasurebox_UGD010(1)": "Treasurebox_SAN013(1)",
        "Treasurebox_UGD011(1)": "Treasurebox_UGD011(1)",
        "Treasurebox_UGD021(1)": "Treasurebox_BIG006(1)",
        "Treasurebox_UGD024(1)": "Treasurebox_UGD005(1)",
        "Treasurebox_UGD024(2)": "Treasurebox_UGD020(1)",
        "Treasurebox_UGD024(3)": "Treasurebox_UGD024(3)",
        "Treasurebox_UGD025(1)": "Treasurebox_BIG006(3)",
        "Treasurebox_UGD025(2)": "Treasurebox_RVA004(1)",
        "Treasurebox_UGD025(3)": "Treasurebox_UGD036(1)",
        "Treasurebox_UGD027(1)": "Treasurebox_UGD032(1)",
        "Treasurebox_UGD030(1)": "Treasurebox_SND019(1)",
        "Treasurebox_UGD031(1)": "Treasurebox_KNG022(1)",
        "Treasurebox_UGD031(2)": "Treasurebox_TWR017(3)",
        "Treasurebox_UGD036(1)": "Treasurebox_ICE011(1)",
        "Treasurebox_UGD036(2)": "Treasurebox_TWR018(1)",
        "Treasurebox_UGD038(1)": "Treasurebox_UGD045(1)",
        "Treasurebox_UGD040(1)": "Treasurebox_BIG010(1)",
        "Treasurebox_UGD041(1)": "Treasurebox_TAR009(1)",
        "Treasurebox_UGD042(1)": "Treasurebox_SND026(1)",
        "Treasurebox_UGD044(1)": "Treasurebox_UGD047(2)",
        "Treasurebox_UGD044(2)": "Treasurebox_TRN002(5)",
        "Treasurebox_UGD046(1)": "Treasurebox_UGD046(1)",
        "Treasurebox_UGD046(2)": "Treasurebox_ICE008(2)",
        "Treasurebox_UGD047(2)": "Treasurebox_KNG021(3)",
        "Treasurebox_UGD048(1)": "Treasurebox_SND008(1)",
        "Treasurebox_UGD050(1)": "Treasurebox_UGD025(2)",
        "Treasurebox_UGD051(1)": "Treasurebox_TWR017(1)",
        "Treasurebox_UGD052(1)": "Treasurebox_ENT011(2)",
        "Treasurebox_UGD052(2)": "Treasurebox_SND010(1)",
        "Treasurebox_UGD053(1)": "Treasurebox_JPN005(1)",
        "Treasurebox_UGD054(1)": "Treasurebox_JPN008(1)",
        "Treasurebox_UGD056(1)": "Treasurebox_JPN002(1)",
        "Treasurebox_SND002(1)": "Treasurebox_SAN005(3)",
        "Treasurebox_SND003(1)": "Treasurebox_TWR005(1)",
        "Treasurebox_SND004(1)": "Treasurebox_KNG021(1)",
        "Treasurebox_SND006(1)": "Treasurebox_UGD031(1)",
        "Treasurebox_SND008(1)": "Treasurebox_SAN019(1)",
        "Treasurebox_SND008(2)": "Treasurebox_KNG021(2)",
        "Treasurebox_SND009(1)": "Treasurebox_SIP009(1)",
        "Treasurebox_SND010(1)": "Treasurebox_SND014(1)",
        "Treasurebox_SND010(2)": "Treasurebox_TWR017(6)",
        "Treasurebox_SND013(1)": "Treasurebox_JPN003(1)",
        "Treasurebox_SND015(1)": "Treasurebox_RVA014(1)",
        "Treasurebox_SND016(1)": "Treasurebox_ENT021(1)",
        "Treasurebox_SND017(1)": "Treasurebox_TAR003(1)",
        "Treasurebox_SND018(1)": "Treasurebox_BIG016(1)",
        "Treasurebox_SND019(1)": "Treasurebox_ICE010(1)",
        "Treasurebox_SND020(1)": "Treasurebox_RVA009(1)",
        "Treasurebox_SND024(1)": "Treasurebox_UGD057(1)",
        "Treasurebox_SND025(1)": "Treasurebox_RVA003(1)",
        "Treasurebox_ARC000(1)": "Treasurebox_UGD026(1)",
        "Treasurebox_ARC002(1)": "Treasurebox_UGD019(1)",
        "Treasurebox_ARC003(1)": "Treasurebox_UGD007(1)",
        "Treasurebox_ARC004(1)": "Treasurebox_BIG012(3)",
        "Treasurebox_ARC006(1)": "Treasurebox_SND006(1)",
        "Treasurebox_ARC006(2)": "Treasurebox_SIP024(1)",
        "Treasurebox_ARC007(1)": "Treasurebox_SIP003(1)",
        "Treasurebox_ARC007(2)": "Treasurebox_ENT014(3)",
        "Treasurebox_TAR001(1)": "Treasurebox_TAR005(1)",
        "Treasurebox_TAR002(1)": "N3106_2ND_Treasure",
        "Treasurebox_TAR006(1)": "Treasurebox_PureMiriam_Dress",
        "Treasurebox_TAR007(1)": "Treasurebox_ICE001(2)",
        "Treasurebox_TAR010(1)": "Treasurebox_UGD015(1)",
        "Treasurebox_JPN002(1)": "Treasurebox_UGD056(1)",
        "Treasurebox_JPN002(2)": "Treasurebox_JPN002(2)",
        "Treasurebox_JPN004(1)": "Treasurebox_TWR018(4)",
        "Treasurebox_JPN005(1)": "Treasurebox_TWR018(6)",
        "Treasurebox_JPN009(1)": "Treasurebox_UGD001(1)",
        "Treasurebox_JPN010(1)": "Treasurebox_SIP015(1)",
        "Treasurebox_JPN010(2)": "Treasurebox_SAN021(5)",
        "Treasurebox_JPN013(1)": "N3106_1ST_Treasure",
        "Treasurebox_JPN015(1)": "Treasurebox_SAN016(1)",
        "Treasurebox_JPN017(1)": "Treasurebox_VIL005(1)",
        "Treasurebox_JPN018(1)": "Treasurebox_ARC007(1)",
        "Treasurebox_RVA001(1)": "Treasurebox_ENT018(2)",
        "Treasurebox_RVA001(2)": "Treasurebox_SIP013(1)",
        "Treasurebox_RVA002(1)": "Treasurebox_UGD052(2)",
        "Treasurebox_RVA004(1)": "Treasurebox_JPN017(1)",
        "Treasurebox_RVA006(1)": "Treasurebox_JPN009(1)",
        "Treasurebox_RVA010(1)": "Treasurebox_UGD037(1)",
        "Treasurebox_RVA011(1)": "Treasurebox_RVA011(1)",
        "Treasurebox_RVA011(2)": "Treasurebox_VIL010(1)",
        "Treasurebox_RVA012(1)": "Treasurebox_SND027(1)",
        "Treasurebox_RVA015(1)": "Treasurebox_TWR003(1)",
        "Treasurebox_BIG002(1)": "Treasurebox_UGD022(1)",
        "Treasurebox_BIG005(1)": "Treasurebox_LIB042(1)",
        "Treasurebox_BIG006(1)": "Treasurebox_SND009(1)",
        "Treasurebox_BIG006(2)": "Treasurebox_KNG017(2)",
        "Treasurebox_BIG006(3)": "Treasurebox_SAN019(2)",
        "Treasurebox_BIG006(4)": "Treasurebox_BIG008(1)",
        "Treasurebox_BIG006(5)": "Treasurebox_SAN005(2)",
        "Treasurebox_BIG006(6)": "Treasurebox_ENT005(2)",
        "Treasurebox_BIG007(1)": "Treasurebox_SND012(1)",
        "Treasurebox_BIG008(1)": "Treasurebox_BIG006(4)",
        "Treasurebox_BIG010(1)": "Treasurebox_UGD029(1)",
        "Treasurebox_BIG011(1)": "Treasurebox_SIP021(2)",
        "Treasurebox_BIG012(1)": "Treasurebox_SIP017(1)",
        "Treasurebox_BIG012(2)": "Treasurebox_UGD039(1)",
        "Treasurebox_BIG012(3)": "Treasurebox_SND010(2)",
        "Treasurebox_BIG013(1)": "Treasurebox_KNG003(1)",
        "Treasurebox_BIG014(1)": "Treasurebox_KNG011(1)",
        "Treasurebox_BIG016(1)": "Treasurebox_JPN010(1)",
        "Treasurebox_BIG016(2)": "Treasurebox_TWR012(1)",
        "Treasurebox_BIG016(3)": "Treasurebox_GDN013(4)",
        "Treasurebox_ICE001(1)": "Treasurebox_TWR006(2)",
        "Treasurebox_ICE001(2)": "Treasurebox_UGD036(2)",
        "Treasurebox_ICE002(1)": "Treasurebox_SND007(1)",
        "Treasurebox_ICE003(1)": "Treasurebox_SIP005(1)",
        "Treasurebox_ICE003(2)": "Treasurebox_VIL006(4)",
        "Treasurebox_ICE006(1)": "Treasurebox_UGD016(1)",
        "Treasurebox_ICE008(1)": "Treasurebox_VIL007(1)",
        "Treasurebox_ICE008(2)": "Treasurebox_RVA005(1)",
        "Treasurebox_ICE010(1)": "Treasurebox_ENT024(3)",
        "Treasurebox_ICE011(1)": "Treasurebox_GDN013(2)",
        "Treasurebox_ICE013(1)": "Treasurebox_BIG006(2)",
        "Treasurebox_ICE014(1)": "Treasurebox_SND020(1)",
        "Treasurebox_PureMiriam_Hair": "Treasurebox_SAN009(1)",
        "Treasurebox_PureMiriam_Tiare": "Treasurebox_PureMiriam_Tiare",
        "Treasurebox_PureMiriam_Dress": "Treasurebox_TAR006(1)",
        "Treasurebox_PureMiriam_Sword": "Treasurebox_SAN000(1)",
        "Wall_SIP004(1)": "Wall_BIG012(1)",
        "Wall_SIP009(1)": "Wall_LIB004(1)",
        "Wall_SIP014(1)": "Wall_UGD031(1)",
        "Wall_SIP016(1)": "Wall_ICE003(1)",
        "Wall_ENT002(1)": "Wall_TRN005(1)",
        "Wall_ENT012(1)": "Wall_TWR013(1)",
        "Wall_GDN006(1)": "Wall_GDN006(1)",
        "Wall_SAN000(1)": "Wall_UGD006(1)",
        "Wall_SAN005(1)": "Wall_RVA011(1)",
        "Wall_SAN019(1)": "Wall_LIB025(1)",
        "Wall_KNG000(1)": "Wall_SND001(1)",
        "Wall_KNG007(1)": "Wall_RVA003(1)",
        "Wall_LIB004(1)": "Wall_ICE010(1)",
        "Wall_LIB019(1)": "Wall_UGD012(1)",
        "Wall_LIB025(1)": "Wall_TWR006(1)",
        "Wall_TWR006(1)": "Wall_UGD020(1)",
        "Wall_TWR013(1)": "Wall_ENT012(1)",
        "Wall_TWR016(1)": "Wall_TWR016(1)",
        "Wall_TRN005(1)": "Wall_SIP009(1)",
        "Wall_UGD000(1)": "Wall_ENT002(1)",
        "Wall_UGD003(1)": "Wall_UGD003(1)",
        "Wall_UGD006(1)": "Wall_SND019(1)",
        "Wall_UGD012(1)": "Wall_SAN005(1)",
        "Wall_UGD020(1)": "Wall_BIG016(1)",
        "Wall_UGD031(1)": "Wall_SIP014(1)",
        "Wall_UGD037(1)": "Wall_ICE017(1)",
        "Wall_UGD046(1)": "Wall_TAR007(1)",
        "Wall_UGD056(1)": "Wall_UGD056(1)",
        "Wall_SND001(1)": "Wall_SAN019(1)",
        "Wall_SND019(1)": "Wall_KNG007(1)",
        "Wall_TAR007(1)": "Wall_UGD046(1)",
        "Wall_JPN011(1)": "Wall_KNG000(1)",
        "Wall_JPN013(1)": "Wall_JPN013(1)",
        "Wall_RVA011(1)": "Wall_SIP016(1)",
        "Wall_BIG002(1)": "Wall_BIG002(1)",
        "Wall_BIG012(1)": "Wall_UGD000(1)",
        "Wall_BIG016(1)": "Wall_JPN011(1)",
        "Wall_ICE003(1)": "Wall_LIB019(1)",
        "Wall_ICE010(1)": "Wall_SIP004(1)",
        "Wall_ICE017(1)": "Wall_SAN000(1)",
        "N3106_1ST_Treasure": "Treasurebox_ARC002(1)",
        "N3106_2ND_Treasure": "Treasurebox_KNG006(1)"
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
    boss_rooms = [
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
    #8 Bit Nightmare is always gonna be connected to Hall of Termination regardless of map
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
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Bloodsteel"]           = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Swordsman"]            = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Silverbromide"]        = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker1"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker2"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker3"]         = False
    Manager.mod_data["MapLogic"]["m51EBT_000"]["Keyofbacker4"]         = False
    #Same goes for Kingdom 2 Crown's connection to the train
    #Also add Crown of Creation to the logic manually
    for i in Manager.mod_data["MapLogic"]:
        Manager.mod_data["MapLogic"][i]["MonarchCrown"] = False
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
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Bloodsteel"]           = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Swordsman"]            = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Silverbromide"]        = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["BreastplateofAguilar"] = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker1"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker2"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker3"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["Keyofbacker4"]         = False
    Manager.mod_data["MapLogic"]["m19K2C_000"]["MonarchCrown"]         = True
    #Benjamin's last reward appears if you've completed all his quests which is not guaranteed to be possible early on
    #Gebel's Glasses chest only appears if you to get 1 copy of every shard
    #OD can only be fought if the Tome of Conquest was obtained
    #Make sure none of these are required
    if Manager.mod_data["MapLogic"]["m18ICE_019"]["GateRoom"]:
        Manager.mod_data["MapLogic"]["m02VIL_003"]["NearestGate"]      = ["m18ICE_019"]
        Manager.mod_data["MapLogic"]["m02VIL_005"]["NearestGate"]      = ["m18ICE_019"]
        Manager.mod_data["MapLogic"]["m18ICE_004"]["NearestGate"]      = ["m18ICE_019"]
    else:
        Manager.mod_data["MapLogic"]["m02VIL_003"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["MapLogic"]["m18ICE_019"]["NearestGate"])
        Manager.mod_data["MapLogic"]["m02VIL_005"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["MapLogic"]["m18ICE_019"]["NearestGate"])
        Manager.mod_data["MapLogic"]["m18ICE_004"]["NearestGate"]      = copy.deepcopy(Manager.mod_data["MapLogic"]["m18ICE_019"]["NearestGate"])

def hard_enemy_logic():
    #On hard mode some rooms have extra enemies so update the location info
    for i in Manager.mod_data["EnemyLocation"]:
        Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"].extend(Manager.mod_data["EnemyLocation"][i]["HardModeRooms"])
    #Dulla heads can also be replaced with maledictions so adapt for that
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m07LIB_029")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_005")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m08TWR_013")
    Manager.mod_data["EnemyLocation"]["N3090"]["NormalModeRooms"].remove("m11UGD_013")

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
    while "Gebelsglasses" in Manager.mod_data["ItemDrop"]["Accessory"]["ItemPool"]:
        Manager.mod_data["ItemDrop"]["Accessory"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in Manager.mod_data["ItemDrop"]["Headgear"]["ItemPool"]:
        Manager.mod_data["ItemDrop"]["Headgear"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"]:
        Manager.mod_data["QuestRequirement"]["Memento"]["ItemPool"].remove("Recyclehat")

def give_shortcut():
    #Start the player with all shortcut slots since it is a quality of life more than an ability
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemId"] = "Shortcut"
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemQuantity"] = 7
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareItemRate"] = 100.0
    while "Shortcut" in Manager.mod_data["ShardDrop"]["ItemPool"]:
        Manager.mod_data["ShardDrop"]["ItemPool"].remove("Shortcut")
    
def give_eye():
    #Start the player with Detective's Eye so that missing breakable walls isn't an issue
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonItemId"] = "SkilledDetectiveeye"
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonItemQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["CommonRate"] = 100.0
    while "Detectiveeye" in Manager.mod_data["ShardDrop"]["ItemPool"]:
        Manager.mod_data["ShardDrop"]["ItemPool"].remove("Detectiveeye")

def give_extra(shard):
    #Start the player with a specific shard by putting it in the Village Key container
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientId"] = shard
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"]["VillageKeyBox"]["RareIngredientRate"] = 100.0
    while shard in Manager.mod_data["ShardDrop"]["ItemPool"]:
        Manager.mod_data["ShardDrop"]["ItemPool"].remove(shard)

def no_shard_craft():
    #If shards are randomized then disable the possiblity to manually craft shards so that they aren't always available
    #This is because there is currently no way to randomize which shards are craftable
    Manager.datatable["PB_DT_CraftMaster"]["HighJump"]["OpenKeyRecipeID"] = "Medal019"
    for i in Manager.datatable["PB_DT_CraftMaster"]:
        if Manager.datatable["PB_DT_CraftMaster"][i]["Type"] == "ECraftType::Craft" and Manager.datatable["PB_DT_CraftMaster"][i]["CraftItemId"] in Manager.mod_data["ShardDrop"]["ItemPool"]:
            Manager.datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "Medal019"

def deseema_fix():
    #If item are not randomized then quickly fix the aqua stream progression logic by giving Deseema increased drop chances
    Manager.datatable["PB_DT_DropRateMaster"]["N3022_Shard"]["DropSpecialFlags"] = "EDropSpecialFlag::DropShardOnce"
    Manager.datatable["PB_DT_DropRateMaster"]["N3022_Shard"]["ShardRate"]        = Manager.mod_data["ShardDrop"]["ItemRate"]*3

def key_logic():
    #Place all key items with logic so that the game is always beatable
    #The strategy used here is similar to the one implemented in vanilla where it reads from a room check file and loops through all the rooms based on that
    #The logic starts in all rooms that have no requirements until a gate is reached to determine which key item to place and so on
    #Since this has to adapt to different map layouts we cannot get away with using any "cheats" that are specific to the default map
    previous_gate = []
    requirement_to_gate = {}
    #Filling list with all room names
    all_rooms = list(Manager.mod_data["MapLogic"])
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
                #Increasing chances of late rooms
                #Otherwise early game areas are more likely to have everything
                gate_count = 1
                gate_list = copy.deepcopy(Manager.mod_data["MapLogic"][i]["NearestGate"])
                while gate_list:
                    nearest_gate = random.choice(gate_list)
                    for e in Manager.mod_data["MapLogic"]:
                        if e == nearest_gate:
                            gate_count += 1
                            gate_list = copy.deepcopy(Manager.mod_data["MapLogic"][e]["NearestGate"])
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
    #Convert room to container
    for i in key_item_to_location:
        key_item_to_location[i] = random.choice(room_to_chests(key_item_to_location[i]))
    for i in key_shard_to_location:
        enemy_list = room_to_enemies(key_shard_to_location[i])
        #Checking if enemy isn't already taken
        chosen_enemy = random.choice(enemy_list)
        while chosen_enemy in list(key_shard_to_location.values()):
            chosen_enemy = random.choice(enemy_list)
        #Changing
        key_shard_to_location[i] = chosen_enemy

def previous_in_nearest(previous_gate, nearest_gate):
    if not nearest_gate:
        return True
    else:
        for i in previous_gate:
            if i in nearest_gate:
                return True
    return False

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
        if chosen_room in list(key_item_to_location.values()) or chosen_room in list(key_shard_to_location.values()) or chosen_room in ["m01SIP_000", "m01SIP_020"]:
            continue
        #Checking if room has chest
        if chosen_item in key_items:
            if room_chest_check(chosen_room):
                break
        #Checking if room has enemy
        if chosen_item in key_shards:
            if room_enemy_check(chosen_room):
                break
    #Updating key location
    if chosen_item in key_items:
        key_item_to_location[chosen_item] = chosen_room
    if chosen_item in key_shards:
        key_shard_to_location[chosen_item] = chosen_room

def room_chest_check(room):
    for i in chest_to_seed:
        #Checking if chest corresponds to room
        if chest_to_room(i) == room:
            return True
    return False

def room_enemy_check(room):
    for i in Manager.mod_data["EnemyLocation"]:
        #Checking if enemy weilds a shard and is in room
        if not i in enemy_skip_list and Manager.mod_data["EnemyLocation"][i]["HasShard"] and room in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
            #Checking if enemy isn't in an already assigned room
            for e in key_shard_to_location:
                if key_shard_to_location[e] in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
                    return False
            return True
    return False

def room_to_chests(room):
    chest_list = []
    for i in chest_to_seed:
        if room[3:].replace("_", "") in i:
            chest_list.append(i)
        elif room in room_to_special_chest:
            if i in room_to_special_chest[room]:
                chest_list.append(i)
    return chest_list

def room_to_enemies(room):
    enemy_list = []
    for i in Manager.mod_data["EnemyLocation"]:
        if not i in enemy_skip_list and Manager.mod_data["EnemyLocation"][i]["HasShard"] and room in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
            #Increasing chances of uncommon enemies
            #Otherwise shards tend to mostly end up on bats an whatnot
            for o in range(math.ceil(36/len(Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]))):
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
    #Other keys
    for i in other_key:
        patch_key_item_entry(i, random.choice(list(chest_to_seed)))

def rand_overworld_shard():
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        #Check if the entry should be skipped
        id = i.split("_")
        if not id[0] in Manager.mod_data["EnemyLocation"]:
            continue
        if not Manager.mod_data["EnemyLocation"][id[0]]["HasShard"]:
            continue
        if "Treasure" in id:
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
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = any_pick(Manager.mod_data["ShardDrop"]["ItemPool"], True, "None")
            if Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] != 100.0:
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        else:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"]   = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["ShardId"]
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.datatable["PB_DT_DropRateMaster"][id[0] + "_Shard"]["ShardRate"]

def rand_overworld_pool(waystone):
    #Start chest
    patch_start_chest_entry()
    #Vepar chest
    if waystone:
        patch_key_item_entry("Waystone", "Treasurebox_SIP020(1)")
    else:
        patch_key_item_entry("Potion", "Treasurebox_SIP020(1)")
    #Johannes mats
    patch_chest_entry(random.choice(blue_chest_type), "PotionMaterial")
    #Final Benjamin reward
    patch_chest_entry(random.choice(green_chest_type), "Qu07_Last")
    #Ultimate Zangetsu reward
    patch_chest_entry(random.choice(green_chest_type), "Swordsman")
    #Carpenter's first chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_1ST_Treasure")
    #Carpenter's second chest
    patch_chest_entry(random.choice(green_chest_type), "N3106_2ND_Treasure")
    #Upgrades
    for i in range(30):
        patch_key_item_entry("MaxHPUP", random.choice(list(chest_to_seed)))
    for i in range(30):
        patch_key_item_entry("MaxMPUP", random.choice(list(chest_to_seed)))
    for i in range(22):
        patch_key_item_entry("MaxBulletUP", random.choice(list(chest_to_seed)))
    #Item pool
    for i in list(chest_to_seed):
        patch_chest_entry(random.choice(chest_type), i)
    #Enemy pool
    for i in Manager.datatable["PB_DT_DropRateMaster"]:
        id = i.split("_")
        if not id[0] in Manager.mod_data["EnemyLocation"]:
            continue
        if not Manager.mod_data["EnemyLocation"][id[0]]["HasShard"]:
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

def empty_drop_entry(container):
    if not "Shard" in container:
        container = chest_to_seed[container]
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
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = item
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = 1
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = 100.0
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
                Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = Manager.mod_data["ShardDrop"]["ItemRate"]*3*drop_rate_multiplier
        elif i.split("_")[0] == enemy:
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardId"] = "None"
            Manager.datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = 0.0

def patch_start_chest_entry():
    #Randomize the very first chest so that it is always a weapon
    container = "Treasurebox_SIP000_Tutorial"
    empty_drop_entry(container)
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.mod_data["ItemDrop"]["Weapon"]["ItemPool"], Manager.mod_data["ItemDrop"]["Weapon"]["IsUnique"], "Weapon")
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.mod_data["ItemDrop"]["Weapon"]["ItemQuantity"]
    Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.mod_data["ItemDrop"]["Weapon"]["ItemRate"]
    #Give extra bullets if the starting weapon is a gun
    if Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] in gun_list:
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = any_pick(Manager.mod_data["ItemDrop"]["Bullet"]["ItemPool"], Manager.mod_data["ItemDrop"]["Bullet"]["IsUnique"], "Bullet")
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = Manager.mod_data["ItemDrop"]["Bullet"]["ItemQuantity"]*3
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = Manager.mod_data["ItemDrop"]["Bullet"]["ItemRate"]
    del chest_to_seed[container]

def patch_chest_entry(item_type, container):
    #Randomize chest items based on item types
    if not container in chest_to_seed:
        return
    empty_drop_entry(container)
    if Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Blue":
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemId"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonItemQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientId"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareIngredientRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientId"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], False, item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CommonIngredientRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = random.choice(coin)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::D" + str(Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"])
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = 0.0
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["AreaChangeTreasureFlag"] = True
    elif Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Red":
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinOverride"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinType"] = "EDropCoin::D2000"
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["CoinRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    else:
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemId"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemQuantity"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]
        Manager.datatable["PB_DT_DropRateMaster"][chest_to_seed[container]]["RareItemRate"] = Manager.mod_data["ItemDrop"][item_type]["ItemRate"]
    del chest_to_seed[container]
    
def patch_enemy_entry(item_type, item_rate, container):
    #Randomize enemy drops in a varied fashion while slightly favouring one item type
    #Also randomize the amount of drops so that it isn't always 4 per enemy
    empty_drop_entry(container)
    if item_type == "CookingMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
    elif item_type == "StandardMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
    elif item_type == "EnemyMat":
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemId"] = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareItemRate"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemId"] = any_pick(Manager.mod_data["ItemDrop"]["CookingMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["CookingMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonItemQuantity"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonRate"] = Manager.mod_data["EnemyDrop"]["CookingMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientId"] = any_pick(Manager.mod_data["ItemDrop"]["StandardMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["StandardMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["RareIngredientRate"] = Manager.mod_data["EnemyDrop"]["StandardMat"]["ItemRate"]*item_rate
        if random.randint(1, 3) > 1 and Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"]:
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientId"] = any_pick(Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemPool"], Manager.mod_data["EnemyDrop"]["EnemyMat"]["IsUnique"], item_type)
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientQuantity"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemQuantity"]
            Manager.datatable["PB_DT_DropRateMaster"][container]["CommonIngredientRate"] = Manager.mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*item_rate

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
    all_enemies = list(Manager.mod_data["EnemyLocation"])
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
            if Manager.mod_data["ItemDrop"][item_type]["IsUnique"]:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = 1
            else:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]*9
        elif Manager.mod_data["ItemDrop"][item_type]["ChestColor"] == "Red":
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = "Money"
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
        else:
            Manager.datatable["PB_DT_QuestMaster"][i]["RewardItem01"] = any_pick(Manager.mod_data["ItemDrop"][item_type]["ItemPool"], Manager.mod_data["ItemDrop"][item_type]["IsUnique"], item_type)
            if Manager.mod_data["ItemDrop"][item_type]["IsUnique"]:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = 1
            else:
                Manager.datatable["PB_DT_QuestMaster"][i]["RewardNum01"] = Manager.mod_data["ItemDrop"][item_type]["ItemQuantity"]*3
    invert_ratio()

def catering_quest_info():
    #Update catering quests descriptions so that it is possible to tell what Susie wants
    for i in range(21):
        Manager.stringtable["PBScenarioStringTable"]["QST_Catering_Name" + "{:02d}".format(i + 1)]    = Manager.mod_data["ItemTranslation"][Manager.datatable["PB_DT_QuestMaster"]["Quest_Catering" + "{:02d}".format(i + 1)]["Item01"]]
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
    for i in Manager.mod_data["ItemDrop"]:
        for e in shop_skip_list:
            if e in Manager.mod_data["ItemDrop"][i]["ItemPool"]:
                Manager.mod_data["ItemDrop"][i]["ShopRatio"] -= 1
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
        if Manager.datatable["PB_DT_ItemMaster"][i]["buyPrice"] == 0 or i in shop_skip_list:
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

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for i in Manager.file_to_path:
        if Manager.file_to_type[i] == "Material":
            enemy_id = Manager.file_to_path[i].split("\\")[-2]
            if Manager.is_enemy(enemy_id)["Enemy"]:
                shard_name = Manager.datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
                shard_type = Manager.datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
                shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
                Manager.change_material_hsv(i, "ShardColor", shard_hsv)

def update_shard_candles():
    #While candle shards have entries in DropRateMaster they are completely ignored by the game
    #Instead those are read directly from the level files so they need to be updated to reflect the new shard drops
    for i in ["Shortcut", "Deepsinker", "FamiliaSilverKnight"]:
        for e in Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"]:
            Manager.search_and_replace_string(e + "_Gimmick", "ShardChild", "ShardID", i, Manager.datatable["PB_DT_DropRateMaster"][i + "_Shard"]["ShardId"])

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
            log["Key"][Manager.mod_data["ItemTranslation"][i]] = [chest_to_room(key_item_to_location[i])]
        if i in key_shards:
            log["Key"][Manager.mod_data["ShardTranslation"][i]] = enemy_to_room(key_shard_to_location[i])
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
            log_string += "  " + Manager.mod_data["ItemTranslation"][i] + ": " + key_item_to_location[i] + "\n"
        if i in key_shards:
            log_string += "  " + Manager.mod_data["ShardTranslation"][i] + ": " + Manager.mod_data["EnemyTranslation"][key_shard_to_location[i]] + "\n"
    return log_string