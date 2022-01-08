import ClassManagement
import math
import random

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
special_list = [
    "Safering",
    "Cursering",
    "Riskring",
    "Adversityring"
]

property_list = [
    "MeleeAttack", 
    "MagicAttack",
    "MeleeDefense",
    "MagicDefense",
    "ZAN",
    "DAG",
    "TOT",
    "FLA",
    "ICE",
    "LIG",
    "HOL",
    "DAR",
    "POI",
    "CUR",
    "STO",
    "STR",
    "CON",
    "INT",
    "MND",
    "LUC"
]
attack_list = [
    "MeleeAttack", 
    "MagicAttack"
]
defense_list = [
    "MeleeDefense",
    "MagicDefense"
]
resist_list = [
    "ZAN",
    "DAG",
    "TOT",
    "FLA",
    "ICE",
    "LIG",
    "HOL",
    "DAR"
]
status_list = [
    "POI",
    "CUR",
    "STO"
]
stat_list = [
    "STR",
    "CON",
    "INT",
    "MND",
    "LUC"
]

weapon_type_to_max_value = {
    "Boots":         [8, 45],
    "Knife":         [8, 45],
    "Rapir":         [12, 52],
    "ShortSword":    [12, 58],
    "Club":          [15, 52],
    "LargeSword":    [17, 84],
    "JapaneseSword": [13, 52],
    "Spear":         [13, 58],
    "Whip":          [13, 52],
    "Gun":           [5, 32]
}
equipment_type_to_max_value = {
    "Head": {
        "Attack": 0,
        "Defense": 20,
        "Resist": 10,
        "Status": 20,
        "Stat": 8
    },
    "Muffler": {
        "Attack": 0,
        "Defense": 7,
        "Resist": 10,
        "Status": 10,
        "Stat": 5
    },
    "Accessory1": {
        "Attack": 5,
        "Defense": 5,
        "Resist": 20,
        "Status": 20,
        "Stat": 10
    },
    "Body": {
        "Attack": 0,
        "Defense": 50,
        "Resist": 10,
        "Status": 10,
        "Stat": 10
    }
}

stat_pool = []
armor_log = {}
weapon_log = {}

def init():
    stat_int = -60
    for i in range(60 + 30 + 1):
        if stat_int < 0:
            for e in range(2**(abs(math.ceil(abs(stat_int)/12)-5))):
                stat_pool.append(stat_int)
        elif stat_int > 0:
            for e in range(2**(abs(math.ceil(stat_int/6)-5))*8):
                stat_pool.append(stat_int)
        stat_int += 1
    for i in range(len(stat_pool)*4):
        stat_pool.append(0)
    ClassManagement.debug("ClassEquipment.init()")

def zangetsu_black_belt():
    ClassManagement.armor_content[109]["Value"]["STR"] = 0
    ClassManagement.armor_content[109]["Value"]["CON"] = 0
    ClassManagement.debug("ClassEquipment.zangetsu_black_belt()")

