import os
import clr
import shutil
import json
import math
import glob
import random
import struct
import sys
import colorsys
import copy
import filecmp
from enum import Enum
from collections import OrderedDict

#Open file information
with open("Data\\FileToPath.json", "r", encoding="utf8") as file_reader:
    file_to_path = json.load(file_reader)
file_to_type = {}
for i in file_to_path:
    if "DataTable" in file_to_path[i]:
        file_to_type[i] = "DataTable"
    elif "Level" in file_to_path[i]:
        file_to_type[i] = "Level"
    elif "StringTable" in file_to_path[i]:
        file_to_type[i] = "StringTable"
    elif "Material" in file_to_path[i]:
        file_to_type[i] = "Material"
    elif "Texture" in file_to_path[i] or "UI" in file_to_path[i] and not "StartupSelecter" in file_to_path[i]:
        file_to_type[i] = "Texture"
    elif "Sound" in file_to_path[i]:
        file_to_type[i] = "Sound"
    else:
        file_to_type[i] = "Blueprint"
load_types = ["DataTable", "Level", "StringTable", "Blueprint", "Material"]
simplify_types = ["DataTable", "StringTable"]

mod_dir = "Tools\\UnrealPak\\Mod\\BloodstainedRotN\\Content"
asset_dir = "Game"

#Open UAssetAPI module
sys.path.append(os.path.abspath("Tools\\UAssetAPI"))
clr.AddReference("UAssetAPI")

from UAssetAPI import *
from UAssetAPI.FieldTypes import *
from UAssetAPI.JSON import *
from UAssetAPI.Kismet import *
from UAssetAPI.Kismet.Bytecode import *
from UAssetAPI.Kismet.Bytecode.Expressions import *
from UAssetAPI.PropertyTypes import *
from UAssetAPI.PropertyTypes.Objects import *
from UAssetAPI.PropertyTypes.Structs import *
from UAssetAPI.PropertyTypes.Structs.Movies import *
from UAssetAPI.UnrealTypes import *
from UAssetAPI.Unversioned import *

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
    global datatable
    datatable = {}
    global original_datatable
    original_datatable = {}
    global stringtable
    stringtable = {}
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

def load_game_data():
    global game_data
    game_data = {}
    global data_struct
    data_struct = {}
    for i in file_to_type:
        if file_to_type[i] in load_types:
            #Load all game data in one dict
            if file_to_type[i] == "Level":
                extension = ".umap"
            else:
                extension = ".uasset"
            game_data[i] = UAsset(asset_dir + "\\" + file_to_path[i] + "\\" + i + extension, UE4Version(517))
            #Store extra data for convenience
            if file_to_type[i] == "DataTable":
                for e in game_data[i].Exports[0].Table.Data:
                    for o in e.Value:
                        if str(o.PropertyType) == "ArrayProperty":
                            if str(o.ArrayType) == "StructProperty":
                                for u in o.Value:
                                    data_struct[str(u.Name)] = u
    
def load_mod_data():
    global mod_data
    mod_data = {}
    for i in os.listdir("Data\\Dictionary"):
        name, extension = os.path.splitext(i)
        with open("Data\\Dictionary\\" + i, "r", encoding="utf8") as file_reader:
            mod_data[name] = json.load(file_reader)

def load_map(path):
    #Load map related files
    if not path:
        path = "MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json"
    with open(path, "r", encoding="utf8") as file_reader:
        json_file = json.load(file_reader)
    if "PB_DT_RoomMaster" in datatable:
        for i in json_file["MapData"]:
            for e in json_file["MapData"][i]:
                datatable["PB_DT_RoomMaster"][i][e] = json_file["MapData"][i][e]
    else:
        datatable["PB_DT_RoomMaster"] = json_file["MapData"]
    mod_data["MapLogic"] = json_file["KeyLogic"]
    mod_data["BloodlessModeMapLogic"] = copy.deepcopy(mod_data["MapLogic"])
    mod_data["MapOrder"] = json_file["AreaOrder"]
    mod_data["OriginalMapOrder"] = [
      "m01SIP",
      "m02VIL",
      "m03ENT",
      "m04GDN",
      "m05SAN",
      "m08TWR",
      "m07LIB",
      "m09TRN",
      "m13ARC",
      "m06KNG",
      "m11UGD",
      "m12SND",
      "m14TAR",
      "m17RVA",
      "m15JPN",
      "m10BIG",
      "m18ICE"
    ]
    mod_data["BloodlessModeMapOrder"] = ["m05SAN"]
    mod_data["BloodlessModeOriginalMapOrder"] = [
      "m05SAN",
      "m03ENT",
      "m02VIL",
      "m01SIP",
      "m04GDN",
      "m08TWR",
      "m07LIB",
      "m09TRN",
      "m13ARC",
      "m06KNG",
      "m11UGD",
      "m12SND",
      "m14TAR",
      "m17RVA",
      "m15JPN",
      "m10BIG",
      "m18ICE"
    ]

