import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Room
import Graphic
import Sound
import Bloodless
import Utility

from PySide6.QtCore import*
from PySide6.QtGui import*
from PySide6.QtWidgets import*

import os
import sys
import shutil
import copy
import json
import glob
import random
import zipfile
import requests
import subprocess
import configparser
import psutil

script_name, script_extension = os.path.splitext(os.path.basename(__file__))

item_color    = "#ff8080"
shop_color    = "#ffff80"
library_color = "#bf80ff"
shard_color   = "#80ffff"
equip_color   = "#80ff80"
enemy_color   = "#80bfff"
map_color     = "#ffbf80"
graphic_color = "#80ffbf"
sound_color   = "#ff80ff"
extra_color   = "#ff80bf"

main_setting_length = 6
sub_setting_length = 6
main_widget_to_setting = {}
sub_widget_to_setting = {}
spin_index_to_shift = {1: 0, 2: 2, 3: 1}
shift_to_spin_index = {value: key for key, value in spin_index_to_shift.items()}
    
map_num = len(glob.glob("MapEdit\\Custom\\*.json"))

preset_to_bytes = {
    "Empty": 0x000000,
    "Trial": 0x7807FF,
    "Race":  0x3806EF,
    "Meme":  0x7F3AAF,
    "Risk":  0x7FFFFF,
    "Blood": 0xB80001
}
bytes_to_preset = {value: key for key, value in preset_to_bytes.items()}

cheats = {
    "BIGTOSS": Manager.set_bigtoss_mode
}

modified_files = {
    "DataTable": {
        "Files": [
            "PB_DT_AmmunitionMaster",
            "PB_DT_ArchiveEnemyMaster",
            "PB_DT_ArmorMaster",
            "PB_DT_ArtsCommandMaster",
            "PB_DT_BallisticMaster",
            "PB_DT_BloodlessAbilityData",
            "PB_DT_BookMaster",
            "PB_DT_BRVAttackDamage",
            "PB_DT_BRVCharacterParameters",
            "PB_DT_BulletMaster",
            "PB_DT_CharacterMaster",
            "PB_DT_CharacterParameterMaster",
            "PB_DT_CharaUniqueParameterMaster",
            "PB_DT_CollisionMaster",
            "PB_DT_ConsumableMaster",
            "PB_DT_CoordinateParameter",
            "PB_DT_CraftMaster",
            "PB_DT_DamageMaster",
            "PB_DT_DialogueTableItems",
            "PB_DT_DialogueTextMaster",
            "PB_DT_DropRateMaster",
            "PB_DT_EnchantParameterType",
            "PB_DT_EventFlagMaster",
            "PB_DT_GimmickFlagMaster",
            "PB_DT_HairSalonOldDefaults",
            "PB_DT_ItemMaster",
            "PB_DT_QuestMaster",
            "PB_DT_RoomMaster",
            "PB_DT_ShardMaster",
            "PB_DT_SoundMaster",
            "PB_DT_SpecialEffectDefinitionMaster",
            "PB_DT_SpecialEffectGroupMaster",
            "PB_DT_SpecialEffectMaster",
            "PB_DT_WeaponMaster"
        ]
    },
    "StringTable": {
        "Files": [
            "PBMasterStringTable",
            "PBScenarioStringTable",
            "PBSystemStringTable"
        ]
    },
    "Texture": {
        "Files": [
            "T_N3127_Body_Color",
            "T_N3127_Uni_Color",
            "m51_EBT_BG",
            "m51_EBT_BG_01",
            "m51_EBT_Block",
            "m51_EBT_Block_00",
            "m51_EBT_Block_01",
            "m51_EBT_Door",
            "time_shard_diffuse"
        ]
    },
    "UI": {
        "Files": [
            "WindowMinimap02",
            "icon",
            "ui_icon_pickup_dagger",
            "ui_icon_pickup_timeShard",
            "ui_icon_results_dagger",
            "ui_icon_results_timeShard"
        ]
    },
    "Blueprint": {
        "Files": [
            "PBExtraModeInfo_BP"
        ]
    }
}

#Config

config = configparser.ConfigParser()
config.optionxform = str
config.read("Data\\config.ini")

def writing():
    with open("Data\\config.ini", "w") as file_writer:
        config.write(file_writer)

def writing_and_exit():
    writing()
    sys.exit()

#Threads

class Signaller(QObject):
    progress = Signal(int)
    finished = Signal()
    error    = Signal()

