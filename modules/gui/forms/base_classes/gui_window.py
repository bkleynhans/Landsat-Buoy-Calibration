###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Base class for all Windows in the GUI
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 30, 2019
# Filename            : gui_window.py
#
###

# Imports
from tkinter import *
from tkinter import ttk


class Gui_Window():
        
    # Settings Window constructor
    def __init__(self, master, window_name, window_title):
                
        self.window_name = window_name
        self.window_title = window_title
        
        self.create_gui_window(master)
        
    
    # Create the actual window as a separate window
    def create_gui_window(self, master):
        
        self.gui_window = Toplevel(master)
        
        # Create frame container to easily access frames from other areas in the gui
        self.frames = {}
        self.gui_window.frames = self.frames
        
        # Create notebook container to easily access notebooks from other areas in the gui
        self.notebooks = {}
        self.gui_window_notebooks = self.notebooks
        
        # Create widgets container to easily access widgets from other areas in the gui
        self.widgets = {}
        self.gui_window.widgets = self.widgets
        
        master.windows[self.window_name] = self.gui_window