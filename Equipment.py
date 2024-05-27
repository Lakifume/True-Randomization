from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Enemy
import Room
import Graphic
import Sound
import Bloodless
import Utility

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
    global dlc_weapons
    dlc_weapons = [
        "Scythe",
        "MagicalScepter",
        "PirateSword",
        "PirateGun",
        "Wagasa"
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
        "Boots":           45,
        "Knife":           50,
        "Rapir":           52,
        "ShortSword":      58,
        "Club":            58,
        "LargeSword":      84,
        "JapaneseSword":   52,
        "Spear":           58,
        "Whip":            52,
        "Gun":             32,
        "Scythe":          55,
        "MagicalGirlWand": 26
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

def set_global_stat_weight(weight):
    global global_stat_weight
    global_stat_weight = Utility.weight_exponents[weight - 1]

def reset_zangetsu_black_belt():
    #Playable Zangetsu has the Black Belt on by default giving him extra stats
    #In Progressive Zangetsu we want all his starting stats to be 0
    datatable["PB_DT_ArmorMaster"]["Blackbelt"]["STR"] = 0
    datatable["PB_DT_ArmorMaster"]["Blackbelt"]["CON"] = 0

def randomize_equipment_stats():
    for entry in datatable["PB_DT_ArmorMaster"]:
        #Only randomize equipment that has a description entry
        if not "ITEM_EXPLAIN_" + entry in stringtable["PBMasterStringTable"]:
            continue
        #Some equipments have extreme stats that need to be evenly multiplied
        if has_negative_stat(entry):
            list = []
            for stat in stat_to_property:
                if datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                list.append(abs(datatable["PB_DT_ArmorMaster"][entry][stat]))
            multiplier = Utility.random_weighted(min(list), 1, int(min(list)*1.2), 1, global_stat_weight)/min(list)
            for stat in stat_to_property:
                if datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                datatable["PB_DT_ArmorMaster"][entry][stat] = round(datatable["PB_DT_ArmorMaster"][entry][stat]*multiplier)
        #The rest can be semi-random
        else:
            for stat in stat_to_property:
                if datatable["PB_DT_ArmorMaster"][entry][stat] == 0:
                    continue
                max_value = 20 if entry == "SkullNecklace" else equipment_type_to_max_value[datatable["PB_DT_ArmorMaster"][entry]["SlotType"].split("::")[1]][stat_to_property[stat]]
                datatable["PB_DT_ArmorMaster"][entry][stat] = Utility.random_weighted(datatable["PB_DT_ArmorMaster"][entry][stat], 1, int(max_value*1.2), 1, global_stat_weight)
    #Shovel Armor's attack
    max_value = weapon_type_to_max_value["LargeSword"]
    min_value = round(max_value*min_value_multiplier)
    datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"] = Utility.random_weighted(int(datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"]), int(min_value*low_bound_multiplier), int(max_value*high_bound_multiplier), 1, global_stat_weight)

def randomize_weapon_power():
    for entry in datatable["PB_DT_WeaponMaster"]:
        if datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] == 0:
            continue
        max_value = weapon_type_to_max_value[datatable["PB_DT_WeaponMaster"][entry]["WeaponType"].split("::")[1]]
        min_value = round(max_value*min_value_multiplier)
        reduction = get_weapon_reduction(entry)
        weapon_tier = get_weapon_tier(entry)
        if weapon_tier == 0:
            datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = Utility.random_weighted(datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"], int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction), 1, global_stat_weight)
        #Make progressive weapons retain their tier system
        if weapon_tier == 1:
            high_tier_name = (entry[:-1] if entry[-1].isnumeric() else entry) + str(3 if entry in bit_weapons else 5 if "Pirate" in entry else 4)
            weapon_power = Utility.random_weighted(datatable["PB_DT_WeaponMaster"][high_tier_name]["MeleeAttack"], int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction), 1, global_stat_weight)/3
            datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(weapon_power)
        if weapon_tier == 2:
            datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(weapon_power*2)
        if weapon_tier == 3:
            datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = int(weapon_power*3)
        #Update magic attack for weapons with elemental attributes
        if datatable["PB_DT_WeaponMaster"][entry]["MagicAttack"] != 0:
            datatable["PB_DT_WeaponMaster"][entry]["MagicAttack"] = datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"]

