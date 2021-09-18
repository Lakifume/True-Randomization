import json
import os
import shutil
import random

Miriam = []
Johannes = []
Ziber = []
Gremory = []
Dominique = []
Alfred = []
Zangetsu = []
OD = []
An = []
Hallie = []
Benjamin = []
Susie = []
Lindsay = []
Abigail = []
Todd = []
Coachman = []

#Content
with open("Data\\DialogueTableItems\\Content\\PB_DT_DialogueTableItems.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
for i in range(1151):
    if content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Miriam" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Miriam" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Miriam(3)" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Miriam(3)":
        Miriam.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Johannes" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Johannes":
        Johannes.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Ziber" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Ziber":
        Ziber.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Gremory" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Gremory":
        Gremory.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Dominique" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Dominique":
        Dominique.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Alfred" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Alfred":
        Alfred.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Zangetsu" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Zangetsu" or content[i]["Key"] == "Event_06_001":
        Zangetsu.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "OD" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "OD":
        OD.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "An" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "An":
        An.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Hallie" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Hallie":
        Hallie.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Benjamin" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Benjamin":
        Benjamin.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Susie" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Susie":
        Susie.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Lindsay" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Lindsay":
        Lindsay.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Abigail" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Abigail":
        Abigail.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Todd" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Todd":
        Todd.append(content[i]["Key"])
    elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Coachman" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Coachman":
        Coachman.append(content[i]["Key"])

def rand_dialogue():
    for i in range(1151):
        if content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Miriam" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Miriam" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Miriam(3)" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Miriam(3)":
            content[i]["Value"]["EventID"] = any_pick(Miriam)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Johannes" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Johannes":
            content[i]["Value"]["EventID"] = any_pick(Johannes)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Ziber" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Ziber":
            content[i]["Value"]["EventID"] = any_pick(Ziber)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Gremory" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Gremory":
            content[i]["Value"]["EventID"] = any_pick(Gremory)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Dominique" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Dominique":
            content[i]["Value"]["EventID"] = any_pick(Dominique)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Alfred" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Alfred":
            content[i]["Value"]["EventID"] = any_pick(Alfred)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Zangetsu" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Zangetsu" or content[i]["Key"] == "Event_06_001":
            content[i]["Value"]["EventID"] = any_pick(Zangetsu)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "OD" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "OD":
            content[i]["Value"]["EventID"] = any_pick(OD)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "An" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "An":
            content[i]["Value"]["EventID"] = any_pick(An)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Hallie" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Hallie":
            content[i]["Value"]["EventID"] = any_pick(Hallie)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Benjamin" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Benjamin":
            content[i]["Value"]["EventID"] = any_pick(Benjamin)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Susie" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Susie":
            content[i]["Value"]["EventID"] = any_pick(Susie)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Lindsay" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Lindsay":
            content[i]["Value"]["EventID"] = any_pick(Lindsay)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Abigail" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Abigail":
            content[i]["Value"]["EventID"] = any_pick(Abigail)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Todd" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Todd":
            content[i]["Value"]["EventID"] = any_pick(Todd)
        elif content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and content[i]["Value"]["SpeakerID_Left"] == "Coachman" or content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and content[i]["Value"]["SpeakerID_Right"] == "Coachman":
            content[i]["Value"]["EventID"] = any_pick(Coachman)

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item

def write_patched_dialogue():
    with open("Serializer\\PB_DT_DialogueTableItems.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_DialogueTableItems.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_DialogueTableItems.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_DialogueTableItems.uasset")
    os.remove("Serializer\\PB_DT_DialogueTableItems.json")