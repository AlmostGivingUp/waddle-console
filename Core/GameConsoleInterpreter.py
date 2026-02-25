import platform
import hid
import time 
from Util.mapping import show_popup, messagebox
if platform.system() == "Windows":
    from Injectors.windows_injector import key_mapping
"""
elif platform.system() == "Linux":
    from Injectors.linux_injector import key_mapping
elif platform.system() == "Darwin":
    from Injectors.darwin_injector import key_mapping
else:
    raise RuntimeError("Unsupported OS")
"""


VID = 0x0483
PID = 0x5750


def connect_device():
    show_popup("Connecting device...Press OK when acknowledged", 0)

    while True:
        try:
            print("Opening the device")
            device = hid.device()
            device.open(VID, PID)
            print("Manufacturer: %s" % device.get_manufacturer_string())
            print("Product: %s" % device.get_product_string())
            print("Serial No: %s" % device.get_serial_number_string())
        
            device.set_nonblocking(True)
            show_popup(
                f"Device VID {VID} PID {PID} connected successfully!",
                0
            )
            return device

        except OSError:
            res = show_popup(
                f"Device VID {VID} PID {PID} not found. Retry?",
                1
            )
            if not res:
                return None
            time.sleep(2)


def read_loop(device):
    while True:
        data = device.read(4) # 32 bits 
        if data:
            print(data)
            key_mapping(data)
            
def connecting_and_read():
    device = connect_device()
    if device:
        read_loop(device)