def fix_custom_map():
    #The two underground rooms with very specific shapes only display properly based on their Y position below the origin
    #Start by resetting their no traverse list as if they were above 0
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_013"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_013"]["AreaWidthSize"]*2
    for i in range(len(datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"])):
        datatable["PB_DT_RoomMaster"]["m11UGD_031"]["NoTraverse"][i] += datatable["PB_DT_RoomMaster"]["m11UGD_031"]["AreaWidthSize"]*3
    #Then shift those lists if the rooms are below 0
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
    #The uasset data is inconvenient to access and would take up too much text space in the code
    #Convert them to a simplified dictionary that is similar to Serializer's outputs
    for i in file_to_type:
        if file_to_type[i] in simplify_types:
            if file_to_type[i] == "DataTable":
                datatable[i] = {}
                for e in game_data[i].Exports[0].Table.Data:
                    datatable[i][str(e.Name)] = {}
                    for o in e.Value:
                        datatable[i][str(e.Name)][str(o.Name)] = read_datatable(o)
                original_datatable[i] = copy.deepcopy(datatable[i])
            elif file_to_type[i] == "StringTable":
                stringtable[i] = {}
                for e in game_data[i].Exports[0].Table:
                    stringtable[i][str(e.Key)] = str(e.Value)

def simple_to_complex():
    #Convert the simplified datatables back to their complex versions
    for i in file_to_type:
        if file_to_type[i] in simplify_types:
            if file_to_type[i] == "DataTable":
                ecount = 0
                for e in datatable[i]:
                    ocount = 0
                    #If the datatables had entries added then add an entry slot in the uasset too
                    if ecount >= game_data[i].Exports[0].Table.Data.Count:
                        append_datatable_entry(i, e)
                    for o in datatable[i][e]:
                        #The unused field in room master is only used by the mod, not by the game
                        if i == "PB_DT_RoomMaster" and o == "Unused":
                            ocount += 1
                            continue
                        #Only patch the value if it is different from the original, saves a lot of load time
                        if e in original_datatable[i]:
                            if datatable[i][e][o] == original_datatable[i][e][o]:
                                ocount += 1
                                continue
                        patch_datatable(i, ecount, ocount, datatable[i][e][o])
                        ocount += 1
                    ecount += 1
            elif file_to_type[i] == "StringTable":
                game_data[i].Exports[0].Table.Clear()
                for e in stringtable[i]:
                    game_data[i].Exports[0].Table.Add(FString(e), FString(stringtable[i][e]))

def read_datatable(struct):
    #Read a uasset variable as a python variable
    type = str(struct.PropertyType)
    if type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        value = []
        for i in struct.Value:
            if sub_type == "ByteProperty":
                sub_value = str(i.EnumValue)
            elif sub_type == "FloatProperty":
                sub_value = round(i.Value, 3)
            elif sub_type in ["EnumProperty", "NameProperty", "SoftObjectProperty", "StrProperty", "TextProperty"] and struct.Value:
                sub_value = str(i.Value)
            elif sub_type == "StructProperty":
                sub_value = {}
                for e in i.Value:
                    sub_sub_type = str(e.PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_sub_value = str(e.EnumValue)
                    elif sub_sub_type == "FloatProperty":
                        sub_sub_value = round(e.Value, 3)
                    elif sub_sub_type in ["EnumProperty", "NameProperty", "StrProperty"]:
                        sub_sub_value = str(e.Value)
                    else:
                        sub_sub_value = e.Value
                    sub_value[str(e.Name)] = sub_sub_value
            else:
                sub_value = i.Value
            value.append(sub_value)
    elif type == "ByteProperty":
        value = str(struct.EnumValue)
    elif type == "FloatProperty":
        value = round(struct.Value, 3)
    elif type in ["EnumProperty", "NameProperty", "SoftObjectProperty", "StrProperty", "TextProperty"] and struct.Value:
        value = str(struct.Value)
    else:
        value = struct.Value
    return value

def patch_datatable(file, entry, data, value):
    #Patch a python variable over a uasset's variable
    struct = game_data[file].Exports[0].Table.Data[entry].Value[data]
    type = str(struct.PropertyType)
    if type == "ArrayProperty":
        sub_type = str(struct.ArrayType)
        new_list = []
        for i in value:
            if sub_type == "BoolProperty":
                sub_struct = BoolPropertyData()
                sub_struct.Value = i
            elif sub_type == "ByteProperty":
                sub_struct = BytePropertyData()
                sub_struct.ByteType = BytePropertyType.FName
                sub_struct.EnumValue = FName(game_data[file], split_fname(i)[0], split_fname(i)[1] + 1)
            elif sub_type == "EnumProperty":
                sub_struct = EnumPropertyData()
                sub_struct.Value = FName(game_data[file], split_fname(i)[0], split_fname(i)[1] + 1)
            elif sub_type == "FloatProperty":
                sub_struct = FloatPropertyData()
                sub_struct.Value = i
            elif sub_type == "IntProperty":
                sub_struct = IntPropertyData()
                sub_struct.Value = i
            elif sub_type == "NameProperty":
                sub_struct = NamePropertyData()
                sub_struct.Value = FName(game_data[file], split_fname(i)[0], split_fname(i)[1] + 1)
            elif sub_type == "SoftObjectProperty":
                sub_struct = SoftObjectPropertyData()
                sub_struct.Value = FName(game_data[file], split_fname(i)[0], split_fname(i)[1] + 1)
            elif sub_type == "StrProperty":
                sub_struct = StrPropertyData()
                sub_struct.Value = FString(i)
            elif sub_type == "StructProperty":
                sub_struct = data_struct[str(struct.Name)].Clone()
                count = 0
                for e in i:
                    sub_sub_type = str(sub_struct.Value[count].PropertyType)
                    if sub_sub_type == "ByteProperty":
                        sub_struct.Value[count].EnumValue = FName(game_data[file], split_fname(i[e])[0], split_fname(i[e])[1] + 1)
                    elif sub_sub_type in ["NameProperty", "EnumProperty"]:
                        sub_struct.Value[count].Value = FName(game_data[file], split_fname(i[e])[0], split_fname(i[e])[1] + 1)
                    elif sub_sub_type == "StrProperty":
                        sub_struct.Value[count].Value = FString(i[e])
                    else:
                        sub_struct.Value[count].Value = i[e]
                    count += 1
            elif sub_type == "TextProperty":
                sub_struct = TextPropertyData()
                sub_struct.Value = FString(i)
            new_list.append(sub_struct)
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = new_list
    elif type == "ByteProperty":
        game_data[file].Exports[0].Table.Data[entry].Value[data].EnumValue = FName(game_data[file], split_fname(value)[0], split_fname(value)[1] + 1)
    elif type in ["EnumProperty", "NameProperty", "SoftObjectProperty"]:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FName(game_data[file], split_fname(value)[0], split_fname(value)[1] + 1)
    elif type in ["StrProperty", "TextProperty"] and value:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = FString(value)
    else:
        game_data[file].Exports[0].Table.Data[entry].Value[data].Value = value

def append_datatable_entry(file, entry):
    #Append a new datatable entry to the end to be edited later on
    new_entry = game_data[file].Exports[0].Table.Data[0].Clone()
    new_entry.Name = FName(game_data[file], split_fname(entry)[0], split_fname(entry)[1] + 1)
    game_data[file].Exports[0].Table.Data.Add(new_entry)

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
    #Apply manual tweaks defined in the json
    for i in mod_data["DefaultTweak"]:
        for e in mod_data["DefaultTweak"][i]:
            for o in mod_data["DefaultTweak"][i][e]:
                datatable[i][e][o] = mod_data["DefaultTweak"][i][e][o]
    #Loop through all enemies
    for i in datatable["PB_DT_CharacterParameterMaster"]:
        if not is_enemy(i)["Enemy"]:
            continue
        if is_enemy(i)["Boss"]:
            #Make boss health scale with level
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]*(99/datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]))
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"] = round(datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]/5)*5
            datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP99Enemy"] = datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]
            #Expand expertise point range that scales with level
            #In vanilla the range is too small and barely makes a difference
            if datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 15
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
            #Set stone type
            #Some regular enemies are originally set to the boss stone type which doesn't work well when petrified
            datatable["PB_DT_CharacterParameterMaster"][i]["StoneType"] = "EPBStoneType::Boss"
        else:
            if datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] > 0:
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience99Enemy"] = 10
                datatable["PB_DT_CharacterParameterMaster"][i]["ArtsExperience"]        = 1
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
        if datatable["PB_DT_CharacterParameterMaster"][i]["LUC"] == 0 and i != "N1008":
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
            datatable["PB_DT_DropRateMaster"][i]["ShardRate"] = mod_data["ShardDrop"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["RareItemRate"] = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["CommonRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["CommonRate"] = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["RareIngredientRate"] = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
        if 0.0 < datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] < 100.0:
            datatable["PB_DT_DropRateMaster"][i]["CommonIngredientRate"] = mod_data["EnemyDrop"]["EnemyMat"]["ItemRate"]*drop_rate_multiplier
    #Loop through all items
    for i in datatable["PB_DT_ItemMaster"]:
        #Remove dishes from shop to prevent heal spam
        #In vanilla you can easily stock up on an infinite amount of them which breaks the game completely
        #This change also makes regular potions more viable now
        if i in mod_data["ItemDrop"]["Dish"]["ItemPool"]:
            datatable["PB_DT_ItemMaster"][i]["max"]       = 1
            datatable["PB_DT_ItemMaster"][i]["buyPrice"]  = 0
            datatable["PB_DT_ItemMaster"][i]["sellPrice"] = 0
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
    stringtable["PBMasterStringTable"]["ENEMY_NAME_N1011_STRONG"] = mod_data["EnemyTranslation"]["N1011_STRONG"]
    #Update Jinrai cost description
    stringtable["PBMasterStringTable"]["ARTS_TXT_017_00"] += str(datatable["PB_DT_ArtsCommandMaster"]["JSword_GodSpeed1"]["CostMP"])
    #Add Breeder and Greedling to the enemy archives
    add_enemy_to_archive("N3125", ["SYS_SEN_AreaName021"], None, "N3124")
    add_enemy_to_archive("N2016", ["SYS_SEN_AreaName021"], None, "N2015")
    #Rebalance boss rush mode a bit
    #Remove all consumables from inventory
    for i in game_data["PBExtraModeInfo_BP"].Exports[1].Data[7].Value:
        i.Value[1].Value = 0
    #Start both stages at level 50
    for i in range(8, 14):
        game_data["PBExtraModeInfo_BP"].Exports[1].Data[i].Value = 50
    #Give all bosses level 66
    for i in game_data["PBExtraModeInfo_BP"].Exports[1].Data[14].Value:
        i.Value.Value = 66
    #Starting equipment test
    #sub_struct = NamePropertyData()
    #sub_struct.Name = FName(game_data["PBExtraModeInfo_BP"], "EffectiveShard")
    #sub_struct.Value = FName(game_data["PBExtraModeInfo_BP"], "Accelerator")
    #game_data["PBExtraModeInfo_BP"].Exports[1].Data[0].Value.Add(sub_struct)

def search_and_replace_string(filename, entry_keyword, data, old_value, new_value):
    #Search for a specific piece of data to change in a level file and swap it
    for i in game_data[filename].Exports:
        if entry_keyword in str(i.ObjectName):
            for e in i.Data:
                if str(e.Name) == data and str(e.Value) == old_value:
                    e.Value = FName(game_data[filename], split_fname(new_value)[0], split_fname(new_value)[1] + 1)

def update_descriptions():
    #Add magical stats to descriptions
    for i in datatable["PB_DT_ArmorMaster"]:
        if not "ITEM_EXPLAIN_" + i in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_ArmorMaster"][i]["MagicAttack"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff8000\">mATK " + str(datatable["PB_DT_ArmorMaster"][i]["MagicAttack"]) + "</>")
        if datatable["PB_DT_ArmorMaster"][i]["MagicDefense"] != 0:
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#ff00ff\">mDEF " + str(datatable["PB_DT_ArmorMaster"][i]["MagicDefense"]) + "</>")
    #Add restoration amount to descriptions
    for i in datatable["PB_DT_SpecialEffectDefinitionMaster"]:
        if not "ITEM_EXPLAIN_" + i in stringtable["PBMasterStringTable"]:
            continue
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeHP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00ff00\">HP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
        if datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Type"] == "EPBSpecialEffect::ChangeMP":
            append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_" + i, "<span color=\"#00bfff\">MP " + str(int(datatable["PB_DT_SpecialEffectDefinitionMaster"][i]["Parameter01"])) + "</>")
    #Add Shovel Armor's attack stat to its description
    append_string_entry("PBMasterStringTable", "ITEM_EXPLAIN_Shovelarmorsarmor", "<span color=\"#ff0000\">wATK " + str(int(datatable["PB_DT_CoordinateParameter"]["ShovelArmorWeaponAtk"]["Value"])) + "</>")

