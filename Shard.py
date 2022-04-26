import Manager
import math
import random

def init():
    #DeclareVariables
    global average_power
    average_power = 50
    global correction
    correction = 0.2
    global min_cost
    min_cost = 1
    global max_cost
    max_cost = 300
    global stat_pool
    stat_pool = []
    global special_list
    special_list = [
        "Jackpot",
        "ChangeBunny",
        "Voidlay",
        "Chiselbalage",
        "TissRosain",
        "FoldingTurb"
    ]
    global skip_list
    skip_list = [
        "Bloodsteel",
        "SummonChair",
        "Demoniccapture",
        "Accelerator",
        "AccelWorld",
        "Beastguard",
        "Sacredshade",
        "Reflectionray",
        "Aquastream",
        "Dimensionshift",
        "GoldBarrett",
        "Aimingshield",
        "CurseDray",
        "Petrey",
        "PetraBless",
        "Acidgouache",
        "Venomsmog",
        "LigaDoin"
    ]

def default_shard():
    #Recalculate default shard power in a more convenient way for balance
    for i in Manager.datatable["PB_DT_ShardMaster"]:
        if not i in Manager.dictionary["ShardBase"]:
            continue
        base = Manager.datatable["PB_DT_ShardMaster"][i]["useMP"] * Manager.dictionary["ShardBase"][i]["Base"]
        if i in skip_list or i == "Healing":
            balance = 1.0
        else:
            balance = (average_power/base)**correction
        Manager.datatable["PB_DT_ShardMaster"][i]["minGradeValue"] = round(base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][i]["maxGradeValue"] = round(base * balance * Manager.dictionary["ShardBase"][i]["Grade"], 3)

def rand_shard(scale):
    for i in Manager.datatable["PB_DT_ShardMaster"]:
        #Only randomize shards that have an entry in shard base
        if not i in Manager.dictionary["ShardBase"]:
            continue
        if i in skip_list:
            continue
        original_cost      = Manager.datatable["PB_DT_ShardMaster"][i]["useMP"]
        original_doin_cost = Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"]
        #Reduce the range for shards that can be pulsed
        if i in special_list:
            reduction = 3
        else:
            reduction = 1
        #Randome magic cost first
        multiplier = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 4)/original_cost
        Manager.datatable["PB_DT_ShardMaster"][i]["useMP"] = int(Manager.datatable["PB_DT_ShardMaster"][i]["useMP"] * multiplier)
        #Riga Doin explosion is shared with Riga Storeama
        if i == "LigaStreyma":
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"] = int(Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"] * multiplier)
        #Randomize power based on magic cost
        if not scale:
            multiplier = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 4)/original_cost
        new_base = original_cost * Manager.dictionary["ShardBase"][i]["Base"] * multiplier
        #Prevent power from scaling too high or too low
        if i == "Healing":
            balance = 1.0
        elif i in special_list:
            balance = 1/(multiplier**0.5)
        else:
            balance = (average_power/new_base)**correction
        Manager.datatable["PB_DT_ShardMaster"][i]["minGradeValue"] = round(new_base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][i]["maxGradeValue"] = round(new_base * balance * Manager.dictionary["ShardBase"][i]["Grade"], 3)
        #Riga Doin explosion is shared with Riga Storeama
        if i == "LigaStreyma":
            doin_base = original_doin_cost * Manager.dictionary["ShardBase"]["LigaDoin"]["Base"] * multiplier
            balance   = (average_power/doin_base)**correction
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["minGradeValue"] = round(doin_base * balance, 3)
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["maxGradeValue"] = round(doin_base * balance * Manager.dictionary["ShardBase"]["LigaDoin"]["Grade"], 3)

def eye_max_range():
    #Give Detective's Eye infinite range
    Manager.datatable["PB_DT_ShardMaster"]["Detectiveeye"]["minGradeValue"] = 999.0
    Manager.datatable["PB_DT_ShardMaster"]["Detectiveeye"]["maxGradeValue"] = 999.0