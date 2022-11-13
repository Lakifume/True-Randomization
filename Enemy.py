import Manager
import math
import random
import copy

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
    global unsizable_enemies
    unsizable_enemies = [
        "N3013",
        "N3014"
        "N3077",
        "N3076",
        "N3123",
        "N3100",
        "N3113",
        "N3116",
        "N3117"
    ]
    global large_enemies
    large_enemies = [
        "N3067",
        "N3030",
        "N3045",
        "N3016",
        "N3023",
        "N3028",
        "N3081",
        "N2003",
        "N3126"
    ]
    global current_portrait_pos
    current_portrait_pos = 0
    global enemy_id_to_class
    enemy_id_to_class = {}
    global enemy_replacement
    enemy_replacement = {}
    global enemy_replacement_invert
    enemy_replacement_invert = {}
    global available_portrait_index
    available_portrait_index = []
    global special_enemy_removal
    special_enemy_removal = {
        "m01SIP_004_Enemy": [
            "Chr_N3006_1122"
        ],
        "m01SIP_011_Enemy": [
            "Chr_N3007",
            "Chr_N3008",
            "Chr_N3011"
        ],
        "m11UGD_013_Enemy": [
            "Chr_N3001_Lift4",
            "Chr_N3001_Lift5",
            "Chr_N3001_Lift6",
            "Chr_N3001_Lift8"
        ],
        "m10BIG_001_Enemy": [
            "Chr_N3005_895"
        ],
        "m10BIG_005_Enemy": [
            "Chr_N3005_895"
        ],
        "m10BIG_008_Enemy_Hard": [
            "Chr_N3019_1202",
            "Chr_N3020",
            "Chr_N3021",
            "Chr_N3022",
            "Chr_N3025",
            "Chr_N3026"
        ],
        "m10BIG_009_Enemy": [
            "Chr_N3017"
        ],
        "m10BIG_013_Enemy_Hard": [
            "Chr_N3019_1378",
            "Chr_N3020",
            "Chr_N3021",
            "Chr_N3022",
            "Chr_N3024"
        ],
        "m10BIG_014_Enemy": [
            "Chr_N3018",
            "Chr_N3020",
            "Chr_N3024",
            "Chr_N3026"
        ],
        "m51EBT_000_Enemy": [
            "Chr_N3126_3612",
            "Chr_N3129_9474",
            "Chr_N3144_9920",
            "Chr_N3150_10960",
            "Chr_N3152",
            "Chr_N3153_3000",
            "Chr_N3155",
            "Chr_N3156"
        ]
    }
    global spawner_to_advantageous_location
    spawner_to_advantageous_location = {
        "m01SIP_001_Enemy_Hard": {
            "N3003_Generator_3258":      ( 1890,    0,  120)
        },
        "m01SIP_001_Enemy_Normal": {
            "Chr_N3003_50":                             None
        },
        "m01SIP_003_Enemy": {
            "Chr_N3006_Generator_422":   ( 1200,    0,  300)
        },
        "m01SIP_004_Enemy": {
            "Chr_N3006_1122":                           None
        },
        "m01SIP_005_Enemy": {
            "Chr_N3003_562":                            None,
            "Chr_N3004_1365":            ( 1280,    0,  120)
        },
        "m01SIP_006_Enemy": {
            "Chr_N3006_1":               (  280,    0,  120),
            "Chr_N3006_2":                              None
        },
        "m01SIP_009_Enemy": {
            "Chr_N3003_834":             (  640,    0,  120),
            "Chr_N3004_1589":                           None,
            "Chr_N3005":                                None
        },
        "m01SIP_010_Enemy": {
            "Chr_N3006_2":                              None,
            "Chr_N3006_457":             (  320,    0,  260)
        },
        "m01SIP_011_Enemy": {
            "Chr_N3003_994":                            None,
            "Chr_N3004":                 ( 4400,    0,  120),
            "Chr_N3006_660":                            None,
            "Chr_N3009":                 ( 2220,    0, 1080)
        },
        "m01SIP_014_Enemy": {
            "Chr_N3003_1346":                           None,
            "Chr_N3004":                 (  820,    0,  120),
            "Chr_N3006_478":                            None
        },
        "m01SIP_016_Enemy": {
            "Chr_N1001_2":               (  520,    0,  780),
        },
        "m01SIP_017_Enemy": {
            "Chr_N3006_478":                            None
        },
        "m01SIP_017_Enemy_Hard": {
            "Chr_N3007_1000":            ( 2520,    0,  120)
        },
        "m01SIP_018_Enemy_Hard": {
            "N3090_Generator_50":        (  960,    0,  120)
        },
        "m01SIP_019_Enemy": {
            "Chr_N3006_Generator2_1825":                None,
            "Chr_N3006_Generator_422":   ( 1120,    0,  300)
        },
        "m02VIL_001_Enemy": {
            "Chr_N3003_2274":                           None,
            "Chr_N3003_3":               (  960,    0,  180)
        },
        "m02VIL_006_Enemy": {
            "Chr_N3003_1":               ( 2700,    0,  120),
            "Chr_N3003_2":                              None
        },
        "m03ENT_001_Enemy": {
            "Chr_N3003_68":                             None
        },
        "m03ENT_001_Enemy_Hard": {
            "N3003_Generator_3258":      ( 4980,    0,  120)
        },
        "m03ENT_001_Enemy_Normal": {
            "N3003_Generator_3258":      ( 4980,    0,  120)
        },
        "m03ENT_003_Enemy": {
            "Chr_N3003_68":                             None
        },
        "m03ENT_003_Enemy_Hard": {
            "N3003_Generator_3258":      ( 3880,    0,  120)
        },
        "m03ENT_003_Enemy_Normal": {
            "N3003_Generator_3258":      ( 3880,    0,  120)
        },
        "m03ENT_014_Enemy_Hard": {
            "N3090_Generator_81":        (  560,    0,  840)
        },
        "m03ENT_017_Enemy_Hard": {
            "N3003_Generator_899":       ( 1040,    0,  120)
        },
        "m05SAN_003_Enemy_Hard": {
            "N3090_Generator_95":        ( 2100,    0, 1380)
        },
        "m05SAN_016_Enemy_Hard": {
            "N3090_Generator_142":       ( 2180,    0, 1860)
        },
        "m05SAN_016_Enemy_Normal": {
            "N3090_Generator_142":       ( 2180,    0, 1860)
        },
        "m05SAN_019_Enemy_Normal": {
            "N3090_Generator_142":       (  680,    0, 3000)
        },
        "m05SAN_019_Enemy_Hard": {
            "N3090_Generator_142":       (  680,    0, 3000)
        },
        "m05SAN_020_Enemy_Hard": {
            "N3090_Generator_142":       ( 1920,    0,  780)
        },
        "m07LIB_029_Enemy_Hard": {
            "N3090_Generator_119":       ( 1860,    0,  180)
        },
        "m07LIB_012_Enemy_Hard": {
            "N3090_Generator_107":       (  340,    0, 1020)
        },
        "m07LIB_013_Enemy_Hard": {
            "N3090_Generator2_55":       ( 1080,    0,  240)
        },
        "m07LIB_013_Enemy_Normal": {
            "N3090_Generator2_55":       ( 1080,    0,  240)
        },
        "m07LIB_017_Enemy_Hard": {
            "N3090_Generator_92":        ( 1540,    0,  120)
        },
        "m07LIB_019_Enemy_Hard": {
            "N3090_Generator_86":        (  680,    0,  120)
        },
        "m07LIB_023_Enemy_Hard": {
            "N3090_Generator2_60":       (  600,    0,  120)
        },
        "m07LIB_023_Enemy_Normal": {
            "N3090_Generator2_60":       (  600,    0,  120)
        },
        "m07LIB_027_Enemy_Hard": {
            "N3090_Generator2_112":      (  300,    0,  120)
        },
        "m07LIB_027_Enemy_Normal": {
            "N3090_Generator_53":        (  300,    0,  120)
        },
        "m07LIB_029_Enemy_Normal": {
            "N3090_Generator_119":       ( 1860,    0,  180)
        },
        "m07LIB_032_Enemy_Hard": {
            "N3090_Generator_73":        ( 2240,    0,  300)
        },
        "m07LIB_035_Enemy_Hard": {
            "N3090_Generator_113":       (  960,    0,  120)
        },
        "m07LIB_035_Enemy_Normal": {
            "N3090_Generator_113":       (  960,    0,  120)
        },
        "m08TWR_005_Enemy_Hard": {
            "N3090_Generator_142":       ( 2200,    0,  120)
        },
        "m08TWR_005_Enemy_Normal": {
            "N3090_Generator_142":       ( 2200,    0,  120)
        },
        "m08TWR_006_Enemy": {
            "N3090_Generator_142":       ( 1080,    0,  300)
        },
        "m08TWR_006_Enemy_Hard": {
            "N3090_Generator2_112":      (  360,    0,  840)
        },
        "m08TWR_013_Enemy_Hard": {
            "N3090_Generator_142":       (  620,    0,  120)
        },
        "m08TWR_013_Enemy_Normal": {
            "N3090_Generator_142":       (  620,    0,  120)
        },
        "m08TWR_017_Enemy": {            
            "N3082_Generator_1445":      ( 3720, -720, 1640)
        },
        "m08TWR_018_Enemy": {            
            "N3082_Generator_509":       ( 3660,  680, 3660)
        },
        "m11UGD_000_Enemy_Hard": {
            "N3090_Generator_89":        (  500,    0,  120)
        },
        "m11UGD_006_Enemy_Hard": {
            "N3090_Generator_75":        (  180,    0,  940)
        },
        "m11UGD_013_Enemy_Hard": {
            "N3090_Generator2_44":                      None,
            "N3090_Generator3":                         None,
            "N3090_Generator_142":       ( 1600,    0, 1980)
        },
        "m11UGD_013_Enemy_Normal": {
            "N3090_Generator2_44":                      None,
            "N3090_Generator3":                         None,
            "N3090_Generator_142":       ( 1600,    0, 1980)
        },
        "m11UGD_031_Enemy_Hard": {
            "N3090_Generator_142":       ( 2700,    0, 1980)
        },
        "m11UGD_031_Enemy_Normal": {
            "N3090_Generator_142":       ( 2700,    0, 1980)
        },
        "m11UGD_037_Enemy_Hard": {
            "N3090_Generator_79":        (  960,    0, 2220)
        },
        "m11UGD_040_Enemy_Hard": {
            "N3090_Generator_99":        (  960,    0,  960)
        },
        "m14TAR_006_Enemy_Hard": {
            "N3090_Generator_107":       ( 1300,    0,  120)
        },
        "m20JRN_000_Enemy": {            
            "N3126_Generator5":          (10040,    0, 2160)
        },
        "m20JRN_001_Enemy": {            
            "N3126_Generator_119":       ( 7480,    0, 1080)
        },
        "m20JRN_002_Enemy": {            
            "N3126_Generator3_131":                     None,
            "N3126_Generator4":          ( 1980,    0,  300)
        },
        "m51EBT_000_Enemy": {            
            "Chr_N3122_Generator2":      (13820,    0,   20),
            "Chr_N3122_Generator3":      (10080,    0,   20),
            "Chr_N3122_Generator4":      ( 5680,    0,   20),
            "Chr_N3122_Generator_74":    ( 3160,    0,   20)
        }
    }

