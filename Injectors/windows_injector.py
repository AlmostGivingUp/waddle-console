import ctypes 
from ctypes import wintypes
from Constants.windows_const import VK, MOUSE_FLAG, SCROLL
from Util.mapping import get_mapping, InpEng

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
RELEASE = 0x0002
user32 = ctypes.WinDLL("user32", use_last_error=True)

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
        ("dwExtraInfo", wintypes.ULONG_PTR),
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
        ("dwExtraInfo", wintypes.ULONG_PTR),
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

def press_key(vk_code):
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
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def release_key(vk_code):
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
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def left_click_press():
    """
    Mouse left click press 
    """
    down = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["LEFTDOWN"], 0, 0)
    )
    
    user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
    
def left_click_release():
    """
    Mouse right click release
    """
    up = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["LEFTUP"], 0, 0)
    )
    user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))

def right_click_press():
    """
    Mouse right click press 
    """
    down = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["RIGHTDOWN"], 0, 0)
    )
    
    user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
    
def right_click_release():
    """
    Mouse right click release
    """
    up = INPUT(
        type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSE_FLAG["RIGHTUP"], 0, 0)
    )
    user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))

def v_scroll(amount):
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

    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def h_scroll(amount):
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
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def move_cursor(dx, dy):
    mi = MOUSEINPUT(
        dx,
        dy,
        0,
        MOUSE_FLAG["Move"],
        0,
        0
    )
    inp = INPUT(type=INPUT_MOUSE, mi=mi)
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

inp = InpEng()
key_map, mouse_map = get_mapping() 

def cursor_handler():
    """
    handle cursor movement
    """
    dx, dy = inp.check_cursor_movement()
    if dx or dy:
        move_cursor(dx, dy)
  
    
def knob_handler_keyb():
    """
    handle knob 
    """
    Y_mode = inp.check_Y_mode_on()
    if Y_mode:
        if inp.delta > 0: 
            release_key(VK[key_map["Knob Anti-Clockwise (Y)"]])
            press_key(VK[key_map["Knob Clockwise (Y)"]])
        if inp.delta < 0: 
            release_key(VK[key_map["Knob Clockwise (Y)"]])
            press_key(VK[key_map["Knob Anti-Clockwise (Y)"]])
        if inp.delta == 0:
            release_key(VK[key_map["Knob Clockwise (Y)"]])
            release_key(VK[key_map["Knob Anti-Clockwise (Y)"]])
    else:
        if inp.delta > 0: 
            release_key(VK[key_map["Knob Anti-Clockwise (X)"]])
            press_key(VK[key_map["Knob Clockwise (X)"]])
        if inp.delta < 0: 
            release_key(VK[key_map["Knob Clockwise (X)"]])
            press_key(VK[key_map["Knob Anti-Clockwise (X)"]])
        if inp.delta == 0:
            release_key(VK[key_map["Knob Clockwise (X)"]])
            release_key(VK[key_map["Knob Anti-Clockwise (X)"]])

def knob_handler_mouse():
    Y_mode = inp.check_Y_mode_on()
    if Y_mode:
        v_scroll(inp.delta * SCROLL) 
    else: 
        h_scroll(inp.delta * SCROLL)

def update_keyboard():
    inp.clear_cur()

    inp.update_cur_keys("Button 1", inp.button1)
    inp.update_cur_keys("Button 2", inp.button2)
    inp.update_cur_keys("Button 3", inp.button3)
    inp.update_cur_keys("Button 4", inp.button4)

    for key in inp.get_cur_diff_prev():
        press_key(VK[key_map[key]])

    for key in inp.get_prev_diff_cur():
        release_key(VK[key_map[key]])
    
    inp.update_prev() 
   
def update_mouse():
    inp.clear_cur()

    inp.update_cur_keys("Button 2", inp.button2)
    inp.update_mouse_cur_keys("Button 3", inp.button3)
    inp.update_mouse_cur_keys("Button 4", inp.button4)
     
    for key in inp.get_cur_diff_prev():
        press_key(VK[mouse_map[key]])

    for key in inp.get_prev_diff_cur():
        release_key(VK[mouse_map[key]])
    
    for key in inp.get_cur_diff_prev_mouse():
        if key == "Button 3":
            left_click_press()
        else:
            right_click_press()
        
    for key in inp.get_prev_diff_cur_mouse():
        if key == "Button 3":
            left_click_release()
        else:
            right_click_release()

    inp.update_prev()
    inp.update_mouse_prev()
    
def key_mapping(data: list):
    inp.update_data(data)
    mouse_on = inp.check_mouse_on()

    if mouse_on:
        update_mouse()
        if inp.check_cursor_mode_on():
            cursor_handler()
        else:
            knob_handler_mouse()
    else:
        update_keyboard()
        knob_handler_keyb()

