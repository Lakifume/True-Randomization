#Import subclasses
import Bloodless
import Enemy
import Equipment
import Item
import Library
import Manager
import Shard
import Sound
#Import GUI
from PySide6.QtCore import*
from PySide6.QtGui import*
from PySide6.QtWidgets import*
#Import modules
import configparser
import sys
import os
import shutil
import random
import requests
import zipfile
import subprocess
import psutil
import glob
import copy
import json

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

checkbox_list = []
    
map_num = len(glob.glob("MapEdit\\Custom\\*.json"))

presets = {
    "Empty": [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False
    ],
    "Trial": [
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        False,
        False,
        False,
        False,
        False,
        True ,
        True ,
        True ,
        False,
        False
    ],
    "Race": [
        True ,
        True ,
        True ,
        True ,
        False,
        True ,
        True ,
        True ,
        False,
        True ,
        True ,
        False,
        False,
        False,
        False,
        False,
        True ,
        True ,
        False,
        False,
        False
    ],
    "Meme": [
        True ,
        True ,
        True ,
        True ,
        False,
        True ,
        False,
        True ,
        False,
        True ,
        False,
        True ,
        True ,
        False,
        True ,
        False,
        True ,
        True ,
        True ,
        False,
        False
    ],
    "Risk": [
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        True ,
        False,
        False
    ],
    "Blood": [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True ,
        True ,
        False,
        True ,
        False
    ]
}

