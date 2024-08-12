from .Task import Task
import threading
import subprocess


class CommandTask(Task):
    def __init__(self, controller: object, id: str, command: list, timeout: list, nextTasks: list = [], start: bool = True):
        super().__init__(controller, id, "Command", nextTasks, start)
        self.command = command
        self.timeout = timeout
        self.thread = None

    def runCommand(self, command, timeout, x):
        print(f"run command in task {self.id}")
        _x = str(x).replace(' ', '')
        for i, c in enumerate(command):
            print(f"\t running command {c}")
            cmd = ""
            last = ''
            for i in c:
                if i != '%':
                    if last == '%':
                        last = ''
                        if i == 's':
                            cmd += _x
                            continue
                        elif i == '%':
                            cmd += '%'
                            continue
                        else:
                            raise ValueError
                    cmd += i
                last = i
            try:
                res = subprocess.call(cmd, shell=True, timeout=(
                    None if timeout[i] == 0 else timeout[i]))
            except TimeoutError:
                print(f"Timeout when processing {cmd}")
            except OSError:
                print(f"Error when processing {cmd}")
            if res.returncode != 0:
                print(f"Error when processing {cmd}")

    def activate(self, x):
        self.thread = threading.Thread(
            target=self.runCommand, args=(self.command, self.timeout, x))
        self.thread.start()

    def _listen(self, x):
        if not self.thread.is_alive():
            self.process(x)
