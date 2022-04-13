import os
import shutil
import json
import math
import glob
import random
from enum import Enum
from collections import OrderedDict

class Direction(Enum):
    LEFT         = 0x0001
    BOTTOM       = 0x0002
    RIGHT        = 0x0004
    TOP          = 0x0008
    LEFT_BOTTOM  = 0x0010
    RIGHT_BOTTOM = 0x0020
    LEFT_TOP     = 0x0040
    RIGHT_TOP    = 0x0080
    TOP_LEFT     = 0x0100
    TOP_RIGHT    = 0x0200
    BOTTOM_RIGHT = 0x0400
    BOTTOM_LEFT  = 0x0800

OppositeDirection = {
    Direction.LEFT:         Direction.RIGHT,
    Direction.BOTTOM:       Direction.TOP,
    Direction.RIGHT:        Direction.LEFT,
    Direction.TOP:          Direction.BOTTOM,
    Direction.LEFT_BOTTOM:  Direction.RIGHT_BOTTOM,
    Direction.RIGHT_BOTTOM: Direction.LEFT_BOTTOM,
    Direction.LEFT_TOP:     Direction.RIGHT_TOP,
    Direction.RIGHT_TOP:    Direction.LEFT_TOP,
    Direction.TOP_LEFT:     Direction.BOTTOM_LEFT,
    Direction.TOP_RIGHT:    Direction.BOTTOM_RIGHT,
    Direction.BOTTOM_RIGHT: Direction.TOP_RIGHT,
    Direction.BOTTOM_LEFT:  Direction.TOP_LEFT,
}

class Door:
    def __init__(self, x_block, z_block, direction_part, breakable):
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        self.breakable = breakable

def init():
    global used_doors
    used_doors = []
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

