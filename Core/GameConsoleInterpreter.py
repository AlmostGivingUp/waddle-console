import platform
import hid
import time 
import queue 

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


def connect_device(event_queue: queue):
    while True:
        try:
            print("Opening the device")
            device = hid.device()
            device.open(VID, PID)
            print("Manufacturer: %s" % device.get_manufacturer_string())
            print("Product: %s" % device.get_product_string())
            print("Serial No: %s" % device.get_serial_number_string())
        
            device.set_nonblocking(True)
            event_queue.put(("Success", f"Device VID={VID}  PID={PID} is found."))
            return device

        except OSError:
            event_queue.put(("Error", f"Device VID={VID}  PID={PID} not found. Retrying."))
            time.sleep(2)


def read_loop(device):
    while True:
        data = device.read(4) # 32 bits 
        if data:
            print(data)
            key_mapping(data)
            
def connecting_and_read(event_queue: queue):
    device = connect_device(event_queue)
    if device:
        read_loop(device)