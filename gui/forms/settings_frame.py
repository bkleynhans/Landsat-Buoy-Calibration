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
# Last Modified Date  : May 30, 2019
# Filename            : settings_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gui.forms import menu_bar
from gui.forms import settings_notebook


class Settings_Frame(menu_bar.Menu_Bar):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        self.create_settings_frame(master)
        
    
    # Create the actual frame as a separate window
    def create_settings_frame(self, master):
        
        self.settings_frame = Toplevel(master)
        master.settings_frame = self.settings_frame
        
        self.settings_frame.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(master.settings_frame))
        
        # Add the settings notebook to the frame
        #settings_notebook.Notebook(master)
        
        
    # Save changes made to settings
    def save_changes(self):
        
        pass
    
    
    # Action to perform when settings window is closed
    def on_closing(self, settings_frame):
    
        if messagebox.askyesno("Save Preferences", "Do you wish to save your changes?"):
            self.save_changes
        else:
            settings_frame.destroy()