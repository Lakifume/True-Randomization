import Manager
import math
import random

def init():
    #Declare variables
    global stat
    stat = [
        "ZAN",
        "DAG",
        "TOT",
        "FLA",
        "ICE",
        "LIG",
        "HOL",
        "DAR"
    ]
    global second_stat
    second_stat = [
        "POI",
        "CUR",
        "STO",
        "SLO"
    ]
    global area
    area = [
        "m01SIP",
        "m02VIL",
        "m03ENT",
        "m04GDN",
        "m05SAN",
        "m06KNG",
        "m07LIB",
        "m08TWR",
        "m09TRN",
        "m10BIG",
        "m11UGD",
        "m12SND",
        "m13ARC",
        "m14TAR",
        "m15JPN",
        "m17RVA",
        "m18ICE"
    ]
    global original_area_to_progress
    original_area_to_progress = {}
    global area_to_progress
    area_to_progress = {}
    global zangetsu_exp
    zangetsu_exp = {
        "N1001":        34,
        "N1011":        58,
        "N1003":        106,
        "N2004":        178,
        "N1005":        274,
        "N2001":        394,
        "N1006":        538,
        "N1012":        706,
        "N1002":        898,
        "N2014":        1114,
        "N2007":        1354,
        "N2006":        1618,
        "N1011_STRONG": 1906,
        "N1004":        2218,
        "N1008":        2554
    }

def convert_area_to_progress():
    #Convert area list to difficulty scale
    for i in range(len(Manager.dictionary["MapOrder"])):
        original_area_to_progress[Manager.dictionary["MapOriginalOrder"][i]] = i + 1.0
        area_to_progress[Manager.dictionary["MapOrder"][i]] = i + 1
    #In between areas with unique difficulty scale
    original_area_to_progress["m04GDN_1"] = (original_area_to_progress["m04GDN"] + original_area_to_progress["m05SAN"])/2
    area_to_progress["m04GDN_1"]          = area_to_progress["m04GDN"]
    original_area_to_progress["m05SAN_1"] = original_area_to_progress["m06KNG"]
    area_to_progress["m05SAN_1"]          = area_to_progress["m05SAN"]
    original_area_to_progress["m07LIB_1"] = original_area_to_progress["m06KNG"]
    area_to_progress["m07LIB_1"]          = area_to_progress["m07LIB"]
    original_area_to_progress["m08TWR_1"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m08TWR_1"]          = area_to_progress["m08TWR"]
    original_area_to_progress["m11UGD_1"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m11UGD_1"]          = area_to_progress["m11UGD"]

def rename_difficulty(normal, hard, nightmare):
    #Rename in-game difficulty options to let the user know what was picked in the mod
    Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Difficulty_Normal"]    = normal
    Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Difficulty_Hard"]      = hard
    Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Difficulty_Nightmare"] = nightmare

def remove_animation(skip):
    #Set the player animation on the difficulties that were not chosen to 0
    #This ensures that there is no difficulty mismatch between the mod and the game
    for i in ["AnimaionPlayRateNormal", "AnimaionPlayRateHard", "AnimaionPlayRateNightmare"]:
        if i in skip:
            continue
        for e in ["P0000", "P0001", "P0006"]:
            Manager.datatable["PB_DT_CharacterParameterMaster"][e][i] = 0.0

def higher_HPMP():
    #Random enemy levels can be rough at the start of the game so give the player a starting stat boost
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxHP"]        += 300.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxMP"]        += 150.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxHP99Enemy"] += 300.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxMP99Enemy"] += 150.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxHP"]        += 300.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxMP"]        += 150.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxHP99Enemy"] += 300.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxMP99Enemy"] += 150.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0006"]["MaxHP"]        += 300.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0006"]["MaxMP"]        += 150.0

def lower_HPMP_growth():
    #If starting stats were increased decrease the correspinding growth to compensate
    Manager.datatable["PB_DT_SpecialEffectDefinitionMaster"]["MaxHPUP"]["Parameter01"]             -= 10.0
    Manager.datatable["PB_DT_SpecialEffectDefinitionMaster"]["MaxMPUP"]["Parameter01"]             -= 5.0
    Manager.datatable["PB_DT_CoordinateParameter"]["BloodlessMainStoryModeMaxHpUpAmount"]["Value"] -= 10.0
    Manager.datatable["PB_DT_CoordinateParameter"]["BloodlessMainStoryModeMaxMpUpAmount"]["Value"] -= 5.0

