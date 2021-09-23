from GenerateArmorMaster import *
from GenerateAttackParameter import *
from GenerateBookMaster import *
from GenerateBloodlessAbilityData import *
from GenerateBloodlessGimmickData import *
from GenerateCharacterParameterMaster import *
from GenerateCoordinateParameter import *
from GenerateDialogueTableItems import *
from GenerateDropRateMaster import *
from GenerateMisc import *
from GenerateRandomHue import *
from GenerateRoomMaster import *
from GenerateShardMaster import *
from GenerateSpecialEffectDefinitionMaster import *
from GenerateWeaponMaster import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import json
import sys
import re
import os
import shutil
import random
import requests
import zipfile
import subprocess
import psutil

item_color = "#ff8080" 
shop_color = "#ffff80"
library_color = "#bf80ff"
shard_color = "#80ffff"
weapon_color = "#80ff80"
enemy_color = "#80bfff"
map_color = "#ffbf80"
graphic_color = "#80ffbf"
sound_color = "#ff80ff"
extra_color = "#ff80bf"

checkbox_list = []

empty_preset = [
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
]
trial_preset = [
    True,
    True,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    False,
    False,
    False,
    True,
    True,
    True,
    False,
    False
]
race_preset = [
    True,
    True,
    True,
    True,
    False,
    True,
    True,
    True,
    False,
    True,
    True,
    True,
    False,
    False,
    False,
    True,
    True,
    False,
    False,
    False
]
meme_preset = [
    True,
    True,
    False,
    False,
    False,
    True,
    False,
    True,
    False,
    True,
    False,
    True,
    False,
    True,
    False,
    True,
    True,
    True,
    False,
    False
]
all_in_preset = [
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    False,
    False
]
risk_preset = [
    True,
    True,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    False,
    False
]
    
map_num = len(os.listdir("MapEdit\\Custom"))

datatable_files = [
    "PB_DT_AmmunitionMaster",
    "PB_DT_ArmorMaster",
    "PB_DT_ArtsCommandMaster",
    "PB_DT_BallisticMaster",
    "PB_DT_BloodlessAbilityData",
    "PB_DT_BRVAttackDamage",
    "PB_DT_BulletMaster",
    "PB_DT_CharacterParameterMaster",
    "PB_DT_CharaUniqueParameterMaster",
    "PB_DT_CollisionMaster",
    "PB_DT_CoordinateParameter",
    "PB_DT_CraftMaster",
    "PB_DT_DamageMaster",
    "PB_DT_DropRateMaster",
    "PB_DT_EnchantParameterType",
    "PB_DT_ItemMaster",
    "PB_DT_RoomMaster",
    "PB_DT_ShardMaster",
    "PB_DT_SpecialEffectDefinitionMaster",
    "PB_DT_WeaponMaster",
    "PBMasterStringTable",
    "~datatable"
]
ui_files = [
    "~ui"
]
texture_files = [
    "m51_EBT_BG",
    "m51_EBT_BG_01",
    "m51_EBT_Block",
    "m51_EBT_Block_00",
    "m51_EBT_Block_01",
    "m51_EBT_Door",
    "~texture"
]
sound_files = [
    "~sound"
]

patch_list = []
write_list = [write_ammunition, write_arts, write_brv, write_unique, write_craft, write_damage, write_enchant, write_8bit]
json_list = []

#Config

with open("Data\\config.json", "r") as file_reader:
    config = json.load(file_reader)

def writing():
    with open("Data\\config.json", "w") as file_writer:
        file_writer.write(json.dumps(config, indent=2))

def writing_and_exit():
    with open("Data\\config.json", "w") as file_writer:
        file_writer.write(json.dumps(config, indent=2))
    sys.exit()

class Generate(QThread):
    updateProgress = Signal(int)
    
    def __init__(self, string):
        QThread.__init__(self)
        self.string = string

    def run(self):
        progress = 0
        self.updateProgress.emit(progress)
        
        #Serializer
        
        print("")
        for i in patch_list:
            if i == write_patched_room:
                i(self.string)
            else:
                i()
            progress += 1
            self.updateProgress.emit(progress)
            if i != write_patched_gimmick:
                print("")

        #UnrealPak
        
        root = os.getcwd()
        os.chdir("UnrealPak")
        os.system("cmd /c UnrealPak.exe \"Randomizer.pak\" -create=filelist.txt -compress Randomizer")
        os.chdir(root)
        
        progress += 1
        self.updateProgress.emit(progress)
        
        #Reset
        
        for root, dirs, files in os.walk("UnrealPak\\Mod"):
            for file in os.listdir(root):
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        #Move
        
        if config[13]["Value"]["String"]:
            shutil.move("UnrealPak\\Randomizer.pak", config[13]["Value"]["String"] + "\\Randomizer.pak")
        else:
            shutil.move("UnrealPak\\Randomizer.pak", "Randomizer.pak")
        
        writing_and_exit()

class Update(QThread):
    updateProgress = Signal(int)
    
    def __init__(self, progressBar, api):
        QThread.__init__(self)
        self.progressBar = progressBar
        self.api = api

    def run(self):
        progress = 0
        self.updateProgress.emit(progress)
        
        with open("True Randomization.zip", "wb") as file_writer:
            url = requests.get(self.api["assets"][0]["browser_download_url"], stream=True)
            for data in url.iter_content(chunk_size=4096):
                file_writer.write(data)
                progress += len(data)
                self.updateProgress.emit(progress)
        
        self.progressBar.setLabelText("Extracting...")
        
        os.rename("Randomizer.exe", "OldRandomizer.exe")
        with zipfile.ZipFile("True Randomization.zip", "r") as zip_ref:
            zip_ref.extractall("")
        os.remove("True Randomization.zip")
        
        subprocess.Popen("Randomizer.exe")
        sys.exit()

class Convert(QThread):
    updateProgress = Signal(int)
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        progress = 0
        self.updateProgress.emit(progress)
        
        for i in json_list:
            if i == "PB_DT_RoomMaster":
                shutil.copyfile("MapEdit\\Data\\Content\\" + i + ".json", "Serializer\\" + i + ".json")
            elif "_" in i:
                shutil.copyfile("Data\\" + i[6:] + "\\Content\\" + i + ".json", "Serializer\\" + i + ".json")
            else:
                shutil.copyfile("Data\\" + i[2:] + "\\Content\\" + i + ".json", "Serializer\\" + i + ".json")
            root = os.getcwd()
            os.chdir("Serializer")
            os.system("cmd /c UAsset2Json.exe -tobin " + i + ".json")
            os.remove(i + ".uasset")
            os.rename(i + ".bin", i + ".uasset")
            os.remove(i + ".json")
            os.chdir(root)
            progress += 1
            self.updateProgress.emit(progress)
        
        writing_and_exit()

