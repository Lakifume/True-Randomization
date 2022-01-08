import ClassManagement
import math
import random

#Logic

chest_to_seed = {
    "PotionMaterial":               "Treasurebox_SIP000_Tutorial",
    "Qu07_Last":                    "Qu07_Last",
    "Swordsman":                    "Swordsman",
    "Treasurebox_SIP000_Tutorial":  "Treasurebox_SIP011(5)",
    "Treasurebox_SIP002(2)":        "Treasurebox_SIP005(3)",
    "Treasurebox_SIP003(2)":        "Treasurebox_LIB009(2)",
    "Treasurebox_SIP004(2)":        "Treasurebox_GDN006(6)",
    "Treasurebox_SIP005(2)":        "Treasurebox_ENT002(2)",
    "Treasurebox_SIP005(3)":        "Treasurebox_SIP002(2)",
    "Treasurebox_SIP006(2)":        "Treasurebox_LIB022(2)",
    "Treasurebox_SIP007(2)":        "Treasurebox_KNG017(2)",
    "Treasurebox_SIP007(3)":        "Treasurebox_SIP011(4)",
    "Treasurebox_SIP009(2)":        "Treasurebox_JPN011(2)",
    "Treasurebox_SIP011(2)":        "Treasurebox_SIP014(2)",
    "Treasurebox_SIP011(3)":        "Treasurebox_TWR015(2)",
    "Treasurebox_SIP011(4)":        "Treasurebox_TWR000(4)",
    "Treasurebox_SIP011(5)":        "PotionMaterial",
    "Treasurebox_SIP012(2)":        "Treasurebox_TAR007(2)",
    "Treasurebox_SIP013(2)":        "Treasurebox_RVA001(3)",
    "Treasurebox_SIP014(2)":        "Treasurebox_UGD051(2)",
    "Treasurebox_SIP015(2)":        "Treasurebox_ARC000(2)",
    "Treasurebox_SIP016(2)":        "Treasurebox_SAN024(2)",
    "Treasurebox_SIP017(2)":        "Treasurebox_RVA011(3)",
    "Treasurebox_SIP018(2)":        "Treasurebox_SIP016(2)",
    "Treasurebox_SIP019(2)":        "Treasurebox_UGD025(2)",
    "Treasurebox_SIP020(2)":        "Treasurebox_RVA015(2)",
    "Treasurebox_SIP021(3)":        "Treasurebox_BIG011(2)",
    "Treasurebox_SIP024(2)":        "Treasurebox_ENT014(3)",
    "Treasurebox_SIP024(3)":        "Treasurebox_TWR009(2)",
    "Treasurebox_SIP025(2)":        "Treasurebox_UGD009(5)",
    "Treasurebox_SIP025(3)":        "Treasurebox_SAN015(3)",
    "Treasurebox_SIP026(2)":        "Treasurebox_SAN005(2)",
    "Treasurebox_VIL001(2)":        "Treasurebox_UGD044(3)",
    "Treasurebox_VIL003(2)":        "Treasurebox_LIB009(3)",
    "Treasurebox_VIL005(2)":        "Treasurebox_JPN018(2)",
    "Treasurebox_VIL006(2)":        "Treasurebox_TWR017(6)",
    "Treasurebox_VIL006(3)":        "Treasurebox_VIL006(3)",
    "Treasurebox_VIL006(4)":        "Treasurebox_UGD044(2)",
    "Treasurebox_VIL006(5)":        "Treasurebox_ENT020(3)",
    "Treasurebox_VIL007(2)":        "Treasurebox_SAN003(2)",
    "Treasurebox_VIL008(2)":        "Treasurebox_TRN002(4)",
    "Treasurebox_VIL008(3)":        "Treasurebox_SAN003(6)",
    "Treasurebox_VIL010(2)":        "Treasurebox_ENT015(2)",
    "Treasurebox_ENT002(2)":        "Treasurebox_TWR019(3)",
    "Treasurebox_ENT002(3)":        "Treasurebox_ENT018(2)",
    "Treasurebox_ENT002(4)":        "Treasurebox_GDN012(2)",
    "Treasurebox_ENT004(2)":        "Treasurebox_VIL001(2)",
    "Treasurebox_ENT005(2)":        "Treasurebox_ENT005(2)",
    "Treasurebox_ENT005(3)":        "Treasurebox_TWR018(9)",
    "Treasurebox_ENT007(2)":        "Treasurebox_VIL008(3)",
    "Treasurebox_ENT007(3)":        "Treasurebox_UGD052(2)",
    "Treasurebox_ENT007(4)":        "Treasurebox_SIP007(2)",
    "Treasurebox_ENT009(2)":        "Treasurebox_GDN004(2)",
    "Treasurebox_ENT011(2)":        "Treasurebox_SAN009(3)",
    "Treasurebox_ENT014(2)":        "Treasurebox_SAN003(4)",
    "Treasurebox_ENT014(3)":        "Treasurebox_SAN016(6)",
    "Treasurebox_ENT014(4)":        "Treasurebox_SND016(2)",
    "Treasurebox_ENT018(2)":        "Treasurebox_SND011(2)",
    "Treasurebox_ENT018(3)":        "Treasurebox_BIG002(2)",
    "Treasurebox_ENT020(2)":        "Treasurebox_GDN006(2)",
    "Treasurebox_ENT020(3)":        "Treasurebox_ARC004(2)",
    "Treasurebox_ENT021(2)":        "Treasurebox_ARC006(3)",
    "Treasurebox_ENT022(2)":        "Treasurebox_ENT020(2)",
    "Treasurebox_ENT024(2)":        "Treasurebox_LIB032(2)",
    "Treasurebox_ENT024(3)":        "Treasurebox_ARC007(3)",
    "Treasurebox_ENT024(4)":        "Treasurebox_BIG012(2)",
    "Treasurebox_GDN002(2)":        "Treasurebox_TWR019(5)",
    "Treasurebox_GDN004(2)":        "Treasurebox_TRN002(5)",
    "Treasurebox_GDN006(2)":        "Treasurebox_LIB040(2)",
    "Treasurebox_GDN006(3)":        "Treasurebox_PureMiriam_Hair",
    "Treasurebox_GDN006(4)":        "Treasurebox_SAN019(4)",
    "Treasurebox_GDN006(5)":        "Treasurebox_VIL008(2)",
    "Treasurebox_GDN006(6)":        "Treasurebox_ICE003(2)",
    "Treasurebox_GDN007(2)":        "Treasurebox_GDN007(2)",
    "Treasurebox_GDN009(2)":        "Treasurebox_SAN017(2)",
    "Treasurebox_GDN009(3)":        "Treasurebox_SIP025(3)",
    "Treasurebox_GDN010(2)":        "Treasurebox_ICE006(2)",
    "Treasurebox_GDN012(2)":        "Treasurebox_ENT004(2)",
    "Treasurebox_GDN012(3)":        "Treasurebox_GDN009(3)",
    "Treasurebox_GDN013(2)":        "Treasurebox_TWR004(2)",
    "Treasurebox_GDN013(3)":        "Treasurebox_KNG002(2)",
    "Treasurebox_GDN013(4)":        "Treasurebox_SAN021(5)",
    "Treasurebox_GDN013(5)":        "Treasurebox_UGD038(2)",
    "Treasurebox_GDN014(2)":        "Treasurebox_UGD049(2)",
    "Treasurebox_SAN003(2)":        "Treasurebox_SIP011(2)",
    "Treasurebox_SAN003(3)":        "Treasurebox_ARC003(2)",
    "Treasurebox_SAN003(4)":        "Treasurebox_ENT008(2)",
    "Treasurebox_SAN003(5)":        "Treasurebox_BIG006(6)",
    "Treasurebox_SAN003(6)":        "Treasurebox_TWR019(4)",
    "Treasurebox_SAN003(7)":        "Treasurebox_KNG018(4)",
    "Treasurebox_SAN003(8)":        "Treasurebox_UGD033(2)",
    "Treasurebox_SAN003(9)":        "Treasurebox_TWR018(8)",
    "Treasurebox_SAN005(2)":        "Treasurebox_SND003(2)",
    "Treasurebox_SAN005(3)":        "Treasurebox_SAN003(9)",
    "Treasurebox_SAN009(2)":        "Treasurebox_TWR018(3)",
    "Treasurebox_SAN009(3)":        "Treasurebox_UGD053(2)",
    "Treasurebox_SAN013(2)":        "Treasurebox_ARC006(2)",
    "Treasurebox_SAN013(3)":        "Treasurebox_ENT007(2)",
    "Treasurebox_SAN014(2)":        "Treasurebox_SIP004(2)",
    "Treasurebox_SAN015(3)":        "Treasurebox_SND008(3)",
    "Treasurebox_SAN015(4)":        "Treasurebox_TRN002(2)",
    "Treasurebox_SAN016(2)":        "Treasurebox_SND000(2)",
    "Treasurebox_SAN016(3)":        "Treasurebox_UGD035(2)",
    "Treasurebox_SAN016(4)":        "Treasurebox_RVA001(2)",
    "Treasurebox_SAN016(5)":        "Treasurebox_SAN016(5)",
    "Treasurebox_SAN016(6)":        "Treasurebox_SAN003(7)",
    "Treasurebox_SAN017(2)":        "Treasurebox_ENT024(2)",
    "Treasurebox_SAN019(2)":        "Treasurebox_JPN004(2)",
    "Treasurebox_SAN019(3)":        "Treasurebox_SIP025(2)",
    "Treasurebox_SAN019(4)":        "Treasurebox_SAN013(3)",
    "Treasurebox_SAN020(2)":        "Treasurebox_SAN003(8)",
    "Treasurebox_SAN021(2)":        "Treasurebox_ICE013(2)",
    "Treasurebox_SAN021(3)":        "Treasurebox_SAN021(3)",
    "Treasurebox_SAN021(4)":        "Treasurebox_GDN002(2)",
    "Treasurebox_SAN021(5)":        "Treasurebox_GDN006(4)",
    "Treasurebox_SAN021(6)":        "Treasurebox_KNG017(4)",
    "Treasurebox_SAN024(2)":        "Treasurebox_SIP024(3)",
    "Treasurebox_TWR000(2)":        "Treasurebox_RVA003(3)",
    "Treasurebox_TWR003(2)":        "Treasurebox_ENT012(2)",
    "Treasurebox_TWR004(2)":        "Treasurebox_GDN013(2)",
    "Treasurebox_TWR005(2)":        "Treasurebox_LIB011(2)",
    "Treasurebox_TWR006(2)":        "Treasurebox_UGD023(2)",
    "Treasurebox_TWR008(2)":        "Treasurebox_BIG014(2)",
    "Treasurebox_TWR009(2)":        "Treasurebox_SIP018(2)",
    "Treasurebox_TWR010(2)":        "Treasurebox_KNG005(2)",
    "Treasurebox_TWR012(2)":        "Treasurebox_UGD018(2)",
    "Treasurebox_TWR013(2)":        "Treasurebox_ENT014(2)",
    "Treasurebox_TWR016(2)":        "Treasurebox_SAN005(5)",
    "Treasurebox_TWR017(2)":        "Treasurebox_KNG012(2)",
    "Treasurebox_TWR017(3)":        "Treasurebox_BIG005(2)",
    "Treasurebox_TWR017(4)":        "Treasurebox_ENT007(3)",
    "Treasurebox_TWR017(5)":        "Treasurebox_RVA006(2)",
    "Treasurebox_TWR017(6)":        "Treasurebox_LIB043(2)",
    "Treasurebox_TWR017(7)":        "Treasurebox_SAN021(4)",
    "Treasurebox_TWR017(8)":        "Treasurebox_TRN002(3)",
    "Treasurebox_TWR018(2)":        "Treasurebox_GDN010(2)",
    "Treasurebox_TWR018(3)":        "Treasurebox_UGD009(3)",
    "Treasurebox_TWR018(4)":        "Treasurebox_SND018(2)",
    "Treasurebox_TWR018(5)":        "Treasurebox_SAN003(3)",
    "Treasurebox_TWR018(6)":        "Treasurebox_PureMiriam_Sword",
    "Treasurebox_TWR018(7)":        "Treasurebox_GDN009(2)",
    "Treasurebox_TWR018(8)":        "Treasurebox_KNG018(3)",
    "Treasurebox_TWR018(9)":        "Treasurebox_GDN013(4)",
    "Treasurebox_TWR019(2)":        "Treasurebox_SAN021(2)",
    "Treasurebox_TWR019(3)":        "Treasurebox_SAN014(2)",
    "Treasurebox_TWR019(5)":        "Treasurebox_GDN012(3)",
    "Treasurebox_LIB001(2)":        "Treasurebox_UGD047(2)",
    "Treasurebox_LIB002(2)":        "Treasurebox_TWR017(5)",
    "Treasurebox_LIB007(2)":        "Treasurebox_GDN014(2)",
    "Treasurebox_LIB009(2)":        "Treasurebox_VIL006(2)",
    "Treasurebox_LIB009(3)":        "Treasurebox_VIL003(2)",
    "Treasurebox_LIB011(2)":        "Treasurebox_SIP006(2)",
    "Treasurebox_LIB012(2)":        "Treasurebox_ICE003(3)",
    "Treasurebox_LIB017(2)":        "Treasurebox_JPN000(2)",
    "Treasurebox_LIB019(2)":        "Treasurebox_LIB002(2)",
    "Treasurebox_LIB022(2)":        "Treasurebox_SIP026(2)",
    "Treasurebox_LIB030(2)":        "Treasurebox_ARC005(2)",
    "Treasurebox_LIB032(2)":        "Treasurebox_LIB019(2)",
    "Treasurebox_LIB033(2)":        "Treasurebox_SAN009(4)",
    "Treasurebox_LIB040(2)":        "Treasurebox_ENT022(2)",
    "Treasurebox_LIB043(2)":        "Treasurebox_UGD010(2)",
    "Treasurebox_TRN002(2)":        "Treasurebox_TWR017(8)",
    "Treasurebox_TRN002(3)":        "Treasurebox_ENT024(3)",
    "Treasurebox_TRN002(4)":        "Treasurebox_UGD003(4)",
    "Treasurebox_TRN002(5)":        "Treasurebox_ENT007(4)",
    "Treasurebox_TRN002(6)":        "Treasurebox_JPN010(3)",
    "Treasurebox_KNG002(2)":        "Treasurebox_UGD040(2)",
    "Treasurebox_KNG002(3)":        "Treasurebox_TWR008(2)",
    "Treasurebox_KNG003(2)":        "Treasurebox_ENT002(3)",
    "Treasurebox_KNG006(2)":        "Treasurebox_JPN001(2)",
    "Treasurebox_KNG010(2)":        "Treasurebox_UGD012(2)",
    "Treasurebox_KNG011(2)":        "Treasurebox_KNG018(5)",
    "Treasurebox_KNG012(2)":        "Treasurebox_ENT009(2)",
    "Treasurebox_KNG012(3)":        "Treasurebox_UGD009(2)",
    "Treasurebox_KNG016(2)":        "Treasurebox_UGD048(2)",
    "Treasurebox_KNG017(2)":        "Treasurebox_ICE008(2)",
    "Treasurebox_KNG017(3)":        "Treasurebox_TWR019(2)",
    "Treasurebox_KNG017(4)":        "Treasurebox_ENT002(4)",
    "Treasurebox_KNG017(5)":        "Treasurebox_UGD003(3)",
    "Treasurebox_KNG017(6)":        "Treasurebox_KNG017(6)",
    "Treasurebox_KNG018(3)":        "Treasurebox_KNG018(2)",
    "Treasurebox_KNG018(4)":        "Treasurebox_LIB012(2)",
    "Treasurebox_KNG018(5)":        "Treasurebox_KNG002(3)",
    "Treasurebox_KNG021(2)":        "Treasurebox_RVA005(3)",
    "Treasurebox_KNG022(2)":        "Treasurebox_UGD050(2)",
    "Treasurebox_UGD001(2)":        "Treasurebox_KNG016(2)",
    "Treasurebox_UGD003(2)":        "Treasurebox_SND005(2)",
    "Treasurebox_UGD003(3)":        "Treasurebox_VIL006(4)",
    "Treasurebox_UGD003(4)":        "Treasurebox_KNG017(5)",
    "Treasurebox_UGD003(5)":        "Treasurebox_SND001(2)",
    "Treasurebox_UGD005(2)":        "Treasurebox_ICE014(2)",
    "Treasurebox_UGD005(3)":        "Treasurebox_SND021(2)",
    "Treasurebox_UGD007(2)":        "Treasurebox_GDN006(3)",
    "Treasurebox_UGD009(2)":        "Treasurebox_LIB018(2)",
    "Treasurebox_UGD009(3)":        "Treasurebox_ENT011(2)",
    "Treasurebox_UGD009(4)":        "Treasurebox_UGD048(3)",
    "Treasurebox_UGD009(5)":        "Treasurebox_SIP019(2)",
    "Treasurebox_UGD010(2)":        "Treasurebox_SAN013(2)",
    "Treasurebox_UGD011(2)":        "Treasurebox_UGD011(2)",
    "Treasurebox_UGD021(2)":        "Treasurebox_BIG006(2)",
    "Treasurebox_UGD024(2)":        "Treasurebox_UGD005(2)",
    "Treasurebox_UGD024(3)":        "Treasurebox_UGD020(2)",
    "Treasurebox_UGD024(4)":        "Treasurebox_UGD024(4)",
    "Treasurebox_UGD025(2)":        "Treasurebox_BIG006(4)",
    "Treasurebox_UGD025(3)":        "Treasurebox_RVA004(2)",
    "Treasurebox_UGD025(4)":        "Treasurebox_UGD036(2)",
    "Treasurebox_UGD027(2)":        "Treasurebox_UGD032(2)",
    "Treasurebox_UGD030(2)":        "Treasurebox_SND019(2)",
    "Treasurebox_UGD031(2)":        "Treasurebox_KNG022(2)",
    "Treasurebox_UGD031(3)":        "Treasurebox_TWR017(4)",
    "Treasurebox_UGD036(2)":        "Treasurebox_ICE011(2)",
    "Treasurebox_UGD036(3)":        "Treasurebox_TWR018(2)",
    "Treasurebox_UGD038(2)":        "Treasurebox_UGD045(2)",
    "Treasurebox_UGD040(2)":        "Treasurebox_BIG010(2)",
    "Treasurebox_UGD041(2)":        "Treasurebox_TAR009(2)",
    "Treasurebox_UGD042(2)":        "Treasurebox_SND026(2)",
    "Treasurebox_UGD044(2)":        "Treasurebox_UGD047(3)",
    "Treasurebox_UGD044(3)":        "Treasurebox_TRN002(6)",
    "Treasurebox_UGD046(2)":        "Treasurebox_UGD046(2)",
    "Treasurebox_UGD046(3)":        "Treasurebox_ICE008(3)",
    "Treasurebox_UGD047(3)":        "Treasurebox_KNG021(4)",
    "Treasurebox_UGD048(2)":        "Treasurebox_SND008(2)",
    "Treasurebox_UGD050(2)":        "Treasurebox_UGD025(3)",
    "Treasurebox_UGD051(2)":        "Treasurebox_TWR017(2)",
    "Treasurebox_UGD052(2)":        "Treasurebox_ENT011(3)",
    "Treasurebox_UGD052(3)":        "Treasurebox_SND010(2)",
    "Treasurebox_UGD053(2)":        "Treasurebox_JPN005(2)",
    "Treasurebox_UGD054(2)":        "Treasurebox_JPN008(2)",
    "Treasurebox_UGD056(2)":        "Treasurebox_JPN002(2)",
    "Treasurebox_SND002(2)":        "Treasurebox_SAN005(4)",
    "Treasurebox_SND003(2)":        "Treasurebox_TWR005(2)",
    "Treasurebox_SND004(2)":        "Treasurebox_KNG021(2)",
    "Treasurebox_SND006(2)":        "Treasurebox_UGD031(2)",
    "Treasurebox_SND008(2)":        "Treasurebox_SAN019(2)",
    "Treasurebox_SND008(3)":        "Treasurebox_KNG021(3)",
    "Treasurebox_SND009(2)":        "Treasurebox_SIP009(2)",
    "Treasurebox_SND010(2)":        "Treasurebox_SND014(2)",
    "Treasurebox_SND010(3)":        "Treasurebox_TWR017(7)",
    "Treasurebox_SND013(2)":        "Treasurebox_JPN003(2)",
    "Treasurebox_SND015(2)":        "Treasurebox_RVA014(2)",
    "Treasurebox_SND016(2)":        "Treasurebox_ENT021(2)",
    "Treasurebox_SND017(2)":        "Treasurebox_TAR003(2)",
    "Treasurebox_SND018(2)":        "Treasurebox_BIG016(2)",
    "Treasurebox_SND019(2)":        "Treasurebox_ICE010(2)",
    "Treasurebox_SND020(2)":        "Treasurebox_RVA009(2)",
    "Treasurebox_SND024(2)":        "Treasurebox_UGD057(2)",
    "Treasurebox_SND025(2)":        "Treasurebox_RVA003(2)",
    "Treasurebox_ARC000(2)":        "Treasurebox_UGD026(2)",
    "Treasurebox_ARC002(2)":        "Treasurebox_UGD019(2)",
    "Treasurebox_ARC003(2)":        "Treasurebox_UGD007(2)",
    "Treasurebox_ARC004(2)":        "Treasurebox_BIG012(4)",
    "Treasurebox_ARC006(2)":        "Treasurebox_SND006(2)",
    "Treasurebox_ARC006(3)":        "Treasurebox_SIP024(2)",
    "Treasurebox_ARC007(2)":        "Treasurebox_SIP003(2)",
    "Treasurebox_ARC007(3)":        "Treasurebox_ENT014(4)",
    "Treasurebox_TAR001(2)":        "Treasurebox_TAR005(2)",
    "Treasurebox_TAR002(2)":        "N3106_2ND_Treasure",
    "Treasurebox_TAR006(2)":        "Treasurebox_PureMiriam_Dress",
    "Treasurebox_TAR007(2)":        "Treasurebox_ICE001(3)",
    "Treasurebox_TAR010(2)":        "Treasurebox_UGD015(2)",
    "Treasurebox_JPN002(2)":        "Treasurebox_UGD056(2)",
    "Treasurebox_JPN002(3)":        "Treasurebox_JPN002(3)",
    "Treasurebox_JPN004(2)":        "Treasurebox_TWR018(5)",
    "Treasurebox_JPN005(2)":        "Treasurebox_TWR018(7)",
    "Treasurebox_JPN009(2)":        "Treasurebox_UGD001(2)",
    "Treasurebox_JPN010(2)":        "Treasurebox_SIP015(2)",
    "Treasurebox_JPN010(3)":        "Treasurebox_SAN021(6)",
    "Treasurebox_JPN013(2)":        "N3106_1ST_Treasure",
    "Treasurebox_JPN015(2)":        "Treasurebox_SAN016(2)",
    "Treasurebox_JPN017(2)":        "Treasurebox_VIL005(2)",
    "Treasurebox_JPN018(2)":        "Treasurebox_ARC007(2)",
    "Treasurebox_RVA001(2)":        "Treasurebox_ENT018(3)",
    "Treasurebox_RVA001(3)":        "Treasurebox_SIP013(2)",
    "Treasurebox_RVA002(2)":        "Treasurebox_UGD052(3)",
    "Treasurebox_RVA004(2)":        "Treasurebox_JPN017(2)",
    "Treasurebox_RVA006(2)":        "Treasurebox_JPN009(2)",
    "Treasurebox_RVA010(2)":        "Treasurebox_UGD037(2)",
    "Treasurebox_RVA011(2)":        "Treasurebox_RVA011(2)",
    "Treasurebox_RVA011(3)":        "Treasurebox_VIL010(2)",
    "Treasurebox_RVA012(2)":        "Treasurebox_SND027(2)",
    "Treasurebox_RVA015(2)":        "Treasurebox_TWR003(2)",
    "Treasurebox_BIG002(2)":        "Treasurebox_UGD022(2)",
    "Treasurebox_BIG005(2)":        "Treasurebox_LIB042(2)",
    "Treasurebox_BIG006(2)":        "Treasurebox_SND009(2)",
    "Treasurebox_BIG006(3)":        "Treasurebox_KNG017(3)",
    "Treasurebox_BIG006(4)":        "Treasurebox_SAN019(3)",
    "Treasurebox_BIG006(5)":        "Treasurebox_BIG008(2)",
    "Treasurebox_BIG006(6)":        "Treasurebox_SAN005(3)",
    "Treasurebox_BIG006(7)":        "Treasurebox_ENT005(3)",
    "Treasurebox_BIG007(2)":        "Treasurebox_SND012(2)",
    "Treasurebox_BIG008(2)":        "Treasurebox_BIG006(5)",
    "Treasurebox_BIG010(2)":        "Treasurebox_UGD029(2)",
    "Treasurebox_BIG011(2)":        "Treasurebox_SIP021(3)",
    "Treasurebox_BIG012(2)":        "Treasurebox_SIP017(2)",
    "Treasurebox_BIG012(3)":        "Treasurebox_UGD039(2)",
    "Treasurebox_BIG012(4)":        "Treasurebox_SND010(3)",
    "Treasurebox_BIG013(2)":        "Treasurebox_KNG003(2)",
    "Treasurebox_BIG014(2)":        "Treasurebox_KNG011(2)",
    "Treasurebox_BIG016(2)":        "Treasurebox_JPN010(2)",
    "Treasurebox_BIG016(3)":        "Treasurebox_TWR012(2)",
    "Treasurebox_BIG016(4)":        "Treasurebox_GDN013(5)",
    "Treasurebox_ICE001(2)":        "Treasurebox_TWR006(3)",
    "Treasurebox_ICE001(3)":        "Treasurebox_UGD036(3)",
    "Treasurebox_ICE002(2)":        "Treasurebox_SND007(2)",
    "Treasurebox_ICE003(2)":        "Treasurebox_SIP005(2)",
    "Treasurebox_ICE003(3)":        "Treasurebox_VIL006(5)",
    "Treasurebox_ICE006(2)":        "Treasurebox_UGD016(2)",
    "Treasurebox_ICE008(2)":        "Treasurebox_VIL007(2)",
    "Treasurebox_ICE008(3)":        "Treasurebox_RVA005(2)",
    "Treasurebox_ICE010(2)":        "Treasurebox_ENT024(4)",
    "Treasurebox_ICE011(2)":        "Treasurebox_GDN013(3)",
    "Treasurebox_ICE013(2)":        "Treasurebox_BIG006(3)",
    "Treasurebox_ICE014(2)":        "Treasurebox_SND020(2)",
    "Treasurebox_PureMiriam_Hair":  "Treasurebox_SAN009(2)",
    "Treasurebox_PureMiriam_Tiare": "Treasurebox_PureMiriam_Tiare",
    "Treasurebox_PureMiriam_Dress": "Treasurebox_TAR006(2)",
    "Treasurebox_PureMiriam_Sword": "Treasurebox_SAN000(2)",
    "Wall_SIP004(2)":               "Wall_BIG012(2)",
    "Wall_SIP009(2)":               "Wall_LIB004(2)",
    "Wall_SIP014(2)":               "Wall_UGD031(2)",
    "Wall_SIP016(2)":               "Wall_ICE003(2)",
    "Wall_ENT002(2)":               "Wall_TRN005(2)",
    "Wall_ENT012(2)":               "Wall_TWR013(2)",
    "Wall_GDN006(2)":               "Wall_GDN006(2)",
    "Wall_SAN000(2)":               "Wall_UGD006(2)",
    "Wall_SAN005(2)":               "Wall_RVA011(2)",
    "Wall_SAN019(2)":               "Wall_LIB025(2)",
    "Wall_KNG000(2)":               "Wall_SND001(2)",
    "Wall_KNG007(2)":               "Wall_RVA003(2)",
    "Wall_LIB004(2)":               "Wall_ICE010(2)",
    "Wall_LIB019(2)":               "Wall_UGD012(2)",
    "Wall_LIB025(2)":               "Wall_TWR006(2)",
    "Wall_TWR006(2)":               "Wall_UGD020(2)",
    "Wall_TWR013(2)":               "Wall_ENT012(2)",
    "Wall_TWR016(2)":               "Wall_TWR016(2)",
    "Wall_TRN005(2)":               "Wall_SIP009(2)",
    "Wall_UGD000(2)":               "Wall_ENT002(2)",
    "Wall_UGD003(2)":               "Wall_UGD003(2)",
    "Wall_UGD006(2)":               "Wall_SND019(2)",
    "Wall_UGD012(2)":               "Wall_SAN005(2)",
    "Wall_UGD020(2)":               "Wall_BIG016(2)",
    "Wall_UGD031(2)":               "Wall_SIP014(2)",
    "Wall_UGD037(2)":               "Wall_ICE017(2)",
    "Wall_UGD046(2)":               "Wall_TAR007(2)",
    "Wall_UGD056(2)":               "Wall_UGD056(2)",
    "Wall_SND001(2)":               "Wall_SAN019(2)",
    "Wall_SND019(2)":               "Wall_KNG007(2)",
    "Wall_TAR007(2)":               "Wall_UGD046(2)",
    "Wall_JPN011(2)":               "Wall_KNG000(2)",
    "Wall_JPN013(2)":               "Wall_JPN013(2)",
    "Wall_RVA011(2)":               "Wall_SIP016(2)",
    "Wall_BIG002(2)":               "Wall_BIG002(2)",
    "Wall_BIG012(2)":               "Wall_UGD000(2)",
    "Wall_BIG016(2)":               "Wall_JPN011(2)",
    "Wall_ICE003(2)":               "Wall_LIB019(2)",
    "Wall_ICE010(2)":               "Wall_SIP004(2)",
    "Wall_ICE017(2)":               "Wall_SAN000(2)",
    "N3106_1ST_Treasure":           "Treasurebox_ARC002(2)",
    "N3106_2ND_Treasure":           "Treasurebox_KNG006(2)"
}
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
    "m19K2C_000",
    "m51EBT_000",
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
    "Keyofbacker4",
    "MonarchCrown"
]
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
key_item_to_location = {}
key_shard_to_location = {}
previous_gate = []
previous_room = []
all_rooms = []
requirement = []
requirement_to_gate = {}
other_key = [
    "ShipMap",
    "DiscountCard"
]

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

