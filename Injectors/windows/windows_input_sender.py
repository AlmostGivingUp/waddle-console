import ctypes 
from ctypes import wintypes

from ctypes import c_ulong, c_ulonglong
from Constants.windows_const import MOUSE_FLAG



INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
RELEASE = 0x0002
from platform import architecture

if architecture()[0] == '64bit':
    ULONG_PTR = c_ulonglong
else:
    ULONG_PTR = c_ulong
""" 
https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput 
typedef struct tagKEYBDINPUT {
  WORD      wVk;
  WORD      wScan;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} KEYBDINPUT, *PKEYBDINPUT, *LPKEYBDINPUT;
"""
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]
"""
https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
typedef struct tagMOUSEINPUT {
  LONG      dx;
  LONG      dy;
  DWORD     mouseData;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} MOUSEINPUT, *PMOUSEINPUT, *LPMOUSEINPUT;
"""
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

"""
https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input 
typedef struct tagINPUT {
  DWORD type;
  union {
    MOUSEINPUT    mi;
    KEYBDINPUT    ki;
    HARDWAREINPUT hi;
  } DUMMYUNIONNAME;
} INPUT, *PINPUT, *LPINPUT;
"""

class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [
            ("ki", KEYBDINPUT),
            ("mi", MOUSEINPUT),
           #("hi", HARDWAREINPUT) 
        ]
    #expose keyboard and mouseinput
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", _INPUT_UNION),
    ]

"""
https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
UINT SendInput(
  [in] UINT    cInputs,
  [in] LPINPUT pInputs,
  [in] int     cbSize
);
"""

class InputSender:
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    def press_key(self, vk_code):
        """
        Press keys 
        """
        ki = KEYBDINPUT(
            wVk=vk_code,
            wScan=0,
            dwFlags=0,
            time=0,
            dwExtraInfo=0
        )
        inp = INPUT(type=INPUT_KEYBOARD, ki=ki)
        self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
        print(f"pressing key {vk_code}")


    def release_key(self, vk_code):
        """
        Release keys    
        """
        ki = KEYBDINPUT(
            wVk=vk_code,
            wScan=0,
            dwFlags=RELEASE,
            time=0,
            dwExtraInfo=0
        )
        inp = INPUT(type=INPUT_KEYBOARD, ki=ki)
        self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
        print(f"releasing key {vk_code}")

    def left_click_press(self):
        """
        Mouse left click press 
        """
        down = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["LEFTDOWN"], 0, 0)
        )
        
        self.user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
        print("left click press")
        
    def left_click_release(self):
        """
        Mouse right click release
        """
        up = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["LEFTUP"], 0, 0)
        )
        self.user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))
        print("left click release")

    def right_click_press(self):
        """
        Mouse right click press 
        """
        down = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["RIGHTDOWN"], 0, 0)
        )
        
        self.user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
        print("Right click pressed")
        
    def right_click_release(self):
        """
        Mouse right click release
        """
        up = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["RIGHTUP"], 0, 0)
        )
        self.user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))
        print("Right click release")

    def v_scroll(self, amount):
        """
        handle vertical scrolling
        amount = + for up
        amount = - for down
        """

        mi = MOUSEINPUT(
            dx=0,
            dy=0,
            mouseData=amount,
            dwFlags=MOUSE_FLAG["V_WHEEL"],
            time=0,
            dwExtraInfo=0
        )

        inp = INPUT(type=INPUT_MOUSE, mi=mi)
        self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
        print(f"horizontal scroll by {amount}")


    def h_scroll(self, amount):
        """
        handle horizontal scrolling 
        amount = + for right
        amount = - for left
        """
        mi = MOUSEINPUT(
            dx=0,
            dy=0,
            mouseData=amount,
            dwFlags=MOUSE_FLAG["H_WHEEL"],
            time=0,
            dwExtraInfo=0
        )
        inp = INPUT(type=INPUT_MOUSE, mi=mi)
        self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
        print(f"horizontal scroll by {amount}")

    def move_cursor(self, dx, dy):
        mi = MOUSEINPUT(
            dx,
            dy,
            0,
            MOUSE_FLAG["MOVE"],
            0,
            0
        )
        inp = INPUT(type=INPUT_MOUSE, mi=mi)
        self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
        print(f"Moving cursor by ( {dx}, {dy} )")