def remove_difficulties(current):
    new_list = []
    sub_struct = BytePropertyData()
    sub_struct.ByteType = BytePropertyType.FName
    sub_struct.EnumValue = FName(game_data["DifficultSelecter"], "EPBGameLevel::" + current)
    new_list = [sub_struct]
    game_data["DifficultSelecter"].Exports[2].Data[1].Value = new_list

def default_nightmare_cheatcode():
    game_data["EntryNameSetter"].Exports[110].Data[0].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[110].Data[1].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[111].Data[2].CultureInvariantString = FString("NIGHTMARE")
    game_data["EntryNameSetter"].Exports[111].Data[3].CultureInvariantString = FString("NIGHTMARE")

def write_log(filename, log):
    with open("SpoilerLog\\" + filename + ".json", "w", encoding="utf8") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def write_files():
    #Dump all uasset objects to files
    for i in file_to_type:
        if file_to_type[i] in load_types:
            if file_to_type[i] == "Level":
                extension = ".umap"
            else:
                extension = ".uasset"
            game_data[i].Write(mod_dir + "\\" + file_to_path[i] + "\\" + i + extension)

def remove_unchanged():
    #Since uasset objects cannot be compared successfully we need to compare the files after they've been written
    #That way unchanged files get removed from the pak
    for i in file_to_path:
        remove = True
        for e in os.listdir(mod_dir + "\\" + file_to_path[i]):
            name, extension = os.path.splitext(e)
            if name == i:
                if not filecmp.cmp(mod_dir + "\\" + file_to_path[i] + "\\" + e, asset_dir + "\\" + file_to_path[i] + "\\" + e, shallow=False):
                    remove = False
        if remove:
            for e in os.listdir(mod_dir + "\\" + file_to_path[i]):
                name, extension = os.path.splitext(e)
                if name == i:
                    os.remove(mod_dir + "\\" + file_to_path[i] + "\\" + e)

