import os
import shutil

def write_ammunition():
    shutil.copyfile("Serializer\\PB_DT_AmmunitionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_AmmunitionMaster.uasset")
    debug("write_ammunition()")

def write_arts():
    shutil.copyfile("Serializer\\PB_DT_ArtsCommandMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArtsCommandMaster.uasset")
    debug("write_arts()")

def write_bloodless():
    shutil.copyfile("Serializer\\PB_DT_BloodlessAbilityData.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset")
    debug("write_bloodless()")

def write_brv_char():
    shutil.copyfile("Serializer\\PB_DT_BRVCharacterParameters.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVCharacterParameters.uasset")
    debug("write_brv_char()")

def write_unique():
    shutil.copyfile("Serializer\\PB_DT_CharaUniqueParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CharaUniqueParameterMaster.uasset")
    debug("write_unique()")

def write_damage():
    shutil.copyfile("Serializer\\PB_DT_DamageMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DamageMaster.uasset")
    debug("write_damage()")

def write_enchant():
    shutil.copyfile("Serializer\\PB_DT_EnchantParameterType.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_EnchantParameterType.uasset")
    debug("write_enchant()")

def write_frame():
    shutil.copyfile("Serializer\\Uasset\\frameMiriam.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\HUD\\HUD_asset\\StateGauge\\0000\\frameMiriam.uasset")
    debug("write_frame()")

def write_icon():
    shutil.copyfile("Serializer\\Uasset\\icon.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\UI_Pause\\Menu\\MainMenu\\Asset\\icon.uasset")
    debug("write_icon()")

def write_8bit():
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_BG.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG.uasset")
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_BG_01.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG_01.uasset")
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_Block.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block.uasset")
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_Block_00.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_00.uasset")
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_Block_01.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_01.uasset")
    shutil.copyfile("Serializer\\Uasset\\m51_EBT_Door.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Door.uasset")
    debug("write_8bit()")

def write_brm():
    shutil.copyfile("Serializer\\Awb\\ACT50_BRM.awb", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Sound\\bgm\\ACT50_BRM.awb")
    debug("write_brm()")

def write_ent():
    shutil.copyfile("UAssetGUI\\Umap\\m03ENT_000_Gimmick.umap", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT03_ENT\\Level\\m03ENT_000_Gimmick.umap")
    debug("write_ent()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()