def convert_area_to_progress():
    #Adapt the area order of Bloodless mode based on her starting position
    start_index = Manager.mod_data["MapOrder"].index("m05SAN")
    if start_index < len(Manager.mod_data["MapOrder"]) - start_index - 1:
        shortest_distance = start_index
        remainder_index = shortest_distance*2 + 1
        remainder_range = len(Manager.mod_data["MapOrder"]) - remainder_index
        direction = 1
    else:
        shortest_distance = len(Manager.mod_data["MapOrder"]) - start_index - 1
        remainder_index = len(Manager.mod_data["MapOrder"]) - shortest_distance*2 - 2
        remainder_range = remainder_index + 1
        direction = -1
    for i in range(shortest_distance):
        current_distance = i + 1
        Manager.mod_data["BloodlessModeMapOrder"].append(Manager.mod_data["MapOrder"][start_index - current_distance])
        Manager.mod_data["BloodlessModeMapOrder"].append(Manager.mod_data["MapOrder"][start_index + current_distance])
    for i in range(remainder_range):
        Manager.mod_data["BloodlessModeMapOrder"].append(Manager.mod_data["MapOrder"][remainder_index + direction*i])
    if len(Manager.mod_data["BloodlessModeMapOrder"]) != len(Manager.mod_data["MapOrder"]):
        raise IndexError("Bloodless map order mismatches regular map order length")
    #Convert area list to difficulty scale
    for i in ["", "Original", "BloodlessMode", "BloodlessModeOriginal"]:
        entry = i + "MapOrder"
        area_to_progress[entry] = {}
        for e in range(len(Manager.mod_data[entry])):
            area_to_progress[entry][Manager.mod_data[entry][e]] = e + 1.0
    #Handle in between areas with unique difficulty scale
    area_to_progress["OriginalMapOrder"]["m04GDN_1"] = (area_to_progress["OriginalMapOrder"]["m04GDN"] + area_to_progress["OriginalMapOrder"]["m05SAN"])/2
    area_to_progress["OriginalMapOrder"]["m05SAN_1"] = (area_to_progress["OriginalMapOrder"]["m06KNG"])
    area_to_progress["OriginalMapOrder"]["m07LIB_1"] = (area_to_progress["OriginalMapOrder"]["m06KNG"])
    area_to_progress["OriginalMapOrder"]["m08TWR_1"] = (area_to_progress["OriginalMapOrder"]["m07LIB"] + area_to_progress["OriginalMapOrder"]["m13ARC"])/2
    area_to_progress["OriginalMapOrder"]["m11UGD_1"] = (area_to_progress["OriginalMapOrder"]["m07LIB"] + area_to_progress["OriginalMapOrder"]["m13ARC"])/2
    area_to_progress["BloodlessModeOriginalMapOrder"]["m04GDN_1"] = (area_to_progress["BloodlessModeOriginalMapOrder"]["m04GDN"])
    area_to_progress["BloodlessModeOriginalMapOrder"]["m05SAN_1"] = (area_to_progress["BloodlessModeOriginalMapOrder"]["m05SAN"])
    area_to_progress["BloodlessModeOriginalMapOrder"]["m07LIB_1"] = (area_to_progress["BloodlessModeOriginalMapOrder"]["m06KNG"])
    area_to_progress["BloodlessModeOriginalMapOrder"]["m08TWR_1"] = (area_to_progress["BloodlessModeOriginalMapOrder"]["m07LIB"] + area_to_progress["BloodlessModeOriginalMapOrder"]["m13ARC"])/2
    area_to_progress["BloodlessModeOriginalMapOrder"]["m11UGD_1"] = (area_to_progress["BloodlessModeOriginalMapOrder"]["m07LIB"] + area_to_progress["BloodlessModeOriginalMapOrder"]["m13ARC"])/2
    for i in ["m04GDN", "m05SAN", "m07LIB", "m08TWR", "m11UGD"]:
        area_to_progress["MapOrder"][i + "_1"]              = area_to_progress["MapOrder"][i]
        area_to_progress["BloodlessModeMapOrder"][i + "_1"] = area_to_progress["BloodlessModeMapOrder"][i]
    #Change the order of progressive Zangetsu experience
    new_boss_order = []
    for i in range(len(Manager.mod_data["MapOrder"])):
        for e in zangetsu_exp:
            if Manager.mod_data["EnemyLocation"][e]["AreaID"] == "Minor":
                current_area = Manager.mod_data["EnemyLocation"][e]["NormalModeRooms"][0][:6]
            else:
                current_area = Manager.mod_data["EnemyLocation"][e]["AreaID"]
            if area_to_progress["MapOrder"][current_area] == i + 1.0:
                new_boss_order.append(e)
    if len(new_boss_order) != len(zangetsu_exp):
        raise IndexError("New Zangetsu boss order mismatches original EXP order length")
    values = list(zangetsu_exp.values())
    zangetsu_exp.clear()
    zangetsu_exp.update(dict(zip(new_boss_order, values)))

