import json
from .Task import Task
import os
import logging


class MatchTask(Task):

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)
        flag1, flag2, flag3, flag4 = False, False, False, False

        if not 'bodyPart' in task.keys():
            logging.error("Key Error: missing key 'bodyPart'")
            errorCount += 1
        elif type(task['bodyPart']) != list:
            logging.error(
                f"Type Error: 'bodyPart' expects a list, but found a {type(task['bodyPart'])}({task['bodyPart']}) instead"
            )
            errorCount += 1
        else:
            flag1 = True
            for i, parts in enumerate(task['bodyPart']):
                if type(parts) != list:
                    logging.error(
                        f"bodyPart[{i}] Type Error: expects a list, but found a {type(parts)}({parts}) instead"
                    )
                    errorCount += 1
                else:
                    for j, part in enumerate(parts):
                        if not part in [
                                'face', 'leftHand', 'rightHand', 'body'
                        ]:
                            logging.error(
                                f"bodyPart[{i}][{j}] Value Error: expects a key in ['face','leftHand','rightHand','body'], but found a {part} instead"
                            )
                            errorCount += 1

        if not 'poseFile' in task.keys():
            logging.error("Key Error: missing key 'poseFile'")
            errorCount += 1
        elif type(task['poseFile']) != list:
            logging.error(
                f"Type Error: 'poseFile' expects a list, but found a {type(task['poseFile'])}({task['poseFile']}) instead"
            )
            errorCount += 1
        else:
            flag2 = True
            for i, file in enumerate(task['poseFile']):
                if type(file) != str:
                    logging.error(
                        f"poseFile[{i}] Type Error: expects a string, but found a {type(file)}({file}) instead"
                    )
                    errorCount += 1
                else:
                    if not (os.path.exists(file) and os.path.isfile(file)):
                        logging.error(
                            f"poseFile[{i}] Value Error: {file} is not exist or not a file"
                        )
                        errorCount += 1
                        continue
                    try:
                        f = open(file, 'r')
                        pose = json.loads(f.read())
                        f.close()
                    except OSError:
                        logging.error(
                            f"poseFile[{i}] Value Error: can not open file {file}")
                        errorCount += 1
                        continue
                    except json.JSONDecodeError as e:
                        logging.error(
                            f"poseFile[{i}] Value Error: can not load json file {file}:\n\t{e.msg}"
                        )
                        errorCount += 1
                        continue
                    if not 'face' in pose.keys() or pose['face'] == None:
                        logging.warning(
                            f"poseFile[{i}] Warning: missing key 'face' in {file}"
                        )
                        warningCount += 1
                    else:
                        if len(pose['face']) != 468:
                            logging.error(
                                f"poseFile[{i}] Value Error: 'face' array has an incorrect length: {len(pose['face'])}"
                            )
                            errorCount += 1
                    if not 'leftHand' in pose.keys(
                    ) or pose['leftHand'] == None:
                        logging.warning(
                            f"poseFile[{i}] Warning: missing key 'leftHand' in {file}"
                        )
                        warningCount += 1
                    else:
                        if len(pose['leftHand']) != 21:
                            logging.error(
                                f"poseFile[{i}] Value Error: 'leftHand' array has an incorrect length: {len(pose['leftHand'])}"
                            )
                            errorCount += 1
                    if not 'rightHand' in pose.keys(
                    ) or pose['rightHand'] == None:
                        logging.warning(
                            f"poseFile[{i}] Warning: missing key 'rightHand' in {file}"
                        )
                        warningCount += 1
                    else:
                        if len(pose['rightHand']) != 21:
                            logging.error(
                                f"poseFile[{i}] Value Error: 'rightHand' array has an incorrect length: {len(pose['rightHand'])}"
                            )
                            errorCount += 1
                    if not 'body' in pose.keys() or pose['body'] == None:
                        logging.warning(
                            f"poseFile[{i}] Warning: missing key 'body' in {file}"
                        )
                        warningCount += 1
                    else:
                        if len(pose['body']) != 33:
                            logging.error(
                                f"poseFile[{i}] Value Error: 'body' array has an incorrect length: {len(pose['body'])}"
                            )
                            errorCount += 1

        if not 'sensetive' in task.keys():
            logging.error("Key Error: missing key 'sensetive'")
            errorCount += 1
        elif type(task['sensetive']) != list:
            logging.error(
                f"Type Error: 'sensetive' expects a list, but found a {type(task['sensetive'])}({task['sensetive']}) instead"
            )
            errorCount += 1
        else:
            flag3 = True
            for i, sensetive in enumerate(task['sensetive']):
                if not type(sensetive) in [int, float]:
                    logging.error(
                        f"sensetive[{i}] Type Error: expects an int or float, but found a {type(sensetive)}({sensetive}) instead"
                    )
                    errorCount += 1

        if not 'frames' in task.keys():
            logging.error("Key Error: missing key 'frames'")
            errorCount += 1
        elif type(task['frames']) != list:
            logging.error(
                f"Type Error: 'frames' expects a list, but found a {type(task['frames'])}({task['frames']}) instead"
            )
            errorCount += 1
        else:
            flag4 = True
            for i, frame in enumerate(task['frames']):
                if type(frame) != int:
                    logging.error(
                        f"frames[{i}] Type Error: expects an int, but found a {type(frame)}({frame}) instead"
                    )
                    errorCount += 1

        if flag1 and flag2 and flag3 and flag4 and not (
                len(task['poseFile']) == len(task['bodyPart'])
                and len(task['poseFile']) == len(task['sensetive'])
                and len(task['poseFile']) == len(task['frames'])):
            logging.error(
                "ValueError: the lengths of 'poseFile' array, 'bodyPart' array, 'sensetive' array and 'frames' array do not match"
            )
            errorCount += 1

        return errorCount, warningCount

    def normalizePoints(points):
        res = []
        maxx, maxy, maxz, minx, miny, minz = -1, -1, -1, 1, 1, 1
        for point in points:
            maxx = max(maxx, point[0])
            maxy = max(maxy, point[1])
            maxz = max(maxz, point[2])
            minx = min(minx, point[0])
            miny = min(miny, point[1])
            minz = min(minz, point[2])
        maxDelta = max(maxx - minx, maxy - miny)
        if maxDelta <= 1e-8:
            return [[0, 0, 0]] * len(points)
        for point in points:
            newx = (point[0] - (maxx + minx) / 2) / maxDelta
            newy = (point[1] - (maxy + miny) / 2) / maxDelta
            newz = (point[2] - (maxz + minz) / (maxz - minz) / 4)
            if newx < -0.5 - 1e-8 or newx > 0.5 + 1e-8 or newy < -0.5 - 1e-8 or newy > 0.5 + 1e-8 or newz < -0.125 - 1e-8 or newz > 0.125 + 1e-8:
                raise ValueError(f"NormalizePoints out of range: {[point[0], point[1], point[2], newx, newy, newz, maxDelta, maxx, maxy, minx, miny, maxz, minz]}")
            res.append([newx, newy, newz])
        return res

    def calcDelta(bodyPart, x, pose):
        delta = 0.0
        for part in bodyPart:
            if x[part] == None or pose[part] == None:
                return -1
            points = MatchTask.normalizePoints(x[part])
            match = MatchTask.normalizePoints(pose[part])
            if len(points) != len(match):
                raise ValueError(
                    f"Point count unmatch! Expect {len(match)} but find {len(points)}"
                )
            for i in range(len(points)):
                delta += ((points[i][0] - match[i][0])**2 +
                          (points[i][1] - match[i][1])**2 +
                          (points[i][2] - match[i][2])**2)
        return delta

    def __init__(self,
                 controller: object,
                 id: str,
                 bodyPart: list,
                 poseFile: list,
                 sensetive: list,
                 frames: list,
                 nextTasks: list = [],
                 start: bool = True):
        super().__init__(controller, id, "Match", nextTasks, start)
        self.bodyPart = bodyPart
        self.pose = []
        self.poseName = []
        self.sensetive = sensetive
        self.frames = frames
        for file in poseFile:
            logging.info(f"reading {file}...")
            with open(file, "r") as f:
                self.pose.append(json.loads(f.read()))
            self.poseName.append(file.split('/')[-1].split('\\')[-1])
        self.count = [0] * len(self.pose)

    def activate(self, x):
        self.count = [0] * len(self.pose)

    def _listen(self, x):
        logging.info(f"poses {str(self.poseName)}:")
        for i in range(len(self.pose)):
            delta = MatchTask.calcDelta(self.bodyPart[i], x, self.pose[i])
            msg = (
                f"\tpose {self.poseName[i]}, delta {delta:.5f} ({self.count[i]}/{self.frames[i]})"
            )
            if delta != -1 and delta < self.sensetive[i]:
                logging.info(msg + " match")
                self.count[i] += 1
                if self.count[i] >= self.frames[i]:
                    self.process(x)
                    return
            logging.info(msg)
            self.count[i] = 0
