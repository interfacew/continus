from .Task import Task
try:
    import requests
except ModuleNotFoundError:
    print("Warning: cannot found module 'requests', ignore all keytask.")
    print("         use 'pip install requests==2.32.4' to install")
    class _dummy:
        @classmethod
        def request(*args):
            pass
    requests=_dummy
import json
from datetime import datetime

class RequestTask(Task):

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)

        if not 'url' in task.keys():
            print("KeyError: missing key 'url'")
            errorCountCount += 1
        elif type(task['url']) != str:
            print(
                f"Type Error: 'url' expects a string, but found a {type(task['url'])}({task['url']}) instead"
            )
            errorCount += 1

        if not 'method' in task.keys():
            print("KeyError: missing key 'method'")
            errorCount += 1
        elif not task['method'] in ["HEAD","GET","POST","PUT","PATCH","DELETE"]:
            print(
                f"ValueError: 'port' expects a http method, but found {task['timeout']} instead"
            )
            errorCount += 1
        elif task['method'] in ["POST","PUT","PATCH"]:
            if not 'data' in task.keys():
                print("Warning: missing key 'data', use null as default")
                warningCount+=1

        if not 'headers' in task.keys():
            print("Warning: missing key 'headers', use null as default")
            warningCount+=1

        if not 'cookies' in task.keys():
            print("Warning: missing key 'cookies', use null as default")
            warningCount+=1

        if not 'extra' in task.keys():
            print("Warning: missing key 'extra', use null as default")
            warningCount += 1

        return errorCount, warningCount

    def __init__(self,
                 controller: object,
                 id: str,
                 url: str,
                 method: int,
                 data: dict,
                 headers: dict,
                 cookies: dict,
                 nextTasks: list,
                 start: bool = True):
        super().__init__(controller, id, "Request", nextTasks, start)
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers
        self.cookies = cookies

    def formatData(self,data,pose:str):
        if type(data)==list:
            for i in range(len(data)):
                if type(data[i])==str :
                    if data[i].find(r"${pose}")!=-1:
                        data[i].replace(r"${pose}",pose)
                elif type(data[i])==dict or type(data[i])==list:
                    data[i]=self.formatData(data[i],pose)
            return data
        for key in data.keys():
            if type(data[key])==str :
                if data[key].find(r"${pose}")!=-1:
                    data[key].replace(r"${pose}",pose)
            elif type(data[key])==dict or type(data[key])==list:
                data[key]=self.formatData(data[key],pose)
        return data

    def activate(self, x):
        now = datetime.now().timestamp()
        print(f"time {now}")
        pose=json.dumps({"pose": x, "time": now})
        requests.request(self.method,self.url,headers=self.headers,cookies=self.cookies,data=self.formatData(self.data,pose))
        self.process(x)