def high_starting_stats():
    #Random enemy levels can be rough at the start of the game so give the player a starting stat boost
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxHP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxMP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxHP99Enemy"] += Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0000"]["MaxMP99Enemy"] += Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxHP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxMP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxHP99Enemy"] += Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0001"]["MaxMP99Enemy"] += Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0006"]["MaxHP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"]/2
    Manager.datatable["PB_DT_CharacterParameterMaster"]["P0006"]["MaxMP"]        += Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"]/2
    #Reduce the stats gained from upgrades in return
    Manager.datatable["PB_DT_SpecialEffectDefinitionMaster"]["MaxHPUP"]["Parameter01"]             /= 2
    Manager.datatable["PB_DT_SpecialEffectDefinitionMaster"]["MaxMPUP"]["Parameter01"]             /= 2
    Manager.datatable["PB_DT_CoordinateParameter"]["BloodlessMainStoryModeMaxHpUpAmount"]["Value"] /= 2
    Manager.datatable["PB_DT_CoordinateParameter"]["BloodlessMainStoryModeMaxMpUpAmount"]["Value"] /= 2
    #As well as the upgrade cap
    Manager.datatable["PB_DT_CoordinateParameter"]["HpMaxUpLimit"]["Value"] /= 2
    Manager.datatable["PB_DT_CoordinateParameter"]["MpMaxUpLimit"]["Value"] /= 2

def zangetsu_growth(nightmare):
    #Progressive Zangetsu is all about using level ups for combat growth
    #Nightmare only lets you level up off of bosses so adapt the stats for that
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
    #Progressive Zangetsu on nightmare has to be built over hard since the vanilla nightmare slot is hardcoded to not receive EXP
    #Update the hard mode damage multipliers to reflect nightmare
    Manager.datatable["PB_DT_CoordinateParameter"]["HardEnemyDamageRate"]["Value"]   = 3.0
    Manager.datatable["PB_DT_CoordinateParameter"]["HardBossDamageRate"]["Value"]    = 3.0
    Manager.datatable["PB_DT_CoordinateParameter"]["HardGimmickDamageRate"]["Value"] = 3.0