def randomize_cheat_equipment_stats():
    #Cheat equipments stats are completely random
    #Gives them a chance to not be useless
    for entry in datatable["PB_DT_ArmorMaster"]:
        if entry in cheat_equip:
            for stat in stat_to_property:
                #Avoid having direct attack stats as this would favor rapid weapons over slow ones
                if stat_to_property[stat] == "Attack":
                    continue
                if random.random() < 0.25:
                    max_value = equipment_type_to_max_value[datatable["PB_DT_ArmorMaster"][entry]["SlotType"].split("::")[1]][stat_to_property[stat]]
                    if random.random() < 7/8:
                        datatable["PB_DT_ArmorMaster"][entry][stat] =  random.randint(1, int(max_value*1.2))
                    else:
                        datatable["PB_DT_ArmorMaster"][entry][stat] = -random.randint(1, int(max_value*1.2)*2)

def randomize_cheat_weapon_power():
    #Cheat weapons stats are completely random
    #Gives them a chance to not be completely useless
    for entry in datatable["PB_DT_WeaponMaster"]:
        if entry in cheat_weapon:
            max_value = weapon_type_to_max_value[datatable["PB_DT_WeaponMaster"][entry]["WeaponType"].split("::")[1]]
            min_value = round(max_value*min_value_multiplier)
            reduction = get_weapon_reduction(entry)
            datatable["PB_DT_WeaponMaster"][entry]["MeleeAttack"] = random.randint(int(min_value*low_bound_multiplier*reduction), int(max_value*high_bound_multiplier*reduction))
            #Randomize special effect rate too
            if datatable["PB_DT_WeaponMaster"][entry]["SpecialEffectDenominator"] != 0.0:
                datatable["PB_DT_WeaponMaster"][entry]["SpecialEffectDenominator"] = random.randint(1, 3)

def update_special_properties():
    datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_BloodBringer"]["Value"] = int(datatable["PB_DT_WeaponMaster"]["BradBlingerLv1"]["MeleeAttack"]*2.3)
    datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_RedbeastEdge"]["Value"] = datatable["PB_DT_WeaponMaster"]["CrystalSword3"]["MeleeAttack"]
    datatable["PB_DT_CoordinateParameter"]["WeaponGrowMaxAtk_Izayoi"]["Value"]       = int(datatable["PB_DT_WeaponMaster"]["Truesixteenthnight"]["MeleeAttack"]*1.2)

