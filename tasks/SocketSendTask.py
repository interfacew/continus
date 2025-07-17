from .Task import Task
import socket
import sys
import json
from datetime import datetime
import logging


class SocketSendTask(Task):
    PACKAGE_LENGTH = 44000
    MAX_RETRY = 5

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)

        if not 'ip' in task.keys():
            logging.warning("Warning: missing key 'ip', use \"127.0.0.1\" as default")
            warningCount += 1
        elif type(task['ip']) != str:
            logging.warning(
                f"Type Error: 'ip' expects a string, but found a {type(task['ip'])}({task['ip']}) instead"
            )
            errorCount += 1

        if not 'port' in task.keys():
            logging.warning("KeyError: missing key 'port'")
            errorCount += 1
        elif not task['port'] in range(65536):
            logging.warning(
                f"Type Error: 'port' expects an int between 0 and 65535, but found {task['port']} instead"
            )
            errorCount += 1

        if not 'extra' in task.keys():
            logging.warning("Warning: missing key 'extra', use null as default")
            warningCount += 1

        return errorCount, warningCount

    def __init__(self,
                 controller: object,
                 id: str,
                 ip: str,
                 port: int,
                 extra: dict,
                 nextTasks: list,
                 start: bool = True):
        super().__init__(controller, id, "SocketSend", nextTasks, start)
        self.ip = ip
        self.port = port
        self.extra = extra
        self.isLink = False

    def activate(self, x):
        if not self.isLink:
            self.connect(x)
            self.isLink = True

    def deactivate(self, x):
        self.send("quit\0".encode('ascii'), x)
        self.socket.close()
        self.isLink = False
        self.process(x)

    def process(self, x):
        logging.info(f"processing {self.id}")
        for i in self.nextTasks:
            if i['operate'] == 'start':
                self.controller.activateTask(i['id'], x)
            if i['operate'] == 'stop':
                self.controller.deactivateTask(i['id'], x)

    def connect(self, x):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(60)
        try:
            self.socket.connect((self.ip, self.port))
        except:
            logging.warning(f"[socket] Can't connect to {self.ip}:{self.port}",
                  file=sys.stderr)
            self.controller.deactivateTask(self.id, x)

    def send(self, msg, x):
        retry = 0
        start = 0
        l = 0
        while start < len(msg):
            try:
                l = self.socket.send(msg[start:])
            except:
                logging.warning(f"[socket] Can't send message to {self.ip}:{self.port}",
                      file=sys.stderr)
                if msg != 'quit\0'.encode('ascii'):
                    self.controller.deactivateTask(self.id, x)
                break
            if l == 0:
                retry += 1
                if retry > self.MAX_RETRY:
                    logging.warning(
                        f"[socket] Can't send message to {self.ip}:{self.port}",
                        file=sys.stderr)
                    if msg != 'quit\0'.encode('ascii'):
                        self.controller.deactivateTask(self.id, x)
            else:
                retry = 0
            start += l

    def _listen(self, x):
        now = datetime.now().timestamp()
        logging.info(f"time {now}")
        _x = json.dumps({"pose": x, "time": now, "extra": self.extra}) + '\0'
        _x = _x.replace(" ", "")
        _x = _x + " " * (self.PACKAGE_LENGTH - len(_x))
        _x = _x.encode('ascii')
        self.send(_x, x)