enemy_skip_list = [
    "N1003",
    "N2001",
    "N2013"
]
shop_skip_list = [
    "Waystone"
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

log = {}

def init():
    #FillingLootTypes
    for i in ClassManagement.item_drop_data:
        for e in range(ClassManagement.item_drop_data[i]["ChestRatio"]):
            chest_type.append(i)
            if ClassManagement.item_drop_data[i]["ChestColor"] == "Green":
                green_chest_type.append(i)
            if ClassManagement.item_drop_data[i]["ChestColor"] == "Blue":
                blue_chest_type.append(i)
        for e in range(ClassManagement.item_drop_data[i]["QuestRatio"]):
            quest_type.append(i)
    for i in ClassManagement.enemy_drop_data:
        enemy_type.append(i)
    
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
        for e in range(10):
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
        if i["Value"]["WarpPositionX"] == -1.0:
            room_unused_list.append(i["Key"])
    for i in ClassManagement.drop_content:
        if chest_to_room(i["Key"]) in room_unused_list and i["Key"] in chest_to_seed:
            del chest_to_seed[i["Key"]]
    ClassManagement.debug("ClassItem.unused_room_check()")

def extra_logic():
    #8BitNightmare
    ClassManagement.logic_data["m51EBT_000"] = {}
    ClassManagement.logic_data["m51EBT_000"]["GateRoom"] = False
    ClassManagement.logic_data["m51EBT_000"]["NearestGate"] = ClassManagement.logic_data["m06KNG_021"]["NearestGate"]
    ClassManagement.logic_data["m51EBT_000"]["Doublejump"] = False
    ClassManagement.logic_data["m51EBT_000"]["HighJump"] = False
    ClassManagement.logic_data["m51EBT_000"]["Invert"] = False
    ClassManagement.logic_data["m51EBT_000"]["Deepsinker"] = False
    ClassManagement.logic_data["m51EBT_000"]["Dimensionshift"] = False
    ClassManagement.logic_data["m51EBT_000"]["Reflectionray"] = False
    ClassManagement.logic_data["m51EBT_000"]["Aquastream"] = False
    ClassManagement.logic_data["m51EBT_000"]["Bloodsteel"] = False
    ClassManagement.logic_data["m51EBT_000"]["Swordsman"] = False
    ClassManagement.logic_data["m51EBT_000"]["Silverbromide"] = False
    ClassManagement.logic_data["m51EBT_000"]["BreastplateofAguilar"] = False
    ClassManagement.logic_data["m51EBT_000"]["Keyofbacker1"] = False
    ClassManagement.logic_data["m51EBT_000"]["Keyofbacker2"] = False
    ClassManagement.logic_data["m51EBT_000"]["Keyofbacker3"] = False
    ClassManagement.logic_data["m51EBT_000"]["Keyofbacker4"] = False
    #K2C
    for i in ClassManagement.logic_data:
        ClassManagement.logic_data[i]["MonarchCrown"] = False
    ClassManagement.logic_data["m19K2C_000"] = {}
    ClassManagement.logic_data["m19K2C_000"]["GateRoom"] = True
    if ClassManagement.logic_data["m09TRN_002"]["GateRoom"]:
        ClassManagement.logic_data["m19K2C_000"]["NearestGate"] = ["m09TRN_002"]
    else:
        ClassManagement.logic_data["m19K2C_000"]["NearestGate"] = ClassManagement.logic_data["m09TRN_002"]["NearestGate"]
    ClassManagement.logic_data["m19K2C_000"]["Doublejump"] = False
    ClassManagement.logic_data["m19K2C_000"]["HighJump"] = False
    ClassManagement.logic_data["m19K2C_000"]["Invert"] = False
    ClassManagement.logic_data["m19K2C_000"]["Deepsinker"] = False
    ClassManagement.logic_data["m19K2C_000"]["Dimensionshift"] = False
    ClassManagement.logic_data["m19K2C_000"]["Reflectionray"] = False
    ClassManagement.logic_data["m19K2C_000"]["Aquastream"] = False
    ClassManagement.logic_data["m19K2C_000"]["Bloodsteel"] = False
    ClassManagement.logic_data["m19K2C_000"]["Swordsman"] = False
    ClassManagement.logic_data["m19K2C_000"]["Silverbromide"] = False
    ClassManagement.logic_data["m19K2C_000"]["BreastplateofAguilar"] = False
    ClassManagement.logic_data["m19K2C_000"]["Keyofbacker1"] = False
    ClassManagement.logic_data["m19K2C_000"]["Keyofbacker2"] = False
    ClassManagement.logic_data["m19K2C_000"]["Keyofbacker3"] = False
    ClassManagement.logic_data["m19K2C_000"]["Keyofbacker4"] = False
    ClassManagement.logic_data["m19K2C_000"]["MonarchCrown"] = True
    #Benjamin
    ClassManagement.logic_data["m02VIL_003"]["NearestGate"] = ClassManagement.logic_data["m18ICE_019"]["NearestGate"]
    #100%Chest
    ClassManagement.logic_data["m02VIL_005"]["NearestGate"] = ClassManagement.logic_data["m18ICE_019"]["NearestGate"]
    #OD
    if ClassManagement.book_content[21]["Value"]["RoomTraverseThreshold"] > 80:
        ClassManagement.logic_data["m18ICE_004"]["NearestGate"] = ClassManagement.logic_data["m18ICE_019"]["NearestGate"]
    ClassManagement.debug("ClassItem.extra_logic()")

def hard_enemy_logic():
    for i in ClassManagement.enemy_location_data:
        for e in ClassManagement.enemy_location_data[i]["HardModeRooms"]:
            ClassManagement.enemy_location_data[i]["NormalModeRooms"].append(e)
    #DullaHeadFix
    ClassManagement.enemy_location_data["N3090"]["NormalModeRooms"].remove("m07LIB_029")
    ClassManagement.enemy_location_data["N3090"]["NormalModeRooms"].remove("m08TWR_005")
    ClassManagement.enemy_location_data["N3090"]["NormalModeRooms"].remove("m08TWR_013")
    ClassManagement.enemy_location_data["N3090"]["NormalModeRooms"].remove("m11UGD_013")
    ClassManagement.debug("ClassItem.hard_enemy_logic()")

def story_chest():
    for i in chest_to_seed:
        chest_to_seed[i] = i
    enemy_skip_list.append("N3006")
    enemy_skip_list.append("N3005")
    ClassManagement.debug("ClassItem.story_chest()")

def remove_infinite():
    while "Gebelsglasses" in ClassManagement.item_drop_data["Accessory"]["ItemPool"]:
        ClassManagement.item_drop_data["Accessory"]["ItemPool"].remove("Gebelsglasses")
    while "Gebelsglasses" in ClassManagement.quest_requirement_data["Memento"]["ItemPool"]:
        ClassManagement.quest_requirement_data["Memento"]["ItemPool"].remove("Gebelsglasses")
    while "Recyclehat" in ClassManagement.item_drop_data["Headgear"]["ItemPool"]:
        ClassManagement.item_drop_data["Headgear"]["ItemPool"].remove("Recyclehat")
    while "Recyclehat" in ClassManagement.quest_requirement_data["Memento"]["ItemPool"]:
        ClassManagement.quest_requirement_data["Memento"]["ItemPool"].remove("Recyclehat")
    ClassManagement.debug("ClassItem.remove_infinite()")

def give_shortcut():
    ClassManagement.drop_content[6]["Value"]["RareItemId"] = "Shortcut"
    ClassManagement.drop_content[6]["Value"]["RareItemQuantity"] = 7
    ClassManagement.drop_content[6]["Value"]["RareItemRate"] = 100.0
    while "Shortcut" in ClassManagement.shard_drop_data["ItemPool"]:
        ClassManagement.shard_drop_data["ItemPool"].remove("Shortcut")
    ClassManagement.debug("ClassItem.give_shortcut()")
    
def give_eye():
    ClassManagement.drop_content[6]["Value"]["CommonItemId"] = "SkilledDetectiveeye"
    ClassManagement.drop_content[6]["Value"]["CommonItemQuantity"] = 1
    ClassManagement.drop_content[6]["Value"]["CommonRate"] = 100.0
    while "Detectiveeye" in ClassManagement.shard_drop_data["ItemPool"]:
        ClassManagement.shard_drop_data["ItemPool"].remove("Detectiveeye")
    ClassManagement.debug("ClassItem.give_eye()")

def give_extra(shard):
    ClassManagement.drop_content[6]["Value"]["RareIngredientId"] = shard
    ClassManagement.drop_content[6]["Value"]["RareIngredientQuantity"] = 1
    ClassManagement.drop_content[6]["Value"]["RareIngredientRate"] = 100.0
    if shard in key_shards:
        key_shards.remove(shard)
        all_keys.remove(shard)
        for i in ClassManagement.logic_data:
            if ClassManagement.logic_data[i][shard]:
                ClassManagement.logic_data[i]["GateRoom"] = False
                for e in ClassManagement.logic_data:
                    if i in ClassManagement.logic_data[e]["NearestGate"]:
                        ClassManagement.logic_data[e]["NearestGate"] = ClassManagement.logic_data[i]["NearestGate"]
    else:
        while shard in ClassManagement.shard_drop_data["ItemPool"]:
            ClassManagement.shard_drop_data["ItemPool"].remove(shard)
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
        all_rooms.append(i)
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
            if ClassManagement.logic_data[i]["GateRoom"] and previous_in_nearest(previous_gate, ClassManagement.logic_data[i]["NearestGate"]) and not i in previous_gate:
                for e in key_items:
                    if ClassManagement.logic_data[i][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
                for e in key_shards:
                    if ClassManagement.logic_data[i][e]:
                        requirement.append(e)
                        requirement_to_gate[e].append(i)
        #CheckIfRequirementIsntAlreadySatisfied
        check = False
        for i in key_item_to_location:
            if i in requirement:
                check = True
                for e in requirement_to_gate[i]:
                    previous_gate.append(e)
        for i in key_shard_to_location:
            if i in requirement:
                check = True
                for e in requirement_to_gate[i]:
                    previous_gate.append(e)
        if check:
            continue
        #GatheringRoomsAvailableBeforeGate
        for i in ClassManagement.logic_data:
            if not ClassManagement.logic_data[i]["GateRoom"] and previous_in_nearest(previous_gate, ClassManagement.logic_data[i]["NearestGate"]) or i in previous_gate:
                #IncreasingChancesOfLateRooms
                gate_count = 1
                gate_list = ClassManagement.logic_data[i]["NearestGate"]
                while gate_list:
                    nearest_gate = random.choice(gate_list)
                    for e in ClassManagement.logic_data:
                        if e == nearest_gate:
                            gate_count += 1
                            gate_list = ClassManagement.logic_data[e]["NearestGate"]
                            break
                #IncreasingChancesOfBossRooms
                if i in boss_rooms:
                    gate_count *= 6
                for e in range(gate_count):
                    previous_room.append(i)
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
    return ClassManagement.enemy_location_data[enemy]["NormalModeRooms"]

def logic_choice(chosen_item, room_list):
    #RemovingKeyFromList
    while chosen_item in all_keys:
        all_keys.remove(chosen_item)
    #ChoosingRoomToPlaceItemIn
    check = False
    while not check:
        chosen_room = random.choice(room_list)
        if chosen_room in list(key_item_to_location.values()) or chosen_room in list(key_shard_to_location.values()) or chosen_room == "m01SIP_000":
            continue
        #CheckingIfRoomHasChest
        if chosen_item in key_items:
            check = room_chest_check(chosen_room)
        #CheckingIfRoomHasEnemy
        if chosen_item in key_shards:
            check = room_enemy_check(chosen_room)
    #UpdatingKeyLocation
    if chosen_item in key_items:
        key_item_to_location[chosen_item] = chosen_room
    if chosen_item in key_shards:
        key_shard_to_location[chosen_item] = chosen_room

def room_chest_check(room):
    for i in ClassManagement.drop_content:
        #CheckingIfChestIsntUnused
        if i["Key"] in chest_to_seed:
            #CheckingIfChestCorrespondsToRoom
            if chest_to_room(i["Key"]) == room:
                return True
    return False

def room_enemy_check(room):
    for i in ClassManagement.enemy_location_data:
        #CheckingIfEnemyHasShardSlotAndIsInRoom
        if not i in enemy_skip_list and ClassManagement.enemy_location_data[i]["HasShard"] and room in ClassManagement.enemy_location_data[i]["NormalModeRooms"]:
            #CheckingIfEnemyIsntInAlreadyAssignedRoom
            for e in key_shard_to_location:
                if key_shard_to_location[e] in ClassManagement.enemy_location_data[i]["NormalModeRooms"]:
                    return False
            return True
    return False

def room_to_chest():
    for i in key_item_to_location:
        #GatheringPossibleChestChoices
        possible_chests = []
        for e in ClassManagement.drop_content:
            if e["Key"] in chest_to_seed:
                if key_item_to_location[i][3:].replace("_", "") in e["Key"]:
                    possible_chests.append(e["Key"])
                try:
                    if e["Key"] in room_to_special_chest[key_item_to_location[i]]:
                        possible_chests.append(e["Key"])
                except KeyError:
                    continue
        #PickingChest
        key_item_to_location[i] = random.choice(possible_chests)

def room_to_enemy():
    for i in key_shard_to_location:
        #GatheringPossibleEnemyChoices
        possible_enemy = []
        for e in ClassManagement.enemy_location_data:
            if not e in enemy_skip_list and ClassManagement.enemy_location_data[e]["HasShard"] and key_shard_to_location[i] in ClassManagement.enemy_location_data[e]["NormalModeRooms"]:
                #IncreasingChancesOfUncommonEnemies
                for o in range(math.ceil(36/len(ClassManagement.enemy_location_data[e]["NormalModeRooms"]))):
                    possible_enemy.append(e)
        #CheckingIfEnemyIsntAlreadyTaken
        chosen_enemy = random.choice(possible_enemy)
        while chosen_enemy in list(key_shard_to_location.values()):
            chosen_enemy = random.choice(possible_enemy)
        #Changing
        key_shard_to_location[i] = chosen_enemy

def fill_log():
    for i in key_items:
        log[ClassManagement.item_translation[i]] = [chest_to_room(key_item_to_location[i])]
    for i in key_shards:
        log[ClassManagement.shard_translation[i]] = enemy_to_room(key_shard_to_location[i])

def rand_overworld_key():
    key_logic()
    #KeyItems
    for i in key_items:
        patch_key_item_entry(i, key_item_to_location[i])
    #KeyShards
    for i in ClassManagement.drop_content:
        i["Value"]["DropSpecialFlags"] = "EDropSpecialFlag::None"
    for i in key_shards:
        patch_key_shard_entry(i, key_shard_to_location[i])
    #OtherKeys
    for i in other_key:
        patch_key_item_entry(i, random.choice(list(chest_to_seed)))
    ClassManagement.debug("ClassItem.rand_overworld_key()")

def rand_ship_waystone():
    #CheckStartingKey
    if not "Doublejump" in key_shards or not "Dimensionshift" in key_shards or not "Reflectionray" in key_shards:
        ship_height()
    if not "HighJump" in key_shards or not "Invert" in key_shards:
        ship_flight()
    #CheckShardsOnShip
    for i in key_shards:
        for e in ClassManagement.enemy_location_data[key_shard_to_location[i]]["NormalModeRooms"]:
            if "m01SIP" in e and e not in ship_skip_list:
                if i == "Doublejump" or i == "Dimensionshift" or i == "Reflectionray":
                    ship_height()
                if i == "HighJump" or i == "Invert":
                    ship_flight()
    #AssignChest
    chosen_chest = random.choice(ship_chest_list)
    while chosen_chest not in chest_to_seed:
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
    while i <= 630:
        if ClassManagement.drop_content[i]["Key"].split("_")[0] in list(key_shard_to_location.values()) or ClassManagement.drop_content[i]["Value"]["ShardRate"] == 0.0 or ClassManagement.drop_content[i]["Key"].split("_")[0] in enemy_skip_list:
            i += 1
            continue
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == ClassManagement.drop_content[i-1]["Key"].split("_")[0]:
            ClassManagement.drop_content[i]["Value"]["ShardId"] = ClassManagement.drop_content[i-1]["Value"]["ShardId"]
        else:
            ClassManagement.drop_content[i]["Value"]["ShardId"] = any_pick(ClassManagement.shard_drop_data["ItemPool"], True, "None")
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
        ClassManagement.drop_content[i]["Value"]["ShardRate"] = ClassManagement.shard_drop_data["ItemRate"]
        if ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3090" or ClassManagement.drop_content[i]["Key"].split("_")[0] == "N3099":
            ClassManagement.drop_content[i]["Value"]["ShardRate"] /= 2
        if ClassManagement.drop_content[i]["Value"]["DropSpecialFlags"] == "EDropSpecialFlag::DropShardOnce":
            ClassManagement.drop_content[i]["Value"]["ShardRate"] *= 3
        if ClassManagement.drop_content[i]["Value"]["ShardRate"] > 100.0:
            ClassManagement.drop_content[i]["Value"]["ShardRate"] = 100.0
    #FireCannonShardFix
    if not "N3005" in enemy_skip_list:
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
    del chest_to_seed[chest]
    
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
    ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data["Weapon"]["ItemPool"], ClassManagement.item_drop_data["Weapon"]["IsUnique"], "Weapon")
    ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data["Weapon"]["ItemQuantity"]
    ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data["Weapon"]["ItemRate"]
    if ClassManagement.drop_content[i]["Value"]["RareItemId"] in gun_list:
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data["Bullet"]["ItemPool"], ClassManagement.item_drop_data["Bullet"]["IsUnique"], "Bullet")
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.item_drop_data["Bullet"]["ItemQuantity"]*3
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.item_drop_data["Bullet"]["ItemRate"]
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
    if ClassManagement.drop_content[i]["Key"] not in chest_to_seed:
        return
    i = seed_convert(i)
    if ClassManagement.item_drop_data[item_type]["ChestColor"] == "Blue":
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], False, item_type)
        ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = random.choice(coin)
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::D" + str(ClassManagement.drop_content[i]["Value"]["CoinOverride"])
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = 0.0
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = True
    elif ClassManagement.item_drop_data[item_type]["ChestColor"] == "Red":
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
        ClassManagement.drop_content[i]["Value"]["CoinOverride"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], ClassManagement.item_drop_data[item_type]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["CoinType"] = "EDropCoin::D2000"
        ClassManagement.drop_content[i]["Value"]["CoinRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
        ClassManagement.drop_content[i]["Value"]["AreaChangeTreasureFlag"] = False
    else:
        ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], ClassManagement.item_drop_data[item_type]["IsUnique"], item_type)
        ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]
        ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.item_drop_data[item_type]["ItemRate"]
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
    if item_type == "CookingMat":
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["CookingMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data["CookingMat"]["ItemPool"], ClassManagement.enemy_drop_data["CookingMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["StandardMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data["StandardMat"]["ItemPool"], ClassManagement.enemy_drop_data["StandardMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"], ClassManagement.enemy_drop_data["EnemyMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["CookingMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data["CookingMat"]["ItemPool"], ClassManagement.enemy_drop_data["CookingMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == "StandardMat":
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["StandardMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.item_drop_data["StandardMat"]["ItemPool"], ClassManagement.enemy_drop_data["StandardMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"], ClassManagement.enemy_drop_data["EnemyMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["CookingMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data["CookingMat"]["ItemPool"], ClassManagement.enemy_drop_data["CookingMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["StandardMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.item_drop_data["StandardMat"]["ItemPool"], ClassManagement.enemy_drop_data["StandardMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0
    elif item_type == "EnemyMat":
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = any_pick(ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"], ClassManagement.enemy_drop_data["EnemyMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareItemRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["CookingMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = any_pick(ClassManagement.item_drop_data["CookingMat"]["ItemPool"], ClassManagement.enemy_drop_data["CookingMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = ClassManagement.enemy_drop_data["CookingMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonItemId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonItemQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.item_drop_data["StandardMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = any_pick(ClassManagement.item_drop_data["StandardMat"]["ItemPool"], ClassManagement.enemy_drop_data["StandardMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = ClassManagement.enemy_drop_data["StandardMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["RareIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["RareIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["RareIngredientRate"] = 0.0
        if random.choice(odd) == 1 and ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"]:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = any_pick(ClassManagement.enemy_drop_data["EnemyMat"]["ItemPool"], ClassManagement.enemy_drop_data["EnemyMat"]["IsUnique"], item_type)
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemQuantity"]
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = ClassManagement.enemy_drop_data["EnemyMat"]["ItemRate"]*item_rate
        else:
            ClassManagement.drop_content[i]["Value"]["CommonIngredientId"] = "None"
            ClassManagement.drop_content[i]["Value"]["CommonIngredientQuantity"] = 0
            ClassManagement.drop_content[i]["Value"]["CommonIngredientRate"] = 0.0

def seed_convert(i):
    new_chest = chest_to_seed[ClassManagement.drop_content[i]["Key"]]
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
    keys_list = list(ClassManagement.enemy_location_data)
    for i in range(len(keys_list)):
        if keys_list[i][0] != "N" or keys_list[i] == "N2013":
            continue
        enemy_req_number.append(i)
    for i in range(19):
        enemy_req_index.append(any_pick(enemy_req_number, True, "None"))
    enemy_req_index.sort()
    for i in range(19):
        ClassManagement.quest_content[i]["Value"]["Enemy01"] = keys_list[enemy_req_index[i]]
        ClassManagement.quest_content[i]["Value"]["EnemyNum01"] = len(ClassManagement.enemy_location_data[keys_list[enemy_req_index[i]]]["NormalModeRooms"])
        enemy_room = ""
        for e in ClassManagement.enemy_location_data[keys_list[enemy_req_index[i]]]["NormalModeRooms"]:
            enemy_room += e + ","
        ClassManagement.quest_content[i]["Value"]["EnemySpawnLocations"] = enemy_room[:-1]
    #MementoQuests
    i = 20
    while i <= 34:
        ClassManagement.quest_content[i]["Value"]["Item01"] = any_pick(ClassManagement.quest_requirement_data["Memento"]["ItemPool"], True, "None")
        i += 1
    #CateringQuests
    i = 35
    while i <= 55:
        ClassManagement.quest_content[i]["Value"]["Item01"] = any_pick(ClassManagement.quest_requirement_data["Catering"]["ItemPool"], True, "None")
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
        if ClassManagement.item_drop_data[item_type]["ChestColor"] == "Blue":
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], ClassManagement.item_drop_data[item_type]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[item_type]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]*9
        elif ClassManagement.item_drop_data[item_type]["ChestColor"] == "Red":
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = "Money"
            ClassManagement.quest_content[i]["Value"]["RewardNum01"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], ClassManagement.item_drop_data[item_type]["IsUnique"], item_type)
        else:
            ClassManagement.quest_content[i]["Value"]["RewardItem01"] = any_pick(ClassManagement.item_drop_data[item_type]["ItemPool"], ClassManagement.item_drop_data[item_type]["IsUnique"], item_type)
            if ClassManagement.item_drop_data[item_type]["IsUnique"]:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = 1
            else:
                ClassManagement.quest_content[i]["Value"]["RewardNum01"] = ClassManagement.item_drop_data[item_type]["ItemQuantity"]*3
    invert_ratio()
    ClassManagement.debug("ClassItem.rand_quest_pool()")

def catering_quest_info():
    ClassManagement.scenario_content["Table"]["QST_Catering_Name01"] = ClassManagement.item_translation[ClassManagement.quest_content[35]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name02"] = ClassManagement.item_translation[ClassManagement.quest_content[50]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name03"] = ClassManagement.item_translation[ClassManagement.quest_content[51]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name04"] = ClassManagement.item_translation[ClassManagement.quest_content[42]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name05"] = ClassManagement.item_translation[ClassManagement.quest_content[41]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name06"] = ClassManagement.item_translation[ClassManagement.quest_content[39]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name07"] = ClassManagement.item_translation[ClassManagement.quest_content[44]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name08"] = ClassManagement.item_translation[ClassManagement.quest_content[38]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name09"] = ClassManagement.item_translation[ClassManagement.quest_content[52]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name10"] = ClassManagement.item_translation[ClassManagement.quest_content[45]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name11"] = ClassManagement.item_translation[ClassManagement.quest_content[40]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name12"] = ClassManagement.item_translation[ClassManagement.quest_content[49]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name13"] = ClassManagement.item_translation[ClassManagement.quest_content[46]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name14"] = ClassManagement.item_translation[ClassManagement.quest_content[37]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name15"] = ClassManagement.item_translation[ClassManagement.quest_content[53]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name16"] = ClassManagement.item_translation[ClassManagement.quest_content[47]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name17"] = ClassManagement.item_translation[ClassManagement.quest_content[36]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name18"] = ClassManagement.item_translation[ClassManagement.quest_content[54]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name19"] = ClassManagement.item_translation[ClassManagement.quest_content[43]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name20"] = ClassManagement.item_translation[ClassManagement.quest_content[48]["Value"]["Item01"]]
    ClassManagement.scenario_content["Table"]["QST_Catering_Name21"] = ClassManagement.item_translation[ClassManagement.quest_content[55]["Value"]["Item01"]]
    ClassManagement.debug("ClassItem.catering_quest_info()")

def all_hair_in_shop():
    i = 521
    while i <= 532:
        ClassManagement.item_content[i]["Value"]["buyPrice"] = 100
        ClassManagement.item_content[i]["Value"]["Producted"] = "Event_01_001_0000"
        i += 1
    ClassManagement.debug("ClassItem.all_hair_in_shop()")

def no_key_in_shop():
    ClassManagement.item_content[561]["Value"]["buyPrice"] = 0
    ClassManagement.item_content[561]["Value"]["sellPrice"] = 0
    ClassManagement.item_content[886]["Value"]["buyPrice"] = 0
    ClassManagement.item_content[886]["Value"]["sellPrice"] = 0
    ClassManagement.debug("ClassItem.no_key_in_shop()")

def rand_shop_pool():
    for i in ClassManagement.item_drop_data:
        for e in shop_skip_list:
            while e in ClassManagement.item_drop_data[i]["ItemPool"]:
                ClassManagement.item_drop_data[i]["ItemPool"].remove(e)
        chosen = []
        for e in range(ClassManagement.item_drop_data[i]["ShopRatio"]):
            if ClassManagement.item_drop_data[i]["ItemPool"]:
                chosen.append(any_pick(ClassManagement.item_drop_data[i]["ItemPool"], True, "None"))
        for e in ClassManagement.item_content:
            if e["Key"] in shop_skip_list:
                continue
            if e["Key"] in chosen:
                e["Value"]["Producted"] = random.choice(event_type)
            elif e["Value"]["ItemType"] == "ECarriedCatalog::" + ClassManagement.item_drop_data[i]["ShopName"] or e["Value"]["ItemType"] == "ECarriedCatalog::Seed" and ClassManagement.item_drop_data[i]["ShopName"] == "FoodStuff":
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
            i["Value"]["sellPrice"] = int(chosen/20)
        else:
            i["Value"]["sellPrice"] = int(chosen/10)
        if i["Value"]["sellPrice"] < 1:
            i["Value"]["sellPrice"] = 1
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
        if ClassManagement.item_drop_data[i]["IsUnique"]:
            continue
        ratio = []
        new_list = []
        duplicate = 1
        for e in range(len(ClassManagement.item_drop_data[i]["ItemPool"]) - 1):
            previous = ClassManagement.item_drop_data[i]["ItemPool"][e]
            current = ClassManagement.item_drop_data[i]["ItemPool"][e + 1]
            if current == previous:
                duplicate += 1
            else:
                ratio.append(duplicate)
                duplicate = 1
            if e == len(ClassManagement.item_drop_data[i]["ItemPool"]) - 2:
                ratio.append(duplicate)
            e += 1
        max_ratio = max(ratio)
        ClassManagement.item_drop_data[i]["ItemPool"] = list(dict.fromkeys(ClassManagement.item_drop_data[i]["ItemPool"]))
        for e in range(len(ClassManagement.item_drop_data[i]["ItemPool"])):
            for o in range(abs(ratio[e] - (max_ratio + 1))):
                new_list.append(ClassManagement.item_drop_data[i]["ItemPool"][e])
        ClassManagement.item_drop_data[i]["ItemPool"] = new_list

def get_log():
    return log