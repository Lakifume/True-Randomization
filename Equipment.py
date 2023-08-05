import Manager
import Utility
import random

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
        "Boots":         45,
        "Knife":         50,
        "Rapir":         52,
        "ShortSword":    58,
        "Club":          58,
        "LargeSword":    84,
        "JapaneseSword": 52,
        "Spear":         58,
        "Whip":          52,
        "Gun":           32
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
            "Attack":   0,
            "Defense":  5,
            "Resist":  10,
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
    global min_value_multiplier
    min_value_multiplier = 0.2
    global low_bound_multiplier
    low_bound_multiplier = 0.8
    global high_bound_multiplier
    high_bound_multiplier = 1.2

def set_global_stat_wheight(wheight):
    global global_stat_wheight
    global_stat_wheight = Manager.wheight_exponents[wheight - 1]

def reset_zangetsu_black_belt():
    #Playable Zangetsu has the Black Belt on by default giving him extra stats
    #In Progressive Zangetsu we want all his starting stats to be 0
    Manager.datatable["PB_DT_ArmorMaster"]["Blackbelt"]["STR"] = 0
    Manager.datatable["PB_DT_ArmorMaster"]["Blackbelt"]["CON"] = 0

def randomize_equipment_stats():
    for entry in Manager.datatable["PB_DT_ArmorMaster"]:
        #Only randomize equipment that has a description entry
        if not "ITEM_EXPLAIN_" + entry in Manager.stringtable["PBMasterStringTable"]:
            continue
        #Some equipments have extreme stats that need to be evenly multiplied
        if has_negative_stat(entry):
            list = []
            for stat in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                list.append(abs(Manager.datatable["PB_DT_ArmorMaster"][entry][stat]))
            multiplier = Utility.random_weighted(min(list), 1, int(min(list)*1.2), 1, global_stat_wheight)/min(list)
            for stat in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                Manager.datatable["PB_DT_ArmorMaster"][entry][stat] = round(Manager.datatable["PB_DT_ArmorMaster"][entry][stat]*multiplier)
        #The rest can be semi-random
        else:
            for stat in stat_to_property:
                if Manager.datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                if entry == "SkullNecklace":
                    max_value = 20
                else:
                    max_value = equipment_type_to_max_value[Manager.datatable["PB_DT_ArmorMaster"][entry]["SlotType"].split("::")[1]][stat_to_property[stat]]
                Manager.datatable["PB_DT_ArmorMaster"][entry][stat] = Utility.random_weighted(Manager.datatable["PB_DT_ArmorMaster"][entry][stat], 1, int(max_value*1.2), 1, global_stat_wheight)
    #Shovel Armor's attack
    max_value = weapon_type_to_max_value["LargeSword"]
    min_value = round(max_value*min_value_multiplier)
    Manager.datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"] = Utility.random_weighted(int(Manager.datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"]), int(min_value*low_bound_multiplier), int(max_value*high_bound_multiplier), 1, global_stat_wheight)

def randomize_weapon_power():
    for entry in Manager.datatable["PB_DT_WeaponMaster"]:
        if Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] == 0:
            continue
        max_value = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][entry]["WeaponType"].split("::")[1]]
        min_value = round(max_value*min_value_multiplier)
        reduction = get_weapon_reduction(entry)
        #Make 8 bit weapons retain their tier system
        if entry in Manager.bit_weapons:
            bweapon_power = Utility.random_weighted(Manager.datatable["PB_DT_WeaponMaster"][entry + "3"]["MeleeAttack"], int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction), 1, global_stat_wheight)/3
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(bweapon_power)
        elif entry[:-1] in Manager.bit_weapons and entry[-1] == "2":
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(bweapon_power*2)
        elif entry[:-1] in Manager.bit_weapons and entry[-1] == "3":
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(bweapon_power*3)
        else:
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = Utility.random_weighted(Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"], int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction), 1, global_stat_wheight)
        #Update magic attack for weapons with elemental attributes
        if Manager.datatable["PB_DT_WeaponMaster"][entry]["MagicAttack"] != 0:
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MagicAttack"] = Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"]