def import_texture(filename):
    #Convert DDS to game assets dynamically instead of cooking them within Unreal Editor
    absolute_asset_dir   = os.path.abspath(asset_dir + "\\" + file_to_path[filename])
    absolute_texture_dir = os.path.abspath("Data\\Texture")
    absolute_mod_dir     = os.path.abspath(mod_dir + "\\" + file_to_path[filename])
    
    root = os.getcwd()
    os.chdir("Tools\\UE4 DDS Tools")
    os.system("cmd /c python\python.exe src\main.py \"" + absolute_asset_dir  + "\\" + filename + ".uasset\" \"" + absolute_texture_dir + "\\" + filename + ".dds\" --save_folder=\"" + absolute_mod_dir + "\" --mode=inject --version=4.22")
    os.chdir(root)
    
    #UE4 DDS Tools does output an error but it does not interrupt the program if a texture fails to convert so do it from here
    if not os.path.isfile(absolute_mod_dir + "\\" + filename + ".uasset"):
        raise FileNotFoundError(filename + ".dds failed to inject")

def import_music(filename):
    #Start by coppying all secondary music files to destination
    for i in os.listdir(asset_dir + "\\" + file_to_path[filename]):
        name, extension = os.path.splitext(i)
        if extension == ".awb":
            continue
        if name == filename:
            shutil.copyfile(asset_dir + "\\" + file_to_path[filename] + "\\" + i, mod_dir + "\\" + file_to_path[filename] + "\\" + i)
    #Append the HCA data to the AWB's header
    with open(asset_dir + "\\" + file_to_path[filename] + "\\" + filename + ".awb", "rb") as inputfile, open(mod_dir + "\\" + file_to_path[filename] + "\\" + filename + ".awb", "wb") as outfile:
        offset = inputfile.read().find(str.encode("HCA"))
        inputfile.seek(0)
        outfile.write(inputfile.read(offset))
        with open("Data\\Music\\" + filename + ".hca", "rb") as hca:
            outfile.write(hca.read())

