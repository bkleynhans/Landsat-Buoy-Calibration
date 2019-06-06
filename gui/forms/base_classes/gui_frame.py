###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 29, 2019
# Filename            : input_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import pdb

class Gui_Frame():
    
    # Create Notebook container
    notebooks = {}
    
    # Main Gui Frame constructor
    def __init__(self, master, frame_name):
        
        self.frame_name = frame_name
        
        self.create_gui_frame(master)
        
    
    # Create the actual Frame
    def create_gui_frame(self, master):
        
        self.gui_frame = ttk.LabelFrame(master)
        
        self.gui_frame.notebooks = Gui_Frame.notebooks
        
        master.frames[self.frame_name] = self.gui_frame