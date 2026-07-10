from Core.game_console_configurator import MappingApp
import dearpygui.dearpygui as dpg # type: ignore

def main():
    MappingApp()
    dpg.start_dearpygui() 
    dpg.destroy_context() #main program

if __name__ == "__main__":
    print("starting main...\n")
    main()
