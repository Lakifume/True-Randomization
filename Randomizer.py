import Manager
import Item
import Classic
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
import glob
import random
import zipfile
import requests
import subprocess
import configparser
import traceback
import psutil
import vdf
import textwrap

from enum import Enum

script_name = os.path.splitext(os.path.basename(__file__))[0]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

main_param_length = 6
sub_param_length = 6
main_widget_to_param = {}
sub_widget_to_param = {}
spin_index_to_shift = {1: 0, 2: 2, 3: 1}
shift_to_spin_index = {value: key for key, value in spin_index_to_shift.items()}
    
map_num = len(glob.glob("MapEdit\\Custom\\*.json"))
window_sizes = [720, 900, 1080]

preset_to_bytes = {
    "Empty": 0x000000,
    "Trial": 0x3807FF,
    "Race":  0x5806EF,
    "Meme":  0x7F3AAF,
    "Risk":  0x7FFFFF,
    "Blood": 0x980001
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
            "PB_DT_SetBonus",
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

def write_config():
    with open("Data\\config.ini", "w") as file_writer:
        config.write(file_writer)

def write_and_exit():
    write_config()
    sys.exit()

#Enums

class DLCType(Enum):
    IGA       = 0
    Shantae   = 1
    Succubus  = 2
    MagicGirl = 3
    Japanese  = 4
    Classic2  = 5

#Threads

class Signaller(QObject):
    progress = Signal(int)
    finished = Signal()
    error    = Signal(str)

class Generate(QThread):
    def __init__(self, progress_bar, selected_seed, selected_map, starting_items, owned_dlc):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.selected_seed = selected_seed
        self.selected_map = selected_map
        self.starting_items = starting_items
        self.owned_dlc = owned_dlc
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit(traceback.format_exc())

    def process(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Mod directory
        
        if os.path.isdir(Manager.mod_dir):
            shutil.rmtree(Manager.mod_dir)
        for directory in list(Manager.file_to_path.values()):
            if not os.path.isdir(f"{Manager.mod_dir}\\{directory}"):
                os.makedirs(f"{Manager.mod_dir}\\{directory}")
        
        #Log directory
        
        if os.path.isdir("Spoiler"):
            for file in os.listdir("Spoiler"):
                os.remove(f"Spoiler\\{file}")
        else:
            os.makedirs("Spoiler")
        
        #Open files
        
        self.progress_bar.setLabelText("Loading data...")
        
        Manager.init()
        Utility.init()
        Manager.load_game_data()
        Manager.load_constant()
        current += 1
        self.signaller.progress.emit(current)
        
        #Simplify data
        
        self.progress_bar.setLabelText("Processing data...")
        
        Manager.table_complex_to_simple()
        #Manager.debug_output_datatables()
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
        Classic.init()
        miriam_color = None
        zangetsu_color = None
        
        #Apply parameters
        
        Item.set_logic_complexity(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        Classic.set_logic_complexity(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        Item.set_shop_event_weight(config.getint("ItemRandomization", "iShopPoolWeight"))
        Shop.set_shop_price_weight(config.getint("ShopRandomization", "iItemCostAndSellingPriceWeight"))
        Classic.set_shop_price_weight(config.getint("ShopRandomization", "iItemCostAndSellingPriceWeight"))
        Library.set_requirement_weight(config.getint("LibraryRandomization", "iMapRequirementsWeight"))
        Shard.set_shard_power_weight(config.getint("ShardRandomization", "iShardPowerAndMagicCostWeight"))
        Equipment.set_global_stat_weight(config.getint("EquipmentRandomization", "iGlobalGearStatsWeight"))
        Enemy.set_enemy_level_weight(config.getint("EnemyRandomization", "iEnemyLevelsWeight"))
        Enemy.set_boss_level_weight(config.getint("EnemyRandomization", "iBossLevelsWeight"))
        Enemy.set_enemy_tolerance_weight(config.getint("EnemyRandomization", "iEnemyTolerancesWeight"))
        Enemy.set_boss_tolerance_weight(config.getint("EnemyRandomization", "iBossTolerancesWeight"))
        Sound.set_voice_language(config.getint("SoundRandomization", "iDialoguesLanguage"))
        Bloodless.set_logic_complexity(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
        
        #Map
        
        random.seed(self.selected_seed)
        if not self.selected_map and config.getboolean("MapRandomization", "bRoomLayout"):
            self.selected_map = random.choice(glob.glob("MapEdit\\Custom\\*.json")) if glob.glob("MapEdit\\Custom\\*.json") else ""
        Manager.load_map(self.selected_map)
        Room.get_map_info()
        Room.update_any_map()
        
        #Apply tweaks
        
        Manager.apply_default_tweaks()
        Shard.set_default_shard_power()
        Enemy.get_original_enemy_stats()
        if DLCType.Classic2 in self.owned_dlc:
            Classic.apply_default_tweaks()
        
        #Apply cheats
        
        if type(self.selected_seed) is str:
            for code in cheats:
                if code in self.selected_seed:
                    random.seed(self.selected_seed)
                    cheats[code]()
        
        #Datatables
        
        has_risky_option = (config.getboolean("EnemyRandomization", "bEnemyLevels") or config.getboolean("EnemyRandomization", "bBossLevels")) and not config.getboolean("SpecialMode", "bCustomNG")
        
        if self.selected_map:
            Room.update_custom_map()
            Enemy.rebalance_enemies_to_map()
        
        if not config.getboolean("GameDifficulty", "bNormal"):
            Item.set_hard_mode()
        
        if not DLCType.IGA in self.owned_dlc:
            Item.del_iga_dlc()
        elif not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_iga_dlc()
        
        if not DLCType.Shantae in self.owned_dlc:
            Item.del_shantae_dlc()
        elif not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_shantae_dlc()
        
        if not DLCType.Succubus in self.owned_dlc:
            Item.del_succubus_dlc()
        elif not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_succubus_dlc()
        
        if not DLCType.MagicGirl in self.owned_dlc:
            Item.del_magicgirl_dlc()
        elif not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_magicgirl_dlc()
        
        if not DLCType.Japanese in self.owned_dlc:
            Item.del_japanese_dlc()
        elif not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_japanese_dlc()
        
        if config.getboolean("EnemyRandomization", "bEnemyLocations"):
            random.seed(self.selected_seed)
            Enemy.randomize_enemy_locations()
            Enemy.update_enemy_locations()
            Enemy.restore_enemy_scaling()
        
        Item.fill_enemy_to_room()
        
        if config.getboolean("ItemRandomization", "bRemoveInfinites"):
            Item.remove_infinite_items()
        
        for item in self.starting_items:
            if config.getboolean("ItemRandomization", "bOverworldPool") and item == "Shortcut":
                continue
            Item.add_starting_item(item)
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.selected_seed)
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
            random.seed(self.selected_seed)
            Classic.randomize_candle_drops()
        
        if config.getboolean("ItemRandomization", "bOverworldPool") and DLCType.Classic2 in self.owned_dlc:
            random.seed(self.selected_seed)
            Classic.randomize_item_pool()
            Classic.randomize_shop_pool()
        
        if config.getboolean("ItemRandomization", "bOverworldPool") or config.getboolean("EnemyRandomization", "bEnemyLocations") or self.selected_map:
            Manager.remove_fire_shard_requirement()
        
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            random.seed(self.selected_seed)
            Bloodless.randomize_bloodless_candles()
            if self.selected_map:
                Bloodless.remove_gremory_cutscene()
        
        if config.getboolean("ItemRandomization", "bQuestPool"):
            random.seed(self.selected_seed)
            Item.randomize_quest_rewards()
        
        if config.getboolean("ItemRandomization", "bShopPool"):
            random.seed(self.selected_seed)
            Item.randomize_shop_items()
        
        if config.getboolean("ItemRandomization", "bQuestRequirements"):
            random.seed(self.selected_seed)
            Item.randomize_quest_requirements()
            Item.update_catering_quest_info()
        
        if self.selected_map:
            Item.replace_silver_bromide()
            Item.remove_enemy_quest_icons()
        
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"):
            random.seed(self.selected_seed)
            Shop.randomize_shop_prices(config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"))
        
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice") and DLCType.Classic2 in self.owned_dlc:
            random.seed(self.selected_seed)
            Classic.randomize_shop_prices(config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"))
        
        if config.getboolean("LibraryRandomization", "bMapRequirements"):
            random.seed(self.selected_seed)
            Library.randomize_library_requirements()
        
        if config.getboolean("LibraryRandomization", "bTomeAppearance"):
            random.seed(self.selected_seed)
            Library.randomize_tome_appearance()
        
        if config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"):
            random.seed(self.selected_seed)
            Shard.randomize_shard_power(config.getboolean("ShardRandomization", "bScaleMagicCostWithPower"))
        
        if config.getboolean("EquipmentRandomization", "bGlobalGearStats"):
            random.seed(self.selected_seed)
            Equipment.randomize_equipment_stats()
            Equipment.randomize_weapon_power()
        
        if config.getboolean("EquipmentRandomization", "bCheatGearStats"):
            random.seed(self.selected_seed)
            Equipment.randomize_cheat_equipment_stats()
            Equipment.randomize_cheat_weapon_power()
        
        if config.getboolean("EnemyRandomization", "bEnemyLevels"):
            random.seed(self.selected_seed)
            Enemy.randomize_enemy_levels()
        
        if config.getboolean("EnemyRandomization", "bBossLevels"):
            random.seed(self.selected_seed)
            Enemy.randomize_boss_levels()
        
        if has_risky_option:
            Enemy.increase_starting_stats()
            #Bloodless.increase_starting_stats()
        
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            random.seed(self.selected_seed)
            Enemy.randomize_enemy_tolerances()
        
        if config.getboolean("EnemyRandomization", "bBossTolerances"):
            random.seed(self.selected_seed)
            Enemy.randomize_boss_tolerances()
        
        if config.getboolean("GraphicRandomization", "bOutfitColor"):
            miriam_outfit_list = config.get("OutfitConfig", "sMiriamList").split(",")
            random.seed(self.selected_seed)
            miriam_color = random.choice(miriam_outfit_list) if miriam_outfit_list else None
            zangetsu_outfit_list = config.get("OutfitConfig", "sZangetsuList").split(",")
            random.seed(self.selected_seed)
            zangetsu_color = random.choice(zangetsu_outfit_list) if zangetsu_outfit_list else None
            if miriam_color:
                Graphic.update_default_outfit_hsv(miriam_color)
        
        if config.getboolean("GraphicRandomization", "bBackerPortraits"):
            random.seed(self.selected_seed)
            Graphic.randomize_backer_portraits()
        
        if config.getboolean("SoundRandomization", "bDialogues"):
            random.seed(self.selected_seed)
            Sound.randomize_dialogues()
        
        if config.getboolean("SoundRandomization", "bDialogues") and DLCType.Classic2 in self.owned_dlc:
            random.seed(self.selected_seed)
            Classic.randomize_dialogues()
        
        if config.getboolean("SoundRandomization", "bBackGroundMusic"):
            random.seed(self.selected_seed)
            Sound.randomize_music()
        
        #Change some in-game properties based on the difficulty chosen
        if config.getboolean("GameDifficulty", "bNormal"):
            Manager.set_single_difficulty("Normal")
            Enemy.update_brv_damage("Normal")
            if DLCType.Classic2 in self.owned_dlc:
                Classic.set_easy_mode()
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
            if DLCType.Classic2 in self.owned_dlc:
                Classic.set_hard_mode()
        
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
        if self.selected_map:
            Room.update_map_indicators()
        
        #Display game version, mod version and seed on the title screen
        Manager.show_mod_stats(str(self.selected_seed), config.get("Misc", "sVersion"))
        
        #Write the spoiler logs
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            Manager.write_log("KeyLocation", Bloodless.create_log(self.selected_seed, self.selected_map))
        elif config.getboolean("ItemRandomization", "bOverworldPool"):
            Manager.write_log("KeyLocation", Item.create_log(self.selected_seed, self.selected_map))
        if config.getboolean("ItemRandomization", "bOverworldPool") and DLCType.Classic2 in self.owned_dlc:
            Manager.write_log("Classic2Keys", Classic.create_log())
        
        if config.getboolean("LibraryRandomization", "bMapRequirements") or config.getboolean("LibraryRandomization", "bTomeAppearance"):
            Manager.write_log("LibraryTomes", Library.create_log())
        
        if has_risky_option or config.getboolean("EnemyRandomization", "bEnemyLocations") or config.getboolean("EnemyRandomization", "bEnemyTolerances") or config.getboolean("EnemyRandomization", "bBossTolerances"):
            Manager.write_log("EnemyProperties", Enemy.create_log())
        
        #Add and import any mesh files found in the mesh directory
        for directory in os.listdir("Data\\Mesh"):
            file_name, extension = os.path.splitext(directory)
            if extension == ".uasset":
                Graphic.import_mesh(file_name)
        
        #Add new armor references defined in the json
        for item in Manager.constant["ArmorReference"]:
            Equipment.add_armor_reference(item)
        
        #Add and import any music files found in the music directory
        for directory in os.listdir("Data\\Music"):
            file_name = os.path.splitext(directory)[0]
            Sound.add_music_file(file_name)
        
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
        if self.selected_map:
            Graphic.import_texture("icon_map_journey_")
            Graphic.import_texture("Map_Icon_Keyperson")
            Graphic.import_texture("Map_Icon_RootBox")
            Graphic.import_texture("Map_StartingPoint")
        if self.selected_map or config.getboolean("ItemRandomization", "bOverworldPool"):
            Graphic.import_texture("icon_8bitCrown")
        
        #Import chosen hues for Miriam and Zangetsu
        #While it is technically not necessary to first copy the textures out of the chosen folder we do it so that the random hue does not show up on the terminal
        if miriam_color:
            for texture in os.listdir(f"Data\\Texture\\Miriam\\{miriam_color}"):
                shutil.copyfile(f"Data\\Texture\\Miriam\\{miriam_color}\\{texture}", f"Data\\Texture\\{texture}")
            
            Graphic.import_texture("Face_Miriam")
            Graphic.import_texture("T_Pl01_Cloth_Bace")
            Graphic.import_texture("T_Body01_01_Color")
            
            for texture in os.listdir(f"Data\\Texture\\Miriam\\{miriam_color}"):
                os.remove(f"Data\\Texture\\{texture}")
        
        if zangetsu_color:
            for texture in os.listdir(f"Data\\Texture\\Zangetsu\\{zangetsu_color}"):
                shutil.copyfile(f"Data\\Texture\\Zangetsu\\{zangetsu_color}\\{texture}", f"Data\\Texture\\{texture}")
            
            Graphic.import_texture("Face_Zangetsu")
            Graphic.import_texture("T_N1011_body_color")
            Graphic.import_texture("T_N1011_face_color")
            Graphic.import_texture("T_N1011_weapon_color")
            Graphic.import_texture("T_Tknife05_Base")
            
            for texture in os.listdir(f"Data\\Texture\\Zangetsu\\{zangetsu_color}"):
                os.remove(f"Data\\Texture\\{texture}")
        
        Graphic.update_backer_portraits()
        
        #Clean up the mod folder
        
        Manager.remove_unchanged_files()
        current += 1
        self.signaller.progress.emit(current)
        
        #UnrealPak
        
        self.progress_bar.setLabelText("Packing files...")
        
        with open("Tools\\UnrealPak\\filelist.txt", "w") as file_writer:
            file_writer.write("\"Mod\\*.*\" \"..\\..\\..\\*.*\" \n")
        
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
        
        if not os.path.isdir(config.get("Misc", "sGamePath") + "\\BloodstainedRotN\\Content\\Paks\\~mods"):
            os.makedirs(config.get("Misc", "sGamePath") + "\\BloodstainedRotN\\Content\\Paks\\~mods")
        shutil.move("Tools\\UnrealPak\\Randomizer.pak", config.get("Misc", "sGamePath") + "\\BloodstainedRotN\\Content\\Paks\\~mods\\Randomizer.pak")
        
        #Copy UE4SS
        
        exe_directory = config.get("Misc", "sGamePath") + "\\BloodstainedRotN\\Binaries\\Win64"
        if not os.path.isfile(f"{exe_directory}\\UE4SS.dll"):
            for item in os.listdir("Tools\\UE4SS"):
                if os.path.isfile(f"Tools\\UE4SS\\{item}"):
                    shutil.copyfile(f"Tools\\UE4SS\\{item}", f"{exe_directory}\\{item}")
                if os.path.isdir(f"Tools\\UE4SS\\{item}"):
                    shutil.copytree(f"Tools\\UE4SS\\{item}", f"{exe_directory}\\{item}", dirs_exist_ok=True)
        for directory in os.listdir("Data\\UE4SS"):
            shutil.copytree(f"Data\\UE4SS\\{directory}", f"{exe_directory}\\Mods\\{directory}", dirs_exist_ok=True)
            if not os.path.isfile(f"{exe_directory}\\Mods\\{directory}\\enabled.txt"): 
                open(f"{exe_directory}\\Mods\\{directory}\\enabled.txt", "w").close()
        
        #User randomly chosen mod
        
        if os.path.isdir("Data\\Mod"):
            for directory in os.listdir("Data\\Mod"):
                chosen_mod = random.choice(glob.glob(f"Data\\Mod\\{directory}\\*.pak"))
                shutil.copyfile(chosen_mod, config.get("Misc", "sGamePath") + f"\\BloodstainedRotN\\Content\\Paks\\~mods\\{directory}.pak")
        
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
            self.signaller.error.emit(traceback.format_exc())

    def process(self):
        current = 0
        zip_name = "True Randomization.zip"
        exe_name = f"{script_name}.exe"
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
        shutil.rmtree("Tools\\UE4SS")
        shutil.rmtree("Tools\\UModel")
        shutil.rmtree("Tools\\UnrealPak")
        
        #Extract
        
        os.rename(exe_name, "delete.me")
        os.rename("Tools\\UAssetAPI\\Newtonsoft.Json.dll", "Tools\\UAssetAPI\\delete1.me")
        os.rename("Tools\\UAssetAPI\\UAssetAPI.dll",       "Tools\\UAssetAPI\\delete2.me")
        os.rename("Tools\\UAssetAPI\\UAssetSnippet.dll",   "Tools\\UAssetAPI\\delete3.me")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall("")
        os.remove(zip_name)
        
        #Carry previous config params
        
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
            self.signaller.error.emit(traceback.format_exc())

    def process(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Extract specific assets from the game's pak using UModel
        
        if os.path.isdir(Manager.asset_dir) and self.asset_list == list(Manager.file_to_path):
            shutil.rmtree(Manager.asset_dir)
        
        #There's a limit of around 8000 characters per command, split the list of packages into multiple batches of maximum 7500 characters
        packages = " ".join([f"-pkg=\"{Manager.asset_dir}\\{Manager.file_to_path[asset]}\\{asset}\"" for asset in self.asset_list])
        batches = textwrap.wrap(packages, 7500)
        output_path = os.path.abspath("")
        
        root = os.getcwd()
        os.chdir("Tools\\UModel")
        for batch in batches:
            os.system("cmd /c umodel_64.exe -path=\"" + config.get("Misc", "sGamePath") + f"\\BloodstainedRotN\\Content\\Paks\" -out=\"{output_path}\" -save {batch}")
            current += batch.count(" ") + 1
            self.signaller.progress.emit(current)
        os.chdir(root)
        
        self.signaller.finished.emit()

#GUI

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        sys.excepthook = self.exception_hook
        self.setEnabled(False)
        self.init()
        if not self.check_for_updates():
            self.check_for_resolution()

    def init(self):
        
        self.first_time = False
        if not config.getint("Misc", "iWindowSize") in window_sizes:
            config.set("Misc", "iWindowSize", str(window_sizes[-1]))
            self.first_time = True
        self.size_multiplier = config.getint("Misc", "iWindowSize")/1080
        
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: " + str(int(self.size_multiplier*18)) + "px}"
        + "QGraphicsView{border-image: url(MapEdit/Data/background.png)}"
        + "QComboBox{background-color: #21222e; selection-background-color: #320288ff}"
        + "QComboBox QAbstractItemView{border: 1px solid #21222e}"
        + "QScrollBar::add-page{background-color: #1b1c26}"
        + "QScrollBar::sub-page{background-color: #1b1c26}"
        + "QMenu{background-color: #21222e; margin: 4px}"
        + "QMenu::item{padding: 2px 4px 2px 4px}"
        + "QMenu::item:selected{background: #320288ff}"
        + "QMenu::item:pressed{border: 1px solid #640288ff}" 
        + "QDialog{background-color: #21222e}"
        + "QMessageBox{background-color: #21222e}"
        + "QPushButton{background-color: #21222e}"
        + "QProgressDialog{background-color: #21222e}"
        + "QProgressBar{border: 2px solid white; text-align: center; font: bold}"
        + "QSpinBox{background-color: #21222e; selection-background-color: #320288ff}"
        + "QLineEdit{background-color: #21222e; selection-background-color: #320288ff}"
        + "QListWidget{background-color: #21222e; border: 1px solid #21222e}"
        + "QListWidget::item:selected:!active{background-color: #320288ff; color: #ffffff}"
        + "QToolTip{border: 1px solid white; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: " + str(int(self.size_multiplier*18)) + "px}")
        
        #Main layout
        
        main_window_layout = QHBoxLayout()
        main_window_layout.setSpacing(self.size_multiplier*10)
        self.setLayout(main_window_layout)

        #Left Label

        artwork_label = QLabel()
        artwork_label.setStyleSheet("border: 1px solid white")
        artwork_label.setPixmap(QPixmap("Data\\artwork.png"))
        artwork_label.setScaledContents(True)
        artwork_label.setFixedSize(self.size_multiplier*550, self.size_multiplier*978)
        main_window_layout.addWidget(artwork_label)
        
        #Center widget
        
        center_widget_layout = QGridLayout()
        center_widget_layout.setSpacing(self.size_multiplier*10)
        main_window_layout.addLayout(center_widget_layout)
        
        #Groupboxes

        center_box_1_layout = QGridLayout()
        self.center_box_1 = QGroupBox("Item Randomization")
        self.center_box_1.setLayout(center_box_1_layout)
        center_widget_layout.addWidget(self.center_box_1, 0, 0, 2, 2)

        center_box_2_layout = QGridLayout()
        self.center_box_2 = QGroupBox("Shop Randomization")
        self.center_box_2.setLayout(center_box_2_layout)
        center_widget_layout.addWidget(self.center_box_2, 2, 0, 1, 2)

        center_box_3_layout = QGridLayout()
        self.center_box_3 = QGroupBox("Library Randomization")
        self.center_box_3.setLayout(center_box_3_layout)
        center_widget_layout.addWidget(self.center_box_3, 3, 0, 1, 2)

        center_box_4_layout = QGridLayout()
        self.center_box_4 = QGroupBox("Shard Randomization")
        self.center_box_4.setLayout(center_box_4_layout)
        center_widget_layout.addWidget(self.center_box_4, 4, 0, 1, 2)

        center_box_5_layout = QGridLayout()
        self.center_box_5 = QGroupBox("Equipment Randomization")
        self.center_box_5.setLayout(center_box_5_layout)
        center_widget_layout.addWidget(self.center_box_5, 5, 0, 1, 2)

        center_box_6_layout = QGridLayout()
        self.center_box_6 = QGroupBox("Enemy Randomization")
        self.center_box_6.setLayout(center_box_6_layout)
        center_widget_layout.addWidget(self.center_box_6, 0, 2, 2, 2)

        center_box_7_layout = QGridLayout()
        self.center_box_7 = QGroupBox("Map Randomization")
        self.center_box_7.setLayout(center_box_7_layout)
        center_widget_layout.addWidget(self.center_box_7, 2, 2, 1, 2)

        center_box_8_layout = QGridLayout()
        self.center_box_8 = QGroupBox("Graphic Randomization")
        self.center_box_8.setLayout(center_box_8_layout)
        center_widget_layout.addWidget(self.center_box_8, 3, 2, 1, 2)

        center_box_9_layout = QGridLayout()
        self.center_box_9 = QGroupBox("Sound Randomization")
        self.center_box_9.setLayout(center_box_9_layout)
        center_widget_layout.addWidget(self.center_box_9, 4, 2, 1, 2)
        
        center_box_10_layout = QGridLayout()
        self.center_box_10 = QGroupBox("Extra Randomization")
        self.center_box_10.setLayout(center_box_10_layout)
        center_widget_layout.addWidget(self.center_box_10, 5, 2, 1, 2)
        
        center_box_16_layout = QGridLayout()
        center_box_16 = QGroupBox("Start With")
        center_box_16.setLayout(center_box_16_layout)
        center_widget_layout.addWidget(center_box_16, 7, 0, 1, 2)
        
        center_box_11_layout = QGridLayout()
        center_box_11 = QGroupBox("Game Difficulty")
        center_box_11.setLayout(center_box_11_layout)
        center_widget_layout.addWidget(center_box_11, 6, 0, 1, 2)
        
        center_box_17_layout = QGridLayout()
        center_box_17 = QGroupBox("Special Mode")
        center_box_17.setLayout(center_box_17_layout)
        center_widget_layout.addWidget(center_box_17, 6, 2, 1, 2)
        
        center_box_12_layout = QGridLayout()
        center_box_12 = QGroupBox("Presets")
        center_box_12.setLayout(center_box_12_layout)
        center_widget_layout.addWidget(center_box_12, 8, 0, 1, 2)
        
        center_box_13_layout = QGridLayout()
        center_box_13 = QGroupBox("Parameter String")
        center_box_13.setLayout(center_box_13_layout)
        center_widget_layout.addWidget(center_box_13, 7, 2, 1, 2)
        
        center_box_14_layout = QGridLayout()
        self.center_box_14 = QGroupBox("Game Path")
        self.center_box_14.setLayout(center_box_14_layout)
        center_widget_layout.addWidget(self.center_box_14, 8, 2, 1, 2)
        
        #Right label
        
        modified_file_label = QGroupBox()
        modified_file_label.setFixedSize(self.size_multiplier*550, self.size_multiplier*978)
        main_window_layout.addWidget(modified_file_label)
        
        modified_file_label_layout = QVBoxLayout()
        modified_file_label.setLayout(modified_file_label_layout)
        modified_file_label_top = QHBoxLayout()
        modified_file_label_layout.addLayout(modified_file_label_top)
        modified_file_label_bottom = QHBoxLayout()
        modified_file_label_layout.addStretch(1)
        modified_file_label_layout.addLayout(modified_file_label_bottom)
        modified_file_label_left = QVBoxLayout()
        modified_file_label_top.addLayout(modified_file_label_left)
        modified_file_label_right = QVBoxLayout()
        modified_file_label_top.addLayout(modified_file_label_right)
        
        modified_files["DataTable"]["Label"] = QLabel(self)
        self.label_change("DataTable")
        modified_file_label_left.addWidget(modified_files["DataTable"]["Label"])
        
        modified_files["StringTable"]["Label"] = QLabel(self)
        self.label_change("StringTable")
        modified_file_label_left.addWidget(modified_files["StringTable"]["Label"])
        
        modified_files["Texture"]["Label"] = QLabel(self)
        self.label_change("Texture")
        modified_file_label_right.addWidget(modified_files["Texture"]["Label"])
        
        modified_files["UI"]["Label"] = QLabel(self)
        self.label_change("UI")
        modified_file_label_right.addWidget(modified_files["UI"]["Label"])
        
        modified_files["Blueprint"]["Label"] = QLabel(self)
        self.label_change("Blueprint")
        modified_file_label_right.addWidget(modified_files["Blueprint"]["Label"])
        
        discord_label = QLabel()
        discord_label.setText("<a href=\"https://discord.gg/nUbFA7MEeU\"><font face=Cambria color=#0080ff>Discord</font></a>")
        discord_label.setAlignment(Qt.AlignRight)
        discord_label.setOpenExternalLinks(True)
        modified_file_label_bottom.addStretch(1)
        modified_file_label_bottom.addWidget(discord_label)

        #Checkboxes

        self.check_box_1 = QCheckBox("Overworld Pool")
        self.check_box_1.setToolTip("Randomize all items and shards found in the overworld, now with\nnew improved logic. Everything you pick up will be 100% random\nso say goodbye to the endless sea of fried fish. Also affects items in\nClassic Mode 1 & 2")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        center_box_1_layout.addWidget(self.check_box_1, 0, 0)
        main_widget_to_param[self.check_box_1] = 0x000001

        self.check_box_16 = QCheckBox("Quest Pool")
        self.check_box_16.setToolTip("Randomize all quest rewards.")
        self.check_box_16.stateChanged.connect(self.check_box_16_changed)
        center_box_1_layout.addWidget(self.check_box_16, 1, 0)
        main_widget_to_param[self.check_box_16] = 0x000002

        self.check_box_2 = QCheckBox("Shop Pool")
        self.check_box_2.setToolTip("Randomize all items sold at the shop.")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        center_box_1_layout.addWidget(self.check_box_2, 2, 0)
        main_widget_to_param[self.check_box_2] = 0x000004

        self.check_box_17 = QCheckBox("Quest Requirements")
        self.check_box_17.setToolTip("Randomize the requirements for Susie, Abigail and Lindsay's quests.\nBenjamin will still ask you for waystones.")
        self.check_box_17.stateChanged.connect(self.check_box_17_changed)
        center_box_1_layout.addWidget(self.check_box_17, 3, 0)
        main_widget_to_param[self.check_box_17] = 0x000008

        self.check_box_18 = QCheckBox("Remove Infinites")
        self.check_box_18.setToolTip("Guarantee Gebel's Glasses and Recycle Hat to never appear.\nUseful for runs that favor magic and bullet management.")
        self.check_box_18.stateChanged.connect(self.check_box_18_changed)
        center_box_1_layout.addWidget(self.check_box_18, 4, 0)
        main_widget_to_param[self.check_box_18] = 0x000010

        self.check_box_3 = QCheckBox("Item Cost And Selling Price")
        self.check_box_3.setToolTip("Randomize the cost and selling price of every item in the shop.\nAlso affects prices in Classic Mode 2")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        center_box_2_layout.addWidget(self.check_box_3, 0, 0)
        main_widget_to_param[self.check_box_3] = 0x000020

        self.check_box_4 = QCheckBox("Scale Selling Price With Cost")
        self.check_box_4.setToolTip("Make the selling price scale with the item's random cost.\nAlso affects coin/remnant ratio in Classic Mode 2")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        center_box_2_layout.addWidget(self.check_box_4, 1, 0)
        main_widget_to_param[self.check_box_4] = 0x000040

        self.check_box_5 = QCheckBox("Map Requirements")
        self.check_box_5.setToolTip("Randomize the completion requirement for each tome.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        center_box_3_layout.addWidget(self.check_box_5, 0, 0)
        main_widget_to_param[self.check_box_5] = 0x000080

        self.check_box_6 = QCheckBox("Tome Appearance")
        self.check_box_6.setToolTip("Randomize which books are available in the game at all.\nDoes not affect Tome of Conquest.")
        self.check_box_6.stateChanged.connect(self.check_box_6_changed)
        center_box_3_layout.addWidget(self.check_box_6, 1, 0)
        main_widget_to_param[self.check_box_6] = 0x000100

        self.check_box_7 = QCheckBox("Shard Power And Magic Cost")
        self.check_box_7.setToolTip("Randomize the efficiency and MP cost of each shard.\nDoes not affect progression shards.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        center_box_4_layout.addWidget(self.check_box_7, 0, 0)
        main_widget_to_param[self.check_box_7] = 0x000200

        self.check_box_8 = QCheckBox("Scale Magic Cost With Power")
        self.check_box_8.setToolTip("Make the MP cost scale with the shard's random power.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        center_box_4_layout.addWidget(self.check_box_8, 1, 0)
        main_widget_to_param[self.check_box_8] = 0x000400

        self.check_box_23 = QCheckBox("Global Gear Stats")
        self.check_box_23.setToolTip("Slightly randomize the stats of all weapons and pieces of\nequipment with odds that still favor their original values.")
        self.check_box_23.stateChanged.connect(self.check_box_23_changed)
        center_box_5_layout.addWidget(self.check_box_23, 0, 0)
        main_widget_to_param[self.check_box_23] = 0x000800

        self.check_box_9 = QCheckBox("Cheat Gear Stats")
        self.check_box_9.setToolTip("Completely randomize the stats of the weapons, headgears\nand accessories that are originally obtained via cheatcodes.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        center_box_5_layout.addWidget(self.check_box_9, 1, 0)
        main_widget_to_param[self.check_box_9] = 0x001000

        self.check_box_25 = QCheckBox("Enemy Locations")
        self.check_box_25.setToolTip("Randomize which enemies appear where.")
        self.check_box_25.stateChanged.connect(self.check_box_25_changed)
        center_box_6_layout.addWidget(self.check_box_25, 0, 0)
        main_widget_to_param[self.check_box_25] = 0x002000

        self.check_box_10 = QCheckBox("Enemy Levels")
        self.check_box_10.setToolTip("Randomize the level of every enemy. Stats that scale with\nlevel include HP, attack, defense, luck, EXP and expertise.\nPicking this option will give you more starting HP and MP\nand reduce their growth to compensate.")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        center_box_6_layout.addWidget(self.check_box_10, 1, 0)
        main_widget_to_param[self.check_box_10] = 0x004000

        self.check_box_26 = QCheckBox("Boss Levels")
        self.check_box_26.setToolTip("Only recommended for Miriam mode.")
        self.check_box_26.stateChanged.connect(self.check_box_26_changed)
        center_box_6_layout.addWidget(self.check_box_26, 2, 0)
        main_widget_to_param[self.check_box_26] = 0x008000

        self.check_box_11 = QCheckBox("Enemy Tolerances")
        self.check_box_11.setToolTip("Randomize the first 8 resistance/weakness attributes of every enemy.")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        center_box_6_layout.addWidget(self.check_box_11, 3, 0)
        main_widget_to_param[self.check_box_11] = 0x010000

        self.check_box_27 = QCheckBox("Boss Tolerances")
        self.check_box_27.setToolTip("Only recommended for Miriam mode.")
        self.check_box_27.stateChanged.connect(self.check_box_27_changed)
        center_box_6_layout.addWidget(self.check_box_27, 4, 0)
        main_widget_to_param[self.check_box_27] = 0x020000

        self.check_box_12 = QCheckBox("Room Layout")
        self.check_box_12.setToolTip(f"Randomly pick from a folder of map presets ({map_num}).")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        center_box_7_layout.addWidget(self.check_box_12, 0, 0)
        main_widget_to_param[self.check_box_12] = 0x040000

        self.check_box_13 = QCheckBox("Outfit Color")
        self.check_box_13.setToolTip("Randomize the color of Miriam's and Zangetsu's outfits.")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        center_box_8_layout.addWidget(self.check_box_13, 0, 0)
        main_widget_to_param[self.check_box_13] = 0x080000

        self.check_box_24 = QCheckBox("Backer Portraits")
        self.check_box_24.setToolTip("Shuffle backer paintings.")
        self.check_box_24.stateChanged.connect(self.check_box_24_changed)
        center_box_8_layout.addWidget(self.check_box_24, 1, 0)
        main_widget_to_param[self.check_box_24] = 0x100000

        self.check_box_15 = QCheckBox("Dialogues")
        self.check_box_15.setToolTip("Randomize all conversation lines in the game. Characters\nwill still retain their actual voice (let's not get weird).")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        center_box_9_layout.addWidget(self.check_box_15, 0, 0)
        main_widget_to_param[self.check_box_15] = 0x200000

        self.check_box_14 = QCheckBox("Background Music")
        self.check_box_14.setToolTip("Randomize the music tracks that play in different areas.")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        center_box_9_layout.addWidget(self.check_box_14, 1, 0)
        main_widget_to_param[self.check_box_14] = 0x400000

        self.check_box_21 = QCheckBox("Bloodless Candles")
        self.check_box_21.setToolTip("Randomize candle placement in Bloodless mode.")
        self.check_box_21.stateChanged.connect(self.check_box_21_changed)
        center_box_10_layout.addWidget(self.check_box_21, 0, 0)
        main_widget_to_param[self.check_box_21] = 0x800000
        
        #SpinButtons
        
        self.spin_button_1 = QPushButton()
        self.spin_button_1.setAccessibleName("spin_button_1")
        self.spin_button_1.setToolTip("Logic complexity. Higher values usually follow a\nprogression chain.")
        self.spin_button_1.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_1.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_1.clicked.connect(self.spin_button_1_clicked)
        self.spin_button_1.setVisible(False)
        center_box_1_layout.addWidget(self.spin_button_1, 0, 1)
        sub_widget_to_param[self.spin_button_1] = 0x001
        
        self.spin_button_2 = QPushButton()
        self.spin_button_2.setAccessibleName("spin_button_2")
        self.spin_button_2.setToolTip("Weight of shop items locked behind events.")
        self.spin_button_2.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_2.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_2.clicked.connect(self.spin_button_2_clicked)
        self.spin_button_2.setVisible(False)
        center_box_1_layout.addWidget(self.spin_button_2, 2, 1)
        sub_widget_to_param[self.spin_button_2] = 0x002
        
        self.spin_button_3 = QPushButton()
        self.spin_button_3.setAccessibleName("spin_button_3")
        self.spin_button_3.setToolTip("Price weight. The higher the value the more extreme\nthe price differences.")
        self.spin_button_3.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_3.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_3.clicked.connect(self.spin_button_3_clicked)
        self.spin_button_3.setVisible(False)
        center_box_2_layout.addWidget(self.spin_button_3, 0, 1)
        sub_widget_to_param[self.spin_button_3] = 0x004
        
        self.spin_button_4 = QPushButton()
        self.spin_button_4.setAccessibleName("spin_button_4")
        self.spin_button_4.setToolTip("Requirement weight. 2 is linear, 1 and 3 favor early and\nlate map completion respectively.")
        self.spin_button_4.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_4.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_4.clicked.connect(self.spin_button_4_clicked)
        self.spin_button_4.setVisible(False)
        center_box_3_layout.addWidget(self.spin_button_4, 0, 1)
        sub_widget_to_param[self.spin_button_4] = 0x008
        
        self.spin_button_5 = QPushButton()
        self.spin_button_5.setAccessibleName("spin_button_5")
        self.spin_button_5.setToolTip("Power weight. The higher the value the more extreme\nthe power differences.")
        self.spin_button_5.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_5.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_5.clicked.connect(self.spin_button_5_clicked)
        self.spin_button_5.setVisible(False)
        center_box_4_layout.addWidget(self.spin_button_5, 0, 1)
        sub_widget_to_param[self.spin_button_5] = 0x010
        
        self.spin_button_6 = QPushButton()
        self.spin_button_6.setAccessibleName("spin_button_6")
        self.spin_button_6.setToolTip("Stat weight. The higher the value the more extreme\nthe stat differences.")
        self.spin_button_6.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_6.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_6.clicked.connect(self.spin_button_6_clicked)
        self.spin_button_6.setVisible(False)
        center_box_5_layout.addWidget(self.spin_button_6, 0, 1)
        sub_widget_to_param[self.spin_button_6] = 0x020
        
        self.spin_button_8 = QPushButton()
        self.spin_button_8.setAccessibleName("spin_button_8")
        self.spin_button_8.setToolTip("Level weight. The higher the value the more extreme\nthe level differences.")
        self.spin_button_8.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_8.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_8.clicked.connect(self.spin_button_8_clicked)
        self.spin_button_8.setVisible(False)
        center_box_6_layout.addWidget(self.spin_button_8, 1, 1)
        sub_widget_to_param[self.spin_button_8] = 0x040
        
        self.spin_button_9 = QPushButton()
        self.spin_button_9.setAccessibleName("spin_button_9")
        self.spin_button_9.setToolTip("Level weight. The higher the value the more extreme\nthe level differences.")
        self.spin_button_9.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_9.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_9.clicked.connect(self.spin_button_9_clicked)
        self.spin_button_9.setVisible(False)
        center_box_6_layout.addWidget(self.spin_button_9, 2, 1)
        sub_widget_to_param[self.spin_button_9] = 0x080
        
        self.spin_button_10 = QPushButton()
        self.spin_button_10.setAccessibleName("spin_button_10")
        self.spin_button_10.setToolTip("Tolerance weight. The higher the value the more extreme\nthe tolerance differences.")
        self.spin_button_10.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_10.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_10.clicked.connect(self.spin_button_10_clicked)
        self.spin_button_10.setVisible(False)
        center_box_6_layout.addWidget(self.spin_button_10, 3, 1)
        sub_widget_to_param[self.spin_button_10] = 0x100
        
        self.spin_button_11 = QPushButton()
        self.spin_button_11.setAccessibleName("spin_button_11")
        self.spin_button_11.setToolTip("Tolerance weight. The higher the value the more extreme\nthe tolerance differences.")
        self.spin_button_11.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_11.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_11.clicked.connect(self.spin_button_11_clicked)
        self.spin_button_11.setVisible(False)
        center_box_6_layout.addWidget(self.spin_button_11, 4, 1)
        sub_widget_to_param[self.spin_button_11] = 0x200
        
        self.browse_map_button = QPushButton()
        self.browse_map_button.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.browse_map_button.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.browse_map_button.clicked.connect(self.browse_map_button_clicked)
        self.browse_map_button.setVisible(False)
        center_box_7_layout.addWidget(self.browse_map_button, 0, 1)
        
        self.outfit_config_button = QPushButton()
        self.outfit_config_button.setIcon(QPixmap("Data\\config.png"))
        self.outfit_config_button.setToolTip("Configure which outfit colors can be chosen.")
        self.outfit_config_button.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.outfit_config_button.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.outfit_config_button.clicked.connect(self.outfit_config_button_clicked)
        self.outfit_config_button.setVisible(False)
        center_box_8_layout.addWidget(self.outfit_config_button, 0, 1)
        
        self.language_sequence = "JE"
        self.spin_button_12 = QPushButton()
        self.spin_button_12.setAccessibleName("spin_button_12")
        self.spin_button_12.setToolTip("Voice language")
        self.spin_button_12.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_12.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_12.clicked.connect(self.spin_button_12_clicked)
        self.spin_button_12.setVisible(False)
        center_box_9_layout.addWidget(self.spin_button_12, 0, 1)
        sub_widget_to_param[self.spin_button_12] = 0x400
        
        self.spin_button_13 = QPushButton()
        self.spin_button_13.setAccessibleName("spin_button_13")
        self.spin_button_13.setToolTip("Logic complexity. Higher values usually follow a\nprogression chain.")
        self.spin_button_13.setStyleSheet("QPushButton{color: #ffffff; font-family: Impact}" + "QToolTip{color: #ffffff; font-family: Cambria}")
        self.spin_button_13.setFixedSize(self.size_multiplier*28, self.size_multiplier*24)
        self.spin_button_13.clicked.connect(self.spin_button_13_clicked)
        self.spin_button_13.setVisible(False)
        center_box_10_layout.addWidget(self.spin_button_13, 0, 1)
        sub_widget_to_param[self.spin_button_13] = 0x800
        
        #RadioButtons
        
        self.radio_button_1 = QRadioButton("Normal")
        self.radio_button_1.setToolTip("More like easy mode.")
        self.radio_button_1.toggled.connect(self.radio_button_group_1_checked)
        center_box_11_layout.addWidget(self.radio_button_1, 0, 0)
        
        self.radio_button_2 = QRadioButton("Hard")
        self.radio_button_2.setToolTip("The real normal mode.")
        self.radio_button_2.toggled.connect(self.radio_button_group_1_checked)
        center_box_11_layout.addWidget(self.radio_button_2, 1, 0)
        
        self.radio_button_3 = QRadioButton("Nightmare")
        self.radio_button_3.setToolTip("Shit's gonna get real.")
        self.radio_button_3.toggled.connect(self.radio_button_group_1_checked)
        center_box_11_layout.addWidget(self.radio_button_3, 0, 1)
        
        self.radio_button_4 = QRadioButton("None")
        self.radio_button_4.setToolTip("No special game mode.")
        self.radio_button_4.toggled.connect(self.radio_button_group_2_checked)
        center_box_17_layout.addWidget(self.radio_button_4, 0, 0)
        
        self.radio_button_5 = QRadioButton("Custom NG+")
        self.radio_button_5.setToolTip("Play through your NG+ files with a chosen level\nvalue for all enemies.")
        self.radio_button_5.toggled.connect(self.radio_button_group_2_checked)
        center_box_17_layout.addWidget(self.radio_button_5, 1, 0)
        
        self.radio_button_6 = QRadioButton("Progressive Z")
        self.radio_button_6.setToolTip("Play through a more balanced version of Zangetsu\nmode where his stats scale with progression.")
        self.radio_button_6.toggled.connect(self.radio_button_group_2_checked)
        center_box_17_layout.addWidget(self.radio_button_6, 0, 1)
        
        #Spin boxes
        
        self.custom_level_field = QSpinBox()
        self.custom_level_field.setToolTip("Level of all enemies.")
        self.custom_level_field.valueChanged.connect(self.custom_level_field_changed)
        self.custom_level_field.setValue(config.getint("SpecialMode", "iCustomNGLevel"))
        self.custom_level_field.setRange(1, 99)
        self.custom_level_field.setVisible(False)
        center_box_17_layout.addWidget(self.custom_level_field, 1, 1)
        
        #Dropdown lists
        
        self.preset_drop_down = QComboBox()
        self.preset_drop_down.setToolTip("EMPTY: Clear all options.\nTRIAL: To get started with this mod.\nRACE: Most fitting for a King of Speed.\nMEME: Time to break the game.\nRISK: Chaos awaits !\nBLOOD: She needs more blood.")
        self.preset_drop_down.addItem("Custom")
        for preset in preset_to_bytes:
            self.preset_drop_down.addItem(preset)
        self.preset_drop_down.currentIndexChanged.connect(self.preset_drop_down_changed)
        center_box_12_layout.addWidget(self.preset_drop_down, 0, 0)
        
        #Settings
        
        self.setting_window_layout = QVBoxLayout()
        
        window_size_layout = QHBoxLayout()
        self.setting_window_layout.addLayout(window_size_layout)
        
        archi_name_label = QLabel("Window Size")
        window_size_layout.addWidget(archi_name_label)
        
        self.window_size_drop_down = QComboBox()
        self.window_size_drop_down.addItem("720p")
        self.window_size_drop_down.addItem("900p")
        self.window_size_drop_down.addItem("1080p and above")
        window_size_layout.addWidget(self.window_size_drop_down)
        
        setting_apply_layout = QHBoxLayout()
        self.setting_window_layout.addLayout(setting_apply_layout)
        
        setting_apply_button = QPushButton("Apply")
        setting_apply_button.clicked.connect(self.setting_apply_button_clicked)
        setting_apply_layout.addStretch(1)
        setting_apply_layout.addWidget(setting_apply_button)
        
        #Seed
        
        self.seed_window_layout = QVBoxLayout()
        seed_window_top = QHBoxLayout()
        self.seed_window_layout.addLayout(seed_window_top)
        seed_window_center = QHBoxLayout()
        self.seed_window_layout.addLayout(seed_window_center)
        seed_window_bottom = QHBoxLayout()
        self.seed_window_layout.addLayout(seed_window_bottom)
        
        self.seed_field = QLineEdit(config.get("Misc", "sSeed"))
        self.seed_field.setMaxLength(30)
        self.seed_field.textChanged[str].connect(self.seed_field_changed)
        seed_window_top.addWidget(self.seed_field)
        
        seed_new_button = QPushButton("New Seed")
        seed_new_button.clicked.connect(self.seed_new_button_clicked)
        seed_window_center.addWidget(seed_new_button)
        
        seed_test_button = QPushButton("Test Seed")
        seed_test_button.clicked.connect(self.seed_test_button_clicked)
        seed_window_center.addWidget(seed_test_button)
        
        seed_confirm_button = QPushButton("Confirm")
        seed_confirm_button.clicked.connect(self.seed_confirm_button_clicked)
        seed_window_center.addWidget(seed_confirm_button)

        self.dlc_check_box = QCheckBox("Ignore DLC")
        self.dlc_check_box.setToolTip("Make it so that any DLC that may be installed in\nyour game will be ignored by the randomization.")
        self.dlc_check_box.stateChanged.connect(self.dlc_check_box_changed)
        seed_window_bottom.addWidget(self.dlc_check_box)
        
        #Outfit config
        
        self.outfit_window_layout = QVBoxLayout()
        outfit_window_top = QHBoxLayout()
        self.outfit_window_layout.addLayout(outfit_window_top)
        outfit_window_center = QHBoxLayout()
        self.outfit_window_layout.addLayout(outfit_window_center)
        outfit_window_bottom = QHBoxLayout()
        self.outfit_window_layout.addLayout(outfit_window_bottom)
        
        outfit_instruction_label = QLabel()
        outfit_instruction_label.setText("Select none for vanilla or select multiple for a random\nchoice. Outfits are named after their HSV component.")
        outfit_window_top.addWidget(outfit_instruction_label)
        
        miriam_outfit_box_layout = QVBoxLayout()
        miriam_outfit_box = QGroupBox("Miriam")
        miriam_outfit_box.setLayout(miriam_outfit_box_layout)
        outfit_window_center.addWidget(miriam_outfit_box)
        
        self.miriam_outfit_list = QListWidget()
        self.miriam_outfit_list.setSelectionMode(QListWidget.MultiSelection)
        miriam_outfit_box_layout.addWidget(self.miriam_outfit_list)
        for folder in os.listdir("Data\\Texture\\Miriam"):
            if os.path.isdir(f"Data\\Texture\\Miriam\\{folder}"):
                self.miriam_outfit_list.addItem(folder)
        
        zangetsu_outfit_box_layout = QVBoxLayout()
        zangetsu_outfit_box = QGroupBox("Zangetsu")
        zangetsu_outfit_box.setLayout(zangetsu_outfit_box_layout)
        outfit_window_center.addWidget(zangetsu_outfit_box)
        
        self.zangetsu_outfit_list = QListWidget()
        self.zangetsu_outfit_list.setSelectionMode(QListWidget.MultiSelection)
        zangetsu_outfit_box_layout.addWidget(self.zangetsu_outfit_list)
        for folder in os.listdir("Data\\Texture\\Zangetsu"):
            if os.path.isdir(f"Data\\Texture\\Zangetsu\\{folder}"):
                self.zangetsu_outfit_list.addItem(folder)
        
        outfit_confirm_button = QPushButton("Confirm")
        outfit_confirm_button.clicked.connect(self.outfit_confirm_button_clicked)
        outfit_window_bottom.addStretch(1)
        outfit_window_bottom.addWidget(outfit_confirm_button)
        
        #Archipelago
        
        self.archi_window_layout = QVBoxLayout()

        self.archi_check_box = QCheckBox("Enable Archipelago")
        self.archi_window_layout.addWidget(self.archi_check_box)
        
        archi_name_layout = QHBoxLayout()
        self.archi_window_layout.addLayout(archi_name_layout)
        
        archi_name_label = QLabel("Archipelago Name")
        archi_name_layout.addWidget(archi_name_label)
        
        self.archi_name_field = QLineEdit()
        archi_name_layout.addWidget(self.archi_name_field)
        progression_layout = QHBoxLayout()
        self.archi_window_layout.addLayout(progression_layout)
        
        progression_label = QLabel("Progression Balancing")
        progression_layout.addWidget(progression_label)
        
        self.progression_field = QSpinBox()
        self.progression_field.setRange(0, 99)
        progression_layout.addWidget(self.progression_field)
        
        accessibility_layout = QHBoxLayout()
        self.archi_window_layout.addLayout(accessibility_layout)
        
        accessibility_label = QLabel("Accessibility")
        accessibility_layout.addWidget(accessibility_label)
        
        self.accessibility_drop_down = QComboBox()
        self.accessibility_drop_down.addItem("Locations")
        self.accessibility_drop_down.addItem("Items")
        self.accessibility_drop_down.addItem("Minimal")
        accessibility_layout.addWidget(self.accessibility_drop_down)

        self.death_link_check_box = QCheckBox("Death Link")
        self.archi_window_layout.addWidget(self.death_link_check_box)
        
        archi_apply_layout = QHBoxLayout()
        self.archi_window_layout.addLayout(archi_apply_layout)
        
        archi_apply_button = QPushButton("Apply")
        archi_apply_button.clicked.connect(self.archi_apply_button_clicked)
        archi_apply_layout.addStretch(1)
        archi_apply_layout.addWidget(archi_apply_button)
        
        #Text field
        
        self.starting_items_field = QLineEdit(config.get("StartWith", "sStartItem"))
        self.starting_items_field.setToolTip("Items to start with. Input their english names with\ncommas as separators. If unsure refer to the files\nin Data\\Translation for item names.")
        self.starting_items_field.textChanged[str].connect(self.starting_items_field_changed)
        center_box_16_layout.addWidget(self.starting_items_field, 0, 0)
        
        self.param_string_format = "{:0" + str(main_param_length + sub_param_length) + "x}"
        self.param_string_field = QLineEdit(self.param_string_format.format(0).upper())
        self.param_string_field.setMaxLength(main_param_length + sub_param_length)
        self.param_string_field.setToolTip("Simplified string containing all the randomization settings.")
        self.param_string_field.textChanged[str].connect(self.param_string_field_changed)
        center_box_13_layout.addWidget(self.param_string_field, 0, 0)
        
        self.game_path_field = QLineEdit(config.get("Misc", "sGamePath"))
        self.game_path_field.setToolTip("Path to your game's data (...\\steamapps\\common\\Bloodstained Ritual of the Night).")
        self.game_path_field.textChanged[str].connect(self.game_path_field_changed)
        center_box_14_layout.addWidget(self.game_path_field, 0, 0)
        
        browse_game_path_button = QPushButton()
        browse_game_path_button.setIcon(QPixmap("Data\\browse.png"))
        browse_game_path_button.clicked.connect(self.browse_game_path_button_clicked)
        center_box_14_layout.addWidget(browse_game_path_button, 0, 1)
        
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
        self.check_box_13.setChecked(config.getboolean("GraphicRandomization", "bOutfitColor"))
        self.check_box_24.setChecked(config.getboolean("GraphicRandomization", "bBackerPortraits"))
        self.check_box_15.setChecked(config.getboolean("SoundRandomization", "bDialogues"))
        self.check_box_14.setChecked(config.getboolean("SoundRandomization", "bBackGroundMusic"))
        self.check_box_21.setChecked(config.getboolean("ExtraRandomization", "bBloodlessCandles"))
        
        self.spin_button_1_set_index(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        self.spin_button_2_set_index(config.getint("ItemRandomization", "iShopPoolWeight"))
        self.spin_button_3_set_index(config.getint("ShopRandomization", "iItemCostAndSellingPriceWeight"))
        self.spin_button_4_set_index(config.getint("LibraryRandomization", "iMapRequirementsWeight"))
        self.spin_button_5_set_index(config.getint("ShardRandomization", "iShardPowerAndMagicCostWeight"))
        self.spin_button_6_set_index(config.getint("EquipmentRandomization", "iGlobalGearStatsWeight"))
        self.spin_button_8_set_index(config.getint("EnemyRandomization", "iEnemyLevelsWeight"))
        self.spin_button_9_set_index(config.getint("EnemyRandomization", "iBossLevelsWeight"))
        self.spin_button_10_set_index(config.getint("EnemyRandomization", "iEnemyTolerancesWeight"))
        self.spin_button_11_set_index(config.getint("EnemyRandomization", "iBossTolerancesWeight"))
        self.spin_button_12_set_index(config.getint("SoundRandomization", "iDialoguesLanguage"))
        self.spin_button_13_set_index(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
        
        self.radio_button_1.setChecked(config.getboolean("GameDifficulty", "bNormal"))
        self.radio_button_2.setChecked(config.getboolean("GameDifficulty", "bHard"))
        self.radio_button_3.setChecked(config.getboolean("GameDifficulty", "bNightmare"))
        
        self.radio_button_4.setChecked(config.getboolean("SpecialMode", "bNone"))
        self.radio_button_5.setChecked(config.getboolean("SpecialMode", "bCustomNG"))
        self.radio_button_6.setChecked(config.getboolean("SpecialMode", "bProgressiveZ"))
        
        self.dlc_check_box.setChecked(config.getboolean("Misc", "bIgnoreDLC"))
        
        self.window_size_drop_down.setCurrentIndex(window_sizes.index(config.getint("Misc", "iWindowSize")))
        
        self.matches_preset()

        #Buttons
        
        setting_button = QPushButton("Settings")
        setting_button.setToolTip("Interface settings.")
        setting_button.setShortcut(Qt.Key_S)
        setting_button.clicked.connect(self.setting_button_clicked)
        center_widget_layout.addWidget(setting_button, 9, 0, 1, 1)
        
        import_asset_button = QPushButton("Import Assets")
        import_asset_button.setToolTip("Reimport and convert all base game assets used in this mod.\nUseful if the game updates or if one asset gets corrupted on\naccident.")
        import_asset_button.clicked.connect(self.import_asset_button_clicked)
        center_widget_layout.addWidget(import_asset_button, 9, 1, 1, 1)
        
        archipelago_button = QPushButton("Coming Soon")
        archipelago_button.setToolTip("™")
        #archipelago_button.clicked.connect(self.archipelago_button_clicked)
        center_widget_layout.addWidget(archipelago_button, 9, 2, 1, 1)
        
        credit_button = QPushButton("Credits")
        credit_button.setToolTip("The people involved with this mod.")
        credit_button.clicked.connect(self.credit_button_clicked)
        center_widget_layout.addWidget(credit_button, 9, 3, 1, 1)

        generate_button = QPushButton("Generate")
        generate_button.setToolTip("Generate the mod with the current settings.")
        generate_button.clicked.connect(self.generate_button_clicked)
        center_widget_layout.addWidget(generate_button, 10, 0, 1, 4)
        
        #Window
        
        self.setFixedSize(self.size_multiplier*1800, self.size_multiplier*1000)
        self.reset_selected_map_state()
        self.setWindowIcon(QIcon(resource_path("Bloodstained.ico")))
        self.show()
        
        #Position
        
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        QApplication.processEvents()
    
    def check_box_1_changed(self):
        checked = self.check_box_1.isChecked()
        config.set("ItemRandomization", "bOverworldPool", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_1)
            self.check_box_1.setStyleSheet(f"color: {item_color}")
            if self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.center_box_1.setStyleSheet(f"color: {item_color}")
        else:
            self.remove_main_param(self.check_box_1)
            self.check_box_1.setStyleSheet("color: #ffffff")
            self.center_box_1.setStyleSheet("color: #ffffff")
            self.check_box_16.setChecked(False)
            self.check_box_2.setChecked(False)
        self.spin_button_1.setVisible(checked)
        self.matches_preset()

    def check_box_16_changed(self):
        checked = self.check_box_16.isChecked()
        config.set("ItemRandomization", "bQuestPool", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_16)
            self.check_box_16.setStyleSheet(f"color: {item_color}")
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.center_box_1.setStyleSheet(f"color: {item_color}")
            self.check_box_1.setChecked(True)
        else:
            self.remove_main_param(self.check_box_16)
            self.check_box_16.setStyleSheet("color: #ffffff")
            self.center_box_1.setStyleSheet("color: #ffffff")
            self.check_box_2.setChecked(False)
        self.matches_preset()

    def check_box_2_changed(self):
        checked = self.check_box_2.isChecked()
        config.set("ItemRandomization", "bShopPool", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_2)
            self.check_box_2.setStyleSheet(f"color: {item_color}")
            if self.check_box_1.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.center_box_1.setStyleSheet(f"color: {item_color}")
            self.check_box_1.setChecked(True)
            self.check_box_16.setChecked(True)
        else:
            self.remove_main_param(self.check_box_2)
            self.check_box_2.setStyleSheet("color: #ffffff")
            self.center_box_1.setStyleSheet("color: #ffffff")
        self.spin_button_2.setVisible(checked)
        self.matches_preset()

    def check_box_17_changed(self):
        checked = self.check_box_17.isChecked()
        config.set("ItemRandomization", "bQuestRequirements", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_17)
            self.check_box_17.setStyleSheet(f"color: {item_color}")
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_18.isChecked():
                self.center_box_1.setStyleSheet(f"color: {item_color}")
        else:
            self.remove_main_param(self.check_box_17)
            self.check_box_17.setStyleSheet("color: #ffffff")
            self.center_box_1.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_18_changed(self):
        checked = self.check_box_18.isChecked()
        config.set("ItemRandomization", "bRemoveInfinites", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_18)
            self.check_box_18.setStyleSheet(f"color: {item_color}")
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked():
                self.center_box_1.setStyleSheet(f"color: {item_color}")
        else:
            self.remove_main_param(self.check_box_18)
            self.check_box_18.setStyleSheet("color: #ffffff")
            self.center_box_1.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_3_changed(self):
        checked = self.check_box_3.isChecked()
        config.set("ShopRandomization", "bItemCostAndSellingPrice", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_3)
            self.check_box_3.setStyleSheet(f"color: {shop_color}")
            if self.check_box_4.isChecked():
                self.center_box_2.setStyleSheet(f"color: {shop_color}")
        else:
            self.remove_main_param(self.check_box_3)
            self.check_box_3.setStyleSheet("color: #ffffff")
            self.center_box_2.setStyleSheet("color: #ffffff")
            self.check_box_4.setChecked(False)
        self.spin_button_3.setVisible(checked)
        self.matches_preset()

    def check_box_4_changed(self):
        checked = self.check_box_4.isChecked()
        config.set("ShopRandomization", "bScaleSellingPriceWithCost", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_4)
            self.check_box_4.setStyleSheet(f"color: {shop_color}")
            if self.check_box_3.isChecked():
                self.center_box_2.setStyleSheet(f"color: {shop_color}")
            self.check_box_3.setChecked(True)
        else:
            self.remove_main_param(self.check_box_4)
            self.check_box_4.setStyleSheet("color: #ffffff")
            self.center_box_2.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_5_changed(self):
        checked = self.check_box_5.isChecked()
        config.set("LibraryRandomization", "bMapRequirements", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_5)
            self.check_box_5.setStyleSheet(f"color: {library_color}")
            if self.check_box_6.isChecked():
                self.center_box_3.setStyleSheet(f"color: {library_color}")
        else:
            self.remove_main_param(self.check_box_5)
            self.check_box_5.setStyleSheet("color: #ffffff")
            self.center_box_3.setStyleSheet("color: #ffffff")
        self.spin_button_4.setVisible(checked)
        self.matches_preset()

    def check_box_6_changed(self):
        checked = self.check_box_6.isChecked()
        config.set("LibraryRandomization", "bTomeAppearance", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_6)
            self.check_box_6.setStyleSheet(f"color: {library_color}")
            if self.check_box_5.isChecked():
                self.center_box_3.setStyleSheet(f"color: {library_color}")
        else:
            self.remove_main_param(self.check_box_6)
            self.check_box_6.setStyleSheet("color: #ffffff")
            self.center_box_3.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_7_changed(self):
        checked = self.check_box_7.isChecked()
        config.set("ShardRandomization", "bShardPowerAndMagicCost", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_7)
            self.check_box_7.setStyleSheet(f"color: {shard_color}")
            if self.check_box_8.isChecked():
                self.center_box_4.setStyleSheet(f"color: {shard_color}")
        else:
            self.remove_main_param(self.check_box_7)
            self.check_box_7.setStyleSheet("color: #ffffff")
            self.center_box_4.setStyleSheet("color: #ffffff")
            self.check_box_8.setChecked(False)
        self.spin_button_5.setVisible(checked)
        self.matches_preset()

    def check_box_8_changed(self):
        checked = self.check_box_8.isChecked()
        config.set("ShardRandomization", "bScaleMagicCostWithPower", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_8)
            self.check_box_8.setStyleSheet(f"color: {shard_color}")
            if self.check_box_7.isChecked():
                self.center_box_4.setStyleSheet(f"color: {shard_color}")
            self.check_box_7.setChecked(True)
        else:
            self.remove_main_param(self.check_box_8)
            self.check_box_8.setStyleSheet("color: #ffffff")
            self.center_box_4.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_23_changed(self):
        checked = self.check_box_23.isChecked()
        config.set("EquipmentRandomization", "bGlobalGearStats", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_23)
            self.check_box_23.setStyleSheet(f"color: {equip_color}")
            if self.check_box_9.isChecked():
                self.center_box_5.setStyleSheet(f"color: {equip_color}")
        else:
            self.remove_main_param(self.check_box_23)
            self.check_box_23.setStyleSheet("color: #ffffff")
            self.center_box_5.setStyleSheet("color: #ffffff")
        self.spin_button_6.setVisible(checked)
        self.matches_preset()

    def check_box_9_changed(self):
        checked = self.check_box_9.isChecked()
        config.set("EquipmentRandomization", "bCheatGearStats", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_9)
            self.check_box_9.setStyleSheet(f"color: {equip_color}")
            if self.check_box_23.isChecked():
                self.center_box_5.setStyleSheet(f"color: {equip_color}")
        else:
            self.remove_main_param(self.check_box_9)
            self.check_box_9.setStyleSheet("color: #ffffff")
            self.center_box_5.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_25_changed(self):
        checked = self.check_box_25.isChecked()
        config.set("EnemyRandomization", "bEnemyLocations", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_25)
            self.check_box_25.setStyleSheet(f"color: {enemy_color}")
            if self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.center_box_6.setStyleSheet(f"color: {enemy_color}")
        else:
            self.remove_main_param(self.check_box_25)
            self.check_box_25.setStyleSheet("color: #ffffff")
            self.center_box_6.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_10_changed(self):
        checked = self.check_box_10.isChecked()
        config.set("EnemyRandomization", "bEnemyLevels", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_10)
            self.check_box_10.setStyleSheet(f"color: {enemy_color}")
            if self.check_box_25.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.center_box_6.setStyleSheet(f"color: {enemy_color}")
        else:
            self.remove_main_param(self.check_box_10)
            self.check_box_10.setStyleSheet("color: #ffffff")
            self.center_box_6.setStyleSheet("color: #ffffff")
        self.spin_button_8.setVisible(checked)
        self.matches_preset()

    def check_box_26_changed(self):
        checked = self.check_box_26.isChecked()
        config.set("EnemyRandomization", "bBossLevels", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_26)
            self.check_box_26.setStyleSheet(f"color: {enemy_color}")
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_11.isChecked() and self.check_box_27.isChecked():
                self.center_box_6.setStyleSheet(f"color: {enemy_color}")
        else:
            self.remove_main_param(self.check_box_26)
            self.check_box_26.setStyleSheet("color: #ffffff")
            self.center_box_6.setStyleSheet("color: #ffffff")
        self.spin_button_9.setVisible(checked)
        self.matches_preset()

    def check_box_11_changed(self):
        checked = self.check_box_11.isChecked()
        config.set("EnemyRandomization", "bEnemyTolerances", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_11)
            self.check_box_11.setStyleSheet(f"color: {enemy_color}")
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_27.isChecked():
                self.center_box_6.setStyleSheet(f"color: {enemy_color}")
        else:
            self.remove_main_param(self.check_box_11)
            self.check_box_11.setStyleSheet("color: #ffffff")
            self.center_box_6.setStyleSheet("color: #ffffff")
        self.spin_button_10.setVisible(checked)
        self.matches_preset()

    def check_box_27_changed(self):
        checked = self.check_box_27.isChecked()
        config.set("EnemyRandomization", "bBossTolerances", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_27)
            self.check_box_27.setStyleSheet(f"color: {enemy_color}")
            if self.check_box_25.isChecked() and self.check_box_10.isChecked() and self.check_box_26.isChecked() and self.check_box_11.isChecked():
                self.center_box_6.setStyleSheet(f"color: {enemy_color}")
        else:
            self.remove_main_param(self.check_box_27)
            self.check_box_27.setStyleSheet("color: #ffffff")
            self.center_box_6.setStyleSheet("color: #ffffff")
        self.spin_button_11.setVisible(checked)
        self.matches_preset()

    def check_box_12_changed(self):
        checked = self.check_box_12.isChecked()
        config.set("MapRandomization", "bRoomLayout", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_12)
            self.check_box_12.setStyleSheet(f"color: {map_color}")
            self.center_box_7.setStyleSheet(f"color: {map_color}")
            self.add_to_modified_files("UI", "icon_8bitCrown"    , [])
            self.add_to_modified_files("UI", "Map_Icon_Keyperson", [])
            self.add_to_modified_files("UI", "Map_Icon_RootBox"  , [])
            self.add_to_modified_files("UI", "Map_StartingPoint" , [])
        else:
            self.remove_main_param(self.check_box_12)
            self.check_box_12.setStyleSheet("color: #ffffff")
            self.center_box_7.setStyleSheet("color: #ffffff")
            self.remove_from_modified_files("UI", "icon_8bitCrown"    , [])
            self.remove_from_modified_files("UI", "Map_Icon_Keyperson", [])
            self.remove_from_modified_files("UI", "Map_Icon_RootBox"  , [])
            self.remove_from_modified_files("UI", "Map_StartingPoint" , [])
        self.reset_selected_map_state()
        self.browse_map_button.setVisible(checked)
        self.matches_preset()

    def check_box_13_changed(self):
        checked = self.check_box_13.isChecked()
        config.set("GraphicRandomization", "bOutfitColor", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_13)
            self.check_box_13.setStyleSheet(f"color: {graphic_color}")
            if self.check_box_24.isChecked():
                self.center_box_8.setStyleSheet(f"color: {graphic_color}")
        else:
            self.remove_main_param(self.check_box_13)
            self.check_box_13.setStyleSheet("color: #ffffff")
            self.center_box_8.setStyleSheet("color: #ffffff")
        self.update_modified_files_for_outfit()
        self.outfit_config_button.setVisible(checked)
        self.matches_preset()

    def check_box_24_changed(self):
        checked = self.check_box_24.isChecked()
        config.set("GraphicRandomization", "bBackerPortraits", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_24)
            self.check_box_24.setStyleSheet(f"color: {graphic_color}")
            if self.check_box_13.isChecked():
                self.center_box_8.setStyleSheet(f"color: {graphic_color}")
        else:
            self.remove_main_param(self.check_box_24)
            self.check_box_24.setStyleSheet("color: #ffffff")
            self.center_box_8.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_15_changed(self):
        checked = self.check_box_15.isChecked()
        config.set("SoundRandomization", "bDialogues", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_15)
            self.check_box_15.setStyleSheet(f"color: {sound_color}")
            if self.check_box_14.isChecked():
                self.center_box_9.setStyleSheet(f"color: {sound_color}")
        else:
            self.remove_main_param(self.check_box_15)
            self.check_box_15.setStyleSheet("color: #ffffff")
            self.center_box_9.setStyleSheet("color: #ffffff")
        self.spin_button_12.setVisible(checked)
        self.matches_preset()

    def check_box_14_changed(self):
        checked = self.check_box_14.isChecked()
        config.set("SoundRandomization", "bBackGroundMusic", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_14)
            self.check_box_14.setStyleSheet(f"color: {sound_color}")
            if self.check_box_15.isChecked():
                self.center_box_9.setStyleSheet(f"color: {sound_color}")
        else:
            self.remove_main_param(self.check_box_14)
            self.check_box_14.setStyleSheet("color: #ffffff")
            self.center_box_9.setStyleSheet("color: #ffffff")
        self.matches_preset()

    def check_box_21_changed(self):
        checked = self.check_box_21.isChecked()
        config.set("ExtraRandomization", "bBloodlessCandles", str(checked).lower())
        if checked:
            self.add_main_param(self.check_box_21)
            self.check_box_21.setStyleSheet(f"color: {extra_color}")
            self.center_box_10.setStyleSheet(f"color: {extra_color}")
        else:
            self.remove_main_param(self.check_box_21)
            self.check_box_21.setStyleSheet("color: #ffffff")
            self.center_box_10.setStyleSheet("color: #ffffff")
        self.spin_button_13.setVisible(checked)
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
        self.change_sub_param(self.spin_button_1, index)
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
        config.set("ItemRandomization", "iShopPoolWeight", str(index))
        self.change_sub_param(self.spin_button_2, index)
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
        config.set("ShopRandomization", "iItemCostAndSellingPriceWeight", str(index))
        self.change_sub_param(self.spin_button_3, index)
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
        config.set("LibraryRandomization", "iMapRequirementsWeight", str(index))
        self.change_sub_param(self.spin_button_4, index)
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
        config.set("ShardRandomization", "iShardPowerAndMagicCostWeight", str(index))
        self.change_sub_param(self.spin_button_5, index)
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
        config.set("EquipmentRandomization", "iGlobalGearStatsWeight", str(index))
        self.change_sub_param(self.spin_button_6, index)
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
        config.set("EnemyRandomization", "iEnemyLevelsWeight", str(index))
        self.change_sub_param(self.spin_button_8, index)
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
        config.set("EnemyRandomization", "iBossLevelsWeight", str(index))
        self.change_sub_param(self.spin_button_9, index)
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
        config.set("EnemyRandomization", "iEnemyTolerancesWeight", str(index))
        self.change_sub_param(self.spin_button_10, index)
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
        config.set("EnemyRandomization", "iBossTolerancesWeight", str(index))
        self.change_sub_param(self.spin_button_11, index)
        return True

    def spin_button_12_clicked(self):
        num = self.spin_button_12_get_index()
        num = num % len(self.language_sequence) + 1
        self.spin_button_12_set_index(num)

    def spin_button_12_get_index(self):
        if self.spin_button_12.text():
            return self.language_sequence.index(self.spin_button_12.text()) + 1
        return None

    def spin_button_12_set_index(self, index):
        if index <= len(self.language_sequence):
            self.spin_button_12.setText(self.language_sequence[index - 1])
            config.set("SoundRandomization", "iDialoguesLanguage", str(index))
            self.change_sub_param(self.spin_button_12, index)
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
        self.change_sub_param(self.spin_button_13, index)
        return True
    
    def radio_button_group_1_checked(self):
        checked_1 = self.radio_button_1.isChecked()
        checked_2 = self.radio_button_2.isChecked()
        checked_3 = self.radio_button_3.isChecked()
        config.set("GameDifficulty", "bNormal",    str(checked_1).lower())
        config.set("GameDifficulty", "bHard",      str(checked_2).lower())
        config.set("GameDifficulty", "bNightmare", str(checked_3).lower())
    
    def radio_button_group_2_checked(self):
        checked_1 = self.radio_button_4.isChecked()
        checked_2 = self.radio_button_5.isChecked()
        checked_3 = self.radio_button_6.isChecked()
        config.set("SpecialMode", "bNone",         str(checked_1).lower())
        config.set("SpecialMode", "bCustomNG",     str(checked_2).lower())
        config.set("SpecialMode", "bProgressiveZ", str(checked_3).lower())
        self.custom_level_field.setVisible(checked_2)
    
    def preset_drop_down_changed(self, index):
        current = self.preset_drop_down.itemText(index)
        if current == "Custom":
            return
        main_num = preset_to_bytes[current]
        sub_num = self.get_param_bytes()[1]
        self.set_param_bytes(main_num, sub_num)

    def matches_preset(self):
        main_num = self.get_param_bytes()[0]
        if main_num in bytes_to_preset:
            self.preset_drop_down.setCurrentText(bytes_to_preset[main_num])
            return
        self.preset_drop_down.setCurrentText("Custom")

    def param_string_field_changed(self, text):
        #Check that input is valid hex
        try:
            main_num, sub_num = self.get_param_bytes()
        except ValueError:
            main_num, sub_num = (0, 0)
        self.set_param_bytes(main_num, sub_num)
        #Apply bytes to params
        for widget in main_widget_to_param:
            if (main_num & main_widget_to_param[widget] != 0) != widget.isChecked():
                widget.setChecked(not widget.isChecked())
        for widget in sub_widget_to_param:
            check = False
            index = getattr(self, f"{widget.accessibleName()}_get_index")()
            if not index:
                continue
            for num in range(2):
                if sub_num & sub_widget_to_param[widget]*0x1000**num != 0:
                    check = True
                    if index != shift_to_spin_index[num]:
                        check = getattr(self, f"{widget.accessibleName()}_set_index")(shift_to_spin_index[num])
            if not check and index != 2:
                getattr(self, f"{widget.accessibleName()}_set_index")(2)
    
    def add_main_param(self, widget):
        main_num, sub_num = self.get_param_bytes()
        extra_num = main_widget_to_param[widget]
        if main_num & extra_num == 0:
            main_num += extra_num
        self.set_param_bytes(main_num, sub_num)
    
    def remove_main_param(self, widget):
        main_num, sub_num = self.get_param_bytes()
        extra_num = main_widget_to_param[widget]
        if main_num & extra_num != 0:
            main_num -= extra_num
        self.set_param_bytes(main_num, sub_num)
    
    def change_sub_param(self, widget, index):
        main_num, sub_num = self.get_param_bytes()
        extra_num = sub_widget_to_param[widget]
        for num in range(2):
            abs_num = extra_num*0x1000**num
            if num == spin_index_to_shift[index]:
                if sub_num & abs_num == 0:
                    sub_num += abs_num
            else:
                if sub_num & abs_num != 0:
                    sub_num -= abs_num
        self.set_param_bytes(main_num, sub_num)
    
    def get_param_bytes(self):
        total_num = int(self.param_string_field.text(), 16)
        factor = 0x10**main_param_length
        return (total_num % factor, total_num // factor)
    
    def set_param_bytes(self, main_num, sub_num):
        factor = 0x10**main_param_length
        total_num = main_num + sub_num*factor
        self.param_string_field.setText(self.param_string_format.format(total_num).upper())
    
    def custom_level_field_changed(self):
        config.set("SpecialMode", "iCustomNGLevel", str(self.custom_level_field.value()))
    
    def starting_items_field_changed(self, text):
        config.set("StartWith", "sStartItem", text)
    
    def game_path_field_changed(self, text):
        config.set("Misc", "sGamePath", text)
    
    def seed_field_changed(self, text):
        if " " in text:
            self.seed_field.setText(text.replace(" ", ""))
        else:
            config.set("Misc", "sSeed", text)

    def seed_new_button_clicked(self):
        self.seed_field.setText(str(random.randint(1000000000, 9999999999)))
    
    def seed_test_button_clicked(self):
        #Check seed
        
        if not config.get("Misc", "sSeed"):
            return
        self.selected_seed = self.cast_seed(config.get("Misc", "sSeed"))
        self.selected_map = config.get("MapRandomization", "sSelectedMap") if config.getboolean("MapRandomization", "bRoomLayout") else ""
        
        #Start
        
        Manager.init()
        Manager.load_constant()
        
        Item.init()
        Enemy.init()
        Room.init()
        Bloodless.init()
        
        Item.set_logic_complexity(config.getint("ItemRandomization", "iOverworldPoolComplexity"))
        Bloodless.set_logic_complexity(config.getint("ExtraRandomization", "iBloodlessCandlesComplexity"))
        
        random.seed(self.selected_seed)
        if not self.selected_map and config.getboolean("MapRandomization", "bRoomLayout"):
            self.selected_map = random.choice(glob.glob("MapEdit\\Custom\\*.json")) if glob.glob("MapEdit\\Custom\\*.json") else ""
        Manager.load_map(self.selected_map)
        Room.get_map_info()
        
        if not config.getboolean("GameDifficulty", "bNormal"):
            Item.set_hard_mode()
        
        if DLCType.IGA in self.owned_dlc and not config.getboolean("Misc", "bIgnoreDLC"):
            Item.add_iga_dlc()
        
        if config.getboolean("EnemyRandomization", "bEnemyLocations"):
            random.seed(self.selected_seed)
            Enemy.randomize_enemy_locations()
        
        Item.fill_enemy_to_room()
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.selected_seed)
            Item.process_key_logic()
        
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            random.seed(self.selected_seed)
            Bloodless.randomize_bloodless_candles()
        
        box = QMessageBox(self)
        box.setWindowTitle("Test")
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            box.setText(Bloodless.create_log_string(self.selected_seed, self.selected_map))
        elif config.getboolean("ItemRandomization", "bOverworldPool"):
            box.setText(Item.create_log_string(self.selected_seed, self.selected_map, Enemy.enemy_replacement_invert))
        else:
            box.setText("No keys to randomize")
        box.exec()
    
    def seed_confirm_button_clicked(self):
        if not config.get("Misc", "sSeed"):
            return
        self.seed_box.close()
        self.pre_generate()
    
    def dlc_check_box_changed(self):
        checked = self.dlc_check_box.isChecked()
        config.set("Misc", "bIgnoreDLC", str(checked).lower())

    def cast_seed(self, seed):
        #Cast seed to another object type if possible
        try:
            return float(seed) if "." in seed else int(seed)
        except ValueError:
            return seed
    
    def setting_apply_button_clicked(self):
        if config.getint("Misc", "iWindowSize") == window_sizes[self.window_size_drop_down.currentIndex()]:
            self.setting_window.close()
            return
        config.set("Misc", "iWindowSize", str(window_sizes[self.window_size_drop_down.currentIndex()]))
        write_config()
        subprocess.Popen(f"{script_name}.exe")
        sys.exit()
    
    def label_change(self, filetype):
        files  = modified_files[filetype]["Files"]
        label  = modified_files[filetype]["Label"]
        string = f"Modified {filetype}:\n\n"
        files.sort()
        for file in files:
            string += f"{file}\n"
        label.setText(string)
    
    def add_to_modified_files(self, filetype, file, checkboxes):
        list   = modified_files[filetype]["Files"]
        change = True
        for checkbox in checkboxes:
            if checkbox.isChecked():
                change = False
        if change and not file in list:
            list.append(file)
            self.label_change(filetype)
    
    def remove_from_modified_files(self, filetype, file, checkboxes):
        list   = modified_files[filetype]["Files"]
        change = True
        for checkbox in checkboxes:
            if checkbox.isChecked():
                change = False
        if change and file in list:
            list.remove(file)
            self.label_change(filetype)

    def has_rando_options(self):
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
            if not config.get("MapRandomization", "sSelectedMap"):
                return True
        if config.getboolean("GraphicRandomization", "bOutfitColor"):
            if config.get("OutfitConfig", "sMiriamList"):
                return True
            if config.get("OutfitConfig", "sZangetsuList"):
                return True
        if config.getboolean("GraphicRandomization", "bBackerPortraits"):
            return True
        if config.getboolean("SoundRandomization", "bDialogues"):
            return True
        if config.getboolean("SoundRandomization", "bBackGroundMusic"):
            return True
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            return True
        return False

    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def get_dlc_info(self):
        #Shantae is on by default
        dlc_list = [DLCType.Shantae]
        #Steam
        if "steamapps" in config.get("Misc", "sGamePath"):
            steam_path = os.path.abspath(os.path.join(config.get("Misc", "sGamePath"), "../../.."))
            #Override the Steam path if the game path is on another drive
            library_config_path = f"{steam_path}\\libraryfolder.vdf"
            if os.path.isfile(library_config_path):
                with open(library_config_path, "r", encoding="utf8") as file_reader:
                    steam_exe_path = self.lowercase_vdf_dict(vdf.parse(file_reader))["libraryfolder"]["launcher"]
                    steam_path = os.path.split(steam_exe_path)[0]
            #Get user config
            user_config_path = f"{steam_path}\\config\\loginusers.vdf"
            if not os.path.isfile(user_config_path):
                self.dlc_failure()
                return dlc_list
            with open(f"{steam_path}\\config\\loginusers.vdf", "r", encoding="utf8") as file_reader:
                user_config = self.lowercase_vdf_dict(vdf.parse(file_reader))["users"]
            #Determine the Steam friend code based on their user ID
            steam_user = None
            for user in user_config:
                if user_config[user]["mostrecent"] == "1":
                    steam_user = int(user) - 76561197960265728
                    break
            #Get local config
            local_config_path = f"{steam_path}\\userdata\\{steam_user}\\config\\localconfig.vdf"
            if not os.path.isfile(local_config_path):
                self.dlc_failure()
                return dlc_list
            with open(local_config_path, "r", encoding="utf8") as file_reader:
                dlc_config = self.lowercase_vdf_dict(vdf.parse(file_reader))["userlocalconfigstore"]["apptickets"]
            #Check for DLC IDs in the config
            if "1041460" in dlc_config:
                dlc_list.append(DLCType.IGA)
            if "2380800" in dlc_config:
                dlc_list.append(DLCType.Succubus)
            if "2380801" in dlc_config:
                dlc_list.append(DLCType.MagicGirl)
            if "2380802" in dlc_config:
                dlc_list.append(DLCType.Japanese)
            if "2380803" in dlc_config:
                dlc_list.append(DLCType.Classic2)
            return dlc_list
        #GOG
        if "GOG Games" in config.get("Misc", "sGamePath"):
            #List the DLC IDs in the game path
            dlc_id_list = []
            for file in glob.glob(config.get("Misc", "sGamePath") + "\\*.hashdb"):
                file_name = os.path.split(os.path.splitext(file)[0])[-1]
                dlc_id_list.append(file_name.split("-")[-1])
            #Check for DLC IDs in the list
            if "2089941670" in dlc_id_list:
                dlc_list.append(DLCType.IGA)
            if "2021103941" in dlc_id_list:
                dlc_list.append(DLCType.Succubus)
            if "1841144430" in dlc_id_list:
                dlc_list.append(DLCType.MagicGirl)
            if "1255553972" in dlc_id_list:
                dlc_list.append(DLCType.Japanese)
            if "1229761293" in dlc_config:
                dlc_list.append(DLCType.Classic2)
            return dlc_list
        #Installation is unknown
        self.dlc_failure()
        return dlc_list
    
    def lowercase_vdf_dict(self, vdf_dict):
        new_dict = {}
        for key, value in vdf_dict.items():
            new_dict[key.lower()] = self.lowercase_vdf_dict(value) if type(value) is dict else value
        return new_dict
    
    def dlc_failure(self):
        box = QMessageBox(self)
        box.setWindowTitle("Warning")
        box.setIcon(QMessageBox.Warning)
        box.setText("Failed to retrieve DLC information from user installation. Proceeding without DLC.")
        box.exec()
    
    def update_file_info(self):
        for file in list(Manager.file_to_path):
            if "DLC_0002" in Manager.file_to_path[file] and not DLCType.IGA in self.owned_dlc or "Classic2" in Manager.file_to_path[file] and not DLCType.Classic2 in self.owned_dlc:
                del Manager.file_to_path[file]
                del Manager.file_to_type[file]
    
    def generate_button_clicked(self):
        #Check if path is valid
        
        if not self.is_game_path_valid():
            self.notify_error("Game path invalid, input the path to your game's data\n(...\\steamapps\\common\\Bloodstained Ritual of the Night).")
            return
        
        #Check if starting items are valid
        
        Manager.load_translation()
        self.starting_items = []
        for item in config.get("StartWith", "sStartItem").split(","):
            if not item:
                continue
            simple_name = Utility.simplify_item_name(item)
            if not simple_name in Manager.start_item_translation:
                self.notify_error("Starting item name invalid.")
                return
            item_name = Manager.start_item_translation[simple_name]
            if "Skilled" in item_name:
                self.starting_items.append(item_name.replace("Skilled", ""))
            self.starting_items.append(item_name)
        self.starting_items = list(dict.fromkeys(self.starting_items))
        
        #Check DLC
        
        Manager.load_file_info()
        self.owned_dlc = self.get_dlc_info()
        self.update_file_info()
        
        #Prompt seed options
        
        if self.has_rando_options():
            self.seed_box = QDialog(self)
            self.seed_box.setLayout(self.seed_window_layout)
            self.seed_box.setWindowTitle("Seed")
            self.seed_box.exec()
        else:
            self.pre_generate()
    
    def pre_generate(self):
        #Check if every asset is already cached
        
        if os.path.isdir(Manager.asset_dir): 
            cached_assets = []
            for root, dirs, files in os.walk(Manager.asset_dir):
                for file in files:
                    name = os.path.splitext(file)[0]
                    cached_assets.append(name)
            cached_assets = list(dict.fromkeys(cached_assets))
            asset_list = []
            for file in Manager.file_to_path:
                if not file in cached_assets:
                    asset_list.append(file)
        else:
            asset_list = list(Manager.file_to_path)
        
        self.import_assets(asset_list, self.generate_pak) if asset_list else self.generate_pak()
    
    def generate_pak(self):
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Initializing...", None, 0, 7, self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.selected_seed = self.cast_seed(config.get("Misc", "sSeed"))
        self.selected_map = config.get("MapRandomization", "sSelectedMap") if config.getboolean("MapRandomization", "bRoomLayout") else ""
        self.worker = Generate(self.progress_bar, self.selected_seed, self.selected_map, self.starting_items, self.owned_dlc)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(self.generate_finished)
        self.worker.signaller.error.connect(self.thread_failure)
        self.worker.start()
    
    def generate_finished(self):
        self.progress_bar.close()
        self.setEnabled(True)
        box = QMessageBox(self)
        box.setWindowTitle("Done")
        box.setText("Pak file generated !")
        box.exec()
    
    def update_finished(self):
        sys.exit()

    def browse_map_button_clicked(self):
        if config.get("MapRandomization", "sSelectedMap"):
            config.set("MapRandomization", "sSelectedMap", "")
        else:
            path = QFileDialog.getOpenFileName(parent=self, caption="Open", dir="MapEdit\\Custom", filter="*.json")[0]
            if path:
                config.set("MapRandomization", "sSelectedMap", path.replace("/", "\\"))
        self.reset_selected_map_state()
    
    def reset_selected_map_state(self):
        selected_map = config.get("MapRandomization", "sSelectedMap")
        if config.getboolean("MapRandomization", "bRoomLayout") and selected_map:
            self.browse_map_button.setIcon(QPixmap("Data\\cancel.png"))
            self.browse_map_button.setToolTip("Revert map selection back to random.")
            self.setWindowTitle(f"{script_name} ({selected_map})")
        else:
            self.browse_map_button.setIcon(QPixmap("Data\\browse.png"))
            self.browse_map_button.setToolTip("Manually browse a custom map to play on.")
            self.setWindowTitle(script_name)
    
    def outfit_config_button_clicked(self):
        miriam_selected_outfit_list   = config.get("OutfitConfig", "sMiriamList").split(",")
        zangetsu_selected_outfit_list = config.get("OutfitConfig", "sZangetsuList").split(",")
        for index in range(self.miriam_outfit_list.count()):
            item = self.miriam_outfit_list.item(index)
            item.setSelected(item.text() in miriam_selected_outfit_list)
        for index in range(self.zangetsu_outfit_list.count()):
            item = self.zangetsu_outfit_list.item(index)
            item.setSelected(item.text() in zangetsu_selected_outfit_list)
        max_size = max(self.miriam_outfit_list.count(), self.zangetsu_outfit_list.count())
        self.outfit_window = QDialog(self)
        self.outfit_window.setLayout(self.outfit_window_layout)
        self.outfit_window.setWindowTitle("Outfit")
        self.outfit_window.setFixedSize(0, self.size_multiplier*min(140 + max_size*24, 500))
        self.outfit_window.exec()
    
    def outfit_confirm_button_clicked(self):
        miriam_selected_outfit_list   = []
        zangetsu_selected_outfit_list = []
        for item in self.miriam_outfit_list.selectedItems():
            miriam_selected_outfit_list.append(item.text())
        for item in self.zangetsu_outfit_list.selectedItems():
            zangetsu_selected_outfit_list.append(item.text())
        miriam_selected_outfit_list.sort()
        zangetsu_selected_outfit_list.sort()
        config.set("OutfitConfig", "sMiriamList", ",".join(miriam_selected_outfit_list))
        config.set("OutfitConfig", "sZangetsuList", ",".join(zangetsu_selected_outfit_list))
        self.update_modified_files_for_outfit()
        self.outfit_window.close()
    
    def update_modified_files_for_outfit(self):
        if config.getboolean("GraphicRandomization", "bOutfitColor") and config.get("OutfitConfig", "sMiriamList"):
            self.add_to_modified_files("UI"     , "Face_Miriam"      , [])
            self.add_to_modified_files("Texture", "T_Body01_01_Color", [])
            self.add_to_modified_files("Texture", "T_Pl01_Cloth_Bace", [])
        else:
            self.remove_from_modified_files("UI"     , "Face_Miriam"      , [])
            self.remove_from_modified_files("Texture", "T_Body01_01_Color", [])
            self.remove_from_modified_files("Texture", "T_Pl01_Cloth_Bace", [])
        if config.getboolean("GraphicRandomization", "bOutfitColor") and config.get("OutfitConfig", "sZangetsuList"):
            self.add_to_modified_files("UI"     , "Face_Zangetsu"      , [])
            self.add_to_modified_files("Texture", "T_N1011_body_color" , [])
            self.add_to_modified_files("Texture", "T_N1011_face_color" , [])
            self.add_to_modified_files("Texture", "T_N1011_equip_color", [])
            self.add_to_modified_files("Texture", "T_Tknife05_Base"    , [])
        else:
            self.remove_from_modified_files("UI"     , "Face_Zangetsu"      , [])
            self.remove_from_modified_files("Texture", "T_N1011_body_color" , [])
            self.remove_from_modified_files("Texture", "T_N1011_face_color" , [])
            self.remove_from_modified_files("Texture", "T_N1011_equip_color", [])
            self.remove_from_modified_files("Texture", "T_Tknife05_Base"    , [])

    def browse_game_path_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.game_path_field.setText(path.replace("/", "\\"))
    
    def is_game_path_valid(self):
        return os.path.isdir(config.get("Misc", "sGamePath")) and os.path.isfile(config.get("Misc", "sGamePath") + "\\BloodstainedRotN.exe")

    def setting_button_clicked(self):
        self.window_size_drop_down.setCurrentIndex(window_sizes.index(config.getint("Misc", "iWindowSize")))
        self.setting_window = QDialog(self)
        self.setting_window.setLayout(self.setting_window_layout)
        self.setting_window.setWindowTitle("Settings")
        self.setting_window.setFixedSize(0, 0)
        self.setting_window.exec()

    def import_asset_button_clicked(self):
        #Check if path is valid
        
        if not self.is_game_path_valid():
            self.notify_error("Game path invalid, input the path to your game's data\n(...\\steamapps\\common\\Bloodstained Ritual of the Night).")
            return
        
        #Check DLC
        
        Manager.load_file_info()
        self.owned_dlc = self.get_dlc_info()
        self.update_file_info()
        
        self.import_assets(list(Manager.file_to_path), self.import_finished)

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
    
    def import_finished(self):
        self.setEnabled(True)

    def archipelago_button_clicked(self):
        self.archi_check_box.setChecked(config.getboolean("Archipelago", "bEnable"))
        self.archi_name_field.setText(config.get("Archipelago", "sName"))
        self.progression_field.setValue(config.getint("Archipelago", "iProgression"))
        self.accessibility_drop_down.setCurrentIndex(config.getint("Archipelago", "iAccessibility"))
        self.death_link_check_box.setChecked(config.getboolean("Archipelago", "bDeathLink"))
        self.archi_window = QDialog(self)
        self.archi_window.setLayout(self.archi_window_layout)
        self.archi_window.setWindowTitle("Archipelago")
        self.archi_window.setFixedSize(self.size_multiplier*400, 0)
        self.archi_window.exec()

    def archi_apply_button_clicked(self):
        config.set("Archipelago", "bEnable", str(self.archi_check_box.isChecked()).lower())
        config.set("Archipelago", "sName", self.archi_name_field.text())
        config.set("Archipelago", "iProgression", str(self.progression_field.value()))
        config.set("Archipelago", "iAccessibility", str(self.accessibility_drop_down.currentIndex()))
        config.set("Archipelago", "bDeathLink", str(self.death_link_check_box.isChecked()).lower())
        self.archi_window.close()

    def credit_button_clicked(self):
        credit_1_layout = QHBoxLayout()
        credit_1_label_image = QLabel()
        credit_1_label_image.setPixmap(QPixmap("Data\\profile1.png"))
        credit_1_label_image.setScaledContents(True)
        credit_1_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_1_layout.addWidget(credit_1_label_image)
        credit_1_label_text = QLabel()
        credit_1_label_text.setText("<span style=\"font-weight: bold; color: #67aeff;\">Lakifume</span><br/>Author of True Randomization<br/><a href=\"https://github.com/Lakifume\"><font face=Cambria color=#67aeff>Github</font></a>")
        credit_1_label_text.setOpenExternalLinks(True)
        credit_1_layout.addWidget(credit_1_label_text)
        credit_2_layout = QHBoxLayout()
        credit_2_label_image = QLabel()
        credit_2_label_image.setPixmap(QPixmap("Data\\profile2.png"))
        credit_2_label_image.setScaledContents(True)
        credit_2_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_2_layout.addWidget(credit_2_label_image)
        credit_2_label_text = QLabel()
        credit_2_label_text.setText("<span style=\"font-weight: bold; color: #e91e63;\">FatihG_</span><br/>Founder of Bloodstained Modding<br/><a href=\"http://discord.gg/b9XBH4f\"><font face=Cambria color=#e91e63>Discord</font></a>")
        credit_2_label_text.setOpenExternalLinks(True)
        credit_2_layout.addWidget(credit_2_label_text)
        credit_3_layout = QHBoxLayout()
        credit_3_label_image = QLabel()
        credit_3_label_image.setPixmap(QPixmap("Data\\profile3.png"))
        credit_3_label_image.setScaledContents(True)
        credit_3_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_3_layout.addWidget(credit_3_label_image)
        credit_3_label_text = QLabel()
        credit_3_label_text.setText("<span style=\"font-weight: bold; color: #e6b31a;\">Joneirik</span><br/>Datatable researcher<br/><a href=\"http://wiki.omf2097.com/doku.php?id=joneirik:bs:start\"><font face=Cambria color=#e6b31a>Wiki</font></a>")
        credit_3_label_text.setOpenExternalLinks(True)
        credit_3_layout.addWidget(credit_3_label_text)
        credit_4_layout = QHBoxLayout()
        credit_4_label_image = QLabel()
        credit_4_label_image.setPixmap(QPixmap("Data\\profile4.png"))
        credit_4_label_image.setScaledContents(True)
        credit_4_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_4_layout.addWidget(credit_4_label_image)
        credit_4_label_text = QLabel()
        credit_4_label_text.setText("<span style=\"font-weight: bold; color: #db1ee9;\">Atenfyr</span><br/>Creator of UAssetAPI<br/><a href=\"https://github.com/atenfyr/UAssetAPI\"><font face=Cambria color=#db1ee9>Github</font></a>")
        credit_4_label_text.setOpenExternalLinks(True)
        credit_4_layout.addWidget(credit_4_label_text)
        credit_5_layout = QHBoxLayout()
        credit_5_label_image = QLabel()
        credit_5_label_image.setPixmap(QPixmap("Data\\profile5.png"))
        credit_5_label_image.setScaledContents(True)
        credit_5_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_5_layout.addWidget(credit_5_label_image)
        credit_5_label_text = QLabel()
        credit_5_label_text.setText("<span style=\"font-weight: bold; color: #25c04e;\">Giwayume</span><br/>Creator of Bloodstained Level Editor<br/><a href=\"https://github.com/Giwayume/BloodstainedLevelEditor\"><font face=Cambria color=#25c04e>Github</font></a>")
        credit_5_label_text.setOpenExternalLinks(True)
        credit_5_layout.addWidget(credit_5_label_text)
        credit_6_layout = QHBoxLayout()
        credit_6_label_image = QLabel()
        credit_6_label_image.setPixmap(QPixmap("Data\\profile6.png"))
        credit_6_label_image.setScaledContents(True)
        credit_6_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_6_layout.addWidget(credit_6_label_image)
        credit_6_label_text = QLabel()
        credit_6_label_text.setText("<span style=\"font-weight: bold; color: #ffffff;\">Matyalatte</span><br/>Creator of UE4 DDS Tools<br/><a href=\"https://github.com/matyalatte/UE4-DDS-Tools\"><font face=Cambria color=#ffffff>Github</font></a>")
        credit_6_label_text.setOpenExternalLinks(True)
        credit_6_layout.addWidget(credit_6_label_text)
        credit_7_layout = QHBoxLayout()
        credit_7_label_image = QLabel()
        credit_7_label_image.setPixmap(QPixmap("Data\\profile7.png"))
        credit_7_label_image.setScaledContents(True)
        credit_7_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_7_layout.addWidget(credit_7_label_image)
        credit_7_label_text = QLabel()
        credit_7_label_text.setText("<span style=\"font-weight: bold; color: #7b9aff;\">Chrisaegrimm</span><br/>Testing and suffering<br/><a href=\"https://www.twitch.tv/chrisaegrimm\"><font face=Cambria color=#7b9aff>Twitch</font></a>")
        credit_7_label_text.setOpenExternalLinks(True)
        credit_7_layout.addWidget(credit_7_label_text)
        credit_8_layout = QHBoxLayout()
        credit_8_label_image = QLabel()
        credit_8_label_image.setPixmap(QPixmap("Data\\profile8.png"))
        credit_8_label_image.setScaledContents(True)
        credit_8_label_image.setFixedSize(self.size_multiplier*60, self.size_multiplier*60)
        credit_8_layout.addWidget(credit_8_label_image)
        credit_8_label_text = QLabel()
        credit_8_label_text.setText("<span style=\"font-weight: bold; color: #dd872e;\">Tourmi</span><br/>True Randomization Contributor<br/><a href=\"https://github.com/Tourmi\"><font face=Cambria color=#dd872e>Github</font></a>")
        credit_8_label_text.setOpenExternalLinks(True)
        credit_8_layout.addWidget(credit_8_label_text)
        credit_box_layout = QVBoxLayout()
        credit_box_layout.setSpacing(self.size_multiplier*10)
        credit_box_layout.addLayout(credit_1_layout)
        credit_box_layout.addLayout(credit_8_layout)
        credit_box_layout.addLayout(credit_4_layout)
        credit_box_layout.addLayout(credit_5_layout)
        credit_box_layout.addLayout(credit_6_layout)
        credit_box_layout.addLayout(credit_2_layout)
        credit_box_layout.addLayout(credit_3_layout)
        credit_box_layout.addLayout(credit_7_layout)
        credit_box = QDialog(self)
        credit_box.setLayout(credit_box_layout)
        credit_box.setWindowTitle("Credits")
        credit_box.setFixedSize(0, 0)
        credit_box.exec()
    
    def thread_failure(self, detail):
        self.progress_bar.close()
        self.setEnabled(True)
        print(detail)
        self.notify_error("An error has occured.\nCheck the command window for more detail.")
    
    def notify_error(self, message):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText(message)
        box.exec()
    
    def check_for_updates(self):
        if os.path.isfile("delete.me"):
            os.remove("delete.me")
        for index in range(3):
            if os.path.isfile(f"Tools\\UAssetAPI\\delete{index + 1}.me"):
                os.remove(f"Tools\\UAssetAPI\\delete{index + 1}.me")
        try:
            api = requests.get("https://api.github.com/repos/Lakifume/True-Randomization/releases/latest").json()
        except requests.ConnectionError:
            return False
        try:
            tag = api["tag_name"]
        except KeyError:
            return False
        if tag != config.get("Misc", "sVersion"):
            choice = QMessageBox.question(self, "Auto Updater", "New version found:\n\n" + api["body"] + "\n\nUpdate ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                if "Map Editor.exe" in (program.name() for program in psutil.process_iter()):
                    self.notify_error("MapEditor.exe is running, cannot overwrite.")
                    return False
                
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
                return True
        return False
    
    def check_for_resolution(self):
        if self.first_time:
            self.setting_button_clicked()
        self.setEnabled(True)
    
    def exception_hook(self, exc_type, exc_value, exc_traceback):
        traceback_format = traceback.format_exception(exc_type, exc_value, exc_traceback)
        traceback_string = "".join(traceback_format)
        print(traceback_string)
        self.notify_error("An error has occured.\nCheck the command window for more detail.")

def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(write_and_exit)
    main = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()