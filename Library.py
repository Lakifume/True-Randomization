from System import *
import Utility

class ReqCurve(Enum):
    Concave = 0
    Linear  = 1
    Convex  = 2

def init():
    global tome_to_properties
    tome_to_properties = {}

def set_requirement_weight(weight):
    global requirement_weight
    requirement_weight = ReqCurve(weight-1)

def randomize_library_requirements():
    #Fill requirement list
    property_list = []
    for num in range(20):
        match requirement_weight:
            case ReqCurve.Concave:
                completion = round(Utility.squircle(num/20, 1.5)*100)
            case ReqCurve.Linear:
                completion = round(num*5)
            case ReqCurve.Convex:
                completion = round(Utility.invert_squircle(num/20, 1.5)*100)
        property_list.append((completion, num % 2 == 0))
    property_list.append((99, True))
    #Assign tome of conquest
    chosen = random.choice(property_list)
    while not chosen[1]:
        chosen = random.choice(property_list)
    property_list.remove(chosen)
    tome_to_properties["Bookofthechampion"] = chosen
    datatable["PB_DT_BookMaster"]["Bookofthechampion"]["RoomTraverseThreshold"] = chosen[0]
    #Assign the rest
    for entry in datatable["PB_DT_BookMaster"]:
        if entry in ["Dummy", "Bookofthechampion"]:
            continue
        tome_to_properties[entry] = pick_and_remove(property_list)
        datatable["PB_DT_BookMaster"][entry]["RoomTraverseThreshold"] = tome_to_properties[entry][0]

def randomize_tome_appearance():
    #If requirements were randomized remove tomes that have uneven indexes
    if tome_to_properties:
        for entry in datatable["PB_DT_BookMaster"]:
            if entry in ["Dummy", "Bookofthechampion"]:
                continue
            datatable["PB_DT_BookMaster"][entry]["IslibraryBook"] = tome_to_properties[entry][1]
    #If requirements are vanilla remove 10 tomes at complete random
    else:
        book_list = list(datatable["PB_DT_BookMaster"])
        book_list.remove("Dummy")
        book_list.remove("Bookofthechampion")
        for num in range(10):
            chosen = pick_and_remove(book_list)
            datatable["PB_DT_BookMaster"][chosen]["IslibraryBook"] = False

def pick_and_remove(array):
    item = random.choice(array)
    array.remove(item)
    return item

def create_log():
    log = {}
    for entry in datatable["PB_DT_BookMaster"]:
        if datatable["PB_DT_BookMaster"][entry]["IslibraryBook"]:
            log[translation["Item"][entry]] = datatable["PB_DT_BookMaster"][entry]["RoomTraverseThreshold"]
    return log