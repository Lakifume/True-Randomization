import json
import os
import shutil
import random

base = []
ten = []
hundred = []
thousand = []
log = []

#Content
with open("Data\\ItemMaster\\Content\\PB_DT_ItemMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

i = 10
while i <= 90:
    for e in range(10):
        base.append(i)
    i += 10

i = 100
while i <= 900:
    for e in range(10):
        base.append(i)
    i += 100

i = 1000
while i <= 9000:
    for e in range(10):
        base.append(i)
    i += 1000

i = 10000
while i <= 90000:
    for e in range(10):
        base.append(i)
    i += 10000

base.append(100000)

i = 0
while i <= 90:
    ten.append(i)
    i += 10

i = 0
while i <= 900:
    hundred.append(i)
    i += 100

i = 0
while i <= 9000:
    thousand.append(i)
    i += 1000

def hair_app_shop():
    i = 521
    while i <= 532:
        content[i]["Value"]["buyPrice"] = 100
        content[i]["Value"]["Producted"] = "Event_01_001_0000"
        i += 1

def no_dishes_and_bullet():
    i = 443
    while i <= 509:
        content[i]["Value"]["max"] = 1
        content[i]["Value"]["buyPrice"] = 0
        content[i]["Value"]["sellPrice"] = 0
        i += 1
    i = 608
    while i <= 620:
        content[i]["Value"]["buyPrice"] = 0
        content[i]["Value"]["sellPrice"] = 0
        i += 1

def no_card():
    content[561]["Value"]["buyPrice"] = 0
    content[561]["Value"]["sellPrice"] = 0

def rand_shop(scale):
    for i in range(702):
        if content[i]["Key"] == "Waystone" or content[i]["Key"] == "DiscountCard" or content[i]["Key"] == "MonarchCrown" or content[i]["Value"]["buyPrice"] == 0:
            continue
        chosen = random.choice(base)
        if chosen != 100000:
            if chosen >= 100:
                chosen += random.choice(ten)
            if chosen >= 1000:
                chosen += random.choice(hundred)
            if chosen >= 10000:
                chosen += random.choice(thousand)
        content[i]["Value"]["buyPrice"] = chosen
        if not scale:
            chosen = random.choice(base)
            if chosen != 100000:
                if chosen >= 100:
                    chosen += random.choice(ten)
                if chosen >= 1000:
                    chosen += random.choice(hundred)
                if chosen >= 10000:
                    chosen += random.choice(thousand)
        content[i]["Value"]["sellPrice"] = round(chosen/10)
        log_data = {}
        log_data["Key"] = translation["Value"][content[i]["Key"]]
        log_data["Value"] = {}
        log_data["Value"]["BuyPrice"] = content[i]["Value"]["buyPrice"]
        log_data["Value"]["SellPrice"] = content[i]["Value"]["sellPrice"]
        log.append(log_data)

def write_patched_item():
    with open("Serializer\\PB_DT_ItemMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, ensure_ascii=False, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_ItemMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_ItemMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")
    os.remove("Serializer\\PB_DT_ItemMaster.json")

def write_item():
    shutil.copyfile("Serializer\\PB_DT_ItemMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")

def reset_item():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Item\\PB_DT_ItemMaster.uasset")

def write_item_log():
    with open("SpoilerLog\\Shop.json", "w") as file_writer:
        file_writer.write(json.dumps(log, ensure_ascii=False, indent=2))

def reset_item_log():
    if os.path.isfile("SpoilerLog\\Shop.json"):
        os.remove("SpoilerLog\\Shop.json")