#GUI

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setEnabled(False)
        self.initUI()
        self.check_for_updates()

    def initUI(self):
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: " + str(int(config[14]["Value"]["Size"]*18)) + "px}"
        + "QLabel{border: 1px}"
        + "QComboBox{background-color: #21222e}"
        + "QMessageBox{background-color: #21222e}"
        + "QDialog{background-color: #21222e}"
        + "QProgressDialog{background-color: #21222e}"
        + "QPushButton{background-color: #21222e}"
        + "QSpinBox{background-color: #21222e}"
        + "QLineEdit{background-color: #21222e}"
        + "QMenu{background-color: #21222e}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: " + str(int(config[14]["Value"]["Size"]*18)) + "px}")
        self.string = ""
        
        #MainLayout
        
        grid = QGridLayout()
        grid.setSpacing(config[14]["Value"]["Size"]*10)

        #Label

        label = QLabel()
        label.setStyleSheet("border: 1px solid white")
        label.setPixmap(QPixmap("Data\\artwork.png"))
        label.setScaledContents(True)
        label.setFixedSize(config[14]["Value"]["Size"]*550, config[14]["Value"]["Size"]*978)
        grid.addWidget(label, 0, 0, 10, 1)
        
        #Groupboxes

        p = re.compile(r'(\S)([A-Z])')

        box_1_grid = QGridLayout()
        self.box_1 = QGroupBox(re.sub(p, r"\1 \2", config[0]["Key"]))
        self.box_1.setLayout(box_1_grid)
        grid.addWidget(self.box_1, 0, 1, 2, 2)

        box_2_grid = QGridLayout()
        self.box_2 = QGroupBox(re.sub(p, r"\1 \2", config[1]["Key"]))
        self.box_2.setLayout(box_2_grid)
        grid.addWidget(self.box_2, 2, 1, 1, 2)

        box_3_grid = QGridLayout()
        self.box_3 = QGroupBox(re.sub(p, r"\1 \2", config[2]["Key"]))
        self.box_3.setLayout(box_3_grid)
        grid.addWidget(self.box_3, 3, 1, 1, 2)

        box_4_grid = QGridLayout()
        self.box_4 = QGroupBox(re.sub(p, r"\1 \2", config[3]["Key"]))
        self.box_4.setLayout(box_4_grid)
        grid.addWidget(self.box_4, 4, 1, 1, 2)

        box_5_grid = QGridLayout()
        self.box_5 = QGroupBox(re.sub(p, r"\1 \2", config[4]["Key"]))
        self.box_5.setLayout(box_5_grid)
        grid.addWidget(self.box_5, 0, 3, 1, 2)

        box_6_grid = QGridLayout()
        self.box_6 = QGroupBox(re.sub(p, r"\1 \2", config[5]["Key"]))
        self.box_6.setLayout(box_6_grid)
        grid.addWidget(self.box_6, 1, 3, 1, 2)

        box_7_grid = QGridLayout()
        self.box_7 = QGroupBox(re.sub(p, r"\1 \2", config[6]["Key"]))
        self.box_7.setLayout(box_7_grid)
        grid.addWidget(self.box_7, 2, 3, 1, 2)

        box_8_grid = QGridLayout()
        self.box_8 = QGroupBox(re.sub(p, r"\1 \2", config[7]["Key"]))
        self.box_8.setLayout(box_8_grid)
        grid.addWidget(self.box_8, 3, 3, 1, 2)

        box_9_grid = QGridLayout()
        self.box_9 = QGroupBox(re.sub(p, r"\1 \2", config[8]["Key"]))
        self.box_9.setLayout(box_9_grid)
        grid.addWidget(self.box_9, 4, 3, 1, 2)

        box_10_grid = QGridLayout()
        self.box_10 = QGroupBox(re.sub(p, r"\1 \2", config[9]["Key"]))
        self.box_10.setLayout(box_10_grid)
        grid.addWidget(self.box_10, 5, 1, 1, 4)
        
        box_11_grid = QGridLayout()
        box_11 = QGroupBox(re.sub(p, r"\1 \2", config[10]["Key"]))
        box_11.setLayout(box_11_grid)
        grid.addWidget(box_11, 6, 1, 1, 2)
        
        box_12_grid = QGridLayout()
        box_12 = QGroupBox("Presets")
        box_12.setLayout(box_12_grid)
        grid.addWidget(box_12, 7, 1, 1, 2)
        
        box_13_grid = QGridLayout()
        box_13 = QGroupBox(re.sub(p, r"\1 \2", config[11]["Key"]))
        box_13.setLayout(box_13_grid)
        grid.addWidget(box_13, 6, 3, 1, 2)
        
        box_14_grid = QGridLayout()
        box_14 = QGroupBox(re.sub(p, r"\1 \2", config[13]["Key"]))
        box_14.setLayout(box_14_grid)
        grid.addWidget(box_14, 7, 3, 1, 2)
        
        box_15_grid = QGridLayout()
        box_15 = QGroupBox()
        box_15.setLayout(box_15_grid)
        box_15.setFixedSize(config[14]["Value"]["Size"]*550, config[14]["Value"]["Size"]*978)
        grid.addWidget(box_15, 0, 5, 10, 1)
        
        box_16_grid = QGridLayout()
        box_16 = QGroupBox()
        box_16.setLayout(box_16_grid)
        box_1_grid.addWidget(box_16, 2, 0, 3, 1)
        
        #TextLabel
        
        self.datatable_label = QLabel(self)
        self.label_change(datatable_files)
        box_15_grid.addWidget(self.datatable_label, 0, 0)
        
        self.ui_label = QLabel(self)
        self.label_change(ui_files)
        box_15_grid.addWidget(self.ui_label, 1, 0)
        
        self.texture_label = QLabel(self)
        self.label_change(texture_files)
        box_15_grid.addWidget(self.texture_label, 0, 1)
        
        self.sound_label = QLabel(self)
        self.label_change(sound_files)
        box_15_grid.addWidget(self.sound_label, 1, 1)

        #Checkboxes

        self.check_box_1 = QCheckBox(re.sub(p, r"\1 \2", config[0]["Value"]["Option1Id"]), self)
        self.check_box_1.setToolTip("The primary purpose of this mod. Everything you pick up will\nbe 100% random. Say goodbye to the endless sea of fried fish.")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        box_1_grid.addWidget(self.check_box_1, 0, 0)
        checkbox_list.append(self.check_box_1)

        self.check_box_2 = QCheckBox(re.sub(p, r"\1 \2", config[0]["Value"]["Option2Id"]), self)
        self.check_box_2.setToolTip("Randomize the requirements for Susie, Abigail and Lindsay's quests.\nBenjamin will still ask you for waystones.")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        box_1_grid.addWidget(self.check_box_2, 1, 0)
        checkbox_list.append(self.check_box_2)

        self.check_box_16 = QCheckBox(re.sub(p, r"\1 \2", config[0]["Value"]["Option3Id"]), self)
        self.check_box_16.setToolTip("Shuffle key items between themselves.")
        self.check_box_16.stateChanged.connect(self.check_box_16_changed)
        box_16_grid.addWidget(self.check_box_16, 0, 0)
        checkbox_list.append(self.check_box_16)

        self.check_box_17 = QCheckBox(re.sub(p, r"\1 \2", config[0]["Value"]["Option4Id"]), self)
        self.check_box_17.setToolTip("Shuffle shard colors between themselves.")
        self.check_box_17.stateChanged.connect(self.check_box_17_changed)
        box_16_grid.addWidget(self.check_box_17, 1, 0)
        checkbox_list.append(self.check_box_17)

        self.check_box_18 = QCheckBox(re.sub(p, r"\1 \2", config[0]["Value"]["Option5Id"]), self)
        self.check_box_18.setToolTip("Guarantee Gebel's Glasses and Recycle to not appear in the item\npool. Useful for runs that favor magic and bullet management.")
        self.check_box_18.stateChanged.connect(self.check_box_18_changed)
        box_16_grid.addWidget(self.check_box_18, 2, 0)
        checkbox_list.append(self.check_box_18)

        self.check_box_3 = QCheckBox(re.sub(p, r"\1 \2", config[1]["Value"]["Option1Id"]), self)
        self.check_box_3.setToolTip("Randomize the cost and selling price of every item in the shop.")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        box_2_grid.addWidget(self.check_box_3, 0, 0)
        checkbox_list.append(self.check_box_3)

        self.check_box_4 = QCheckBox(re.sub(p, r"\1 \2", config[1]["Value"]["Option2Id"]), self)
        self.check_box_4.setToolTip("Make the selling price scale with the item's random cost.")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        box_2_grid.addWidget(self.check_box_4, 1, 0)
        checkbox_list.append(self.check_box_4)

        self.check_box_5 = QCheckBox(re.sub(p, r"\1 \2", config[2]["Value"]["Option1Id"]), self)
        self.check_box_5.setToolTip("Randomize the completion requirement for each tome.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        box_3_grid.addWidget(self.check_box_5, 0, 0)
        checkbox_list.append(self.check_box_5)

        self.check_box_6 = QCheckBox(re.sub(p, r"\1 \2", config[2]["Value"]["Option2Id"]), self)
        self.check_box_6.setToolTip("Randomize which books are available in the game at all.\nDoes not affect Tome of Conquest.")
        self.check_box_6.stateChanged.connect(self.check_box_6_changed)
        box_3_grid.addWidget(self.check_box_6, 1, 0)
        checkbox_list.append(self.check_box_6)

        self.check_box_7 = QCheckBox(re.sub(p, r"\1 \2", config[3]["Value"]["Option1Id"]), self)
        self.check_box_7.setToolTip("Randomize the efficiency and MP cost of each shard.\nDoes not affect progression shards.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        box_4_grid.addWidget(self.check_box_7, 0, 0)
        checkbox_list.append(self.check_box_7)

        self.check_box_8 = QCheckBox(re.sub(p, r"\1 \2", config[3]["Value"]["Option2Id"]), self)
        self.check_box_8.setToolTip("Make the MP cost scale with the shard's random power.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        box_4_grid.addWidget(self.check_box_8, 1, 0)
        checkbox_list.append(self.check_box_8)

        self.check_box_9 = QCheckBox(re.sub(p, r"\1 \2", config[4]["Value"]["Option1Id"]), self)
        self.check_box_9.setToolTip("Randomize the stats of the weapons, headgears and\naccessories that are originally obtained via cheatcodes.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        box_5_grid.addWidget(self.check_box_9, 0, 0)
        checkbox_list.append(self.check_box_9)

        self.check_box_10 = QCheckBox(re.sub(p, r"\1 \2", config[5]["Value"]["Option1Id"]), self)
        self.check_box_10.setToolTip("Randomize the level of every enemy. Stats that scale with\nlevel include HP, attack, defense, luck, EXP and expertise.\nPicking this option will give you more starting HP and MP\nand reduce their growth to compensate.")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        box_6_grid.addWidget(self.check_box_10, 0, 0)
        checkbox_list.append(self.check_box_10)

        self.check_box_11 = QCheckBox(re.sub(p, r"\1 \2", config[5]["Value"]["Option2Id"]), self)
        self.check_box_11.setToolTip("Randomize the first 8 resistance/weakness attributes of every enemy.")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        box_6_grid.addWidget(self.check_box_11, 1, 0)
        checkbox_list.append(self.check_box_11)

        self.check_box_12 = QCheckBox(re.sub(p, r"\1 \2", config[6]["Value"]["Option1Id"]), self)
        self.check_box_12.setToolTip("Randomly pick from a folder of map presets (" + str(map_num) + ").")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        box_7_grid.addWidget(self.check_box_12, 0, 0)
        checkbox_list.append(self.check_box_12)

        self.check_box_13 = QCheckBox(re.sub(p, r"\1 \2", config[7]["Value"]["Option1Id"]), self)
        self.check_box_13.setToolTip("Randomize the hue of Miriam's outfit.")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        box_8_grid.addWidget(self.check_box_13, 0, 0)
        checkbox_list.append(self.check_box_13)

        self.check_box_14 = QCheckBox(re.sub(p, r"\1 \2", config[7]["Value"]["Option2Id"]), self)
        self.check_box_14.setToolTip("Randomize the hue of Zangetsu's outfit.")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        box_8_grid.addWidget(self.check_box_14, 1, 0)
        checkbox_list.append(self.check_box_14)

        self.check_box_15 = QCheckBox(re.sub(p, r"\1 \2", config[8]["Value"]["Option1Id"]), self)
        self.check_box_15.setToolTip("Randomize all conversation lines in the game. Characters\nwill still retain their actual voice (let's not get weird).")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        box_9_grid.addWidget(self.check_box_15, 0, 0)
        checkbox_list.append(self.check_box_15)

        self.check_box_21 = QCheckBox(re.sub(p, r"\1 \2", config[9]["Value"]["Option1Id"]), self)
        self.check_box_21.setToolTip("Randomize candle placement in Bloodless mode.")
        self.check_box_21.stateChanged.connect(self.check_box_21_changed)
        box_10_grid.addWidget(self.check_box_21, 0, 0)
        checkbox_list.append(self.check_box_21)
        
        self.check_box_22 = QCheckBox(re.sub(p, r"\1 \2", config[9]["Value"]["Option2Id"]), self)
        self.check_box_22.setToolTip("Shuffle abilities and upgrades between themselves.")
        self.check_box_22.stateChanged.connect(self.check_box_22_changed)
        box_10_grid.addWidget(self.check_box_22, 1, 0)
        checkbox_list.append(self.check_box_22)

        #RadioButtons
        
        self.radio_button_1 = QRadioButton(re.sub(p, r"\1 \2", config[10]["Value"]["Option1Id"]))
        self.radio_button_1.setToolTip("Select the difficulty you'll be using in-game.")
        self.radio_button_1.toggled.connect(self.radio_button_group_1_checked)
        box_11_grid.addWidget(self.radio_button_1, 0, 0)
        
        self.radio_button_2 = QRadioButton(re.sub(p, r"\1 \2", config[10]["Value"]["Option2Id"]))
        self.radio_button_2.setToolTip("Select the difficulty you'll be using in-game.")
        self.radio_button_2.toggled.connect(self.radio_button_group_1_checked)
        box_11_grid.addWidget(self.radio_button_2, 1, 0)
        
        self.radio_button_4 = QRadioButton(re.sub(p, r"\1 \2", config[11]["Value"]["Option1Id"]))
        self.radio_button_4.setToolTip("Select the game mode that this file is meant for.")
        self.radio_button_4.toggled.connect(self.radio_button_group_2_checked)
        box_13_grid.addWidget(self.radio_button_4, 0, 0)
        
        self.radio_button_5 = QRadioButton(re.sub(p, r"\1 \2", config[11]["Value"]["Option2Id"]))
        self.radio_button_5.setToolTip("Select the game mode that this file is meant for.")
        self.radio_button_5.toggled.connect(self.radio_button_group_2_checked)
        box_13_grid.addWidget(self.radio_button_5, 1, 0)
        
        self.radio_button_6 = QRadioButton(re.sub(p, r"\1 \2", config[11]["Value"]["Option3Id"]))
        self.radio_button_6.setToolTip("Select the game mode that this file is meant for.")
        self.radio_button_6.toggled.connect(self.radio_button_group_2_checked)
        box_13_grid.addWidget(self.radio_button_6, 0, 1)
        
        if config[12]["Value"]["Level"] < 1:
            config[12]["Value"]["Level"] = 1
        if config[12]["Value"]["Level"] > 99:
            config[12]["Value"]["Level"] = 99
        
        self.level_box = QSpinBox()
        self.level_box.setToolTip("Select the level value that you want to apply to\nall enemies.")
        self.level_box.setRange(1, 99)
        self.level_box.setValue(config[12]["Value"]["Level"])
        self.level_box.valueChanged.connect(self.new_level)
        self.level_box.setVisible(False)
        box_13_grid.addWidget(self.level_box, 1, 1)
        
        #DropDownLists
        
        self.preset_drop_down = QComboBox()
        self.preset_drop_down.setToolTip("EMPTY: Clear all options.\nTRIAL: A good way to get started with this mod.\nRACE: Most fitting for one who seeks speed.\nMEME: Turn your brain off and annihilate everything.\nALL IN: A chaotic, challenging and safe way to play.\nRISK: May require glitches to complete.")
        self.preset_drop_down.addItem("Custom")
        self.preset_drop_down.addItem("Empty")
        self.preset_drop_down.addItem("Trial")
        self.preset_drop_down.addItem("Race")
        self.preset_drop_down.addItem("Meme")
        self.preset_drop_down.addItem("All in")
        self.preset_drop_down.addItem("Risk")
        self.preset_drop_down.currentIndexChanged.connect(self.preset_drop_down_change)
        box_12_grid.addWidget(self.preset_drop_down, 0, 0)
        
        #Settings
        
        self.setting_layout = QGridLayout()
        
        setting_box_grid = QGridLayout()
        setting_box = QGroupBox(re.sub(p, r"\1 \2", config[14]["Key"]))
        setting_box.setLayout(setting_box_grid)
        self.setting_layout.addWidget(setting_box, 0, 0, 1, 3)
        
        self.size_drop_down = QComboBox()
        self.size_drop_down.addItem("0.7")
        self.size_drop_down.addItem("0.8")
        self.size_drop_down.addItem("0.9")
        self.size_drop_down.addItem("1.0")
        self.size_drop_down.currentIndexChanged.connect(self.size_drop_down_change)
        setting_box_grid.addWidget(self.size_drop_down, 0, 0)
        
        setting_button = QPushButton("Apply")
        setting_button.clicked.connect(self.setting_button_clicked)
        self.setting_layout.addWidget(setting_button, 1, 1, 1, 1)
        
        #InitCheckboxes
        
        if config[0]["Value"]["Option1Value"]:
            self.check_box_1.setChecked(True)
        else:
            self.check_box_16.setEnabled(False)
            self.check_box_17.setEnabled(False)
            self.check_box_18.setEnabled(False)
        if config[0]["Value"]["Option2Value"]:
            self.check_box_2.setChecked(True)
        if config[0]["Value"]["Option3Value"]:
            self.check_box_16.setChecked(True)
        if config[0]["Value"]["Option4Value"]:
            self.check_box_17.setChecked(True)
        if config[0]["Value"]["Option5Value"]:
            self.check_box_18.setChecked(True)
        if config[1]["Value"]["Option1Value"]:
            self.check_box_3.setChecked(True)
        else:
            self.check_box_4.setEnabled(False)
        if config[1]["Value"]["Option2Value"]:
            self.check_box_4.setChecked(True)
        if config[2]["Value"]["Option1Value"]:
            self.check_box_5.setChecked(True)
        if config[2]["Value"]["Option2Value"]:
            self.check_box_6.setChecked(True)
        if config[3]["Value"]["Option1Value"]:
            self.check_box_7.setChecked(True)
        else:
            self.check_box_8.setEnabled(False)
        if config[3]["Value"]["Option2Value"]:
            self.check_box_8.setChecked(True)
        if config[4]["Value"]["Option1Value"]:
            self.check_box_9.setChecked(True)
        if config[5]["Value"]["Option1Value"]:
            self.check_box_10.setChecked(True)
        if config[5]["Value"]["Option2Value"]:
            self.check_box_11.setChecked(True)
        if config[6]["Value"]["Option1Value"]:
            self.check_box_12.setChecked(True)
        if config[7]["Value"]["Option1Value"]:
            self.check_box_13.setChecked(True)
        if config[7]["Value"]["Option2Value"]:
            self.check_box_14.setChecked(True)
        if config[8]["Value"]["Option1Value"]:
            self.check_box_15.setChecked(True)
        if config[9]["Value"]["Option1Value"]:
            self.check_box_21.setChecked(True)
        else:
            self.check_box_21_changed()
            self.check_box_22.setEnabled(False)
        if config[9]["Value"]["Option2Value"]:
            self.check_box_22.setChecked(True)
        
        if config[10]["Value"]["Option1Value"]:
            self.radio_button_1.setChecked(True)
        else:
            self.radio_button_2.setChecked(True)
        
        if config[11]["Value"]["Option1Value"]:
            self.radio_button_4.setChecked(True)
        elif config[11]["Value"]["Option2Value"]:
            self.radio_button_5.setChecked(True)
        else:
            self.radio_button_6.setChecked(True)
        
        if config[14]["Value"]["Size"] == 0.7:
            self.size_drop_down.setCurrentIndex(0)
        elif config[14]["Value"]["Size"] == 0.8:
            self.size_drop_down.setCurrentIndex(1)
        elif config[14]["Value"]["Size"] == 0.9:
            self.size_drop_down.setCurrentIndex(2)
        else:
            self.size_drop_down.setCurrentIndex(3)
        
        self.matches_preset()
        
        #TextField

        text_field = QLineEdit(config[13]["Value"]["String"], self)
        text_field.setToolTip("Use this field to link the path to your ~mods directory for a direct\ninstall.")
        text_field.textChanged[str].connect(self.new_text)
        box_14_grid.addWidget(text_field, 0, 0)

        #Buttons
        
        button_3 = QPushButton("Settings")
        button_3.setToolTip("Interface Settings.")
        button_3.clicked.connect(self.button_3_clicked)
        grid.addWidget(button_3, 8, 1, 1, 1)

        button_4 = QPushButton("Pick Map")
        button_4.setToolTip("Manually pick a custom map to play on (overrides the random map selection).")
        button_4.clicked.connect(self.button_4_clicked)
        grid.addWidget(button_4, 8, 2, 1, 1)

        button_5 = QPushButton("Generate")
        button_5.setToolTip("Generate .pak file with current settings.")
        button_5.clicked.connect(self.button_5_clicked)
        grid.addWidget(button_5, 9, 1, 1, 4)
        
        button_6 = QPushButton("Auto Convert")
        button_6.setToolTip("Convert all the .json files from the Data folder into .uasset automatically.\nOnly use this if you've made manual edits to those datatables and want\nto apply them to this mod.")
        button_6.clicked.connect(self.button_6_clicked)
        grid.addWidget(button_6, 8, 3, 1, 1)
        
        button_7 = QPushButton("Credits")
        button_7.setToolTip("The people involved with this mod.")
        button_7.clicked.connect(self.button_7_clicked)
        grid.addWidget(button_7, 8, 4, 1, 1)
        
        #Window
        
        self.setLayout(grid)
        self.setFixedSize(config[14]["Value"]["Size"]*1800, config[14]["Value"]["Size"]*1000)
        self.setWindowTitle("Randomizer")
        self.setWindowIcon(QIcon("Data\\icon.png"))
        
        #Background
        
        background = QPixmap("MapEdit\\Data\\background.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, background)
        self.show()        
        self.setPalette(palette)
        
        #Position
        
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        QApplication.processEvents()

    def check_box_1_changed(self):
        self.matches_preset()
        if self.check_box_1.isChecked():
            config[0]["Value"]["Option1Value"] = True
            self.check_box_1.setStyleSheet("color: " + item_color)
            if self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            self.check_box_16.setEnabled(True)
            self.check_box_17.setEnabled(True)
            self.check_box_18.setEnabled(True)
            if not self.string:
                self.add_to_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_2, self.check_box_12, self.radio_button_4])
        else:
            config[0]["Value"]["Option1Value"] = False
            self.check_box_1.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
            self.check_box_16.setEnabled(False)
            self.check_box_17.setEnabled(False)
            self.check_box_18.setEnabled(False)
            if not self.string:
                self.remove_from_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_2, self.check_box_12, self.radio_button_4])

    def check_box_2_changed(self):
        self.matches_preset()
        if self.check_box_2.isChecked():
            config[0]["Value"]["Option2Value"] = True
            self.check_box_2.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
            if not self.string:
                self.add_to_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_12, self.radio_button_4])
            self.add_to_list(datatable_files, "PBScenarioStringTable", [])
        else:
            config[0]["Value"]["Option2Value"] = False
            self.check_box_2.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")
            if not self.string:
                self.remove_from_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_12, self.radio_button_4])
            self.remove_from_list(datatable_files, "PBScenarioStringTable", [])

    def check_box_16_changed(self):
        self.matches_preset()
        if self.check_box_16.isChecked():
            config[0]["Value"]["Option3Value"] = True
            self.check_box_16.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_17.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config[0]["Value"]["Option3Value"] = False
            self.check_box_16.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")

    def check_box_17_changed(self):
        self.matches_preset()
        if self.check_box_17.isChecked():
            config[0]["Value"]["Option4Value"] = True
            self.check_box_17.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_18.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config[0]["Value"]["Option4Value"] = False
            self.check_box_17.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")

    def check_box_18_changed(self):
        self.matches_preset()
        if self.check_box_18.isChecked():
            config[0]["Value"]["Option5Value"] = True
            self.check_box_18.setStyleSheet("color: " + item_color)
            if self.check_box_1.isChecked() and self.check_box_2.isChecked() and self.check_box_16.isChecked() and self.check_box_17.isChecked():
                self.box_1.setStyleSheet("color: " + item_color)
        else:
            config[0]["Value"]["Option5Value"] = False
            self.check_box_18.setStyleSheet("color: #ffffff")
            self.box_1.setStyleSheet("color: #ffffff")

    def check_box_3_changed(self):
        self.matches_preset()
        if self.check_box_3.isChecked():
            config[1]["Value"]["Option1Value"] = True
            self.check_box_3.setStyleSheet("color: " + shop_color)
            if self.check_box_4.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
            self.check_box_4.setEnabled(True)
        else:
            config[1]["Value"]["Option1Value"] = False
            self.check_box_3.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")
            self.check_box_4.setEnabled(False)

    def check_box_4_changed(self):
        self.matches_preset()
        if self.check_box_4.isChecked():
            config[1]["Value"]["Option2Value"] = True
            self.check_box_4.setStyleSheet("color: " + shop_color)
            if self.check_box_3.isChecked():
                self.box_2.setStyleSheet("color: " + shop_color)
        else:
            config[1]["Value"]["Option2Value"] = False
            self.check_box_4.setStyleSheet("color: #ffffff")
            self.box_2.setStyleSheet("color: #ffffff")

    def check_box_5_changed(self):
        self.matches_preset()
        if self.check_box_5.isChecked():
            config[2]["Value"]["Option1Value"] = True
            self.check_box_5.setStyleSheet("color: " + library_color)
            if self.check_box_6.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
            self.add_to_list(datatable_files, "PB_DT_BookMaster", [self.check_box_6])
        else:
            config[2]["Value"]["Option1Value"] = False
            self.check_box_5.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
            self.remove_from_list(datatable_files, "PB_DT_BookMaster", [self.check_box_6])

    def check_box_6_changed(self):
        self.matches_preset()
        if self.check_box_6.isChecked():
            config[2]["Value"]["Option2Value"] = True
            self.check_box_6.setStyleSheet("color: " + library_color)
            if self.check_box_5.isChecked():
                self.box_3.setStyleSheet("color: " + library_color)
            self.add_to_list(datatable_files, "PB_DT_BookMaster", [self.check_box_5])
        else:
            config[2]["Value"]["Option2Value"] = False
            self.check_box_6.setStyleSheet("color: #ffffff")
            self.box_3.setStyleSheet("color: #ffffff")
            self.remove_from_list(datatable_files, "PB_DT_BookMaster", [self.check_box_5])

    def check_box_7_changed(self):
        self.matches_preset()
        if self.check_box_7.isChecked():
            config[3]["Value"]["Option1Value"] = True
            self.check_box_7.setStyleSheet("color: " + shard_color)
            if self.check_box_8.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
            self.check_box_8.setEnabled(True)
        else:
            config[3]["Value"]["Option1Value"] = False
            self.check_box_7.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")
            self.check_box_8.setEnabled(False)

    def check_box_8_changed(self):
        self.matches_preset()
        if self.check_box_8.isChecked():
            config[3]["Value"]["Option2Value"] = True
            self.check_box_8.setStyleSheet("color: " + shard_color)
            if self.check_box_7.isChecked():
                self.box_4.setStyleSheet("color: " + shard_color)
        else:
            config[3]["Value"]["Option2Value"] = False
            self.check_box_8.setStyleSheet("color: #ffffff")
            self.box_4.setStyleSheet("color: #ffffff")

    def check_box_9_changed(self):
        self.matches_preset()
        if self.check_box_9.isChecked():
            config[4]["Value"]["Option1Value"] = True
            self.check_box_9.setStyleSheet("color: " + weapon_color)
            self.box_5.setStyleSheet("color: " + weapon_color)
        else:
            config[4]["Value"]["Option1Value"] = False
            self.check_box_9.setStyleSheet("color: #ffffff")
            self.box_5.setStyleSheet("color: #ffffff")

    def check_box_10_changed(self):
        self.matches_preset()
        if self.check_box_10.isChecked():
            config[5]["Value"]["Option1Value"] = True
            self.check_box_10.setStyleSheet("color: " + enemy_color)
            if self.check_box_11.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config[5]["Value"]["Option1Value"] = False
            self.check_box_10.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")

    def check_box_11_changed(self):
        self.matches_preset()
        if self.check_box_11.isChecked():
            config[5]["Value"]["Option2Value"] = True
            self.check_box_11.setStyleSheet("color: " + enemy_color)
            if self.check_box_10.isChecked():
                self.box_6.setStyleSheet("color: " + enemy_color)
        else:
            config[5]["Value"]["Option2Value"] = False
            self.check_box_11.setStyleSheet("color: #ffffff")
            self.box_6.setStyleSheet("color: #ffffff")

    def check_box_12_changed(self):
        self.matches_preset()
        if self.check_box_12.isChecked():
            config[6]["Value"]["Option1Value"] = True
            self.check_box_12.setStyleSheet("color: " + map_color)
            self.box_7.setStyleSheet("color: " + map_color)
            if not self.string:
                self.add_to_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.radio_button_4])
                self.add_to_list(ui_files, "icon_8bitCrown", [])
                self.add_to_list(ui_files, "Map_Icon_Keyperson", [])
                self.add_to_list(ui_files, "Map_Icon_RootBox", [])
                self.add_to_list(ui_files, "Map_StartingPoint", [])
        else:
            config[6]["Value"]["Option1Value"] = False
            self.check_box_12.setStyleSheet("color: #ffffff")
            self.box_7.setStyleSheet("color: #ffffff")
            if not self.string:
                self.remove_from_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.radio_button_4])
                self.remove_from_list(ui_files, "icon_8bitCrown", [])
                self.remove_from_list(ui_files, "Map_Icon_Keyperson", [])
                self.remove_from_list(ui_files, "Map_Icon_RootBox", [])
                self.remove_from_list(ui_files, "Map_StartingPoint", [])

    def check_box_13_changed(self):
        self.matches_preset()
        if self.check_box_13.isChecked():
            config[7]["Value"]["Option1Value"] = True
            self.check_box_13.setStyleSheet("color: " + graphic_color)
            if self.check_box_14.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list(ui_files, "Face_Miriam", [])
            self.add_to_list(texture_files, "T_Body01_01_Color", [])
            self.add_to_list(texture_files, "T_Pl01_Cloth_Bace", [])
        else:
            config[7]["Value"]["Option1Value"] = False
            self.check_box_13.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list(ui_files, "Face_Miriam", [])
            self.remove_from_list(texture_files, "T_Body01_01_Color", [])
            self.remove_from_list(texture_files, "T_Pl01_Cloth_Bace", [])

    def check_box_14_changed(self):
        self.matches_preset()
        if self.check_box_14.isChecked():
            config[7]["Value"]["Option2Value"] = True
            self.check_box_14.setStyleSheet("color: " + graphic_color)
            if self.check_box_13.isChecked():
                self.box_8.setStyleSheet("color: " + graphic_color)
            self.add_to_list(ui_files, "Face_Zangetsu", [])
            self.add_to_list(texture_files, "T_N1011_body_color", [])
            self.add_to_list(texture_files, "T_N1011_face_color", [])
            self.add_to_list(texture_files, "T_N1011_weapon_color", [])
            self.add_to_list(texture_files, "T_Tknife05_Base", [])
        else:
            config[7]["Value"]["Option2Value"] = False
            self.check_box_14.setStyleSheet("color: #ffffff")
            self.box_8.setStyleSheet("color: #ffffff")
            self.remove_from_list(ui_files, "Face_Zangetsu", [])
            self.remove_from_list(texture_files, "T_N1011_body_color", [])
            self.remove_from_list(texture_files, "T_N1011_face_color", [])
            self.remove_from_list(texture_files, "T_N1011_weapon_color", [])
            self.remove_from_list(texture_files, "T_Tknife05_Base", [])

    def check_box_15_changed(self):
        self.matches_preset()
        if self.check_box_15.isChecked():
            config[8]["Value"]["Option1Value"] = True
            self.check_box_15.setStyleSheet("color: " + sound_color)
            self.box_9.setStyleSheet("color: " + sound_color)
            self.add_to_list(datatable_files, "PB_DT_DialogueTableItems", [])
        else:
            config[8]["Value"]["Option1Value"] = False
            self.check_box_15.setStyleSheet("color: #ffffff")
            self.box_9.setStyleSheet("color: #ffffff")
            self.remove_from_list(datatable_files, "PB_DT_DialogueTableItems", [])

    def check_box_21_changed(self):
        self.matches_preset()
        if self.check_box_21.isChecked():
            config[9]["Value"]["Option1Value"] = True
            self.check_box_21.setStyleSheet("color: " + extra_color)
            if self.check_box_22.isChecked():
                self.box_10.setStyleSheet("color: " + extra_color)
            self.check_box_22.setEnabled(True)
            self.remove_from_list(ui_files, "icon", [])
            self.remove_from_list(sound_files, "ACT50_BRM", [])
        else:
            config[9]["Value"]["Option1Value"] = False
            self.check_box_21.setStyleSheet("color: #ffffff")
            self.box_10.setStyleSheet("color: #ffffff")
            self.check_box_22.setEnabled(False)
            self.add_to_list(ui_files, "icon", [])
            self.add_to_list(sound_files, "ACT50_BRM", [])
    
    def check_box_22_changed(self):
        self.matches_preset()
        if self.check_box_22.isChecked():
            config[9]["Value"]["Option2Value"] = True
            self.check_box_22.setStyleSheet("color: " + extra_color)
            if self.check_box_21.isChecked():
                self.box_10.setStyleSheet("color: " + extra_color)
        else:
            config[9]["Value"]["Option2Value"] = False
            self.check_box_22.setStyleSheet("color: #ffffff")
            self.box_10.setStyleSheet("color: #ffffff")

    def radio_button_group_1_checked(self):
        if self.radio_button_1.isChecked():
            config[10]["Value"]["Option1Value"] = True
            config[10]["Value"]["Option2Value"] = False
        else:
            config[10]["Value"]["Option1Value"] = False
            config[10]["Value"]["Option2Value"] = True

    def radio_button_group_2_checked(self):
        if self.radio_button_4.isChecked():
            self.level_box.setVisible(False)
            config[11]["Value"]["Option1Value"] = True
            config[11]["Value"]["Option2Value"] = False
            config[11]["Value"]["Option3Value"] = False
            if not self.string:
                self.add_to_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.check_box_12])
        elif self.radio_button_5.isChecked():
            self.level_box.setVisible(True)
            config[11]["Value"]["Option1Value"] = False
            config[11]["Value"]["Option2Value"] = True
            config[11]["Value"]["Option3Value"] = False
            if not self.string:
                self.remove_from_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.check_box_12])
        else:
            self.level_box.setVisible(False)
            config[11]["Value"]["Option1Value"] = False
            config[11]["Value"]["Option2Value"] = False
            config[11]["Value"]["Option3Value"] = True
            if not self.string:
                self.remove_from_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.check_box_12])
    
    def preset_drop_down_change(self, index):
        if index == 1:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(empty_preset[i])
        elif index == 2:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(trial_preset[i])
        elif index == 3:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(race_preset[i])
        elif index == 4:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(meme_preset[i])
        elif index == 5:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(all_in_preset[i])
        elif index == 6:
            for i in range(len(checkbox_list)):
                checkbox_list[i].setChecked(risk_preset[i])

    def size_drop_down_change(self, index):
        if index == 0:
            config[14]["Value"]["Size"] = 0.7
        elif index == 1:
            config[14]["Value"]["Size"] = 0.8
        elif index == 2:
            config[14]["Value"]["Size"] = 0.9
        elif index == 3:
            config[14]["Value"]["Size"] = 1.0

    def matches_preset(self):
        is_preset_1 = True
        for i in range(len(checkbox_list)):
            if not(empty_preset[i] and checkbox_list[i].isChecked() or not empty_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_1 = False
        if is_preset_1:
            self.preset_drop_down.setCurrentIndex(1)
            return
        
        is_preset_2 = True
        for i in range(len(checkbox_list)):
            if not(trial_preset[i] and checkbox_list[i].isChecked() or not trial_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_2 = False
        if is_preset_2:
            self.preset_drop_down.setCurrentIndex(2)
            return
        
        is_preset_3 = True
        for i in range(len(checkbox_list)):
            if not(race_preset[i] and checkbox_list[i].isChecked() or not race_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_3 = False
        if is_preset_3:
            self.preset_drop_down.setCurrentIndex(3)
            return
        
        is_preset_4 = True
        for i in range(len(checkbox_list)):
            if not(meme_preset[i] and checkbox_list[i].isChecked() or not meme_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_4 = False
        if is_preset_4:
            self.preset_drop_down.setCurrentIndex(4)
            return
        
        is_preset_5 = True
        for i in range(len(checkbox_list)):
            if not(all_in_preset[i] and checkbox_list[i].isChecked() or not all_in_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_5 = False
        if is_preset_5:
            self.preset_drop_down.setCurrentIndex(5)
            return
        
        is_preset_6 = True
        for i in range(len(checkbox_list)):
            if not(risk_preset[i] and checkbox_list[i].isChecked() or not risk_preset[i] and not checkbox_list[i].isChecked()):
                is_preset_6 = False
        if is_preset_6:
            self.preset_drop_down.setCurrentIndex(6)
            return
        
        self.preset_drop_down.setCurrentIndex(0)
    
    def new_level(self):
        config[12]["Value"]["Level"] = self.level_box.value()
    
    def new_text(self, text):
        config[13]["Value"]["String"] = text
    
    def add_to_list(self, list, file, checkboxes):
        change = True
        for i in checkboxes:
            if i.isChecked():
                change = False
        if change and not file in list:
            list.append(file)
            self.label_change(list)
    
    def remove_from_list(self, list, file, checkboxes):
        change = True
        for i in checkboxes:
            if i.isChecked():
                change = False
        if change and file in list:
            list.remove(file)
            self.label_change(list)
    
    def label_change(self, list):
        if list == datatable_files:
            string = "Modified DataTable:\n\n"
            label = self.datatable_label
        elif list == ui_files:
            string = "Modified UI:\n\n"
            label = self.ui_label
        elif list == texture_files:
            string = "Modified Texture:\n\n"
            label = self.texture_label
        elif list == sound_files:
            string = "Modified Sound:\n\n"
            label = self.sound_label
        list.sort()
        for i in range(len(list) - 1):
            string += list[i] + "\n"
        label.setText(string)
    
    def setProgress(self, progress):
        self.progressBar.setValue(progress)
    
    def setting_button_clicked(self):
        writing()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def button_3_clicked(self):
        box = QDialog(self)
        box.setLayout(self.setting_layout)
        box.setWindowTitle("Settings")
        box.exec()
        self.size_drop_down.setCurrentIndex(3)

    def button_4_clicked(self):
        path = QFileDialog.getOpenFileName(parent=self, caption="Open", dir="MapEdit//Custom", filter="*.json")[0]
        if path:
            self.string = path.replace("/", "\\")
            self.setWindowTitle("Randomizer (" + self.string + ")")
            self.add_to_list(datatable_files, "PB_DT_QuestMaster", [self.check_box_1, self.check_box_2, self.check_box_12, self.radio_button_4])
            self.add_to_list(ui_files, "icon_8bitCrown", [self.check_box_12])
            self.add_to_list(ui_files, "Map_Icon_Keyperson", [self.check_box_12])
            self.add_to_list(ui_files, "Map_Icon_RootBox", [self.check_box_12])
            self.add_to_list(ui_files, "Map_StartingPoint", [self.check_box_12])

    def button_5_clicked(self):
        self.setEnabled(False)
        QApplication.processEvents()
        
        #CheckIfPathExists
        
        if config[13]["Value"]["String"] and not os.path.isdir(config[13]["Value"]["String"]):
            self.no_path()
            self.setEnabled(True)
            return
        
        #CheckSerializerInstallRequirement
        
        try:
            subprocess.check_call("Serializer\\UAsset2Json.exe", shell=True)
        except subprocess.CalledProcessError as error:
            self.install_3()
            self.setEnabled(True)
            return
        
        #CheckOffSetterInstallRequirement
        
        root = os.getcwd()
        os.chdir("OffSetter")
        os.system("cmd /c OffSetter.exe m08TWR_019_Gimmick.umap.temp -n -r -m 0 0")
        os.chdir(root)
        if os.path.isfile("OffSetter\\m08TWR_019_Gimmick.umap.temp.offset"):
            os.remove("OffSetter\\m08TWR_019_Gimmick.umap.temp.offset")
        else:
            self.install_5()
            self.setEnabled(True)
            return
        
        #InitializeSpoilerLog
        
        if not os.path.isdir("SpoilerLog"):
            os.makedirs("SpoilerLog")
        
        for file in os.listdir("SpoilerLog"):
            file_path = os.path.join("SpoilerLog", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        #Map
        
        if not self.string and config[6]["Value"]["Option1Value"]:
            if os.listdir("MapEdit\\Custom"):
                self.string = "MapEdit\\Custom\\" + random.choice(os.listdir("MapEdit\\Custom"))
        
        #Patch
        
        if config[11]["Value"]["Option1Value"]:
            unused_chest_check()
            if self.string:
                unused_room_check(self.string)
        
        if config[0]["Value"]["Option1Value"]:
            if not config[0]["Value"]["Option3Value"]:
                chaos_key()
            if not config[0]["Value"]["Option4Value"]:
                chaos_shard()
            if config[0]["Value"]["Option5Value"]:
                remove_infinite()
            rand_item_pool()
            rand_quest_pool()
            rand_shop_pool()
            no_card()
            write_drop_log()
        
        if config[0]["Value"]["Option2Value"]:
            quest_req(config[10]["Value"]["Option2Value"], bool(self.string))
            req_string()
        
        if config[1]["Value"]["Option1Value"]:
            rand_shop_price(config[1]["Value"]["Option2Value"])
        
        if config[2]["Value"]["Option1Value"] or config[2]["Value"]["Option2Value"]:
            rand_book(config[2]["Value"]["Option1Value"], config[2]["Value"]["Option2Value"])
            write_book_log()
        
        if config[3]["Value"]["Option1Value"]:
            rand_shard(config[3]["Value"]["Option2Value"])
            write_shard_log()
        
        if config[4]["Value"]["Option1Value"]:
            rand_equip()
            rand_weapon()
            write_armor_log()
            write_weapon_log()
        
        if config[5]["Value"]["Option1Value"] or config[5]["Value"]["Option2Value"] or config[11]["Value"]["Option2Value"]:
            rand_enemy(config[5]["Value"]["Option1Value"] or config[11]["Value"]["Option2Value"], config[5]["Value"]["Option2Value"], config[11]["Value"]["Option2Value"], config[12]["Value"]["Level"])
            if config[5]["Value"]["Option2Value"] or not config[11]["Value"]["Option2Value"]:
                write_chara_log()
        
        if config[5]["Value"]["Option1Value"] and not config[11]["Value"]["Option2Value"]:
            more_HPMP()
            low_HPMP_growth()
            bloodless_low_HPMP_growth()
            low_HPMP_cap()
            bloodless_all_upgrades()
        
        if self.string:
            no_quest_icon()
            create_room_log(self.string)
            write_map_log()
        
        if config[8]["Value"]["Option1Value"]:
            rand_dialogue()
        
        if config[9]["Value"]["Option1Value"]:
            if not config[9]["Value"]["Option2Value"]:
                chaos_candle()
            candle_shuffle()
            write_gimmick_log()
        
        if config[10]["Value"]["Option1Value"]:
            normal_bomber()
            normal_bael()
        
        if config[11]["Value"]["Option1Value"]:
            give_shortcut()
            give_eye()
            eye_max()
            all_quest()
            hair_app_shop()
            if self.string[-7:-5] == "_J":
                give_map_help("Doublejump")
            elif self.string[-7:-5] == "_I":
                give_map_help("Invert")
            elif self.string[-7:-5] == "_S":
                give_map_help("Deepsinker")
            elif self.string[-7:-5] == "_H":
                give_map_help("HighJump")
            elif self.string[-7:-5] == "_R":
                give_map_help("Reflectionray")
            elif self.string[-7:-5] == "_D":
                give_map_help("Dimensionshift")
            elif self.string[-7:-5] == "_A":
                give_map_help("Accelerator")
            elif self.string[-7:-5] == "_C":
                give_map_help("Bookofthechampion")
            elif self.string[-7:-5] == "_Z":
                give_map_help("Swordsman")
        
        #Write
        
        if config[0]["Value"]["Option1Value"] or config[11]["Value"]["Option1Value"]:
            patch_list.append(write_patched_drop)
        else:
            write_list.append(write_drop)
        
        if config[0]["Value"]["Option1Value"] or config[0]["Value"]["Option2Value"] or config[11]["Value"]["Option1Value"] or self.string:
            patch_list.append(write_patched_quest)
        
        if config[0]["Value"]["Option2Value"]:
            patch_list.append(write_patched_scenario)
        
        if config[0]["Value"]["Option1Value"] or config[1]["Value"]["Option1Value"] or config[11]["Value"]["Option1Value"]:
            patch_list.append(write_patched_item)
        else:
            write_list.append(write_item)
        
        if config[2]["Value"]["Option1Value"] or config[2]["Value"]["Option2Value"]:
            patch_list.append(write_patched_book)
        
        if config[3]["Value"]["Option1Value"] or config[11]["Value"]["Option1Value"]:
            patch_list.append(write_patched_shard)
        else:
            write_list.append(write_shard)
        
        if config[4]["Value"]["Option1Value"]:
            patch_list.append(write_patched_weapon)
            patch_list.append(write_patched_armor)
            patch_list.append(write_patched_master)
        else:
            write_list.append(write_weapon)
            write_list.append(write_armor)
            write_list.append(write_master)
        
        if config[5]["Value"]["Option1Value"] or config[5]["Value"]["Option2Value"] or config[11]["Value"]["Option2Value"]:
            patch_list.append(write_patched_chara)
        else:
            write_list.append(write_chara)
        
        if config[5]["Value"]["Option1Value"] and not config[11]["Value"]["Option2Value"]:
            patch_list.append(write_patched_effect)
            patch_list.append(write_patched_coordinate)
            patch_list.append(write_patched_bloodless)
        else:
            write_list.append(write_effect)
            write_list.append(write_coordinate)
            write_list.append(write_bloodless)
        
        if self.string:
            patch_list.append(write_patched_room)
            write_list.append(write_crown_icon)
            write_list.append(write_map_icon)
        else:
            write_list.append(write_room)
        
        if config[7]["Value"]["Option1Value"]:
            write_list.append(write_miriam)
        
        if config[7]["Value"]["Option2Value"]:
            write_list.append(write_zangetsu)
        
        if config[8]["Value"]["Option1Value"]:
            patch_list.append(write_patched_dialogue)
        
        if config[9]["Value"]["Option1Value"]:
            patch_list.append(write_patched_gimmick)
        else:
            write_list.append(write_icon)
            write_list.append(write_brm)
        
        if config[10]["Value"]["Option1Value"]:
            patch_list.append(write_patched_ballistic)
            patch_list.append(write_patched_bullet)
            patch_list.append(write_patched_collision)
        else:
            write_list.append(write_ballistic)
            write_list.append(write_bullet)
            write_list.append(write_collision)
        
        if config[11]["Value"]["Option1Value"]:
            write_list.append(write_options)
        
        for i in write_list:
            i()
        
        #Process
        
        self.progressBar = QProgressDialog("Generating...", None, 0, len(patch_list) + 1, self)
        self.progressBar.setWindowTitle("Status")
        self.progressBar.setWindowModality(Qt.WindowModal)
        self.progressBar.setAutoClose(False)
        self.progressBar.setAutoReset(False)
        
        self.worker = Generate(self.string)
        self.worker.updateProgress.connect(self.setProgress)
        self.worker.start()
    
    def button_6_clicked(self):
        self.setEnabled(False)
        QApplication.processEvents()
        
        for i in os.listdir("Data"):
            if os.path.isdir("Data\\" + i) and i != "Hue":
                json_list.append(os.listdir("Data\\" + i + "\\Content")[0][:-5])
        json_list.append(os.listdir("MapEdit\\Data\\Content")[0][:-5])
        
        self.progressBar = QProgressDialog("Converting...", None, 0, len(json_list), self)
        self.progressBar.setWindowTitle("Status")
        self.progressBar.setWindowModality(Qt.WindowModal)
        self.progressBar.setAutoClose(False)
        self.progressBar.setAutoReset(False)
        
        self.worker = Convert()
        self.worker.updateProgress.connect(self.setProgress)
        self.worker.start()
    
    def button_7_clicked(self):
        label1_image = QLabel()
        label1_image.setPixmap(QPixmap("Data\\profile1.png"))
        label1_image.setScaledContents(True)
        label1_image.setFixedSize(config[14]["Value"]["Size"]*60, config[14]["Value"]["Size"]*60)
        label1_text = QLabel()
        label1_text.setText("<span style=\"font-weight: bold; color: #67aeff;\">Lakifume</span><br/>Author of True Randomization<br/><a href=\"https://github.com/Lakifume\"><font face=Cambria color=#67aeff>Github</font></a>")
        label1_text.setOpenExternalLinks(True)
        label2_image = QLabel()
        label2_image.setPixmap(QPixmap("Data\\profile2.png"))
        label2_image.setScaledContents(True)
        label2_image.setFixedSize(config[14]["Value"]["Size"]*60, config[14]["Value"]["Size"]*60)
        label2_text = QLabel()
        label2_text.setText("<span style=\"font-weight: bold; color: #e91e63;\">FatihG_</span><br/>Founder of Bloodstained Modding<br/><a href=\"http://discord.gg/b9XBH4f\"><font face=Cambria color=#e91e63>Discord</font></a>")
        label2_text.setOpenExternalLinks(True)
        label3_image = QLabel()
        label3_image.setPixmap(QPixmap("Data\\profile3.png"))
        label3_image.setScaledContents(True)
        label3_image.setFixedSize(config[14]["Value"]["Size"]*60, config[14]["Value"]["Size"]*60)
        label3_text = QLabel()
        label3_text.setText("<span style=\"font-weight: bold; color: #e6b31a;\">Joneirik</span><br/>Datatable researcher<br/><a href=\"http://wiki.omf2097.com/doku.php?id=joneirik:bs:start\"><font face=Cambria color=#e6b31a>Wiki</font></a>")
        label3_text.setOpenExternalLinks(True)
        label4_image = QLabel()
        label4_image.setPixmap(QPixmap("Data\\profile4.png"))
        label4_image.setScaledContents(True)
        label4_image.setFixedSize(config[14]["Value"]["Size"]*60, config[14]["Value"]["Size"]*60)
        label4_text = QLabel()
        label4_text.setText("<span style=\"font-weight: bold; color: #25c04e;\">BadmoonZ</span><br/>Randomizer researcher<br/><a href=\"https://github.com/BadmoonzZ/Bloodstained\"><font face=Cambria color=#25c04e>Github</font></a>")
        label4_text.setOpenExternalLinks(True)
        label5_image = QLabel()
        label5_image.setPixmap(QPixmap("Data\\profile5.png"))
        label5_image.setScaledContents(True)
        label5_image.setFixedSize(config[14]["Value"]["Size"]*60, config[14]["Value"]["Size"]*60)
        label5_text = QLabel()
        label5_text.setText("<span style=\"font-weight: bold; color: #7b9aff;\">Chrisaegrimm</span><br/>Testing and suffering<br/><a href=\"https://www.twitch.tv/chrisaegrimm\"><font face=Cambria color=#7b9aff>Twitch</font></a>")
        label5_text.setOpenExternalLinks(True)
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1_image, 0, 0, 1, 1)
        layout.addWidget(label1_text, 0, 1, 1, 1)
        layout.addWidget(label2_image, 1, 0, 1, 1)
        layout.addWidget(label2_text, 1, 1, 1, 1)
        layout.addWidget(label3_image, 2, 0, 1, 1)
        layout.addWidget(label3_text, 2, 1, 1, 1)
        layout.addWidget(label4_image, 3, 0, 1, 1)
        layout.addWidget(label4_text, 3, 1, 1, 1)
        layout.addWidget(label5_image, 4, 0, 1, 1)
        layout.addWidget(label5_text, 4, 1, 1, 1)
        box = QDialog(self)
        box.setLayout(layout)
        box.setWindowTitle("Credits")
        box.exec()
    
    def install_3(self):
        label = QLabel()
        label.setText("<span style=\"font-weight: bold; color: #e06666;\">.NET Runtime 3.0 Preview 8</span> is currently not installed, it is required for datatable conversion:<br/><a href=\"https://dotnet.microsoft.com/download/thank-you/dotnet-runtime-3.0.0-preview8-windows-x64-installer\"><font face=Cambria color=#f6b26b>64bit Installer</font></a><br/><a href=\"https://dotnet.microsoft.com/download/thank-you/dotnet-runtime-3.0.0-preview8-windows-x86-installer\"><font face=Cambria color=#f6b26b>32bit Installer</font></a>")
        label.setOpenExternalLinks(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        box = QDialog(self)
        box.setLayout(layout)
        box.setWindowTitle("Install")
        box.exec()
    
    def install_5(self):
        label = QLabel()
        label.setText("<span style=\"font-weight: bold; color: #e06666;\">.NET Runtime 5.0</span> is currently not installed, it is required for umap offsetting:<br/><a href=\"https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-5.0.10-windows-x64-installer\"><font face=Cambria color=#f6b26b>64bit Installer</font></a><br/><a href=\"https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-5.0.10-windows-x86-installer\"><font face=Cambria color=#f6b26b>32bit Installer</font></a>")
        label.setOpenExternalLinks(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        box = QDialog(self)
        box.setLayout(layout)
        box.setWindowTitle("Install")
        box.exec()
    
    def no_path(self):
        box = QMessageBox(self)
        box.setWindowTitle("Path")
        box.setIcon(QMessageBox.Critical)
        box.setText("Output path does not exist.")
        box.exec()
    
    def error(self):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText("MapEditor.exe is running, cannot overwrite.")
        box.exec()
    
    def check_for_updates(self):
        if os.path.isfile("OldRandomizer.exe"):
            os.remove("OldRandomizer.exe")
        try:
            api = requests.get("https://api.github.com/repos/Lakifume/True-Randomization/releases/latest").json()
        except requests.ConnectionError:
            self.setEnabled(True)
            return
        for i in config:
            if i["Key"] == "Version":
                tag = i["Value"]["Tag"]
        try:
            latest_tag = api["tag_name"]
        except KeyError:
            self.setEnabled(True)
            return
        if latest_tag != tag:
            choice = QMessageBox.question(self, "Auto Updater", "New version found:\n\n" + api["body"] + "\n\nUpdate ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                if "MapEditor.exe" in (i.name() for i in psutil.process_iter()):
                    self.error()
                    self.setEnabled(True)
                    return
                
                self.progressBar = QProgressDialog("Downloading...", None, 0, api["assets"][0]["size"], self)
                self.progressBar.setWindowTitle("Status")
                self.progressBar.setWindowModality(Qt.WindowModal)
                self.progressBar.setAutoClose(False)
                self.progressBar.setAutoReset(False)
                
                self.worker = Update(self.progressBar, api)
                self.worker.updateProgress.connect(self.setProgress)
                self.worker.start()
            else:
                self.setEnabled(True)
        else:
            self.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(writing_and_exit)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()