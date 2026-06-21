from Core.maps.map import Map 

class MouseMap(Map):
    """
    Stores mouse-mode mappings for buttons and joystick directions.
    """
    def __init__(self):
        super().__init__()
        self.buttons = {
            "BUTTON 1": 'W',
            "BUTTON 2": 'RIGHT',
            "BUTTON 3": 'D',
            "BUTTON 4": 'LEFT'
        }

        self.joysticks = {
            'JOYSTICK X-AXIS LEFT': 'LEFT',
            'JOYSTICK X-AXIS RIGHT': 'RIGHT',
            'JOYSTICK Y-AXIS UP': 'UP',
            'JOYSTICK Y-AXIS DOWN': 'DOWN',
            'JOYSTICK SWITCH': 'V/H-SCROLL'
        }


    def __setitem__(self, key, value):
        """
        Setting item (Unable to set joysticks in mouse mode)
        Button 2 -> reserved for right click 
        Button 4 -> reserved for left click 
        Joystick Switch -> reserved for horizontal / vertical scrolling 
        """
        key = key.upper() 
        if key in ("BUTTON 1", "BUTTON 3"):
            self.buttons[key] = value
        else:
            raise KeyError(key)


    def __repr__(self):
        """
        String representation
        """
        return (
            f"MouseMap("
            f"buttons={self.buttons}, "
            f"joysticks={self.joysticks})"
        )