def randomize_cheat_equipment_stats():
    #Cheat equipments stats are completely random
    #Gives them a chance to not be useless
    for entry in Manager.datatable["PB_DT_ArmorMaster"]:
        if entry in cheat_equip:
            for stat in stat_to_property:
                #Avoid having direct attack stats as this would favor rapid weapons over slow ones
                if stat_to_property[stat] == "Attack":
                    continue
                if random.random() < 0.25:
                    max_value = equipment_type_to_max_value[Manager.datatable["PB_DT_ArmorMaster"][entry]["SlotType"].split("::")[1]][stat_to_property[stat]]
                    if random.random() < 7/8:
                        Manager.datatable["PB_DT_ArmorMaster"][entry][stat] =  random.randint(1, int(max_value*1.2))
                    else:
                        Manager.datatable["PB_DT_ArmorMaster"][entry][stat] = -random.randint(1, int(max_value*1.2)*2)

def randomize_cheat_weapon_power():
    #Cheat weapons stats are completely random
    #Gives them a chance to not be completely useless
    for entry in Manager.datatable["PB_DT_WeaponMaster"]:
        if entry in cheat_weapon:
            max_value = weapon_type_to_max_value[Manager.datatable["PB_DT_WeaponMaster"][entry]["WeaponType"].split("::")[1]]
            min_value = round(max_value*min_value_multiplier)
            reduction = get_weapon_reduction(entry)
            Manager.datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = random.randint(int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction))
            #Randomize special effect rate too
            if Manager.datatable["PB_DT_WeaponMaster"][entry]["SpecialEffectDenominator"] != 0.0:
                Manager.datatable["PB_DT_WeaponMaster"][entry]["SpecialEffectDenominator"] = random.randint(1, 3)

def update_special_properties():
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_BloodBringer"]["Value"] = int(Manager.datatable["PB_DT_WeaponMaster"]["BradBlingerLv1"]["MeleeAttack"]*2.3)
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_RedbeastEdge"]["Value"] = Manager.datatable["PB_DT_WeaponMaster"]["CrystalSword3"]["MeleeAttack"]
    Manager.datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_Izayoi"]["Value"]       = int(Manager.datatable["PB_DT_WeaponMaster"]["Truesixteenthnight"]["MeleeAttack"]*1.2)

def has_negative_stat(equipment):
    for stat in stat_to_property:
        if Manager.datatable["PB_DT_ArmorMaster"][equipment][stat] < 0:
            return True
    return False

def get_weapon_reduction(weapon):
    #Apply reductions to weapons with special properties to not make them super broken
    if weapon == "Juwuse":
        return 0.85
    if weapon in ["KillerBoots", "Decapitator"]:
        return 0.9
    if weapon in ["Swordbreaker", "Adrastea"]:
        return 0.8
    if weapon in ["Liddyl", "SwordWhip", "BradBlingerLv1"]:
        return 23/weapon_type_to_max_value["ShortSword"]
    if weapon == "OutsiderKnightSword":
        return 13/32
    if weapon in ["RemoteDart", "OracleBlade"]:
        return 25/weapon_type_to_max_value["ShortSword"]
    if weapon in ["WalalSoulimo", "ValralAltar"]:
        return 12/weapon_type_to_max_value["ShortSword"]
    if weapon == "Truesixteenthnight":
        return 49/weapon_type_to_max_value["JapaneseSword"]
    if Manager.datatable["PB_DT_WeaponMaster"][weapon]["FLA"]:
        return 0.9
    if Manager.datatable["PB_DT_WeaponMaster"][weapon]["LIG"]:
        return 0.8
    if Manager.datatable["PB_DT_WeaponMaster"][weapon]["UniqeValue"] != 0.0:
        return 0.9
    if Manager.datatable["PB_DT_WeaponMaster"][weapon]["SpecialEffectId"] in ["Stone", "Slow"]:
        return 0.6
    if Manager.datatable["PB_DT_WeaponMaster"][weapon]["SpecialEffectId"] != "None":
        return 0.8
    return 1.0