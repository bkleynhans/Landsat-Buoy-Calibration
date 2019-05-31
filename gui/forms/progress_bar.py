###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 23, 2019
# Filename            : progress_bar.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui


class Progress_Bar(tarca_gui.Tarca_Gui):
    
    def __init__(self, master):
        
        self.create_progressbar_window(master)
        
    
    def create_progressbar_window(self, master):
        
        # Create the progressbar object
        self.progressbar_window = Toplevel(master)                              # Create a progressbar toplevel window
        master.progressbar_window = self.progressbar_window                # Add the progressbar window to the master window as object variable
        
        self.progressbar_label = ttk.Label(self.progressbar_window, text = 'Loading Help Page ... ')
        self.progressbar_window.progressbar_label = self.progressbar_label
        
        self.progressbar_label.pack(anchor = 'sw', padx = 10, pady = (10, 0))
        
        self.progressbar = ttk.Progressbar(self.progressbar_window, orient = HORIZONTAL, length = 200)  # Create a progressbar
        self.progressbar_window.progressbar = self.progressbar                  # Add the progressbar to the progressbar window as object variable
                
        self.progressbar.pack(anchor = 'nw', padx = 10, pady = (0, 10))
        self.progressbar_window.withdraw()