def load_content():
    #DataTable
    global full_datatable
    full_datatable = {}
    for i in os.listdir("UAssetGUI\\DataTable"):
        name, extension = os.path.splitext(i)
        full_datatable[name] = {}
        with open("UAssetGUI\\DataTable\\" + i, "r", encoding="utf8") as file_reader:
            full_datatable[name]["DataTable"] = json.load(file_reader)
    #StoreExtraDataForConvenience
    for i in full_datatable:
        full_datatable[i]["KeyIndex"] = {}
        for e in range(len(full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"])):
            full_datatable[i]["KeyIndex"][full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"][e]["Name"]] = e
        full_datatable[i]["ValueIndex"] = {}
        for e in range(len(full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"][0]["Value"])):
            full_datatable[i]["ValueIndex"][full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"][0]["Value"][e]["Name"]] = e
        full_datatable[i]["ArrayStruct"] = {}
        for e in full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"]:
            for o in e["Value"]:
                if "ArrayPropertyData" in o["$type"] and o["Value"]:
                    full_datatable[i]["ArrayStruct"][o["Name"]] = o["Value"][0]
    #StringTable
    global full_stringtable
    full_stringtable = {}
    for i in os.listdir("UAssetGUI\\StringTable"):
        name, extension = os.path.splitext(i)
        with open("UAssetGUI\\StringTable\\" + i, "r", encoding="utf8") as file_reader:
            full_stringtable[name] = json.load(file_reader)
    #Blueprint
    global full_blueprint
    full_blueprint = {}
    for i in os.listdir("UAssetGUI\\Blueprint"):
        name, extension = os.path.splitext(i)
        with open("UAssetGUI\\Blueprint\\" + i, "r", encoding="utf8") as file_reader:
            full_blueprint[name] = json.load(file_reader)
    
def load_data():
    global dictionary
    dictionary = {}
    for i in os.listdir("Data\\Dictionary"):
        name, extension = os.path.splitext(i)
        with open("Data\\Dictionary\\" + i, "r", encoding="utf8") as file_reader:
            dictionary[name] = json.load(file_reader)
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json", "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    dictionary["MapLogic"] = json_file["KeyLogic"]
    dictionary["MapOrder"] = json_file["AreaOrder"]
    dictionary["MapOriginalOrder"] = json_file["AreaOrder"]

def load_custom_map(path):
    #Load the file for a custom map, overriding the vanilla RoomMaster file
    with open(path, "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    datatable["PB_DT_RoomMaster"] = json_file["MapData"]
    dictionary["MapLogic"] = json_file["KeyLogic"]
    dictionary["MapOrder"] = json_file["AreaOrder"]
    #The two underground rooms with very specific shapes only display properly based on their Y position below the origin
    #Start by resetting their no traverse list as if they were above 0
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaWidthSize"]*2
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaWidthSize"]*3
    #Then shoft those lists if the rooms are below 0
    if datatable["PB_DT_RoomMaster"]["m11UGD_013"]["OffsetZ"] < 0:
        multiplier = abs(int(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["OffsetZ"]/7.2)) - 1
        if multiplier > datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaHeightSize"] - 1:
            multiplier = datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaHeightSize"] - 1
        for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"])):
            datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"][i] -= datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaWidthSize"]*multiplier
    if datatable["PB_DT_RoomMaster"]["m11UGD_031"]["OffsetZ"] < 0:
        multiplier = abs(int(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["OffsetZ"]/7.2)) - 1
        if multiplier > datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaHeightSize"] - 1:
            multiplier = datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaHeightSize"] - 1
        for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"])):
            datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"][i] -= datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaWidthSize"]*multiplier
    #Each area has limitations as to where it can be displayed on the canvas
    #Change area IDs based on their X positions so that everything is always displayed
    for i in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][i]["OffsetX"] < 214.2:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m01SIP"
        elif datatable["PB_DT_RoomMaster"][i]["OffsetX"] + datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"]*12.6 > 1108.8:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m13ARC"
        else:
            datatable["PB_DT_RoomMaster"][i]["AreaID"] = "EAreaID::m03ENT"

def complex_to_simple():
    #The json files outputted by UAssetGUI are hard to read and would take up too much text space in the code
    #Convert them to a simplified version that is similar to Serializer's outputs
    global datatable
    datatable = {}
    for i in full_datatable:
        datatable[i] = {}
        for e in full_datatable[i]["DataTable"]["Exports"][0]["Table"]["Data"]:
            datatable[i][e["Name"]] = {}
            for o in e["Value"]:
                datatable[i][e["Name"]][o["Name"]] = read_datatable(i, e["Name"], o["Name"])
    global stringtable
    stringtable = {}
    for i in full_stringtable:
        stringtable[i] = {}
        for e in full_stringtable[i]["Exports"][0]["Table"]["StringTable"]:
            stringtable[i][e] = full_stringtable[i]["Exports"][0]["Table"]["StringTable"][e]
    #RoomMaster already has a simplified version from the map editor
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json", "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    datatable["PB_DT_RoomMaster"] = json_file["MapData"]

def simple_to_complex():
    #Convert the simplified datatables back to their complex versions
    for i in datatable:
        for e in datatable[i]:
            for o in datatable[i][e]:
                if i == "PB_DT_RoomMaster" and o == "Unused":
                    continue
                patch_datatable(i, e, o, datatable[i][e][o])
    for i in stringtable:
        for e in stringtable[i]:
            full_stringtable[i]["Exports"][0]["Table"]["StringTable"][e] = stringtable[i][e]

def apply_tweaks():
    #Make levels identical in all modes
    #This needs to be done before applying the json tweaks so that exceptions can be patched over
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(i)["Enemy"]:
            continue
        datatable["PB_DT_CharacterParameterMaster"][i]["HardEnemyLevel"]                       = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["NightmareEnemyLevel"]                  = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeDefaultEnemyLevel"]       = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeHardEnemyLevel"]          = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeNightmareEnemyLevel"]     = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyHPOverride"]         = 0.0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyExperienceOverride"] = 0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyStrIntMultiplier"]   = 1.0
        datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyConMndMultiplier"]   = 1.0
    #Apply manuel tweaks defined in the json
    for i in dictionary["DefaultTweak"]:
        for e in dictionary["DefaultTweak"][i]:
            for o in dictionary["DefaultTweak"][i][e]:
                datatable[i][e][o] = dictionary["DefaultTweak"][i][e][o]
    #Loop through all enemies
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(i)["Enemy"]:
            continue
        if datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"] == 0:
            continue
        if is_enemy(i)["Boss"]:
            #Make boss health scale with level
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*(99/datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]))
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]/5)*5
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP99Enemy"] = datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]
            #Expand expertise point range that scales with level
            #In vanilla the range is too small and barely makes a difference
            datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
            datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 15
            #Set stone type
            #Some regular enemies are originally set to the boss stone type which doesn't work well when petrified
            datatable["PB_DT_CharacterParameterMaster"][i]["StoneType"] = "EPBStoneType::Boss"
        else:
            datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
            datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 10
            datatable["PB_DT_CharacterParameterMaster"][i]["StoneType"] = "EPBStoneType::Mob"
        #Make level 1 health based off of level 99 health
        datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"] = int(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]/100) + 2.0
        datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP"] = datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"]
        #Make experience 80% of health
        if datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] > 0:
            datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = int(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*0.8)
            datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = int(datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"]/100) + 2
        #Give all enemies a luck stat which reduces the chances of critting them
        #Originally only Gebel, Valefar and OD have one
        if datatable["PB_DT_CharacterParameterMaster"][i]["LUC"] == 0:
            datatable["PB_DT_CharacterParameterMaster"][i]["LUC"]        = 5.0
            datatable["PB_DT_CharacterParameterMaster"][i]["LUC99Enemy"] = 50.0
        #Allow Zangetsu to chain grab everyone
        #Whether he can grab or not is entirely based on the enemy's stone resistance
        #As long as it's not 100% resist the chain grab will connect so cap stone resistance at 99.9%
        if datatable["PB_DT_CharacterParameterMaster"][i]["STO"] >= 100.0:
            datatable["PB_DT_CharacterParameterMaster"][i]["STO"] = 99.9
    #Make up for the increased expertise range
    for i in datatable["PB_DT_ArtsCommandMaster"]:
        datatable["PB_DT_ArtsCommandMaster"][i]["Expertise"] = int(datatable["PB_DT_ArtsCommandMaster"][i]["Expertise"]*2.5)
    #Lock 8 bit weapons behind recipes so that they aren't always easily accessible
    for i in datatable["PB_DT_CraftMaster"]:
        if i in bit_weapons:
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe018"
        elif i[:-1] in bit_weapons and i[-1] == "2":
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe019"
        elif i[:-1] in bit_weapons and i[-1] == "3":
            datatable["PB_DT_CraftMaster"][i]["OpenKeyRecipeID"] = "ArmsRecipe020"
    #Remove the minimal damage addition on attacks
    for i in datatable["PB_DT_DamageMaster"]:
        datatable["PB_DT_DamageMaster"][i]["FixedDamage"] = 0.0
    #Increase default drop rates
    for i in datatable["PB_DT_DropRateMaster"]:
        #Keep dulla head drops relatively low due to their spawn frequency
        if i.split("_")[0] in ["N3090", "N3099"]:
            drop_rate_multiplier = 0.5
        else:
            drop_rate_multiplier = 1.0
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["ShardRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = dictionary["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] = dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["CommonRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["CommonRate"] = dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] = dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] = dictionary["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
    #Loop through all items
    for i in datatable["PB_DT_ItemMaster"]:
        #Remove dishes from shop to prevent heal spam
        #In vanilla you can easily stock up on an infinite amount of them which breaks the game completely
        #This change also makes regular potions more viable now
        if i in dictionary["ItemDrop"]["Dish"]["ItemPool"]:
            datatable["PB_DT_ItemMaster"][i]["max"]       = 1
            datatable["PB_DT_ItemMaster"][i]["buyPrice"]  = 0
            datatable["PB_DT_ItemMaster"][i]["sellPrice"] = 0
        #Increase the selling price of consumables
        #It's not likely the player will give them up so they should be rewarding
        if datatable["PB_DT_ItemMaster"][i]["ItemType"] == "ECarriedCatalog::Potion":
            datatable["PB_DT_ItemMaster"][i]["sellPrice"] = int(datatable["PB_DT_ItemMaster"][i]["sellPrice"]*2.0)
        #On the other hand reduce the selling price of materials
        #Otherwise it's too easy to get money fast with the new drop rates
        if datatable["PB_DT_ItemMaster"][i]["ItemType"] in ["ECarriedCatalog::Ingredient", "ECarriedCatalog::FoodStuff", "ECarriedCatalog::Seed"]:
            datatable["PB_DT_ItemMaster"][i]["sellPrice"] = int(datatable["PB_DT_ItemMaster"][i]["sellPrice"]*0.5)
        #Update icon pointer of 8 bit weapons for the new icons
        #The icon texture was edited so that all new icons are evenly shifted from the original ones
        if i[:-1] in bit_weapons and i[-1] == "2":
            datatable["PB_DT_ItemMaster"][i]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][i]["IconPath"]) + 204)
        elif i[:-1] in bit_weapons and i[-1] == "3":
            datatable["PB_DT_ItemMaster"][i]["IconPath"] = str(int(datatable["PB_DT_ItemMaster"][i]["IconPath"]) + 338)
    #Loop through all shards
    for i in datatable["PB_DT_ShardMaster"]:
        #Make all shard colors match their type
        datatable["PB_DT_ShardMaster"][i]["ShardColorOverride"] = "EShardColor::None"
        #Make all shards ignore standstill
        datatable["PB_DT_ShardMaster"][i]["IsStopByAccelWorld"] = False
    #Rename the second Zangetsu boss so that he isn't confused with the first
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N1011_STRONG"] = dictionary["EnemyTranslation"]["N1011_STRONG"]
    #Update Jinrai cost description
    stringtable["PBMasterStringTable"]["ARTS_TXT_017_00"] = "<span size=\"30\">Jinrai</>\r\n \r\nDraw your blade and strike opponents down in one fierce motion.\r\n \r\n<image id=\"Text_Command_Arrow_Right\"/><image id=\"Text_Command_Arrow_Left\"/><image id=\"Text_Command_Arrow_Right\"/> + <input id=\"Attack\"/>\r\n\r\nMP Cost: " + str(datatable["PB_DT_ArtsCommandMaster"]["JSword_GodSpeed1"]["CostMP"])
    #Rebalance boss rush mode a bit
    #Remove all consumables from inventory
    for i in full_blueprint["PBExtraModeInfo_BP"]["Exports"][1]["Data"][7]["Value"]:
        i["Value"][1]["Value"] = 0
    #Start both stages at level 50
    for i in range(8, 14):
        full_blueprint["PBExtraModeInfo_BP"]["Exports"][1]["Data"][i]["Value"]  = 50
    #Give all bosses level 66
    for i in full_blueprint["PBExtraModeInfo_BP"]["Exports"][1]["Data"][14]["Value"]:
        i[1]["Value"] = 66
    #Keep a dict of the current enemy stats for easier scaling of during randomization
    global original_enemy_stats
    original_enemy_stats = {}
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        original_enemy_stats[i] = {}
        original_enemy_stats[i]["Level"] = datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        original_enemy_stats[i]["POI"]   = datatable["PB_DT_CharacterParameterMaster"][i]["POI"]
        original_enemy_stats[i]["CUR"]   = datatable["PB_DT_CharacterParameterMaster"][i]["CUR"]
        original_enemy_stats[i]["STO"]   = datatable["PB_DT_CharacterParameterMaster"][i]["STO"]
        original_enemy_stats[i]["SLO"]   = datatable["PB_DT_CharacterParameterMaster"][i]["SLO"]

