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
    bullet_content[559]["Value"]["BeginEffectBeginScale"] /= 2.0
    bullet_content[559]["Value"]["BeginEffectEndScale"] /= 2.0
    
    collision_content[537]["Value"]["R00"] /= 2.0
    collision_content[537]["Value"]["R01"] /= 2.0
    
    debug("normal_bomber()")

def normal_bael():
    #LightRay
    ballistic_content[73]["Value"]["InitialSpeed"] /= 2.0
    #TracerRay
    ballistic_content[317]["Value"]["InitialSpeed"] /= 6.0
    #RingLasers
    ballistic_content[320]["Value"]["InitialSpeed"] /= 9.0
    
    #FlameSkull
    bullet_content[783]["Value"]["EffectBeginScale"] /= 2.5
    bullet_content[783]["Value"]["EffectEndScale"] /= 2.5
    bullet_content[783]["Value"]["BeginEffectBeginScale"] /= 2.5
    bullet_content[783]["Value"]["BeginEffectEndScale"] /= 2.5
    bullet_content[783]["Value"]["EndEffectBeginScale"] /= 2.5
    bullet_content[783]["Value"]["EndEffectEndScale"] /= 2.5
    
    #Bubbles
    bullet_content[787]["Value"]["EffectBeginScale"] /= 1.5
    bullet_content[787]["Value"]["EffectEndScale"] /= 1.5
    bullet_content[787]["Value"]["BeginEffectBeginScale"] /= 1.5
    bullet_content[787]["Value"]["BeginEffectEndScale"] /= 1.5
    bullet_content[787]["Value"]["EndEffectBeginScale"] /= 1.5
    bullet_content[787]["Value"]["EndEffectEndScale"] /= 1.5
    
    #RingLasers
    bullet_content[789]["Value"]["EffectBeginScale"] /= 2.0
    bullet_content[789]["Value"]["EffectEndScale"] /= 2.0
    bullet_content[789]["Value"]["BeginEffectBeginScale"] /= 2.0
    bullet_content[789]["Value"]["BeginEffectEndScale"] /= 2.0
    bullet_content[789]["Value"]["EndEffectBeginScale"] /= 2.0
    bullet_content[789]["Value"]["EndEffectEndScale"] /= 2.0
    
    #Screech
    bullet_content[790]["Value"]["EffectBeginScale"] /= 2.0
    bullet_content[790]["Value"]["EffectEndScale"] /= 2.0
    bullet_content[790]["Value"]["EndEffectBeginScale"] /= 2.0
    bullet_content[790]["Value"]["EndEffectEndScale"] /= 2.0
    
    #FlameSkullExplosion
    bullet_content[792]["Value"]["EffectBeginScale"] /= 2.5
    bullet_content[792]["Value"]["EffectEndScale"] /= 2.5
    bullet_content[792]["Value"]["BeginEffectBeginScale"] /= 2.5
    bullet_content[792]["Value"]["BeginEffectEndScale"] /= 2.5
    bullet_content[792]["Value"]["EndEffectBeginScale"] /= 2.5
    bullet_content[792]["Value"]["EndEffectEndScale"] /= 2.5
    
    #FlameSkullDestroyed
    bullet_content[793]["Value"]["EffectBeginScale"] /= 2.5
    bullet_content[793]["Value"]["EffectEndScale"] /= 2.5
    bullet_content[793]["Value"]["BeginEffectBeginScale"] /= 2.5
    bullet_content[793]["Value"]["BeginEffectEndScale"] /= 2.5
    bullet_content[793]["Value"]["EndEffectBeginScale"] /= 2.5
    bullet_content[793]["Value"]["EndEffectEndScale"] /= 2.5
    
    #BubblesDestroyed
    bullet_content[794]["Value"]["EffectBeginScale"] /= 1.5
    bullet_content[794]["Value"]["EffectEndScale"] /= 1.5
    bullet_content[794]["Value"]["BeginEffectBeginScale"] /= 1.5
    bullet_content[794]["Value"]["BeginEffectEndScale"] /= 1.5
    bullet_content[794]["Value"]["EndEffectBeginScale"] /= 1.5
    bullet_content[794]["Value"]["EndEffectEndScale"] /= 1.5
    
    #RingLasersImpact
    bullet_content[797]["Value"]["EffectBeginScale"] /= 2.0
    bullet_content[797]["Value"]["EffectEndScale"] /= 2.0
    bullet_content[797]["Value"]["BeginEffectBeginScale"] /= 2.0
    bullet_content[797]["Value"]["BeginEffectEndScale"] /= 2.0
    bullet_content[797]["Value"]["EndEffectBeginScale"] /= 2.0
    bullet_content[797]["Value"]["EndEffectEndScale"] /= 2.0
    
    #FlameSkull
    collision_content[738]["Value"]["R00"] /= 2.5
    collision_content[738]["Value"]["R01"] /= 2.5
    
    #FlameSkullExplosion
    collision_content[739]["Value"]["R00"] /= 2.5
    collision_content[739]["Value"]["R01"] /= 2.5
    
    #Bubbles
    collision_content[743]["Value"]["R00"] /= 1.5
    collision_content[743]["Value"]["R01"] /= 1.5
    
    #RingLasers
    collision_content[745]["Value"]["R00"] /= 2.0
    collision_content[745]["Value"]["R01"] /= 2.0
    
    #Screech
    collision_content[746]["Value"]["R00"] /= 2.0
    collision_content[746]["Value"]["R01"] /= 2.0
    
    debug("normal_bael()")

def write_patched_ballistic():
    with open("Serializer\\PB_DT_BallisticMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(ballistic_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BallisticMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BallisticMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BallisticMaster.uasset")
    os.remove("Serializer\\PB_DT_BallisticMaster.json")
    debug("write_patched_ballistic()")

def write_ballistic():
    shutil.copyfile("Serializer\\PB_DT_BallisticMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BallisticMaster.uasset")
    debug("write_ballistic()")

def write_patched_bullet():
    with open("Serializer\\PB_DT_BulletMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(bullet_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BulletMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BulletMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BulletMaster.uasset")
    os.remove("Serializer\\PB_DT_BulletMaster.json")
    debug("write_patched_bullet()")
    
def write_bullet():
    shutil.copyfile("Serializer\\PB_DT_BulletMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BulletMaster.uasset")
    debug("write_bullet()")

def write_patched_collision():
    with open("Serializer\\PB_DT_CollisionMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(collision_content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CollisionMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_CollisionMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CollisionMaster.uasset")
    os.remove("Serializer\\PB_DT_CollisionMaster.json")
    debug("write_patched_collision()")

def write_collision():
    shutil.copyfile("Serializer\\PB_DT_CollisionMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_CollisionMaster.uasset")
    debug("write_collision()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()