def no_upgrade_cap():
    #With random item pool the ratio of upgrades can slightly vary so remove the max cap so that all of them can be used
    Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]       = 9999.0
    Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]       = 9999.0
    Manager.datatable["PB_DT_CoordinateParameter"]["PlayerBulletMaxNum"]["Value"] = 999.0

def zangetsu_growth(nightmare):
    #Progressive Zangetsu is all about using level ups for combat growth
    #Nightmare only lets you level up off of bosses so adapt the stats to that
    if nightmare:
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffHp"]["Value"]  = 0.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffMp"]["Value"]  = 0.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffStr"]["Value"] = 6.2
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffCon"]["Value"] = 6.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffInt"]["Value"] = 6.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffMnd"]["Value"] = 5.8
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffLuc"]["Value"] = 3.0
    else:
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffStr"]["Value"] = 3.1
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffCon"]["Value"] = 3.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffInt"]["Value"] = 3.0
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffMnd"]["Value"] = 2.9
        Manager.datatable["PB_DT_CoordinateParameter"]["ZangetsuGrowthCoeffLuc"]["Value"] = 1.5

def nightmare_damage():
    #Progressive Zangetsu on nightmare has to be built onver hard since the vanilla nightmare slot is hardcoded to not receive EXP
    #Update the hard mode damage multipliers to reflect nightmare
    Manager.datatable["PB_DT_CoordinateParameter"]["HardEnemyDamageRate"]["Value"]   = 3.0
    Manager.datatable["PB_DT_CoordinateParameter"]["HardBossDamageRate"]["Value"]    = 3.0
    Manager.datatable["PB_DT_CoordinateParameter"]["HardGimmickDamageRate"]["Value"] = 3.0

def zangetsu_progress():
    #On nightmare only bosses should give out EXP
    #Make it so that each major boss gives exactly one level up if fought in order
    #Max level will be 16
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] == 0:
            continue
        if i in zangetsu_exp:
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = zangetsu_exp[i]
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = zangetsu_exp[i]
        elif i[0:5] in zangetsu_exp:
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = zangetsu_exp[i[0:5]]
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = zangetsu_exp[i[0:5]]
        else:
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = 0
            Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = 0

def zangetsu_no_stats():
    #Zangetsu is very strong by default due to him weilding a late game weapon
    #Make all starting stats 0 to compensate
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["STR"]        = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["INT"]        = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["CON"]        = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MND"]        = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["LUC"]        = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["STR99Enemy"] = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["INT99Enemy"] = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["CON99Enemy"] = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MND99Enemy"] = 0.0
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["LUC99Enemy"] = 0.0

def brv_speed(play_rate):
    #Update boss revenge bosses to have the animation speed of the chosen difficulty
    Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"]["AnimaionPlayRateNormal"]  = Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"][play_rate]
    Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"]["AnimaionPlayRateNormal"] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"][play_rate]
    Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"]["AnimaionPlayRateNormal"]        = Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"][play_rate]

