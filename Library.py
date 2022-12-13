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
    for i in range(20):
        completion.append(i*5)
    completion.append(99)
    for i in range(21):
        if i % 2 == 0:
            is_tome.append(True)
        else:
            is_tome.append(False)
        count.append(i)

def rand_book(req, appear):
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
    for i in Manager.datatable["PB_DT_BookMaster"]:
        if i in ["Dummy", "Bookofthechampion"]:
            continue
        chosen = any_pick(count)
        if req:
            Manager.datatable["PB_DT_BookMaster"][i]["RoomTraverseThreshold"] = completion[chosen]
        if appear:
            Manager.datatable["PB_DT_BookMaster"][i]["IslibraryBook"] = is_tome[chosen]

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item

def create_log():
    log = {}
    for i in Manager.datatable["PB_DT_BookMaster"]:
        if i == "Dummy":
            continue
        if Manager.datatable["PB_DT_BookMaster"][i]["IslibraryBook"]:
            log[Manager.translation["Item"][i]] = Manager.datatable["PB_DT_BookMaster"][i]["RoomTraverseThreshold"]
    return log