def update_descriptions():
    #Add magical stats to descriptions
    for i in datatable["PB_DT_ArmorMaster"]:
        try:
            test = stringtable["PBMasterStringTable"]["ITEM_EXPLAIN_" + i]
        except KeyError:
            continue
        if datatable["PB_DT_ArmorMaster"][i]["MagicAttack"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff8000\">mATK " + str(datatable["PB_DT_ArmorMaster"][i]["MagicAttack"]) + "</>")
        if datatable["PB_DT_ArmorMaster"][i]["MagicDefense"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff00ff\">mDEF " + str(datatable["PB_DT_ArmorMaster"][i]["MagicDefense"]) + "</>")
    #Add restoration amount to descriptions
    for i in datatable["PB_DT_SpecialEffectDefinitionMaster"]:
        try:
            test = stringtable["PBMasterStringTable"]["ITEM_EXPLAIN_" + i]
        except KeyError:
            continue
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeHP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00ff00\">HP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeMP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00bfff\">MP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
    #Add Shovel Armor's attack stat to its description
    append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_Shovelarmorsarmor", "<span color=\"#ff0000\">wATK " + str(int(datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"])) + "</>")

def write_log(filename, filepath, log):
    with open(filepath + "\\" + filename + ".json", "w", encoding="utf8") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def read_datatable(file, entry, data):
    #Convert strings to indexes
    entry = full_datatable[file]["KeyIndex"][entry]
    data  = full_datatable[file]["ValueIndex"][data]
    #Handle special data types
    type  = full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["$type"]
    value = full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["Value"]
    #Round floats to 3 digits and fix the "+0" field
    if "FloatPropertyData" in type:
        if value == "+0":
            value = 0.0
        else:
            value = round(value, 3)
    #Convert name map index to enum
    elif "BytePropertyData" in type:
        value = full_datatable[file]["DataTable"]["NameMap"][value]
    #Convert array of structs to simple array
    elif "ArrayPropertyData" in type:
        new_array = []
        for i in value:
            new_array.append(i["Value"])
        value = new_array
    return value

def patch_datatable(file, entry, data, value):
    #Convert strings to indexes
    entry = full_datatable[file]["KeyIndex"][entry]
    data  = full_datatable[file]["ValueIndex"][data]
    #Handle special data types
    type = full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["$type"]
    name = full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["Name"]
    #Add string entry to the name map
    if "NamePropertyData" in type or "EnumPropertyData" in type:
        if not remove_inst(value) in full_datatable[file]["DataTable"]["NameMap"]:
            full_datatable[file]["DataTable"]["NameMap"].append(remove_inst(value))
    #Convert enum to its index in the name map
    elif "BytePropertyData" in type:
        try:
            index = full_datatable[file]["DataTable"]["NameMap"].index(value)
        except ValueError:
            full_datatable[file]["DataTable"]["NameMap"].append(value)
            index = full_datatable[file]["DataTable"]["NameMap"].index(value)
        value = index
    #Convert simple array to an array of structs
    elif "ArrayPropertyData" in type:
        if value:
            try:
                del full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["DummyStruct"]
            except KeyError:
                pass
            new_array = []
            for i in range(len(value)):
                new_struct = dict(full_datatable[file]["ArrayStruct"][name])
                new_struct["Value"] = value[i]
                try: 
                    test = int(new_struct["Name"])
                    new_struct["Name"] = str(i)
                except ValueError:
                    pass
                new_array.append(new_struct)
            value = new_array
        else:
            full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["DummyStruct"] = None
    #Patch
    full_datatable[file]["DataTable"]["Exports"][0]["Table"]["Data"][entry]["Value"][data]["Value"] = value

def convert_json(filename, content):
    #Convert json to its asset files
    name, extension = os.path.splitext(filename)
    absolute_asset_dir = os.path.abspath("UnrealPak\\Mod\\BloodstainedRotN\\" + dictionary["FileToPath"][name])
    with open("UAssetGUI\\" + name + ".json", "w", encoding="utf8") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=False))
    
    root = os.getcwd()
    os.chdir("UAssetGUI")
    os.system("cmd /c UAssetGUI.exe fromjson " + name + ".json \"" + absolute_asset_dir + "\\" + filename + "\"")
    os.chdir(root)
    
    #UAssetGUI does not throw an exception if it fails to convert something so throw one from here
    if not os.path.isfile(absolute_asset_dir + "\\" + filename):
        raise FileNotFoundError(name + ".json failed to convert")
    
    os.remove("UAssetGUI\\" + name + ".json")

