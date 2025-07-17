import json
import os
from tasks import *
import logging


def ValidateConfig(path):
    errorCount = 0
    warningCount = 0
    try:
        with open(path, "r") as f:
            config = json.loads(f.read())
    except json.JSONDecodeError as err:
        logging.error(f"Invalid Json file: {err}")
        return False
    except OSError as err:
        logging.error(f"Can't read file {path}: {err}")
        return False

    if type(config) != list:
        logging.error(
            f"Type Error: expected a list in 'config.json', but found a {type(config)} instead"
        )
        return False

    logging.info("checking ids...")
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
    logging.info(f"Loaded {len(ids)} id")

    logging.info("checking tasks...")
    for i, task in enumerate(config):
        logging.info("=" * 20 + f"Task {i:05d}" + "=" * 20)
        if type(task) != dict:
            logging.error(
                f"Type Error: expected a dict, but found a {type(task)} instead"
            )
            errorCount += 1
            continue

        if not 'type' in task.keys():
            logging.error(f"Key Error: missing key 'type'")
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
            logging.error(f"Value Error: unknown task type {taskType}")
            a, b = 1, 0
        errorCount += a
        warningCount += b

    logging.info("=" * 30)
    if errorCount == 0:
        if warningCount == 0:
            logging.info(f"Total: {errorCount} Errors, {warningCount} Warnings")
        else:
            logging.warning(f"Total: {errorCount} Errors, {warningCount} Warnings")
    else:
        logging.error(f"Total: {errorCount} Errors, {warningCount} Warnings")
    return errorCount == 0


if __name__ == "__main__":
    data_dir = "./data"
    if not os.path.exists(data_dir):
        logging.error("folder not found")
        exit(0)
    if not os.path.exists(os.path.join(data_dir, "config.json")):
        logging.error("file not found")
        exit(0)
    os.chdir("./data")
    ValidateConfig("config.json")
