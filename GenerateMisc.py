import os
import shutil

def write_ammunition():
    shutil.copyfile("Serializer\\PB_DT_AmmunitionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_AmmunitionMaster.uasset")

def write_arts():
    shutil.copyfile("Serializer\\PB_DT_ArtsCommandMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArtsCommandMaster.uasset")

def write_brv():
    shutil.copyfile("Serializer\\PB_DT_BRVAttackDamage.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset")

def write_unique():
    shutil.copyfile("Serializer\\PB_DT_CharaUniqueParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CharaUniqueParameterMaster.uasset")

def write_craft():
    shutil.copyfile("Serializer\\PB_DT_CraftMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset")

def write_damage():
    shutil.copyfile("Serializer\\PB_DT_DamageMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DamageMaster.uasset")

def write_enchant():
    shutil.copyfile("Serializer\\PB_DT_EnchantParameterType.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_EnchantParameterType.uasset")

def write_icon():
    shutil.copyfile("Serializer\\icon.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\UI_Pause\\Menu\\MainMenu\\Asset\\icon.uasset")

def write_8bit():
    shutil.copyfile("Serializer\\m51_EBT_BG.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG.uasset")
    shutil.copyfile("Serializer\\m51_EBT_BG_01.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG_01.uasset")
    shutil.copyfile("Serializer\\m51_EBT_Block.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block.uasset")
    shutil.copyfile("Serializer\\m51_EBT_Block_00.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_00.uasset")
    shutil.copyfile("Serializer\\m51_EBT_Block_01.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_01.uasset")
    shutil.copyfile("Serializer\\m51_EBT_Door.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Door.uasset")

def write_brm():
    shutil.copyfile("Serializer\\ACT50_BRM.awb", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Sound\\bgm\\ACT50_BRM.awb")

def write_options():
    shutil.copyfile("Serializer\\RandomizerOptions.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\Title\\RandomizerMode\\RandomizerOptions.uasset")