def convert_asset(game_dir, filename, destination):
    #Convert an asset's files to a single json
    name, extension = os.path.splitext(filename)
    root = os.getcwd()
    os.chdir("UAssetGUI")
    os.system("cmd /c UAssetGUI.exe tojson \"" + game_dir + "\\" + dictionary["FileToPath"][name] + "\\" + filename + "\" \"" + destination + "\\" + name + ".json\" VER_UE4_27")
    os.chdir(root)

def copy_file(game_dir, filename, destination):
    #Copy all files of an asset based on its name
    for i in os.listdir(game_dir + "\\" + dictionary["FileToPath"][filename]):
        name, extension = os.path.splitext(i)
        if name == filename:
            shutil.copyfile(game_dir + "\\" + dictionary["FileToPath"][filename] + "\\" + i, destination + "\\" + i)

def convert_miriam_candle(candle, shard):
    #While candle shards have entries in DroprateMaster those are completely ignored by the game
    #Instead those are read directly from the level files so they need to be updated to reflect the new shard drops
    candle_type = datatable["PB_DT_ShardMaster"][candle]["ShardType"]
    shard_type  = datatable["PB_DT_ShardMaster"][shard]["ShardType"]
    for i in dictionary["EnemyLocation"][candle]["NormalModeRooms"]:
        filename = i + "_Gimmick"
        #Read json
        with open("UAssetGUI\\Level\\" + filename + ".json", "r", encoding="utf-8") as file_reader:
            level = json.load(file_reader)
        #Patch json
        for e in level["Exports"]:
            for o in e["Data"]:
                try:
                    if candle in o["Value"]:
                        o["Value"] = shard
                except TypeError:
                    continue
                except IndexError:
                    continue
                except KeyError:
                    continue
        for e in range(len(level["NameMap"])):
            if level["NameMap"][e] == candle:
                level["NameMap"][e] = shard
            if level["NameMap"][e] == candle_type:
                level["NameMap"][e] = shard_type
        #Convert
        convert_json(filename + ".umap", level)

