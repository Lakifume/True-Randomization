import Manager
import random
import copy

def init():
    global event_skip
    event_skip = [
        "Event_09_001_2",
        "Event_09_002_2",
        "Event_09_003_2",
        "Event_10_001_2",
        "Event_10_002_2",
        "Event_10_003_2",
        "Event_10_004_2",
        "Event_10_005_2",
        "Event_10_006_2",
        "Event_10_007_2"
    ]
    global background_events
    background_events = [
        "Train_AlchemyRoom_Enter_01",
        "Train_AlchemyRoom_Enter_02",
        "Train_ConfirmAlchemy_01",
        "Train_ConfirmAlchemy_02",
        "Train_QuitAlchemy_01",
        "Train_QuitAlchemy_02",
        "Train_AlchemyBegins_01",
        "Train_AlchemyBegins_02",
        "Train_AlchemyFinishes_01",
        "Train_AlchemyFinishes_02",
        "Train_AlchemyFinishes_03",
        "Train_AlchemyFinishes_04",
        "Train_AlchemyFinishes_05",
        "Train_AlchemyFinishes_06",
        "Train_AlchemyContinue_01",
        "Train_AlchemyContinue_02",
        "Church_An_etc_01",
        "Church_An_etc_02",
        "Church_An_etc_03",
        "Church_An_etc_04",
        "Church_An_etc_05",
        "Church_An_etc_06",
        "Church_An_etc_07",
        "Church_An_etc_09",
        "Church_An_etc_10",
        "Church_An_etc_11",
        "Church_Dominique_etc_01",
        "Church_Dominique_etc_02",
        "Church_Dominique_etc_03",
        "Church_Dominique_etc_04",
        "Church_Dominique_etc_05",
        "Church_Dominique_etc_06",
        "Church_Dominique_etc_07",
        "Church_Dominique_etc_08",
        "Church_Dominique_etc_09",
        "Church_Dominique_etc_10",
        "Qu05_N5006_010",
        "Qu06_N5008_008"
    ]
    global character_to_event
    character_to_event = {}
    global event_to_face_anim
    event_to_face_anim = {}
    global all_replacement
    all_replacement = {}

def set_voice_language(language):
    global voice_language
    voice_language = ["jp", "en"][language - 1]

