import os
import clr
import json
import math
import random
import sys
import shutil
import copy
import filecmp
import struct
import colorsys

from enum import Enum
from collections import OrderedDict

sys.path.append(os.path.abspath("Tools\\UAssetAPI"))
clr.AddReference("UAssetAPI")
clr.AddReference("UAssetSnippet")

from UAssetAPI import Import, UAsset
from UAssetAPI.PropertyTypes.Objects import BoolPropertyData, BytePropertyType, BytePropertyData, EnumPropertyData, FloatPropertyData, \
    IntPropertyData, NamePropertyData, SoftObjectPropertyData, StrPropertyData, TextPropertyData
from UAssetAPI.PropertyTypes.Structs import RotatorPropertyData, StructPropertyData, VectorPropertyData
from UAssetAPI.UnrealTypes import EngineVersion, FName, FPackageIndex, FRotator, FString, FVector
from UAssetSnippet import UAssetSnippet

#test = UAsset("PB_DT_DropRateMaster.uasset", UE4Version.VER_UE4_22)
#test.AddNameReference(FString("FloatProperty"))
#test.Write("PB_DT_DropRateMaster2.uasset")

game_data = {}
datatable = {}
stringtable = {}
constant = {}
translation = {}