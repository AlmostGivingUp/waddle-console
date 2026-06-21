import dearpygui.dearpygui as dpg # type: ignore
from Core.maps.map import Map
from Core.game_console_interpreter import connecting_and_read
import threading
import queue  
import platform

from Core.maps.key_map import KeyMap
from Core.maps.mouse_map import MouseMap 
from Core.profile_manager import ProfileManager
from Constants.config import * 
from Constants.enum import * 


class MappingApp:
    
    def __init__(self):
        """
        Initialising the mapping app. 
        """
        dpg.create_context()
        
        self.event_queue = queue.Queue()
        self.os = platform.system() 
        self.popup_open = False

        # Mappings 
        self.key_mapping = KeyMap() 
        self.mouse_mapping = MouseMap() 
        self.profile_manager = ProfileManager(PROFILE_PATH, ACTIVE_PATH) 
        self.current_config_mode = ConfigMode.KEYBOARD  
        self.current_input_state = InputState.IDLE 
        self.capture_origin = None 
        self.current_selected_key = None

        #--------------------------Assets-------------------------- 
        width, height, channels, data = dpg.load_image(str(IMAGE_PATH))
        with dpg.texture_registry(show=False):
            """
            Loading Console Image 
            """
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="Console_Img")
       
       
       #--------------------------Themes--------------------------#
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
        
        #--------------------------Font--------------------------#
        with dpg.font_registry():
            """
            Prepare fonts to be used
            """
            with dpg.font(str(FONT_PATH / "fa-solid-900.ttf"), 18) as icon_font:
                dpg.add_font_range(0xf000, 0xf8ff)
            self.icon_font = icon_font

            header_size = 35
            self.header_noname_bold = dpg.add_font(str(FONT_PATH / "NoName37-Bold.otf"), header_size)
            self.header_noname_light = dpg.add_font(str(FONT_PATH / "NoName37-Light.otf"), header_size)
            self.header_trueno_semibold_italic = dpg.add_font(str( FONT_PATH / "TruenoSemiboldItalic.otf"), header_size)
                    
            body_size = 20
            self.body_noname_bold = dpg.add_font(str(FONT_PATH / "NoName37-Bold.otf"), body_size)
            self.body_noname_light = dpg.add_font(str(FONT_PATH / "NoName37-Light.otf"), body_size)
            self.body_trueno_semibold_italic = dpg.add_font(str( FONT_PATH / "TruenoSemiboldItalic.otf"), body_size)
             
        # Layout
        with dpg.window(tag="Primary_Window"):

            with dpg.group(horizontal=True):
                # --- LEFT SIDE (Horizontal Group)---#
                #--------------------------Sidebar Child Window------------------------#
                with dpg.child_window(width=CHILD_WIDTH, height=CHILD_HEIGHT) as Profile_Manager:
                    with dpg.child_window(tag="Profile_Manager", height=CHILD_HEIGHT):
                        dpg.add_text("Profiles", color=(0, 255, 0))    
                        # Populate profile buttons                
                        self.profile_items() 

                    with dpg.child_window(tag="Instructions", width=-1, height=-1, pos=(0, INIT_HEIGHT)) as Instructions: 
                        dpg.add_text("Thanks for using Waddle Console! (^0^) " \
                        "Hint: Be aware the leftmost button is reserved for switching the knob to mouse click mode.",
                        wrap = 380)
                        mode = self.current_mode_name
                        dpg.add_button(
                            tag="Mode_Button", 
                            label=f"{mode}", 
                            width=-1,
                            callback=self.toggle_mode
                        )

                # --- RIGHT SIDE (Vertical Group) --- #
                #--------------------------Canvas/Mapping Child Window--------------------------
                with dpg.child_window(tag="Console_Map", width=-1, height=-1) as Console_Map:
                    current_width = INIT_WIDTH * aspect_ratio
                    new_height = current_width * 0.5
                    dpg.add_spacer(height=50)
                    dpg.add_text("Visual Console Map", indent = 350, tag="Console_Map_Label")
                    dpg.add_text("Press Desired Key to Map", indent = 400, tag="Console_Map_Para")
                        
                    
                    #--------------------------Console Diagram--------------------------#
                    with dpg.drawlist(width=current_width, height=new_height, tag="Console_Diagram"):
                        """
                        Draw Game Console Diagram
                        """
                        dpg.draw_image("Console_Img", (100, 0), (current_width, new_height))
                        dpg.draw_circle((0, 0), 15, color=(255, 0, 0), 
                                tag="Hover_Indicator", show=False, thickness=20)
                    
                    
                    
                    #--------------------------Config List--------------------------#
                    with dpg.child_window(tag="Config_List", border=True, width=-1, height=-1) as Config_List:
                        """
                        Show table of current configuration
                        """ 
                        self.build_config_table() 
                    
                   
                    #--------------------------KeyBoard Listening-------------------------#
                    with dpg.handler_registry():
                        """
                        Handle keyboard listening 
                        """
                        dpg.add_key_press_handler(callback=self.record_key_cb)

                    #--------------------------Click Listening--------------------------#
                    with dpg.item_handler_registry(tag="Config_Handler"):
                        """
                        Handle clicks on diagram
                        """
                        dpg.add_item_clicked_handler(callback=self.check_cursor_position)
                    dpg.bind_item_handler_registry("Console_Diagram", "Config_Handler")
                
                
                dpg.bind_item_theme(Profile_Manager, main_theme)
                dpg.bind_item_theme(Console_Map, main_theme) 
                # Main Window Label 
                dpg.bind_font(self.header_noname_bold)
                dpg.bind_item_font("Console_Map_Label", self.header_noname_bold)
                dpg.bind_item_font("Console_Map_Para", self.body_noname_light)
        
        #--------------------------Joystick Popup --------------------------#
        self.build_joystick_popup()
        #self._build_error_popup()

        #--------------------------Boilerplate --------------------------#
        dpg.create_viewport(title="Waddle Console", width=INIT_WIDTH, height=INIT_HEIGHT)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary_Window", True)
        dpg.set_frame_callback(1, self._poll_events)
        """
        threading.Thread(
            target=connecting_and_read,
            args=(self.event_queue,),
            daemon=True
        ).start()
        """

    #--------------------Dynamic Mapping----------------------------------#
    @property
    def current_mapping(self) -> Map:
        """
        Getter for current mapping (used as dynamic attribute)
        """
        return (
            self.key_mapping
            if self.current_config_mode == ConfigMode.KEYBOARD
            else self.mouse_mapping
        )

    @current_mapping.setter
    def current_mapping(self, value: Map):
        """
        Setter for current mapping (used as dynamic attribute)
        """
        if self.current_config_mode == ConfigMode.KEYBOARD:
            self.key_mapping = value
        else:
            self.mouse_mapping = value

    @property
    def current_layout(self) -> dict:
        return (
            BUTTON_LAYOUT_KEYBOARD
            if self.current_config_mode == ConfigMode.KEYBOARD
            else BUTTON_LAYOUT_MOUSE
        )

    @property
    def current_mode_name(self):
        return (
            "Mouse Configuration"
            if self.current_config_mode == ConfigMode.MOUSE
            else "KeyBoard Configuration"
        )

    #----------------USB Connection Popup----------------#

    def _build_error_popup(self):
            """
            Building Popup 
            """
            with dpg.window(
                tag="Pop_Up_Window",
                modal=True,
                show=False,
                no_close=True,
                width=400,
                height=150
            ):
                dpg.add_text("", tag="Pop_Up", wrap=350)
                dpg.add_spacer(height=10)
                dpg.add_button(label="OK", callback=lambda: dpg.hide_item("Pop_Up_Window"))

    def _poll_events(self, sender, app_data):
        while not self.event_queue.empty():
            event_type, message = self.event_queue.get()
            if event_type == "Error" or event_type == "Success":
                dpg.set_value("Pop_Up", message)
                dpg.show_item("Pop_Up_Window")
        # Keep polling every frame
        dpg.set_frame_callback(dpg.get_frame_count() + 1, self._poll_events)


    #--------------------Joystick Popup----------------------------------#
    def set_input_state(self, input_state: InputState):
        """
        Popup and input state are coupled 
        """
        self.current_input_state = input_state 
        self.popup_open = (input_state == InputState.JOYSTICK_CONFIG)

    def build_joystick_popup(self):
        """
        Building a custom popup for Joystick configuration
        """
        print("pop up built")
        with dpg.window(
            tag="Joystick_Window",
            label="Configure Joystick",
            modal=True,
            show=False,
            width=1000,
            height=300,
            no_move=False,
            no_resize=False,
            on_close=self.close_joystick_popup
        ):
            for mapping_key in JOYSTICK_FIELDS.values():
                with dpg.group(horizontal=True):
                    dpg.add_text(mapping_key)
                    dpg.add_button(
                        tag=f"joy_btn_{mapping_key}",
                        label="",
                        width=200,
                        callback=self.start_joystick_capture,
                        user_data=mapping_key
                    )
            dpg.add_spacer(height=10)
            dpg.add_button(label="Close", callback=self.close_joystick_popup)

    def close_joystick_popup(self, sender=None, app_data=None, user_data=None):
        """
        Closing the popup using the 'x' button 
        """
        # Back to idle 
        self.set_input_state(InputState.IDLE) 
        self.refresh_mapping_table()
        dpg.hide_item("Joystick_Window")
        print("Joystick configuration saved")

    def load_joystick_popup(self, sender=None, app_data=None, user_data=None):
        """
        Populate joystick popup fields from current mapping.
        """
        for mapping_key in JOYSTICK_FIELDS.values():
            dpg.set_item_label(
                f"joy_btn_{mapping_key}",
                self.current_mapping[mapping_key]
            )
        self.set_input_state(InputState.JOYSTICK_CONFIG)
        dpg.show_item("Joystick_Window")
    
    def start_joystick_capture(self, sender, app_data, user_data):
        """
        Start capturing current key 
        """
        self.capture_origin = "joystick"
        self.current_selected_key = user_data
        self.set_input_state(InputState.WAITING_FOR_KEY)
        print(f"Waiting for key for {user_data}")

    #---------------------------Key Listener------------------------------#
    
    def check_cursor_position(self):
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
        RADIUS = 30 
        X_DIFF = 431
        Y_DIFF = 140 
        
        layout = self.current_layout  
        for name, center in layout.items():
            new_center = (center[0]-X_DIFF, center[1]-Y_DIFF)
            dist = ((pos[0] - center[0])**2 + (pos[1] - center[1])**2)**0.5
            if dist < RADIUS:
                if name == "Joystick":
                    self.load_joystick_popup()
                    return True, (new_center)
                
                self.capture_origin = "BUTTON"
                self.current_selected_key = name
                self.set_input_state(InputState.WAITING_FOR_KEY)
                return True, new_center
        
        return False, (0,0)
        
    def record_key_cb(self, sender, key_code):
        """
        Listen to key press.
        """

        if (self.current_input_state != InputState.WAITING_FOR_KEY):
            return
        print("Listening for key...")

        key_name = key_lookup.get(
            key_code,
            self.current_mapping[self.current_selected_key]
        )
        self.current_mapping[self.current_selected_key] = key_name
        # Joystick popup 
        if self.capture_origin == "JOYSTICK":
            dpg.set_item_label(
                f"joy_btn_{self.current_selected_key}",
                key_name
            )
            self.set_input_state(InputState.JOYSTICK_CONFIG)
        # Normal button
        else:
            dpg.set_value(
                f"key_value_{self.current_selected_key}",
                key_name
            )
            self.set_input_state(InputState.IDLE)
            # Clearing 
            self.current_selected_key = None

    #--------------------Configuration table UI----------------------------------#
    def toggle_mode(self, sender, app_data, user_data):
        """"
        Allow the user to toggle the mode from Mouse to KeyBoard configuration
        or vice versa 
        """
        if self.current_config_mode == ConfigMode.KEYBOARD:
            self.current_config_mode = ConfigMode.MOUSE
        else:
            self.current_config_mode = ConfigMode.KEYBOARD
        dpg.configure_item(
            "Mode_Button",
            label=self.current_mode_name
        )
        self.refresh_mapping_table()
        self.profile_items()

    #--------------------Configuration table UI----------------------------------#
    def build_config_table(self):
        """
        Building a configuration table in UI 
        """
        dpg.add_input_text(
            label="Profile Name",
            default_value="Untitled",
            tag="Profile_Name",
            parent="Config_List"
        )

        with dpg.table(
            header_row=True,
            tag="Mapping_Table",
            parent="Config_List",
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True
        ):
            dpg.add_table_column(label="Hardware Button")
            dpg.add_table_column(label="Keyboard Map")
            for btn, key in self.current_mapping.get_map().items():
                with dpg.table_row():
                    dpg.add_text(btn, color=(128,128,128))
                    dpg.add_text(key,
                        color=(255,255,255),
                        tag=f"key_value_{btn}")
        dpg.add_button(label="Save", callback=self.save_config)
    
    def refresh_mapping_table(self):
        """
        Refreshing a the configuration table in UI 
        by resetting the value 
        """
        for btn, key in self.current_mapping.get_map().items():
            tag = f"key_value_{btn}"
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, key)
                continue 
            
            tag = f"joy_btn_{btn}"
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, key)
                continue 



    #--------------------Profile Management----------------------------------#
            
    def profile_items(self):
        """
        List out profile items
        """
        dpg.delete_item("Profile_Manager", children_only=True)
        dpg.add_text("Profiles", parent="Profile_Manager", color=(0, 255, 0), tag="Profile_Label")
        profiles = self.profile_manager.list_profiles(self.current_config_mode) 
        for profile in profiles:  
            with dpg.group(horizontal=True, parent="Profile_Manager"):
                # Load Button
                dpg.add_button(
                    label=profile,
                    width=200,
                    callback=self.load_config,
                    user_data=profile
                )
                # Delete Button
                delete_btn = dpg.add_button(
                    label="\uf2ed",  
                    width=35,
                    callback= self.delete_config,
                    user_data=profile,
                )
                dpg.bind_item_font(delete_btn, self.icon_font)

        dpg.bind_item_font("Profile_Manager", self.body_noname_light)
        dpg.bind_item_font("Profile_Label", self.header_noname_bold)
    
    def load_config(self, sender, app_data, user_data):
        """
        Load a configuration map 
        """
        self.current_mapping = self.profile_manager.load_profile(
            user_data,
            self.current_config_mode
        )
        self.refresh_mapping_table() 

    def save_config(self, sender, app_data, user_data):
        """
        Save a configuration map 
        """
        profile_name = dpg.get_value("Profile_Name")
        self.profile_manager.save_profile(
            profile_name,
            self.current_config_mode,
            self.current_mapping
        )
        # Refresh profile items 
        self.profile_items() 
    
    def delete_config(self, sender, app_data, user_data):
        """
        Delete a configuration map 
        """
        self.profile_manager.delete_profile(user_data)
        #Refresh profile items 
        self.profile_items()
