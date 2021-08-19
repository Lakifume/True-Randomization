import os
import shutil

def write_master():
    shutil.copyfile("Serializer\\PBMasterStringTable.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")

def write_ammunition():
    shutil.copyfile("Serializer\\PB_DT_AmmunitionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_AmmunitionMaster.uasset")

def write_armor():
    shutil.copyfile("Serializer\\PB_DT_ArmorMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")

def write_arts():
    shutil.copyfile("Serializer\\PB_DT_ArtsCommandMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArtsCommandMaster.uasset")

def write_bloodless():
    shutil.copyfile("Serializer\\PB_DT_BloodlessAbilityData.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset")

def write_brv():
    shutil.copyfile("Serializer\\PB_DT_BRVAttackDamage.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset")

def write_unique():
    shutil.copyfile("Serializer\\PB_DT_CharaUniqueParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CharaUniqueParameterMaster.uasset")

def write_craft():
    shutil.copyfile("Serializer\\PB_DT_CraftMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset")

def write_damage():
    shutil.copyfile("Serializer\\PB_DT_DamageMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DamageMaster.uasset")

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

def reset_master():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\L10N\\en\\Core\\StringTable\\PBMasterStringTable.uasset")

def reset_ammunition():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_AmmunitionMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_AmmunitionMaster.uasset")

def reset_armor():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArmorMaster.uasset")

def reset_arts():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArtsCommandMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_ArtsCommandMaster.uasset")

def reset_bloodless():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BloodlessAbilityData.uasset")

def reset_brv():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Character\\PB_DT_BRVAttackDamage.uasset")

def reset_unique():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CharaUniqueParameterMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CharaUniqueParameterMaster.uasset")

def reset_craft():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CraftMaster.uasset")

def reset_damage():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DamageMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DamageMaster.uasset")

def reset_icon():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\UI_Pause\\Menu\\MainMenu\\Asset\\icon.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\UI_Pause\\Menu\\MainMenu\\Asset\\icon.uasset")

def reset_8bit():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG.uasset")
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG_01.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_BG_01.uasset")
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block.uasset")
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_00.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_00.uasset")
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_01.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Block_01.uasset")
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Door.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Environment\\ACT51_EBT\\Texture\\m51_EBT_Door.uasset")

def reset_brm():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Sound\\bgm\\ACT50_BRM.awb"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Sound\\bgm\\ACT50_BRM.awb")