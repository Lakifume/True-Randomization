import Manager
import math
import random
import copy

def init():
    global cheat_equip
    cheat_equip = [
        "HumptyDumpty",
        "LoveOfBenki",
        "Plan9FOSpace",
        "Mega64Head",
        "HeyI’mGrump",
        "I’mNotSoGrump",
        "AKindaFunnyMask",
        "BigMustache",
        "PlagueDoctorFace",
        "The-BazMask"
    ]
    global cheat_weapon
    cheat_weapon = [
        "ClockSowrd",
        "LoveOfPizza",
        "KongSword",
        "SwordOfTheMushroom",
        "PowerSword",
        "SilverAndBlackSword",
        "DungeonNightSword",
        "EvilTheSword"
    ]
    global stat_to_property
    stat_to_property = {
        "MeleeAttack":  "Attack",
        "MagicAttack":  "Attack",
        "MeleeDefense": "Defense",
        "MagicDefense": "Defense",
        "ZAN":          "Resist",
        "DAG":          "Resist",
        "TOT":          "Resist",
        "FLA":          "Resist",
        "ICE":          "Resist",
        "LIG":          "Resist",
        "HOL":          "Resist",
        "DAR":          "Resist",
        "POI":          "Status",
        "CUR":          "Status",
        "STO":          "Status",
        "STR":          "Stat",
        "CON":          "Stat",
        "INT":          "Stat",
        "MND":          "Stat",
        "LUC":          "Stat"
    }
    global weapon_type_to_max_value
    weapon_type_to_max_value = {
        "Boots":         [ 8, 45],
        "Knife":         [10, 52],
        "Rapir":         [12, 52],
        "ShortSword":    [12, 58],
        "Club":          [12, 58],
        "LargeSword":    [17, 84],
        "JapaneseSword": [13, 52],
        "Spear":         [13, 58],
        "Whip":          [13, 52],
        "Gun":           [ 5, 32]
    }
    global equipment_type_to_max_value
    equipment_type_to_max_value = {
        "Head": {
            "Attack":   0,
            "Defense": 20,
            "Resist":  10,
            "Status":  20,
            "Stat":     8
        },
        "Muffler": {
            "Attack":   0,
            "Defense":  7,
            "Resist":  10,
            "Status":  10,
            "Stat":     5
        },
        "Accessory1": {
            "Attack":   5,
            "Defense":  5,
            "Resist":  20,
            "Status":  20,
            "Stat":    10
        },
        "Body": {
            "Attack":   0,
            "Defense": 50,
            "Resist":  10,
            "Status":  10,
            "Stat":    10
        }
    }
    global stat_pool
    stat_pool = []
    positives = Manager.create_weighted_list(0,   0, 30, 1, 3)[1]
    negatives = Manager.create_weighted_list(0, -60,  0, 1, 3)[0]
    zeros = [0]
    for i in range(4):
        stat_pool.append(positives)
    for i in range(1):
        stat_pool.append(negatives)
    for i in range(15):
        stat_pool.append(zeros)

def zangetsu_black_belt():
    #Playable Zangetsu has the Black Belt on by default giving him extra stats
    #In Progressive Zangetsu we want all his starting stats to be 0
    Manager.datatable["PB_DT_ArmorMaster"]["Blackbelt"]["STR"] = 0
    Manager.datatable["PB_DT_ArmorMaster"]["Blackbelt"]["CON"] = 0

def rand_all_equip():
    for i in Manager.datatable["PB_DT_ArmorMaster"]:
        #Only randomize equipment that has a description entry
        if not "ITEM_EXPLAIN_" + i in Manager.stringtable["PBMasterStringTable"]:
            continue
        #Some equipments have extreme stats that need to be evenly multiplied
        if has_negative_stat(i):
            list = []
            for e in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][i][e] == 0:
                    continue
                list.append(abs(Manager.datatable["PB_DT_ArmorMaster"][i][e]))
            multiplier = Manager.random_weighted(min(list), 1, int(min(list)*1.2), 1, 3)/min(list)
            for e in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][i][e] == 0:
                    continue
                Manager.datatable["PB_DT_ArmorMaster"][i][e] = round(Manager.datatable["PB_DT_ArmorMaster"][i][e]*multiplier)
        #The rest can be semi-random
        else:
            for e in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][i][e] == 0:
                    continue
                max = equipment_type_to_max_value[Manager.datatable["PB_DT_ArmorMaster"][i]["SlotType"].split("::")[1]][stat_to_property[e]]
                Manager.datatable["PB_DT_ArmorMaster"][i][e] = Manager.random_weighted(Manager.datatable["PB_DT_ArmorMaster"][i][e], 1, int(max*1.2), 1, 3)
    #Shovel Armor's attack
    Manager.datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"] = Manager.random_weighted(int(Manager.datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"]), int(weapon_type_to_max_value["LargeSword"][0]*0.8), int(weapon_type_to_max_value["LargeSword"][1]*1.2), 1, 3)

