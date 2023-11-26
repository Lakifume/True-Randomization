from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Room
import Graphic
import Bloodless
import Utility

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
    global music_list
    music_list = [
        "BGM_m01SIP",
        "BGM_m03ENT",
        "BGM_m04GDN",
        "BGM_m05SAN",
        "BGM_m08TWR",
        "BGM_m07LIB",
        "BGM_m09TRN",
        "BGM_m13ARC",
        "BGM_m06KNG",
        "BGM_m11UGD",
        "BGM_m12SND",
        "BGM_m17RVA",
        "BGM_m15JPN",
        "BGM_m10BIG",
        "BGM_m18ICE",
        "BGM_m19K2C",
        "BGM_m20JRN"
    ]
    global event_replacement
    event_replacement = {}
    global music_replacement
    music_replacement = {}

def set_voice_language(language):
    global voice_language
    voice_language = ["jp", "en"][language - 1]

def randomize_dialogues():
    for entry in datatable["PB_DT_DialogueTableItems"]:
        if entry in event_skip:
            continue
        direction = datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1]
        #Zangetsu has an event that doesn't have his name
        if entry == "Event_06_001":
            character_to_event["Zangetsu"] = []
        else:
            character_to_event[Utility.remove_inst_number(datatable["PB_DT_DialogueTableItems"][entry]["SpeakerID_" + direction])] = []
        #Anything past this is dummy events
        if entry == "Tutorial_Open_Door":
            break
    for entry in datatable["PB_DT_DialogueTableItems"]:
        if entry in event_skip:
            continue
        direction = datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1]
        if entry == "Event_06_001":
            character_to_event["Zangetsu"].append(entry)
        else:
            character_to_event[Utility.remove_inst_number(datatable["PB_DT_DialogueTableItems"][entry]["SpeakerID_" + direction])].append(entry)
        if entry == "Tutorial_Open_Door":
            break
    #Get every event's face anim, taking in consideration that null fields inherit previous anim 
    for direction in ["Left", "Right"]:
        #Start with standard consecutions
        for entry in datatable["PB_DT_DialogueTableItems"]:
            #Get anim of current event
            current_anim = datatable["PB_DT_DialogueTableItems"][entry]["FaceAnim_" + direction]
            next_event = datatable["PB_DT_DialogueTableItems"][entry]["Branches"]
            if current_anim == "None":
                continue
            if datatable["PB_DT_DialogueTableItems"][entry]["SpeakingPosition"].split("::")[-1] == direction:
                event_to_face_anim[entry] = current_anim
            if not next_event:
                continue
            if ";" in next_event:
                next_event = next_event.split(";")[0]
            #Get anim of following events
            while datatable["PB_DT_DialogueTableItems"][next_event]["FaceAnim_" + direction] == "None":
                if datatable["PB_DT_DialogueTableItems"][next_event]["SpeakingPosition"].split("::")[-1] == direction:
                    event_to_face_anim[next_event] = current_anim
                next_event = datatable["PB_DT_DialogueTableItems"][next_event]["Branches"]
                if not next_event:
                    break
                if ";" in next_event:
                    next_event = next_event.split(";")[0]
        #Loop again to get the few branching paths
        for entry in datatable["PB_DT_DialogueTableItems"]:
            #Get anim of current event
            current_anim = datatable["PB_DT_DialogueTableItems"][entry]["FaceAnim_" + direction]
            next_event = datatable["PB_DT_DialogueTableItems"][entry]["Branches"]
            if current_anim == "None":
                continue
            if not next_event:
                continue
            if not ";" in next_event:
                continue
            next_event = next_event.split(";")[1]
            #Get anim of following events
            while datatable["PB_DT_DialogueTableItems"][next_event]["FaceAnim_" + direction] == "None":
                if datatable["PB_DT_DialogueTableItems"][next_event]["SpeakingPosition"].split("::")[-1] == direction:
                    event_to_face_anim[next_event] = event_to_face_anim[entry]
                next_event = datatable["PB_DT_DialogueTableItems"][next_event]["Branches"]
                if not next_event:
                    break
    #Get the max text length amongst background events
    max_length = 0
    for event in background_events:
        if len(datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"]) > max_length:
            max_length = len(datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"])
    #Randomize in a dict by first giving background events short lines and then doing the rest
    for character in character_to_event:
        new_list = copy.deepcopy(character_to_event[character])
        for event in character_to_event[character]:
            if event in background_events:
                chosen = random.choice(new_list)
                try:
                    while len(datatable["PB_DT_DialogueTextMaster"][chosen]["DialogueText"]) > max_length:
                        chosen = random.choice(new_list)
                except KeyError:
                    pass
                new_list.remove(chosen)
                event_replacement[event] = chosen
        for event in character_to_event[character]:
            if not event in background_events:
                chosen = random.choice(new_list)
                new_list.remove(chosen)
                event_replacement[event] = chosen
    #Apply the changes
    for event in event_replacement:
        direction = datatable["PB_DT_DialogueTableItems"][event]["SpeakingPosition"].split("::")[-1]
        if event_replacement[event] in event_to_face_anim:
            datatable["PB_DT_DialogueTableItems"][event]["FaceAnim_" + direction] = event_to_face_anim[event_replacement[event]]
        else:
            datatable["PB_DT_DialogueTableItems"][event]["FaceAnim_" + direction] = "None"
        try:
            datatable["PB_DT_DialogueTextMaster"][event]["DialogueText"]    = Manager.original_datatable["PB_DT_DialogueTextMaster"][event_replacement[event]]["DialogueText"]
            datatable["PB_DT_DialogueTextMaster"][event]["DialogueAudioID"] = Manager.original_datatable["PB_DT_DialogueTextMaster"][event_replacement[event]]["DialogueAudioID"]
            datatable["PB_DT_DialogueTextMaster"][event]["JPLipRef"]        = Manager.original_datatable["PB_DT_DialogueTextMaster"][event_replacement[event]]["JPLipRef"]
            datatable["PB_DT_DialogueTextMaster"][event]["ENLipRef"]        = Manager.original_datatable["PB_DT_DialogueTextMaster"][event_replacement[event]]["ENLipRef"]
        except KeyError:
            pass
        try:
            datatable["PB_DT_SoundMaster"][voice_language + "_" + event + "_SE"]["AssetPath"] = Manager.original_datatable["PB_DT_SoundMaster"][voice_language + "_" + event_replacement[event] + "_SE"]["AssetPath"]
        except KeyError:
            pass

def randomize_music():
    new_list = copy.deepcopy(music_list)
    random.shuffle(new_list)
    new_dict = dict(zip(music_list, new_list))
    music_replacement.update(new_dict)
    for room in datatable["PB_DT_RoomMaster"]:
        if datatable["PB_DT_RoomMaster"][room]["BgmID"] in music_replacement:
            datatable["PB_DT_RoomMaster"][room]["BgmID"] = music_replacement[datatable["PB_DT_RoomMaster"][room]["BgmID"]]

def update_lip_movement():
    #While the dialogue datatable contains lip movement information it is completely ignored by the game
    #So the only solution left is to rename the pointer of every lip file to match the random dialogue
    #Quite a bit costly but this is the only way
    for event in event_replacement:
        update_lip_pointer(event, event_replacement[event], voice_language)

def update_lip_pointer(old_event, new_event, prefix):
    #Simply swap the file's name in the name map and save as the new name
    old_event = prefix + "_" + old_event + "_LIP"
    new_event = prefix + "_" + new_event + "_LIP"
    
    if new_event + ".uasset" in os.listdir("Data\\LipSync"):
        new_event_data = UAsset("Data\\LipSync\\" + new_event + ".uasset", UE4Version.VER_UE4_22)
        index = new_event_data.SearchNameReference(FString(new_event))
        new_event_data.SetNameReference(index, FString(old_event))
        index = new_event_data.SearchNameReference(FString("/Game/Core/UI/Dialog/Data/LipSync/" + new_event))
        new_event_data.SetNameReference(index, FString("/Game/Core/UI/Dialog/Data/LipSync/" + old_event))
        new_event_data.Write(Manager.mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + old_event + ".uasset")
    elif old_event + ".uasset" in os.listdir("Data\\LipSync"):
        old_event_data = UAsset("Data\\LipSync\\" + old_event + ".uasset", UE4Version.VER_UE4_22)
        for export in old_event_data.Exports:
            if str(export.ObjectName) == old_event:
                export.Data.Clear()
        old_event_data.Write(Manager.mod_dir + "\\Core\\UI\\Dialog\\Data\\LipSync\\" + old_event + ".uasset")

def add_music_file(filename):
    #Check if the filename is valid
    if len(filename.split("_")) != 2:
        raise TypeError("Invalid music name: " + filename)
    if len(filename.split("_")[0]) != 5 or len(filename.split("_")[-1]) != 3:
        raise TypeError("Invalid music name: " + filename)
    if filename[0:3] != "ACT":
        raise TypeError("Invalid music name: " + filename)
    try:
        int(filename[3:5])
    except ValueError:
        raise TypeError("Invalid music name: " + filename)
    #Copy the awb and import the new music in it
    filesize = None
    with open(Manager.asset_dir + "\\" + Manager.file_to_path["ACT50_BRM"] + "\\ACT50_BRM.awb", "rb") as inputfile, open(Manager.mod_dir + "\\" + Manager.file_to_path["ACT50_BRM"] + "\\" + filename + ".awb", "wb") as outfile:
        offset = inputfile.read().find(str.encode("HCA"))
        inputfile.seek(0)
        outfile.write(inputfile.read(offset))
        with open("Data\\Music\\" + filename + ".hca", "rb") as hca:
            outfile.write(hca.read())
        outfile.seek(0, os.SEEK_END)
        filesize = outfile.tell()
        outfile.seek(0x16)
        outfile.write(filesize.to_bytes(4, "little"))
    #Add the music pointer in soundmaster
    music_id = "BGM_m" + filename[3:5] + filename.split("_")[-1]
    datatable["PB_DT_SoundMaster"][music_id] = copy.deepcopy(datatable["PB_DT_SoundMaster"]["BGM_m50BRM"])
    datatable["PB_DT_SoundMaster"][music_id]["AssetPath"] = datatable["PB_DT_SoundMaster"][music_id]["AssetPath"].replace("BGM_m50BRM", music_id)
    #Copy the act file
    new_file = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path["ACT50_BRM"] + "\\ACT50_BRM.uasset", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("ACT50_BRM"))
    new_file.SetNameReference(index, FString(filename))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/ACT50_BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + filename))
    new_file.Exports[0].Data[0].Value = FString(filename)
    string = "{:02x}".format(int.from_bytes(str.encode(filename), "big"))
    for num in range(int(len(string)/2)):
        new_file.Exports[0].Extras[0x662 + num] = int(string[num*2] + string[num*2 + 1], 16)
        new_file.Exports[0].Extras[0xE82 + num] = int(string[num*2] + string[num*2 + 1], 16)
    string = "{:02x}".format(int.from_bytes(str.encode(music_id), "big"))
    for num in range(int(len(string)/2)):
        new_file.Exports[0].Extras[0x7E1 + num] = int(string[num*2] + string[num*2 + 1], 16)
    string = "{:08x}".format(filesize)
    count = 0
    for num in range(int(len(string)/2) -1, -1, -1):
        new_file.Exports[0].Extras[0x1A32 + count] = int(string[num*2] + string[num*2 + 1], 16)
        count += 1
    new_file.Write(Manager.mod_dir + "\\" + Manager.file_to_path["ACT50_BRM"] + "\\" + filename + ".uasset")
    #Copy the bgm file
    new_file = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path["BGM_m50BRM"] + "\\BGM_m50BRM.uasset", UE4Version.VER_UE4_22)
    index = new_file.SearchNameReference(FString("ACT50_BRM"))
    new_file.SetNameReference(index, FString(filename))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/ACT50_BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + filename))
    index = new_file.SearchNameReference(FString("BGM_m50BRM"))
    new_file.SetNameReference(index, FString(music_id))
    index = new_file.SearchNameReference(FString("/Game/Core/Sound/bgm/BGM_m50BRM"))
    new_file.SetNameReference(index, FString("/Game/Core/Sound/bgm/" + music_id))
    new_file.Exports[0].Data[1].Value = FString(music_id)
    new_file.Exports[0].Data[2].Value = 300.0
    new_file.Write(Manager.mod_dir + "\\" + Manager.file_to_path["BGM_m50BRM"] + "\\" + music_id + ".uasset")