def brv_damage(difficulty):
    #Rebalance boss revenge so that damage is canon with the main game
    #This is also means that random resistances will now affect this mode
    for i in Manager.datatable["PB_DT_BRVAttackDamage"]:
        #Getting enemy strength as if level 45
        if Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Zangetsu":
            base = int(((Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"]["STR99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"]["STR"])/98)*44 + Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"]["STR"])
        elif Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Dominique":
            base = int(((Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"]["STR99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"]["STR"])/98)*44 + Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"]["STR"])
        elif Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Miriam":
            base = int(((Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"]["STR99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"]["STR"])/98)*44 + Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"]["STR"])
        #Multiplier for crits on Gremory
        if Manager.datatable["PB_DT_BRVAttackDamage"][i]["IsZangetsutoAttack"]:
            critical = 2.5
        else:
            critical = 1.0
        #Getting attack multiplier and attributes from DamageMaster
        multiplier = 1.0
        attribute  = []
        #This entry has a different name than the corresponding boss revenge on
        if i == "N1008_Moon_Attack_01_Burst":
            for e in stat:
                if Manager.datatable["PB_DT_DamageMaster"]["N1008_Moon_Attack_Screen"][e]:
                    attribute.append(e)
        #This entry is shared for all of Zangetsu's Flying Vajra elemental versions in boss revenge so average its damage multiplier between the 3 elements
        elif i == "N1011_ATTACK_EXPLOSION":
            multiplier = (Manager.datatable["PB_DT_DamageMaster"]["N1011_ATTACK_ICE_EXPLOSION"]["STR_Correction"] + Manager.datatable["PB_DT_DamageMaster"]["N1011_ATTACK_FIRE_EXPLOSION"]["STR_Correction"])/2
        #Rest is straightforward
        else:
            for e in Manager.datatable["PB_DT_DamageMaster"]:
                if i in e:
                    multiplier = Manager.datatable["PB_DT_DamageMaster"][e]["STR_Correction"]
                    if i == e:
                        for o in stat:
                            if Manager.datatable["PB_DT_DamageMaster"][e][o]:
                                attribute.append(o)
                        break
            if multiplier == 0.0:
                continue
        #Getting enemy and player resistances
        andrealphus = 0.0
        bathin      = 0.0
        bloodless   = 0.0
        gremory     = 0.0
        zangetsu    = 0.0
        dominique   = 0.0
        miriam      = 0.0
        for e in attribute:
            #Add up resistances into a multiplier and average out
            andrealphus += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["P0004"][e]/100
            bathin      += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["P0005"][e]/100
            bloodless   += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["P0006"][e]/100
            gremory     += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["P0007"][e]/100
            zangetsu    += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["N1011_STRONG"][e]/100
            dominique   += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"][e]/100
            miriam      += 1.0 - Manager.datatable["PB_DT_CharacterParameterMaster"]["N0000"][e]/100
        if attribute:
            andrealphus /= len(attribute)
            bathin      /= len(attribute)
            bloodless   /= len(attribute)
            gremory     /= len(attribute)
            zangetsu    /= len(attribute)
            dominique   /= len(attribute)
            miriam      /= len(attribute)
        else:
            #If the attack has no attributes set every multiplier to 1 except for Gremory who is resistant to almost everything
            andrealphus = 1.0
            bathin      = 1.0
            bloodless   = 1.0
            gremory     = 0.75
            zangetsu    = 1.0
            dominique   = 1.0
            miriam      = 1.0
        #Calculating enemy damage
        if Manager.datatable["PB_DT_BRVAttackDamage"][i]["ChanceAndrealphus"] == 100.0 and Manager.datatable["PB_DT_BRVAttackDamage"][i]["ChanceBathin"] == 100.0 and Manager.datatable["PB_DT_BRVAttackDamage"][i]["ChanceBloodless"] == 100.0 and Manager.datatable["PB_DT_BRVAttackDamage"][i]["ChanceGremory"] == 100.0:
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsAndrealphus"] = int((base*multiplier - 40)*andrealphus*difficulty)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBathin"]      = int((base*multiplier - 40)*bathin*difficulty)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBloodless"]   = int((base*multiplier - 40)*bloodless*difficulty)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsGremory"]     = int((base*multiplier - 40)*gremory*critical*difficulty)
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsAndrealphus"] == 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsAndrealphus"] = 1.0
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBathin"]      <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBathin"]      = 1.0
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBloodless"]   <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsBloodless"]   = 1.0
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsGremory"]     <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsGremory"]     = 1.0
        #Calculating player damage
        if i in Manager.dictionary["BossBase"]:
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsZangetsu"]  = int(Manager.dictionary["BossBase"][i]*zangetsu)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsDominique"] = int(Manager.dictionary["BossBase"][i]*dominique)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsMiriam"]    = int(Manager.dictionary["BossBase"][i]*miriam)
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsZangetsu"]  <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsZangetsu"]  = 1.0
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsDominique"] <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsDominique"] = 1.0
            if Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsMiriam"]    <= 0.0:
                Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsMiriam"]    = 1.0