def rand_all_weapon():
    for i in Manager.datatable["PB_DT_WeaponMaster"]:
        if Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] == 0:
            continue
        min = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][i]["WeaponType"].split("::")[1]][0]
        max = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][i]["WeaponType"].split("::")[1]][1]
        #Apply reductions to weapons with special properties to not make them super broken
        if i == "Juwuse":
            reduction = 0.85
        elif i in ["KillerBoots", "Decapitator"]:
            reduction = 0.9
        elif i in ["Swordbreaker", "Adrastea"]:
            reduction = 0.8
        elif i in ["Liddyl", "SwordWhip", "BradBlingerLv1"]:
            reduction = 23/weapon_type_to_max_value["ShortSword"][1]
        elif i == "OutsiderKnightSword":
            reduction = 13/32
        elif i in ["RemoteDart", "OracleBlade"]:
            reduction = 30/weapon_type_to_max_value["ShortSword"][1]
        elif i in ["WalalSoulimo", "ValralAltar"]:
            reduction = 12/weapon_type_to_max_value["ShortSword"][1]
        elif i == "Truesixteenthnight":
            reduction = 49/weapon_type_to_max_value["JapaneseSword"][1]
        elif Manager.datatable["PB_DT_WeaponMaster"][i]["FLA"]:
            reduction = 0.9
        elif Manager.datatable["PB_DT_WeaponMaster"][i]["LIG"]:
            reduction = 0.8
        elif Manager.datatable["PB_DT_WeaponMaster"][i]["UniqeValue"] != 0.0:
            reduction = 0.9
        elif Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectId"] == "Stone":
            reduction = 0.6
        elif Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectId"] != "None":
            reduction = 0.8
        else:
            reduction = 1.0
        #Make 8 bit weapons retain their tier system
        if i in Manager.bit_weapons:
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = Manager.random_weighted(Manager.datatable["PB_DT_WeaponMaster"][i + "3"]["MeleeAttack"], int(min*0.8*reduction), int(max*1.2*reduction), 1, 3)
            bweapon = Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"]/3
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = int(bweapon)
        elif i[:-1] in Manager.bit_weapons and i[-1] == "2":
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = int(bweapon*2)
        elif i[:-1] in Manager.bit_weapons and i[-1] == "3":
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = int(bweapon*3)
        else:
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = Manager.random_weighted(Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"], int(min*0.8*reduction), int(max*1.2*reduction), 1, 3)
        #Update magic attack for weapons with elemental attributes
        if Manager.datatable["PB_DT_WeaponMaster"][i]["MagicAttack"] != 0:
            Manager.datatable["PB_DT_WeaponMaster"][i]["MagicAttack"] = Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"]

def rand_cheat_equip():
    #Cheat equipments stats are completely random
    #Gives them a chance to not be completely useless
    for i in Manager.datatable["PB_DT_ArmorMaster"]:
        if i in cheat_equip:
            for e in stat_to_property:
                #Avoid having direct attack stats as this would favor rapid weapons over slow ones
                if stat_to_property[e] == "Attack":
                    continue
                Manager.datatable["PB_DT_ArmorMaster"][i][e] = random.choice(random.choice(stat_pool))

def rand_cheat_weapon():
    #Cheat weapons stats are completely random
    #Gives them a chance to not be completely useless
    for i in Manager.datatable["PB_DT_WeaponMaster"]:
        if i in cheat_weapon:
            min = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][i]["WeaponType"].split("::")[1]][0]
            max = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][i]["WeaponType"].split("::")[1]][1]
            if Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectId"] == "Stone":
                reduction = 0.6
            elif Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectId"] != "None":
                reduction = 0.8
            else:
                reduction = 1.0
            Manager.datatable["PB_DT_WeaponMaster"][i]["MeleeAttack"] = random.randint(int(min*0.8*reduction), int(max*1.2*reduction))
            #Randomize special effect rate too
            if Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectDenominator"] != 0.0:
                Manager.datatable["PB_DT_WeaponMaster"][i]["SpecialEffectDenominator"] = random.randint(1, 3)

def update_special_properties():
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_BloodBringer"]["Value"] = int(Manager.datatable["PB_DT_WeaponMaster"]["BradBlingerLv1"]["MeleeAttack"]*2.3)
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_RedbeastEdge"]["Value"] = Manager.datatable["PB_DT_WeaponMaster"]["CrystalSword3"]["MeleeAttack"]
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_Izayoi"]["Value"]       = int(Manager.datatable["PB_DT_WeaponMaster"]["Truesixteenthnight"]["MeleeAttack"]*1.2)

def has_negative_stat(equipment):
    for i in stat_to_property:
        if Manager.datatable["PB_DT_ArmorMaster"][equipment][i] < 0:
            return True
    return False