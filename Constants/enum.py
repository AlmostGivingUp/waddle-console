

from enum import Enum

class ConfigMode(Enum):
    """
    Allow choosing of which configuration 
    """
    KEYBOARD = 1
    MOUSE = 2


class InputState(Enum):
    """
    For Keylistener state 
    """
    IDLE = 0
    WAITING_FOR_KEY = 1
    JOYSTICK_CONFIG = 2