def rand_all_equip():
    #ShovelArmorAttack
    ClassManagement.coordinate_content[28]["Value"]["Value"] = random.choice(create_list(ClassManagement.coordinate_content[28]["Value"]["Value"], int(weapon_type_to_max_value["LargeSword"][0]*0.8), int(weapon_type_to_max_value["LargeSword"][1]*1.2))) + 0.0
    ClassManagement.master_content["Table"]["ITEM_EXPLAIN_Shovelarmorsarmor"] = ClassManagement.master_content["Table"]["ITEM_EXPLAIN_Shovelarmorsarmor"].split("<span color=\"#ff0000\">")[0] + "<span color=\"#ff0000\">wATK " + str(int(ClassManagement.coordinate_content[28]["Value"]["Value"])) + "</> "
    #AllArmor
    for i in ClassManagement.armor_content:
        try:
            test = ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]]
        except KeyError:
            continue
        if i["Key"] in special_list:
            list = []
            for e in property_list:
                if i["Value"][e] == 0:
                    continue
                list.append(abs(i["Value"][e]))
            multiplier = random.choice(create_list(min(list), 1, int(min(list)*1.2)))/min(list)
            for e in property_list:
                if i["Value"][e] == 0:
                    continue
                i["Value"][e] = round(i["Value"][e]*multiplier)
        else:
            for e in property_list:
                if i["Value"][e] == 0:
                    continue
                if e in attack_list:
                    max = equipment_type_to_max_value[i["Value"]["SlotType"].split("::")[1]]["Attack"]
                elif e in defense_list:
                    max = equipment_type_to_max_value[i["Value"]["SlotType"].split("::")[1]]["Defense"]
                elif e in resist_list:
                    max = equipment_type_to_max_value[i["Value"]["SlotType"].split("::")[1]]["Resist"]
                elif e in status_list:
                    max = equipment_type_to_max_value[i["Value"]["SlotType"].split("::")[1]]["Status"]
                elif e in stat_list:
                    max = equipment_type_to_max_value[i["Value"]["SlotType"].split("::")[1]]["Stat"]
                i["Value"][e] = random.choice(create_list(i["Value"][e], 1, int(max*1.2)))
        if i["Value"]["MagicAttack"] != 0:
            ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]] = ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]].split("<span color=\"#ff8000\">")[0] + "<span color=\"#ff8000\">mATK " + str(i["Value"]["MagicAttack"]) + "</> "
        if i["Value"]["MagicDefense"] != 0:
            ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]] = ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]].split("<span color=\"#ff00ff\">")[0] + "<span color=\"#ff00ff\">mDEF " + str(i["Value"]["MagicDefense"]) + "</>"
    ClassManagement.debug("ClassEquipment.rand_all_equip()")

def rand_all_weapon():
    for i in range(len(ClassManagement.weapon_content)):
        if ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] == 0:
            continue
        min = weapon_type_to_max_value[ClassManagement.weapon_content[i]["Value"]["WeaponType"].split("::")[1]][0]
        max = weapon_type_to_max_value[ClassManagement.weapon_content[i]["Value"]["WeaponType"].split("::")[1]][1]
        #Reductions
        if ClassManagement.weapon_content[i]["Key"] == "KillerBoots" or ClassManagement.weapon_content[i]["Key"] == "Decapitator" or ClassManagement.weapon_content[i]["Key"] == "Swordbreaker" or ClassManagement.weapon_content[i]["Key"] == "Adrastea" or ClassManagement.weapon_content[i]["Value"]["FLA"] or ClassManagement.weapon_content[i]["Value"]["LIG"] or ClassManagement.weapon_content[i]["Value"]["UniqeValue"] != 0.0:
            reduction = 0.9
        elif ClassManagement.weapon_content[i]["Key"] == "Liddyl" or ClassManagement.weapon_content[i]["Key"] == "SwordWhip" or ClassManagement.weapon_content[i]["Key"] == "BradBlingerLv1" or ClassManagement.weapon_content[i]["Key"] == "OutsiderKnightSword":
            reduction = 0.4
        elif ClassManagement.weapon_content[i]["Key"] == "RemoteDart" or ClassManagement.weapon_content[i]["Key"] == "OracleBlade":
            reduction = 0.5
        elif ClassManagement.weapon_content[i]["Key"] == "WalalSoulimo" or ClassManagement.weapon_content[i]["Key"] == "ValralAltar":
            reduction = 0.24
        elif ClassManagement.weapon_content[i]["Key"] == "Truesixteenthnight":
            reduction = 0.94
        elif ClassManagement.weapon_content[i]["Value"]["SpecialEffectId"] != "None":
            reduction = 0.8
        else:
            reduction = 1.0
        #8BitWeapons
        if ClassManagement.weapon_content[i]["Key"][-1] == "2":
            ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] = int(bweapon*2)
        elif ClassManagement.weapon_content[i]["Key"][-1] == "3":
            ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] = int(bweapon*3)
        elif "Bweapon" in ClassManagement.weapon_content[i]["Value"]["ReferencePath"]["Package"] and ClassManagement.weapon_content[i]["Key"] != "HuntedBrad" and ClassManagement.weapon_content[i]["Key"] != "SteamFlatWideEnd" and ClassManagement.weapon_content[i]["Key"] != "OgreWoodenSword":
            ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] = random.choice(create_list(ClassManagement.weapon_content[i+2]["Value"]["MeleeAttack"], int(min*0.8*reduction), int(max*1.2*reduction)))
            bweapon = ClassManagement.weapon_content[i]["Value"]["MeleeAttack"]/3
            ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] = int(bweapon)
        else:
            ClassManagement.weapon_content[i]["Value"]["MeleeAttack"] = random.choice(create_list(ClassManagement.weapon_content[i]["Value"]["MeleeAttack"], int(min*0.8*reduction), int(max*1.2*reduction)))
        #MagicAttack
        if ClassManagement.weapon_content[i]["Value"]["MagicAttack"] != 0:
            ClassManagement.weapon_content[i]["Value"]["MagicAttack"] = ClassManagement.weapon_content[i]["Value"]["MeleeAttack"]
    #SpecialWeaponScaling
    ClassManagement.coordinate_content[16]["Value"]["Value"] = int( ClassManagement.weapon_content[41]["Value"]["MeleeAttack"]*2.3) + 0.0
    ClassManagement.coordinate_content[17]["Value"]["Value"] = ClassManagement.weapon_content[140]["Value"]["MeleeAttack"] + 0.0
    ClassManagement.coordinate_content[18]["Value"]["Value"] = int(ClassManagement.weapon_content[79]["Value"]["MeleeAttack"]*1.2) + 0.0
    ClassManagement.debug("ClassEquipment.rand_all_weapon()")