def enemy_rebalance():
    #If custom map is on then default enemy levels need to be rebalanced in order you encounter them
    convert_area_to_progress()
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if not Manager.is_enemy(i)["Enemy"]:
            continue
        if Manager.is_enemy(i)["Main"]:
            #Determine enemy area
            if Manager.dictionary["EnemyLocation"][i]["AreaID"] == "Minor":
                current_area = Manager.dictionary["EnemyLocation"][i]["NormalModeRooms"][0][:6]
            else:
                current_area = Manager.dictionary["EnemyLocation"][i]["AreaID"]
            #Determine new level
            if Manager.dictionary["EnemyLocation"][i]["AreaID"] == "Static" or Manager.dictionary["EnemyLocation"][i]["AreaID"] == "Major":
                continue
            else:
                current_level = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"] + (area_to_progress[current_area] - original_area_to_progress[current_area])*(40/17))
                if current_level < 1:
                    current_level = 1
                elif current_level > 50:
                    current_level = 50
            #Patch
            patch_level(current_level, i)
        elif Manager.is_enemy(i)["Exception"]:
            patch_level(0, i)
        else:
            patch_level(Manager.datatable["PB_DT_CharacterParameterMaster"][i[0:5]]["DefaultEnemyLevel"], i)

def custom_enemy(value):
    #If custom NG+ is chosen ignore random levels and assign a set value to all enemies
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if Manager.is_enemy(i)["Enemy"]:
            patch_level(value, i)

def rand_enemy_level():
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if not Manager.is_enemy(i)["Enemy"]:
            continue
        if Manager.is_enemy(i)["Main"]:
            #Some bosses have a cap for either being too boring or having a time limit
            if Manager.dictionary["EnemyLocation"][i]["AreaID"] == "Minor":
                patch_level(Manager.random_weighted(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"], 1, 50, 1, 5), i)
            #While all enemies have a weigthed random level based on their regular level the last boss can be anything
            elif Manager.dictionary["EnemyLocation"][i]["AreaID"] == "Major":
                patch_level(Manager.random_weighted(999, 1, 99, 1, 5), i)
            else:
                patch_level(Manager.random_weighted(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"], 1, 99, 1, 5), i)
        elif Manager.is_enemy(i)["Exception"]:
            patch_level(0, i)
        else:
            patch_level(Manager.datatable["PB_DT_CharacterParameterMaster"][i[0:5]]["DefaultEnemyLevel"], i)

def rand_enemy_resist():
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if not Manager.is_enemy(i)["Enemy"]:
            continue
        rand_stat(i)

def patch_level(value, entry):
    #Make sure Vepar always has double health in Bloodless mode otherwise the fight is always too short
    if entry == "N1001":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = value
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeEnemyHPOverride"] = int(int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])/98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])*2.0)
    #Update Gebel's health threshold for the red moon based on his level
    elif entry == "N1012":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = value
        Manager.datatable["PB_DT_CoordinateParameter"]["FakeMoon_ChangeHPThreshold"]["Value"] = int(int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])/98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])*0.15)
    #Make Dom's level be the inverse of the chosen value
    elif entry == "N1009_Enemy":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = abs(value - 100)
    #Make it so that Bael and Dom's levels combined always equal 100
    #This ensures that the final fight is never too easy or too hard
    elif entry[0:5] == "N1013" or entry[0:5] == "N1009":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = abs(Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"]["DefaultEnemyLevel"] - 100)
    #Greedling is shared with Breeder despite having a completely different ID
    elif entry == "N3125":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N2016"]["DefaultEnemyLevel"]
    #Other
    else:
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] = value
    
    #While physical and elemental resistances can be random status effect ones should scale with the enemy's level
    #Otherwise some enemies made strong could be easily one shot with petrifying weapons and whatnot
    stat_scale(entry)
    
    #Make level match in all modes
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["HardEnemyLevel"]                   = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["NightmareEnemyLevel"]              = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeDefaultEnemyLevel"]   = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeHardEnemyLevel"]      = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["BloodlessModeNightmareEnemyLevel"] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]

