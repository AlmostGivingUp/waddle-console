import sys
from pathlib import Path
import os

APP_NAME = "Waddle Console"

def get_resource_path(relative_path: str) -> Path:
    """
    Get path to bundled resources 
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)  # PyInstaller temp folder
    else:
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


def get_user_data_dir() -> Path:
    """
    Get user-writable application data directory
    """
    base_path = Path(os.getenv("LOCALAPPDATA", Path.home()))
    app_dir = base_path / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_profiles_dir() -> Path:
    """
    AppData / Profiles 
    """
    path = get_user_data_dir() / "Profiles"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_active_dir() -> Path:
    """
    AppData / Active 
    """
    path = get_user_data_dir() / "Active"
    path.mkdir(parents=True, exist_ok=True)
    return path