def zangetsu_progress():
    #On nightmare only bosses should give EXP
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
    #This also means that random resistances will now affect this mode
    for i in Manager.datatable["PB_DT_BRVAttackDamage"]:
        #Getting enemy strength as if level 45
        if Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Zangetsu":
            base = calculate_stat("N1011_STRONG", 45, "STR")
        elif Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Dominique":
            base = calculate_stat("N1009_Enemy", 45, "STR")
        elif Manager.datatable["PB_DT_BRVAttackDamage"][i]["Owner"] == "Miriam":
            base = calculate_stat("N0000", 45, "STR")
        #Multiplier for crits on Gremory
        if Manager.datatable["PB_DT_BRVAttackDamage"][i]["IsZangetsutoAttack"]:
            critical = 2.5
        else:
            critical = 1.0
        #Getting attack multiplier and attributes from DamageMaster
        multiplier = 1.0
        attribute  = []
        #This entry has a different name than the corresponding boss revenge one
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
        if i in Manager.mod_data["BossBase"]:
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsZangetsu"]  = int(Manager.mod_data["BossBase"][i]*zangetsu)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsDominique"] = int(Manager.mod_data["BossBase"][i]*dominique)
            Manager.datatable["PB_DT_BRVAttackDamage"][i]["VsMiriam"]    = int(Manager.mod_data["BossBase"][i]*miriam)
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
        if not Manager.is_enemy(i):
            continue
        for e in ["", "BloodlessMode"]:
            if Manager.is_main_enemy(i):
                #Determine enemy area
                if Manager.mod_data["EnemyLocation"][i]["AreaID"] == "Minor":
                    current_area = Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"][0][:6]
                else:
                    current_area = Manager.mod_data["EnemyLocation"][i]["AreaID"]
                #Determine new level
                if Manager.mod_data["EnemyLocation"][i]["AreaID"] == "Static" or Manager.mod_data["EnemyLocation"][i]["AreaID"] == "Major":
                    continue
                else:
                    current_level = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "DefaultEnemyLevel"] + (area_to_progress[e + "MapOrder"][current_area] - area_to_progress[e + "OriginalMapOrder"][current_area])*(40/17))
                    if current_level < 1:
                        current_level = 1
                    elif current_level > 50:
                        current_level = 50
                #Patch
                patch_level(current_level, i, e)
            elif i[0:5] in Manager.datatable["PB_DT_CharacterParameterMaster"]:
                patch_level(Manager.datatable["PB_DT_CharacterParameterMaster"][i[0:5]]["DefaultEnemyLevel"], i, e)
            else:
                patch_level(0, i, e)

def custom_enemy(value):
    #If custom NG+ is chosen ignore random levels and assign a set value to all enemies
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if Manager.is_enemy(i):
            patch_level(value, i, "")
            patch_level(value, i, "BloodlessMode")

def rand_enemy_level():
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if not Manager.is_enemy(i):
            continue
        for e in ["", "BloodlessMode"]:
            if Manager.is_main_enemy(i):
                #Some bosses have a cap for either being too boring or having a time limit
                if Manager.mod_data["EnemyLocation"][i]["AreaID"] == "Minor":
                    patch_level(Manager.random_weighted(Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "DefaultEnemyLevel"], 1, 50, 1, 2), i, e)
                #While all enemies have a weigthed random level based on their regular level the last boss can be anything
                elif Manager.mod_data["EnemyLocation"][i]["AreaID"] == "Major":
                    patch_level(random.randint(1, 99), i, e)
                else:
                    patch_level(Manager.random_weighted(Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "DefaultEnemyLevel"], 1, 99, 1, 2), i, e)
            elif i[0:5] in Manager.datatable["PB_DT_CharacterParameterMaster"]:
                patch_level(Manager.datatable["PB_DT_CharacterParameterMaster"][i[0:5]]["DefaultEnemyLevel"], i, e)
            else:
                patch_level(0, i, e)

def rand_enemy_resist():
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if Manager.is_enemy(i):
            rand_stat(i)