def convert_bloodless_candle(bloodless_datatable):
    #All of Bloodless' abilities are stored inside of shard candles
    #Just like for Miriam those are defined inside of the level files
    tower_check = 0
    for i in bloodless_datatable:
        #RoomToFile
        filename = remove_inst(bloodless_datatable[i]) + "_Gimmick"
        #Valac's room has two candle abilities and is the only one in the game
        #Setup an exception so that this file searches for a specific ability
        if bloodless_datatable[i] == "m08TWR_019":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_BLOOD_STEAL"
        elif bloodless_datatable[i] == "m08TWR_019_2":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP"
        else:
            search = "EPBBloodlessAbilityType::"
        #Read json
        #Open the same file a second time if it is Valac's room
        if "m08TWR_019" in filename and tower_check == 1:
            with open("UAssetGUI\\" + filename + ".json", "r", encoding="utf-8") as file_reader:
                level = json.load(file_reader)
        else:
            with open("UAssetGUI\\Level\\" + filename + ".json", "r", encoding="utf-8") as file_reader:
                level = json.load(file_reader)
        #Patch json
        for e in level["Exports"]:
            for o in e["Data"]:
                try:
                    if search in o["Value"]:
                        o["Value"] = "EPBBloodlessAbilityType::" + i
                except TypeError:
                    continue
                except IndexError:
                    continue
                except KeyError:
                    continue
        for e in range(len(level["NameMap"])):
            if search in level["NameMap"][e]:
                level["NameMap"][e] = "EPBBloodlessAbilityType::" + remove_inst(i)
        #If it is Valac's room for the first time only dump the information
        if "m08TWR_019" in filename and tower_check == 0:
            with open("UAssetGUI\\" + filename + ".json", "w", encoding="utf-8") as file_writer:
                file_writer.write(json.dumps(level, ensure_ascii=False))
        #Otherwise dump and convert
        else:
            convert_json(filename + ".umap", level)
        #Update tower check if the edited file was Valac's room
        if "m08TWR_019" in filename:
            tower_check += 1

def import_texture(filename):
    #Convert DDS to game assets dynamically instead of cooking them within Unreal Editor
    absolute_texture_dir = os.path.abspath("Data\\Texture")
    absolute_asset_dir   = os.path.abspath("UnrealPak\\Mod\\BloodstainedRotN\\" + dictionary["FileToPath"][filename])
    
    root = os.getcwd()
    os.chdir("UE4 DDS Tools")
    os.system("cmd /c python\python.exe src\main.py \"" + absolute_texture_dir + "\\" + filename + ".dds\" --save_folder=\"" + absolute_asset_dir + "\" --mode=inject")
    os.chdir(root)
    
    #UE4 DDS Tools does output an error but it does not interrupt the program if a texture fails to convert so do it from here
    if not os.path.isfile(absolute_asset_dir + "\\" + filename + ".uasset"):
        raise FileNotFoundError(filename + ".dds failed to inject")

