import ClassManagement
import math
import random

stat_pool = []
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
second_stat = [
    "POI",
    "CUR",
    "STO",
    "SLO"
]
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
original_area_to_progress = {}
area_to_progress = {}
area_to_list = {}

zangetsu_exp = [
    34,
    34,
    0,
    106,
    0,
    178,
    274,
    274,
    394,
    0,
    0,
    538,
    706,
    0,
    898,
    0,
    1114,
    1354,
    1618,
    2218,
    2554,
    0,
    58,
    1906
]

log = []

def init():
    stat_int = -100
    for i in range(int(100/5)*2 + 1):
        for e in range(2**(abs(math.ceil(abs(stat_int)/20)-5))):
            stat_pool.append(stat_int + 0.0)
        stat_int += 5
    ClassManagement.debug("ClassEnemy.init()")

def convert_area_to_progress():
    #General
    for i in range(len(ClassManagement.order_data["Value"]["AreaList"])):
        original_area_to_progress[ClassManagement.original_order_data["Value"]["AreaList"][i]] = i + 1.0
        area_to_progress[ClassManagement.order_data["Value"]["AreaList"][i]] = i + 1
    #Special
    original_area_to_progress["m04GDN(2)"] = (original_area_to_progress["m04GDN"] + original_area_to_progress["m05SAN"])/2
    area_to_progress["m04GDN(2)"] = area_to_progress["m04GDN"]
    original_area_to_progress["m05SAN(2)"] = original_area_to_progress["m06KNG"]
    area_to_progress["m05SAN(2)"] = area_to_progress["m05SAN"]
    original_area_to_progress["m07LIB(2)"] = original_area_to_progress["m06KNG"]
    area_to_progress["m07LIB(2)"] = area_to_progress["m07LIB"]
    original_area_to_progress["m08TWR(2)"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m08TWR(2)"] = area_to_progress["m08TWR"]
    original_area_to_progress["m11UGD(2)"] = (original_area_to_progress["m07LIB"] + original_area_to_progress["m13ARC"])/2
    area_to_progress["m11UGD(2)"] = area_to_progress["m11UGD"]

def convert_area_to_list():
    #Variable
    for i in area:
        list = []
        for e in range(99):
            if e <= 49:
                for o in range(abs(area_to_progress[i] - 19)):
                    list.append(e+1)
            else:
                list.append(e+1)
        area_to_list[i] = list
    #SpecialCases
    area_to_list["m04GDN(2)"] = area_to_list["m04GDN"]
    area_to_list["m05SAN(2)"] = area_to_list["m05SAN"]
    area_to_list["m07LIB(2)"] = area_to_list["m07LIB"]
    area_to_list["m08TWR(2)"] = area_to_list["m08TWR"]
    area_to_list["m11UGD(2)"] = area_to_list["m11UGD"]
    #Minor
    list = []
    for i in range(50):
        list.append(i+1)
    area_to_list["Minor"] = list
    #Intermediate
    list = []
    for e in range(99):
        if e <= 49:
            for o in range(10):
                list.append(e+1)
        else:
            list.append(e+1)
    area_to_list["Intermediate"] = list
    #PreMajor
    list = []
    for e in range(99):
        if e <= 49:
            for o in range(2):
                list.append(e+1)
        else:
            list.append(e+1)
    area_to_list["PreMajor"] = list
    #Major
    list = []
    for i in range(99):
        list.append(i+1)
    area_to_list["Major"] = list

def rename_difficulty(normal, hard, nightmare):
    ClassManagement.system_content["Table"]["SYS_SEN_Difficulty_Normal"] = normal
    ClassManagement.system_content["Table"]["SYS_SEN_Difficulty_Hard"] = hard
    ClassManagement.system_content["Table"]["SYS_SEN_Difficulty_Nightmare"] = nightmare
    ClassManagement.debug("ClassEnemy.rename_difficulty(" + normal + ", " + hard + ", " + nightmare + ")")

def higher_HPMP():
    ClassManagement.character_content[5]["Value"]["MaxHP"] += 300.0
    ClassManagement.character_content[5]["Value"]["MaxMP"] += 150.0
    ClassManagement.character_content[5]["Value"]["MaxHP99Enemy"] += 300.0
    ClassManagement.character_content[5]["Value"]["MaxMP99Enemy"] += 150.0
    ClassManagement.character_content[6]["Value"]["MaxHP"] += 300.0
    ClassManagement.character_content[6]["Value"]["MaxMP"] += 150.0
    ClassManagement.character_content[6]["Value"]["MaxHP99Enemy"] += 300.0
    ClassManagement.character_content[6]["Value"]["MaxMP99Enemy"] += 150.0
    ClassManagement.character_content[10]["Value"]["MaxHP"] += 300.0
    ClassManagement.character_content[10]["Value"]["MaxMP"] += 150.0
    ClassManagement.debug("ClassEnemy.higher_HPMP()")

def no_upgrade_cap():
    ClassManagement.coordinate_content[130]["Value"]["Value"] = 9999.0
    ClassManagement.coordinate_content[131]["Value"]["Value"] = 9999.0
    ClassManagement.coordinate_content[3]["Value"]["Value"] = 999.0
    ClassManagement.debug("ClassEnemy.no_upgrade_cap()")

def lower_HPMP_growth():
    ClassManagement.effect_content[105]["Value"]["Parameter01"] -= 10.0
    ClassManagement.effect_content[106]["Value"]["Parameter01"] -= 5.0
    ClassManagement.coordinate_content[65]["Value"]["Value"] -= 10.0
    ClassManagement.coordinate_content[66]["Value"]["Value"] -= 5.0
    ClassManagement.debug("ClassEnemy.lower_HPMP_growth()")

def zangetsu_growth(nightmare):
    if nightmare:
        ClassManagement.coordinate_content[51]["Value"]["Value"] = 0.0
        ClassManagement.coordinate_content[52]["Value"]["Value"] = 0.0
        ClassManagement.coordinate_content[53]["Value"]["Value"] = 6.2
        ClassManagement.coordinate_content[54]["Value"]["Value"] = 6.0
        ClassManagement.coordinate_content[55]["Value"]["Value"] = 6.0
        ClassManagement.coordinate_content[56]["Value"]["Value"] = 5.8
        ClassManagement.coordinate_content[57]["Value"]["Value"] = 3.0
    else:
        ClassManagement.coordinate_content[53]["Value"]["Value"] = 3.1
        ClassManagement.coordinate_content[54]["Value"]["Value"] = 3.0
        ClassManagement.coordinate_content[55]["Value"]["Value"] = 3.0
        ClassManagement.coordinate_content[56]["Value"]["Value"] = 2.9
        ClassManagement.coordinate_content[57]["Value"]["Value"] = 1.5
    ClassManagement.debug("ClassEnemy.zangetsu_growth(" + str(nightmare) + ")")

def nightmare_damage():
    ClassManagement.coordinate_content[7]["Value"]["Value"] = 3.0
    ClassManagement.coordinate_content[9]["Value"]["Value"] = 3.0
    ClassManagement.coordinate_content[10]["Value"]["Value"] = 3.0
    ClassManagement.debug("ClassEnemy.nightmare_damage()")

def zangetsu_progress():
    #Enemies
    i = 12
    while i <= 137:
        ClassManagement.character_content[i]["Value"]["Experience99Enemy"] = 0
        ClassManagement.character_content[i]["Value"]["Experience"] = 0
        i += 1
    #Bosses
    i = 138
    while i <= 161:
        ClassManagement.character_content[i]["Value"]["Experience99Enemy"] = zangetsu_exp[i-138]
        ClassManagement.character_content[i]["Value"]["Experience"] = zangetsu_exp[i-138]
        i += 1
    #Rest
    i = 162
    while i <= 188:
        ClassManagement.character_content[i]["Value"]["Experience99Enemy"] = 0
        ClassManagement.character_content[i]["Value"]["Experience"] = 0
        i += 1
    ClassManagement.debug("ClassEnemy.zangetsu_progress()")

def zangetsu_no_stats():
    ClassManagement.character_content[6]["Value"]["STR"] = 0.0
    ClassManagement.character_content[6]["Value"]["INT"] = 0.0
    ClassManagement.character_content[6]["Value"]["CON"] = 0.0
    ClassManagement.character_content[6]["Value"]["MND"] = 0.0
    ClassManagement.character_content[6]["Value"]["LUC"] = 0.0
    ClassManagement.character_content[6]["Value"]["STR99Enemy"] = 0.0
    ClassManagement.character_content[6]["Value"]["INT99Enemy"] = 0.0
    ClassManagement.character_content[6]["Value"]["CON99Enemy"] = 0.0
    ClassManagement.character_content[6]["Value"]["MND99Enemy"] = 0.0
    ClassManagement.character_content[6]["Value"]["LUC99Enemy"] = 0.0
    ClassManagement.debug("ClassEnemy.zangetsu_no_stats()")

def brv_speed(play_rate):
    ClassManagement.character_content[159]["Value"]["AnimaionPlayRateNormal"] = ClassManagement.character_content[159]["Value"][play_rate]
    ClassManagement.character_content[161]["Value"]["AnimaionPlayRateNormal"] = ClassManagement.character_content[161]["Value"][play_rate]
    ClassManagement.character_content[177]["Value"]["AnimaionPlayRateNormal"] = ClassManagement.character_content[177]["Value"][play_rate]
    ClassManagement.debug("ClassEnemy.brv_speed(" + play_rate + ")")

def brv_damage(difficulty):
    for i in ClassManagement.attack_content:
        #GettingEnemySTR
        if i["Value"]["Owner"] == "Zangetsu":
            base = int(((ClassManagement.character_content[161]["Value"]["STR99Enemy"] - ClassManagement.character_content[161]["Value"]["STR"])/98)*44 + ClassManagement.character_content[161]["Value"]["STR"])
        elif i["Value"]["Owner"] == "Dominique":
            base = int(((ClassManagement.character_content[159]["Value"]["STR99Enemy"] - ClassManagement.character_content[159]["Value"]["STR"])/98)*44 + ClassManagement.character_content[159]["Value"]["STR"])
        elif i["Value"]["Owner"] == "Miriam":
            base = int(((ClassManagement.character_content[177]["Value"]["STR99Enemy"] - ClassManagement.character_content[177]["Value"]["STR"])/98)*44 + ClassManagement.character_content[177]["Value"]["STR"])
        #CritOnGremory
        if i["Value"]["IsZangetsutoAttack"]:
            critical = 2.5
        else:
            critical = 1.0
        #GettingAttackMultiplierAndAttributes
        multiplier = 1.0
        attribute = []
        if i["Key"] == "N1008_Moon_Attack_01_Burst":
            for e in stat:
                if ClassManagement.damage_content[386]["Value"][e]:
                    attribute.append(e)
        elif i["Key"] == "N1011_ATTACK_EXPLOSION":
            multiplier = (ClassManagement.damage_content[412]["Value"]["STR_Correction"] + ClassManagement.damage_content[419]["Value"]["STR_Correction"])/2
        else:
            for e in ClassManagement.damage_content:
                if i["Key"] in e["Key"]:
                    multiplier = e["Value"]["STR_Correction"]
                    if i["Key"] == e["Key"]:
                        for o in stat:
                            if e["Value"][o]:
                                attribute.append(o)
                        break
            if multiplier == 0.0:
                continue
        #GettingResistances
        andrealphus = 0.0
        bathin = 0.0
        bloodless = 0.0
        gremory = 0.0
        zangetsu = 0.0
        dominique = 0.0
        miriam = 0.0
        for e in attribute:
            andrealphus += 1.0 - ClassManagement.character_content[8]["Value"][e]/100
            bathin += 1.0 - ClassManagement.character_content[9]["Value"][e]/100
            bloodless += 1.0 - ClassManagement.character_content[10]["Value"][e]/100
            gremory += 1.0 - ClassManagement.character_content[11]["Value"][e]/100
            zangetsu += 1.0 - ClassManagement.character_content[161]["Value"][e]/100
            dominique += 1.0 - ClassManagement.character_content[159]["Value"][e]/100
            miriam += 1.0 - ClassManagement.character_content[177]["Value"][e]/100
        if attribute:
            andrealphus /= len(attribute)
            bathin /= len(attribute)
            bloodless /= len(attribute)
            gremory /= len(attribute)
            zangetsu /= len(attribute)
            dominique /= len(attribute)
            miriam /= len(attribute)
        else:
            andrealphus = 1.0
            bathin = 1.0
            bloodless = 1.0
            gremory = 0.75
            zangetsu = 1.0
            dominique = 1.0
            miriam = 1.0
        #Calculating
        if i["Value"]["ChanceAndrealphus"] == 100.0 and i["Value"]["ChanceBathin"] == 100.0 and i["Value"]["ChanceBloodless"] == 100.0 and i["Value"]["ChanceGremory"] == 100.0:
            i["Value"]["VsAndrealphus"] = int((base*multiplier - 40)*andrealphus*difficulty) + 0.0
            i["Value"]["VsBathin"] = int((base*multiplier - 40)*bathin*difficulty) + 0.0
            i["Value"]["VsBloodless"] = int((base*multiplier - 40)*bloodless*difficulty) + 0.0
            i["Value"]["VsGremory"] = int((base*multiplier - 40)*gremory*critical*difficulty) + 0.0
            if i["Value"]["VsAndrealphus"] == 0.0:
                i["Value"]["VsAndrealphus"] = 1.0
            if i["Value"]["VsBathin"] <= 0.0:
                i["Value"]["VsBathin"] = 1.0
            if i["Value"]["VsBloodless"] <= 0.0:
                i["Value"]["VsBloodless"] = 1.0
            if i["Value"]["VsGremory"] <= 0.0:
                i["Value"]["VsGremory"] = 1.0
        if i["Value"]["VsZangetsu"] != 0 and i["Value"]["VsDominique"] != 0 and i["Value"]["VsMiriam"] != 0:
            i["Value"]["VsZangetsu"] = int(i["Value"]["VsZangetsu"]*zangetsu) + 0.0
            i["Value"]["VsDominique"] = int(i["Value"]["VsDominique"]*dominique) + 0.0
            i["Value"]["VsMiriam"] = int(i["Value"]["VsMiriam"]*miriam) + 0.0
            if i["Value"]["VsZangetsu"] <= 0.0:
                i["Value"]["VsZangetsu"] = 1.0
            if i["Value"]["VsDominique"] <= 0.0:
                i["Value"]["VsDominique"] = 1.0
            if i["Value"]["VsMiriam"] <= 0.0:
                i["Value"]["VsMiriam"] = 1.0
    ClassManagement.debug("ClassEnemy.brv_damage(" + str(difficulty) + ")")

def enemy_property(level, resist, map, custom, value):
    convert_area_to_progress()
    convert_area_to_list()
    #All
    i = 12
    while i <= 176:
        if resist:
            rand_stat(i)
        if custom:
            patch_level([value], i)
        elif level:
            check = True
            for e in ClassManagement.enemy_location_data:
                if ClassManagement.character_content[i]["Key"] == e["Key"]:
                    check = False
                    patch_level(area_to_list[e["Value"]["AreaID"]], i)
            if check:
                patch_level([0], i)
        elif map:
            check = True
            for e in ClassManagement.enemy_location_data:
                if ClassManagement.character_content[i]["Key"] == e["Key"]:
                    check = False
                    #Area
                    if e["Value"]["AreaID"] == "Minor":
                        current_area = e["Value"]["NormalModeRooms"][0][:6]
                    elif e["Value"]["AreaID"] == "Intermediate" or "Major" in e["Value"]["AreaID"]:
                        continue
                    else:
                        current_area = e["Value"]["AreaID"]
                    #Level
                    new_level = round(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] + (area_to_progress[current_area] - original_area_to_progress[current_area])*(40/17))
                    if new_level < 1:
                        new_level = 1
                    if new_level > 50:
                        new_level = 50
                    patch_level([new_level], i)
            if check:
                patch_level([0], i)
        create_log(i)
        i += 1
    #Miriam
    if resist:
        rand_stat(177)
    if custom:
        patch_level([value], 177)
    elif level:
        patch_level(area_to_list["Major"], 177)
    create_log(177)
    #Breeder
    if resist:
        rand_stat(185)
        rand_stat(186)
    if custom:
        patch_level([value], 185)
        patch_level([value], 186)
    elif level:
        patch_level(area_to_list["Major"], 185)
        patch_level(area_to_list["Major"], 186)
    create_log(185)
    ClassManagement.debug("ClassEnemy.enemy_property(" + str(level) + ", " + str(resist) + ", " + str(map) + ", " + str(custom) + ", " + str(value) + ")")