def add_armor_reference(armor_id):
    #Give a specific armor its own graphical asset pointer when equipped
    datatable["PB_DT_ArmorMaster"][armor_id]["ReferencePath"] = f"/Game/Core/Item/Body/BDBP_{armor_id}.BDBP_{armor_id}"
    new_file = UAsset("\\".join([Manager.asset_dir, Manager.file_to_path["BDBP_BodyValkyrie"], "BDBP_BodyValkyrie.uasset"]), EngineVersion.VER_UE4_22)
    index = new_file.SearchNameReference(FString("BDBP_BodyValkyrie_C"))
    new_file.SetNameReference(index, FString(f"BDBP_{armor_id}_C"))
    index = new_file.SearchNameReference(FString("Default__BDBP_BodyValkyrie_C"))
    new_file.SetNameReference(index, FString(f"Default__BDBP_{armor_id}_C"))
    default_body_mat          = constant["ArmorReference"][armor_id]["DefaultBodyMat"]         + "." + constant["ArmorReference"][armor_id]["DefaultBodyMat"].split("/")[-1]
    chroma_body_mat           = constant["ArmorReference"][armor_id]["ChromaBodyMat"]          + "." + constant["ArmorReference"][armor_id]["ChromaBodyMat"].split("/")[-1]
    default_skin_mat          = constant["ArmorReference"][armor_id]["DefaultSkinMat"]         + "." + constant["ArmorReference"][armor_id]["DefaultSkinMat"].split("/")[-1]
    chroma_skin_mat           = constant["ArmorReference"][armor_id]["ChromaSkinMat"]          + "." + constant["ArmorReference"][armor_id]["ChromaSkinMat"].split("/")[-1]
    dialogue_default_skin_mat = constant["ArmorReference"][armor_id]["DialogueDefaultSkinMat"] + "." + constant["ArmorReference"][armor_id]["DialogueDefaultSkinMat"].split("/")[-1]
    dialogue_chroma_skin_mat  = constant["ArmorReference"][armor_id]["DialogueChromaSkinMat"]  + "." + constant["ArmorReference"][armor_id]["DialogueChromaSkinMat"].split("/")[-1]
    new_file.Imports[18].ObjectName            = FName.FromString(new_file, constant["ArmorReference"][armor_id]["Mesh"])
    new_file.Imports[27].ObjectName            = FName.FromString(new_file, constant["ArmorReference"][armor_id]["Mesh"].split("/")[-1])
    new_file.Exports[1].Data[0].Value[0].Value = FSoftObjectPath(None, FName.FromString(new_file, chroma_body_mat), None)
    new_file.Exports[1].Data[1].Value[0].Value = FSoftObjectPath(None, FName.FromString(new_file, default_body_mat), None)
    new_file.Exports[1].Data[2].Value          = FSoftObjectPath(None, FName.FromString(new_file, chroma_skin_mat), None)
    sub_struct                                 = SoftObjectPropertyData()
    sub_struct.Value                           = FSoftObjectPath(None, FName.FromString(new_file, default_skin_mat), None)
    new_file.Exports[1].Data[3].Value          = [sub_struct]
    new_file.Exports[1].Data[4].Value          = FSoftObjectPath(None, FName.FromString(new_file, dialogue_chroma_skin_mat), None)
    new_file.Exports[1].Data[5].Value          = FSoftObjectPath(None, FName.FromString(new_file, dialogue_default_skin_mat), None)
    new_file.Exports[1].Data[9].Value          = False
    new_file.Exports[1].Data[10].Value         = 1
    new_file.Exports[1].Data[11].Value         = 0
    new_file.Write("\\".join([Manager.mod_dir, Manager.file_to_path["BDBP_BodyValkyrie"], f"BDBP_{armor_id}.uasset"]))

def has_negative_stat(equipment):
    for stat in stat_to_property:
        if datatable["PB_DT_ArmorMaster"][equipment][stat] < 0:
            return True
    return False

def get_weapon_tier(weapon):
    if weapon in bit_weapons + dlc_weapons:
        return 1
    if weapon[:-1] in bit_weapons:
        return int(weapon[-1])
    if weapon[:-1] in dlc_weapons:
        return (int(weapon[-1]) + (0 if "Pirate" in weapon else 1))//2 + 1
    return 0

def get_weapon_reduction(weapon):
    #Apply reductions to weapons with special properties to not make them super broken
    if "ShieldWeapon" in weapon:
        return 0.9
    if "Wagasa" in weapon:
        return 0.4
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
    if datatable["PB_DT_WeaponMaster"][weapon]["FLA"]:
        return 0.9
    if datatable["PB_DT_WeaponMaster"][weapon]["LIG"]:
        return 0.8
    if datatable["PB_DT_WeaponMaster"][weapon]["UniqeValue"] != 0.0:
        return 0.9
    if datatable["PB_DT_WeaponMaster"][weapon]["SpecialEffectId"] in ["Stone", "Slow"]:
        return 0.6
    if datatable["PB_DT_WeaponMaster"][weapon]["SpecialEffectId"] != "None":
        return 0.8
    return 1.0