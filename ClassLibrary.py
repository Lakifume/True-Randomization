import ClassManagement
import random

is_tome = []
completion = []
count = []
log = {}

def init():
    for i in range(20):
        completion.append(i*5)
    completion.append(99)
    
    for i in range(21):
        if i % 2 == 0:
            is_tome.append(True)
        else:
            is_tome.append(False)
        count.append(i)
    ClassManagement.debug("ClassLibrary.init()")

def rand_book(req, appear):
    chosen = any_pick_true(count)
    if req:
        ClassManagement.book_content[21]["Value"]["RoomTraverseThreshold"] = completion[chosen]
    if appear:
        ClassManagement.book_content[21]["Value"]["IslibraryBook"] = is_tome[chosen]
    i = 1
    while i <= 20:
        chosen = any_pick(count)
        if req:
            ClassManagement.book_content[i]["Value"]["RoomTraverseThreshold"] = completion[chosen]
        if appear:
            ClassManagement.book_content[i]["Value"]["IslibraryBook"] = is_tome[chosen]
        i += 1
    i = 1
    while i <= 21:
        if ClassManagement.book_content[i]["Value"]["IslibraryBook"]:
            log[ClassManagement.item_translation[ClassManagement.book_content[i]["Key"]]] = ClassManagement.book_content[i]["Value"]["RoomTraverseThreshold"]
        i += 1
    ClassManagement.debug("ClassLibrary.rand_book(" + str(req) + ", " + str(appear) + ")")

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item
    
def any_pick_true(array):
    item = random.choice(array)
    while not is_tome[item]:
        item = random.choice(array)
    array.remove(item)
    return item

def get_log():
    return log