from Core.GameConsoleConfigurator import start_configurator
from Core.GameConsoleInterpreter import interpret
import time 

def main():
    start_configurator()
    time.sleep(2)
    interpret()


if __name__ == "__main__":
    print("starting main...\n")
    main()
