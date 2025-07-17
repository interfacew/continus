import os
import sys
import getopt
import logging

def showHelp():
    print("Usage:")
    print("\tMain.py -h | --help")
    print(
        "\tMain.py [--fps=<fps>] [--complexity=0|1|2] [--data=\"<path to data>\"] [--cvshow]"
    )
    print("")
    print("Options:")
    print("\t-h --help\t\tshow this help message and exit")
    print(
        "\t--fps=<fps>\t\ttarget fps when tracking (fps>=0, 0 means unlimited) [default: 8]"
    )
    print(
        "\t--complexity=0|1|2\ttrack model complexity (0 for lite, 1 for medium, 2 for heavy) [default: 2]"
    )
    print(
        "\t--data=\"<path to data>\"\tuse config file in folder <path to data> [default: \"./data\"]"
    )
    print(
        "\t--cvshow\t\tuse opencv to display camera view"
    )

if __name__ == "__main__":
    fps = 8
    complexity = 2
    dataDir = "./data"
    cvShow = False
    opts, _ = getopt.getopt(sys.argv[1:], 'h', [
        'fps=', 'complexity=', 'help', 'data=','cvshow'
    ])
    for name, value in opts:
        if name in ['-h', '--help']:
            showHelp()
            exit(0)
        elif name == '--fps':
            try:
                fps = int(value)
            except:
                print(f"invalid fps {value}")
                exit(0)
            if fps < 0:
                print(f"invalid fps {value}")
                exit(0)
        elif name == '--complexity':
            try:
                complexity = int(value)
            except:
                print(f"invalid complexity {value}")
                exit(0)
            if not complexity in [0, 1, 2]:
                print(f"invalid complexity {value}")
                exit(0)
        elif name == '--data':
            dataDir = value
        elif name=='--cvshow':
            cvShow=True

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f"{dataDir}/error.log", encoding='utf-8')
        ]
    )

    from TaskController import TaskController
    from ValidateConfig import ValidateConfig
    import mediapipe.python.solutions as sol

    logging.info(f"working in folder {dataDir}")
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
    configPath = os.path.join(dataDir, "config.json")
    if not os.path.exists(configPath):
        with open(configPath, "w") as f:
            f.write("[]")
        with sol.holistic.Holistic(min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5,
                                   model_complexity=0) as holistic:
            pass
        with sol.holistic.Holistic(min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5,
                                   model_complexity=1) as holistic:
            pass
        with sol.holistic.Holistic(min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5,
                                   model_complexity=2) as holistic:
            pass

        logging.info(f"Now you can modify {configPath} to custom your own task list")
        exit(0)

    os.chdir(dataDir)
    if not ValidateConfig("config.json"):
        exit(0)

    logging.info(f"use fps limit {fps}, model complexity {complexity}")
    controller = TaskController()
    controller.readConfig("config.json")
    controller.startListen(fps, complexity,cvShow)
