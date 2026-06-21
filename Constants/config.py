import dearpygui.dearpygui as dpg
from Util import pathfinder

INIT_WIDTH, INIT_HEIGHT = 800, 600
CHILD_WIDTH, CHILD_HEIGHT = 400, -1
aspect_ratio = (INIT_HEIGHT / INIT_WIDTH) * 1.5
IMAGE_PATH = pathfinder.get_resource_path("Assets/Console.png")
FONT_PATH = pathfinder.get_resource_path("Assets")
PROFILE_PATH = pathfinder.get_profiles_dir()
ACTIVE_PATH = pathfinder.get_active_dir()

BUTTON_LAYOUT_KEYBOARD = {
    "BUTTON 1": [1122.0, 305.0],
    "BUTTON 2": [1179.0, 349.0], 
    "BUTTON 3":  [1065.0, 349.0],
    "BUTTON 4": [1122.0, 400.0],
    "JOYSTICK":[744.0, 360.0]
}

BUTTON_LAYOUT_MOUSE = {
  "BUTTON 1": [1122.0, 305.0],
  "BUTTON 3":[1179.0, 349.0], 
}

JOYSTICK_FIELDS = {
    "RX": "Joystick X-axis Right",
    "LX": "Joystick X-axis Left",
    "UY": "Joystick Y-axis Up",
    "DY": "Joystick Y-axis Down",
    "SW": "Joystick Switch"
}

key_lookup = {
    dpg.mvKey_A: "A",
    dpg.mvKey_B: "B",
    dpg.mvKey_C: "C",
    dpg.mvKey_D: "D",
    dpg.mvKey_E: "E",
    dpg.mvKey_F: "F",
    dpg.mvKey_G: "G",
    dpg.mvKey_H: "H",
    dpg.mvKey_I: "I",
    dpg.mvKey_J: "J",
    dpg.mvKey_K: "K",
    dpg.mvKey_L: "L",
    dpg.mvKey_M: "M",
    dpg.mvKey_N: "N",
    dpg.mvKey_O: "O",
    dpg.mvKey_P: "P",
    dpg.mvKey_Q: "Q",
    dpg.mvKey_R: "R",
    dpg.mvKey_S: "S",
    dpg.mvKey_T: "T",
    dpg.mvKey_U: "U",
    dpg.mvKey_V: "V",
    dpg.mvKey_W: "W",
    dpg.mvKey_X: "X",
    dpg.mvKey_Y: "Y",
    dpg.mvKey_Z: "Z",

    dpg.mvKey_0: "0",
    dpg.mvKey_1: "1",
    dpg.mvKey_2: "2",
    dpg.mvKey_3: "3",
    dpg.mvKey_4: "4",
    dpg.mvKey_5: "5",
    dpg.mvKey_6: "6",
    dpg.mvKey_7: "7",
    dpg.mvKey_8: "8",
    dpg.mvKey_9: "9",

    dpg.mvKey_Escape: "ESC",
    dpg.mvKey_Return: "ENTER",
    dpg.mvKey_Tab: "TAB",
    dpg.mvKey_Back: "BACKSPACE",
    dpg.mvKey_LShift: "SHIFT",
    dpg.mvKey_RShift: "SHIFT",
    dpg.mvKey_LControl: "CTRL",
    dpg.mvKey_RControl: "CTRL",
    dpg.mvKey_Spacebar: "SPACE",
    dpg.mvKey_Left: "LEFT",
    dpg.mvKey_Right: "RIGHT",
    dpg.mvKey_Up: "UP",
    dpg.mvKey_Down: "DOWN",
  }