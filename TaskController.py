from tasks import *
import json
import cv2 as cv
from Utils import drawLandmarks, extractLandmarks, generateNullLandmarks
import mediapipe.python.solutions as sol
import time
from collections import deque
import math
import logging


class TaskController:
    FPS_COUNT_FRAME = 10

    def __init__(self):
        self.tasks = {}
        self.activate = {}

    def listen(self, x):
        print("\033[H\033[J")

        for i in self.tasks.keys():
            if self.activate[i]:
                self.tasks[i].listen(x)

    def activateTask(self, id: str, x):
        if not id in self.activate.keys():
            logging.error(f"Unknown task id {id}")
            return
        self.activate[id] = True
        self.tasks[id].activate(x)

    def deactivateTask(self, id: str, x):
        if not id in self.activate.keys():
            logging.error(f"Unknown task id {id}")
            return
        self.activate[id] = False
        self.tasks[id].deactivate(x)

    def removeTask(self, id: str):
        self.activate.pop(id)

    def addTask(self, task: Task):
        self.tasks[task.id] = task
        self.activate[task.id] = False
        if task.start:
            self.activateTask(task.id, generateNullLandmarks())

    def clear(self):
        self.tasks = {}
        self.Activate = {}

    def readConfig(self, path: str):
        with open(path, "r") as f:
            config = json.loads(f.read())
        for task in config:
            taskType = task['type']
            if taskType == "command":
                taskObject = CommandTask(self, task['id'], task['command'],
                                         task.get('timeout',[]),
                                         task.get('nextTasks', []),
                                         task.get('start', False))
            elif taskType == "keypress":
                taskObject = KeyTask(self, task['id'], task['keys'],
                                     task.get('nextTasks', []),
                                     task.get('start', False))
            elif taskType == "detect":
                taskObject = DetectTask(self, task['id'], task['bodyPart'],
                                        task['frames'],
                                        task.get('nextTasks', []),
                                        task.get('start', False))
            elif taskType == "match":
                taskObject = MatchTask(self, task['id'], task['bodyPart'],
                                       task['poseFile'],
                                       task['sensetive'], task['frames'],
                                       task.get('nextTasks', []),
                                       task.get('start', False))
            elif taskType == "timeout":
                taskObject = TimeoutTask(self, task['id'], task['timeout'],
                                         task.get('nextTasks', []),
                                         task.get('start', False))
            elif taskType == "socketsend":
                taskObject = SocketSendTask(self, task['id'],
                                            task.get('ip', "127.0.0.1"),
                                            task['port'],
                                            task.get('extra', None),
                                            task.get('nextTasks', []),
                                            task.get('start', False))
            elif taskType == "request":
                taskObject = RequestTask(self, task['id'],
                                            task['url'],
                                            task['port'],
                                            task.get('data', {}),
                                            task.get('headers', {}),
                                            task.get('cookies', {}),
                                            task.get('nextTasks', []),
                                            task.get('start', False))
            self.addTask(taskObject)

    def startListen(self, targetFPS, modelComplexity):
        camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        camera.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        camera.set(cv.CAP_PROP_FPS, 60)
        q = deque([], self.FPS_COUNT_FRAME + 10)
        framecnt = 0
        with sol.holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                model_complexity=modelComplexity) as holistic:
            while camera.isOpened():
                ret, frame = camera.read()
                waitTime = 1
                if ret:
                    start = time.time() * 1e3

                    frame = frame[:, ::-1, :]
                    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = holistic.process(image)
                    image.flags.writeable = True
                    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                    drawLandmarks(image, results)

                    if framecnt >= self.FPS_COUNT_FRAME * 3:
                        self.listen(extractLandmarks(results))

                    now = time.time() * 1e3
                    if framecnt >= self.FPS_COUNT_FRAME:
                        last = q.pop()
                        cv.putText(
                            image,
                            f"FPS: {self.FPS_COUNT_FRAME*1e3/(now-last):.3f}",
                            (10, 30),
                            cv.FONT_HERSHEY_COMPLEX,
                            1.0, (255, 0, 0),
                            bottomLeftOrigin=False)
                        if targetFPS != 0:
                            waitTime = max(
                                1,
                                math.floor(1e3 / targetFPS - (now - start)) -
                                3)
                        else:
                            waitTime = 1
                    q.appendleft(now)

                    cv.imshow('OpenCV Feed', image)
                    framecnt += 1

                if cv.waitKey(waitTime) & 0xFF == ord('q'):
                    for task in self.tasks.keys():
                        self.deactivateTask(task, generateNullLandmarks())
                    break
            camera.release()
            cv.destroyAllWindows()
