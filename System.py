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
clr.AddReference("UAssetSnippet")
clr.AddReference("UAssetAPI")

from UAssetAPI import Import, UAsset
from UAssetAPI.PropertyTypes.Objects import BoolPropertyData, BytePropertyType, BytePropertyData, EnumPropertyData, FloatPropertyData, \
    IntPropertyData, NamePropertyData, SoftObjectPropertyData, StrPropertyData, TextPropertyData, FSoftObjectPath
from UAssetAPI.PropertyTypes.Structs import RotatorPropertyData, StructPropertyData, VectorPropertyData
from UAssetAPI.UnrealTypes import EngineVersion, FName, FPackageIndex, FRotator, FString, FVector
from UAssetAPI.ExportTypes import RawExport
from UAssetSnippet import UAssetSnippet

game_data : dict[str, UAsset] = {}
datatable = {}
stringtable = {}
constant = {}
translation = {}