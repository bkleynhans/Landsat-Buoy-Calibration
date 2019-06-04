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
from gui_frame import Gui_Frame
from settings_notebook import Settings_Notebook
import pdb

class Settings_Frame(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "settings_frame", "Settings")
        self.create_settings_frame(master)
        
    
    # Create the actual frame as a separate window
    def create_settings_frame(self, master):
        
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        # Add the settings notebook to the frame
        Settings_Notebook(master, self.frame_name)