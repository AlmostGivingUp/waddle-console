
import json 
from Core.maps.mouse_map import MouseMap 
from Core.maps.key_map import KeyMap 
from Core.maps.map import Map
from Util import pathfinder

import struct

class KeyState:
    def __init__(self):
        self.current = set()
        self.previous = set()

    def clear(self):
        """
        Clear out current set 
        """
        self.current.clear()

    def update(self):
        """
        Update previous set 
        """
        self.previous = self.current.copy()

    def set_pressed(self, key, pressed):
        """
        If this key is pressed, add it to current. 
        If it is no longer pressed, remove it from current 
        """
        if pressed:
            self.current.add(key)
        else:
            self.current.discard(key)

    @property
    def pressed(self):
        """
        Current has but not previous 
        """
        return self.current - self.previous

    @property
    def released(self):
        """
        Previous has but not current 
        """
        return self.previous - self.current

class InpEng:
    """
    Input Engine to unpack received data and translate into 
    hardware states to be interpreted and mapped 
    """
    # Button masks
    BUTTON1 = 0x01
    BUTTON2 = 0x02
    BUTTON3 = 0x04
    BUTTON4 = 0x08
    SCROLL_BUTTON = 0x10

    # Mode bits
    MOUSE_MODE = 0x02

    # Cursor
    CURSOR_GAIN = 15
    MAX_CURSOR_DIST = 100

    def __init__(self):

        # Init value = empty sets 
        self.keyboard = KeyState()
        self.mouse = KeyState()

        # Init value = False 
        self.is_mouse_on = False
        self.is_scroll_on = False
        self._scroll_prev = False

        # Init value = 0 
        self.joystick_x = 0
        self.joystick_y = 0
        self.mode_bits = 0
        self.button_bits = 0

    def unpack_data(self, data: list):
        """
        HID Report Layout

        int16 joystick_x
        int16 joystick_y
        uint8 mode
        uint8 buttons
        """

        joystick_x, joystick_y, mode_bits, button_bits = struct.unpack("<hhBB", bytes(data))
        return joystick_x, joystick_y, mode_bits, button_bits


    def update_data(self, data):
        """
        Unpacking data 
        """
        (
            self.joystick_x,
            self.joystick_y,
            self.mode_bits,
            self.button_bits
        ) = self.unpack_data(data)

        self.is_mouse_on = bool(self.mode_bits & self.MOUSE_MODE)
        self._update_scroll_toggle() 

    def _update_scroll_toggle(self):
        """
        Each press toggles scrolling on/off 
        """
        scroll_pressed = bool(
            self.button_bits &
            self.SCROLL_BUTTON
        )

        if scroll_pressed and not self._scroll_prev:
            # Toggle 
            self.is_scroll_on = not self.is_scroll_on
        # Remember last state 
        self._scroll_prev = scroll_pressed

    def update_keyboard_key(self, key, mask):
        """
        Update keyboards states 
        """
        self.keyboard.set_pressed(key, bool(self.button_bits & mask))


    def update_mouse_key(self, key, mask):
        """
        Update mouse states 
        """
        self.mouse.set_pressed(key, bool(self.button_bits & mask))

    def get_cursor_delta(self):
        """
        Getting cursor movements 
        """
        if not self.is_mouse_on:
            return 0, 0
        
        # Normalizing  
        dx = int(
            self.joystick_x / 2048.0 *
            self.CURSOR_GAIN
        )

        dy = int(
            self.joystick_y / 2048.0 *
            self.CURSOR_GAIN
        )

        # Boundary control 
        dx = max(
            -self.MAX_CURSOR_DIST,
            min(self.MAX_CURSOR_DIST, dx)
        )

        dy = max(
            -self.MAX_CURSOR_DIST,
            min(self.MAX_CURSOR_DIST, dy)
        )
        return dx, dy
    
    def commit(self):
        """
        Update changes (log into previous sets)
        """
        self.keyboard.update()
        self.mouse.update()

def get_mapping(): 
    """
    Loading keyboard and mouse selected configuration 
    """
    key_mapping = {}
    mouse_mapping = {} 
    ACTIVE_PATH = pathfinder.get_active_dir()
    acfg = ACTIVE_PATH / "Active_Config.json"
    mcfg =  ACTIVE_PATH / "Active_Mouse_Config.json"

    # KeyBoard
    try:
        print(f"{acfg} is found")
        with open(acfg, "r") as f:
            key_mapping = json.load(f)
    except: 
        print(f"{acfg} not found. Defaulting...\n")
        key_mapping = KeyMap().get_map()

    # Mouse 
    try: 
        print(f"{mcfg} found")
        with open(mcfg, "r") as f:
            mouse_mapping = json.load(f)
    except:
        print(f"{mcfg} not found. Defaulting...\n")
        mouse_mapping = MouseMap().get_map()

    return key_mapping, mouse_mapping