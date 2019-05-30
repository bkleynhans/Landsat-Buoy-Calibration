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
# Filename            : output_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui

class Output_Frame(tarca_gui.Tarca_Gui):
    
    def create_output_frame(self, master):
        
        self.output_frame = ttk.LabelFrame(master, text = 'Output')
        master.output_frame = self.output_frame
        
        self.output_frame.pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
    
    def __init__(self, master):
        
        self.create_output_frame(master)