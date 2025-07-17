import json
import os
from tasks import *


def ValidateConfig(path):
    errorCount = 0
    warningCount = 0
    try:
        with open(path, "r") as f:
            config = json.loads(f.read())
    except json.JSONDecodeError as err:
        print(f"Invalid Json file: {err}")
        return False
    except OSError as err:
        print(f"Can't read file {path}: {err}")
        return False

    if type(config) != list:
        print(
            f"Type Error: expected a list in 'config.json', but found a {type(config)} instead"
        )
        return False

    print("checking ids...")
    ids = []
    sameIds = []
    for i, task in enumerate(config):
        if type(task) != dict:
            continue
        if not 'id' in task.keys():
            continue
        if not task['id'] in ids:
            ids.append(task['id'])
        else:
            if not task['id'] in sameIds:
                sameIds.append(task['id'])
    print(f"Loaded {len(ids)} id")

    print("checking tasks...")
    for i, task in enumerate(config):
        print("=" * 20 + f"Task {i:05d}" + "=" * 20)
        if type(task) != dict:
            print(
                f"Type Error: expected a dict, but found a {type(task)} instead"
            )
            errorCount += 1
            continue

        if not 'type' in task.keys():
            print(f"Key Error: missing key 'type'")
            errorCount += 1
            continue

        taskType = task['type']
        if taskType == "command":
            a, b = CommandTask.validate(task, ids, sameIds)
        elif taskType == "keypress":
            a, b = KeyTask.validate(task, ids, sameIds)
        elif taskType == "detect":
            a, b = DetectTask.validate(task, ids, sameIds)
        elif taskType == "match":
            a, b = MatchTask.validate(task, ids, sameIds)
        elif taskType == "timeout":
            a, b = TimeoutTask.validate(task, ids, sameIds)
        elif taskType == "socketsend":
            a, b = SocketSendTask.validate(task, ids, sameIds)
        else:
            print(f"Value Error: unknown task type {taskType}")
            a, b = 1, 0
        errorCount += a
        warningCount += b

    print("=" * 30)
    print(f"Total: {errorCount} Errors, {warningCount} Warnings")
    return errorCount == 0


if __name__ == "__main__":
    data_dir = r".\data"
    if not os.path.exists(data_dir):
        print("folder not found")
        exit(0)
    if not os.path.exists(os.path.join(data_dir, "config.json")):
        print("file not found")
        exit(0)
    os.chdir("./data")
    ValidateConfig("config.json")
