import platform
import usb.core as core  # type: ignore
import usb.util as util  # type: ignore
import time 
import tkinter as tk
from tkinter import messagebox
import dearpygui.dearpygui as dpg
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

def show_popup(message):
    """
    Show pop up
    """
    root = tk.Tk()
    root.withdraw()  # Hide main window
    messagebox.showinfo("HID Status", message)
    root.destroy()

def interpret(VID=VID, PID=PID):
    """
    Find device using VID and PID
    """
    print("Interpreter started.")
    not_connected = True 
    show_popup(f"Connecting to device VID {VID} PID {PID}...")
   
    while not_connected:    
        dev = core.find(idVendor=VID, idProduct=PID)
        if dev is not None:
            not_connected = False
            show_popup(f"Device VID {VID} PID {PID} connected successfully!")
            messagebox.askokcancel()    
    print(f"Device of VID {VID} and PID {PID} found. \n")

    """
    Detach, claim, and listen into USB IN endpoint
    """
    if dev.is_kernel_driver_active(0): #check if interface index 0 is attached 
        print("Detaching kernel driver...")
        dev.detach_kernel_driver(0)
    config = dev.get_active_configuration()
    interface = config[(0,0)]

    ep_in = util.find_descriptor(
        interface,
        custom_match=lambda e:
            util.endpoint_direction(e.bEndpointAddress) == util.ENDPOINT_IN
    )

    print("Interface claimed.\n")
    print("Listening to endpoint", ep_in)

    """
    data harvesting
    """
    while True:
        try:
            data = dev.read(ep_in.bEndpointAddress, ep_in.wMaxPacketSize, timeout=1000)
            print("Raw:", data)
            key_mapping(data)
        except core.USBError as e:
            if e.errno != 110:
                print("USB Error:", e)