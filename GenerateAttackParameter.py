import json
import os
import shutil

#Content
with open("Data\\BallisticMaster\\Content\\PB_DT_BallisticMaster.json", "r") as file_reader:
    ballistic_content = json.load(file_reader)

with open("Data\\BulletMaster\\Content\\PB_DT_BulletMaster.json", "r") as file_reader:
    bullet_content = json.load(file_reader)

with open("Data\\CollisionMaster\\Content\\PB_DT_CollisionMaster.json", "r") as file_reader:
    collision_content = json.load(file_reader)

def normal_bomber():
    bullet_content[559]["Value"]["BeginEffectBeginScale"] = 2.0
    bullet_content[559]["Value"]["BeginEffectEndScale"] = 2.0
    
    collision_content[537]["Value"]["R00"] = 4.0
    collision_content[537]["Value"]["R01"] = 4.0

def normal_bael():
    ballistic_content[73]["Value"]["InitialSpeed"] = 12.0
    ballistic_content[317]["Value"]["InitialSpeed"] = 5.0
    ballistic_content[320]["Value"]["InitialSpeed"] = 5.0
    
    bullet_content[783]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[783]["Value"]["EffectEndScale"] = 1.0
    bullet_content[783]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[783]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[783]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[783]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[787]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[787]["Value"]["EffectEndScale"] = 1.0
    bullet_content[787]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[787]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[787]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[787]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[789]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[789]["Value"]["EffectEndScale"] = 1.0
    bullet_content[789]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[789]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[789]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[789]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[790]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[790]["Value"]["EffectEndScale"] = 1.0
    bullet_content[790]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[790]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[792]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[792]["Value"]["EffectEndScale"] = 1.0
    bullet_content[792]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[792]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[792]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[792]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[793]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[793]["Value"]["EffectEndScale"] = 1.0
    bullet_content[793]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[793]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[793]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[793]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[794]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[794]["Value"]["EffectEndScale"] = 1.0
    bullet_content[794]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[794]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[794]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[794]["Value"]["EndEffectEndScale"] = 1.0
    
    bullet_content[797]["Value"]["EffectBeginScale"] = 1.0
    bullet_content[797]["Value"]["EffectEndScale"] = 1.0
    bullet_content[797]["Value"]["BeginEffectBeginScale"] = 1.0
    bullet_content[797]["Value"]["BeginEffectEndScale"] = 1.0
    bullet_content[797]["Value"]["EndEffectBeginScale"] = 1.0
    bullet_content[797]["Value"]["EndEffectEndScale"] = 1.0
    
    collision_content[738]["Value"]["R00"] = 0.3
    collision_content[738]["Value"]["R01"] = 0.3
    
    collision_content[739]["Value"]["R00"] = 1.0
    collision_content[739]["Value"]["R01"] = 1.0
    
    collision_content[743]["Value"]["R00"] = 0.45
    collision_content[743]["Value"]["R01"] = 0.45
    
    collision_content[745]["Value"]["R00"] = 0.4
    collision_content[745]["Value"]["R01"] = 0.9
    
    collision_content[746]["Value"]["R00"] = 2.0
    collision_content[746]["Value"]["R01"] = 6.0

def write_patched_ballistic():
    with open("Serializer\\PB_DT_BallisticMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(ballistic_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BallisticMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BallisticMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BallisticMaster.uasset")
    os.remove("Serializer\\PB_DT_BallisticMaster.json")

def write_ballistic():
    shutil.copyfile("Serializer\\PB_DT_BallisticMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BallisticMaster.uasset")

def write_patched_bullet():
    with open("Serializer\\PB_DT_BulletMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(bullet_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BulletMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BulletMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BulletMaster.uasset")
    os.remove("Serializer\\PB_DT_BulletMaster.json")
    
def write_bullet():
    shutil.copyfile("Serializer\\PB_DT_BulletMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BulletMaster.uasset")

def write_patched_collision():
    with open("Serializer\\PB_DT_CollisionMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(collision_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CollisionMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CollisionMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CollisionMaster.uasset")
    os.remove("Serializer\\PB_DT_CollisionMaster.json")

def write_collision():
    shutil.copyfile("Serializer\\PB_DT_CollisionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CollisionMaster.uasset")