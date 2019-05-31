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
# Last Modified Date  : May 29, 2019
# Filename            : header_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from forms import input_frame
import pdb


class Header_Frame(input_frame.Input_Frame):
    
    # Header Frame constructor
    def __init__(self, master):
        
        self.create_header(master)
        
        
    # Create header frame object
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
                value = 'full',
                command = lambda: self.change_tabs(master, self.process_type)).grid(
                        row = 0,
                        column = 0)

        ttk.Radiobutton(
                self.frame_header,
                text = 'Partial Process',
                variable = self.process_type,
                value = 'partial',
                command = lambda: self.change_tabs(master, self.process_type)).grid(
                        row = 0,
                        column = 1)
        
        self.frame_header.pack(padx = 10, pady = 10)
        
          
    # Function to change visible tables based on radio button selection
    def change_tabs(self, master, selection):
        
        if (selection.get() == 'full') :            
            
            master.input_frame.input_notebook.tab(1, state = 'hidden')
            master.input_frame.input_notebook.tab(0, state = 'normal')
            master.input_frame.input_notebook.select(0)
            
        elif (selection.get() == 'partial'):            
            
            master.input_frame.input_notebook.tab(0, state = 'hidden')
            master.input_frame.input_notebook.tab(1, state = 'normal')
            master.input_frame.input_notebook.select(1)
             
            
        master.input_frame.input_notebook.tab(2, state = 'normal')