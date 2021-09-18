import os
import shutil
import random

#Data
miriam_hue = random.choice(os.listdir("Data\\Hue\\Miriam"))
zangetsu_hue = random.choice(os.listdir("Data\\Hue\\Zangetsu"))

def write_miriam():
    shutil.copyfile("Data\\Hue\\Miriam\\" + miriam_hue + "\\T_Body01_01_Color.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Character\\P0000\\Texture\\Body\\T_Body01_01_Color.uasset")
    shutil.copyfile("Data\\Hue\\Miriam\\" + miriam_hue + "\\T_Pl01_Cloth_Bace.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Character\\P0000\\Texture\\T_Pl01_Cloth_Bace.uasset")
    shutil.copyfile("Data\\Hue\\Miriam\\" + miriam_hue + "\\Face_Miriam.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\HUD\\HUD_asset\\StateGauge\\0000\\Face_Miriam.uasset")

def write_zangetsu():
    shutil.copyfile("Data\\Hue\\Zangetsu\\" + zangetsu_hue + "\\T_N1011_body_color.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Character\\N1011\\Texture\\T_N1011_body_color.uasset")
    shutil.copyfile("Data\\Hue\\Zangetsu\\" + zangetsu_hue + "\\T_N1011_face_color.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Character\\N1011\\Texture\\T_N1011_face_color.uasset")
    shutil.copyfile("Data\\Hue\\Zangetsu\\" + zangetsu_hue + "\\T_N1011_weapon_color.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Character\\N1011\\Texture\\T_N1011_weapon_color.uasset")
    shutil.copyfile("Data\\Hue\\Zangetsu\\" + zangetsu_hue + "\\T_Tknife05_Base.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\Item\\Weapon\\Tknife\\Tknife05\\Texture\\T_Tknife05_Base.uasset")
    shutil.copyfile("Data\\Hue\\Zangetsu\\" + zangetsu_hue + "\\Face_Zangetsu.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\UI\\HUD\\HUD_asset\\StateGauge\\0001\\Face_Zangetsu.uasset")