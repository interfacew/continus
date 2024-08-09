import pyautogui
from io import BytesIO
import win32clipboard

def screenshot():
    screenshot = pyautogui.screenshot()
    output = BytesIO()
    screenshot.convert("RGB").save(output, "BMP")

    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    print("screenshot completed")

def game_bar_recording_start():
    pyautogui.hotkey('win','alt','r')
    print("game bar recording start")

def game_bar_recording_stop():
    pyautogui.hotkey('win','alt','r')
    print("game bar recording stop")




# if __name__ == '__main__':
    # screenshot()