modified_files = {
    "DataTable": {
        "Files": [
            "PB_DT_AmmunitionMaster",
            "PB_DT_ArmorMaster",
            "PB_DT_ArtsCommandMaster",
            "PB_DT_BallisticMaster",
            "PB_DT_BloodlessAbilityData",
            "PB_DT_BookMaster",
            "PB_DT_BRVAttackDamage",
            "PB_DT_BRVCharacterParameters",
            "PB_DT_BulletMaster",
            "PB_DT_CharacterParameterMaster",
            "PB_DT_CharaUniqueParameterMaster",
            "PB_DT_CollisionMaster",
            "PB_DT_CoordinateParameter",
            "PB_DT_CraftMaster",
            "PB_DT_DamageMaster",
            "PB_DT_DialogueTableItems",
            "PB_DT_DropRateMaster",
            "PB_DT_EnchantParameterType",
            "PB_DT_ItemMaster",
            "PB_DT_QuestMaster",
            "PB_DT_RoomMaster",
            "PB_DT_ShardMaster",
            "PB_DT_SpecialEffectDefinitionMaster",
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
    "Blueprint": {
        "Files": [
            "PBExtraModeInfo_BP",
            "mXXXXX_XXX_Gimmick"
        ]
    },
    "Texture": {
        "Files": [
            "m51_EBT_BG",
            "m51_EBT_BG_01",
            "m51_EBT_Block",
            "m51_EBT_Block_00",
            "m51_EBT_Block_01",
            "m51_EBT_Door"
        ]
    },
    "UI": {
        "Files": [
            "frameMiriam",
            "icon"
        ]
    },
    "Sound": {
        "Files": [
            "ACT50_BRM"
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
    with open("Data\\config.ini", "w") as file_writer:
        config.write(file_writer)
    sys.exit()

#Threads

class Signaller(QObject):
    progress = Signal(int)
    finished = Signal(str)

class Generate(QThread):
    def __init__(self, progress_bar, seed, map):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.seed = seed
        self.map = map

    def run(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Initialize directories
        
        #Mod
        for i in list(Manager.file_to_path.values()):
            if not os.path.isdir(Manager.mod_dir + "\\" + i):
                os.makedirs(Manager.mod_dir + "\\" + i)
        
        #Logs
        if not os.path.isdir("SpoilerLog"):
            os.makedirs("SpoilerLog")
        for file in os.listdir("SpoilerLog"):
            file_path = os.path.join("SpoilerLog", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        #Open files
        
        self.progress_bar.setLabelText("Loading data...")
        
        Manager.init()
        Manager.load_game_data()
        Manager.load_mod_data()
        current += 1
        self.signaller.progress.emit(current)
        
        #Simplify data
        
        self.progress_bar.setLabelText("Processing data...")
        
        Manager.complex_to_simple()
        current += 1
        self.signaller.progress.emit(current)
        
        self.progress_bar.setLabelText("Randomizing...")
        
        #Init classes
        
        Item.init()
        Library.init()
        Shard.init()
        Enemy.init()
        Equipment.init()
        Sound.init()
        Bloodless.init()
        
        #Apply tweaks
        
        Manager.apply_tweaks()
        Shard.default_shard()
        
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
        
        #Hue
        
        random.seed(self.seed)
        miriam_hue   = random.choice(os.listdir("Data\\Texture\\Miriam"))
        zangetsu_hue = random.choice(os.listdir("Data\\Texture\\Zangetsu"))
        
        #Datatables
        
        if self.map:
            Manager.fix_custom_map()
            Item.unused_room_check()
            Enemy.enemy_rebalance()
        
        if not config.getboolean("GameDifficulty", "bNormal"):
            Item.hard_enemy_logic()
        
        if config.getboolean("GameMode", "bRandomizer"):
            Item.give_shortcut()
            Item.give_eye()
            Shard.eye_max_range()
            Item.unlock_all_quest()
            Item.all_hair_in_shop()
        else:
            Item.story_chest()
        
        if config.getboolean("StartWith", "bDoubleJump"):
            Item.give_extra("Doublejump")
        elif config.getboolean("StartWith", "bAccelerator"):
            Item.give_extra("Accelerator")
        
        if config.getboolean("ItemRandomization", "bRemoveInfinites"):
            Item.remove_infinite()
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.seed)
            Item.no_key_in_shop()
            Item.no_shard_craft()
            Item.extra_logic()
            Item.rand_overworld_key()
            Item.rand_overworld_pool(config.getboolean("EnemyRandomization", "bEnemyLevels") or config.getboolean("EnemyRandomization", "bEnemyTolerances"))
            Item.rand_overworld_shard()
        
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            random.seed(self.seed)
            Bloodless.extra_logic()
            Bloodless.candle_shuffle()
        
        if not config.getboolean("ItemRandomization", "bOverworldPool"):
            Item.deseema_fix()
        
        if config.getboolean("ItemRandomization", "bQuestPool"):
            random.seed(self.seed)
            Item.rand_quest_pool()
        
        if config.getboolean("ItemRandomization", "bShopPool"):
            random.seed(self.seed)
            Item.rand_shop_pool()
        
        if config.getboolean("ItemRandomization", "bQuestRequirements"):
            random.seed(self.seed)
            Item.rand_quest_requirement()
            Item.catering_quest_info()
        
        if self.map:
            Item.replace_silver_bromide()
            Item.no_enemy_quest_icon()
        
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"):
            random.seed(self.seed)
            Item.rand_shop_price(config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"))
        
        if config.getboolean("LibraryRandomization", "bMapRequirements") or config.getboolean("LibraryRandomization", "bTomeAppearance"):
            random.seed(self.seed)
            Library.rand_book(config.getboolean("LibraryRandomization", "bMapRequirements"), config.getboolean("LibraryRandomization", "bTomeAppearance"))
            Manager.write_log("LibraryTomes", Library.create_log())
        
        if config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"):
            random.seed(self.seed)
            Shard.rand_shard(config.getboolean("ShardRandomization", "bScaleMagicCostWithPower"))
        
        if config.getboolean("EquipmentRandomization", "bGlobalGearStats"):
            random.seed(self.seed)
            Equipment.rand_all_equip()
            Equipment.rand_all_weapon()
        
        if config.getboolean("EquipmentRandomization", "bCheatGearStats"):
            random.seed(self.seed)
            Equipment.rand_cheat_equip()
            Equipment.rand_cheat_weapon()
        
        if config.getboolean("SpecialMode", "bCustom"):
            Enemy.custom_enemy(config.getint("Misc", "iCustomLevel"))
        elif config.getboolean("EnemyRandomization", "bEnemyLevels"):
            random.seed(self.seed)
            Enemy.rand_enemy_level()
            Enemy.high_starting_stats()
            Manager.write_log("EnemyProperties", Enemy.create_log())
        
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            random.seed(self.seed)
            Enemy.rand_enemy_resist()
            Manager.write_log("EnemyProperties", Enemy.create_log())
        
        if config.getboolean("SoundRandomization", "bDialogues"):
            random.seed(self.seed)
            Sound.rand_dialogue()
        
        if config.getboolean("GameDifficulty", "bNormal"):
            Manager.remove_difficulties("Normal")
            Enemy.brv_damage(1.0)
        elif config.getboolean("GameDifficulty", "bHard"):
            Manager.default_nightmare_cheatcode()
            Manager.remove_difficulties("Hard")
            Enemy.hard_patterns()
            Enemy.brv_speed("AnimaionPlayRateHard")
            Enemy.brv_damage(Manager.datatable["PB_DT_CoordinateParameter"]["HardBossDamageRate"]["Value"])
        elif config.getboolean("GameDifficulty", "bNightmare"):
            Manager.default_nightmare_cheatcode()
            if config.getboolean("SpecialMode", "bProgressive"):
                Manager.remove_difficulties("Hard")
                Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Difficulty_Hard"] = "Nightmare"
                Enemy.zangetsu_progress()
                Enemy.nightmare_damage()
            else:
                Manager.remove_difficulties("Nightmare")
            Enemy.hard_patterns()
            Enemy.brv_speed("AnimaionPlayRateNightmare")
            Enemy.brv_damage(Manager.datatable["PB_DT_CoordinateParameter"]["NightmareBossDamageRate"]["Value"])
        
        if config.getboolean("SpecialMode", "bProgressive"):
            Enemy.zangetsu_no_stats()
            Enemy.zangetsu_growth(config.getboolean("GameDifficulty", "bNightmare"))
            Equipment.zangetsu_black_belt()
        
        Item.update_boss_crystal_color()
        Item.update_shard_candles()
        Bloodless.update_shard_candles()
        Enemy.update_special_properties()
        Equipment.update_special_properties()
        Manager.update_descriptions()
        
        if self.seed:
            Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Menu_RandomSeed"]            = "Seed # " + str(self.seed)
            Manager.stringtable["PBSystemStringTable"]["SYS_SEN_Randomizer_ConfirmSeed"]     = "Confirm Settings for Seed # " + str(self.seed)
            Manager.stringtable["PBSystemStringTable"]["SYS_SEN_RandomizerManual_Title"]     = "Enter 17791"
            Manager.stringtable["PBSystemStringTable"]["SYS_SEN_RandomizerSelect_Customize"] = "XXX"
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            Manager.write_log("KeyLocation", Item.create_log(self.seed, self.map))
        elif config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            Manager.write_log("KeyLocation", Bloodless.create_log(self.seed, self.map))
        
        Manager.connect_map()
        current += 1
        self.signaller.progress.emit(current)
        
        #Convert data
        
        self.progress_bar.setLabelText("Converting data...")
        
        Manager.simple_to_complex()
        current += 1
        self.signaller.progress.emit(current)
        
        #Write files
        
        self.progress_bar.setLabelText("Writing files...")
        
        #Remove the Dullhammer in the first galleon room on hard to prevent rough starts
        #That way you can at least save once before the game truly starts
        Manager.remove_level_actor("m01SIP_001_Enemy_Hard", ["Chr_N3015(1040)"])
        #Also remove the bone mortes from that one crowded room in galleon
        Manager.remove_level_actor("m01SIP_014_Enemy_Hard", ["Chr_N3004(4)", "Chr_N3005"])
        #Remove the iron maidens that were added by the devs in an update in the tall entrance shaft
        #This is to simplify the logic a bit as we have no control over the Craftwork shard placement
        #To compensate for this the cooldown on spike damage was reduced, making it less likely for the player to tank through
        Manager.remove_level_actor("m03ENT_000_Gimmick", ["BP_IronMaiden(766)", "BP_IronMaiden3"])
        
        Manager.write_files()
        
        #The recently added Kingdom 2 Crowns crossover area lacks any exclusive music, it just plays the regular cave theme
        #Since this is easy to fix via modding include it in this rando
        #Import the new music over one of the few unused slots, the slot ID is already referenced in the RoomMaster under MapEdit
        Manager.import_music("ACT50_BRM")
        
        #Edit the health bar frame slightly to give an easy visual cue to tell if someone is using the mod or not
        #This is especially useful on twitch as this difference is even visible from stream previews
        Manager.import_texture("frameMiriam")
        #Edit the file that contains all the icons in the game to give 8 bit weapons unique icons per rank
        #Otherwise it is almost impossible to tell which tier the weapon you're looking at actually is
        Manager.import_texture("icon")
        
        #The textures used in the 8 Bit Nightmare area have inconsistent formats and mostly use block compression which butchers the pixel arts completely
        #Once again an easy fix so include it here
        Manager.import_texture("m51_EBT_BG")
        Manager.import_texture("m51_EBT_BG_01")
        Manager.import_texture("m51_EBT_Block")
        Manager.import_texture("m51_EBT_Block_00")
        Manager.import_texture("m51_EBT_Block_01")
        Manager.import_texture("m51_EBT_Door")
        
        #Most map icons have fixed positions on the canvas and will not adapt to the position of the rooms
        #Might be possible to edit them via a blueprint but that's not worth it so remove them if custom map is chosen
        if self.map:
            Manager.import_texture("icon_8bitCrown")
            Manager.import_texture("Map_Icon_Keyperson")
            Manager.import_texture("Map_Icon_RootBox")
            Manager.import_texture("Map_StartingPoint")
        
        #Import chosen hues for Miriam and Zangetsu
        #While it is technically not necessary to first copy the textures out of the chosen folder we do it so that the random hue does not show up on the terminal
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            for i in os.listdir("Data\\Texture\\Miriam\\" + miriam_hue):
                shutil.copyfile("Data\\Texture\\Miriam\\" + miriam_hue + "\\" + i, "Data\\Texture\\" + i)
            
            Manager.import_texture("Face_Miriam")
            Manager.import_texture("T_Pl01_Cloth_Bace")
            Manager.import_texture("T_Body01_01_Color")
            
            for i in os.listdir("Data\\Texture\\Miriam\\" + miriam_hue):
                os.remove("Data\\Texture\\" + i)
        if config.getboolean("GraphicRandomization", "bZangetsuColor"):
            for i in os.listdir("Data\\Texture\\Zangetsu\\" + zangetsu_hue):
                shutil.copyfile("Data\\Texture\\Zangetsu\\" + zangetsu_hue + "\\" + i, "Data\\Texture\\" + i)
            
            Manager.import_texture("Face_Zangetsu")
            Manager.import_texture("T_N1011_body_color")
            Manager.import_texture("T_N1011_face_color")
            Manager.import_texture("T_N1011_weapon_color")
            Manager.import_texture("T_Tknife05_Base")
            
            for i in os.listdir("Data\\Texture\\Zangetsu\\" + zangetsu_hue):
                os.remove("Data\\Texture\\" + i)
        
        Manager.remove_unchanged()
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
        self.signaller.finished.emit(self.map)

class Update(QThread):
    def __init__(self, progress_bar, api):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.api = api

    def run(self):
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
        shutil.rmtree("Tools")
        
        #Extract
        
        os.rename(exe_name, "delete.me")
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
        sys.exit()

class Import(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.signaller = Signaller()

    def run(self):
        current = 0
        self.signaller.progress.emit(current)
        
        #Extract specific assets from the game's pak using UModel
        
        if os.path.isdir(Manager.asset_dir):
            shutil.rmtree(Manager.asset_dir)
        
        for i in Manager.file_to_path:
            output_path = os.path.abspath("")
            
            root = os.getcwd()
            os.chdir("Tools\\UModel")
            os.system("cmd /c umodel_64.exe -path=\"" + config.get("Misc", "sGamePath") + "\" -out=\"" + output_path + "\" -save \"" + Manager.asset_dir + "\\" + Manager.file_to_path[i] + "\\" + i + "\"")
            os.chdir(root)
            
            current += 1
            self.signaller.progress.emit(current)
        
        self.signaller.finished.emit("")

#GUI

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setEnabled(False)
        self.initUI()
        self.check_for_updates()

    def initUI(self):
        
        self.first_time = False
        if config.getfloat("Misc", "fWindowSize") != 0.8 and config.getfloat("Misc", "fWindowSize") != 0.9 and config.getfloat("Misc", "fWindowSize") != 1.0:
            config.set("Misc", "fWindowSize", "1.0")
            self.first_time = True
        
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: " + str(int(config.getfloat("Misc", "fWindowSize")*18)) + "px}"
        + "QComboBox{background-color: #21222e}"
        + "QMessageBox{background-color: #21222e}"
        + "QDialog{background-color: #21222e}"
        + "QProgressDialog{background-color: #21222e}"
        + "QPushButton{background-color: #21222e}"
        + "QSpinBox{background-color: #21222e}"
        + "QLineEdit{background-color: #21222e}"
        + "QMenu{background-color: #21222e}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: " + str(int(config.getfloat("Misc", "fWindowSize")*18)) + "px}")
        self.map = ""
        
        #Main layout
        
        grid = QGridLayout()
        grid.setSpacing(config.getfloat("Misc", "fWindowSize")*10)
        
        self.dummy_box = QGroupBox()
        grid.addWidget(self.dummy_box, 10, 1, 1, 4)

        #Label

        label = QLabel()
        label.setStyleSheet("border: 1px solid white")
        label.setPixmap(QPixmap("Data\\artwork.png"))
        label.setScaledContents(True)
        label.setFixedSize(config.getfloat("Misc", "fWindowSize")*550, config.getfloat("Misc", "fWindowSize")*978)
        grid.addWidget(label, 0, 0, 10, 1)
        
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
        grid.addWidget(self.box_6, 0, 3, 1, 2)

        box_7_grid = QGridLayout()
        self.box_7 = QGroupBox("Map Randomization")
        self.box_7.setLayout(box_7_grid)
        grid.addWidget(self.box_7, 1, 3, 1, 2)

        box_8_grid = QGridLayout()
        self.box_8 = QGroupBox("Graphic Randomization")
        self.box_8.setLayout(box_8_grid)
        grid.addWidget(self.box_8, 2, 3, 1, 2)

        box_9_grid = QGridLayout()
        self.box_9 = QGroupBox("Sound Randomization")
        self.box_9.setLayout(box_9_grid)
        grid.addWidget(self.box_9, 3, 3, 1, 2)
        
        box_10_left = QVBoxLayout()
        box_10_right = QVBoxLayout()
        box_10_box = QHBoxLayout()
        box_10_box.addLayout(box_10_left)
        box_10_box.addLayout(box_10_right)
        self.box_10 = QGroupBox("Extra Randomization")
        self.box_10.setLayout(box_10_box)
        grid.addWidget(self.box_10, 4, 3, 2, 2)
        
        box_11_grid = QGridLayout()
        box_11 = QGroupBox("Game Difficulty")
        box_11.setToolTip("Select the difficulty you'll be using in-game.")
        box_11.setLayout(box_11_grid)
        grid.addWidget(box_11, 6, 1, 1, 2)
        
        box_16_grid = QGridLayout()
        box_16 = QGroupBox("Start With")
        box_16.setToolTip("Select the shard you want to start the randomizer with.")
        box_16.setLayout(box_16_grid)
        grid.addWidget(box_16, 7, 1, 1, 2)
        
        box_13_grid = QGridLayout()
        box_13 = QGroupBox("Game Mode")
        box_13.setToolTip("Select the in-game mode this file is meant for.")
        box_13.setLayout(box_13_grid)
        grid.addWidget(box_13, 6, 3, 1, 2)
        
        box_17_grid = QGridLayout()
        box_17 = QGroupBox("Special Mode")
        box_17.setToolTip("Select from a few extra modes that this mod has to offer.")
        box_17.setLayout(box_17_grid)
        grid.addWidget(box_17, 7, 3, 1, 2)
        
        box_12_grid = QGridLayout()
        box_12 = QGroupBox("Presets")
        box_12.setLayout(box_12_grid)
        grid.addWidget(box_12, 8, 1, 1, 2)
        
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
        
        #Text label
        
        modified_files["DataTable"]["Label"] = QLabel(self)
        self.label_change("DataTable")
        box_15_left.addWidget(modified_files["DataTable"]["Label"])
        
        modified_files["StringTable"]["Label"] = QLabel(self)
        self.label_change("StringTable")
        box_15_left.addWidget(modified_files["StringTable"]["Label"])
        
        modified_files["Blueprint"]["Label"] = QLabel(self)
        self.label_change("Blueprint")
        box_15_left.addWidget(modified_files["Blueprint"]["Label"])
        
        modified_files["Texture"]["Label"] = QLabel(self)
        self.label_change("Texture")
        box_15_right.addWidget(modified_files["Texture"]["Label"])
        
        modified_files["UI"]["Label"] = QLabel(self)
        self.label_change("UI")
        box_15_right.addWidget(modified_files["UI"]["Label"])
        
        modified_files["Sound"]["Label"] = QLabel(self)
        self.label_change("Sound")
        box_15_right.addWidget(modified_files["Sound"]["Label"])

        #Checkboxes

        self.check_box_1 = QCheckBox("Overworld Pool")
        self.check_box_1.setToolTip("Randomize all items and shards found in the overworld, now with\nnew improved logic. Everything you pick up will be 100% random\nso say goodbye to the endless sea of fried fish.")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        box_1_grid.addWidget(self.check_box_1, 0, 0)
        checkbox_list.append(self.check_box_1)

        self.check_box_2 = QCheckBox("Shop Pool")
        self.check_box_2.setToolTip("Randomize all items sold at the shop.")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        box_1_grid.addWidget(self.check_box_2, 1, 0)
        checkbox_list.append(self.check_box_2)

        self.check_box_16 = QCheckBox("Quest Pool")
        self.check_box_16.setToolTip("Randomize all quest rewards.")
        self.check_box_16.stateChanged.connect(self.check_box_16_changed)
        box_1_grid.addWidget(self.check_box_16, 2, 0)
        checkbox_list.append(self.check_box_16)

        self.check_box_17 = QCheckBox("Quest Requirements")
        self.check_box_17.setToolTip("Randomize the requirements for Susie, Abigail and Lindsay's quests.\nBenjamin will still ask you for waystones.")
        self.check_box_17.stateChanged.connect(self.check_box_17_changed)
        box_1_grid.addWidget(self.check_box_17, 3, 0)
        checkbox_list.append(self.check_box_17)

        self.check_box_18 = QCheckBox("Remove Infinites")
        self.check_box_18.setToolTip("Guarantee Gebel's Glasses and Recycle Hat to never appear.\nUseful for runs that favor magic and bullet management.")
        self.check_box_18.stateChanged.connect(self.check_box_18_changed)
        box_1_grid.addWidget(self.check_box_18, 4, 0)
        checkbox_list.append(self.check_box_18)

        self.check_box_3 = QCheckBox("Item Cost And Selling Price")
        self.check_box_3.setToolTip("Randomize the cost and selling price of every item in the shop.")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        box_2_grid.addWidget(self.check_box_3, 0, 0)
        checkbox_list.append(self.check_box_3)

        self.check_box_4 = QCheckBox("Scale Selling Price With Cost")
        self.check_box_4.setToolTip("Make the selling price scale with the item's random cost.")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        box_2_grid.addWidget(self.check_box_4, 1, 0)
        checkbox_list.append(self.check_box_4)

        self.check_box_5 = QCheckBox("Map Requirements")
        self.check_box_5.setToolTip("Randomize the completion requirement for each tome.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        box_3_grid.addWidget(self.check_box_5, 0, 0)
        checkbox_list.append(self.check_box_5)

        self.check_box_6 = QCheckBox("Tome Appearance")
        self.check_box_6.setToolTip("Randomize which books are available in the game at all.\nDoes not affect Tome of Conquest.")
        self.check_box_6.stateChanged.connect(self.check_box_6_changed)
        box_3_grid.addWidget(self.check_box_6, 1, 0)
        checkbox_list.append(self.check_box_6)

        self.check_box_7 = QCheckBox("Shard Power And Magic Cost")
        self.check_box_7.setToolTip("Randomize the efficiency and MP cost of each shard.\nDoes not affect progression shards.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        box_4_grid.addWidget(self.check_box_7, 0, 0)
        checkbox_list.append(self.check_box_7)

        self.check_box_8 = QCheckBox("Scale Magic Cost With Power")
        self.check_box_8.setToolTip("Make the MP cost scale with the shard's random power.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        box_4_grid.addWidget(self.check_box_8, 1, 0)
        checkbox_list.append(self.check_box_8)

        self.check_box_23 = QCheckBox("Global Gear Stats")
        self.check_box_23.setToolTip("Slightly randomize the stats of all weapons and pieces of\nequipment with odds that still favor their original values.\nWARNING: Breaks the balance of playable Zangetsu !")
        self.check_box_23.stateChanged.connect(self.check_box_23_changed)
        box_5_grid.addWidget(self.check_box_23, 0, 0)
        checkbox_list.append(self.check_box_23)

        self.check_box_9 = QCheckBox("Cheat Gear Stats")
        self.check_box_9.setToolTip("Completely randomize the stats of the weapons, headgears\nand accessories that are originally obtained via cheatcodes.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        box_5_grid.addWidget(self.check_box_9, 1, 0)
        checkbox_list.append(self.check_box_9)

        self.check_box_10 = QCheckBox("Enemy Levels")
        self.check_box_10.setToolTip("Randomize the level of every enemy. Stats that scale with\nlevel include HP, attack, defense, luck, EXP and expertise.\nPicking this option will give you more starting HP and MP\nand reduce their growth to compensate.\nWARNING: Only recommended for Miriam mode !")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        box_6_grid.addWidget(self.check_box_10, 0, 0)
        checkbox_list.append(self.check_box_10)

        self.check_box_11 = QCheckBox("Enemy Tolerances")
        self.check_box_11.setToolTip("Randomize the first 8 resistance/weakness attributes of every enemy.\nWARNING: Only recommended for Miriam mode !")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        box_6_grid.addWidget(self.check_box_11, 1, 0)
        checkbox_list.append(self.check_box_11)

        self.check_box_12 = QCheckBox("Room Layout")
        self.check_box_12.setToolTip("Randomly pick from a folder of map presets (" + str(map_num) + ").\nWARNING: Only recommended for Miriam mode !")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        box_7_grid.addWidget(self.check_box_12, 0, 0)
        checkbox_list.append(self.check_box_12)

        self.check_box_13 = QCheckBox("Miriam Color")
        self.check_box_13.setToolTip("Randomize the hue of Miriam's outfit.")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        box_8_grid.addWidget(self.check_box_13, 0, 0)
        checkbox_list.append(self.check_box_13)

        self.check_box_14 = QCheckBox("Zangetsu Color")
        self.check_box_14.setToolTip("Randomize the hue of Zangetsu's outfit.")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        box_8_grid.addWidget(self.check_box_14, 1, 0)
        checkbox_list.append(self.check_box_14)

        self.check_box_15 = QCheckBox("Dialogues")
        self.check_box_15.setToolTip("Randomize all conversation lines in the game. Characters\nwill still retain their actual voice (let's not get weird).")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        box_9_grid.addWidget(self.check_box_15, 0, 0)
        checkbox_list.append(self.check_box_15)

        self.check_box_21 = QCheckBox("Bloodless Candles")
        self.check_box_21.setToolTip("Randomize candle placement in Bloodless mode.")
        self.check_box_21.stateChanged.connect(self.check_box_21_changed)
        box_10_left.addWidget(self.check_box_21)
        checkbox_list.append(self.check_box_21)

        self.check_box_22 = QCheckBox("Coming Soon")
        self.check_box_22.setToolTip("???")
        #self.check_box_22.stateChanged.connect(self.check_box_22_changed)
        self.check_box_22.setEnabled(False)
        box_10_left.addWidget(self.check_box_22)
        checkbox_list.append(self.check_box_22)
        
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
        
        self.radio_button_11 = QRadioButton("Nothing")
        self.radio_button_11.setToolTip("Start with no extra abilities.")
        self.radio_button_11.toggled.connect(self.radio_button_group_5_checked)
        box_16_grid.addWidget(self.radio_button_11, 0, 0)
        
        self.radio_button_12 = QRadioButton("Double Jump")
        self.radio_button_12.setToolTip("Start with the ability to double jump.")
        self.radio_button_12.toggled.connect(self.radio_button_group_5_checked)
        box_16_grid.addWidget(self.radio_button_12, 1, 0)
        
        self.radio_button_13 = QRadioButton("Accelerator")
        self.radio_button_13.setToolTip("Start with an accelerator shard.")
        self.radio_button_13.toggled.connect(self.radio_button_group_5_checked)
        box_16_grid.addWidget(self.radio_button_13, 0, 1)
        
        self.radio_button_4 = QRadioButton("Randomizer")
        self.radio_button_4.setToolTip("Adapt the file for randomizer mode.")
        self.radio_button_4.toggled.connect(self.radio_button_group_2_checked)
        box_13_grid.addWidget(self.radio_button_4, 0, 0)
        
        self.radio_button_6 = QRadioButton("Story")
        self.radio_button_6.setToolTip("Adapt the file for story mode.")
        self.radio_button_6.toggled.connect(self.radio_button_group_2_checked)
        box_13_grid.addWidget(self.radio_button_6, 1, 0)
        
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
        
        if config.getint("Misc", "iCustomLevel") < 1:
            config.set("Misc", "iCustomLevel", "1")
        if config.getint("Misc", "iCustomLevel") > 99:
            config.set("Misc", "iCustomLevel", "99")
        
        self.level_box = QSpinBox()
        self.level_box.setToolTip("Level of all enemies.")
        self.level_box.setRange(1, 99)
        self.level_box.setValue(config.getint("Misc", "iCustomLevel"))
        self.level_box.valueChanged.connect(self.new_level)
        self.level_box.setVisible(False)
        box_17_grid.addWidget(self.level_box, 1, 1)
        
        #Dropdown lists
        
        self.preset_drop_down = QComboBox()
        self.preset_drop_down.setToolTip("EMPTY: Clear all options.\nTRIAL: To get started with this mod.\nRACE: Most fitting for a King of Speed.\nMEME: Time to break the game.\nRISK: Chaos awaits !\nBLOOD: She needs more blood.")
        self.preset_drop_down.addItem("Custom")
        for i in presets:
            self.preset_drop_down.addItem(i)
        self.preset_drop_down.currentIndexChanged.connect(self.preset_drop_down_change)
        box_12_grid.addWidget(self.preset_drop_down, 0, 0)
        
        #Settings
        
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
        
        #Init checkboxes
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            self.check_box_1.setChecked(True)
        if config.getboolean("ItemRandomization", "bShopPool"):
            self.check_box_2.setChecked(True)
        if config.getboolean("ItemRandomization", "bQuestPool"):
            self.check_box_16.setChecked(True)
        if config.getboolean("ItemRandomization", "bQuestRequirements"):
            self.check_box_17.setChecked(True)
        if config.getboolean("ItemRandomization", "bRemoveInfinites"):
            self.check_box_18.setChecked(True)
        if config.getboolean("ShopRandomization", "bItemCostAndSellingPrice"):
            self.check_box_3.setChecked(True)
        if config.getboolean("ShopRandomization", "bScaleSellingPriceWithCost"):
            self.check_box_4.setChecked(True)
        if config.getboolean("LibraryRandomization", "bMapRequirements"):
            self.check_box_5.setChecked(True)
        if config.getboolean("LibraryRandomization", "bTomeAppearance"):
            self.check_box_6.setChecked(True)
        if config.getboolean("ShardRandomization", "bShardPowerAndMagicCost"):
            self.check_box_7.setChecked(True)
        if config.getboolean("ShardRandomization", "bScaleMagicCostWithPower"):
            self.check_box_8.setChecked(True)
        if config.getboolean("EquipmentRandomization", "bGlobalGearStats"):
            self.check_box_23.setChecked(True)
        if config.getboolean("EquipmentRandomization", "bCheatGearStats"):
            self.check_box_9.setChecked(True)
        if config.getboolean("EnemyRandomization", "bEnemyLevels"):
            self.check_box_10.setChecked(True)
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            self.check_box_11.setChecked(True)
        if config.getboolean("MapRandomization", "bRoomLayout"):
            self.check_box_12.setChecked(True)
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            self.check_box_13.setChecked(True)
        if config.getboolean("GraphicRandomization", "bZangetsuColor"):
            self.check_box_14.setChecked(True)
        if config.getboolean("SoundRandomization", "bDialogues"):
            self.check_box_15.setChecked(True)
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            self.check_box_21.setChecked(True)
        
        if config.getboolean("GameDifficulty", "bNormal"):
            self.radio_button_1.setChecked(True)
        elif config.getboolean("GameDifficulty", "bHard"):
            self.radio_button_2.setChecked(True)
        else:
            self.radio_button_3.setChecked(True)
        
        if config.getboolean("StartWith", "bNothing"):
            self.radio_button_11.setChecked(True)
        elif config.getboolean("StartWith", "bDoubleJump"):
            self.radio_button_12.setChecked(True)
        else:
            self.radio_button_13.setChecked(True)
        
        if config.getboolean("GameMode", "bRandomizer"):
            self.radio_button_4.setChecked(True)
        else:
            self.radio_button_6.setChecked(True)
        
        if config.getboolean("SpecialMode", "bNone"):
            self.radio_button_14.setChecked(True)
        elif config.getboolean("SpecialMode", "bCustom"):
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
        
        #Text field
        
        self.output_field = QLineEdit(config.get("Misc", "sGamePath"))
        self.output_field.setToolTip("Path to your game's data (...\BloodstainedRotN\Content\Paks)")
        self.output_field.textChanged[str].connect(self.new_output)
        box_14_grid.addWidget(self.output_field, 0, 0)
        
        browse_button = QPushButton()
        browse_button.setIcon(QPixmap("Data\\browse.png"))
        browse_button.clicked.connect(self.browse_button_clicked)
        box_14_grid.addWidget(browse_button, 0, 1)

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
        self.matches_preset()
        if self.check_box_1.isChecked():
            config.set("ItemRandomization", "bOverworldPool", "true")
            self.check_box_1.setStyleSheet("color: " + item_color)
            if self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            #Uncheck extra
            self.check_box_21.setChecked(False)
            self.check_box_22.setChecked(False)
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("ItemRandomization", "bOverworldPool", "false")
            self.check_box_1.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_2_changed(self):
        self.matches_preset()
        if self.check_box_2.isChecked():
            config.set("ItemRandomization", "bShopPool", "true")
            self.check_box_2.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            #Uncheck extra
            self.check_box_21.setChecked(False)
            self.check_box_22.setChecked(False)
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("ItemRandomization", "bShopPool", "false")
            self.check_box_2.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_16_changed(self):
        self.matches_preset()
        if self.check_box_16.isChecked():
            config.set("ItemRandomization", "bQuestPool", "true")
            self.check_box_16.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            #Uncheck extra
            self.check_box_21.setChecked(False)
            self.check_box_22.setChecked(False)
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("ItemRandomization", "bQuestPool", "false")
            self.check_box_16.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_17_changed(self):
        self.matches_preset()
        if self.check_box_17.isChecked():
            config.set("ItemRandomization", "bQuestRequirements", "true")
            self.check_box_17.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            #Uncheck extra
            self.check_box_21.setChecked(False)
            self.check_box_22.setChecked(False)
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("ItemRandomization", "bQuestRequirements", "false")
            self.check_box_17.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_18_changed(self):
        self.matches_preset()
        if self.check_box_18.isChecked():
            config.set("ItemRandomization", "bRemoveInfinites", "true")
            self.check_box_18.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            #Uncheck extra
            self.check_box_21.setChecked(False)
            self.check_box_22.setChecked(False)
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("ItemRandomization", "bRemoveInfinites", "false")
            self.check_box_18.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_3_changed(self):
        self.matches_preset()
        if self.check_box_3.isChecked():
            config.set("ShopRandomization", "bItemCostAndSellingPrice", "true")
            self.check_box_3.setStyleSheet("color: " + shop_color)
            if self.check_box_4.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
        else:
            config.set("ShopRandomization", "bItemCostAndSellingPrice", "false")
            self.check_box_3.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")
            self.check_box_4.setChecked(False)
        self.fix_background_glitch()

    def check_box_4_changed(self):
        self.matches_preset()
        if self.check_box_4.isChecked():
            config.set("ShopRandomization", "bScaleSellingPriceWithCost", "true")
            self.check_box_4.setStyleSheet("color: " + shop_color)
            if self.check_box_3.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
            self.check_box_3.setChecked(True)
        else:
            config.set("ShopRandomization", "bScaleSellingPriceWithCost", "false")
            self.check_box_4.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_5_changed(self):
        self.matches_preset()
        if self.check_box_5.isChecked():
            config.set("LibraryRandomization", "bMapRequirements", "true")
            self.check_box_5.setStyleSheet("color: " + library_color)
            if self.check_box_6.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
        else:
            config.set("LibraryRandomization", "bMapRequirements", "false")
            self.check_box_5.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_6_changed(self):
        self.matches_preset()
        if self.check_box_6.isChecked():
            config.set("LibraryRandomization", "bTomeAppearance", "true")
            self.check_box_6.setStyleSheet("color: " + library_color)
            if self.check_box_5.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
        else:
            config.set("LibraryRandomization", "bTomeAppearance", "false")
            self.check_box_6.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_7_changed(self):
        self.matches_preset()
        if self.check_box_7.isChecked():
            config.set("ShardRandomization", "bShardPowerAndMagicCost", "true")
            self.check_box_7.setStyleSheet("color: " + shard_color)
            if self.check_box_8.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
        else:
            config.set("ShardRandomization", "bShardPowerAndMagicCost", "false")
            self.check_box_7.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")
            self.check_box_8.setChecked(False)
        self.fix_background_glitch()

    def check_box_8_changed(self):
        self.matches_preset()
        if self.check_box_8.isChecked():
            config.set("ShardRandomization", "bScaleMagicCostWithPower", "true")
            self.check_box_8.setStyleSheet("color: " + shard_color)
            if self.check_box_7.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
            self.check_box_7.setChecked(True)
        else:
            config.set("ShardRandomization", "bScaleMagicCostWithPower", "false")
            self.check_box_8.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_23_changed(self):
        self.matches_preset()
        if self.check_box_23.isChecked():
            config.set("EquipmentRandomization", "bGlobalGearStats", "true")
            self.check_box_23.setStyleSheet("color: " + equip_color)
            if self.check_box_9.isChecked():
                self.box_5.setStyleSheet("color: " + equip_color)
        else:
            config.set("EquipmentRandomization", "bGlobalGearStats", "false")
            self.check_box_23.setStyleSheet("color: #ffffff")
            self.box_5.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_9_changed(self):
        self.matches_preset()
        if self.check_box_9.isChecked():
            config.set("EquipmentRandomization", "bCheatGearStats", "true")
            self.check_box_9.setStyleSheet("color: " + equip_color)
            if self.check_box_23.isChecked():
                self.box_5.setStyleSheet("color: " + equip_color)
        else:
            config.set("EquipmentRandomization", "bCheatGearStats", "false")
            self.check_box_9.setStyleSheet("color: #ffffff")
            self.box_5.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_10_changed(self):
        self.matches_preset()
        if self.check_box_10.isChecked():
            config.set("EnemyRandomization", "bEnemyLevels", "true")
            self.check_box_10.setStyleSheet("color: " + enemy_color)
            if self.check_box_11.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bEnemyLevels", "false")
            self.check_box_10.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_11_changed(self):
        self.matches_preset()
        if self.check_box_11.isChecked():
            config.set("EnemyRandomization", "bEnemyTolerances", "true")
            self.check_box_11.setStyleSheet("color: " + enemy_color)
            if self.check_box_10.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config.set("EnemyRandomization", "bEnemyTolerances", "false")
            self.check_box_11.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_12_changed(self):
        self.matches_preset()
        if self.check_box_12.isChecked():
            config.set("MapRandomization", "bRoomLayout", "true")
            self.check_box_12.setStyleSheet("color: " + map_color)
            self.box_7.setStyleSheet("color: " + map_color)
            if not self.map:
                self.add_to_list("UI", "icon_8bitCrown"    , [])
                self.add_to_list("UI", "Map_Icon_Keyperson", [])
                self.add_to_list("UI", "Map_Icon_RootBox"  , [])
                self.add_to_list("UI", "Map_StartingPoint" , [])
        else:
            config.set("MapRandomization", "bRoomLayout", "false")
            self.check_box_12.setStyleSheet("color: #ffffff")
            self.box_7.setStyleSheet("color: #ffffff")
            if not self.map:
                self.remove_from_list("UI", "icon_8bitCrown"    , [])
                self.remove_from_list("UI", "Map_Icon_Keyperson", [])
                self.remove_from_list("UI", "Map_Icon_RootBox"  , [])
                self.remove_from_list("UI", "Map_StartingPoint" , [])
        self.fix_background_glitch()

    def check_box_13_changed(self):
        self.matches_preset()
        if self.check_box_13.isChecked():
            config.set("GraphicRandomization", "bMiriamColor", "true")
            self.check_box_13.setStyleSheet("color: " + graphic_color)
            if self.check_box_14.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list("UI"     , "Face_Miriam"      , [])
            self.add_to_list("Texture", "T_Body01_01_Color", [])
            self.add_to_list("Texture", "T_Pl01_Cloth_Bace", [])
        else:
            config.set("GraphicRandomization", "bMiriamColor", "false")
            self.check_box_13.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list("UI"     , "Face_Miriam"      , [])
            self.remove_from_list("Texture", "T_Body01_01_Color", [])
            self.remove_from_list("Texture", "T_Pl01_Cloth_Bace", [])
        self.fix_background_glitch()

    def check_box_14_changed(self):
        self.matches_preset()
        if self.check_box_14.isChecked():
            config.set("GraphicRandomization", "bZangetsuColor", "true")
            self.check_box_14.setStyleSheet("color: " + graphic_color)
            if self.check_box_13.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list("UI"     , "Face_Zangetsu"      , [])
            self.add_to_list("Texture", "T_N1011_body_color" , [])
            self.add_to_list("Texture", "T_N1011_face_color" , [])
            self.add_to_list("Texture", "T_N1011_equip_color", [])
            self.add_to_list("Texture", "T_Tknife05_Base"    , [])
        else:
            config.set("GraphicRandomization", "bZangetsuColor", "false")
            self.check_box_14.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list("UI"     , "Face_Zangetsu"      , [])
            self.remove_from_list("Texture", "T_N1011_body_color" , [])
            self.remove_from_list("Texture", "T_N1011_face_color" , [])
            self.remove_from_list("Texture", "T_N1011_equip_color", [])
            self.remove_from_list("Texture", "T_Tknife05_Base"    , [])
        self.fix_background_glitch()

    def check_box_15_changed(self):
        self.matches_preset()
        if self.check_box_15.isChecked():
            config.set("SoundRandomization", "bDialogues", "true")
            self.check_box_15.setStyleSheet("color: " + sound_color)
            self.box_9.setStyleSheet("color: " + sound_color)
        else:
            config.set("SoundRandomization", "bDialogues", "false")
            self.check_box_15.setStyleSheet("color: #ffffff")
            self.box_9.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()

    def check_box_21_changed(self):
        self.matches_preset()
        if self.check_box_21.isChecked():
            config.set("ExtraRandomization", "bBloodlessCandles", "true")
            self.check_box_21.setStyleSheet("color: " + extra_color)
            if self.check_box_22.isChecked():
                self.box_10.setStyleSheet("color: " + extra_color)
            #Uncheck item
            self.check_box_1.setChecked(False)
            self.check_box_2.setChecked(False)
            self.check_box_16.setChecked(False)
            self.check_box_17.setChecked(False)
            self.check_box_18.setChecked(False)
            #Check story
            self.radio_button_6.setChecked(True)
        else:
            config.set("ExtraRandomization", "bBloodlessCandles", "false")
            self.check_box_21.setStyleSheet("color: #ffffff")
            self.box_10.setStyleSheet("color: #ffffff")
        self.fix_background_glitch()
    
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
    
    def radio_button_group_5_checked(self):
        if self.radio_button_11.isChecked():
            config.set("StartWith", "bNothing", "true")
            config.set("StartWith", "bDoubleJump", "false")
            config.set("StartWith", "bAccelerator", "false")
        elif self.radio_button_12.isChecked():
            config.set("StartWith", "bNothing", "false")
            config.set("StartWith", "bDoubleJump", "true")
            config.set("StartWith", "bAccelerator", "false")
            #Check randomizer
            self.radio_button_4.setChecked(True)
        else:
            config.set("StartWith", "bNothing", "false")
            config.set("StartWith", "bDoubleJump", "false")
            config.set("StartWith", "bAccelerator", "true")
            #Check randomizer
            self.radio_button_4.setChecked(True)

    def radio_button_group_2_checked(self):
        if self.radio_button_4.isChecked():
            config.set("GameMode", "bRandomizer", "true")
            config.set("GameMode", "bStory", "false")
            #Check special none
            self.radio_button_14.setChecked(True)
        else:
            config.set("GameMode", "bRandomizer", "false")
            config.set("GameMode", "bStory", "true")
            #Check start nothing
            self.radio_button_11.setChecked(True)
    
    def radio_button_group_6_checked(self):
        if self.radio_button_14.isChecked():
            self.level_box.setVisible(False)
            config.set("SpecialMode", "bNone", "true")
            config.set("SpecialMode", "bCustom", "false")
            config.set("SpecialMode", "bProgressive", "false")
        elif self.radio_button_5.isChecked():
            self.level_box.setVisible(True)
            config.set("SpecialMode", "bNone", "false")
            config.set("SpecialMode", "bCustom", "true")
            config.set("SpecialMode", "bProgressive", "false")
            #Check story
            self.radio_button_6.setChecked(True)
            #Fix background
            self.fix_background_glitch()
        else:
            self.level_box.setVisible(False)
            config.set("SpecialMode", "bNone", "false")
            config.set("SpecialMode", "bCustom", "false")
            config.set("SpecialMode", "bProgressive", "true")
            #Check story
            self.radio_button_6.setChecked(True)
    
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
        for i in range(len(checkbox_list)):
            checkbox_list[i].setChecked(presets[current][i])

    def matches_preset(self):
        for i in presets:
            is_preset = True
            for e in range(len(checkbox_list)):
                if not(presets[i][e] and checkbox_list[e].isChecked() or not presets[i][e] and not checkbox_list[e].isChecked()):
                    is_preset = False
            if is_preset:
                self.preset_drop_down.setCurrentText(i)
                return
        self.preset_drop_down.setCurrentText("Custom")
    
    def new_level(self):
        config.set("Misc", "iCustomLevel", str(self.level_box.value()))
    
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
        for i in checkboxes:
            if i.isChecked():
                change = False
        if change and not file in list:
            list.append(file)
            self.label_change(filetype)
    
    def remove_from_list(self, filetype, file, checkboxes):
        list   = modified_files[filetype]["Files"]
        change = True
        for i in checkboxes:
            if i.isChecked():
                change = False
        if change and file in list:
            list.remove(file)
            self.label_change(filetype)
    
    def label_change(self, filetype):
        files  = modified_files[filetype]["Files"]
        label  = modified_files[filetype]["Label"]
        string = "Modified " + filetype + ":\n\n"
        files.sort()
        for i in files:
            string += i + "\n"
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
        if config.getboolean("EnemyRandomization", "bEnemyLevels"):
            return True
        if config.getboolean("EnemyRandomization", "bEnemyTolerances"):
            return True
        if config.getboolean("MapRandomization", "bRoomLayout"):
            return True
        if config.getboolean("GraphicRandomization", "bMiriamColor"):
            return True
        if config.getboolean("GraphicRandomization", "bZangetsuColor"):
            return True
        if config.getboolean("SoundRandomization", "bDialogues"):
            return True
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            return True
        return False

    def generate_pak(self):
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Initializing...", None, 0, 6, self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.worker = Generate(self.progress_bar, self.seed, self.map)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(self.generate_finished)
        self.worker.start()
    
    def import_assets(self, finished):
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Importing assets...", None, 0, len(list(Manager.file_to_path)), self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.worker = Import()
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(finished)
        self.worker.start()
    
    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def generate_finished(self, map):
        box = QMessageBox(self)
        box.setWindowTitle("Done")
        text = "Pak file generated !"
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            text += "\n\nMake absolutely sure to use existing seed 17791 in the game randomizer for this to work."
        elif config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            text += "\n\nTo access Bloodless mode enter BLOODLESS as the in-game file username."
        box.setText(text)
        box.exec()
        self.setEnabled(True)
    
    def import_finished(self):
        self.setEnabled(True)
    
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
        
        Manager.init()
        Manager.load_mod_data()
        
        Item.init()
        Bloodless.init()
        
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
        
        if self.map_test:
            Item.unused_room_check()
        
        if not config.getboolean("GameDifficulty", "bNormal"):
            Item.hard_enemy_logic()
        
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            random.seed(self.seed_test)
            Item.extra_logic()
            Item.key_logic()
        
        if config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            random.seed(self.seed_test)
            Bloodless.extra_logic()
            Bloodless.candle_shuffle()
        
        box = QMessageBox(self)
        box.setWindowTitle("Test")
        if config.getboolean("ItemRandomization", "bOverworldPool"):
            box.setText(Item.create_log_string(self.seed_test, self.map_test))
        elif config.getboolean("ExtraRandomization", "bBloodlessCandles"):
            box.setText(Bloodless.create_log_string(self.seed_test, self.map_test))
        else:
            box.setText("No keys to randomize")
        box.exec()
    
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
            self.error("Game path invalid.")
            return
        
        #Prompt seed options
        
        self.seed = ""
        if self.check_rando_options():
            self.seed_box = QDialog(self)
            self.seed_box.setLayout(self.seed_layout)
            self.seed_box.setWindowTitle("Seed")
            self.seed_box.exec()
            if not self.seed:
                return
        
        #Start
        
        if os.path.isdir(Manager.asset_dir):
            self.generate_pak()
        else:
            self.import_assets(self.generate_pak)
    
    def button_6_clicked(self):
        #Check if path is valid
        
        if not config.get("Misc", "sGamePath") or not os.path.isdir(config.get("Misc", "sGamePath")) or config.get("Misc", "sGamePath").split("\\")[-1] != "Paks":
            self.error("Game path invalid.")
            return
        
        #Start
        
        self.import_assets(self.import_finished)
    
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
        label4_text.setText("<span style=\"font-weight: bold; color: #25c04e;\">BadmoonZ</span><br/>Randomizer researcher<br/><a href=\"https://github.com/BadmoonzZ/Bloodstained\"><font face=Cambria color=#25c04e>Github</font></a>")
        label4_text.setOpenExternalLinks(True)
        label5_image = QLabel()
        label5_image.setPixmap(QPixmap("Data\\profile5.png"))
        label5_image.setScaledContents(True)
        label5_image.setFixedSize(config.getfloat("Misc", "fWindowSize")*60, config.getfloat("Misc", "fWindowSize")*60)
        label5_text = QLabel()
        label5_text.setText("<span style=\"font-weight: bold; color: #db1ee9;\">Atenfyr</span><br/>Creator of UAssetAPI<br/><a href=\"https://github.com/atenfyr/UAssetAPI\"><font face=Cambria color=#db1ee9>Github</font></a>")
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
    
    def error(self, text):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText(text)
        box.exec()
    
    def check_for_updates(self):
        if os.path.isfile("delete.me"):
            os.remove("delete.me")
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
                if "Map Editor.exe" in (i.name() for i in psutil.process_iter()):
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