from pathlib import Path
import json


class Map:
    """
    Super Mapping class! 
    """
    def __init__(self):
        """
        Empty initialisation 
        """
        self.buttons = {}
        self.joysticks = {}

    def get_map(self):
        """
        Retrieving itself (deserializing)
        """
        return {
            **self.buttons,
            **self.joysticks
        }

    def to_dict(self):
        """
        Construct dict from key map  
        """
        return {
            "buttons": self.buttons,
            "joysticks": self.joysticks
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Construct key map from dict 
        """
        obj = cls()
        if "buttons" in data:
            obj.buttons = data["buttons"]
        if "joysticks" in data:
            obj.joysticks = data["joysticks"]
        return obj


    def save(self, filename):
        """
        Saving self 
        """
        filename = Path(filename)
        with open(filename, "w") as f:
            json.dump(
                self.to_dict(),
                f,
                indent=4
            )

    @classmethod
    def load(cls, filename):
        """
        Loading self 
        """
        filename = Path(filename)
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __getitem__(self, key):
        """
        Accessing item 
        """
        key = key.upper() 
        if key in self.buttons:
            return self.buttons[key]
        elif key in self.joysticks:
            return self.joysticks[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Setting item 
        """
        key = key.upper() 
        if key in self.buttons:
            self.buttons[key] = value
        elif key in self.joysticks:
            self.joysticks[key] = value
        else:
            raise KeyError(key)

    def __repr__(self):
        """
        String representation
        """
        return (
            f"{self.__class__.__name__}"
            f"({self.get_map()})"
        )