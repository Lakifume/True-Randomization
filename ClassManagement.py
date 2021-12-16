import os
import shutil
import json

def open_content():
    global armor_content
    with open("Serializer\\Json\\PB_DT_ArmorMaster.json", "r") as file_reader:
        armor_content = json.load(file_reader)
    
    global ballistic_content
    with open("Serializer\\Json\\PB_DT_BallisticMaster.json", "r") as file_reader:
        ballistic_content = json.load(file_reader)
    
    global book_content
    with open("Serializer\\Json\\PB_DT_BookMaster.json", "r") as file_reader:
        book_content = json.load(file_reader)
    
    global attack_content
    with open("Serializer\\Json\\PB_DT_BRVAttackDamage.json", "r") as file_reader:
        attack_content = json.load(file_reader)
    
    global bullet_content
    with open("Serializer\\Json\\PB_DT_BulletMaster.json", "r") as file_reader:
        bullet_content = json.load(file_reader)
    
    global character_content
    with open("Serializer\\Json\\PB_DT_CharacterParameterMaster.json", "r") as file_reader:
        character_content = json.load(file_reader)
    
    global collision_content
    with open("Serializer\\Json\\PB_DT_CollisionMaster.json", "r") as file_reader:
        collision_content = json.load(file_reader)
    
    global coordinate_content
    with open("Serializer\\Json\\PB_DT_CoordinateParameter.json", "r") as file_reader:
        coordinate_content = json.load(file_reader)
    
    global craft_content
    with open("Serializer\\Json\\PB_DT_CraftMaster.json", "r") as file_reader:
        craft_content = json.load(file_reader)
    
    global damage_content
    with open("Serializer\\Json\\PB_DT_DamageMaster.json", "r") as file_reader:
        damage_content = json.load(file_reader)
    
    global dialogue_content
    with open("Serializer\\Json\\PB_DT_DialogueTableItems.json", "r") as file_reader:
        dialogue_content = json.load(file_reader)
    
    global drop_content
    with open("Serializer\\Json\\PB_DT_DropRateMaster.json", "r") as file_reader:
        drop_content = json.load(file_reader)
    
    global item_content
    with open("Serializer\\Json\\PB_DT_ItemMaster.json", "r") as file_reader:
        item_content = json.load(file_reader)
    
    global quest_content
    with open("Serializer\\Json\\PB_DT_QuestMaster.json", "r") as file_reader:
        quest_content = json.load(file_reader)
    
    global shard_content
    with open("Serializer\\Json\\PB_DT_ShardMaster.json", "r") as file_reader:
        shard_content = json.load(file_reader)
    
    global effect_content
    with open("Serializer\\Json\\PB_DT_SpecialEffectDefinitionMaster.json", "r") as file_reader:
        effect_content = json.load(file_reader)
    
    global weapon_content
    with open("Serializer\\Json\\PB_DT_WeaponMaster.json", "r") as file_reader:
        weapon_content = json.load(file_reader)
    
    global master_content
    with open("Serializer\\Json\\PBMasterStringTable.json", "r") as file_reader:
        master_content = json.load(file_reader)
    
    global scenario_content
    with open("Serializer\\Json\\PBScenarioStringTable.json", "r") as file_reader:
        scenario_content = json.load(file_reader)
    
    global system_content
    with open("Serializer\\Json\\PBSystemStringTable.json", "r") as file_reader:
        system_content = json.load(file_reader)
    
    global room_content
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.json", "r") as file_reader:
        room_content = json.load(file_reader)
    debug("ClassManagement.open_content()")
    
def open_data():
    global bloodless_ability_data
    with open("Data\\Constant\\BloodlessAbility.json", "r") as file_reader:
        bloodless_ability_data = json.load(file_reader)
    
    global bloodless_upgrade_data
    with open("Data\\Constant\\BloodlessUpgrade.json", "r") as file_reader:
        bloodless_upgrade_data = json.load(file_reader)
    
    global enemy_drop_data
    with open("Data\\Constant\\EnemyDrop.json", "r") as file_reader:
        enemy_drop_data = json.load(file_reader)
    
    global enemy_location_data
    with open("Data\\Constant\\EnemyLocation.json", "r") as file_reader:
        enemy_location_data = json.load(file_reader)
    
    global item_drop_data
    with open("Data\\Constant\\ItemDrop.json", "r") as file_reader:
        item_drop_data = json.load(file_reader)
    
    global quest_requirement_data
    with open("Data\\Constant\\QuestRequirement.json", "r") as file_reader:
        quest_requirement_data = json.load(file_reader)
    
    global seed_conversion_data
    with open("Data\\Constant\\SeedConversion.json", "r") as file_reader:
        seed_conversion_data = json.load(file_reader)
    
    global shard_drop_data
    with open("Data\\Constant\\ShardDrop.json", "r") as file_reader:
        shard_drop_data = json.load(file_reader)
    
    global logic_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.logic", "r") as file_reader:
        logic_data = json.load(file_reader)
    
    global order_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.order", "r") as file_reader:
        order_data = json.load(file_reader)
    
    global original_order_data
    with open("MapEdit\\Data\\RoomMaster\\PB_DT_RoomMaster.order", "r") as file_reader:
        original_order_data = json.load(file_reader)
    debug("ClassManagement.open_data()")
    
