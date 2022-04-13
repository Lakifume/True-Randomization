import Manager
import random

def init():
    #Declare variables
    global character_to_line
    character_to_line = {}
    global skip
    skip = [
        "Qu01_N2012_027_2"
    ]
    #Process variables
    for i in Manager.datatable["PB_DT_DialogueTableItems"]:
        if i in skip:
            continue
        #Zangetsu has an event that doesn't have his name
        if i == "Event_06_001":
            character_to_line["Zangetsu"] = []
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Left":
            character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Left"].split("(")[0]] = []
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Right":
            character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Right"].split("(")[0]] = []
        #Anything past this is dummy events
        if i == "Tutorial_Open_Door":
            break
    for i in Manager.datatable["PB_DT_DialogueTableItems"]:
        if i in skip:
            continue
        #Zangetsu has an event that doesn't have his name
        if i == "Event_06_001":
            character_to_line["Zangetsu"].append(i)
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Left":
            character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Left"].split("(")[0]].append(i)
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Right":
            character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Right"].split("(")[0]].append(i)
        #Anything past this is dummy events
        if i == "Tutorial_Open_Door":
            break

def rand_dialogue():
    for i in Manager.datatable["PB_DT_DialogueTableItems"]:
        if i in skip:
            continue
        #Zangetsu has an event that doesn't have his name
        if i == "Event_06_001":
            Manager.datatable["PB_DT_DialogueTableItems"][i]["EventID"] = any_pick(character_to_line["Zangetsu"])
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Left":
            Manager.datatable["PB_DT_DialogueTableItems"][i]["EventID"] = any_pick(character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Left"].split("(")[0]])
        elif Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakingPosition"] == "ESpeakingPosition::Right":
            Manager.datatable["PB_DT_DialogueTableItems"][i]["EventID"] = any_pick(character_to_line[Manager.datatable["PB_DT_DialogueTableItems"][i]["SpeakerID_Right"].split("(")[0]])
        #Anything past this is dummy events
        if i == "Tutorial_Open_Door":
            break

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item