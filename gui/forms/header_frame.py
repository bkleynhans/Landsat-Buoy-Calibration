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
from forms import input_frame

class Header(input_frame.Input_Frame):
    
    def create_header(self, master):
        
        # Create the Header frame
        self.frame_header = ttk.Frame(master)
        master.header_frame = self.frame_header
        
        # Add Radio Buttons to Header frame
        self.process_type = StringVar()
        
        ttk.Radiobutton(                
                self.frame_header,
                text = 'Full Process',
                variable = self.process_type,
                value = 'full').grid(
                        row = 0,
                        column = 0)

        ttk.Radiobutton(
                self.frame_header,
                text = 'Partial Process',
                variable = self.process_type,
                value = 'partial').grid(
                        row = 0,
                        column = 1)
        
        self.frame_header.pack()
        
    
    def __init__(self, master):
        
        self.create_header(master)