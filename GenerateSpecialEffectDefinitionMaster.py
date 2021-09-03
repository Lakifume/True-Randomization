import json
import os
import shutil

#Content
with open("Data\\SpecialEffectDefinitionMaster\\Content\\PB_DT_SpecialEffectDefinitionMaster.json", "r") as file_reader:
    content = json.load(file_reader)

def low_HPMP_growth():
    content[105]["Value"]["Parameter01"] -= 10.0
    content[106]["Value"]["Parameter01"] -= 5.0

def write_patched_effect():
    with open("Serializer\\PB_DT_SpecialEffectDefinitionMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_SpecialEffectDefinitionMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_SpecialEffectDefinitionMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset")
    os.remove("Serializer\\PB_DT_SpecialEffectDefinitionMaster.json")

def write_effect():
    shutil.copyfile("Serializer\\PB_DT_SpecialEffectDefinitionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset")

def reset_effect():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_SpecialEffectDefinitionMaster.uasset")