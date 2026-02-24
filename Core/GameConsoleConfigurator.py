import dearpygui.dearpygui as dpg # type: ignore
import json 
import platform 
from pathlib import Path 

# Key Mapping interface
INIT_WIDTH, INIT_HEIGHT = 800, 600
CHILD_WIDTH, CHILD_HEIGHT = 400, -1 # -1 fills to bottom
aspect_ratio = (INIT_HEIGHT / INIT_WIDTH) * 1.5 

BASE_DIR = Path(__file__).resolve().parent   # Console / Core   
PROJECT_ROOT = BASE_DIR.parent      # Console     
IMAGE_PATH = PROJECT_ROOT / "Assets" / "Console.png"
FONT_PATH = PROJECT_ROOT / "Assets" 
PROFILE_PATH = PROJECT_ROOT / "Profiles" 
ACTIVE_PATH = PROJECT_ROOT / "Injectors"

class MappingApp:
    def __init__(self):
        dpg.create_context()
        self.os = platform.system() 
        self.popup_open = False
        self.key_mapping = {
            "Button 1": "A",
            "Button 2" : "SHIFT",
            "Button 3": "ESC",
            "Button 4": "K", 
            
            "Knob Clockwise (X)" : "D",
            "Knob Anti-Clockwise (X)": "A",
            "Knob Clockwise (Y)" : "W",
            "Knob Anti-Clockwise (Y)": "S" 
        }

        self.mouse_mapping = {
            "Button 1": "Cursor Mode",
            "Button 2" : "SHIFT",
            
            "Button 3": "Left Click",
            "Button 4": "Right Click", 
        
            "Knob Clockwise (X)" : "Scroll Right",
            "Knob Anti-Clockwise (X)": "Scroll Left",
            "Knob Clockwise (Y)" : "Scroll Up",
            "Knob Anti-Clockwise (Y)": "Scroll Down" 
        }
        self.key_lookup = {
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
        self.current_config_mode = "Normal"
        self.current_selected_key = "Button 1"

        # Load Assets 
        width, height, channels, data = dpg.load_image(str(IMAGE_PATH))
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="Console_Img")
        #--------------------------Themes--------------------------
        with dpg.theme() as main_theme:
            """
            Preparing themes
            """
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (99, 99, 99), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 50, category=dpg.mvThemeCat_Core)

            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                
        
        #--------------------------Font--------------------------
        with dpg.font_registry():
            """
            Prepare fonts to be used
            """
            header_size = 35
            self.header_noname_bold = dpg.add_font(str(FONT_PATH / "NoName37-Bold.otf"), header_size)
            self.header_noname_light = dpg.add_font(str(FONT_PATH / "NoName37-Light.otf"), header_size)
            self.header_trueno_semibold_italic = dpg.add_font(str( FONT_PATH / "TruenoSemiboldItalic.otf"), header_size)
                    
            body_size = 20
            self.body_noname_bold = dpg.add_font(str(FONT_PATH / "NoName37-Bold.otf"), body_size)
            self.body_noname_light = dpg.add_font(str(FONT_PATH / "NoName37-Light.otf"), body_size)
            self.body_trueno_semibold_italic = dpg.add_font(str( FONT_PATH / "TruenoSemiboldItalic.otf"), body_size)
             
        # Layout
        with dpg.window(tag="Primary_Window") as Primary_Window:
            with dpg.group(horizontal=True) as group1:
                # --- LEFT SIDE (Horizontal Group)--- 
                #--------------------------Sidebar Child Window--------------------------
                with dpg.child_window(width=CHILD_WIDTH, height=CHILD_HEIGHT) as Profile_Manager:
                    with dpg.child_window(tag="Profile_Manager", height=CHILD_HEIGHT):
                        dpg.add_text("Profiles", color=(0, 255, 0))    
                        # Populate profile buttons                
                        self.profile_items() 

                    with dpg.child_window(tag="Instructions", width=-1, height=-1, pos=(0, INIT_HEIGHT)) as Instructions: 
                
                        dpg.add_text("Thanks for using Waddle Console! (^0^) " \
                        "Hint: Be aware the leftmost button is reserved for switching the knob to mouse click mode.",
                        wrap = 380)
                        
                        mode = "Mouse Configuration" if self.current_config_mode == "Normal" else "Normal"
                        dpg.add_button(
                            tag="mode_button", 
                            label=f"{mode}", 
                            width=-1,
                            callback=self.toggle_mode
                        )

                # --- RIGHT SIDE (Vertical Group) ---
                #--------------------------Canvas/Mapping Child Window--------------------------
                with dpg.child_window(tag="Console_Map", width=-1, height=-1) as Console_Map:
                    current_width = INIT_WIDTH * aspect_ratio
                    new_height = current_width * 0.5
                    dpg.add_spacer(height=50)
                    dpg.add_text("Visual Console Map", indent = 350, tag="Console_Map_Label")
                    dpg.add_text("Press Desired Key to Map", indent = 400, tag="Console_Map_Para")
                        
                    with dpg.drawlist(width=current_width, height=new_height, tag="Console_Diagram"):
                        """
                        Draw Game Console Diagram
                        """
                        dpg.draw_image("Console_Img", (100, 0), (current_width, new_height))
                        dpg.draw_circle((0, 0), 15, color=(255, 0, 0), 
                                tag="Hover_Indicator", show=False, thickness=20)
                    #--------------------------Config List--------------------------
                    with dpg.child_window(tag="Config_List", border=True, width=-1, height=-1) as Config_List:
                        """
                        Show table of current configuration
                        """ 
                        self.config_list() 
                    
                   
               #--------------------------Click--------------------------
                    with dpg.handler_registry():
                        """
                        Handle keyboard listening 
                        """
                        dpg.add_key_press_handler(callback=self.record_key_cb)
                    self.waiting_for_key = False

                    with dpg.item_handler_registry(tag="Config_Handler"):
                        """
                        Handle clicks on diagram
                        """
                        dpg.add_item_clicked_handler(callback=self.check_click_pos)
                    dpg.bind_item_handler_registry("Console_Diagram", "Config_Handler")
                dpg.bind_item_theme(Profile_Manager, main_theme)
                dpg.bind_item_theme(Console_Map, main_theme) 
                # Main Window Label 
                dpg.bind_font(self.header_noname_bold)
                dpg.bind_item_font("Console_Map_Label", self.header_noname_bold)
                dpg.bind_item_font("Console_Map_Para", self.body_noname_light)
               
        self._build_knob_popup()

        #--------------------------Boilerplate --------------------------
        dpg.create_viewport(title="Waddle Console", width=INIT_WIDTH, height=INIT_HEIGHT)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary_Window", True)
    
    def toggle_mode(self, sender, app_data, user_data):
        new_mode = "Mouse Configuration" if self.current_config_mode == "Normal" else "Normal"
        self.current_config_mode = new_mode
        next_label = "Normal" if new_mode == "Mouse Configuration" else "Mouse Configuration"
        dpg.configure_item("mode_button", label=f"{next_label}")
        if self.current_config_mode == "Normal": 
            for btn, key in self.key_mapping.items():
                tag = f"key_value_{btn}"
                if dpg.does_item_exist(tag):
                    dpg.set_value(tag, key)
        else:
            for btn, key in self.mouse_mapping.items():
                tag = f"key_value_{btn}"
                if dpg.does_item_exist(tag):
                    dpg.set_value(tag, key)
        self.profile_items()
                
        return next_label

    def check_click_pos(self):
        """
        Check current mouse position and turn on Keyboard listener
        """
        if not dpg.does_item_exist("Hover_Indicator"):
            return
        try:
            mouse_viewport_pos = dpg.get_mouse_pos(local=False)
            canvas_pos = dpg.get_item_pos("Console_Diagram")
            mouse_pos = [
                    mouse_viewport_pos[0] - canvas_pos[0],
                    mouse_viewport_pos[1] - canvas_pos[1]
                ]
            print(f"Manually Calculated Pos: {mouse_pos}")
            res, new_center = self.is_over_button(mouse_pos)
            if res:
                dpg.configure_item("Hover_Indicator", center=new_center, show=True)
            else:
                dpg.configure_item("Hover_Indicator", show=False)
        except EOFError:
            print(f"Potential crash")

    def is_over_button(self, pos):
        """
        Check if click is hovering within button area
        radius 30                      
        """
        
        radius = 30 
        if self.current_config_mode == "Normal":
            buttons = {
                "Button 1": [1122.0, 305.0],
                "Button 2": [1065.0, 349.0],
                "Button 3":  [1179.0, 349.0], 
                "Button 4": [1122.0, 400.0],
                "Knob":[744.0, 360.0]
            }
        else:
            buttons = {
                "Button 1": [1122.0, 305.0],
                "Button 2": [1065.0, 349.0],
            } 

        for name, center in buttons.items():
            dist = ((pos[0] - center[0])**2 + (pos[1] - center[1])**2)**0.5

            if dist < radius:
                if name == "Knob":
                    self.popup_open = True
                    self.waiting_for_key = False 
                    print("show popup")
                    dpg.show_item("Knob_Window")
                    dpg.set_value("knob_cw_x", self.key_mapping["Knob Clockwise (X)"])
                    dpg.set_value("knob_ccw_x", self.key_mapping["Knob Anti-Clockwise (X)"])
                    dpg.set_value("knob_cw_y", self.key_mapping["Knob Clockwise (Y)"])
                    dpg.set_value("knob_ccw_y", self.key_mapping["Knob Anti-Clockwise (Y)"])

                self.current_selected_key = name
                new_center = (center[0]-431, center[1]-140)
                print(f"new center: {new_center}")
                self.waiting_for_key = True 
                print(f"{name} is pressed")
                return True, new_center
            
        self.waiting_for_key = False 
        return False, (0,0)
        
    def record_key_cb(self, sender, key_code):
        """
        Listen to key press
        """
        if self.popup_open:
            return
        if self.waiting_for_key and self.current_selected_key != "Knob":   
            offset = 481
            # Stop waiting 
            self.waiting_for_key = False
            print("Listening for key,,,")
            # Convert key_code to string if on an os system (e.g., 65 -> "A")
            if (self.os == "Darwin"): 
                new_key_code = key_code - offset
                special_keys = {
                    45: "ESC",
                    44: "ENTER",
                    31: "TAB",
                    43: "BACKSPACE",
                    47: "SHIFT",
                    56: "1",
                    57: "2",
                    58: "3",
                    59: "4",
                    60: "5",
                    61: "6",
                    62: "7",
                    63: "8",
                    64: "9",
                    55: "0",
                    34: "UP", 
                    32: "LEFT",
                    35: "DOWN", 
                    33: "RIGHT"
                }
                if new_key_code not in special_keys.keys() and new_key_code != 174:
                    key_name = chr(new_key_code) 
                elif new_key_code in special_keys.keys() and new_key_code != 174: 
                    key_name = special_keys[new_key_code]
                elif key_code == 174:
                    key_name = dpg.get_value(f"key_value_{self.current_selected_key}")
            else: 
                key_name = self.key_lookup.get(key_code, self.key_mapping[self.current_selected_key])

            # Save the mapping
            if self.current_config_mode == "normal":
                self.key_mapping[self.current_selected_key] = key_name
                print(f"Mapped {self.current_selected_key} to {key_name} new {new_key_code if new_key_code else key_code}")
            else:
                self.mouse_mapping[self.current_selected_key] = key_name
            dpg.set_value(f"key_value_{self.current_selected_key}", key_name) 


    def _build_knob_popup(self):
        """
        Building a custom popup for knob configuration
        """
        print("pop up built")
        def save_knob():
            values = {
                "Knob Clockwise (X)": dpg.get_value("knob_cw_x"),
                "Knob Anti-Clockwise (X)": dpg.get_value("knob_ccw_x"),
                "Knob Clockwise (Y)": dpg.get_value("knob_cw_y"),
                "Knob Anti-Clockwise (Y)": dpg.get_value("knob_ccw_y"),
            }

            for btn, val in values.items():
                self.key_mapping[btn] = val
                dpg.set_value(f"key_value_{btn}", val)

            self.popup_open = False
            print("Config saved")
            dpg.hide_item("Knob_Window")

        def close_knob():
            self.popup_open = False
            print("pop up closed")
            dpg.hide_item("Knob_Window")

        with dpg.window(
            tag="Knob_Window",
            label="Configure Knob",
            modal=True,
            show=False,
            width=1000,
            height=300,
            no_move=False,
            no_resize=False,
            on_close=close_knob
        ):
            dpg.add_input_text(tag="knob_cw_x", label="Knob Clockwise (X)")
            dpg.add_input_text(tag="knob_ccw_x", label="Knob Anti-Clockwise (X)")
            dpg.add_input_text(tag="knob_cw_y", label="Knob Clockwise (Y)")
            dpg.add_input_text(tag="knob_ccw_y", label="Knob Anti-Clockwise (Y)")
            dpg.add_spacer(height=10)
            dpg.add_button(label="Save", callback=save_knob)
            
    def profile_items(self):
        """
        List out profile items
        """
        dpg.delete_item("Profile_Manager", children_only=True)
        dpg.add_text("Profiles", parent="Profile_Manager", color=(0, 255, 0), tag="Profile_Label")
        
        script_dir = Path(__file__).parent
        suffix = "_Mouse.json" if self.current_config_mode != "Normal" else ".json"
        
        for file_path in script_dir.glob("*.json"):
            if "Active_" in file_path.name: continue
            
            is_mouse_file = file_path.name.endswith("_Mouse.json")
            
            if (self.current_config_mode == "Normal" and not is_mouse_file) or \
            (self.current_config_mode != "Normal" and is_mouse_file):
                
                profile_name = file_path.stem
                dpg.add_button(
                    label=profile_name, 
                    parent="Profile_Manager",
                    width=-1,
                    callback=self.load_config,
                    user_data=profile_name
                )
            
            dpg.bind_item_font("Profile_Manager", self.body_noname_light)
            dpg.bind_item_font("Profile_Label", self.header_noname_bold)

    def mouse_config_list(self):
        """
        Show a list of current configuration
        """
    
        dpg.add_input_text(label="Profile Name", default_value="Mouse_Config", 
            tag="Profile_Name", parent="Config_List")
                
        with dpg.table(header_row=True, tag="Mapping_Table", parent="Config_List", 
            borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                
            # Define Columns
            dpg.add_table_column(label="Hardware Button")
            dpg.add_table_column(label="Keyboard Map")

            # Fill Rows
            for btn, key in self.mouse_mapping.items():
                with dpg.table_row():
                    dpg.add_text(btn, color = (128, 128, 128)) # Green for button name
                    dpg.add_text(key, color = (255, 255, 255), tag=f"key_value_{btn}") # White for key
                
        dpg.add_spacer(height=20, parent="Config_List")
        dpg.add_button(
                    label="Save and Apply",
                    parent="Config_List",
                    callback=self.save_config,
                    tag = "Save_Button",
                    height = 40,
                    width = -1
                )
        
        dpg.bind_item_font("Save_Button", self.body_noname_light)
        dpg.bind_item_font("Mapping_Table", self.body_noname_bold)

                    
    
    def config_list(self):
        """
        Show a list of current configuration
        """
    
        dpg.add_input_text(label="Profile Name", default_value="Untitled", 
            tag="Profile_Name", parent="Config_List")
                
        with dpg.table(header_row=True, tag="Mapping_Table", parent="Config_List", 
            borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                
            # Define Columns
            dpg.add_table_column(label="Hardware Button")
            dpg.add_table_column(label="Keyboard Map")

            # Fill Rows
            for btn, key in self.key_mapping.items():
                with dpg.table_row():
                    dpg.add_text(btn, color = (128, 128, 128)) # Green for button name
                    dpg.add_text(key, color = (255, 255, 255), tag=f"key_value_{btn}") # White for key
                
        dpg.add_spacer(height=20, parent="Config_List")
        dpg.add_button(
                    label="Save and Apply",
                    parent="Config_List",
                    callback=self.save_config,
                    tag = "Save_Button",
                    height = 40,
                    width = -1
                )
        
        dpg.bind_item_font("Save_Button", self.body_noname_light)
        dpg.bind_item_font("Mapping_Table", self.body_noname_bold)

    def save_config(self):
        """
        Save and Apply current configuration
        """
        profile_name = dpg.get_value("Profile_Name")
        
        filename = PROFILE_PATH / f"{profile_name}_Mouse.json" if self.current_config_mode == "Mouse Configuration" and not profile_name.endswith("_Mouse.json") else f"{profile_name}.json"
        active_configs = ACTIVE_PATH / "Active_Config.json"
        active_mouse_configs = ACTIVE_PATH / "Active_Mouse_Config.json"
        #Save Data
        
        if self.current_config_mode == "Normal":
        #Send Data to Processing Backend (Apply)
            with open(filename, 'w') as f:
                json.dump(self.key_mapping, f, indent=4)

            with open(active_configs, 'w') as f:
                json.dump(self.key_mapping, f, indent=4)
        else: 
            with open(filename, 'w') as f:
                json.dump(self.mouse_mapping, f, indent=4)

            with open(active_mouse_configs, 'w') as f:
                json.dump(self.mouse_mapping, f, indent=4)
        
        print(f"Saved to {filename}")
        self.profile_items()

    def load_config(self, sender, app_data, user_data):
        """
        Load chosen configuration
        """
        print(f"User data: {user_data}")
        profile_name = user_data
        filename = PROFILE_PATH / f"{profile_name}.json"
        with open(filename, "r") as f:
            data = json.load(f)
        self.key_mapping = data
        if dpg.does_item_exist("Profile_Name"):
            dpg.set_value("Profile_Name", profile_name)
        for btn, key in self.key_mapping.items():
            tag = f"key_value_{btn}"
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, key)
        print(f"Loading: {profile_name}")
    

            
def start_configurator():
    app = MappingApp()
    dpg.start_dearpygui() 
    dpg.destroy_context()
    return True