def remove_level_actor(filename, actors):
    #While replacing actors is a complex process removing them only requires a few edits
    if file_to_type[filename] != "Level":
        raise "Input is not a level file"
    remove = []
    count = 0
    for i in game_data[filename].Exports:
        count += 1
        if str(i.ObjectName) in actors:
            i.OuterIndex = FPackageIndex(0)
            remove.append(count)
    for i in game_data[filename].Exports:
        if str(i.ObjectName) == "PersistentLevel":
            for e in remove:
                i.IndexData.Remove(e)

def change_material_hsv(filename, parameter, new_hsv):
    #Change a vector color in a material file
    #Here we use hsv as a base as it is easier to work with
    if file_to_type[filename] != "Material":
        raise "Input is not a material file"
    rgb = []
    for i in game_data[filename].Exports[0].Data:
        if str(i.Name) == "VectorParameterValues":
            for e in i.Value:
                if str(e.Value[0].Value[0].Value) == parameter:
                    rgb.append(e.Value[1].Value[0].Value.R)
                    rgb.append(e.Value[1].Value[0].Value.G)
                    rgb.append(e.Value[1].Value[0].Value.B)
                    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                    if new_hsv[0] < 0:
                        new_hue = hsv[0]
                    else:
                        new_hue = new_hsv[0]/360
                    if new_hsv[1] < 0:
                        new_sat = hsv[1]
                    else:
                        new_sat = new_hsv[1]/100
                    if new_hsv[2] < 0:
                        new_val = hsv[2]
                    else:
                        new_val = new_hsv[2]/100
                    rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
                    e.Value[1].Value[0].Value.R = rgb[0]
                    e.Value[1].Value[0].Value.G = rgb[1]
                    e.Value[1].Value[0].Value.B = rgb[2]