def randomize_dialogues():
    for entry in Manager.datatable["PB_DT_DialogueTableItems"]:
        if entry in event_skip:
            continue
        direction = Manager.datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1]
        #Zangetsu has an event that doesn't have his name
        if entry == "Event_06_001":
            character_to_event["Zangetsu"] = []
        else:
            character_to_event[Manager.remove_inst_number(Manager.datatable["PB_DT_DialogueTableItems"][entry]["SpeakerID_" + direction])] = []
        #Anything past this is dummy events
        if entry == "Tutorial_Open_Door":
            break
    for entry in Manager.datatable["PB_DT_DialogueTableItems"]:
        if entry in event_skip:
            continue
        direction = Manager.datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1]
        if entry == "Event_06_001":
            character_to_event["Zangetsu"].append(entry)
        else:
            character_to_event[Manager.remove_inst_number(Manager.datatable["PB_DT_DialogueTableItems"][entry]["SpeakerID_" + direction])].append(entry)
        if entry == "Tutorial_Open_Door":
            break
    #Get every event's face anim, taking in consideration that null fields inherit previous anim 
    for direction in ["Left", "Right"]:
        #Start with standard consecutions
        for entry in Manager.datatable["PB_DT_DialogueTableItems"]:
            #Get anim of current event
            current_anim = Manager.datatable["PB_DT_DialogueTableItems"][entry]["FaceAnim_" + direction]
            next_event = Manager.datatable["PB_DT_DialogueTableItems"][entry]["Branches"]
            if current_anim == "None":
                continue
            if Manager.datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1] == direction:
                event_to_face_anim[entry] = current_anim
            if not next_event:
                continue
            if ";" in next_event:
                next_event = next_event.split(";")[0]
            #Get anim of following events
            while Manager.datatable["PB_DT_DialogueTableItems"][next_event]["FaceAnim_" + direction] == "None":
                if Manager.datatable["PB_DT_DialogueTableItems"][next_event]["SpeakingPosition"].split("::")[-1] == direction:
                    event_to_face_anim[next_event] = current_anim
                next_event = Manager.datatable["PB_DT_DialogueTableItems"][next_event]["Branches"]
                if not next_event:
                    break
                if ";" in next_event:
                    next_event = next_event.split(";")[0]
        #Loop again to get the few branching paths
        for entry in Manager.datatable["PB_DT_DialogueTableItems"]:
            #Get anim of current event
            current_anim = Manager.datatable["PB_DT_DialogueTableItems"][entry]["FaceAnim_" + direction]
            next_event = Manager.datatable["PB_DT_DialogueTableItems"][entry]["Branches"]
            if current_anim == "None":
                continue
            if not next_event:
                continue
            if not ";" in next_event:
                continue
            next_event = next_event.split(";")[1]
            #Get anim of following events
            while Manager.datatable["PB_DT_DialogueTableItems"][next_event]["FaceAnim_" + direction] == "None":
                if Manager.datatable["PB_DT_DialogueTableItems"][next_event]["SpeakingPosition"].split("::")[-1] == direction:
                    event_to_face_anim[next_event] = event_to_face_anim[entry]
                next_event = Manager.datatable["PB_DT_DialogueTableItems"][next_event]["Branches"]
                if not next_event:
                    break
    #Get the max text length amongst background events
    max_length = 0
    for event in background_events:
        if len(Manager.datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"]) > max_length:
            max_length = len(Manager.datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"])
    #Randomize in a dict by first giving background events short lines and then doing the rest
    for character in character_to_event:
        new_list = copy.deepcopy(character_to_event[character])
        for event in character_to_event[character]:
            if event in background_events:
                chosen = random.choice(new_list)
                try:
                    while len(Manager.datatable["PB_DT_DialogueTextMaster"][chosen]["DialogueText"]) > max_length:
                        chosen = random.choice(new_list)
                except KeyError:
                    pass
                new_list.remove(chosen)
                all_replacement[event] = chosen
        for event in character_to_event[character]:
            if not event in background_events:
                chosen = random.choice(new_list)
                new_list.remove(chosen)
                all_replacement[event] = chosen
    #Apply the changes
    for event in all_replacement:
        direction = Manager.datatable["PB_DT_DialogueTableItems"][event]["SpeakingPosition"].split("::")[-1]
        if all_replacement[event] in event_to_face_anim:
            Manager.datatable["PB_DT_DialogueTableItems"][event]["FaceAnim_" + direction] = event_to_face_anim[all_replacement[event]]
        else:
            Manager.datatable["PB_DT_DialogueTableItems"][event]["FaceAnim_" + direction] = "None"
        try:
            Manager.datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"]    = Manager.original_datatable["PB_DT_DialogueTextMaster"][all_replacement[event]]["DialogueText"]
            Manager.datatable["PB_DT_DialogueTextMaster"][event]["DialogueAudioID"] = Manager.original_datatable["PB_DT_DialogueTextMaster"][all_replacement[event]]["DialogueAudioID"]
            Manager.datatable["PB_DT_DialogueTextMaster"][event]["JPLipRef"]        = Manager.original_datatable["PB_DT_DialogueTextMaster"][all_replacement[event]]["JPLipRef"]
            Manager.datatable["PB_DT_DialogueTextMaster"][event]["ENLipRef"]        = Manager.original_datatable["PB_DT_DialogueTextMaster"][all_replacement[event]]["ENLipRef"]
        except KeyError:
            pass
        try:
            Manager.datatable["PB_DT_SoundMaster"][voice_language + "_" + event + "_SE"]["AssetPath"] = Manager.original_datatable["PB_DT_SoundMaster"][voice_language + "_" + all_replacement[event] + "_SE"]["AssetPath"]
        except KeyError:
            pass

def update_lip_movement():
    #While the dialogue datatable contains lip movement information it is completely ignored by the game
    #So the only solution left is to rename the pointer of every lip file to match the random dialogue
    #Quite a bit costly but this is the only way
    for event in all_replacement:
        Manager.update_lip_pointer(event, all_replacement[event], voice_language)