def rand_enemy_placement():
    #This needs to be done before item randomization so that the logic adapts
    #Create a dict for enemy id to their class names
    for i in Manager.mod_data["ActorPointer"]:
        enemy_id = Manager.mod_data["ActorPointer"][i]["Name"]
        if enemy_id in enemy_id_to_class:
            continue
        enemy_id_to_class[enemy_id] = i
    enemy_id_to_class["N3099"] = enemy_id_to_class["N3090"]
    #Gather portrait indexes
    for i in Manager.mod_data["ActorPointer"]:
        if "N3100" in i:
            available_portrait_index.append(int(i.split("_")[2]))
    #Get enemy list
    old_enemy_slots = []
    for i in Manager.mod_data["EnemyLocation"]:
        if Manager.mod_data["EnemyLocation"][i]["Type"] in ["Ground", "Air", "Spawner"]:
            old_enemy_slots.append(i)
    new_enemy_slots = copy.deepcopy(old_enemy_slots)
    #Shuffle enemies (special)
    for i in list(old_enemy_slots):
        chosen = random.choice(new_enemy_slots)
        #Prevent large enemies from ending up over the morte
        if i == "N3003":
            while Manager.mod_data["EnemyLocation"][chosen]["Wheight"] > Manager.mod_data["EnemyLocation"][i]["Wheight"]:
                chosen = random.choice(new_enemy_slots)
        #Som enemies completely ignores any scale modifiers so prevent them from going over large enemies
        elif i in large_enemies:
            while chosen in unsizable_enemies:
                chosen = random.choice(new_enemy_slots)
        else:
            continue
        enemy_replacement[i] = chosen
        new_enemy_slots.remove(chosen)
        old_enemy_slots.remove(i)
    #Shuffle enemies
    for i in old_enemy_slots:
        chosen = random.choice(new_enemy_slots)
        enemy_replacement[i] = chosen
        new_enemy_slots.remove(chosen)
    for i in enemy_replacement:
        enemy_replacement_invert[enemy_replacement[i]] = i
    #Remove the lone Seama in the early Galleon room since it is too weak to reflect its wheight of 4
    if enemy_replacement["N3006"] != "N3006":
        Manager.mod_data["EnemyLocation"]["N3006"]["NormalModeRooms"].remove("m01SIP_004")
    #Update enemy location
    original_enemy_rooms = {}
    for i in Manager.mod_data["EnemyLocation"]:
        original_enemy_rooms[i] = copy.deepcopy(Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"])
    for i in Manager.mod_data["EnemyLocation"]:
        if i in enemy_replacement:
            Manager.mod_data["EnemyLocation"][i]["NormalModeRooms"] = original_enemy_rooms[enemy_replacement_invert[i]]
    #Remove the Gusions from library and labs if they were scaled up
    if not enemy_replacement_invert["N3035"] in large_enemies:
        Manager.mod_data["EnemyLocation"]["N3035"]["NormalModeRooms"].append("m07LIB_001")
        Manager.mod_data["EnemyLocation"]["N3035"]["NormalModeRooms"].append("m13ARC_001")
    Manager.mod_data["EnemyLocation"][enemy_replacement["N3035"]]["NormalModeRooms"].remove("m07LIB_001")
    Manager.mod_data["EnemyLocation"][enemy_replacement["N3035"]]["NormalModeRooms"].remove("m13ARC_001")
    #Lili still spawns at Millionaire's
    Manager.mod_data["EnemyLocation"]["N3058"]["NormalModeRooms"].append("m88BKR_002")
    Manager.mod_data["EnemyLocation"][enemy_replacement["N3058"]]["NormalModeRooms"].remove("m88BKR_002")
    #Demon Lord still spawns at Carpenter's
    Manager.mod_data["EnemyLocation"]["N3057"]["NormalModeRooms"].append("m88BKR_004")
    Manager.mod_data["EnemyLocation"][enemy_replacement["N3057"]]["NormalModeRooms"].remove("m88BKR_004")
    #Scythe Mite and 8 Bit Zombie spawners seem to fail spawning anything in rooms of resistricted sizes
    #Update the logic by removing the rooms that most likely won't spawn them
    for i in list(Manager.mod_data["EnemyLocation"]["N3082"]["NormalModeRooms"]):
        if Manager.datatable["PB_DT_RoomMaster"][i]["AreaHeightSize"] < 2:
            Manager.mod_data["EnemyLocation"]["N3082"]["NormalModeRooms"].remove(i)
    for i in list(Manager.mod_data["EnemyLocation"]["N3121"]["NormalModeRooms"]):
        if Manager.datatable["PB_DT_RoomMaster"][i]["AreaHeightSize"] < 2:
            Manager.mod_data["EnemyLocation"]["N3121"]["NormalModeRooms"].remove(i)

def update_enemy_placement():
    #Actually do the removals mentioned above
    if enemy_replacement_invert["N3035"] in large_enemies:
        Manager.remove_level_class("m07LIB_001_Gimmick", "Chr_N3035_C")
        Manager.remove_level_class("m13ARC_001_Gimmick", "IncubatorGlass_BP_C")
    #Patch enemies in rooms
    for i in Manager.mod_data["MapLogic"]:
        change_room_enemies(i)

def change_room_enemies(room):
    enemy_countdown = {}
    #Loop through all difficulties
    for i in ["", "_Normal", "_Hard"]:
        filename = room + "_Enemy" + i
        if not filename in Manager.game_data:
            continue
        #Loop through all exports
        for e in range(len(Manager.game_data[filename].Exports)):
            #Check if the export is an enemy
            export_name = str(Manager.game_data[filename].Exports[e].ObjectName)
            if int(str(Manager.game_data[filename].Exports[e].OuterIndex)) == 0:
                continue
            class_index = int(str(Manager.game_data[filename].Exports[e].ClassIndex))
            if class_index >= 0:
                continue
            old_class_name = str(Manager.game_data[filename].Imports[abs(class_index) - 1].ObjectName)
            if not old_class_name in Manager.mod_data["ActorPointer"]:
                continue
            old_enemy_id = Manager.mod_data["ActorPointer"][old_class_name]["Name"]
            if not Manager.is_enemy(old_enemy_id):
                continue
            #The village has unused moco weeds
            if room == "m02VIL_006" and old_enemy_id == "N3066":
                continue
            #If it is a dulla head assume it's a Malediction
            if old_enemy_id == "N3090":
                old_enemy_id = "N3099"
            #Get the old actor's properties
            location = Manager.FVector(0, 0, 0)
            rotation = Manager.FRotator(0, 0, 0)
            scale    = Manager.FVector(1, 1, 1)
            for o in Manager.game_data[filename].Exports[e].Data:
                #Change it back to a dulla head if the setting is there
                if str(o.Name) == "SpawnIsN3099":
                    old_enemy_id = "N3090"
                if str(o.Name) == "RootComponent":
                    root_index = int(str(o.Value)) - 1
                    for u in Manager.game_data[filename].Exports[root_index].Data:
                        if str(u.Name) == "RelativeLocation":
                            location = u.Value[0].Value
                        if str(u.Name) == "RelativeRotation":
                            rotation = u.Value[0].Value
                        if str(u.Name) == "RelativeScale3D":
                            scale    = u.Value[0].Value
            if location.X < -500:
                continue
            if not old_enemy_id in enemy_replacement:
                continue
            new_enemy_id = enemy_replacement[old_enemy_id]
            if old_enemy_id == new_enemy_id:
                continue
            #Remove the old enemy
            Manager.remove_level_actor(filename, e)
            #Some enemies shouldn't get replaced and only deleted
            if filename in special_enemy_removal:
                if export_name in special_enemy_removal[filename]:
                    continue
            #If non-spawner enemies are placed over spawner ones determine an advantageous location to avoid clipping into objects
            if filename in spawner_to_advantageous_location:
                if export_name in spawner_to_advantageous_location[filename] and Manager.mod_data["EnemyLocation"][new_enemy_id]["Type"] != "Spawner":
                    if spawner_to_advantageous_location[filename][export_name]:
                        location.X = spawner_to_advantageous_location[filename][export_name][0]
                        location.Y = spawner_to_advantageous_location[filename][export_name][1]
                        location.Z = spawner_to_advantageous_location[filename][export_name][2]
                    else:
                        continue
            #Balance enemy spawns around their wheight
            #If the new wheight is higher only replace a portion of the enemy's instances
            if Manager.mod_data["EnemyLocation"][new_enemy_id]["Wheight"] > Manager.mod_data["EnemyLocation"][old_enemy_id]["Wheight"]:
                enemy_num = 2**(Manager.mod_data["EnemyLocation"][new_enemy_id]["Wheight"] - Manager.mod_data["EnemyLocation"][old_enemy_id]["Wheight"])
                if new_enemy_id in enemy_countdown:
                    if enemy_countdown[new_enemy_id] == 0:
                        add_level_enemy(filename, export_name, old_enemy_id, new_enemy_id, location, rotation, scale, 0, 0)
                        enemy_countdown[new_enemy_id] = enemy_num
                else:
                    enemy_countdown[new_enemy_id] = enemy_num
                    add_level_enemy(filename, export_name, old_enemy_id, new_enemy_id, location, rotation, scale, 0, 0)
                enemy_countdown[new_enemy_id] -= 1
            #If the new wheight is lower spawn more instances of the enemy with the old location as its center
            elif Manager.mod_data["EnemyLocation"][new_enemy_id]["Wheight"] < Manager.mod_data["EnemyLocation"][old_enemy_id]["Wheight"]:
                enemy_num = 2**(Manager.mod_data["EnemyLocation"][old_enemy_id]["Wheight"] - Manager.mod_data["EnemyLocation"][new_enemy_id]["Wheight"])
                offset = 120*(1.5**(Manager.mod_data["EnemyLocation"][new_enemy_id]["Wheight"] - 1))
                if old_enemy_id in large_enemies:
                    offset *= 1.5
                for o in range(enemy_num):
                    horizontal_offset = -offset*(enemy_num - 1)/2 + offset*o
                    if "Air" in Manager.mod_data["EnemyLocation"][new_enemy_id]["Type"] and not new_enemy_id in ["N3029", "N3030"]:
                        vertical_offset = random.uniform(-offset, offset)
                    else:
                        vertical_offset = 0
                    add_level_enemy(filename, export_name, old_enemy_id, new_enemy_id, location, rotation, scale, horizontal_offset, vertical_offset)
            #If the new wheight is identical then do a standard replacement
            else:
                add_level_enemy(filename, export_name, old_enemy_id, new_enemy_id, location, rotation, scale, 0, 0)

def add_level_enemy(filename, export_name, old_enemy_id, new_enemy_id, location, rotation, scale, horizontal_offset, vertical_offset):
    room = filename.split("_Enemy")[0]
    room_width  = Manager.datatable["PB_DT_RoomMaster"][room]["AreaWidthSize"]*1260
    room_height = Manager.datatable["PB_DT_RoomMaster"][room]["AreaHeightSize"]*720
    hard_mode = "Hard" in filename
    location = Manager.FVector(location.X, location.Y, location.Z)
    rotation = Manager.FRotator(rotation.Pitch, rotation.Yaw, rotation.Roll)
    scale    = Manager.FVector(scale.X, scale.Y, scale.Z)
    #If the room is a rotating 3d one then use the forward vector to shift position
    if room in Manager.rotating_room_to_center:
        rotation.Yaw = -math.degrees(math.atan2(location.X - Manager.rotating_room_to_center[room][0], location.Y - Manager.rotating_room_to_center[room][1]))
        forward_vector = (math.sin(math.radians(rotation.Yaw))*(-1),      math.cos(math.radians(rotation.Yaw)))
        right_vector   = (math.sin(math.radians(rotation.Yaw - 90))*(-1), math.cos(math.radians(rotation.Yaw - 90)))
    else:
        rotation.Yaw = 0
        forward_vector = (0, 1)
        right_vector   = (1, 0)
        location.Y = 0
    #Apply offsets
    location.X += right_vector[0]*horizontal_offset
    location.Y += right_vector[1]*horizontal_offset
    location.Z += vertical_offset
    #If it is a portrait then cycle through each version
    global current_portrait_pos
    if new_enemy_id == "N3100":
        new_class_name = "Chr_N3100_" + "{:03d}".format(available_portrait_index[current_portrait_pos]) + "_C"
        if current_portrait_pos < len(available_portrait_index) - 1:
            current_portrait_pos += 1
        else:
            current_portrait_pos = 0
    else:
        new_class_name = enemy_id_to_class[new_enemy_id]
    #Adjust position when necessary
    if Manager.mod_data["EnemyLocation"][old_enemy_id]["Type"] in ["Ground", "Spawner"] and Manager.mod_data["EnemyLocation"][new_enemy_id]["Type"] == "Air":
        location.Z += 120
    if Manager.mod_data["EnemyLocation"][old_enemy_id]["Type"] == "Air" and Manager.mod_data["EnemyLocation"][new_enemy_id]["Type"] in ["Ground", "Spawner"]:
        location.Z -= 120
    if old_enemy_id in ["N3029", "N3030"] and room != "m03ENT_001":
        location.Z -= 200
    if new_enemy_id in ["N3029", "N3030"]:
        location.Z += 120
    if new_enemy_id in ["N3089", "N3088"]:
        location.Z -= 60
    #Some enemies lie farther in the background
    if new_enemy_id == "N3100":
        location.X -= forward_vector[0]*270
        location.Y -= forward_vector[1]*270
    if new_enemy_id in ["N3070", "N3071"]:
        location.X -= forward_vector[0]*120
        location.Y -= forward_vector[1]*120
    if new_enemy_id in ["N3113", "N3116", "N3117"]:
        location.X -= forward_vector[0]*400
        location.Y -= forward_vector[1]*400
    #Some enemies are in inconvenient spots
    if filename == "m03ENT_023_Enemy" and export_name == "Chr_N3087_2":
        location.Z += 120
    if filename == "m05SAN_008_Enemy" and export_name == "Chr_N3055_2407":
        location.X += 340
    if filename == "m05SAN_008_Enemy_Hard" and export_name == "Chr_N3073_1952":
        location.X -= 260
    if filename == "m05SAN_021_Enemy" and export_name == "Chr_N3056_860":
        location.X += 220
    if filename == "m06KNG_014_Enemy_Hard" and export_name == "Chr_N3056_834":
        location.X += 300
    if filename == "m06KNG_017_Enemy_Hard" and export_name == "Chr_N3053_87":
        location.X += 260
    if filename == "m07LIB_025_Enemy" and export_name == "Chr_N3012_1157":
        location.X -= 520
        location.Z -= 180
    if filename == "m07LIB_025_Enemy" and export_name == "Chr_N3033_808":
        location.X -= 240
    if filename == "m07LIB_034_Enemy" and export_name == "Chr_210":
        location.X += 380
    if filename == "m10BIG_006_Enemy" and export_name in ["Chr_N3033", "Chr_N3034", "Chr_N3035", "Chr_N3036", "Chr_N3037"]:
        location.Z += 720
    if filename == "m10BIG_016_Enemy" and export_name == "Chr_N3039":
        location.X += 240
        location.Z += 520
    if filename == "m11UGD_017_Enemy_Hard" and export_name == "Chr_N3055_1042":
        location.X -= 310
    if filename == "m11UGD_032_Enemy" and export_name == "Chr_N3044_977":
        location.X += 270
        location.Z += 120
    if filename == "m51EBT_000_Enemy" and export_name in ["Chr_N3136", "Chr_N3139_3"]:
        location.Z -= 90
    if filename == "m51EBT_000_Enemy" and export_name in ["Chr_N3143", "Chr_N3146"]:
        location.Z += 90
    #Avoid placing 8 bit zombies near the vertical edges of the room
    if new_enemy_id == "N3121":
        location.Z = max(min(location.Z, room_height - 360), 360)
    #The giant dulla head spawner actually requires to be scaled up to function properly
    if new_enemy_id == "N3126":
        scale.X = 32
        scale.Y = 1
        scale.Z = 32
    if old_enemy_id == "N3126":
        scale.X = 1
        scale.Y = 1
        scale.Z = 1
    #Make sure the enemy is never too close to the edge of the screen
    if room != "m12SND_025":
        location.X = max(min(location.X, room_width  - 60), 60)
        location.Z = max(min(location.Z, room_height - 60), 60)
    #If the enemy is right above a downwards entrance do not add it
    if "_".join([room[3:], str(int(location.X//1260)), "0", "BOTTOM"]) in Manager.map_connections[room] and 500 < location.X%1260 < 760 and location.Z < 360:
        return
    #One of the Journey rooms has a faulty persistent level export in its enemy file, so add in its bg file instead
    if room == "m20JRN_002":
        filename = "m20JRN_002_BG"
    #Setup the actor properties
    properties = {}
    if new_enemy_id == "N3003":
        if hard_mode:
            properties["MinSpawnInterval"] = 1.5
            properties["MaxSpawnInterval"] = 3.0
            properties["MaxSpawnCount"]    = 6
        else:
            properties["MinSpawnInterval"] = 2.0
            properties["MaxSpawnInterval"] = 4.0
            properties["MaxSpawnCount"]    = 4
        properties["RightSpawnRate"] = 0.5
    if new_enemy_id == "N3082":
        properties["MaxSpawnCount"]  = 3
        properties["RightSpawnRate"] = 0.5
    if new_enemy_id in ["N3090", "N3099"]:
        if hard_mode:
            properties["MinSpawnInterval"] = random.uniform(0.5, 1.5)
            properties["MaxSpawnInterval"] = random.uniform(1.5, 2.0)
            properties["MaxSpawnCount"]    = random.randint(4, 6)
        else:
            properties["MinSpawnInterval"] = random.uniform(1.5, 2.0)
            properties["MaxSpawnInterval"] = random.uniform(2.0, 3.0)
            properties["MaxSpawnCount"]    = random.randint(3, 4)
    if new_enemy_id == "N3099":
        properties["SpawnIsN3099"] = True
    if new_enemy_id == "N3121":
        properties["IntervalTime"] = random.uniform(1.0, 2.0)
        properties["MaxNum"]       = random.randint(4, 8)
    if new_enemy_id == "N3126":
        properties["MinSpawnInterval"] = random.uniform(2.0, 4.0)
        properties["MaxSpawnInterval"] = random.uniform(5.0, 8.0)
    if new_enemy_id == "N3067":
        properties["HiddenInRock"] = False
    if new_enemy_id == "N3053":
        properties["StandbyType"]        = Manager.FName(Manager.game_data[filename], "EPBEnemyGargoyleStandbyType::Normal")
        properties["TargetNoticeRangeX"] = 1200.0
    if new_enemy_id == "N3063":
        properties["StandbyType"] = Manager.FName(Manager.game_data[filename], "EPBEnemyDantalionEntryType::Floating")
    if new_enemy_id == "N3064":
        properties["ChainLength"] = 350.0
        properties["IsCeiling"]   = location.Y > room_height - 360
    if new_enemy_id == "N3087":
        properties["StandbyType"] = Manager.FName(Manager.game_data[filename], "EPBEnemyCyhiraethStandbyType::Floating")
    if new_enemy_id == "N3122":
        properties["PlayerDistanceX"] = random.uniform( 90.0, 630.0)
        properties["PlayerDistanceZ"] = random.uniform(180.0, 360.0)
    #Add the new enemy
    Manager.add_level_actor(filename, new_class_name, location, rotation, scale, properties)
    #If it is a cannon enemy then potentially add extra stacks
    if new_enemy_id == "N3005":
        stack_num = random.randint(1, 3)
        offset = 170
    elif new_enemy_id == "N3016" and old_enemy_id != "N3023":
        if room_height - location.Z < 480:
            return
        stack_num = random.randint(1, 2)
        offset = 360
    elif new_enemy_id == "N3124":
        stack_num = random.randint(1, 4)
        offset = 100
    else:
        return
    for i in range(stack_num - 1):
        location.Z += offset
        Manager.add_level_actor(filename, new_class_name, location, rotation, scale, properties)

def retain_enemy_progression():
    #After randomizing enemies keep the difficulty progression the same by making them inherit original properties
    original_enemy_levels = {}
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if Manager.is_enemy(i):
            original_enemy_levels[i] = {}
            original_enemy_levels[i]["Miriam"]    = Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
            original_enemy_levels[i]["Bloodless"] = Manager.datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeDefaultEnemyLevel"]
    #Update enemy levels
    for i in Manager.datatable["PB_DT_CharacterParameterMaster"]:
        if not Manager.is_enemy(i):
            continue
        enemy_id = i[0:5]
        if enemy_id in enemy_replacement:
            patch_level(original_enemy_levels[enemy_replacement_invert[enemy_id]]["Miriam"], i, "")
            patch_level(original_enemy_levels[enemy_replacement_invert[enemy_id]]["Bloodless"], i, "BloodlessMode")
            #Den enemies that are placed in the overworld struggle to fit in most places so shrink them down a bit
            if enemy_id in large_enemies and not enemy_replacement_invert[enemy_id] in large_enemies:
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["CapsuleRadius"]     /= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["CapsuleHeight"]     /= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleX"]        /= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleY"]        /= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleZ"]        /= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"]             *= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP"]             *= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]      *= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP99Enemy"]      *= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]*0.8125)
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"]*0.8125)
            #On the other hand increase the size of overworld enemies placed in the Den
            if not enemy_id in large_enemies and enemy_replacement_invert[enemy_id] in large_enemies:
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["CapsuleRadius"]     *= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["CapsuleHeight"]     *= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleX"]        *= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleY"]        *= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MeshScaleZ"]        *= 1.5
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP"]             /= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP"]             /= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxHP99Enemy"]      /= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["MaxMP99Enemy"]      /= 0.8125
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]        = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience"]/0.8125)
                Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"] = round(Manager.datatable["PB_DT_CharacterParameterMaster"][i]["Experience99Enemy"]/0.8125)
    #Update enemy area info
    enemy_id_to_archive = {}
    for i in Manager.datatable["PB_DT_ArchiveEnemyMaster"]:
        enemy_id_to_archive[Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["UniqueID"]] = i
    for i in Manager.datatable["PB_DT_ArchiveEnemyMaster"]:
        enemy_id = Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["UniqueID"]
        if enemy_id in enemy_replacement:
            if enemy_replacement_invert[enemy_id] in enemy_id_to_archive:
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area1"] = Manager.original_datatable["PB_DT_ArchiveEnemyMaster"][enemy_id_to_archive[enemy_replacement_invert[enemy_id]]]["Area1"]
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area2"] = Manager.original_datatable["PB_DT_ArchiveEnemyMaster"][enemy_id_to_archive[enemy_replacement_invert[enemy_id]]]["Area2"]
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area3"] = Manager.original_datatable["PB_DT_ArchiveEnemyMaster"][enemy_id_to_archive[enemy_replacement_invert[enemy_id]]]["Area3"]
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area4"] = Manager.original_datatable["PB_DT_ArchiveEnemyMaster"][enemy_id_to_archive[enemy_replacement_invert[enemy_id]]]["Area4"]
            else:
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area1"] = "None"
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area2"] = "None"
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area3"] = "None"
                Manager.datatable["PB_DT_ArchiveEnemyMaster"][i]["Area4"] = "None"
    #Manager.datatable["PB_DT_ArchiveEnemyMaster"][enemy_id_to_archive[enemy_replacement_invert["N3035"]]]["Area1"] = "None"