def open_translation():
    global bloodless_translation
    with open("Data\\Translation\\BloodlessTranslation.json", "r") as file_reader:
        bloodless_translation = json.load(file_reader)
    
    global enemy_translation
    with open("Data\\Translation\\EnemyTranslation.json", "r") as file_reader:
        enemy_translation = json.load(file_reader)
    
    global item_translation
    with open("Data\\Translation\\ItemTranslation.json", "r") as file_reader:
        item_translation = json.load(file_reader)
    
    global shard_translation
    with open("Data\\Translation\\ShardTranslation.json", "r") as file_reader:
        shard_translation = json.load(file_reader)
    debug("ClassManagement.open_translation()")

def load_custom_map(path):
    global room_content
    with open(path, "r") as file_reader:
        room_content = json.load(file_reader)
    #UndergroundBigRoomsInitialFix
    for i in range(len(room_content[295]["Value"]["NoTraverse"])):
        room_content[295]["Value"]["NoTraverse"][i] += room_content[295]["Value"]["AreaWidthSize"]*2
    for i in range(len(room_content[313]["Value"]["NoTraverse"])):
        room_content[313]["Value"]["NoTraverse"][i] += room_content[313]["Value"]["AreaWidthSize"]*3
    #UndergroundBigRoomsNegativeOffset
    if room_content[295]["Value"]["OffsetZ"] < 0:
        multiplier = abs(int(room_content[295]["Value"]["OffsetZ"]/7.2)) - 1
        if multiplier > room_content[295]["Value"]["AreaHeightSize"] - 1:
            multiplier = room_content[295]["Value"]["AreaHeightSize"] - 1
        for i in range(len(room_content[295]["Value"]["NoTraverse"])):
            room_content[295]["Value"]["NoTraverse"][i] -= room_content[295]["Value"]["AreaWidthSize"]*multiplier
    if room_content[313]["Value"]["OffsetZ"] < 0:
        multiplier = abs(int(room_content[313]["Value"]["OffsetZ"]/7.2)) - 1
        if multiplier > room_content[313]["Value"]["AreaHeightSize"] - 1:
            multiplier = room_content[313]["Value"]["AreaHeightSize"] - 1
        for i in range(len(room_content[313]["Value"]["NoTraverse"])):
            room_content[313]["Value"]["NoTraverse"][i] -= room_content[313]["Value"]["AreaWidthSize"]*multiplier
    #GlobalMapDisplayFix
    for i in room_content:
        if i["Value"]["OffsetX"] < 201.6:
            i["Value"]["AreaID"] = "EAreaID::m01SIP"
        elif i["Value"]["OffsetX"] + i["Value"]["AreaWidthSize"]*12.6 > 1096.2:
            i["Value"]["AreaID"] = "EAreaID::m13ARC"
        else:
            i["Value"]["AreaID"] = "EAreaID::m03ENT"
    debug("ClassManagement.load_custom_map(" + path + ")")

def load_custom_logic(path):
    global logic_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".logic"):
        with open(name + ".logic", "r") as file_reader:
            logic_data = json.load(file_reader)
    debug("ClassManagement.load_custom_logic(" + path + ")")

def load_custom_order(path):
    global order_data
    name, extension = os.path.splitext(path)
    if os.path.isfile(name + ".order"):
        with open(name + ".order", "r") as file_reader:
            order_data = json.load(file_reader)
    debug("ClassManagement.load_custom_order(" + path + ")")

def create_log(path):
    name, extension = os.path.splitext(path)
    global log_data
    log_data = {}
    log_data["Key"] = "Map"
    log_data["Value"] = {}
    log_data["Value"]["FileName"] = name.split("\\")[-1]
    debug("ClassManagement.create_log(" + path + ")")

