import os
import sys
import getopt


def showHelp():
    print("Usage:")
    print("\tMain.py -h | --help")
    print(
        "\tMain.py [--fps=<fps>] [--complexity=0|1|2] [--data=\"<path to data>\"] [--no-env-check] [--no-env-download]"
    )
    print()
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
    print("\t--no-env-check\t\tdo not check environment")
    print("\t--no-env-download\tdo not download when missing package")


if __name__ == "__main__":
    fps = 8
    complexity = 2
    dataDir = r".\data"
    envCheck = True
    envDownload = True
    opts, _ = getopt.getopt(sys.argv[1:], 'h', [
        'fps=', 'complexity=', 'help', 'data=', 'no-env-check',
        'no-env-download'
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

    # from Utils import testPackages
    # if envCheck:
        # res = testPackages(envDownload)
        # if not (envDownload or res):
            # exit(0)

    from TaskController import TaskController
    from ValidateConfig import ValidateConfig
    import mediapipe.python.solutions as sol

    print(f"working in folder {dataDir}")
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

        print(f"Now you can modify {configPath} to custom your own task list")
        exit(0)

    os.chdir(dataDir)
    errlog = open("error.log", "w", encoding='utf-8')
    sys.stderr = errlog
    if not ValidateConfig("config.json"):
        exit(0)

    print(f"use fps limit {fps}, model complexity {complexity}")
    controller = TaskController()
    controller.readConfig("config.json")
    controller.startListen(fps, complexity)
