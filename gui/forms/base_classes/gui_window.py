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
        
        self.frames = {}
        self.gui_window.frames = self.frames
        
        self.widgets = {}
        self.gui_window.widgets = self.widgets
        
        master.windows[self.window_name] = self.gui_window