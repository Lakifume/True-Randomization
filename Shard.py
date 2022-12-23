import Manager
import math
import random
import copy

def init():
    #DeclareVariables
    global average_power
    average_power = 50
    global average_cost
    average_cost = 80
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
        "Tornadoslicer",
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
        "Shadowtracer",
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
        "Venomsmog"
    ]

def default_shard():
    #Recalculate default shard power in a more convenient way for balance
    for i in Manager.datatable["PB_DT_ShardMaster"]:
        if not i in Manager.mod_data["ShardBase"]:
            continue
        base = Manager.datatable["PB_DT_ShardMaster"][i]["useMP"] * Manager.mod_data["ShardBase"][i]["Base"]
        if i in skip_list or i == "Healing":
            balance = 1.0
        elif i in special_list:
            balance = (average_power/base)**correction
        else:
            balance = (average_cost/Manager.datatable["PB_DT_ShardMaster"][i]["useMP"])**correction
        Manager.datatable["PB_DT_ShardMaster"][i]["minGradeValue"] = round(base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][i]["maxGradeValue"] = round(base * balance * Manager.mod_data["ShardBase"][i]["Grade"], 3)

def rand_shard(scale):
    for i in Manager.datatable["PB_DT_ShardMaster"]:
        #Only randomize shards that have an entry in shard base
        if not i in Manager.mod_data["ShardBase"]:
            continue
        if i in skip_list or i == "LigaDoin":
            continue
        original_cost      = int(Manager.datatable["PB_DT_ShardMaster"][i]["useMP"])
        original_doin_cost = int(Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"])
        #Reduce the range for shards that can be pulsed
        if i in special_list or i == "Healing":
            reduction = 3
        else:
            reduction = 1
        #Randome magic cost first
        multiplier = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 3)/original_cost
        Manager.datatable["PB_DT_ShardMaster"][i]["useMP"] = int(original_cost * multiplier)
        #Riga Doin explosion is shared with Riga Storeama
        if i == "LigaStreyma":
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"] = int(original_doin_cost * multiplier)
        #Randomize power based on magic cost
        if scale:
            new_cost      = Manager.datatable["PB_DT_ShardMaster"][i]["useMP"]
            new_doin_cost = Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"]
        else:
            multiplier    = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 3)/original_cost
            new_cost      = int(original_cost * multiplier)
            new_doin_cost = int(original_doin_cost * multiplier)
        new_base = new_cost * Manager.mod_data["ShardBase"][i]["Base"]
        #Prevent power from scaling too high or too low
        if i == "Healing":
            balance = 1.0
        elif i in special_list:
            balance = (1/(multiplier**0.5))*(average_power/new_base)**correction
        else:
            balance = (average_cost/new_cost)**correction
        Manager.datatable["PB_DT_ShardMaster"][i]["minGradeValue"] = round(new_base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][i]["maxGradeValue"] = round(new_base * balance * Manager.mod_data["ShardBase"][i]["Grade"], 3)
        #Riga Doin explosion is shared with Riga Storeama
        if i == "LigaStreyma":
            new_doin_base = new_doin_cost * Manager.mod_data["ShardBase"]["LigaDoin"]["Base"]
            balance       = (average_cost/new_doin_cost)**correction
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["minGradeValue"] = round(new_doin_base * balance, 3)
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["maxGradeValue"] = round(new_doin_base * balance * Manager.mod_data["ShardBase"]["LigaDoin"]["Grade"], 3)

def update_special_properties():
    #A few shards have a multiplier different than 1.0 in DamageMaster so update their shard power based on that
    for i in ["minGradeValue", "maxGradeValue"]:
        Manager.datatable["PB_DT_ShardMaster"]["DragonicRage"][i] = round(Manager.datatable["PB_DT_ShardMaster"]["DragonicRage"][i] / 1.45, 3)
        Manager.datatable["PB_DT_ShardMaster"]["SummonAme"][i]    = round(Manager.datatable["PB_DT_ShardMaster"]["SummonAme"][i]    / 0.75, 3)

def rescale_level_based_shards():
    #Money is Power and Red Rememberance only take starting stats and level up stats in account
    #So considerably increase their multipliers to make them useful if level 1 capped
    Manager.datatable["PB_DT_CoordinateParameter"]["P0000_MONEYISPOWER_ATTACK_RATE_MAX"]["Value"] = 0.5
    #Unfortunately Red Rememberance seems to be capped at 1.0
    Manager.datatable["PB_DT_ShardMaster"]["RedDowther"]["minGradeValue"] = 0.5
    Manager.datatable["PB_DT_ShardMaster"]["RedDowther"]["maxGradeValue"] = 1.0