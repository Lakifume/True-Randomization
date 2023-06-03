import Manager
import random
import copy

def init():
    #Declare variables
    global is_tome
    is_tome = []
    global completion
    completion = []
    global count
    count = []
    #Process variables
    for num in range(20):
        completion.append(num*5)
    completion.append(99)
    for num in range(21):
        if num % 2 == 0:
            is_tome.append(True)
        else:
            is_tome.append(False)
        count.append(num)

def randomize_library_tomes(req, appear):
    #Start by randomizing Tome of Conquest, ensuring that it alwasy exists
    chosen = random.choice(count)
    while not is_tome[chosen]:
        chosen = random.choice(count)
    count.remove(chosen)
    if req:
        Manager.datatable["PB_DT_BookMaster"]["Bookofthechampion"]["RoomTraverseThreshold"] = completion[chosen]
    if appear:
        Manager.datatable["PB_DT_BookMaster"]["Bookofthechampion"]["IslibraryBook"] = is_tome[chosen]
    #Randomize the rest with no guarantees of existing
    for entry in Manager.datatable["PB_DT_BookMaster"]:
        if entry in ["Dummy", "Bookofthechampion"]:
            continue
        chosen = pick_and_remove(count)
        if req:
            Manager.datatable["PB_DT_BookMaster"][entry]["RoomTraverseThreshold"] = completion[chosen]
        if appear:
            Manager.datatable["PB_DT_BookMaster"][entry]["IslibraryBook"] = is_tome[chosen]

def pick_and_remove(array):
    item = random.choice(array)
    array.remove(item)
    return item

def create_log():
    log = {}
    for entry in Manager.datatable["PB_DT_BookMaster"]:
        if entry == "Dummy":
            continue
        if Manager.datatable["PB_DT_BookMaster"][entry]["IslibraryBook"]:
            log[Manager.translation["Item"][entry]] = Manager.datatable["PB_DT_BookMaster"][entry]["RoomTraverseThreshold"]
    return log