def create_list(value, minimum, maximum):
    list = []
    list_int = minimum
    for i in range(maximum-minimum+1):
        for e in range(2**(abs(math.ceil(abs(list_int-value)*5/max(value-minimum, maximum-value))-5))):
            list.append(list_int)
        list_int += 1
    return list

def rand_cheat_equip():
    for i in ClassManagement.armor_content:
        if i["Key"] in cheat_equip:
            for e in property_list:
                i["Value"][e] = random.choice(stat_pool)
            if i["Value"]["MagicAttack"] != 0:
                ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]] += "<span color=\"#ff8000\">mATK " + str(i["Value"]["MagicAttack"]) + "</> "
            if i["Value"]["MagicDefense"] != 0:
                ClassManagement.master_content["Table"]["ITEM_EXPLAIN_" + i["Key"]] += "<span color=\"#ff00ff\">mDEF " + str(i["Value"]["MagicDefense"]) + "</>"
            armor_log[ClassManagement.item_translation[i["Key"]]] = {}
            for e in property_list:
                armor_log[ClassManagement.item_translation[i["Key"]]][e] = i["Value"][e]
    ClassManagement.debug("ClassEquipment.rand_cheat_equip()")

def rand_cheat_weapon():
    for i in ClassManagement.weapon_content:
        if i["Key"] in cheat_weapon:
            min = weapon_type_to_max_value[i["Value"]["WeaponType"].split("::")[1]][0]
            max = weapon_type_to_max_value[i["Value"]["WeaponType"].split("::")[1]][1]
            if i["Value"]["SpecialEffectId"] != "None":
                reduction = 0.8
            else:
                reduction = 1.0
            i["Value"]["MeleeAttack"] = random.randint(int(min*0.8*reduction), int(max*1.2*reduction))
            if i["Value"]["SpecialEffectDenominator"] != 0.0:
                i["Value"]["SpecialEffectDenominator"] = random.randint(1, 3) + 0.0
            weapon_log[ClassManagement.item_translation[i["Key"]]] = {}
            weapon_log[ClassManagement.item_translation[i["Key"]]]["MeleeAttack"] = i["Value"]["MeleeAttack"]
            if i["Value"]["SpecialEffectDenominator"] == 3.0:
                weapon_log[ClassManagement.item_translation[i["Key"]]]["SpecialEffectRate"] = "Rare"
            elif i["Value"]["SpecialEffectDenominator"] == 2.0:
                weapon_log[ClassManagement.item_translation[i["Key"]]]["SpecialEffectRate"] = "Occasional"
            elif i["Value"]["SpecialEffectDenominator"] == 1.0:
                weapon_log[ClassManagement.item_translation[i["Key"]]]["SpecialEffectRate"] = "Frequent"
            else:
                weapon_log[ClassManagement.item_translation[i["Key"]]]["SpecialEffectRate"] = "None"
    ClassManagement.debug("ClassEquipment.rand_cheat_weapon()")

def get_armor_log():
    return armor_log

def get_weapon_log():
    return weapon_log