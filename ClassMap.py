import ClassManagement
import os

log = []

def create_log(path):
    name, extension = os.path.splitext(path)
    log_data = {}
    log_data["Key"] = "Map"
    log_data["Value"] = {}
    log_data["Value"]["FileName"] = name.split("\\")[-1]
    log.append(log_data)
    ClassManagement.debug("ClassMap.create_log(" + path + ")")

def get_log():
    return log