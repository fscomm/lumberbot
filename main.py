import win32api, win32con, win32gui
import time, win32com.client
import SendKeys

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def openItNow(hwnd, windowText):
    if windowText in win32gui.GetWindowText(hwnd):
        win32gui.SetForegroundWindow(hwnd)

def main():
    win32gui.EnumWindows(openItNow, 'Lumberjack')
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("{SPACE}")
    time.sleep(5)

if __name__ == "__main__":
    main()