def stat_scale(entry):
    for e in second_stat:
        stat_num = Manager.original_enemy_stats[entry][e]
        #Bosses should always be immune to stone
        if e == "STO" and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["StoneType"] == "EPBStoneType::Boss":
            continue
        #If an enemy is by default immune to all status effects keep it that way
        if Manager.original_enemy_stats[entry]["POI"] == 100.0 and Manager.original_enemy_stats[entry]["CUR"] == 100.0 and Manager.original_enemy_stats[entry]["STO"] >= 99.0 and Manager.original_enemy_stats[entry]["SLO"] == 100.0:
            continue
        #Gain
        if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] > Manager.original_enemy_stats[entry]["Level"]:
            stat_num += 25.0
        if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] > Manager.original_enemy_stats[entry]["Level"] + ((99 - Manager.original_enemy_stats[entry]["Level"]) * 0.5):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        if e == "STO" and stat_num > 99.9:
            stat_num = 99.9
        #Loss
        if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] < Manager.original_enemy_stats[entry]["Level"]:
            stat_num = math.ceil(stat_num - 25.0)
        if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"] < Manager.original_enemy_stats[entry]["Level"] * 0.5:
            stat_num -= 25.0
        if stat_num < 0.0:
            stat_num = 0.0
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = stat_num

def rand_stat(entry):
    #Don't randomize entries that are meant to guard everything
    if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ZAN"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DAG"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["TOT"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["FLA"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ICE"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["LIG"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["HOL"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DAR"] == 100.0:
        return
    #Weak points
    if entry == "N3015_HEAD" or entry == "N1001_HEAD" or entry == "N2001_HEAD":
        for e in stat:
            if Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e] < -20:
                Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = -100
            else:
                Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e]-80
    #Strong parts
    elif entry == "N3108_GUARD" or entry == "N2001_ARMOR":
        for e in stat:
            if Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e] > 20:
                    Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = 100
            else:
                Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e]+80
    #Bael
    elif entry[0:5] == "N1013" and entry != "N1013_Bael" or entry == "N1009_Bael":
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N1013_Bael"][e]
    #Greedling
    elif entry == "N3125":
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N2016"][e]
    #Main entry
    elif Manager.is_enemy(entry)["Main"]:
        if entry in ["N1009_Enemy", "N1013_Bael"]:
            average = 25
        else:
            average = 0
            for e in stat:
                average += Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e]
            average = round(average/len(stat))
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.random_weighted(average, -100, 100, 5, 4)
    #Sub entry
    else:
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e]

def create_log():
    log = {}
    for i in Manager.dictionary["EnemyLocation"]:
        if i == "N1013_Bael":
            entry = "N1013_Dominique"
        else:
            entry = i
        log[Manager.dictionary["EnemyTranslation"][i]] = {}
        log[Manager.dictionary["EnemyTranslation"][i]]["Level"] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"] = {}
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["HP"]  = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP99Enemy"]          - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])         /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MaxHP"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["STR"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["STR99Enemy"]            - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["STR"])           /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["STR"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["INT"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["INT99Enemy"]            - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["INT"])           /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["INT"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["CON"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["CON99Enemy"]            - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["CON"])           /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["CON"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["MND"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MND99Enemy"]            - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MND"])           /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["MND"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["LUC"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["LUC99Enemy"]            - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["LUC"])           /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["LUC"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["EXP"] = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["Experience99Enemy"]     - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["Experience"])    /98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["Experience"])
        log[Manager.dictionary["EnemyTranslation"][i]]["MainStats"]["AP"]  = int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience"])/98)*(Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DefaultEnemyLevel"]-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ArtsExperience"])
        log[Manager.dictionary["EnemyTranslation"][i]]["Resistances"] = {}
        for e in stat:
            log[Manager.dictionary["EnemyTranslation"][i]]["Resistances"][e] = int(Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e])
        for e in second_stat:
            log[Manager.dictionary["EnemyTranslation"][i]]["Resistances"][e] = int(Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e])
        if i == "N0000":
            break
    return log

