from pathlib import Path

from Constants.enum import ConfigMode

from Core.maps.map import Map
from Core.maps.key_map import KeyMap
from Core.maps.mouse_map import MouseMap

class ProfileManager:
    """
    Handles profile persistence and retrieval.
    """
    MAP_CLASSES = {
        ConfigMode.KEYBOARD: KeyMap,
        ConfigMode.MOUSE: MouseMap
    }

    PROFILE_SUFFIX = {
        ConfigMode.KEYBOARD: "",
        ConfigMode.MOUSE: "_Mouse"
    }

    ACTIVE_CONFIG_FILES = {
        ConfigMode.KEYBOARD: "Active_Config.json",
        ConfigMode.MOUSE: "Active_Mouse_Config.json"
    }

    def __init__(self, profile_path: Path, active_path: Path):
        self.profile_path = profile_path
        self.active_path = active_path

    def list_profiles(self, mode: ConfigMode) -> list[str]:
        """
        Return profile names for the given mode. (only the stem)
        """
        profiles = []
        for file_path in self.profile_path.glob("*.json"):
            is_mouse_profile = (file_path.stem.endswith("_Mouse"))
            if (mode == ConfigMode.KEYBOARD and not is_mouse_profile):
                profiles.append(file_path.stem)
            elif (mode == ConfigMode.MOUSE and is_mouse_profile):
                profiles.append(file_path.stem)
        return sorted(profiles)


    def delete_profile(self, profile_name: str) -> None:
        """
        Delete a profile file.
        """
        file_path = (self.profile_path / f"{profile_name}.json")
        if file_path.exists():
            file_path.unlink()

    def save_profile(self, profile_name: str, mode: ConfigMode, mapping: Map) -> Path:
        """
        Save profile and update active profile.
        """
        suffix = self.PROFILE_SUFFIX[mode]
        if (suffix and not profile_name.endswith(suffix)):
            profile_name += suffix
        filename = (self.profile_path /f"{profile_name}.json")
        mapping.save(filename)
        self._save_active_profile(mapping,mode)
        return filename

    def _save_active_profile(self,mapping: Map,mode: ConfigMode) -> None:
        """
        Update currently active profile.
        """
        active_file = (
            self.active_path /
            self.ACTIVE_CONFIG_FILES[mode]
        )
        mapping.save(active_file)


    def load_profile(self, profile_name: str, mode: ConfigMode) -> Map:
        """
        Load and return a profile.
        """
        filename = (self.profile_path /f"{profile_name}.json")
        map_class = self.MAP_CLASSES[mode]
        return map_class.load(filename)

    def profile_exists(self,profile_name: str) -> bool:
        filename = (self.profile_path /f"{profile_name}.json")
        return filename.exists()

