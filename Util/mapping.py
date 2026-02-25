
import json 
import struct
import tkinter as tk
from tkinter import messagebox

_title = "Waddle Console"

_root = None

def show_popup(message, opt):
    global _root

    if _root is None:
        _root = tk.Tk()
        _root.withdraw()

    match opt:
        case 0:
            return messagebox.showinfo(_title, message)
        case 1:
            return messagebox.askokcancel(_title, message)

def unpack_data(data: list):
    """
    Unpack HID report data
    """
    data = bytes(data)
    mode_bits = data[2]
    buttons_bits = data[3]
    delta = struct.unpack('<h', data[0:2])[0]
    return mode_bits, buttons_bits, delta

class InpEng:
    """
    Class to handle common input vars 
    """
    # Defines 
    button1 = 0x01
    button2 = 0x02
    button3 = 0x04
    button4 = 0x08
    _mouse_on = 0x02
    _Y_mode_on = 0x01
    
    #Cursor
    _CURSOR_GAIN = 10
    _MAX_CURSOR_DIST = 100 
    
    def __init__(self):
        """
        initialise sets and delta acc
        """
        self.current_keys = set()
        self.previous_keys = set()
        self.mouse_current_keys = set()
        self.mouse_previous_keys = set()

        #Cursor
        self._velocity = 0
        self.is_cursor_mode_on = False

    def update_data(self, data):
        """
        update class vars through data unpacking 
        """
        self._mode_bits, self._buttons_bits, self.delta = unpack_data(data)
        self.is_Y_mode_on = bool(self._mode_bits & self._Y_mode_on)
        self.is_mouse_on = bool(self._mode_bits & self._mouse_on)
        self.is_cursor_mode_on = bool(self.is_cursor_mode_on ^ (self._buttons_bits & self.button1))
        
    def clear_cur(self):
        """
        clean up current related sets 
        """
        self.current_keys.clear()
        self.mouse_current_keys.clear()

    def update_cur_keys(self, key, mask):
        """
        update current keys set 
        """
        assert self._buttons_bits is not None 
        self.current_keys.add(key) if self._buttons_bits & mask else self.current_keys.discard(key)

    def update_mouse_cur_keys(self, key, mask):
        """
        update mouse current keys set 
        """
        assert self._buttons_bits is not None
        self.mouse_current_keys.add(key) if self._buttons_bits & mask else self.mouse_current_keys.discard(key) 
    
    def check_mouse_on(self) -> bool:
        """
        check if mouse mode is on
        """
        assert self.is_mouse_on is not None 
        return self.is_mouse_on
    
    def check_Y_mode_on(self) -> bool:
        """
        check if Y mode is on 
        """
        assert self.is_Y_mode_on is not None
        return self.is_Y_mode_on
    
    def check_cursor_mode_on(self)->bool:
        assert self.is_cursor_mode_on is not None
        return self.is_cursor_mode_on 
    
    def check_cursor_movement(self):
        """
        provide cursor movement
        """
        #grab delta's sign 
        
        if not self.is_cursor_mode_on:
            # clear velocity 
            self._velocity = 0
            return 0,0
        if self.delta:
            sign = 1 * self.delta / self.delta 
            self._velocity = (0.6 * self._velocity + self.delta) * sign
        else:
            self._velocity *= 0.4
        movement = int(self._velocity * self._CURSOR_GAIN)
        movement = max(-self._MAX_CURSOR_DIST, min(self._MAX_CURSOR_DIST, movement))

        if self.is_Y_mode_on:
            dy = movement
            dx = 0
        else: 
            dx = movement
            dy = 0
        
        return dx, dy
        

    def update_prev(self):
        """
        update prev keys set 
        """
        self.previous_keys = self.current_keys.copy()
    
    def update_mouse_prev(self):
        """
        update mouse prev keys set
        """
        self.mouse_previous_keys = self.mouse_current_keys.copy()
    
    def get_prev_diff_cur(self):
        """
        prev/cur
        """
        return self.previous_keys - self.current_keys
    
    def get_cur_diff_prev(self):
        """
        cur/prev
        """
        return self.current_keys - self.previous_keys
    
    def get_prev_diff_cur_mouse(self):
        """
        mouse_prev / mouse_cur
        """
        return self.mouse_previous_keys - self.mouse_current_keys
    
    def get_cur_diff_prev_mouse(self):
        """
        mouse_cur / mouse_prev
        """
        return self.mouse_current_keys - self.mouse_previous_keys


def get_mapping(): 
    """
    Loading keyboard and mouse selected configuration 
    """
    key_mapping = {}
    mouse_mapping = {} 
    acfg =  "Active_Config.json"
    mcfg =  "Active_Mouse_Config.json"
    try:
        with open(acfg, "r") as f:
            key_mapping = json.load(f)
    except: 
        print(f"{acfg} not found. Defaulting...\n")
        key_mapping = {
            
            "Button 1": "A",
            "Button 2" : "SHIFT",
            "Button 3": "ESC",
            "Button 4": "K", 
            
            "Knob Clockwise (X)" : "D",
            "Knob Anti-Clockwise (X)": "A",
            "Knob Clockwise (Y)" : "W",
            "Knob Anti-Clockwise (Y)": "S" 
        
        }
    try: 
        with open(mcfg, "r") as f:
            mouse_mapping = json.load(f)
    except:
        print(f"{mcfg} not found. Defaulting...\n")

        mouse_mapping = {
            "Button 1": "Cursor Mode",
            "Button 2" : "SHIFT",
            "Button 3": "Left Click",
            "Button 4": "Right Click", 
        
            "Knob Clockwise (X)" : "Scroll Right",
            "Knob Anti-Clockwise (X)": "Scroll Left",
            "Knob Clockwise (Y)" : "Scroll Up",
            "Knob Anti-Clockwise (Y)": "Scroll Down" 
        }
    return key_mapping, mouse_mapping