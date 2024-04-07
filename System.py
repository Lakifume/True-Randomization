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

from UAssetAPI import *
from UAssetAPI.FieldTypes import *
from UAssetAPI.JSON import *
from UAssetAPI.Kismet import *
from UAssetAPI.Kismet.Bytecode import *
from UAssetAPI.Kismet.Bytecode.Expressions import *
from UAssetAPI.PropertyTypes import *
from UAssetAPI.PropertyTypes.Objects import *
from UAssetAPI.PropertyTypes.Structs import *
from UAssetAPI.UnrealTypes import *
from UAssetAPI.Unversioned import *
from UAssetSnippet import *

#test = UAsset("PB_DT_DropRateMaster.uasset", UE4Version.VER_UE4_22)
#test.AddNameReference(FString("FloatProperty"))
#test.Write("PB_DT_DropRateMaster2.uasset")

game_data = {}
datatable = {}
stringtable = {}
constant = {}
translation = {}