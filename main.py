from Core.GameConsoleConfigurator import start_configurator
from Core.GameConsoleInterpreter import connecting_and_read
import time 
import threading 


def main():
    t = threading.Thread(target=connecting_and_read, daemon=True)
    t.start() #running background thread
    start_configurator() #main program

if __name__ == "__main__":
    print("starting main...\n")
    main()
