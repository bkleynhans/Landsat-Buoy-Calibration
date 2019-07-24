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

class Gui_Label_Frame():
    
    # Main Gui Frame constructor
    def __init__(self, master, frame_name, frame_title):
        
        self.frame_name = frame_name
        self.frame_title = frame_title
        
        self.create_gui_label_frame(master)
        
    
    # Create the actual Frame
    def create_gui_label_frame(self, master):
        
        self.gui_label_frame = ttk.LabelFrame(master, text = self.frame_title)
        
        self.notebooks = {}
        self.gui_label_frame.notebooks = self.notebooks
        
        self.frames = {}
        self.gui_label_frame.frames = self.frames
        
        self.widgets = {}
        self.gui_label_frame.widgets = self.widgets
        
        master.frames[self.frame_name] = self.gui_label_frame