def import_music(filename):
    #Start by coppying all secondary music files to destination
    for i in os.listdir("UAssetGUI\\Other"):
        name, extension = os.path.splitext(i)
        if extension == ".awb":
            continue
        if name == filename:
            shutil.copyfile("UAssetGUI\\Other\\" + filename + ".uasset", "UnrealPak\\Mod\\BloodstainedRotN\\" + dictionary["FileToPath"][filename] + "\\" + i)
    #Append the HCA data to the AWB's header
    with open("UAssetGUI\\Other\\" + filename + ".awb", "rb") as inputfile, open("UnrealPak\\Mod\\BloodstainedRotN\\" + dictionary["FileToPath"][filename] + "\\" + filename + ".awb", "wb") as outfile:
        offset = inputfile.read().find(str.encode("HCA"))
        inputfile.seek(0)
        outfile.write(inputfile.read(offset))
        with open("Data\\Music\\" + filename + ".hca", "rb") as hca:
            outfile.write(hca.read())

def remove_level_actor(filename, search):
    #While replacing actors is a complex process removing them is as simple as changing their names to some dummy text via hex editing
    destination = "UnrealPak\\Mod\\BloodstainedRotN\\" + dictionary["FileToPath"][filename] + "\\" + filename
    for i in ["umap", "uexp"]:
        shutil.copyfile("UAssetGUI\\Other\\" + filename + "." + i, destination + "." + i)
        with open(destination + "." + i, "r+b") as file:
            for e in range(os.path.getsize(file.name)):
                file.seek(e)
                if file.read(len(search)) == str.encode(search):
                    file.seek(e)
                    for o in search:
                        file.write(str.encode("X"))

def convert_flag_to_door(door_flag, width):
    door_list = []
    for i in range(0, len(door_flag), 2):
        tile_index = door_flag[i]
        direction = door_flag[i+1]
        tile_index -= 1
        if width == 0:
            x_block = tile_index
            z_block = 0
        else:
            x_block = tile_index % width
            z_block = tile_index // width
        for direction_part in Direction:
            if (direction & direction_part.value) != 0:
                breakable = (direction & (direction_part.value << 16)) != 0
                door = Door(x_block, z_block, direction_part, breakable)
                door_list.append(door)
    return door_list

def convert_door_to_flag(door_list, width):
    door_flags_by_coords = OrderedDict()
    for door in door_list:
        coords = (door.x_block, door.z_block)
        if coords not in door_flags_by_coords:
            door_flags_by_coords[coords] = 0
            
        door_flags_by_coords[coords] |= door.direction_part.value
        if door.breakable:
            door_flags_by_coords[coords] |= (door.direction_part.value << 16)
        
    door_flag = []
    for (x, z), dir_flags in door_flags_by_coords.items():
        tile_index_in_room = z*width + x
        tile_index_in_room += 1
        door_flag += [tile_index_in_room, dir_flags]
    return door_flag