class Generate(QThread):
    def __init__(self, progress_bar, seed, map, start_items):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.seed = seed
        self.map = map
        self.start_items = start_items
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit()
            raise

    def process(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Check IGA DLC
        
        if len(glob.glob(config.get("Misc", "sGamePath") + "\\*.pak")) < 2:
            for file in list(Manager.file_to_path):
                if "DLC_0002" in Manager.file_to_path[file]:
                    del Manager.file_to_path[file]
                    del Manager.file_to_type[file]
        
        #Initialize directories
        
        #Mod
        if os.path.isdir(Manager.mod_dir):
            shutil.rmtree(Manager.mod_dir)
        for directory in list(Manager.file_to_path.values()):
            if not os.path.isdir(Manager.mod_dir + "\\" + directory):
                os.makedirs(Manager.mod_dir + "\\" + directory)
        if not os.path.isdir(Manager.mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync"):
            os.makedirs(Manager.mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync")
        
        #Logs
        if os.path.isdir("SpoilerLog"):
            shutil.rmtree("SpoilerLog")
        os.makedirs("SpoilerLog")
        
        #Open files
        
        self.progress_bar.setLabelText("Loading data...")
        
        Manager.init()
        Manager.load_game_data()
        Manager.load_constant()
        current += 1
        self.signaller.progress.emit(current)
        
        #Simplify data
        
        self.progress_bar.setLabelText("Processing data...")
        
        Manager.table_complex_to_simple()
        current += 1
        self.signaller.progress.emit(current)
        
        self.progress_bar.setLabelText("Editing data...")
        
        #Init classes
        
        Item.init()
        Shop.init()
        Library.init()
        Shard.init()
        Equipment.init()
        Enemy.init()
        Room.init()
        Graphic.init()
        Sound.init()
        Bloodless.init()
        Utility.init()
        
        #Apply parameters
        
        Item.set_logic_complexity(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        Item.set_shop_event_wheight(config.getint("ItemRandomization", "iShopPoolWheight"))
        Shop.set_shop_price_wheight(config.getint("ShopRandomization", "iItemCostAndSellingPriceWheight"))
        Library.set_requirement_wheight(config.getint("LibraryRandomization", "iMapRequirementsWheight"))
        Shard.set_shard_power_wheight(config.getint("ShardRandomization", "iShardPowerAndMagicCostWheight"))
        Equipment.set_global_stat_wheight(config.getint("EquipmentRandomization", "iGlobalGearStatsWheight"))
        Enemy.set_enemy_level_wheight(config.getint("EnemyRandomization", "iEnemyLevelsWheight"))
        Enemy.set_boss_level_wheight(config.getint("EnemyRandomization", "iBossLevelsWheight"))
        Enemy.set_enemy_tolerance_wheight(config.getint("EnemyRandomization", "iEnemyTolerancesWheight"))
        Enemy.set_boss_tolerance_wheight(config.getint("EnemyRandomization", "iBossTolerancesWheight"))
        Sound.set_voice_language(config.getint("SoundRandomization", "iDialoguesLanguage"))
        Bloodless.set_logic_complexity(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
        
        #Apply tweaks
        
        Manager.apply_default_tweaks()
        Shard.set_default_shard_power()
        Enemy.get_original_enemy_stats()
        
        #Apply cheats
        
        if type(self.seed) is str:
            for code in cheats:
                if code in self.seed:
                    random.seed(self.seed)
                    cheats[code]()
        
        #Map
        
        random.seed(self.seed)
        if self.map:
            pass
        elif config.getboolean("MapRandomization", "bRoomLayout"):
            if glob.glob("MapEdit\\Custom\\*.json"):
                self.map = random.choice(glob.glob("MapEdit\\Custom\\*.json"))
            else:
                self.map = ""
        else:
            self.map = ""
        Manager.load_map(self.map)
        Room.get_map_info()
        Room.update_any_map()
        
        #Hue
        
        random.seed(self.seed)
        miriam_color   = random.choice(os.listdir("Data\\Texture\\Miriam"))
        zangetsu_color = random.choice(os.listdir("Data\\Texture\\Zangetsu"))
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            Graphic.update_default_outfit_hsv(miriam_color)
        
        #Portraits
        
        portraits = []
        for directory in os.listdir(Manager.asset_dir + "\\" + Manager.file_to_path["Ml_N3100_picture_001"]):
            name, extension = os.path.splitext(directory)
            portraits.append(name)
        portraits = list(dict.fromkeys(portraits))
        random.seed(self.seed)
        new_list = copy.deepcopy(portraits)
        random.shuffle(new_list)
        portrait_replacement = dict(zip(portraits, new_list))
        
        #Datatables
        
        has_risky_option = (config.getboolean("EnemyRandomization", "bEnemyLevels") or config.getboolean("EnemyRandomization", "bBossLevels")) and not config.getboolean("SpecialMode", "bCustomNG")
        
        if self.map:
            Room.update_custom_map()
            Enemy.rebalance_enemies_to_map()
        
        if not config.getboolean("GameDifficulty", "bNormal"):
            Item.set_hard_mode()
        
        if config.getboolean("EnemyRandomization", "bEnemyLocations"):
            random.seed(self.seed)
            Enemy.randomize_enemy_locations()
            Enemy.update_enemy_locations()
            Enemy.restore_enemy_scaling()
        
        Item.fill_enemy_to_room()
        
        if config.getboolean("ItemRandomization", "bRemoveInfinites"):
            Item.remove_infinite_items()
        
        for item in self.start_items:
            if config.getboolean("ItemRandomization", "bOverworldPool") and item == "Shortcut":
                continue
            Item.add_starting_item(item)
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.seed)
            Item.unlock_all_quests()
            Item.add_all_hair_apparents_in_shop()
            Item.remove_all_keys_from_shop()
            Item.disable_shard_crafting()
            Item.add_starting_item("Shortcut")
            Item.randomize_overworld_keys()
            Item.randomize_overworld_items()
            Item.randomize_overworld_shards()
            Manager.set_randomizer_events()
        
        if has_risky_option:
            Item.add_pre_vepar_waystone()
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.seed)
            Item.randomize_classic_mode_drops()
        
        if config.getboolean("ItemRandomization", "bOverworldPool") or config.getboolean("EnemyRandomization", "bEnemyLocations") or self.map:
            Manager.remove_fire_shard_requirement()
        
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            random.seed(self.seed)
            Bloodless.randomize_bloodless_candles()
            if self.map:
                Bloodless.remove_gremory_cutscene()
        
        if config.getboolean("ItemRandomization", "bQuestPool"):
            random.seed(self.seed)
            Item.randomize_quest_rewards()
        
        if config.getboolean("ItemRandomization", "bShopPool"):
            random.seed(self.seed)
            Item.randomize_shop_items()
        
        if config.getboolean("ItemRandomization", "bQuestRequirements"):
            random.seed(self.seed)
            Item.randomize_quest_requirements()
            Item.update_catering_quest_info()
        
        if self.map:
            Item.replace_silver_bromide()
            Item.remove_enemy_quest_icons()
        
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"):
            random.seed(self.seed)
            Shop.randomize_shop_prices(config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"))
        
        if config.getboolean("LibraryRandomization", "bMapRequirements"):
            random.seed(self.seed)
            Library.randomize_library_requirements()
        
        if config.getboolean("LibraryRandomization", "bTomeAppearance"):
            random.seed(self.seed)
            Library.randomize_tome_appearance()
        
        if config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"):
            random.seed(self.seed)
            Shard.randomize_shard_power(config.getboolean("ShardRandomization", "bScaleMagicCostWithPower"))
        
        if config.getboolean("EquipmentRandomization", "bGlobalGearStats"):
            random.seed(self.seed)
            Equipment.randomize_equipment_stats()
            Equipment.randomize_weapon_power()
        
        if config.getboolean("EquipmentRandomization", "bCheatGearStats"):
            random.seed(self.seed)
            Equipment.randomize_cheat_equipment_stats()
            Equipment.randomize_cheat_weapon_power()
        
        if config.getboolean("EnemyRandomization", "bEnemyLevels"):
            random.seed(self.seed)
            Enemy.randomize_enemy_levels()
        
        if config.getboolean("EnemyRandomization", "bBossLevels"):
            random.seed(self.seed)
            Enemy.randomize_boss_levels()
        
        if has_risky_option:
            Enemy.increase_starting_stats()
            #Bloodless.increase_starting_stats()
        
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            random.seed(self.seed)
            Enemy.randomize_enemy_tolerances()
        
        if config.getboolean("EnemyRandomization", "bBossTolerances"):
            random.seed(self.seed)
            Enemy.randomize_boss_tolerances()
        
        if config.getboolean("SoundRandomization", "bDialogues"):
            random.seed(self.seed)
            Sound.randomize_dialogues()
        
        #Change some in-game properties based on the difficulty chosen
        if config.getboolean("GameDifficulty", "bNormal"):
            Manager.set_single_difficulty("Normal")
            Enemy.update_brv_damage("Normal")
        elif config.getboolean("GameDifficulty", "bHard"):
            Manager.set_single_difficulty("Hard")
            Manager.set_default_entry_name("NIGHTMARE")
            Enemy.add_hard_enemy_patterns()
            Enemy.update_brv_boss_speed("Hard")
            Enemy.update_brv_damage("Hard")
        elif config.getboolean("GameDifficulty", "bNightmare"):
            Manager.set_single_difficulty("Nightmare")
            Manager.set_default_entry_name("NIGHTMARE")
            Enemy.add_hard_enemy_patterns()
            Enemy.update_brv_boss_speed("Nightmare")
            Enemy.update_brv_damage("Nightmare")
            Shard.rescale_level_based_shards()
        
        #Set custom NG+ levels
        if config.getboolean("SpecialMode", "bCustomNG"):
            Enemy.set_custom_enemy_level(config.getint("SpecialMode", "iCustomNGLevel"))
        
        #Change some extra properties for Progressive Zangetsu mode
        if config.getboolean("SpecialMode", "bProgressiveZ"):
            if config.getboolean("GameDifficulty", "bNightmare"):
                Manager.set_single_difficulty("Hard")
                Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Difficulty_Hard"] = "Nightmare"
                Enemy.set_zangetsu_enemy_exp()
                Enemy.set_zangetsu_nightmare_damage()
            Enemy.reset_zangetsu_starting_stats()
            Enemy.set_zangetsu_progressive_level(config.getboolean("GameDifficulty", "bNightmare"))
            Equipment.reset_zangetsu_black_belt()
        
        #Update some things to reflect previous changes
        Item.update_drop_ids()
        Item.update_container_types()
        Item.update_shard_candles()
        Bloodless.update_shard_candles()
        Shard.update_special_properties()
        Equipment.update_special_properties()
        Enemy.update_special_properties()
        Graphic.update_boss_crystal_color()
        Manager.update_item_descriptions()
        Room.update_map_connections()
        Room.update_map_doors()
        if self.map:
            Room.update_map_indicators()
        
        #Display game version, mod version and seed on the title screen
        Manager.show_mod_stats(str(self.seed), config.get("Misc", "sVersion"))
        
        #Write the spoiler logs
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            Manager.set_default_entry_name("BLOODLESS")
            Manager.write_log("KeyLocation", Bloodless.create_log(self.seed, self.map))
        elif config.getboolean("ItemRandomization", "bOverworldPool"):
            Manager.write_log("KeyLocation", Item.create_log(self.seed, self.map))
        
        if config.getboolean("LibraryRandomization", "bMapRequirements") or config.getboolean("LibraryRandomization", "bTomeAppearance"):
            Manager.write_log("LibraryTomes", Library.create_log())
        
        if has_risky_option or config.getboolean("EnemyRandomization", "bEnemyLocations") or config.getboolean("EnemyRandomization", "bEnemyTolerances") or config.getboolean("EnemyRandomization", "bBossTolerances"):
            Manager.write_log("EnemyProperties", Enemy.create_log())
        
        #Add and import any mesh files found in the mesh directory
        for directory in os.listdir("Data\\Mesh"):
            name, extension = os.path.splitext(directory)
            if extension == ".uasset":
                Graphic.import_mesh(name)
        
        #Add new armor references defined in the json
        for item in Manager.constant["ArmorReference"]:
            Equipment.add_armor_reference(item)
        
        #Add and import any music files found in the music directory
        for directory in os.listdir("Data\\Music"):
            name, extension = os.path.splitext(directory)
            Sound.add_music_file(name)
        
        current += 1
        self.signaller.progress.emit(current)
        
        #Convert data
        
        self.progress_bar.setLabelText("Converting data...")
        
        Manager.table_simple_to_complex()
        Manager.update_datatable_order()
        current += 1
        self.signaller.progress.emit(current)
        
        #Write lip sync
        
        self.progress_bar.setLabelText("Writing lip sync...")
        
        Sound.update_lip_movement()
        current += 1
        self.signaller.progress.emit(current)
        
        #Write files
        
        self.progress_bar.setLabelText("Writing files...")
        
        Manager.write_files()
        
        #Edit the minimap outline to give an easy visual cue to tell if someone is using the mod or not and what difficulty they're on
        #This is especially useful on twitch as this difference is even visible from stream previews
        if config.getboolean("GameDifficulty", "bNormal"):
            shutil.copyfile("Data\\Texture\\Difficulty\\Normal\\WindowMinimap02.dds", "Data\\Texture\\WindowMinimap02.dds")
        elif config.getboolean("GameDifficulty", "bHard"):
            shutil.copyfile("Data\\Texture\\Difficulty\\Hard\\WindowMinimap02.dds", "Data\\Texture\\WindowMinimap02.dds")
        elif config.getboolean("GameDifficulty", "bNightmare"):
            shutil.copyfile("Data\\Texture\\Difficulty\\Nightmare\\WindowMinimap02.dds", "Data\\Texture\\WindowMinimap02.dds")
        Graphic.import_texture("WindowMinimap02")
        os.remove("Data\\Texture\\WindowMinimap02.dds")
        
        #Edit the file that contains all the icons in the game to give 8 bit weapons unique icons per rank
        #Otherwise it is almost impossible to tell which tier the weapon you're looking at actually is
        Graphic.import_texture("icon")
        
        #The textures used in the 8 Bit Nightmare area have inconsistent formats and mostly use block compression which butchers the pixel arts completely
        #An easy fix so include it here
        Graphic.import_texture("m51_EBT_BG")
        Graphic.import_texture("m51_EBT_BG_01")
        Graphic.import_texture("m51_EBT_Block")
        Graphic.import_texture("m51_EBT_Block_00")
        Graphic.import_texture("m51_EBT_Block_01")
        Graphic.import_texture("m51_EBT_Door")
        
        #Give the new dullahammer a unique color scheme
        Graphic.import_texture("T_N3127_Body_Color")
        Graphic.import_texture("T_N3127_Uni_Color")
        
        #Change the timestop shard in classic mode to have the same color as standstill
        Graphic.import_texture("time_shard_diffuse")
        Graphic.import_texture("ui_icon_pickup_timeShard")
        Graphic.import_texture("ui_icon_results_timeShard")
        #Also change the dagger icon to match the model
        Graphic.import_texture("ui_icon_pickup_dagger")
        Graphic.import_texture("ui_icon_results_dagger")
        
        #Most map icons have fixed positions on the canvas and will not adapt to the position of the rooms
        #Might be possible to edit them via a blueprint but that's not worth it so remove them if custom map is chosen
        if self.map:
            Graphic.import_texture("icon_map_journey_")
            Graphic.import_texture("Map_Icon_Keyperson")
            Graphic.import_texture("Map_Icon_RootBox")
            Graphic.import_texture("Map_StartingPoint")
        if self.map or config.getboolean("ItemRandomization", "bOverworldPool"):
            Graphic.import_texture("icon_8bitCrown")
        
        #Import chosen hues for Miriam and Zangetsu
        #While it is technically not necessary to first copy the textures out of the chosen folder we do it so that the random hue does not show up on the terminal
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            for directory in os.listdir("Data\\Texture\\Miriam\\" + miriam_color):
                shutil.copyfile("Data\\Texture\\Miriam\\" + miriam_color + "\\" + directory, "Data\\Texture\\" + directory)
            
            Graphic.import_texture("Face_Miriam")
            Graphic.import_texture("T_Pl01_Cloth_Bace")
            Graphic.import_texture("T_Body01_01_Color")
            
            for directory in os.listdir("Data\\Texture\\Miriam\\" + miriam_color):
                os.remove("Data\\Texture\\" + directory)
        
        if config.getboolean("GraphicRandomization", "bZangetsuColor"):
            for directory in os.listdir("Data\\Texture\\Zangetsu\\" + zangetsu_color):
                shutil.copyfile("Data\\Texture\\Zangetsu\\" + zangetsu_color + "\\" + directory, "Data\\Texture\\" + directory)
            
            Graphic.import_texture("Face_Zangetsu")
            Graphic.import_texture("T_N1011_body_color")
            Graphic.import_texture("T_N1011_face_color")
            Graphic.import_texture("T_N1011_weapon_color")
            Graphic.import_texture("T_Tknife05_Base")
            
            for directory in os.listdir("Data\\Texture\\Zangetsu\\" + zangetsu_color):
                os.remove("Data\\Texture\\" + directory)
        
        #Update portrait pointers
        if config.getboolean("GraphicRandomization", "bBackerPortraits"):
            for portrait in portrait_replacement:
                Graphic.update_portrait_pointer(portrait, portrait_replacement[portrait])
        
        Manager.remove_unchanged_files()
        current += 1
        self.signaller.progress.emit(current)
        
        #UnrealPak
        
        self.progress_bar.setLabelText("Packing files...")
        
        with open("Tools\\UnrealPak\\filelist.txt", "w") as file_writer:
            file_writer.write("\"Mod\*.*\" \"..\..\..\*.*\" \n")
        
        root = os.getcwd()
        os.chdir("Tools\\UnrealPak")
        os.system("cmd /c UnrealPak.exe \"Randomizer.pak\" -create=filelist.txt -compress")
        os.chdir(root)
        
        #Reset
        
        if os.path.isdir("Tools\\UE4 DDS Tools\\src\\__pycache__"):
            shutil.rmtree("Tools\\UE4 DDS Tools\\src\\__pycache__")
        shutil.rmtree("Tools\\UnrealPak\\Mod")
        os.remove("Tools\\UnrealPak\\filelist.txt")
        
        #Move
        
        if config.get("Misc", "sGamePath"):
            if not os.path.isdir(config.get("Misc", "sGamePath") + "\\~mods"):
                os.makedirs(config.get("Misc", "sGamePath") + "\\~mods")
            shutil.move("Tools\\UnrealPak\\Randomizer.pak", config.get("Misc", "sGamePath") + "\\~mods\\Randomizer.pak")
        else:
            shutil.move("Tools\\UnrealPak\\Randomizer.pak", "Randomizer.pak")
        
        current += 1
        self.signaller.progress.emit(current)
        
        self.progress_bar.setLabelText("Done")
        self.signaller.finished.emit()

class Update(QThread):
    def __init__(self, progress_bar, api):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.api = api
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit()
            raise

    def process(self):
        current = 0
        zip_name = "True Randomization.zip"
        exe_name = script_name + ".exe"
        self.signaller.progress.emit(current)
        
        #Download
        
        with open(zip_name, "wb") as file_writer:
            url = requests.get(self.api["assets"][0]["browser_download_url"], stream=True)
            for data in url.iter_content(chunk_size=4096):
                file_writer.write(data)
                current += len(data)
                self.signaller.progress.emit(current)
        
        self.progress_bar.setLabelText("Extracting...")
        
        #Purge folders
        
        shutil.rmtree("Data")
        shutil.rmtree("MapEdit\\Data")
        shutil.rmtree("Tools\\UE4 DDS Tools")
        shutil.rmtree("Tools\\UModel")
        shutil.rmtree("Tools\\UnrealPak")
        
        #Extract
        
        os.rename(exe_name, "delete.me")
        os.rename("Tools\\UAssetAPI\\Newtonsoft.Json.dll",    "Tools\\UAssetAPI\\delete1.me")
        os.rename("Tools\\UAssetAPI\\UAssetAPI.dll",          "Tools\\UAssetAPI\\delete2.me")
        os.rename("Tools\\UAssetAPI\\UAssetSnippet.dll", "Tools\\UAssetAPI\\delete3.me")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall("")
        os.remove(zip_name)
        
        #Carry previous config settings
        
        new_config = configparser.ConfigParser()
        new_config.optionxform = str
        new_config.read("Data\\config.ini")
        for each_section in new_config.sections():
            for (each_key, each_val) in new_config.items(each_section):
                if each_key == "sVersion":
                    continue
                try:
                    new_config.set(each_section, each_key, config.get(each_section, each_key))
                except (configparser.NoSectionError, configparser.NoOptionError):
                    continue
        with open("Data\\config.ini", "w") as file_writer:
            new_config.write(file_writer)
        
        #Open new EXE
        
        subprocess.Popen(exe_name)
        self.signaller.finished.emit()

class Import(QThread):
    def __init__(self, asset_list):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.asset_list = asset_list
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit()
            raise

    def process(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Extract specific assets from the game's pak using UModel
        
        if os.path.isdir(Manager.asset_dir) and self.asset_list == list(Manager.file_to_path):
            shutil.rmtree(Manager.asset_dir)
        
        for asset in self.asset_list:
            output_path = os.path.abspath("")
            
            root = os.getcwd()
            os.chdir("Tools\\UModel")
            os.system("cmd /c umodel_64.exe -path=\"" + config.get("Misc", "sGamePath") + "\" -out=\"" + output_path + "\" -save \"" + Manager.asset_dir + "\\" + Manager.file_to_path[asset] + "\\" + asset.split("(")[0] + "\"")
            os.chdir(root)
            
            current += 1
            self.signaller.progress.emit(current)
        
        self.signaller.finished.emit()

#GUI

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setEnabled(False)
        self.initUI()
        self.check_for_updates()

    def initUI(self):
        
        self.first_time = False
        if not config.getfloat("Misc", "fWindowSize") in [0.8, 0.9, 1.0]:
            config.set("Misc", "fWindowSize", "1.0")
            self.first_time = True
        
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: " + str(int(config.getfloat("Misc", "fWindowSize")*18)) + "px}"
        + "QMenu{background-color: #21222e; selection-background-color: #320288ff}"
        + "QComboBox{background-color: #21222e; selection-background-color: #320288ff}"
        + "QComboBox QAbstractItemView{border: 1px solid #21222e}"
        + "QScrollBar::add-page{background-color: #1b1c26}"
        + "QScrollBar::sub-page{background-color: #1b1c26}"
        + "QMessageBox{background-color: #21222e}"
        + "QDialog{background-color: #21222e}"
        + "QProgressDialog{background-color: #21222e}"
        + "QPushButton{background-color: #21222e}"
        + "QSpinBox{background-color: #21222e; selection-background-color: #320288ff}"
        + "QLineEdit{background-color: #21222e; selection-background-color: #320288ff}"
        + "QProgressBar{border: 2px solid white; text-align: center; font: bold}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: " + str(int(config.getfloat("Misc", "fWindowSize")*18)) + "px}")
        self.map = ""
        
        #Main layout
        
        grid = QGridLayout()
        grid.setSpacing(config.getfloat("Misc", "fWindowSize")*10)
        
        self.dummy_box = QGroupBox()
        grid.addWidget(self.dummy_box, 10, 1, 1, 4)

        #Left Label

        artwork = QLabel()
        artwork.setStyleSheet("border: 1px solid white")
        artwork.setPixmap(QPixmap("Data\\artwork.png"))
        artwork.setScaledContents(True)
        artwork.setFixedSize(config.getfloat("Misc", "fWindowSize")*550, config.getfloat("Misc", "fWindowSize")*978)
        grid.addWidget(artwork, 0, 0, 10, 1)
        
        #Groupboxes

        box_1_grid = QGridLayout()
        self.box_1 = QGroupBox("Item Randomization")
        self.box_1.setLayout(box_1_grid)
        grid.addWidget(self.box_1, 0, 1, 2, 2)

        box_2_grid = QGridLayout()
        self.box_2 = QGroupBox("Shop Randomization")
        self.box_2.setLayout(box_2_grid)
        grid.addWidget(self.box_2, 2, 1, 1, 2)

        box_3_grid = QGridLayout()
        self.box_3 = QGroupBox("Library Randomization")
        self.box_3.setLayout(box_3_grid)
        grid.addWidget(self.box_3, 3, 1, 1, 2)

        box_4_grid = QGridLayout()
        self.box_4 = QGroupBox("Shard Randomization")
        self.box_4.setLayout(box_4_grid)
        grid.addWidget(self.box_4, 4, 1, 1, 2)

        box_5_grid = QGridLayout()
        self.box_5 = QGroupBox("Equipment Randomization")
        self.box_5.setLayout(box_5_grid)
        grid.addWidget(self.box_5, 5, 1, 1, 2)

        box_6_grid = QGridLayout()
        self.box_6 = QGroupBox("Enemy Randomization")
        self.box_6.setLayout(box_6_grid)
        grid.addWidget(self.box_6, 0, 3, 2, 2)

        box_7_grid = QGridLayout()
        self.box_7 = QGroupBox("Map Randomization")
        self.box_7.setLayout(box_7_grid)
        grid.addWidget(self.box_7, 2, 3, 1, 2)

        box_8_grid = QGridLayout()
        self.box_8 = QGroupBox("Graphic Randomization")
        self.box_8.setLayout(box_8_grid)
        grid.addWidget(self.box_8, 3, 3, 1, 2)

        box_9_grid = QGridLayout()
        self.box_9 = QGroupBox("Sound Randomization")
        self.box_9.setLayout(box_9_grid)
        grid.addWidget(self.box_9, 4, 3, 1, 2)
        
        box_10_grid = QGridLayout()
        self.box_10 = QGroupBox("Extra Randomization")
        self.box_10.setLayout(box_10_grid)
        grid.addWidget(self.box_10, 5, 3, 1, 2)
        
        box_16_grid = QGridLayout()
        box_16 = QGroupBox("Start With")
        box_16.setLayout(box_16_grid)
        grid.addWidget(box_16, 7, 1, 1, 2)
        
        box_11_grid = QGridLayout()
        box_11 = QGroupBox("Game Difficulty")
        box_11.setLayout(box_11_grid)
        grid.addWidget(box_11, 6, 1, 1, 2)
        
        box_17_grid = QGridLayout()
        box_17 = QGroupBox("Special Mode")
        box_17.setLayout(box_17_grid)
        grid.addWidget(box_17, 6, 3, 1, 2)
        
        box_12_grid = QGridLayout()
        box_12 = QGroupBox("Presets")
        box_12.setLayout(box_12_grid)
        grid.addWidget(box_12, 8, 1, 1, 2)
        
        box_13_grid = QGridLayout()
        box_13 = QGroupBox("Parameter String")
        box_13.setLayout(box_13_grid)
        grid.addWidget(box_13, 7, 3, 1, 2)
        
        box_14_grid = QGridLayout()
        box_14 = QGroupBox("Game Path")
        box_14.setLayout(box_14_grid)
        grid.addWidget(box_14, 8, 3, 1, 2)
        
        box_15_left = QVBoxLayout()
        box_15_right = QVBoxLayout()
        box_15_box = QHBoxLayout()
        box_15_box.addLayout(box_15_left)
        box_15_box.addLayout(box_15_right)
        box_15 = QGroupBox()
        box_15.setLayout(box_15_box)
        box_15.setFixedSize(config.getfloat("Misc", "fWindowSize")*550, config.getfloat("Misc", "fWindowSize")*978)
        grid.addWidget(box_15, 0, 5, 10, 1)
        
        #Right label
        
        modified_files["DataTable"]["Label"] = QLabel(self)
        self.label_change("DataTable")
        box_15_left.addWidget(modified_files["DataTable"]["Label"])
        
        modified_files["StringTable"]["Label"] = QLabel(self)
        self.label_change("StringTable")
        box_15_left.addWidget(modified_files["StringTable"]["Label"])
        
        modified_files["Texture"]["Label"] = QLabel(self)
        self.label_change("Texture")
        box_15_right.addWidget(modified_files["Texture"]["Label"])
        
        modified_files["UI"]["Label"] = QLabel(self)
        self.label_change("UI")
        box_15_right.addWidget(modified_files["UI"]["Label"])
        
        modified_files["Blueprint"]["Label"] = QLabel(self)
        self.label_change("Blueprint")
        box_15_right.addWidget(modified_files["Blueprint"]["Label"])
        
        discord = QLabel()
        discord.setStyleSheet("border: 2px solid transparent")
        discord.setText("<a href=\"https://discord.gg/nUbFA7MEeU\"><font face=Cambria color=#0080ff>Discord</font></a>")
        discord.setAlignment(Qt.AlignRight)
        discord.setOpenExternalLinks(True)
        grid.addWidget(discord, 10, 5, 1, 1)

        #Checkboxes

        self.check_box_1 = QCheckBox("Overworld Pool")
        self.check_box_1.setToolTip("Randomize all items and shards found in the overworld, now with\nnew improved logic. Everything you pick up will be 100% random\nso say goodbye to the endless sea of fried fish.")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        box_1_grid.addWidget(self.check_box_1, 0, 0)
        main_widget_to_setting[self.check_box_1] = 0x000001

        self.check_box_16 = QCheckBox("Quest Pool")
        self.check_box_16.setToolTip("Randomize all quest rewards.")
        self.check_box_16.stateChanged.connect(self.check_box_16_changed)
        box_1_grid.addWidget(self.check_box_16, 1, 0)
        main_widget_to_setting[self.check_box_16] = 0x000002

        self.check_box_2 = QCheckBox("Shop Pool")
        self.check_box_2.setToolTip("Randomize all items sold at the shop.")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        box_1_grid.addWidget(self.check_box_2, 2, 0)
        main_widget_to_setting[self.check_box_2] = 0x000004

        self.check_box_17 = QCheckBox("Quest Requirements")
        self.check_box_17.setToolTip("Randomize the requirements for Susie, Abigail and Lindsay's quests.\nBenjamin will still ask you for waystones.")
        self.check_box_17.stateChanged.connect(self.check_box_17_changed)
        box_1_grid.addWidget(self.check_box_17, 3, 0)
        main_widget_to_setting[self.check_box_17] = 0x000008

        self.check_box_18 = QCheckBox("Remove Infinites")
        self.check_box_18.setToolTip("Guarantee Gebel's Glasses and Recycle Hat to never appear.\nUseful for runs that favor magic and bullet management.")
        self.check_box_18.stateChanged.connect(self.check_box_18_changed)
        box_1_grid.addWidget(self.check_box_18, 4, 0)
        main_widget_to_setting[self.check_box_18] = 0x000010

        self.check_box_3 = QCheckBox("Item Cost And Selling Price")
        self.check_box_3.setToolTip("Randomize the cost and selling price of every item in the shop.")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        box_2_grid.addWidget(self.check_box_3, 0, 0)
        main_widget_to_setting[self.check_box_3] = 0x000020

        self.check_box_4 = QCheckBox("Scale Selling Price With Cost")
        self.check_box_4.setToolTip("Make the selling price scale with the item's random cost.")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        box_2_grid.addWidget(self.check_box_4, 1, 0)
        main_widget_to_setting[self.check_box_4] = 0x000040

        self.check_box_5 = QCheckBox("Map Requirements")
        self.check_box_5.setToolTip("Randomize the completion requirement for each tome.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        box_3_grid.addWidget(self.check_box_5, 0, 0)
        main_widget_to_setting[self.check_box_5] = 0x000080

        self.check_box_6 = QCheckBox("Tome Appearance")
        self.check_box_6.setToolTip("Randomize which books are available in the game at all.\nDoes not affect Tome of Conquest.")
        self.check_box_6.stateChanged.connect(self.check_box_6_changed)
        box_3_grid.addWidget(self.check_box_6, 1, 0)
        main_widget_to_setting[self.check_box_6] = 0x000100

        self.check_box_7 = QCheckBox("Shard Power And Magic Cost")
        self.check_box_7.setToolTip("Randomize the efficiency and MP cost of each shard.\nDoes not affect progression shards.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        box_4_grid.addWidget(self.check_box_7, 0, 0)
        main_widget_to_setting[self.check_box_7] = 0x000200

        self.check_box_8 = QCheckBox("Scale Magic Cost With Power")
        self.check_box_8.setToolTip("Make the MP cost scale with the shard's random power.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        box_4_grid.addWidget(self.check_box_8, 1, 0)
        main_widget_to_setting[self.check_box_8] = 0x000400

        self.check_box_23 = QCheckBox("Global Gear Stats")
        self.check_box_23.setToolTip("Slightly randomize the stats of all weapons and pieces of\nequipment with odds that still favor their original values.")
        self.check_box_23.stateChanged.connect(self.check_box_23_changed)
        box_5_grid.addWidget(self.check_box_23, 0, 0)
        main_widget_to_setting[self.check_box_23] = 0x000800

        self.check_box_9 = QCheckBox("Cheat Gear Stats")
        self.check_box_9.setToolTip("Completely randomize the stats of the weapons, headgears\nand accessories that are originally obtained via cheatcodes.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        box_5_grid.addWidget(self.check_box_9, 1, 0)
        main_widget_to_setting[self.check_box_9] = 0x001000

        self.check_box_25 = QCheckBox("Enemy Locations")
        self.check_box_25.setToolTip("Randomize which enemies appear where.")
        self.check_box_25.stateChanged.connect(self.check_box_25_changed)
        box_6_grid.addWidget(self.check_box_25, 0, 0)
        main_widget_to_setting[self.check_box_25] = 0x002000

        self.check_box_10 = QCheckBox("Enemy Levels")
        self.check_box_10.setToolTip("Randomize the level of every enemy. Stats that scale with\nlevel include HP, attack, defense, luck, EXP and expertise.\nPicking this option will give you more starting HP and MP\nand reduce their growth to compensate.")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        box_6_grid.addWidget(self.check_box_10, 1, 0)
        main_widget_to_setting[self.check_box_10] = 0x004000

        self.check_box_26 = QCheckBox("Boss Levels")
        self.check_box_26.setToolTip("Only recommended for Miriam mode.")
        self.check_box_26.stateChanged.connect(self.check_box_26_changed)
        box_6_grid.addWidget(self.check_box_26, 2, 0)
        main_widget_to_setting[self.check_box_26] = 0x008000

        self.check_box_11 = QCheckBox("Enemy Tolerances")
        self.check_box_11.setToolTip("Randomize the first 8 resistance/weakness attributes of every enemy.")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        box_6_grid.addWidget(self.check_box_11, 3, 0)
        main_widget_to_setting[self.check_box_11] = 0x010000

        self.check_box_27 = QCheckBox("Boss Tolerances")
        self.check_box_27.setToolTip("Only recommended for Miriam mode.")
        self.check_box_27.stateChanged.connect(self.check_box_27_changed)
        box_6_grid.addWidget(self.check_box_27, 4, 0)
        main_widget_to_setting[self.check_box_27] = 0x020000

        self.check_box_12 = QCheckBox("Room Layout")
        self.check_box_12.setToolTip("Randomly pick from a folder of map presets (" + str(map_num) + ").")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        box_7_grid.addWidget(self.check_box_12, 0, 0)
        main_widget_to_setting[self.check_box_12] = 0x040000

        self.check_box_13 = QCheckBox("Miriam Color")
        self.check_box_13.setToolTip("Randomize the color of Miriam's outfit.")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        box_8_grid.addWidget(self.check_box_13, 0, 0)
        main_widget_to_setting[self.check_box_13] = 0x080000

        self.check_box_14 = QCheckBox("Zangetsu Color")
        self.check_box_14.setToolTip("Randomize the color of Zangetsu's outfit.")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        box_8_grid.addWidget(self.check_box_14, 1, 0)
        main_widget_to_setting[self.check_box_14] = 0x100000

        self.check_box_24 = QCheckBox("Backer Portraits")
        self.check_box_24.setToolTip("Shuffle backer paintings.")
        self.check_box_24.stateChanged.connect(self.check_box_24_changed)
        box_8_grid.addWidget(self.check_box_24, 0, 1)
        main_widget_to_setting[self.check_box_24] = 0x200000

        self.check_box_15 = QCheckBox("Dialogues")
        self.check_box_15.setToolTip("Randomize all conversation lines in the game. Characters\nwill still retain their actual voice (let's not get weird).")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        box_9_grid.addWidget(self.check_box_15, 0, 0)
        main_widget_to_setting[self.check_box_15] = 0x400000

        self.check_box_21 = QCheckBox("Bloodless Candles")
        self.check_box_21.setToolTip("Randomize candle placement in Bloodless mode.")
        self.check_box_21.stateChanged.connect(self.check_box_21_changed)
        box_10_grid.addWidget(self.check_box_21, 0, 0)
        main_widget_to_setting[self.check_box_21] = 0x800000
        
        #SpinButtons
        
        self.spin_button_1 = QPushButton()
        self.spin_button_1.setAccessibleName("spin_button_1")
        self.spin_button_1.setToolTip("Logic complexity. Higher values usually follow a\nprogression chain.")
        self.spin_button_1.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_1.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_1.clicked.connect(self.spin_button_1_clicked)
        self.spin_button_1.setVisible(False)
        box_1_grid.addWidget(self.spin_button_1, 0, 1)
        sub_widget_to_setting[self.spin_button_1] = 0x001
        
        self.spin_button_2 = QPushButton()
        self.spin_button_2.setAccessibleName("spin_button_2")
        self.spin_button_2.setToolTip("Wheight of shop items locked behind events.")
        self.spin_button_2.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_2.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_2.clicked.connect(self.spin_button_2_clicked)
        self.spin_button_2.setVisible(False)
        box_1_grid.addWidget(self.spin_button_2, 2, 1)
        sub_widget_to_setting[self.spin_button_2] = 0x002
        
        self.spin_button_3 = QPushButton()
        self.spin_button_3.setAccessibleName("spin_button_3")
        self.spin_button_3.setToolTip("Price wheight. The higher the value the more extreme\nthe price differences.")
        self.spin_button_3.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_3.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_3.clicked.connect(self.spin_button_3_clicked)
        self.spin_button_3.setVisible(False)
        box_2_grid.addWidget(self.spin_button_3, 0, 1)
        sub_widget_to_setting[self.spin_button_3] = 0x004
        
        self.spin_button_4 = QPushButton()
        self.spin_button_4.setAccessibleName("spin_button_4")
        self.spin_button_4.setToolTip("Requirement wheight. 2 is linear, 1 and 3 favor early and\nlate map completion respectively.")
        self.spin_button_4.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_4.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_4.clicked.connect(self.spin_button_4_clicked)
        self.spin_button_4.setVisible(False)
        box_3_grid.addWidget(self.spin_button_4, 0, 1)
        sub_widget_to_setting[self.spin_button_4] = 0x008
        
        self.spin_button_5 = QPushButton()
        self.spin_button_5.setAccessibleName("spin_button_5")
        self.spin_button_5.setToolTip("Power wheight. The higher the value the more extreme\nthe power differences.")
        self.spin_button_5.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_5.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_5.clicked.connect(self.spin_button_5_clicked)
        self.spin_button_5.setVisible(False)
        box_4_grid.addWidget(self.spin_button_5, 0, 1)
        sub_widget_to_setting[self.spin_button_5] = 0x010
        
        self.spin_button_6 = QPushButton()
        self.spin_button_6.setAccessibleName("spin_button_6")
        self.spin_button_6.setToolTip("Stat wheight. The higher the value the more extreme\nthe stat differences.")
        self.spin_button_6.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_6.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_6.clicked.connect(self.spin_button_6_clicked)
        self.spin_button_6.setVisible(False)
        box_5_grid.addWidget(self.spin_button_6, 0, 1)
        sub_widget_to_setting[self.spin_button_6] = 0x020
        
        self.spin_button_8 = QPushButton()
        self.spin_button_8.setAccessibleName("spin_button_8")
        self.spin_button_8.setToolTip("Level wheight. The higher the value the more extreme\nthe level differences.")
        self.spin_button_8.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_8.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_8.clicked.connect(self.spin_button_8_clicked)
        self.spin_button_8.setVisible(False)
        box_6_grid.addWidget(self.spin_button_8, 1, 1)
        sub_widget_to_setting[self.spin_button_8] = 0x040
        
        self.spin_button_9 = QPushButton()
        self.spin_button_9.setAccessibleName("spin_button_9")
        self.spin_button_9.setToolTip("Level wheight. The higher the value the more extreme\nthe level differences.")
        self.spin_button_9.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_9.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_9.clicked.connect(self.spin_button_9_clicked)
        self.spin_button_9.setVisible(False)
        box_6_grid.addWidget(self.spin_button_9, 2, 1)
        sub_widget_to_setting[self.spin_button_9] = 0x080
        
        self.spin_button_10 = QPushButton()
        self.spin_button_10.setAccessibleName("spin_button_10")
        self.spin_button_10.setToolTip("Tolerance wheight. The higher the value the more extreme\nthe tolerance differences.")
        self.spin_button_10.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_10.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_10.clicked.connect(self.spin_button_10_clicked)
        self.spin_button_10.setVisible(False)
        box_6_grid.addWidget(self.spin_button_10, 3, 1)
        sub_widget_to_setting[self.spin_button_10] = 0x100
        
        self.spin_button_11 = QPushButton()
        self.spin_button_11.setAccessibleName("spin_button_11")
        self.spin_button_11.setToolTip("Tolerance wheight. The higher the value the more extreme\nthe tolerance differences.")
        self.spin_button_11.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_11.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_11.clicked.connect(self.spin_button_11_clicked)
        self.spin_button_11.setVisible(False)
        box_6_grid.addWidget(self.spin_button_11, 4, 1)
        sub_widget_to_setting[self.spin_button_11] = 0x200
        
        self.language_sequence = "JE"
        self.spin_button_12 = QPushButton()
        self.spin_button_12.setAccessibleName("spin_button_12")
        self.spin_button_12.setToolTip("Voice language")
        self.spin_button_12.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_12.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_12.clicked.connect(self.spin_button_12_clicked)
        self.spin_button_12.setVisible(False)
        box_9_grid.addWidget(self.spin_button_12, 0, 1)
        sub_widget_to_setting[self.spin_button_12] = 0x400
        
        self.spin_button_13 = QPushButton()
        self.spin_button_13.setAccessibleName("spin_button_13")
        self.spin_button_13.setToolTip("Logic complexity. Higher values usually follow a\nprogression chain.")
        self.spin_button_13.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_13.setFixedSize(config.getfloat("Misc", "fWindowSize")*28, config.getfloat("Misc", "fWindowSize")*24)
        self.spin_button_13.clicked.connect(self.spin_button_13_clicked)
        self.spin_button_13.setVisible(False)
        box_10_grid.addWidget(self.spin_button_13, 0, 1)
        sub_widget_to_setting[self.spin_button_13] = 0x800
        
        #RadioButtons
        
        self.radio_button_1 = QRadioButton("Normal")
        self.radio_button_1.setToolTip("More like easy mode.")
        self.radio_button_1.toggled.connect(self.radio_button_group_1_checked)
        box_11_grid.addWidget(self.radio_button_1, 0, 0)
        
        self.radio_button_2 = QRadioButton("Hard")
        self.radio_button_2.setToolTip("The real normal mode.")
        self.radio_button_2.toggled.connect(self.radio_button_group_1_checked)
        box_11_grid.addWidget(self.radio_button_2, 1, 0)
        
        self.radio_button_3 = QRadioButton("Nightmare")
        self.radio_button_3.setToolTip("Shit's gonna get real.")
        self.radio_button_3.toggled.connect(self.radio_button_group_1_checked)
        box_11_grid.addWidget(self.radio_button_3, 0, 1)
        
        self.radio_button_14 = QRadioButton("None")
        self.radio_button_14.setToolTip("No special game mode.")
        self.radio_button_14.toggled.connect(self.radio_button_group_6_checked)
        box_17_grid.addWidget(self.radio_button_14, 0, 0)
        
        self.radio_button_5 = QRadioButton("Custom NG+")
        self.radio_button_5.setToolTip("Play through your NG+ files with a chosen level\nvalue for all enemies.")
        self.radio_button_5.toggled.connect(self.radio_button_group_6_checked)
        box_17_grid.addWidget(self.radio_button_5, 1, 0)
        
        self.radio_button_15 = QRadioButton("Progressive Z")
        self.radio_button_15.setToolTip("Play through a more balanced version of Zangetsu\nmode where his stats scale with progression.")
        self.radio_button_15.toggled.connect(self.radio_button_group_6_checked)
        box_17_grid.addWidget(self.radio_button_15, 0, 1)
        
        #Spin boxes
        
        config.set("SpecialMode", "iCustomNGLevel", str(min(max(config.getint("SpecialMode", "iCustomNGLevel"), 1), 99)))
        
        self.level_box = QSpinBox()
        self.level_box.setToolTip("Level of all enemies.")
        self.level_box.setRange(1, 99)
        self.level_box.setValue(config.getint("SpecialMode", "iCustomNGLevel"))
        self.level_box.valueChanged.connect(self.new_level)
        self.level_box.setVisible(False)
        box_17_grid.addWidget(self.level_box, 1, 1)
        
        #Dropdown lists
        
        self.preset_drop_down = QComboBox()
        self.preset_drop_down.setToolTip("EMPTY: Clear all options.\nTRIAL: To get started with this mod.\nRACE: Most fitting for a King of Speed.\nMEME: Time to break the game.\nRISK: Chaos awaits !\nBLOOD: She needs more blood.")
        self.preset_drop_down.addItem("Custom")
        for preset in preset_to_bytes:
            self.preset_drop_down.addItem(preset)
        self.preset_drop_down.currentIndexChanged.connect(self.preset_drop_down_change)
        box_12_grid.addWidget(self.preset_drop_down, 0, 0)
        
        #Interface Settings
        
        self.setting_layout = QGridLayout()
        
        size_box_grid = QGridLayout()
        size_box = QGroupBox("Window Size")
        size_box.setLayout(size_box_grid)
        self.setting_layout.addWidget(size_box, 0, 0, 1, 1)
        
        self.size_drop_down = QComboBox()
        self.size_drop_down.addItem("720p")
        self.size_drop_down.addItem("900p")
        self.size_drop_down.addItem("1080p and above")
        size_box_grid.addWidget(self.size_drop_down, 0, 0, 1, 1)
        
        setting_button = QPushButton("Apply")
        setting_button.clicked.connect(self.setting_button_clicked)
        self.setting_layout.addWidget(setting_button, 1, 0, 1, 1)
        
        #Seed
        
        self.seed_layout = QGridLayout()
        
        self.seed_field = QLineEdit(config.get("Misc", "sSeed"))
        self.seed_field.setMaxLength(30)
        self.seed_field.textChanged[str].connect(self.new_seed)
        self.seed_layout.addWidget(self.seed_field, 0, 0, 1, 3)
        
        seed_button_1 = QPushButton("New Seed")
        seed_button_1.clicked.connect(self.seed_button_1_clicked)
        self.seed_layout.addWidget(seed_button_1, 1, 0, 1, 1)
        
        seed_button_3 = QPushButton("Test Seed")
        seed_button_3.clicked.connect(self.seed_button_3_clicked)
        self.seed_layout.addWidget(seed_button_3, 1, 1, 1, 1)
        
        seed_button_2 = QPushButton("Confirm")
        seed_button_2.clicked.connect(self.seed_button_2_clicked)
        self.seed_layout.addWidget(seed_button_2, 1, 2, 1, 1)
        
        #Text field
        
        self.start_field = QLineEdit(config.get("StartWith", "sStartItem"))
        self.start_field.setToolTip("Items to start with. Input their english names\nwith | as separator. If unsure refer to the files\nin Data\Translation for item names.")
        self.start_field.textChanged[str].connect(self.new_start)
        box_16_grid.addWidget(self.start_field, 0, 0)
        
        self.setting_format = "{:0" + str(main_setting_length + sub_setting_length) + "x}"
        self.setting_field = QLineEdit(self.setting_format.format(0).upper())
        self.setting_field.setMaxLength(main_setting_length + sub_setting_length)
        self.setting_field.setToolTip("Simplified string containing all the randomization settings.")
        self.setting_field.textChanged[str].connect(self.new_setting)
        box_13_grid.addWidget(self.setting_field, 0, 0)
        
        self.output_field = QLineEdit(config.get("Misc", "sGamePath"))
        self.output_field.setToolTip("Path to your game's data (...\BloodstainedRotN\Content\Paks).")
        self.output_field.textChanged[str].connect(self.new_output)
        box_14_grid.addWidget(self.output_field, 0, 0)
        
        browse_button = QPushButton()
        browse_button.setIcon(QPixmap("Data\\browse.png"))
        browse_button.clicked.connect(self.browse_button_clicked)
        box_14_grid.addWidget(browse_button, 0, 1)
        
        #Init checkboxes
        
        self.check_box_1.setChecked(config.getboolean("ItemRandomization", "bOverworldPool"))
        self.check_box_2.setChecked(config.getboolean("ItemRandomization", "bShopPool"))
        self.check_box_16.setChecked(config.getboolean("ItemRandomization", "bQuestPool"))
        self.check_box_17.setChecked(config.getboolean("ItemRandomization", "bQuestRequirements"))
        self.check_box_18.setChecked(config.getboolean("ItemRandomization", "bRemoveInfinites"))
        self.check_box_3.setChecked(config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"))
        self.check_box_4.setChecked(config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"))
        self.check_box_5.setChecked(config.getboolean("LibraryRandomization", "bMapRequirements"))
        self.check_box_6.setChecked(config.getboolean("LibraryRandomization", "bTomeAppearance"))
        self.check_box_7.setChecked(config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"))
        self.check_box_8.setChecked(config.getboolean("ShardRandomization", "bScaleMagicCostWithPower"))
        self.check_box_23.setChecked(config.getboolean("EquipmentRandomization", "bGlobalGearStats"))
        self.check_box_9.setChecked(config.getboolean("EquipmentRandomization", "bCheatGearStats"))
        self.check_box_25.setChecked(config.getboolean("EnemyRandomization", "bEnemyLocations"))
        self.check_box_10.setChecked(config.getboolean("EnemyRandomization", "bEnemyLevels"))
        self.check_box_26.setChecked(config.getboolean("EnemyRandomization", "bBossLevels"))
        self.check_box_11.setChecked(config.getboolean("EnemyRandomization", "bEnemyTolerances"))
        self.check_box_27.setChecked(config.getboolean("EnemyRandomization", "bBossTolerances"))
        self.check_box_12.setChecked(config.getboolean("MapRandomization", "bRoomLayout"))
        self.check_box_13.setChecked(config.getboolean("GraphicRandomization", "bMiriamColor"))
        self.check_box_14.setChecked(config.getboolean("GraphicRandomization", "bZangetsuColor"))
        self.check_box_24.setChecked(config.getboolean("GraphicRandomization", "bBackerPortraits"))
        self.check_box_15.setChecked(config.getboolean("SoundRandomization", "bDialogues"))
        self.check_box_21.setChecked(config.getboolean("ExtraRandomization", "bBloodlessCandles"))
        
        self.spin_button_1_set_index(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        self.spin_button_2_set_index(config.getint("ItemRandomization", "iShopPoolWheight"))
        self.spin_button_3_set_index(config.getint("ShopRandomization", "iItemCostAndSellingPriceWheight"))
        self.spin_button_4_set_index(config.getint("LibraryRandomization", "iMapRequirementsWheight"))
        self.spin_button_5_set_index(config.getint("ShardRandomization", "iShardPowerAndMagicCostWheight"))
        self.spin_button_6_set_index(config.getint("EquipmentRandomization", "iGlobalGearStatsWheight"))
        self.spin_button_8_set_index(config.getint("EnemyRandomization", "iEnemyLevelsWheight"))
        self.spin_button_9_set_index(config.getint("EnemyRandomization", "iBossLevelsWheight"))
        self.spin_button_10_set_index(config.getint("EnemyRandomization", "iEnemyTolerancesWheight"))
        self.spin_button_11_set_index(config.getint("EnemyRandomization", "iBossTolerancesWheight"))
        self.spin_button_12_set_index(config.getint("SoundRandomization", "iDialoguesLanguage"))
        self.spin_button_13_set_index(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
        
        if config.getboolean("GameDifficulty", "bNormal"):
            self.radio_button_1.setChecked(True)
        elif config.getboolean("GameDifficulty", "bHard"):
            self.radio_button_2.setChecked(True)
        else:
            self.radio_button_3.setChecked(True)
        
        if config.getboolean("SpecialMode", "bNone"):
            self.radio_button_14.setChecked(True)
        elif config.getboolean("SpecialMode", "bCustomNG"):
            self.radio_button_5.setChecked(True)
        else:
            self.radio_button_15.setChecked(True)
        
        if config.getfloat("Misc", "fWindowSize") == 0.8:
            self.size_drop_down.setCurrentIndex(0)
        elif config.getfloat("Misc", "fWindowSize") == 0.9:
            self.size_drop_down.setCurrentIndex(1)
        elif config.getfloat("Misc", "fWindowSize") == 1.0:
            self.size_drop_down.setCurrentIndex(2)
        
        self.matches_preset()

        #Buttons
        
        button_3 = QPushButton("Settings")
        button_3.setToolTip("Interface settings.")
        button_3.clicked.connect(self.button_3_clicked)
        grid.addWidget(button_3, 9, 1, 1, 1)

        button_4 = QPushButton("Pick Map")
        button_4.setToolTip("Manually pick a custom map to play on (overrides the random map selection).")
        button_4.clicked.connect(self.button_4_clicked)
        grid.addWidget(button_4, 9, 2, 1, 1)
        
        button_6 = QPushButton("Import Assets")
        button_6.setToolTip("Reimport and convert all base game assets used in this mod.\nUseful if the game updates or if one asset gets corrupted on\naccident.")
        button_6.clicked.connect(self.button_6_clicked)
        grid.addWidget(button_6, 9, 3, 1, 1)
        
        button_7 = QPushButton("Credits")
        button_7.setToolTip("The people involved with this mod.")
        button_7.clicked.connect(self.button_7_clicked)
        grid.addWidget(button_7, 9, 4, 1, 1)

        button_5 = QPushButton("Generate")
        button_5.setToolTip("Generate .pak file with current settings.")
        button_5.clicked.connect(self.button_5_clicked)
        grid.addWidget(button_5, 10, 1, 1, 4)
        
        #Window
        
        self.setLayout(grid)
        self.setFixedSize(config.getfloat("Misc", "fWindowSize")*1800, config.getfloat("Misc", "fWindowSize")*1000)
        self.setWindowTitle(script_name)
        self.setWindowIcon(QIcon("Data\\icon.png"))
        
        #Background
        
        background = QPixmap("MapEdit\\Data\\background.png")
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, background)
        self.show()
        self.setPalette(self.palette)
        
        #Position
        
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        QApplication.processEvents()
    
    def check_box_1_changed(self):
        if self.check_box_1.isChecked():
            config.set("ItemRandomization", "bOverworldPool", "true")
            self.add_main_setting(self.check_box_1)
            self.check_box_1.setStyleSheet("color: " + item_color)
            if self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config.set("ItemRandomization", "bOverworldPool", "false")
            self.remove_main_setting(self.check_box_1)
            self.check_box_1.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
            self.check_box_16.setChecked(False)
            self.check_box_2.setChecked(False)
        self.spin_button_1.setVisible(self.check_box_1.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_16_changed(self):
        if self.check_box_16.isChecked():
            config.set("ItemRandomization", "bQuestPool", "true")
            self.add_main_setting(self.check_box_16)
            self.check_box_16.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            self.check_box_1.setChecked(True)
        else:
            config.set("ItemRandomization", "bQuestPool", "false")
            self.remove_main_setting(self.check_box_16)
            self.check_box_16.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
            self.check_box_2.setChecked(False)
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_2_changed(self):
        if self.check_box_2.isChecked():
            config.set("ItemRandomization", "bShopPool", "true")
            self.add_main_setting(self.check_box_2)
            self.check_box_2.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            self.check_box_1.setChecked(True)
            self.check_box_16.setChecked(True)
        else:
            config.set("ItemRandomization", "bShopPool", "false")
            self.remove_main_setting(self.check_box_2)
            self.check_box_2.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.spin_button_2.setVisible(self.check_box_2.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_17_changed(self):
        if self.check_box_17.isChecked():
            config.set("ItemRandomization", "bQuestRequirements", "true")
            self.add_main_setting(self.check_box_17)
            self.check_box_17.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config.set("ItemRandomization", "bQuestRequirements", "false")
            self.remove_main_setting(self.check_box_17)
            self.check_box_17.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_18_changed(self):
        if self.check_box_18.isChecked():
            config.set("ItemRandomization", "bRemoveInfinites", "true")
            self.add_main_setting(self.check_box_18)
            self.check_box_18.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config.set("ItemRandomization", "bRemoveInfinites", "false")
            self.remove_main_setting(self.check_box_18)
            self.check_box_18.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_3_changed(self):
        if self.check_box_3.isChecked():
            config.set("ShopRandomization", "bItemCostAndSellingPrice", "true")
            self.add_main_setting(self.check_box_3)
            self.check_box_3.setStyleSheet("color: " + shop_color)
            if self.check_box_4.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
        else:
            config.set("ShopRandomization", "bItemCostAndSellingPrice", "false")
            self.remove_main_setting(self.check_box_3)
            self.check_box_3.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")
            self.check_box_4.setChecked(False)
        self.spin_button_3.setVisible(self.check_box_3.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_4_changed(self):
        if self.check_box_4.isChecked():
            config.set("ShopRandomization", "bScaleSellingPriceWithCost", "true")
            self.add_main_setting(self.check_box_4)
            self.check_box_4.setStyleSheet("color: " + shop_color)
            if self.check_box_3.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
            self.check_box_3.setChecked(True)
        else:
            config.set("ShopRandomization", "bScaleSellingPriceWithCost", "false")
            self.remove_main_setting(self.check_box_4)
            self.check_box_4.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_5_changed(self):
        if self.check_box_5.isChecked():
            config.set("LibraryRandomization", "bMapRequirements", "true")
            self.add_main_setting(self.check_box_5)
            self.check_box_5.setStyleSheet("color: " + library_color)
            if self.check_box_6.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
        else:
            config.set("LibraryRandomization", "bMapRequirements", "false")
            self.remove_main_setting(self.check_box_5)
            self.check_box_5.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
        self.spin_button_4.setVisible(self.check_box_5.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_6_changed(self):
        if self.check_box_6.isChecked():
            config.set("LibraryRandomization", "bTomeAppearance", "true")
            self.add_main_setting(self.check_box_6)
            self.check_box_6.setStyleSheet("color: " + library_color)
            if self.check_box_5.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
        else:
            config.set("LibraryRandomization", "bTomeAppearance", "false")
            self.remove_main_setting(self.check_box_6)
            self.check_box_6.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_7_changed(self):
        if self.check_box_7.isChecked():
            config.set("ShardRandomization", "bShardPowerAndMagicCost", "true")
            self.add_main_setting(self.check_box_7)
            self.check_box_7.setStyleSheet("color: " + shard_color)
            if self.check_box_8.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
        else:
            config.set("ShardRandomization", "bShardPowerAndMagicCost", "false")
            self.remove_main_setting(self.check_box_7)
            self.check_box_7.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")
            self.check_box_8.setChecked(False)
        self.spin_button_5.setVisible(self.check_box_7.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_8_changed(self):
        if self.check_box_8.isChecked():
            config.set("ShardRandomization", "bScaleMagicCostWithPower", "true")
            self.add_main_setting(self.check_box_8)
            self.check_box_8.setStyleSheet("color: " + shard_color)
            if self.check_box_7.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
            self.check_box_7.setChecked(True)
        else:
            config.set("ShardRandomization", "bScaleMagicCostWithPower", "false")
            self.remove_main_setting(self.check_box_8)
            self.check_box_8.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_23_changed(self):
        if self.check_box_23.isChecked():
            config.set("EquipmentRandomization", "bGlobalGearStats", "true")
            self.add_main_setting(self.check_box_23)
            self.check_box_23.setStyleSheet("color: " + equip_color)
            if self.check_box_9.isChecked():
                self.box_5.setStyleSheet("color: " + equip_color)
        else:
            config.set("EquipmentRandomization", "bGlobalGearStats", "false")
            self.remove_main_setting(self.check_box_23)
            self.check_box_23.setStyleSheet("color: #ffffff")
            self.box_5.setStyleSheet("color: #ffffff")
        self.spin_button_6.setVisible(self.check_box_23.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_9_changed(self):
        if self.check_box_9.isChecked():
            config.set("EquipmentRandomization", "bCheatGearStats", "true")
            self.add_main_setting(self.check_box_9)
            self.check_box_9.setStyleSheet("color: " + equip_color)
            if self.check_box_23.isChecked():
                self.box_5.setStyleSheet("color: " + equip_color)
        else:
            config.set("EquipmentRandomization", "bCheatGearStats", "false")
            self.remove_main_setting(self.check_box_9)
            self.check_box_9.setStyleSheet("color: #ffffff")
            self.box_5.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_25_changed(self):
        if self.check_box_25.isChecked():
            config.set("EnemyRandomization", "bEnemyLocations", "true")
            self.add_main_setting(self.check_box_25)
            self.check_box_25.setStyleSheet("color: " + enemy_color)
            if self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bEnemyLocations", "false")
            self.remove_main_setting(self.check_box_25)
            self.check_box_25.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_10_changed(self):
        if self.check_box_10.isChecked():
            config.set("EnemyRandomization", "bEnemyLevels", "true")
            self.add_main_setting(self.check_box_10)
            self.check_box_10.setStyleSheet("color: " + enemy_color)
            if self.check_box_25.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bEnemyLevels", "false")
            self.remove_main_setting(self.check_box_10)
            self.check_box_10.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.spin_button_8.setVisible(self.check_box_10.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_26_changed(self):
        if self.check_box_26.isChecked():
            config.set("EnemyRandomization", "bBossLevels", "true")
            self.add_main_setting(self.check_box_26)
            self.check_box_26.setStyleSheet("color: " + enemy_color)
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bBossLevels", "false")
            self.remove_main_setting(self.check_box_26)
            self.check_box_26.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.spin_button_9.setVisible(self.check_box_26.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_11_changed(self):
        if self.check_box_11.isChecked():
            config.set("EnemyRandomization", "bEnemyTolerances", "true")
            self.add_main_setting(self.check_box_11)
            self.check_box_11.setStyleSheet("color: " + enemy_color)
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_27.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bEnemyTolerances", "false")
            self.remove_main_setting(self.check_box_11)
            self.check_box_11.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.spin_button_10.setVisible(self.check_box_11.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_27_changed(self):
        if self.check_box_27.isChecked():
            config.set("EnemyRandomization", "bBossTolerances", "true")
            self.add_main_setting(self.check_box_27)
            self.check_box_27.setStyleSheet("color: " + enemy_color)
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bBossTolerances", "false")
            self.remove_main_setting(self.check_box_27)
            self.check_box_27.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.spin_button_11.setVisible(self.check_box_27.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_12_changed(self):
        if self.check_box_12.isChecked():
            config.set("MapRandomization", "bRoomLayout", "true")
            self.add_main_setting(self.check_box_12)
            self.check_box_12.setStyleSheet("color: " + map_color)
            self.box_7.setStyleSheet("color: " + map_color)
            if not self.map:
                self.add_to_list("UI", "icon_8bitCrown"    , [])
                self.add_to_list("UI", "Map_Icon_Keyperson", [])
                self.add_to_list("UI", "Map_Icon_RootBox"  , [])
                self.add_to_list("UI", "Map_StartingPoint" , [])
        else:
            config.set("MapRandomization", "bRoomLayout", "false")
            self.remove_main_setting(self.check_box_12)
            self.check_box_12.setStyleSheet("color: #ffffff")
            self.box_7.setStyleSheet("color: #ffffff")
            if not self.map:
                self.remove_from_list("UI", "icon_8bitCrown"    , [])
                self.remove_from_list("UI", "Map_Icon_Keyperson", [])
                self.remove_from_list("UI", "Map_Icon_RootBox"  , [])
                self.remove_from_list("UI", "Map_StartingPoint" , [])
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_13_changed(self):
        if self.check_box_13.isChecked():
            config.set("GraphicRandomization", "bMiriamColor", "true")
            self.add_main_setting(self.check_box_13)
            self.check_box_13.setStyleSheet("color: " + graphic_color)
            if self.check_box_14.isChecked() and self.check_box_24.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list("UI"     , "Face_Miriam"      , [])
            self.add_to_list("Texture", "T_Body01_01_Color", [])
            self.add_to_list("Texture", "T_Pl01_Cloth_Bace", [])
        else:
            config.set("GraphicRandomization", "bMiriamColor", "false")
            self.remove_main_setting(self.check_box_13)
            self.check_box_13.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list("UI"     , "Face_Miriam"      , [])
            self.remove_from_list("Texture", "T_Body01_01_Color", [])
            self.remove_from_list("Texture", "T_Pl01_Cloth_Bace", [])
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_14_changed(self):
        if self.check_box_14.isChecked():
            config.set("GraphicRandomization", "bZangetsuColor", "true")
            self.add_main_setting(self.check_box_14)
            self.check_box_14.setStyleSheet("color: " + graphic_color)
            if self.check_box_13.isChecked() and self.check_box_24.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list("UI"     , "Face_Zangetsu"      , [])
            self.add_to_list("Texture", "T_N1011_body_color" , [])
            self.add_to_list("Texture", "T_N1011_face_color" , [])
            self.add_to_list("Texture", "T_N1011_equip_color", [])
            self.add_to_list("Texture", "T_Tknife05_Base"    , [])
        else:
            config.set("GraphicRandomization", "bZangetsuColor", "false")
            self.remove_main_setting(self.check_box_14)
            self.check_box_14.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list("UI"     , "Face_Zangetsu"      , [])
            self.remove_from_list("Texture", "T_N1011_body_color" , [])
            self.remove_from_list("Texture", "T_N1011_face_color" , [])
            self.remove_from_list("Texture", "T_N1011_equip_color", [])
            self.remove_from_list("Texture", "T_Tknife05_Base"    , [])
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_24_changed(self):
        if self.check_box_24.isChecked():
            config.set("GraphicRandomization", "bBackerPortraits", "true")
            self.add_main_setting(self.check_box_24)
            self.check_box_24.setStyleSheet("color: " + graphic_color)
            if self.check_box_13.isChecked() and self.check_box_14.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
        else:
            config.set("GraphicRandomization", "bBackerPortraits", "false")
            self.remove_main_setting(self.check_box_24)
            self.check_box_24.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_15_changed(self):
        if self.check_box_15.isChecked():
            config.set("SoundRandomization", "bDialogues", "true")
            self.add_main_setting(self.check_box_15)
            self.check_box_15.setStyleSheet("color: " + sound_color)
            self.box_9.setStyleSheet("color: " + sound_color)
        else:
            config.set("SoundRandomization", "bDialogues", "false")
            self.remove_main_setting(self.check_box_15)
            self.check_box_15.setStyleSheet("color: #ffffff")
            self.box_9.setStyleSheet("color: #ffffff")
        self.spin_button_12.setVisible(self.check_box_15.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def check_box_21_changed(self):
        if self.check_box_21.isChecked():
            config.set("ExtraRandomization", "bBloodlessCandles", "true")
            self.add_main_setting(self.check_box_21)
            self.check_box_21.setStyleSheet("color: " + extra_color)
            self.box_10.setStyleSheet("color: " + extra_color)
        else:
            config.set("ExtraRandomization", "bBloodlessCandles", "false")
            self.remove_main_setting(self.check_box_21)
            self.check_box_21.setStyleSheet("color: #ffffff")
            self.box_10.setStyleSheet("color: #ffffff")
        self.spin_button_13.setVisible(self.check_box_21.isChecked())
        self.fix_background_glitch()
        self.matches_preset()

    def spin_button_1_clicked(self):
        num = self.spin_button_1_get_index()
        num = num % 3 + 1
        self.spin_button_1_set_index(num)

    def spin_button_1_get_index(self):
        if self.spin_button_1.text():
            return int(self.spin_button_1.text())
        return None

    def spin_button_1_set_index(self, index):
        self.spin_button_1.setText(str(index))
        config.set("ItemRandomization", "iOverworldPoolComplexity", str(index))
        self.change_sub_setting(self.spin_button_1, index)
        return True

    def spin_button_2_clicked(self):
        num = self.spin_button_2_get_index()
        num = num % 3 + 1
        self.spin_button_2_set_index(num)

    def spin_button_2_get_index(self):
        if self.spin_button_2.text():
            return int(self.spin_button_2.text())
        return None

    def spin_button_2_set_index(self, index):
        self.spin_button_2.setText(str(index))
        config.set("ItemRandomization", "iShopPoolWheight", str(index))
        self.change_sub_setting(self.spin_button_2, index)
        return True

    def spin_button_3_clicked(self):
        num = self.spin_button_3_get_index()
        num = num % 3 + 1
        self.spin_button_3_set_index(num)

    def spin_button_3_get_index(self):
        if self.spin_button_3.text():
            return int(self.spin_button_3.text())
        return None

    def spin_button_3_set_index(self, index):
        self.spin_button_3.setText(str(index))
        config.set("ShopRandomization", "iItemCostAndSellingPriceWheight", str(index))
        self.change_sub_setting(self.spin_button_3, index)
        return True

    def spin_button_4_clicked(self):
        num = self.spin_button_4_get_index()
        num = num % 3 + 1
        self.spin_button_4_set_index(num)

    def spin_button_4_get_index(self):
        if self.spin_button_4.text():
            return int(self.spin_button_4.text())
        return None

    def spin_button_4_set_index(self, index):
        self.spin_button_4.setText(str(index))
        config.set("LibraryRandomization", "iMapRequirementsWheight", str(index))
        self.change_sub_setting(self.spin_button_4, index)
        return True

    def spin_button_5_clicked(self):
        num = self.spin_button_5_get_index()
        num = num % 3 + 1
        self.spin_button_5_set_index(num)

    def spin_button_5_get_index(self):
        if self.spin_button_5.text():
            return int(self.spin_button_5.text())
        return None

    def spin_button_5_set_index(self, index):
        self.spin_button_5.setText(str(index))
        config.set("ShardRandomization", "iShardPowerAndMagicCostWheight", str(index))
        self.change_sub_setting(self.spin_button_5, index)
        return True

    def spin_button_6_clicked(self):
        num = self.spin_button_6_get_index()
        num = num % 3 + 1
        self.spin_button_6_set_index(num)

    def spin_button_6_get_index(self):
        if self.spin_button_6.text():
            return int(self.spin_button_6.text())
        return None

    def spin_button_6_set_index(self, index):
        self.spin_button_6.setText(str(index))
        config.set("EquipmentRandomization", "iGlobalGearStatsWheight", str(index))
        self.change_sub_setting(self.spin_button_6, index)
        return True

    def spin_button_8_clicked(self):
        num = self.spin_button_8_get_index()
        num = num % 3 + 1
        self.spin_button_8_set_index(num)

    def spin_button_8_get_index(self):
        if self.spin_button_8.text():
            return int(self.spin_button_8.text())
        return None

    def spin_button_8_set_index(self, index):
        self.spin_button_8.setText(str(index))
        config.set("EnemyRandomization", "iEnemyLevelsWheight", str(index))
        self.change_sub_setting(self.spin_button_8, index)
        return True

    def spin_button_9_clicked(self):
        num = self.spin_button_9_get_index()
        num = num % 3 + 1
        self.spin_button_9_set_index(num)

    def spin_button_9_get_index(self):
        if self.spin_button_9.text():
            return int(self.spin_button_9.text())
        return None

    def spin_button_9_set_index(self, index):
        self.spin_button_9.setText(str(index))
        config.set("EnemyRandomization", "iBossLevelsWheight", str(index))
        self.change_sub_setting(self.spin_button_9, index)
        return True

    def spin_button_10_clicked(self):
        num = self.spin_button_10_get_index()
        num = num % 3 + 1
        self.spin_button_10_set_index(num)

    def spin_button_10_get_index(self):
        if self.spin_button_10.text():
            return int(self.spin_button_10.text())
        return None

    def spin_button_10_set_index(self, index):
        self.spin_button_10.setText(str(index))
        config.set("EnemyRandomization", "iEnemyTolerancesWheight", str(index))
        self.change_sub_setting(self.spin_button_10, index)
        return True

    def spin_button_11_clicked(self):
        num = self.spin_button_11_get_index()
        num = num % 3 + 1
        self.spin_button_11_set_index(num)

    def spin_button_11_get_index(self):
        if self.spin_button_11.text():
            return int(self.spin_button_11.text())
        return None

    def spin_button_11_set_index(self, index):
        self.spin_button_11.setText(str(index))
        config.set("EnemyRandomization", "iBossTolerancesWheight", str(index))
        self.change_sub_setting(self.spin_button_11, index)
        return True

    def spin_button_12_clicked(self):
        num = self.spin_button_12_get_index()
        num = num % 2 + 1
        self.spin_button_12_set_index(num)

    def spin_button_12_get_index(self):
        if self.spin_button_12.text():
            return self.language_sequence.index(self.spin_button_12.text()) + 1
        return None

    def spin_button_12_set_index(self, index):
        if index <= len(self.language_sequence):
            self.spin_button_12.setText(self.language_sequence[index - 1])
            config.set("SoundRandomization", "iDialoguesLanguage", str(index))
            self.change_sub_setting(self.spin_button_12, index)
            return True
        return False

    def spin_button_13_clicked(self):
        num = self.spin_button_13_get_index()
        num = num % 3 + 1
        self.spin_button_13_set_index(num)

    def spin_button_13_get_index(self):
        if self.spin_button_13.text():
            return int(self.spin_button_13.text())
        return None

    def spin_button_13_set_index(self, index):
        self.spin_button_13.setText(str(index))
        config.set("ExtraRandomization", "iBloodlessCandlesComplexity", str(index))
        self.change_sub_setting(self.spin_button_13, index)
        return True
    
    def radio_button_group_1_checked(self):
        if self.radio_button_1.isChecked():
            config.set("GameDifficulty", "bNormal", "true")
            config.set("GameDifficulty", "bHard", "false")
            config.set("GameDifficulty", "bNightmare", "false")
        elif self.radio_button_2.isChecked():
            config.set("GameDifficulty", "bNormal", "false")
            config.set("GameDifficulty", "bHard", "true")
            config.set("GameDifficulty", "bNightmare", "false")
        else:
            config.set("GameDifficulty", "bNormal", "false")
            config.set("GameDifficulty", "bHard", "false")
            config.set("GameDifficulty", "bNightmare", "true")
    
    def radio_button_group_6_checked(self):
        if self.radio_button_14.isChecked():
            self.level_box.setVisible(False)
            config.set("SpecialMode", "bNone", "true")
            config.set("SpecialMode", "bCustomNG", "false")
            config.set("SpecialMode", "bProgressiveZ", "false")
        elif self.radio_button_5.isChecked():
            self.level_box.setVisible(True)
            config.set("SpecialMode", "bNone", "false")
            config.set("SpecialMode", "bCustomNG", "true")
            config.set("SpecialMode", "bProgressiveZ", "false")
            #Fix background
            self.fix_background_glitch()
        else:
            self.level_box.setVisible(False)
            config.set("SpecialMode", "bNone", "false")
            config.set("SpecialMode", "bCustomNG", "false")
            config.set("SpecialMode", "bProgressiveZ", "true")
    
    def fix_background_glitch(self):
        try:
            self.dummy_box.setStyleSheet("")
            QApplication.processEvents()
            self.setPalette(self.palette)
        except TypeError:
            return
    
    def preset_drop_down_change(self, index):
        current = self.preset_drop_down.itemText(index)
        if current == "Custom":
            return
        main_num = preset_to_bytes[current]
        sub_num = self.get_setting_bytes()[1]
        self.set_setting_bytes(main_num, sub_num)

    def matches_preset(self):
        main_num = self.get_setting_bytes()[0]
        if main_num in bytes_to_preset:
            self.preset_drop_down.setCurrentText(bytes_to_preset[main_num])
            return
        self.preset_drop_down.setCurrentText("Custom")
    
    def new_start(self, text):
        config.set("StartWith", "sStartItem", text)
    
    def new_setting(self, text):
        #Check that input is valid hex
        try:
            total_num = self.get_setting_bytes()
        except ValueError:
            total_num = (0, 0)
        main_num = total_num[0]
        sub_num = total_num[1]
        self.set_setting_bytes(main_num, sub_num)
        #Apply bytes to settings
        for widget in main_widget_to_setting:
            if (main_num & main_widget_to_setting[widget] != 0) != widget.isChecked():
                widget.setChecked(not widget.isChecked())
        for widget in sub_widget_to_setting:
            check = False
            index = getattr(self, widget.accessibleName() + "_get_index")()
            if not index:
                continue
            for num in range(2):
                if sub_num & sub_widget_to_setting[widget]*0x1000**num != 0:
                    check = True
                    if index != shift_to_spin_index[num]:
                        check = getattr(self, widget.accessibleName() + "_set_index")(shift_to_spin_index[num])
            if not check and index != 2:
                getattr(self, widget.accessibleName() + "_set_index")(2)
    
    def add_main_setting(self, widget):
        total_num = self.get_setting_bytes()
        main_num = total_num[0]
        sub_num = total_num[1]
        extra_num = main_widget_to_setting[widget]
        if main_num & extra_num == 0:
            main_num += extra_num
        self.set_setting_bytes(main_num, sub_num)
    
    def remove_main_setting(self, widget):
        total_num = self.get_setting_bytes()
        main_num = total_num[0]
        sub_num = total_num[1]
        extra_num = main_widget_to_setting[widget]
        if main_num & extra_num != 0:
            main_num -= extra_num
        self.set_setting_bytes(main_num, sub_num)
    
    def change_sub_setting(self, widget, index):
        total_num = self.get_setting_bytes()
        main_num = total_num[0]
        sub_num = total_num[1]
        extra_num = sub_widget_to_setting[widget]
        for num in range(2):
            abs_num = extra_num*0x1000**num
            if num == spin_index_to_shift[index]:
                if sub_num & abs_num == 0:
                    sub_num += abs_num
            else:
                if sub_num & abs_num != 0:
                    sub_num -= abs_num
        self.set_setting_bytes(main_num, sub_num)
    
    def get_setting_bytes(self):
        total_num = int(self.setting_field.text(), 16)
        factor = 0x10**main_setting_length
        return (total_num % factor, total_num // factor)
    
    def set_setting_bytes(self, main_num, sub_num):
        factor = 0x10**main_setting_length
        total_num = main_num + sub_num*factor
        self.setting_field.setText(self.setting_format.format(total_num).upper())
    
    def new_level(self):
        config.set("SpecialMode", "iCustomNGLevel", str(self.level_box.value()))
    
    def new_output(self, text):
        config.set("Misc", "sGamePath", text)
    
    def new_seed(self, text):
        if " " in text:
            self.seed_field.setText(text.replace(" ", ""))
        else:
            config.set("Misc", "sSeed", text)
    
    def cast_seed(self, seed):
        #Cast seed to another object type if possible
        #By default it is a string
        seed = str(seed)
        try:
            if "." in seed:
                return float(seed)
            else:
                return int(seed)
        except ValueError:
            return seed
    
    def add_to_list(self, filetype, file, checkboxes):
        list   = modified_files[filetype]["Files"]
        change = True
        for checkbox in checkboxes:
            if checkbox.isChecked():
                change = False
        if change and not file in list:
            list.append(file)
            self.label_change(filetype)
    
    def remove_from_list(self, filetype, file, checkboxes):
        list   = modified_files[filetype]["Files"]
        change = True
        for checkbox in checkboxes:
            if checkbox.isChecked():
                change = False
        if change and file in list:
            list.remove(file)
            self.label_change(filetype)
    
    def label_change(self, filetype):
        files  = modified_files[filetype]["Files"]
        label  = modified_files[filetype]["Label"]
        string = "Modified " + filetype + ":\n\n"
        files.sort()
        for file in files:
            string += file + "\n"
        label.setText(string)
    
    def check_rando_options(self):
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            return True
        if config.getboolean("ItemRandomization", "bShopPool"):
            return True
        if config.getboolean("ItemRandomization", "bQuestPool"):
            return True
        if config.getboolean("ItemRandomization", "bQuestRequirements"):
            return True
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"):
            return True
        if config.getboolean("LibraryRandomization", "bMapRequirements"):
            return True
        if config.getboolean("LibraryRandomization", "bTomeAppearance"):
            return True
        if config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"):
            return True
        if config.getboolean("EquipmentRandomization", "bGlobalGearStats"):
            return True
        if config.getboolean("EquipmentRandomization", "bCheatGearStats"):
            return True
        if config.getboolean("EnemyRandomization", "bEnemyLocations"):
            return True
        if config.getboolean("EnemyRandomization", "bEnemyLevels"):
            return True
        if config.getboolean("EnemyRandomization", "bBossLevels"):
            return True
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            return True
        if config.getboolean("EnemyRandomization", "bBossTolerances"):
            return True
        if config.getboolean("MapRandomization", "bRoomLayout"):
            return True
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            return True
        if config.getboolean("GraphicRandomization", "bZangetsuColor"):
            return True
        if config.getboolean("GraphicRandomization", "bBackerPortraits"):
            return True
        if config.getboolean("SoundRandomization", "bDialogues"):
            return True
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            return True
        return False

    def generate_pak(self):
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Initializing...", None, 0, 7, self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.worker = Generate(self.progress_bar, self.seed, self.map, self.start_items)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(self.generate_finished)
        self.worker.signaller.error.connect(self.thread_failure)
        self.worker.start()
    
    def import_assets(self, asset_list, finished):
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Importing assets...", None, 0, len(asset_list), self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.worker = Import(asset_list)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(finished)
        self.worker.signaller.error.connect(self.thread_failure)
        self.worker.start()
    
    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def generate_finished(self):
        self.end_thread()
        box = QMessageBox(self)
        box.setWindowTitle("Done")
        text = "Pak file generated !"
        box.setText(text)
        box.exec()
    
    def import_finished(self):
        self.setEnabled(True)
    
    def update_finished(self):
        sys.exit()
    
    def browse_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.output_field.setText(path.replace("/", "\\"))
    
    def setting_button_clicked(self):
        if config.getfloat("Misc", "fWindowSize") == 0.8 and self.size_drop_down.currentIndex() == 0 or config.getfloat("Misc", "fWindowSize") == 0.9 and self.size_drop_down.currentIndex() == 1 or config.getfloat("Misc", "fWindowSize") == 1.0 and self.size_drop_down.currentIndex() == 2:
            self.box.close()
        else:
            if self.size_drop_down.currentIndex() == 0:
                config.set("Misc", "fWindowSize", "0.8")
            elif self.size_drop_down.currentIndex() == 1:
                config.set("Misc", "fWindowSize", "0.9")
            elif self.size_drop_down.currentIndex() == 2:
                config.set("Misc", "fWindowSize", "1.0")
            writing()
            subprocess.Popen(script_name + ".exe")
            sys.exit()
    
    def seed_button_1_clicked(self):
        self.seed_field.setText(str(random.randint(1000000000, 9999999999)))
    
    def seed_button_3_clicked(self):
        #Check seed
        
        if not config.get("Misc", "sSeed"):
            return
        self.seed_test = self.cast_seed(config.get("Misc", "sSeed"))
        self.map_test = self.map
        
        #Start
        
        try:
            Manager.init()
            Manager.load_constant()
            
            Item.init()
            Enemy.init()
            Room.init()
            Bloodless.init()
            
            Item.set_logic_complexity(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
            Bloodless.set_logic_complexity(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
            
            random.seed(self.seed_test)
            if self.map_test:
                pass
            elif config.getboolean("MapRandomization", "bRoomLayout"):
                if glob.glob("MapEdit\\Custom\\*.json"):
                    self.map_test = random.choice(glob.glob("MapEdit\\Custom\\*.json"))
                else:
                    self.map_test = ""
            else:
                self.map_test = ""
            Manager.load_map(self.map_test)
            Room.get_map_info()
            
            if not config.getboolean("GameDifficulty", "bNormal"):
                Item.set_hard_mode()
            
            if config.getboolean("EnemyRandomization", "bEnemyLocations"):
                random.seed(self.seed_test)
                Enemy.randomize_enemy_locations()
            
            Item.fill_enemy_to_room()
            
            if config.getboolean("ItemRandomization", "bOverworldPool"):
                random.seed(self.seed_test)
                Item.key_logic()
            
            if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
                random.seed(self.seed_test)
                Bloodless.randomize_bloodless_candles()
            
            box = QMessageBox(self)
            box.setWindowTitle("Test")
            if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
                box.setText(Bloodless.create_log_string(self.seed_test, self.map_test))
            elif config.getboolean("ItemRandomization", "bOverworldPool"):
                box.setText(Item.create_log_string(self.seed_test, self.map_test, Enemy.enemy_replacement_invert))
            else:
                box.setText("No keys to randomize")
            box.exec()
        except Exception:
            self.error("An error has occured.\nCheck the command window for more detail.")
            raise
    
    def seed_button_2_clicked(self):
        if not config.get("Misc", "sSeed"):
            return
        self.seed = self.cast_seed(config.get("Misc", "sSeed"))
        self.seed_box.close()
    
    def button_3_clicked(self):
        self.box = QDialog(self)
        self.box.setLayout(self.setting_layout)
        self.box.setWindowTitle("Settings")
        self.box.exec()
        
        if config.getfloat("Misc", "fWindowSize") == 0.8:
            self.size_drop_down.setCurrentIndex(0)
        elif config.getfloat("Misc", "fWindowSize") == 0.9:
            self.size_drop_down.setCurrentIndex(1)
        elif config.getfloat("Misc", "fWindowSize") == 1.0:
            self.size_drop_down.setCurrentIndex(2)

    def button_4_clicked(self):
        path = QFileDialog.getOpenFileName(parent=self, caption="Open", dir="MapEdit//Custom", filter="*.json")[0]
        if path:
            self.map = path.replace("/", "\\")
            self.setWindowTitle("Randomizer (" + self.map + ")")
            self.add_to_list("UI", "icon_8bitCrown"    , [self.check_box_12])
            self.add_to_list("UI", "Map_Icon_Keyperson", [self.check_box_12])
            self.add_to_list("UI", "Map_Icon_RootBox"  , [self.check_box_12])
            self.add_to_list("UI", "Map_StartingPoint" , [self.check_box_12])

    def button_5_clicked(self):
        #Check if path is valid
        
        if not config.get("Misc", "sGamePath") or not os.path.isdir(config.get("Misc", "sGamePath")) or config.get("Misc", "sGamePath").split("\\")[-1] != "Paks":
            self.error("Game path invalid, input the path to your game's data\n(...\BloodstainedRotN\Content\Paks).")
            return
        
        #Check if starting items are valid
        
        self.start_items = []
        for item in config.get("StartWith", "sStartItem").split("|"):
            if not item:
                continue
            simple_name = Utility.simplify_item_name(item)
            if not simple_name in Manager.start_item_translation:
                self.error("Starting item name invalid.")
                return
            item_name = Manager.start_item_translation[simple_name]
            if "Skilled" in item_name:
                self.start_items.append(item_name.replace("Skilled", ""))
            self.start_items.append(item_name)
        self.start_items = list(dict.fromkeys(self.start_items))
        
        #Prompt seed options
        
        self.seed = ""
        if self.check_rando_options():
            self.seed_box = QDialog(self)
            self.seed_box.setLayout(self.seed_layout)
            self.seed_box.setWindowTitle("Seed")
            self.seed_box.exec()
            if not self.seed:
                return
        
        #Check if every asset is already cached
        
        if os.path.isdir(Manager.asset_dir): 
            cached_assets = []
            for root, dirs, files in os.walk(Manager.asset_dir):
                for file in files:
                    name, extension = os.path.splitext(file)
                    cached_assets.append(name)
            cached_assets = list(dict.fromkeys(cached_assets))
            asset_list = []
            for file in Manager.file_to_path:
                if not file in cached_assets:
                    asset_list.append(file)
        else:
            asset_list = list(Manager.file_to_path)
        if asset_list:
            self.import_assets(asset_list, self.generate_pak)
        else:
            self.generate_pak()
    
    def button_6_clicked(self):
        #Check if path is valid
        
        if not config.get("Misc", "sGamePath") or not os.path.isdir(config.get("Misc", "sGamePath")) or config.get("Misc", "sGamePath").split("\\")[-1] != "Paks":
            self.error("Game path invalid, input the path to your game's data\n(...\BloodstainedRotN\Content\Paks).")
            return
        
        #Start
        
        self.import_assets(list(Manager.file_to_path), self.import_finished)
    
    def button_7_clicked(self):
        label1_image = QLabel()
        label1_image.setPixmap(QPixmap("Data\\profile1.png"))
        label1_image.setScaledContents(True)
        label1_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label1_text = QLabel()
        label1_text.setText("<span style=\"font-weight: bold; color: #67aeff;\">Lakifume</span><br/>Author of True Randomization<br/><a href=\"https://github.com/Lakifume\"><font face=Cambria color=#67aeff>Github</font></a>")
        label1_text.setOpenExternalLinks(True)
        label2_image = QLabel()
        label2_image.setPixmap(QPixmap("Data\\profile2.png"))
        label2_image.setScaledContents(True)
        label2_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label2_text = QLabel()
        label2_text.setText("<span style=\"font-weight: bold; color: #e91e63;\">FatihG_</span><br/>Founder of Bloodstained Modding<br/><a href=\"http://discord.gg/b9XBH4f\"><font face=Cambria color=#e91e63>Discord</font></a>")
        label2_text.setOpenExternalLinks(True)
        label3_image = QLabel()
        label3_image.setPixmap(QPixmap("Data\\profile3.png"))
        label3_image.setScaledContents(True)
        label3_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label3_text = QLabel()
        label3_text.setText("<span style=\"font-weight: bold; color: #e6b31a;\">Joneirik</span><br/>Datatable researcher<br/><a href=\"http://wiki.omf2097.com/doku.php?id=joneirik:bs:start\"><font face=Cambria color=#e6b31a>Wiki</font></a>")
        label3_text.setOpenExternalLinks(True)
        label4_image = QLabel()
        label4_image.setPixmap(QPixmap("Data\\profile4.png"))
        label4_image.setScaledContents(True)
        label4_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label4_text = QLabel()
        label4_text.setText("<span style=\"font-weight: bold; color: #db1ee9;\">Atenfyr</span><br/>Creator of UAssetAPI<br/><a href=\"https://github.com/atenfyr/UAssetAPI\"><font face=Cambria color=#db1ee9>Github</font></a>")
        label4_text.setOpenExternalLinks(True)
        label5_image = QLabel()
        label5_image.setPixmap(QPixmap("Data\\profile5.png"))
        label5_image.setScaledContents(True)
        label5_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label5_text = QLabel()
        label5_text.setText("<span style=\"font-weight: bold; color: #25c04e;\">Giwayume</span><br/>Creator of Bloodstained Level Editor<br/><a href=\"https://github.com/Giwayume/BloodstainedLevelEditor\"><font face=Cambria color=#25c04e>Github</font></a>")
        label5_text.setOpenExternalLinks(True)
        label6_image = QLabel()
        label6_image.setPixmap(QPixmap("Data\\profile6.png"))
        label6_image.setScaledContents(True)
        label6_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label6_text = QLabel()
        label6_text.setText("<span style=\"font-weight: bold; color: #ffffff;\">Matyalatte</span><br/>Creator of UE4 DDS Tools<br/><a href=\"https://github.com/matyalatte/UE4-DDS-Tools\"><font face=Cambria color=#ffffff>Github</font></a>")
        label6_text.setOpenExternalLinks(True)
        label7_image = QLabel()
        label7_image.setPixmap(QPixmap("Data\\profile7.png"))
        label7_image.setScaledContents(True)
        label7_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label7_text = QLabel()
        label7_text.setText("<span style=\"font-weight: bold; color: #7b9aff;\">Chrisaegrimm</span><br/>Testing and suffering<br/><a href=\"https://www.twitch.tv/chrisaegrimm\"><font face=Cambria color=#7b9aff>Twitch</font></a>")
        label7_text.setOpenExternalLinks(True)
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1_image, 0, 0, 1, 1)
        layout.addWidget(label1_text , 0, 1, 1, 1)
        layout.addWidget(label2_image, 1, 0, 1, 1)
        layout.addWidget(label2_text , 1, 1, 1, 1)
        layout.addWidget(label3_image, 2, 0, 1, 1)
        layout.addWidget(label3_text , 2, 1, 1, 1)
        layout.addWidget(label4_image, 3, 0, 1, 1)
        layout.addWidget(label4_text , 3, 1, 1, 1)
        layout.addWidget(label5_image, 5, 0, 1, 1)
        layout.addWidget(label5_text , 5, 1, 1, 1)
        layout.addWidget(label6_image, 6, 0, 1, 1)
        layout.addWidget(label6_text , 6, 1, 1, 1)
        layout.addWidget(label7_image, 7, 0, 1, 1)
        layout.addWidget(label7_text , 7, 1, 1, 1)
        box = QDialog(self)
        box.setLayout(layout)
        box.setWindowTitle("Credits")
        box.exec()
    
    def end_thread(self):
        self.progress_bar.close()
        self.setEnabled(True)
    
    def thread_failure(self):
        self.end_thread()
        self.error("An error has occured.\nCheck the command window for more detail.")
    
    def error(self, text):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText(text)
        box.exec()
    
    def check_for_updates(self):
        if os.path.isfile("delete.me"):
            os.remove("delete.me")
        if os.path.isfile("Tools\\UAssetAPI\\delete1.me"):
            os.remove("Tools\\UAssetAPI\\delete1.me")
        if os.path.isfile("Tools\\UAssetAPI\\delete2.me"):
            os.remove("Tools\\UAssetAPI\\delete2.me")
        if os.path.isfile("Tools\\UAssetAPI\\delete3.me"):
            os.remove("Tools\\UAssetAPI\\delete3.me")
        try:
            api = requests.get("https://api.github.com/repos/Lakifume/True-Randomization/releases/latest").json()
        except requests.ConnectionError:
            self.check_for_resolution()
            return
        try:
            tag = api["tag_name"]
        except KeyError:
            self.check_for_resolution()
            return
        if tag != config.get("Misc", "sVersion"):
            choice = QMessageBox.question(self, "Auto Updater", "New version found:\n\n" + api["body"] + "\n\nUpdate ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                if "Map Editor.exe" in (program.name() for program in psutil.process_iter()):
                    self.error("MapEditor.exe is running, cannot overwrite.")
                    self.check_for_resolution()
                    return
                
                self.progress_bar = QProgressDialog("Downloading...", None, 0, api["assets"][0]["size"], self)
                self.progress_bar.setWindowTitle("Status")
                self.progress_bar.setWindowModality(Qt.WindowModal)
                self.progress_bar.setAutoClose(False)
                self.progress_bar.setAutoReset(False)
                
                self.worker = Update(self.progress_bar, api)
                self.worker.signaller.progress.connect(self.set_progress)
                self.worker.signaller.finished.connect(self.update_finished)
                self.worker.signaller.error.connect(self.thread_failure)
                self.worker.start()
            else:
                self.check_for_resolution()
        else:
            self.check_for_resolution()
    
    def check_for_resolution(self):
        if self.first_time:
            self.button_3_clicked()
        self.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(writing_and_exit)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()