def patch_level(value, entry, extra):
    #Make Dom's level be the inverse of the chosen value
    if entry == "N1009_Enemy":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"] = abs(value - 100)
    #Make it so that Bael and Dom's levels combined always equal 100
    #This ensures that the final fight is never too easy or too hard
    elif entry[0:5] in ["N1009", "N1013"]:
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"] = abs(Manager.datatable["PB_DT_CharacterParameterMaster"]["N1009_Enemy"][extra + "DefaultEnemyLevel"] - 100)
    #Greedling is shared with Breeder despite having a completely different ID
    elif entry == "N3125":
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N2016"][extra + "DefaultEnemyLevel"]
    #Other
    else:
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"] = value
    
    #While physical and elemental resistances can be random status effect ones should scale with the enemy's level
    #Otherwise some enemies made strong could be easily one shot with petrifying weapons and whatnot
    #Ignore it for Bloodless mode though
    if not extra:
        stat_scale(entry)
    
    #Make level match in all difficulties
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "HardEnemyLevel"]      = Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"]
    Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "NightmareEnemyLevel"] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry][extra + "DefaultEnemyLevel"]

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
        if e == "STO" and stat_num < 50.0:
            stat_num = 50.0
        Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = stat_num

def rand_stat(entry):
    #Don't randomize entries that are meant to guard everything
    if Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ZAN"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DAG"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["TOT"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["FLA"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["ICE"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["LIG"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["HOL"] == 100.0 and Manager.datatable["PB_DT_CharacterParameterMaster"][entry]["DAR"] == 100.0:
        return
    #Weak points
    if entry in ["N3015_HEAD", "N1001_HEAD", "N2001_HEAD"]:
        for e in stat:
            if Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e] < -20:
                Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = -100
            else:
                Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e]-80
    #Strong parts
    elif entry in ["N3108_GUARD", "N2001_ARMOR"]:
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
    #Dullahammer EX
    elif entry == "N3127":
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"]["N3015"][e]
    #Main entry
    elif Manager.is_main_enemy(entry):
        #Use the original resistances to create an average to base the random resistances off of
        average = 0
        for e in stat:
            average += Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e]
        average = average/len(stat)
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.random_weighted(round(average), -100, 100, 5, 4)
    #Sub entry
    else:
        for e in stat:
            Manager.datatable["PB_DT_CharacterParameterMaster"][entry][e] = Manager.datatable["PB_DT_CharacterParameterMaster"][entry[0:5]][e]

def update_special_properties():
    #Make sure Vepar always has double health in Bloodless mode otherwise the fight is too short
    for i in ["N1001", "N1001_HEAD"]:
        Manager.datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeEnemyHPOverride"] = int(calculate_stat(i, Manager.datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeDefaultEnemyLevel"], "MaxHP")*2.0)
    #Add a bit of defense to the stronger final boss
    for i in ["N1009_Enemy", "N1013_Bael", "N1013_Cat", "N1013_Frog", "N1009_Bael", "N1013_BaelHead", "N1013_Dominique"]:
        for e in ["CON", "MND"]:
            Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] += (Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"] - 45)*2
            if Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] < 60:
                Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] = 60
            if Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] > 80:
                Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] = 80
            Manager.datatable["PB_DT_CharacterParameterMaster"][i][e] += round((Manager.datatable["PB_DT_CharacterParameterMaster"][i][e + "99Enemy"] - 60)/10)
    #Update Gebel's health threshold for the red moon based on his level
    Manager.datatable["PB_DT_CoordinateParameter"]["FakeMoon_ChangeHPThreshold"]["Value"] = int(calculate_stat("N1012", Manager.datatable["PB_DT_CharacterParameterMaster"]["N1012"]["DefaultEnemyLevel"], "MaxHP")*0.15)

