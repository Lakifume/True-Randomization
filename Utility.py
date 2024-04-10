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
import Sound
import Bloodless

def init():
    global weight_exponents
    weight_exponents = [3, 1.8, 1.25]

def simplify_item_name(name):
    return name.replace("Familiar:", "").replace(" ", "").replace("'", "").replace("-", "").replace(".", "").replace("é", "e").replace("è", "e").replace("&", "and").lower()

def remove_inst_number(name):
    #Return a string without its instance number the same way Unreal does it
    name = name.split("_")
    if name[-1][0] != "0":
        try:
            int(name[-1])
            name.pop()
        except ValueError:
            pass
    return "_".join(name)

def get_export_by_name(filename, export_name):
    for export in game_data[filename].Exports:
        if str(export.ObjectName) == export_name:
            return export
    raise Exception("Export not found")

def unreal_to_python_data(struct, unreal_type=None):
    unreal_type = unreal_type if unreal_type else str(struct.PropertyType)
    match unreal_type:
        case "ArrayProperty":
            array = []
            for array_item in struct.Value:
                array.append(unreal_to_python_data(array_item, str(struct.ArrayType)))
            return array
        case "ByteProperty":
            return str(struct.EnumValue)
        case "FloatProperty":
            return round(struct.Value, 3)
        case "EnumProperty":
            return str(struct.Value)
        case "NameProperty":
            return str(struct.Value)
        case "SoftObjectProperty":
            return str(struct.Value.AssetPath.AssetName)
        case "StrProperty":
            return str(struct.Value) if struct.Value else ""
        case "StructProperty":
            dictionary = {}
            for dict_item in struct.Value:
                dictionary[str(dict_item.Name)] = unreal_to_python_data(dict_item)
            return dictionary
        case "TextProperty":
            return str(struct.CultureInvariantString) if struct.CultureInvariantString else ""
        case _:
            return struct.Value

def python_to_unreal_data(value, struct, uasset, unreal_type=None):
    unreal_type = unreal_type if unreal_type else str(struct.PropertyType)
    match unreal_type:
        case "ArrayProperty":
            array = []
            for array_item in value:
                sub_struct = create_unreal_struct(str(struct.ArrayType), struct.DummyStruct)
                python_to_unreal_data(array_item, sub_struct, uasset, str(struct.ArrayType))
                array.append(sub_struct)
            struct.Value = array
        case "ByteProperty":
            struct.EnumValue = FName.FromString(uasset, value)
        case "EnumProperty":
            struct.Value = FName.FromString(uasset, value)
        case "NameProperty":
            struct.Value = FName.FromString(uasset, value)
        case "SoftObjectProperty":
            struct.Value = FSoftObjectPath(None, FName.FromString(uasset, value), None)
        case "StrProperty":
            struct.Value = FString(value) if value else None
        case "StructProperty":
            for dict_item in struct.Value:
                python_to_unreal_data(value[str(dict_item.Name)], dict_item, uasset)
        case "TextProperty":
            struct.CultureInvariantString = FString(value) if value else None
        case _:
            struct.Value = value

def unreal_to_unreal_data(value, struct, unreal_type=None):
    unreal_type = unreal_type if unreal_type else str(struct.PropertyType)
    match unreal_type:
        case "ByteProperty":
            struct.EnumValue = value
        case "TextProperty":
            struct.CultureInvariantString = value
        case _:
            struct.Value = value

def create_unreal_struct(unreal_type, dummy_struct=None):
    match unreal_type:
        case "BoolProperty":
            return BoolPropertyData()
        case "ByteProperty":
            struct = BytePropertyData()
            struct.ByteType = BytePropertyType.FName
            return struct
        case "EnumProperty":
            return EnumPropertyData()
        case "FloatProperty":
            return FloatPropertyData()
        case "IntProperty":
            return IntPropertyData()
        case "NameProperty":
            return NamePropertyData()
        case "SoftObjectProperty":
            return SoftObjectPropertyData()
        case "StrProperty":
            return StrPropertyData()
        case "StructProperty":
            return dummy_struct
        case "TextProperty":
            return TextPropertyData()
        case _:
            raise Exception(f"Unsupported property type: {unreal_type}")

def copy_asset_import(import_name, source_asset, target_asset):
    #Check if import already exists
    count = 0
    for old_import in game_data[target_asset].Imports:
        count -= 1
        if import_name in str(old_import.ObjectName):
            return FPackageIndex(count)
    #Gather import information
    package_index = None
    import_indexes = []
    count = 0
    for old_import in game_data[source_asset].Imports:
        if import_name in str(old_import.ObjectName) and count != package_index:
            import_indexes.append(count)
            package_index = abs(old_import.OuterIndex.Index) - 1
        count += 1
    #Add the import
    new_import_index = len(game_data[target_asset].Imports)
    for index in import_indexes:
        old_import = game_data[source_asset].Imports[index]
        new_import = Import(
            FName.FromString(game_data[target_asset], str(old_import.ClassPackage)),
            FName.FromString(game_data[target_asset], str(old_import.ClassName)),
            FPackageIndex(-(new_import_index + 1 + len(import_indexes))),
            FName.FromString(game_data[target_asset], str(old_import.ObjectName)),
            True
        )
        game_data[target_asset].Imports.Add(new_import)
    old_import = game_data[source_asset].Imports[package_index]
    new_import = Import(
        FName.FromString(game_data[target_asset], str(old_import.ClassPackage)),
        FName.FromString(game_data[target_asset], str(old_import.ClassName)),
        FPackageIndex(0),
        FName.FromString(game_data[target_asset], str(old_import.ObjectName)),
        True
    )
    game_data[target_asset].Imports.Add(new_import)
    return FPackageIndex(-(new_import_index + 1))

def squircle(value, exponent):
    return -(1-value**exponent)**(1/exponent)+1

def invert_squircle(value, exponent):
    return (1-(-value+1)**exponent)**(1/exponent)

def random_weighted(value, minimum, maximum, step, exponent, adaptive = True):
    full_range = maximum - minimum
    if random.randint(0, 1) > 0:
        distance = maximum - value
        if adaptive:
            exponent = (exponent-1)*(0.5*4**(distance/full_range))+1
        return round(round((value + squircle(random.random(), exponent)*distance)/step)*step, 3)
    else:
        distance = value - minimum
        if adaptive:
            exponent = (exponent-1)*(0.5*4**(distance/full_range))+1
        return round(round((value - squircle(random.random(), exponent)*distance)/step)*step, 3)