def connect_map():
    #The game map requires you to manually input a list of which rooms can be transitioned into from the current room
    #Doing this via the map editor would only add long load times upon saving a map so do it here instead
    #Fill same room field for rooms that are overlayed perfectly
    #Not sure if it serves any actual purpose in-game but it does help for the following adjacent room check
    for i in datatable["PB_DT_RoomMaster"]:
        datatable["PB_DT_RoomMaster"][i]["SameRoom"] = "None"
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            continue
        for e in datatable["PB_DT_RoomMaster"]:
            if datatable["PB_DT_RoomMaster"][e]["OutOfMap"]:
                continue
            if datatable["PB_DT_RoomMaster"][i]["OffsetX"] == datatable["PB_DT_RoomMaster"][e]["OffsetX"] and datatable["PB_DT_RoomMaster"][i]["OffsetZ"] == datatable["PB_DT_RoomMaster"][e]["OffsetZ"] and i != e:
                datatable["PB_DT_RoomMaster"][i]["SameRoom"] = e
                break
    #Fill adjacent room lists
    for i in datatable["PB_DT_RoomMaster"]:
        #Start by making sure the list is empty
        datatable["PB_DT_RoomMaster"][i]["AdjacentRoomName"] = []
        used_doors.clear()
        #If a room is unused delete all of its door flags
        if datatable["PB_DT_RoomMaster"][i]["Unused"]:
            datatable["PB_DT_RoomMaster"][i]["DoorFlag"].clear()
            continue
        door_1 = convert_flag_to_door(datatable["PB_DT_RoomMaster"][i]["DoorFlag"], datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"])
        for e in datatable["PB_DT_RoomMaster"]:
            #Skip if rooms are not within the same map "layer" or if a room is unused
            if datatable["PB_DT_RoomMaster"][i]["OutOfMap"] != datatable["PB_DT_RoomMaster"][e]["OutOfMap"] or datatable["PB_DT_RoomMaster"][e]["Unused"]:
                continue
            #Transition rooms in Bloodstained come by pair, each belonging to an area
            #Make it so that an area is only connected to its corresponding transition rooms when possible
            #This avoids having the next area name tag show up within the transition
            #With the exception of standalone transitions with no fallbacks as well as the first entrance transition fallback
            if datatable["PB_DT_RoomMaster"][e]["RoomType"] == "ERoomType::Load" and e[0:6] != i[0:6] and datatable["PB_DT_RoomMaster"][e]["SameRoom"] != "None" and e != "m02VIL_1200" and datatable["PB_DT_RoomMaster"][e]["SameRoom"] != "m03ENT_1200":
                continue
            #The first entrance transition room is hardcoded to bring you back to the village regardless of its position on the canvas
            #Ignore that room and don't connect it to anything
            #Meanwhile the village version of that transition is always needed to trigger the curved effect of the following bridge room
            #So ignore any other transitions overlayed on top of it
            if datatable["PB_DT_RoomMaster"][e]["SameRoom"] == "m02VIL_1200" or e == "m03ENT_1200":
                continue
            door_2 = convert_flag_to_door(datatable["PB_DT_RoomMaster"][e]["DoorFlag"], datatable["PB_DT_RoomMaster"][e]["AreaWidthSize"])
            #Check relative position and distance on every side of the room
            check = False
            if left_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
                if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
                    check = True
                else:
                    check = door_vertical_check(door_1, door_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP, datatable["PB_DT_RoomMaster"][i]["OffsetZ"], datatable["PB_DT_RoomMaster"][e]["OffsetZ"])
            elif bottom_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
                if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
                    check = True
                else:
                    check = door_horizontal_check(door_1, door_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT, datatable["PB_DT_RoomMaster"][i]["OffsetX"], datatable["PB_DT_RoomMaster"][e]["OffsetX"])
            elif right_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
                if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
                    check = True
                else:
                    check = door_vertical_check(door_1, door_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP, datatable["PB_DT_RoomMaster"][i]["OffsetZ"], datatable["PB_DT_RoomMaster"][e]["OffsetZ"])
            elif top_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
                if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
                    check = True
                else:
                    check = door_horizontal_check(door_1, door_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT, datatable["PB_DT_RoomMaster"][i]["OffsetX"], datatable["PB_DT_RoomMaster"][e]["OffsetX"])
            if check:
                datatable["PB_DT_RoomMaster"][i]["AdjacentRoomName"].append(e)
        #If a room transition leads nowhere remove its door flag to make it obvious that it is unused
        for e in list(door_1):
            if not e in used_doors:
                door_1.remove(e)
        datatable["PB_DT_RoomMaster"][i]["DoorFlag"] = convert_door_to_flag(door_1, datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"])
    #Some rooms need specific setups
    #Vepar's room should not be permanently connected to village
    if "m02VIL_001" in datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"].remove("m02VIL_001")
    if "m01SIP_022" in datatable["PB_DT_RoomMaster"]["m02VIL_001"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m02VIL_001"]["AdjacentRoomName"].remove("m01SIP_022")
    if not "m02VIL_000" in datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m01SIP_022"]["AdjacentRoomName"].append("m02VIL_000")
    #Some tower rooms are overlayed and need to be connected manually as the above script ignores all overlayed rooms
    if not "m08TWR_017" in datatable["PB_DT_RoomMaster"]["m08TWR_000"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_000"]["AdjacentRoomName"].append("m08TWR_017")
    if not "m08TWR_018" in datatable["PB_DT_RoomMaster"]["m08TWR_005"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_005"]["AdjacentRoomName"].append("m08TWR_018")
    if not "m08TWR_018" in datatable["PB_DT_RoomMaster"]["m08TWR_006"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_006"]["AdjacentRoomName"].append("m08TWR_018")
    if not "m08TWR_019" in datatable["PB_DT_RoomMaster"]["m08TWR_016"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_016"]["AdjacentRoomName"].append("m08TWR_019")
    
    if not "m08TWR_000" in datatable["PB_DT_RoomMaster"]["m08TWR_017"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_017"]["AdjacentRoomName"].append("m08TWR_000")
    if not "m08TWR_005" in datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"].append("m08TWR_005")
    if not "m08TWR_006" in datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_018"]["AdjacentRoomName"].append("m08TWR_006")
    if not "m08TWR_016" in datatable["PB_DT_RoomMaster"]["m08TWR_019"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m08TWR_019"]["AdjacentRoomName"].append("m08TWR_016")
    
    datatable["PB_DT_RoomMaster"]["m08TWR_000"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_000"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_005"]["DoorFlag"].append(4)
    datatable["PB_DT_RoomMaster"]["m08TWR_005"]["DoorFlag"].append(4)
    datatable["PB_DT_RoomMaster"]["m08TWR_006"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_006"]["DoorFlag"].insert(0, 1)
    datatable["PB_DT_RoomMaster"]["m08TWR_016"]["DoorFlag"].insert(0, 4)
    datatable["PB_DT_RoomMaster"]["m08TWR_016"]["DoorFlag"].insert(0, 2)
    
    datatable["PB_DT_RoomMaster"]["m08TWR_017"]["DoorFlag"].append(18)
    datatable["PB_DT_RoomMaster"]["m08TWR_017"]["DoorFlag"].append(8)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(3)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(2)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(34)
    datatable["PB_DT_RoomMaster"]["m08TWR_018"]["DoorFlag"].append(8)
    datatable["PB_DT_RoomMaster"]["m08TWR_019"]["DoorFlag"].append(39)
    datatable["PB_DT_RoomMaster"]["m08TWR_019"]["DoorFlag"].append(8)
    #Fix bad ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m06KNG_020"]["AdjacentRoomName"].append("m02VIL_099")
    #Fix good ending cutscene not transitioning to the village
    if not "m02VIL_099" in datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"]:
        datatable["PB_DT_RoomMaster"]["m18ICE_019"]["AdjacentRoomName"].append("m02VIL_099")
    #Give the unused Glacial Tomb room the same doors as Dominique's room
    #Otherwise that room hides the doors of the used one
    datatable["PB_DT_RoomMaster"]["m18ICE_020"]["DoorFlag"] = [2, 4]

def left_check(i, e):
    return bool(e["OffsetX"] == round(i["OffsetX"] - 12.6 * e["AreaWidthSize"], 1) and round(i["OffsetZ"] - 7.2 * (e["AreaHeightSize"] - 1), 1) <= e["OffsetZ"] <= round(i["OffsetZ"] + 7.2 * (i["AreaHeightSize"] - 1), 1))

def bottom_check(i, e):
    return bool(round(i["OffsetX"] - 12.6 * (e["AreaWidthSize"] - 1), 1) <= e["OffsetX"] <= round(i["OffsetX"] + 12.6 * (i["AreaWidthSize"] - 1), 1) and e["OffsetZ"] == round(i["OffsetZ"] - 7.2 * e["AreaHeightSize"], 1))

def right_check(i, e):
    return bool(e["OffsetX"] == round(i["OffsetX"] + 12.6 * i["AreaWidthSize"], 1) and round(i["OffsetZ"] - 7.2 * (e["AreaHeightSize"] - 1), 1) <= e["OffsetZ"] <= round(i["OffsetZ"] + 7.2 * (i["AreaHeightSize"] - 1), 1))

def top_check(i, e):
    return bool(round(i["OffsetX"] - 12.6 * (e["AreaWidthSize"] - 1), 1) <= e["OffsetX"] <= round(i["OffsetX"] + 12.6 * (i["AreaWidthSize"] - 1), 1) and e["OffsetZ"] == round(i["OffsetZ"] + 7.2 * i["AreaHeightSize"], 1))

def door_vertical_check(door_1, door_2, direction_1, direction_2, direction_3, offset_1, offset_2):
    check = False
    for i in door_1:
        if i.direction_part == direction_1:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_1] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_2:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_2] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_3:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_3] and i.z_block == (e.z_block + round((offset_2 - offset_1)/7.2)):
                    used_doors.append(i)
                    check = True
    return check

def door_horizontal_check(door_1, door_2, direction_1, direction_2, direction_3, offset_1, offset_2):
    check = False
    for i in door_1:
        if i.direction_part == direction_1:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_1] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_2:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_2] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
        elif i.direction_part == direction_3:
            for e in door_2:
                if e.direction_part == OppositeDirection[direction_3] and i.x_block == (e.x_block + round((offset_2 - offset_1)/12.6)):
                    used_doors.append(i)
                    check = True
    return check

def is_enemy(character):
    #Check if input entry is an enemy and what type
    dict = {
        "Enemy":     False,
        "Boss":      False,
        "Main":      False,
        "Exception": False
    }
    if character in dictionary["EnemyLocation"]:
        dict["Enemy"] = True
        dict["Main"]  = True
    elif character[0:5] in dictionary["EnemyLocation"]:
        dict["Enemy"] = True
    elif character[0:5] == "N1013" or character[0:5] == "N1009" or character == "N3125":
        dict["Enemy"]     = True
        dict["Exception"] = True
    if datatable["PB_DT_CharacterParameterMaster"][character]["IsBoss"] and character != "N2008_BOSS":
        dict["Boss"] = True
    return dict

def remove_inst(name):
    #Return input without its instance number
    try:
        inst = int(name[-1])
        if name[-2] == "_":
            name = name[:-2]
    except ValueError:
        pass
    except IndexError:
        pass
    return name

def random_weighted(value, minimum, maximum, step, deviation):
    #Randomly choose from a range with higher odds around a specific value
    list = []
    for i in range(minimum, maximum+1):
        if i % step == 0:
            for e in range(2**(abs(math.ceil(abs(i-value)*deviation/max(value-minimum, maximum-value))-deviation))):
                list.append(i)
    return random.choice(list)

def append_string_entry(file, entry, text):
    #Make sure the text never exceeds two lines
    if "\r\n" in stringtable[file][entry] or len(stringtable[file][entry]) > 60 or entry == "ITEM_EXPLAIN_RolledOmelette":
        prefix = " "
    else:
        prefix = "\r\n"
    stringtable[file][entry] += prefix + text