def patch_level(array, i):
    #BuerArmor
    if ClassManagement.character_content[i]["Key"] == "N3001_Armor":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = ClassManagement.character_content[38]["Value"]["DefaultEnemyLevel"]
    #Scylla
    elif ClassManagement.character_content[i]["Key"] == "N3098_Guard":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = ClassManagement.character_content[i-2]["Value"]["DefaultEnemyLevel"]
    #Vepar
    elif ClassManagement.character_content[i]["Key"] == "N1001":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        ClassManagement.character_content[i]["Value"]["BloodlessModeEnemyHPOverride"] = int(int(((ClassManagement.character_content[i]["Value"]["MaxHP99Enemy"] - ClassManagement.character_content[i]["Value"]["MaxHP"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["MaxHP"])*2.0) + 0.0
    #Gebel
    elif ClassManagement.character_content[i]["Key"] == "N1012":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        ClassManagement.coordinate_content[140]["Value"]["Value"] = int(int(((ClassManagement.character_content[i]["Value"]["MaxHP99Enemy"] - ClassManagement.character_content[i]["Value"]["MaxHP"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["MaxHP"])*0.15) + 0.0
    #Dom
    elif ClassManagement.character_content[i]["Key"] == "N1009_Enemy":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = abs(random.choice(array) - 100)
    #Bael
    elif ClassManagement.character_content[i]["Key"][0:5] == "N1013" or ClassManagement.character_content[i]["Key"] == "N1009_Bael":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = abs(ClassManagement.character_content[159]["Value"]["DefaultEnemyLevel"] - 100)
    #Duplicate
    elif ClassManagement.character_content[i]["Key"][0:5] == ClassManagement.character_content[i-1]["Key"][0:5] and ClassManagement.character_content[i]["Key"] != "N1011_STRONG" or ClassManagement.character_content[i]["Key"][0:5] == "N3125":
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = ClassManagement.character_content[i-1]["Value"]["DefaultEnemyLevel"]
        ClassManagement.character_content[i]["Value"]["BloodlessModeEnemyHPOverride"] = ClassManagement.character_content[i-1]["Value"]["BloodlessModeEnemyHPOverride"]
    #Other
    else:
        ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] = random.choice(array)
    stat_scale(i)
    
    ClassManagement.character_content[i]["Value"]["HardEnemyLevel"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]
    ClassManagement.character_content[i]["Value"]["NightmareEnemyLevel"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]
    ClassManagement.character_content[i]["Value"]["BloodlessModeDefaultEnemyLevel"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]
    ClassManagement.character_content[i]["Value"]["BloodlessModeHardEnemyLevel"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]
    ClassManagement.character_content[i]["Value"]["BloodlessModeNightmareEnemyLevel"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]

def stat_scale(i):
    for e in second_stat:
        stat_num = ClassManagement.character_content[i]["Value"][e]
        #BossStoneCheck
        if e == "STO" and ClassManagement.character_content[i]["Value"]["StoneType"] == "EPBStoneType::Boss":
            continue
        #Gain
        if ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] > ClassManagement.character_content[i]["Value"]["HardEnemyLevel"]:
            stat_num += 25.0
        if ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] > ClassManagement.character_content[i]["Value"]["HardEnemyLevel"] + ((99 - ClassManagement.character_content[i]["Value"]["HardEnemyLevel"]) * 0.5):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        if e == "STO" and stat_num > 99.9:
            stat_num = 99.9
        #Immunity
        if ClassManagement.character_content[i]["Value"]["POI"] == 100.0 and ClassManagement.character_content[i]["Value"]["CUR"] == 100.0 and ClassManagement.character_content[i]["Value"]["STO"] >= 99.0 and ClassManagement.character_content[i]["Value"]["SLO"] == 100.0:
            continue
        #Loss
        if ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] < ClassManagement.character_content[i]["Value"]["HardEnemyLevel"]:
            stat_num = math.ceil(stat_num - 25.0)
        if ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"] < ClassManagement.character_content[i]["Value"]["HardEnemyLevel"] * 0.5:
            stat_num -= 25.0
        if stat_num < 0.0:
            stat_num = 0.0
        ClassManagement.character_content[i]["Value"][e] = stat_num

def rand_stat(i):
    #Immunity
    if ClassManagement.character_content[i]["Value"]["ZAN"] == 100.0 and ClassManagement.character_content[i]["Value"]["DAG"] == 100.0 and ClassManagement.character_content[i]["Value"]["TOT"] == 100.0 and ClassManagement.character_content[i]["Value"]["FLA"] == 100.0 and ClassManagement.character_content[i]["Value"]["ICE"] == 100.0 and ClassManagement.character_content[i]["Value"]["LIG"] == 100.0 and ClassManagement.character_content[i]["Value"]["HOL"] == 100.0 and ClassManagement.character_content[i]["Value"]["DAR"] == 100.0:
        return
    #WeakPoints
    if ClassManagement.character_content[i]["Key"] == "N3015_HEAD" or ClassManagement.character_content[i]["Key"] == "N1001_HEAD" or ClassManagement.character_content[i]["Key"] == "N2001_HEAD":
        for e in stat:
            if ClassManagement.character_content[i-1]["Value"][e] < -20:
                ClassManagement.character_content[i]["Value"][e] = -100
            else:
                ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[i-1]["Value"][e]-80
    #BuerArmor
    elif ClassManagement.character_content[i]["Key"] == "N3001_Armor":
        for e in stat:
            ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[38]["Value"][e]
    #Vepar
    elif ClassManagement.character_content[i]["Key"] == "N1001_Tentacle":
        for e in stat:
            ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[i-2]["Value"][e]
    #StrongParts
    elif ClassManagement.character_content[i]["Key"] == "N3108_GUARD" or ClassManagement.character_content[i]["Key"] == "N2001_ARMOR":
        for e in stat:
            if ClassManagement.character_content[i-2]["Value"][e] > 20:
                    ClassManagement.character_content[i]["Value"][e] = 100
            else:
                ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[i-2]["Value"][e]+80
    #Bael
    elif ClassManagement.character_content[i]["Key"][0:5] == "N1013" and ClassManagement.character_content[i]["Key"] != "N1013_Bael" or ClassManagement.character_content[i]["Key"] == "N1009_Bael":
        for e in stat:
            ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[168]["Value"][e]
    #Duplicate
    elif ClassManagement.character_content[i]["Key"][0:5] == ClassManagement.character_content[i-1]["Key"][0:5] and ClassManagement.character_content[i]["Key"] != "N1011_STRONG" or ClassManagement.character_content[i]["Key"][0:5] == "N3125":
        for e in stat:
            ClassManagement.character_content[i]["Value"][e] = ClassManagement.character_content[i-1]["Value"][e]
    #Other
    else:
        for e in stat:
            ClassManagement.character_content[i]["Value"][e] = random.choice(stat_pool)

def create_log(i):
    try:
        log_data = {}
        log_data["Key"] = ClassManagement.enemy_translation["Value"][ClassManagement.character_content[i]["Key"]]
    except KeyError:
        return
    log_data["Value"] = {}
    log_data["Value"]["Level"] = ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]
    log_data["Value"]["MainStats"] = {}
    log_data["Value"]["MainStats"]["HP"] = int(((ClassManagement.character_content[i]["Value"]["MaxHP99Enemy"] - ClassManagement.character_content[i]["Value"]["MaxHP"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["MaxHP"])
    log_data["Value"]["MainStats"]["STR"] = int(((ClassManagement.character_content[i]["Value"]["STR99Enemy"] - ClassManagement.character_content[i]["Value"]["STR"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["STR"])
    log_data["Value"]["MainStats"]["INT"] = int(((ClassManagement.character_content[i]["Value"]["INT99Enemy"] - ClassManagement.character_content[i]["Value"]["INT"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["INT"])
    log_data["Value"]["MainStats"]["CON"] = int(((ClassManagement.character_content[i]["Value"]["CON99Enemy"] - ClassManagement.character_content[i]["Value"]["CON"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["CON"])
    log_data["Value"]["MainStats"]["MND"] = int(((ClassManagement.character_content[i]["Value"]["MND99Enemy"] - ClassManagement.character_content[i]["Value"]["MND"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["MND"])
    log_data["Value"]["MainStats"]["LUC"] = int(((ClassManagement.character_content[i]["Value"]["LUC99Enemy"] - ClassManagement.character_content[i]["Value"]["LUC"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["LUC"])
    log_data["Value"]["MainStats"]["EXP"] = int(((ClassManagement.character_content[i]["Value"]["Experience99Enemy"] - ClassManagement.character_content[i]["Value"]["Experience"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["Experience"])
    log_data["Value"]["MainStats"]["AP"] = int(((ClassManagement.character_content[i]["Value"]["ArtsExperience99Enemy"] - ClassManagement.character_content[i]["Value"]["ArtsExperience"])/98)*(ClassManagement.character_content[i]["Value"]["DefaultEnemyLevel"]-1) + ClassManagement.character_content[i]["Value"]["ArtsExperience"])
    log_data["Value"]["Resistances"] = {}
    for e in stat:
        log_data["Value"]["Resistances"][e] = int(ClassManagement.character_content[i]["Value"][e])
    for e in second_stat:
        log_data["Value"]["Resistances"][e] = int(ClassManagement.character_content[i]["Value"][e])
    log.append(log_data)

def get_log():
    return log

def normal_bomber():
    ClassManagement.bullet_content[559]["Value"]["BeginEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[559]["Value"]["BeginEffectEndScale"] /= 2.0
    
    ClassManagement.collision_content[537]["Value"]["R00"] /= 2.0
    ClassManagement.collision_content[537]["Value"]["R01"] /= 2.0
    
    ClassManagement.debug("ClassEnemy.normal_bomber()")

def normal_milli():
    ClassManagement.bullet_content[751]["Value"]["BeginEffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[751]["Value"]["BeginEffectEndScale"] /= 1.5
    
    ClassManagement.collision_content[681]["Value"]["R00"] /= 1.5
    ClassManagement.collision_content[681]["Value"]["R01"] /= 1.5
    
    ClassManagement.debug("ClassEnemy.normal_milli()")

def normal_bael():
    #LightRay
    ClassManagement.ballistic_content[73]["Value"]["InitialSpeed"] /= 2.0
    #TracerRay
    ClassManagement.ballistic_content[317]["Value"]["InitialSpeed"] /= 6.0
    #RingLasers
    ClassManagement.ballistic_content[320]["Value"]["InitialSpeed"] /= 9.0
    
    #FlameSkull
    ClassManagement.bullet_content[783]["Value"]["EffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[783]["Value"]["EffectEndScale"] /= 2.5
    ClassManagement.bullet_content[783]["Value"]["BeginEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[783]["Value"]["BeginEffectEndScale"] /= 2.5
    ClassManagement.bullet_content[783]["Value"]["EndEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[783]["Value"]["EndEffectEndScale"] /= 2.5
    
    #Bubbles
    ClassManagement.bullet_content[787]["Value"]["EffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[787]["Value"]["EffectEndScale"] /= 1.5
    ClassManagement.bullet_content[787]["Value"]["BeginEffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[787]["Value"]["BeginEffectEndScale"] /= 1.5
    ClassManagement.bullet_content[787]["Value"]["EndEffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[787]["Value"]["EndEffectEndScale"] /= 1.5
    
    #RingLasers
    ClassManagement.bullet_content[789]["Value"]["EffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[789]["Value"]["EffectEndScale"] /= 2.0
    ClassManagement.bullet_content[789]["Value"]["BeginEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[789]["Value"]["BeginEffectEndScale"] /= 2.0
    ClassManagement.bullet_content[789]["Value"]["EndEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[789]["Value"]["EndEffectEndScale"] /= 2.0
    
    #Screech
    ClassManagement.bullet_content[790]["Value"]["EffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[790]["Value"]["EffectEndScale"] /= 2.0
    ClassManagement.bullet_content[790]["Value"]["EndEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[790]["Value"]["EndEffectEndScale"] /= 2.0
    
    #FlameSkullExplosion
    ClassManagement.bullet_content[792]["Value"]["EffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[792]["Value"]["EffectEndScale"] /= 2.5
    ClassManagement.bullet_content[792]["Value"]["BeginEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[792]["Value"]["BeginEffectEndScale"] /= 2.5
    ClassManagement.bullet_content[792]["Value"]["EndEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[792]["Value"]["EndEffectEndScale"] /= 2.5
    
    #FlameSkullDestroyed
    ClassManagement.bullet_content[793]["Value"]["EffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[793]["Value"]["EffectEndScale"] /= 2.5
    ClassManagement.bullet_content[793]["Value"]["BeginEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[793]["Value"]["BeginEffectEndScale"] /= 2.5
    ClassManagement.bullet_content[793]["Value"]["EndEffectBeginScale"] /= 2.5
    ClassManagement.bullet_content[793]["Value"]["EndEffectEndScale"] /= 2.5
    
    #BubblesDestroyed
    ClassManagement.bullet_content[794]["Value"]["EffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[794]["Value"]["EffectEndScale"] /= 1.5
    ClassManagement.bullet_content[794]["Value"]["BeginEffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[794]["Value"]["BeginEffectEndScale"] /= 1.5
    ClassManagement.bullet_content[794]["Value"]["EndEffectBeginScale"] /= 1.5
    ClassManagement.bullet_content[794]["Value"]["EndEffectEndScale"] /= 1.5
    
    #RingLasersImpact
    ClassManagement.bullet_content[797]["Value"]["EffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[797]["Value"]["EffectEndScale"] /= 2.0
    ClassManagement.bullet_content[797]["Value"]["BeginEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[797]["Value"]["BeginEffectEndScale"] /= 2.0
    ClassManagement.bullet_content[797]["Value"]["EndEffectBeginScale"] /= 2.0
    ClassManagement.bullet_content[797]["Value"]["EndEffectEndScale"] /= 2.0
    
    #FlameSkull
    ClassManagement.collision_content[738]["Value"]["R00"] /= 2.5
    ClassManagement.collision_content[738]["Value"]["R01"] /= 2.5
    
    #FlameSkullExplosion
    ClassManagement.collision_content[739]["Value"]["R00"] /= 2.5
    ClassManagement.collision_content[739]["Value"]["R01"] /= 2.5
    
    #Bubbles
    ClassManagement.collision_content[743]["Value"]["R00"] /= 1.5
    ClassManagement.collision_content[743]["Value"]["R01"] /= 1.5
    
    #RingLasers
    ClassManagement.collision_content[745]["Value"]["R00"] /= 2.0
    ClassManagement.collision_content[745]["Value"]["R01"] /= 2.0
    
    #Screech
    ClassManagement.collision_content[746]["Value"]["R00"] /= 2.0
    ClassManagement.collision_content[746]["Value"]["R01"] /= 2.0
    
    ClassManagement.debug("ClassEnemy.normal_bael()")