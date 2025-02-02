import json
import math
from collections import OrderedDict

with open("Data\\Dictionary\\EnemyLocation.json", "r") as file_reader:
    enemy_info = json.load(file_reader)
with open("Data\\Dictionary\\ActorPointer.json", "r") as file_reader:
    actor_pointer = json.load(file_reader)

for i in enemy_info:
    try:
        enemy_info[i]["ExportIndex"]
        actor_pointer["Chr_" + i + "_C"] = {}
        actor_pointer["Chr_" + i + "_C"]["Name"] = i
        try:
            actor_pointer["Chr_" + i + "_C"]["File"] = enemy_info[i]["ExportFile"]
        except KeyError:
            actor_pointer["Chr_" + i + "_C"]["File"] = enemy_info[i]["NormalModeRooms"][0] + "_Enemy"
        actor_pointer["Chr_" + i + "_C"]["Index"] = enemy_info[i]["ExportIndex"]
    except KeyError:
        continue
    del enemy_info[i]["ExportName"]
    del enemy_info[i]["ExportIndex"]

with open("Data\\Dictionary\\NewActorPointer.json", "w") as file_writer:
    file_writer.write(json.dumps(actor_pointer, indent=2))
with open("Data\\Dictionary\\NewEnemyLocation.json", "w") as file_writer:
    file_writer.write(json.dumps(enemy_info, indent=2))