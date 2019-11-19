#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI master for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 8, 2019
# Filename            : tarca_gui.py
#
###

# Imports
from tkinter import *
from tkinter import messagebox


class Tarca_Gui:
    
    def __init__(self, master):
        
        # Import gui paths
        from forms.main_window.menu_bar import Menu_Bar
        from forms.main_window.header_frame import Header_Frame
        from forms.main_window.input_module.input_frame import Input_Frame
        from forms.main_window.output_module.output_frame import Output_Frame
        from forms.main_window.status_module.status_frame import Status_Frame
        
        # Create the root Tkinter object
        master.title('CIS Top Of Atmosphere Radiance Calibration System')
        master.geometry('1024x768')
        master.resizable(False, False)
        #master.configure(background = '#FFFFFF')
        
        # Ensure the master frame cannot be detached from the main program
        master.option_add('*tearOff', False)
        
        # Create frame container to easily access frames from other ares in the gui
        frames = {}
        master.frames = frames 
        
        # Create window container to easily access windows from other ares in the gui
        windows = {}
        master.windows = windows
                
        # Create the Menubar - accessed via master.menu_bar
        Menu_Bar(master)        
        
        # Create the Header - accessed via master.header_frame
        Header_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Input_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Output_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Status_Frame(master)
    

# Ask the user to confirm if they want to close the program
def on_closing(root):
    
    if messagebox.askyesno("Quit", "Do you really wish to quit?"):
        root.destroy()
    

# Main entry to the GUI program
def main(project_root):
            
    root = Tk()
    root.project_root = project_root
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    tarca_gui = Tarca_Gui(root)
    
    root.mainloop()
