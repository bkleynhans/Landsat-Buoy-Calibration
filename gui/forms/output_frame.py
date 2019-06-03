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
from gui_frame import Gui_Frame


class Output_Frame(Gui_Frame):
    
    # Output Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "output_frame", "Output")
        self.create_output_frame(master)
        
    
    # Create Output Frame object
    def create_output_frame(self, master):
                
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)