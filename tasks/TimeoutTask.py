from datetime import datetime
from .Task import Task
import logging


class TimeoutTask(Task):

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)

        if not 'timeout' in task.keys():
            logging.error("KeyError: missing key 'timeout'")
            errorCount += 1
        elif not type(task['timeout']) in [int, float]:
            logging.error(
                f"Type Error: 'timeout' expects an int or float, but found a {type(task['timeout'])}({task['timeout']}) instead"
            )
            errorCount += 1

        return errorCount, warningCount

    def __init__(self,
                 controller: object,
                 id: str,
                 timeout: int,
                 nextTasks: list = [],
                 start: bool = True):
        super().__init__(controller, id, "Timeout", nextTasks, start)
        self.activateTime = -1
        self.timeout = timeout

    def activate(self, x):
        self.activateTime = datetime.now().timestamp() * 1000

    def deactivate(self, x):
        self.activateTime = -1

    def _listen(self, x):
        logging.info(
            f"time last {self.timeout-(datetime.now().timestamp()*1000-self.activateTime)}"
        )
        if datetime.now().timestamp(
        ) * 1000 - self.activateTime >= self.timeout:
            self.process(x)
