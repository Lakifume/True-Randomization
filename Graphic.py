from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Room
import Sound
import Bloodless
import Utility

def init():
    global portrait_replacement
    portrait_replacement = {}
    global shard_type_to_hsv
    shard_type_to_hsv = {
        "Skill":       (  0,   0, 100),
        "Trigger":     (  0, 100, 100),
        "Effective":   (230, 100,  80),
        "Directional": (270, 100, 100),
        "Enchant":     ( 60, 100, 100),
        "Familia":     (120, 100,  80)
    }
    global material_to_offset
    material_to_offset = {
        "MI_N1001_Body": [
            0x18BD,
            0x18EA,
            0x1924,
            0x1984,
            0xA1D0,
            0xA1FD,
            0xA237,
            0xA297
        ],
        "MI_N1001_Crystal": [
            0x1CC9,
            0x1CF6,
            0x1D30,
            0x1D90,
            0x1DF6,
            0x1E23,
            0x1E5D,
            0x1EBD,
            0x1A0CE,
            0x1A0FB,
            0x1A135,
            0x1A195,
            0x1A1FB,
            0x1A228,
            0x1A262,
            0x1A2C2
        ],
        "MI_N1001_Eye1": [
            0x1042,
            0x106F,
            0x10A9,
            0x1109,
            0x86B3,
            0x86E0,
            0x871A,
            0x877A
        ],
        "MI_N1001_Eye2": [
            0x1042,
            0x106F,
            0x10A9,
            0x1109,
            0x86B3,
            0x86E0,
            0x871A,
            0x877A
        ],
        "MI_N1001_Face": [
            0x17F9,
            0x1826,
            0x1860,
            0x18C0,
            0x9CC3,
            0x9CF0,
            0x9D2A,
            0x9D8A
        ],
        "MI_N1001_Hair": [
            0x17F9,
            0x1826,
            0x1860,
            0x18C0,
            0x9CC4,
            0x9CF1,
            0x9D2B,
            0x9D8B
        ],
        "MI_N1001_Mouth": [
            0x17F9,
            0x1826,
            0x1860,
            0x18C0,
            0x9CC4,
            0x9CF1,
            0x9D2B,
            0x9D8B
        ],
        "MI_N1001_tongue": [
            0x1ABD,
            0x1AEA,
            0x1B24,
            0x1B84,
            0x13A24,
            0x13A51,
            0x13A8B,
            0x13AEB
        ]
    }

