###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 18, 2019
# Filename            : settings_window.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gui.forms.base_classes.gui_window import Gui_Window
from gui.forms.settings.settings_frame import Settings_Frame
import pdb

class Settings_Window(Gui_Window):    
    
    # Settings Window constructor
    def __init__(self, master):
        
        Gui_Window.__init__(self, master, "settings_window", "Settings")
        self.create_settings_window(master)
        
    
    # Create the actual window as a separate window
    def create_settings_window(self, master):
        
        master.windows[self.window_name].protocol("WM_DELETE_WINDOW", lambda: self.on_closing(master))

        # Add the settings frame to the window
        Settings_Frame(master.windows[self.window_name])
        

    # Save changes made to settings
    def save_changes(self):
        
        pass


    # Action to perform when settings window is closed
    def on_closing(self, master):
    
        if messagebox.askyesno("Save Preferences", "Do you wish to save your changes?"):
            self.save_changes
        else:
            master.windows[self.window_name].destroy()