def hard_patterns():
    #Some major enemies in vanilla lack any form of patterns changes on harder difficulties making them feel underwhelming compared to the rest
    #However this needs to only be done if hard or nightmare is chosen within the mod since those properties would be shared between all difficulties in-game
    
    #Increase Bomber Morte explosion radius
    Manager.datatable["PB_DT_BulletMaster"]["N3024_BOMB_BaudRideBlast"]["BeginEffectBeginScale"] *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N3024_BOMB_BaudRideBlast"]["BeginEffectEndScale"]   *= 2.0
    
    Manager.datatable["PB_DT_CollisionMaster"]["N3024_EXPLOSION"]["R00"] *= 2.0
    Manager.datatable["PB_DT_CollisionMaster"]["N3024_EXPLOSION"]["R01"] *= 2.0
    
    #Increase Millionaire melon explosion radius
    Manager.datatable["PB_DT_BulletMaster"]["N3108_Bomb_Explosion"]["BeginEffectBeginScale"] *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N3108_Bomb_Explosion"]["BeginEffectEndScale"]   *= 1.5
    
    Manager.datatable["PB_DT_CollisionMaster"]["N3108_BOMB_EXPLOSION"]["R00"] *= 1.5
    Manager.datatable["PB_DT_CollisionMaster"]["N3108_BOMB_EXPLOSION"]["R01"] *= 1.5
    
    #Speeding up Bael's animation play rate doesn't work well so instead speed up and expand all of his projectiles
    Manager.datatable["PB_DT_BallisticMaster"]["N1009_RAY"]["InitialSpeed"]        *= 2.0
    Manager.datatable["PB_DT_BallisticMaster"]["N1013_TracerRay"]["InitialSpeed"]  *= 6.0
    Manager.datatable["PB_DT_BallisticMaster"]["N1013_RingLasers"]["InitialSpeed"] *= 9.0
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["EffectBeginScale"]      *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["EffectEndScale"]        *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["BeginEffectBeginScale"] *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["BeginEffectEndScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["EndEffectBeginScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull"]["EndEffectEndScale"]     *= 2.5
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["EffectBeginScale"]      *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["EffectEndScale"]        *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["BeginEffectBeginScale"] *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["BeginEffectEndScale"]   *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["EndEffectBeginScale"]   *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles"]["EndEffectEndScale"]     *= 1.5
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["EffectBeginScale"]      *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["EffectEndScale"]        *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["BeginEffectBeginScale"] *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["BeginEffectEndScale"]   *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["EndEffectBeginScale"]   *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasers"]["EndEffectEndScale"]     *= 2.0
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EffectBeginScale"]    *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EffectEndScale"]      *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EndEffectBeginScale"] *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EndEffectEndScale"]   *= 2.0
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["EffectBeginScale"]      *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["EffectEndScale"]        *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["BeginEffectBeginScale"] *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["BeginEffectEndScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["EndEffectBeginScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Explosion"]["EndEffectEndScale"]     *= 2.5
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["EffectBeginScale"]      *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["EffectEndScale"]        *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["BeginEffectBeginScale"] *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["BeginEffectEndScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["EndEffectBeginScale"]   *= 2.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_FlameSkull_Destroyed"]["EndEffectEndScale"]     *= 2.5
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["EffectBeginScale"]      *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["EffectEndScale"]        *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["BeginEffectBeginScale"] *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["BeginEffectEndScale"]   *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["EndEffectBeginScale"]   *= 1.5
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Bubbles_Destroyed"]["EndEffectEndScale"]     *= 1.5
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["EffectBeginScale"]      *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["EffectEndScale"]        *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["BeginEffectBeginScale"] *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["BeginEffectEndScale"]   *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["EndEffectBeginScale"]   *= 2.0
    Manager.datatable["PB_DT_BulletMaster"]["N1013_RingLasersImpact"]["EndEffectEndScale"]     *= 2.0
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_FlameSkull"]["R00"] *= 2.5
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_FlameSkull"]["R01"] *= 2.5
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_FlameSkull_Explosion"]["R00"] *= 2.5
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_FlameSkull_Explosion"]["R01"] *= 2.5
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Bubbles"]["R00"] *= 1.5
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Bubbles"]["R01"] *= 1.5
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_RingLasers"]["R00"] *= 2.0
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_RingLasers"]["R01"] *= 2.0
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Screech"]["R00"] *= 2.0
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Screech"]["R01"] *= 2.0
    