def write_log(filename, filepath, log, ascii):
    with open(filepath + "\\" + filename + ".json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=ascii, indent=2))
    debug("ClassManagement.write_log(" + filename + ", " + filepath + ", " + "[log]" + ", " + str(ascii) + ")")

def write_json(filename, filepath, content, ascii):
    with open("Serializer\\" + filename + ".json", "w") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=ascii, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    if filename == "PB_DT_RoomMaster":
        os.system("cmd /c UAsset2Json.exe -tobin -force " + filename + ".json")
    else:
        os.system("cmd /c UAsset2Json.exe -tobin " + filename + ".json")
    os.chdir(root)
    shutil.move("Serializer\\" + filename + ".bin", "UnrealPak\\Mod\\BloodstainedRotN\\" + filepath + "\\" + filename + ".uasset")
    os.remove("Serializer\\" + filename + ".json")
    debug("ClassManagement.write_patched_json(" + filename + ", " + filepath + ", [content], " + str(ascii) + ")")

def write_miriam_candle():
    print("mXXXXX_XXX_Gimmick.umap")
    i = 627
    while i <= 629:
        candle_process(drop_content[i]["Value"]["ShardId"], drop_content[i]["Key"].split("_")[0])
        i += 1
    print("Done")
    debug("ClassManagement.write_miriam_candle()")

def write_bloodless_candle(datatable):
    #Start
    print("mXXXXX_XXX_Gimmick.umap")
    tower_check = 0
    for i in datatable:
        #RoomToFile
        file_name = i["Value"]["RoomId"].replace(")", "").split("(")[0] + "_Gimmick"
        #TowerCheck
        if i["Value"]["RoomId"] == "m08TWR_019":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_BLOOD_STEAL"
        elif i["Value"]["RoomId"] == "m08TWR_019(2)":
            search = "EPBBloodlessAbilityType::BLD_ABILITY_INT_UP"
        else:
            search = "EPBBloodlessAbilityType::"
        #ReadJson
        if "m08TWR_019" in file_name and tower_check == 1:
            with open("UAssetGUI\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        else:
            with open("UAssetGUI\\Json\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
                content = json.load(file_reader)
        #PatchJson
        for e in content["Exports"]:
            try:
                if search in e["Data"][1]["Value"]:
                    e["Data"][1]["Value"] = "EPBBloodlessAbilityType::" + i["Key"]
            except TypeError:
                continue
            except IndexError:
                continue
        for e in range(len(content["NameMap"])):
            if search in content["NameMap"][e]:
                content["NameMap"][e] = "EPBBloodlessAbilityType::" + i["Key"][:-3]
        #WriteJson
        with open("UAssetGUI\\" + file_name + ".json", "w") as file_writer:
            file_writer.write(json.dumps(content))
        #UAssetGUI
        if not ("m08TWR_019" in file_name and tower_check == 0):
            #CommandFromJson
            root = os.getcwd()
            os.chdir("UAssetGUI")
            os.system("cmd /c UAssetGUI.exe fromjson " + file_name + ".json " + file_name + ".umap")
            os.chdir(root)
            #Move
            shutil.move("UAssetGUI\\" + file_name + ".umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name + ".umap")
            #Delete
            os.remove("UAssetGUI\\" + file_name + ".json")
        #TowerCheck
        if "m08TWR_019" in file_name:
            tower_check += 1
    #Done
    print("Done")
    debug("ClassManagement.write_bloodless_candle([datatable])")

def candle_process(shard, candle):
    for i in enemy_location_data:
        if i["Key"] == candle:
            filelist = i["Value"]["NormalModeRooms"]
    for i in shard_content:
        if i["Key"] == candle:
            candle_type = i["Value"]["ShardType"]
        if i["Key"] == shard:
            shard_type = i["Value"]["ShardType"]
    for i in filelist:
        file_name = i + "_Gimmick"
        #ReadJson
        with open("UAssetGUI\\Json\\" + file_name + ".json", "r", encoding="utf-8") as file_reader:
            content = json.load(file_reader)
        #PatchJson
        for e in content["Exports"]:
            try:
                if candle in e["Data"][45]["Value"]:
                    e["Data"][45]["Value"] = shard + "(0)"
            except TypeError:
                continue
            except IndexError:
                continue
        for e in range(len(content["NameMap"])):
            if content["NameMap"][e] == candle:
                content["NameMap"][e] = shard
            if content["NameMap"][e] == candle_type:
                content["NameMap"][e] = shard_type
        #WriteJson
        with open("UAssetGUI\\" + file_name + ".json", "w") as file_writer:
            file_writer.write(json.dumps(content))
        #CommandFromJson
        root = os.getcwd()
        os.chdir("UAssetGUI")
        os.system("cmd /c UAssetGUI.exe fromjson " + file_name + ".json " + file_name + ".umap")
        os.chdir(root)
        #Move
        shutil.move("UAssetGUI\\" + file_name + ".umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT" + file_name[1:3] + "_" + file_name[3:6] + "\\Level\\" + file_name + ".umap")
        #Delete
        os.remove("UAssetGUI\\" + file_name + ".json")

def convert_umap_to_json():
    for i in os.listdir("UAssetGUI\\Umap"):
        shutil.copyfile("UAssetGUI\\Umap\\" + i, "UAssetGUI\\" + i)
        
        root = os.getcwd()
        os.chdir("UAssetGUI")
        os.system("cmd /c UAssetGUI.exe tojson " + i + " " + i[:-5] + ".json 514")
        os.chdir(root)
        
        shutil.move("UAssetGUI\\" + i[:-5] + ".json", "UAssetGUI\\Json\\" + i[:-5] + ".json")
        os.remove("UAssetGUI\\" + i)

def copy_file(filename, extension, source, destination):
    shutil.copyfile(source + "\\" + filename + "." + extension, "UnrealPak\\Mod\\BloodstainedRotN\\" + destination + "\\" + filename + "." + extension)
    debug("ClassManagement.copy_file(" + filename + ", " + extension + ", " + source + ", " + destination + ")")

def debug(line):
    with open("SpoilerLog\\~debug.txt", "a") as file:
        file.write(line + "\n")