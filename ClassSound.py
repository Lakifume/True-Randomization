import ClassManagement
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

skip = [
    "Qu01_N2012_027(3)"
]

def init():
    for i in range(1151):
        if ClassManagement.dialogue_content[i]["Key"] in skip:
            continue
        if ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Miriam" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Miriam" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Miriam(3)" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Miriam(3)":
            Miriam.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Johannes" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Johannes":
            Johannes.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Ziber" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Ziber":
            Ziber.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Gremory" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Gremory":
            Gremory.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Dominique" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Dominique":
            Dominique.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Alfred" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Alfred":
            Alfred.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Zangetsu" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Zangetsu" or ClassManagement.dialogue_content[i]["Key"] == "Event_06_001":
            Zangetsu.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "OD" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "OD":
            OD.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "An" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "An":
            An.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Hallie" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Hallie":
            Hallie.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Benjamin" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Benjamin":
            Benjamin.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Susie" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Susie":
            Susie.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Lindsay" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Lindsay":
            Lindsay.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Abigail" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Abigail":
            Abigail.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Todd" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Todd":
            Todd.append(ClassManagement.dialogue_content[i]["Key"])
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Coachman" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Coachman":
            Coachman.append(ClassManagement.dialogue_content[i]["Key"])
    ClassManagement.debug("ClassSound.init()")

def rand_dialogue():
    for i in range(1151):
        if ClassManagement.dialogue_content[i]["Key"] in skip:
            continue
        if ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Miriam" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Miriam" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Miriam(3)" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Miriam(3)":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Miriam)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Johannes" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Johannes":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Johannes)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Ziber" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Ziber":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Ziber)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Gremory" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Gremory":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Gremory)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Dominique" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Dominique":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Dominique)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Alfred" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Alfred":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Alfred)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Zangetsu" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Zangetsu" or ClassManagement.dialogue_content[i]["Key"] == "Event_06_001":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Zangetsu)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "OD" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "OD":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(OD)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "An" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "An":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(An)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Hallie" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Hallie":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Hallie)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Benjamin" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Benjamin":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Benjamin)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Susie" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Susie":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Susie)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Lindsay" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Lindsay":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Lindsay)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Abigail" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Abigail":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Abigail)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Todd" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Todd":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Todd)
        elif ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Left" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Left"] == "Coachman" or ClassManagement.dialogue_content[i]["Value"]["SpeakingPosition"] == "ESpeakingPosition::Right" and ClassManagement.dialogue_content[i]["Value"]["SpeakerID_Right"] == "Coachman":
            ClassManagement.dialogue_content[i]["Value"]["EventID"] = any_pick(Coachman)
    ClassManagement.debug("ClassSound.rand_dialogue()")

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item