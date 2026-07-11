import platform
import hid
import time 
import queue

from Constants.enum import EventType 
processor = None 
if platform.system() == "Windows":
    from Injectors.windows.windows_injector import HIDProcessor
    processor = HIDProcessor()
else:
    raise RuntimeError("Unsupported OS")


VID = 0x0483
PID = 0x5750

def connect_device(event_queue: queue):
    """
    Desperately connecting to the device 
    """
    connected = False
    while True:
        try:
            print("Opening the device")
            device = hid.device()
            device.open(VID, PID)
            print("Manufacturer: %s" % device.get_manufacturer_string())
            print("Product: %s" % device.get_product_string())
            print("Serial No: %s" % device.get_serial_number_string())
            device.set_nonblocking(True)

            if not connected:
                event_queue.put((EventType.SUCCESS, f"Device VID={VID}  PID={PID} is found."))
            connected = True
            return device

        except OSError:
            if connected:
                event_queue.put((EventType.ERROR, f"Device VID={VID}  PID={PID} not found. Retrying."))
            connected = False 
            time.sleep(2)


def read_loop(device, processor):
    """
    Read device continuously
    """
    while True:
        data = device.read(6) 
        if data:
            print(data)
            processor.process_hid_report(data)
        time.sleep(0.001) 
            
def connecting_and_read(event_queue: queue):
    """
    Connect + Read, repeat if fails 
    """
    while True: 
        device = connect_device(event_queue)

        try: 
            read_loop(device=device, processor=processor)
        except OSError as e:
            print(f"USB disconnected: {e}")
            event_queue.put(
                (EventType.ERROR, "Device disconnected. Reconnecting...")
            )
        finally: 
            print(f"USB disconnected: {e}")
            event_queue.put(
                (EventType.ERROR, "Device disconnected. Reconnecting...")
            )
        