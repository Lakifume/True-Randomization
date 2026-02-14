#from clr_loader import get_coreclr
#from pythonnet import set_runtime
#
#rt = get_coreclr(runtime_config = "tr.runtimeconfig.json")
#set_runtime(rt)

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

sys.path.append(os.path.abspath("Tools/UAssetAPI"))
try:
    clr.AddReference("UAssetAPI")
    clr.AddReference("UAssetSnippet")
except Exception:
    raise Exception("Unable to access required extension files. To proceed go into Tools>UAssetAPI and manually unblock each .dll file individually.")

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

game_data = {}
datatable = {}
stringtable = {}
constant = {}
translation = {}