from Core.maps.map import Map

class KeyMap(Map):
    """
    Stores keyboard mappings for buttons and joystick directions.
    """
    def __init__(self):
        """
        Initial state
        """
        super().__init__()
        # Buttons 1-4
        self.buttons = {
            "BUTTON 1": 'W',
            "BUTTON 2": 'D',
            "BUTTON 3": 'S',
            "BUTTON 4": 'A'
        }
        # Joystick directions
        self.joysticks = {
            "JOYSTICK X-AXIS LEFT": 'LEFT',
            "JOYSTICK X-AXIS RIGHT": 'RIGHT',
            "JOYSTICK Y-AXIS UP": 'UP',
            "JOYSTICK Y-AXIS DOWN": 'DOWN',
            "JOYSTICK SWITCH": 'SHIFT'
        }

    def __repr__(self):
        """
        String representation
        """
        return (
            f"KeyMap("
            f"buttons={self.buttons}, "
            f"joysticks={self.joysticks})"
        )