def update_default_outfit_hsv(parameter_string):
    #Set the salon sliders to match the default outfit color
    parameter_list = []
    for index in range(len(parameter_string)//4):
        parameter_list.append(parameter_string[index*4:index*4 + 4])
    for index in range(6):
        for parameter in parameter_list:
            datatable["PB_DT_HairSalonOldDefaults"]["Body_01_" + "{:02d}".format(index + 1)][parameter[0] + "1"] = int(parameter[1:4])

def randomize_backer_portraits():
    #Shuffle backer portraits in a dict
    portraits = []
    for directory in os.listdir(Manager.asset_dir + "\\" + Manager.file_to_path["Ml_N3100_picture_001"]):
        file_name = os.path.splitext(directory)[0]
        portraits.append(file_name)
    portraits = list(dict.fromkeys(portraits))
    new_list = copy.deepcopy(portraits)
    random.shuffle(new_list)
    portrait_replacement = dict(zip(portraits, new_list))

def update_backer_portraits():
    #Update the portrait material pointer
    for portrait in portrait_replacement:
        update_portrait_pointer(portrait, portrait_replacement[portrait])

def update_portrait_pointer(portrait, portrait_replacement):
    #Simply swap the file's name in the name map and save as the new name
    portrait_replacement_data = UAsset(f"{Manager.asset_dir}\\{Manager.file_to_path[portrait_replacement]}\\{portrait_replacement}.uasset", EngineVersion.VER_UE4_22)
    index = portrait_replacement_data.SearchNameReference(FString(portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString(portrait))
    index = portrait_replacement_data.SearchNameReference(FString(f"/Game/Core/Character/N3100/Material/TextureMaterial/{portrait_replacement}"))
    portrait_replacement_data.SetNameReference(index, FString(f"/Game/Core/Character/N3100/Material/TextureMaterial/{portrait}"))
    portrait_replacement_data.Write(f"{Manager.mod_dir}\\{Manager.file_to_path[portrait]}\\{portrait}.uasset")

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for file in Manager.file_to_path:
        if Manager.file_to_type[file] == Manager.FileType.Material:
            enemy_id = Manager.file_to_path[file].split("\\")[-2]
            if Enemy.is_boss(enemy_id) or enemy_id == "N2008":
                shard_name = datatable["PB_DT_DropRateMaster"][f"{enemy_id}_Shard"]["ShardId"]
                shard_type = datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
                shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
                set_material_hsv(file, "ShardColor", shard_hsv)

def set_material_hsv(filename, parameter, new_hsv):
    #Change a vector color in a material file
    #Here we use hsv as a base as it is easier to work with
    if Manager.file_to_type[filename] != Manager.FileType.Material:
        raise TypeError("Input is not a material file")
    #Some color properties are not parsed by UAssetAPI and end up in extra data
    #Hex edit in that case
    if filename in material_to_offset:
        for offset in material_to_offset[filename]:
            #Check if given offset is valid
            string = ""
            for num in range(12):
                string += "{:02x}".format(game_data[filename].Exports[0].Extras[offset + num]).upper()
            if string != "0000000000000002FFFFFFFF":
                raise Exception("Material offset invalid")
            #Get rgb
            rgb = []
            for num in range(3):
                list = []
                for index in range(4):
                    list.insert(0, "{:02x}".format(game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index]).upper())
                string = ""
                for index in list:
                    string += index
                rgb.append(struct.unpack("!f", bytes.fromhex(string))[0])
            #Convert
            hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            new_hue = hsv[0] if new_hsv[0] < 0 else new_hsv[0]/360
            new_sat = hsv[1] if new_hsv[1] < 0 else new_hsv[1]/100
            new_val = hsv[2] if new_hsv[2] < 0 else new_hsv[2]/100
            rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
            #Write rgb
            for num in range(3):
                string = "{:08x}".format(struct.unpack("<I", struct.pack("<f", rgb[num]))[0]).upper()
                list = []
                for index in range(0, len(string), 2):
                    list.insert(0, string[index] + string[index + 1])
                for index in range(4):
                    game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index] = int(list[index], 16)
    #Otherwise change color through the exports
    else:
        for data in game_data[filename].Exports[0].Data:
            if str(data.Name) == "VectorParameterValues":
                for sub_data in data.Value:
                    if str(sub_data.Value[0].Value[0].Value) == parameter:
                        rgb = []
                        rgb.append(sub_data.Value[1].Value[0].Value.R)
                        rgb.append(sub_data.Value[1].Value[0].Value.G)
                        rgb.append(sub_data.Value[1].Value[0].Value.B)
                        alpha = sub_data.Value[1].Value[0].Value.A
                        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                        new_hue = hsv[0] if new_hsv[0] < 0 else new_hsv[0]/360
                        new_sat = hsv[1] if new_hsv[1] < 0 else new_hsv[1]/100
                        new_val = hsv[2] if new_hsv[2] < 0 else new_hsv[2]/100
                        rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
                        sub_data.Value[1].Value[0].Value = LinearColor(rgb[0], rgb[1], rgb[2], alpha)

def import_mesh(filename):
    #Import a mesh file at the right location by reading it in the file
    new_file = UAsset(f"Data\\Mesh\\{filename}.uasset", EngineVersion.VER_UE4_22)
    name_map = new_file.GetNameMapIndexList()
    filepath = None
    for name in name_map:
        if str(name)[0] == "/" and str(name).split("/")[-1] == filename:
            filepath = str(name)[6:][:-(len(filename)+1)].replace("/", "\\")
            break
    if not filepath:
        raise Exception(f"Failed to obtain filepath of asset {filename}")
    if not os.path.isdir(f"{Manager.mod_dir}\\{filepath}"):
        os.makedirs(f"{Manager.mod_dir}\\{filepath}")
    new_file.Write(f"{Manager.mod_dir}\\{filepath}\\{filename}.uasset")

def import_texture(filename):
    #Convert DDS to game assets dynamically instead of cooking them within Unreal Editor
    absolute_asset_dir   = os.path.abspath(f"{Manager.asset_dir}\\{Manager.file_to_path[filename]}")
    absolute_texture_dir = os.path.abspath("Data\\Texture")
    absolute_mod_dir     = os.path.abspath(f"{Manager.mod_dir}\\{Manager.file_to_path[filename]}")
    
    root = os.getcwd()
    os.chdir("Tools\\UE4 DDS Tools")
    os.system(f"cmd /c python\\python.exe src\\main.py \"{absolute_asset_dir}\\{filename}.uasset\" \"{absolute_texture_dir}\\{filename}.dds\" --save_folder=\"{absolute_mod_dir}\" --mode=inject --version=4.22")
    os.chdir(root)
    
    #UE4 DDS Tools does not interrupt the program if a texture fails to convert so do it from here
    if not os.path.isfile(f"{absolute_mod_dir}\\{filename}.uasset"):
        raise FileNotFoundError(f"{filename}.dds failed to inject")