def convert_flag_to_door(door_flag, width):
    #Function by LagoLunatic
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
    #Function by LagoLunatic
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

def convert_door_to_adjacent_room(room, door_flag):
    adjacent = [room]
    door_1 = convert_flag_to_door(door_flag, datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"])
    for i in datatable["PB_DT_RoomMaster"]:
        door_2 = convert_flag_to_door(datatable["PB_DT_RoomMaster"][i]["DoorFlag"], datatable["PB_DT_RoomMaster"][i]["AreaWidthSize"])
        if is_adjacent(room, i, door_1, door_2):
            adjacent.append(i)
    return adjacent

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
            if datatable["PB_DT_RoomMaster"][e]["RoomType"] == "ERoomType::Load" and e[0:6] != i[0:6] and datatable["PB_DT_RoomMaster"][e]["SameRoom"] != "None" and e != "m02VIL(1200)" and datatable["PB_DT_RoomMaster"][e]["SameRoom"] != "m03ENT(1200)":
                continue
            #The first entrance transition room is hardcoded to bring you back to the village regardless of its position on the canvas
            #Ignore that room and don't connect it to anything
            #Meanwhile the village version of that transition is always needed to trigger the curved effect of the following bridge room
            #So ignore any other transitions overlayed on top of it
            if datatable["PB_DT_RoomMaster"][e]["SameRoom"] == "m02VIL(1200)" or e == "m03ENT(1200)":
                continue
            #Check relative position and distance on every side of the room
            door_2 = convert_flag_to_door(datatable["PB_DT_RoomMaster"][e]["DoorFlag"], datatable["PB_DT_RoomMaster"][e]["AreaWidthSize"])
            if is_adjacent(i, e, door_1, door_2):
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

def is_adjacent(i, e, door_1, door_2):
    if left_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            return True
        else:
            return door_vertical_check(door_1, door_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP, datatable["PB_DT_RoomMaster"][i]["OffsetZ"], datatable["PB_DT_RoomMaster"][e]["OffsetZ"])
    elif bottom_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            return True
        else:
            return door_horizontal_check(door_1, door_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT, datatable["PB_DT_RoomMaster"][i]["OffsetX"], datatable["PB_DT_RoomMaster"][e]["OffsetX"])
    elif right_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            return True
        else:
            return door_vertical_check(door_1, door_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP, datatable["PB_DT_RoomMaster"][i]["OffsetZ"], datatable["PB_DT_RoomMaster"][e]["OffsetZ"])
    elif top_check(datatable["PB_DT_RoomMaster"][i], datatable["PB_DT_RoomMaster"][e]):
        if datatable["PB_DT_RoomMaster"][i]["OutOfMap"]:
            return True
        else:
            return door_horizontal_check(door_1, door_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT, datatable["PB_DT_RoomMaster"][i]["OffsetX"], datatable["PB_DT_RoomMaster"][e]["OffsetX"])

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
    if character in mod_data["EnemyLocation"]:
        dict["Enemy"] = True
        dict["Main"]  = True
    elif character[0:5] in mod_data["EnemyLocation"] and character != "N1001_Sip":
        dict["Enemy"] = True
    elif character[0:5] == "N1013" or character[0:5] == "N1009" or character == "N3125":
        dict["Enemy"]     = True
        dict["Exception"] = True
    if datatable["PB_DT_CharacterParameterMaster"][character]["IsBoss"] and character != "N2008_BOSS":
        dict["Boss"] = True
    return dict

def split_fname(name):
    #Return input without its instance number
    stripped_name = name.replace(")", "").split("(")
    if len(stripped_name) == 1:
        return (stripped_name[0], -1)
    else:
        return (stripped_name[0], int(stripped_name[1]))

def create_weighted_list(value, minimum, maximum, step, deviation):
    #Create a list in a range with higher odds around a specific value
    list = []
    for i in [(minimum, value + 1), (value, maximum + 1)]:
        sublist = []
        distance = abs(i[0]-i[1])
        new_deviation = round(deviation*(distance/(maximum-minimum)))*2
        for e in range(i[0], i[1]):
            if e % step == 0:
                difference = abs(e-value)
                for o in range(2**(abs(math.ceil(difference*new_deviation/distance)-new_deviation))):
                    sublist.append(e)
        list.append(sublist)
    return list

def random_weighted(value, minimum, maximum, step, deviation):
    return random.choice(random.choice(create_weighted_list(value, minimum, maximum, step, deviation)))

def add_enemy_to_archive(enemy_id, area_ids, package_path, copy_from):
    last_id = split_fname(list(datatable["PB_DT_ArchiveEnemyMaster"])[-1])[1]
    entry_id = "Enemy(" + "{:03d}".format(last_id + 1) + ")"
    for i in datatable["PB_DT_ArchiveEnemyMaster"]:
        if datatable["PB_DT_ArchiveEnemyMaster"][i]["UniqueID"] == copy_from:
            new_entry = copy.deepcopy(datatable["PB_DT_ArchiveEnemyMaster"][i])
            break
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id] = new_entry
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["UniqueID"] = enemy_id
    for i in range(len(area_ids)):
        datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["Area" + str(i + 1)] = area_ids[i]
    datatable["PB_DT_ArchiveEnemyMaster"][entry_id]["AreaInputPath"] = package_path

def append_string_entry(file, entry, text):
    #Make sure the text never exceeds two lines
    if "\r\n" in stringtable[file][entry] or len(stringtable[file][entry]) > 60 or entry == "ITEM_EXPLAIN_RolledOmelette":
        prefix = " "
    else:
        prefix = "\r\n"
    stringtable[file][entry] += prefix + text