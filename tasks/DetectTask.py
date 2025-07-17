from .Task import Task
import logging

class DetectTask(Task):

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)

        if not 'bodyPart' in task.keys():
            logging.error("Key Error: missing key 'bodyPart'")
            errorCount += 1
        elif type(task['bodyPart']) != list:
            logging.error(
                f"Type Error: 'bodyPart' expects a list, but found a {type(task['bodyPart'])}({task['bodyPart']}) instead"
            )
            errorCount += 1
        else:
            for i, part in enumerate(task['bodyPart']):
                if not part in ['face', 'leftHand', 'rightHand', 'body']:
                    logging.error(
                        f"bodyPart[{i}] Value Error: expects a key in ['face','leftHand','rightHand','body'], but found a {part} instead"
                    )
                    errorCount += 1

        if not 'frames' in task.keys():
            logging.error("Key Error: missing key 'frames'")
            errorCount += 1
        elif type(task['frames']) != int:
            logging.error(
                f"Type Error: 'frames' expects a int, but found a {type(task['frames'])}({task['frames']}) instead"
            )
            errorCount += 1

        return errorCount, warningCount

    def __init__(self,
                 controller: object,
                 id: str,
                 bodyPart: list,
                 frames: int = 1,
                 nextTasks: list = [],
                 start: bool = True):
        super().__init__(controller, id, "Detect", nextTasks, start)
        self.bodyPart = bodyPart
        self.frames = frames
        self.count = 0

    def activate(self, x):
        self.count = 0

    def _listen(self, x):
        logging.info(f"detect {self.bodyPart} ({self.count}/{self.frames})")
        for part in self.bodyPart:
            if x[part] == None:
                self.count = 0
                logging.info(f"")
                return
        self.count += 1
        logging.info("")
        if self.count >= self.frames:
            self.process(x)
