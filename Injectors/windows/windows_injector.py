from Injectors.input_engine import InpEng
from Injectors.windows.windows_input_sender import InputSender
from Constants.windows_const import VK, SCROLL
import json 
from Core.maps.mouse_map import MouseMap 
from Core.maps.key_map import KeyMap 
from Util import pathfinder

BUTTON_MASKS = {
    "BUTTON 1": InpEng.BUTTON1,
    "BUTTON 2": InpEng.BUTTON2,
    "BUTTON 3": InpEng.BUTTON3,
    "BUTTON 4": InpEng.BUTTON4,
}


class HIDProcessor:
    """
    Updating current hardware state
    """
    def __init__(self):
        self.input_engine = InpEng()
        self.key_map, self.mouse_map = self.get_mapping()
        
    def get_mapping(self): 
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

        print ("key mapping", key_mapping, "\n")
        print ("mouse mapping", mouse_mapping, "\n")

        return key_mapping, mouse_mapping

    def process_hid_report(self, data: list):
        """
        Main entry point.
        Called whenever a HID report arrives.
        """
        
        self.input_engine.update_data(data)

        if self.input_engine.is_mouse_on:
            # Handle scrolling/cursor/mouse-related keyboard presses
            self.update_mouse(self.mouse_map)
            self.handle_cursor()
            self.handle_scroll()
        else:
            self.update_keyboard()
            self.handle_joystick_keyboard()

    #------------------KeyBoard Mode--------------------#
    def update_keyboard(self):
        """
        Mapping keyboard-related keypress  
        """
        # getting updated hardware states 
        for button, mask in BUTTON_MASKS.items():
            self.input_engine.update_keyboard_key(
                button,
                mask
            )
        for button in self.input_engine.keyboard.pressed:
            mapped_key = self.key_map[button]
            InputSender.press_key(VK[mapped_key])

        for button in self.input_engine.keyboard.released:
            mapped_key = self.key_map[button]
            InputSender.release_key(VK[mapped_key])

        self.input_engine.keyboard.update()

    #-------------------Mouse Mode-------------------#
    def update_mouse(self, mouse_map):
        """
        Mapping mouse-related keypress 
        """
        for button, mask in BUTTON_MASKS.items():
            self.input_engine.update_mouse_key(
                button,
                mask
            )

        for button in self.input_engine.mouse.pressed:
            mapped_key = mouse_map[button]
            self._mouse_press(mapped_key)

        for button in self.input_engine.mouse.released:
            mapped_key = mouse_map[button]
            self._mouse_release(mapped_key)

        self.input_engine.mouse.update()


    def _mouse_press(self, mapped_key):
        """
        Handling clicks and normal key presses
        """
        if mapped_key == "LEFT":
            InputSender.left_click_press()

        elif mapped_key == "RIGHT":
            InputSender.right_click_press()

        else:
            InputSender.press_key(VK[mapped_key])

    def _mouse_release(self, mapped_key):
        """
        Handling clicks and normal key release
        """
        if mapped_key == "LEFT":
            InputSender.left_click_release()

        elif mapped_key == "RIGHT":
            InputSender.right_click_release()

        else:
            InputSender.release_key(VK[mapped_key])


    #-------------------Cursor-------------------#
    def handle_cursor(self):
        """
        Move cursor 
        """
        dx, dy = self.input_engine.get_cursor_delta()
        if dx != 0 or dy != 0: # Don't move if no reads from both
            InputSender.move_cursor(dx, dy)

    #-------------------Scroll-------------------#
    def handle_scroll(self):
        """
        Scroll page horizontally/vertically 
        """
        if not self.input_engine.is_scroll_on:
            return
        dx, dy = self.input_engine.get_cursor_delta()
        if dx:
            InputSender.h_scroll(dx * SCROLL)

        if dy:
            InputSender.v_scroll(dy * SCROLL)

    #-------------------Joystick Keyboard-------------------#

    def handle_joystick_keyboard(self):
        """
        Handling mapping joystick to keyboard key presses 
        """
        x = self.input_engine.joystick_x
        y = self.input_engine.joystick_y

        # X Axis
        left_key = self.key_map["JOYSTICK X-AXIS LEFT"]
        right_key = self.key_map["JOYSTICK X-AXIS RIGHT"]

        if x > 0:
            InputSender.release_key(VK[left_key])
            InputSender.press_key(VK[right_key])
        elif x <0:
            InputSender.release_key(VK[right_key])
            InputSender.press_key(VK[left_key])
        else: 
            InputSender.release_key(VK[left_key])
            InputSender.release_key(VK[right_key])

        # Y Axis
        up_key = self.key_map["JOYSTICK Y-AXIS UP"]
        down_key = self.key_map["JOYSTICK Y-AXIS DOWN"]

        if y > 0:
            InputSender.release_key(VK[down_key])
            InputSender.press_key(VK[up_key])
        elif y < 0:
            InputSender.release_key(VK[up_key])
            InputSender.press_key(VK[down_key])
        else:
            InputSender.release_key(VK[up_key])
            InputSender.release_key(VK[down_key])