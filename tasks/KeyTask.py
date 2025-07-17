from .Task import Task
try:
    import pyautogui
except ModuleNotFoundError:
    print("Warning: cannot found module 'pyautogui', ignore all keytask.")
    print("         use 'pip install PyAutoGUI==0.9.54' to install")
    class _dummy:
        KEYBOARD_KEYS=[
            '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'alt', 'altleft', 'altright', 'command', 'ctrl', 'ctrlleft', 'ctrlright', 'option', 'optionleft', 'optionright', 'shift', 'shiftleft', 'shiftright', 'win', 'winleft', 'winright',
            'backspace', 'capslock', 'del', 'delete', 'enter', 'esc', 'escape', 'fn', 'insert', 'return', 'space', 'tab',
            'down', 'left', 'right', 'up', 'end', 'home', 'pagedown', 'pageup', 'pgdn', 'pgup',
            'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'add', 'decimal', 'divide', 'multiply', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'subtract',
            'pause', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'scrolllock',
            'accept', 'apps', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'clear', 'convert', 'execute', 'final', 'hanguel', 'hangul', 'hanja', 'help', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'modechange', 'nexttrack', 'nonconvert', 'playpause', 'prevtrack', 'print', 'select', 'separator', 'sleep', 'stop', 'volumedown', 'volumemute', 'volumeup', 'yen'
        ]
        @classmethod
        def hotkey(*args):
            pass
    pyautogui=_dummy


class KeyTask(Task):

    @classmethod
    def validate(cls, task: dict, ids: list, sameIds: list):
        errorCount, warningCount = super().validate(task, ids, sameIds)
        if not 'keys' in task.keys():
            print("Key Error: missing key 'keys'")
            errorCount += 1
        elif type(task['keys']) != list:
            print(
                f"Type Error: 'keys' expects a list, but found a {type(task['keys'])}({task['keys']}) instead"
            )
            errorCount += 1
        else:
            for i, hotkey in enumerate(task['keys']):
                if type(hotkey) != list:
                    print(
                        f"keys[{i}] Type Error: expects a list, but found a {type(hotkey)}({hotkey}) instead"
                    )
                    errorCount += 1
                else:
                    for j, key in enumerate(hotkey):
                        if not key in pyautogui.KEYBOARD_KEYS:
                            print(
                                f"keys[{i}][{j}] Value Error: expects a key in pyautogui.KEYBOARD_KEYS, but found {key} instead"
                            )
        return errorCount, warningCount

    def __init__(self,
                 controller: object,
                 id: str,
                 keys: list,
                 nextTasks: list = [],
                 start: bool = True):
        super().__init__(controller, id, "Key", nextTasks, start)
        self.keys = keys

    def activate(self, x):
        print(f"press keys in task {self.id}")
        for keyset in self.keys:
            pyautogui.hotkey(*keyset)
        self.process(x)