def create_log():
    log = {}
    for i in Manager.mod_data["EnemyLocation"]:
        enemy_name = Manager.mod_data["EnemyTranslation"][i]
        log[enemy_name] = {}
        log[enemy_name]["DefaultLevel"]   = Manager.datatable["PB_DT_CharacterParameterMaster"][i]["DefaultEnemyLevel"]
        log[enemy_name]["BloodlessLevel"] = Manager.datatable["PB_DT_CharacterParameterMaster"][i]["BloodlessModeDefaultEnemyLevel"]
        log[enemy_name]["Resistances"] = {}
        for e in stat:
            log[enemy_name]["Resistances"][e] = int(Manager.datatable["PB_DT_CharacterParameterMaster"][i][e])
        for e in second_stat:
            log[enemy_name]["Resistances"][e] = int(Manager.datatable["PB_DT_CharacterParameterMaster"][i][e])
        if i in enemy_replacement:
            if enemy_replacement[i] != i:
                log[enemy_name]["Position"] = Manager.mod_data["EnemyTranslation"][enemy_replacement_invert[i]]
            else:
                log[enemy_name]["Position"] = "Unchanged"
        else:
            log[enemy_name]["Position"] = "Unchanged"
        if i == "N0000":
            break
    return log

def calculate_stat(entry, level, stat_name):
    #Calculate a stat based on the enemy's level in a way nearly identical to how the game calculates it
    #Though sometimes it can be 1 unit off
    return int(((Manager.datatable["PB_DT_CharacterParameterMaster"][entry][stat_name + "99Enemy"] - Manager.datatable["PB_DT_CharacterParameterMaster"][entry][stat_name])/98)*(level-1) + Manager.datatable["PB_DT_CharacterParameterMaster"][entry][stat_name])

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
    
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EffectBeginScale"]    *= 1.9
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EffectEndScale"]      *= 1.9
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EndEffectBeginScale"] *= 1.9
    Manager.datatable["PB_DT_BulletMaster"]["N1013_Screech"]["EndEffectEndScale"]   *= 1.9
    
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
    
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Screech"]["R00"] *= 1.9
    Manager.datatable["PB_DT_CollisionMaster"]["N1013_Screech"]["R01"] *= 1.9
    
    Manager.datatable["PB_DT_DamageMaster"]["N1013_RingLasers"]["STR_Correction"] = 1.0
    Manager.datatable["PB_DT_DamageMaster"]["N1013_RingLasers"]["INT_Correction"] = 1.0
    Manager.datatable["PB_DT_DamageMaster"]["N1013_RingLasers"]["RapidHitTime"]   = 0.2