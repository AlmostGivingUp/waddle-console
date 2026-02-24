from Core.GameConsoleConfigurator import start_configurator
from Core.GameConsoleInterpreter import connecting_and_read
import time 

def main():
    start_configurator()
    time.sleep(2)
    connecting_and_read()


if __name__ == "__main__":
    print("starting main...\n")
    main()
