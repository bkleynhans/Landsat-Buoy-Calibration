###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The header frame class contains the conditions for the header of 
#                       the program.  From here the user selects which algorithm they want
#                       to calculate (SC - Single Channel; TOA - Top of Atmosphere;SW - Split Window)
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 29, 2019
# Filename            : header_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_frame import Gui_Frame
import pdb

class Header_Frame(Gui_Frame):
    
    # Header Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "header_frame")
        self.create_header(master)
        
        
    # Create header frame object
    def create_header(self, master):
        
        # Add Radio Buttons to Header frame
        self.process_type = StringVar()
        self.process_type.set('buoy_sc')
        
        # Tab 0 on input_frame
        ttk.Radiobutton(
                master.frames[self.frame_name],
                text = 'Buoy SC',
                variable = self.process_type,
                value = 'buoy_sc',
                width = 10,
                command = lambda: self.change_tabs(master, self.process_type)).grid(
                        row = 0,
                        column = 0)

        # Tab 1 on input_frame
        ttk.Radiobutton(
                master.frames[self.frame_name],
                text = 'TOA SC',
                variable = self.process_type,
                value = 'toa_sc',
                width = 10,
                command = lambda: self.change_tabs(master, self.process_type)).grid(
                        row = 0,
                        column = 1)
        
        # Tab 2 on input_frame
        ttk.Radiobutton(
                master.frames[self.frame_name],
                text = 'LST SW',
                variable = self.process_type,
                value = 'lst_sw',
                width = 10,
                command = lambda: self.change_tabs(master, self.process_type)).grid(
                        row = 0,
                        column = 2)
        
        master.frames[self.frame_name].pack(padx = 10, pady = (20, 0))
        
          
    # Function to change visible tables based on radio button selection
    def change_tabs(self, master, selection):
        
        # Tab 0 on input_frame
        if (selection.get() == 'buoy_sc') :            
            
            master.frames['input_frame'].notebooks['input_notebook'].tab(0, state = 'normal')
            master.frames['input_frame'].notebooks['input_notebook'].tab(1, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(2, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(3, state = 'normal')
            master.frames['input_frame'].notebooks['input_notebook'].select(0)
        
        # Tab 1 on input_frame
        elif (selection.get() == 'toa_sc'):            
            
            master.frames['input_frame'].notebooks['input_notebook'].tab(0, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(1, state = 'normal')
            master.frames['input_frame'].notebooks['input_notebook'].tab(2, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(3, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].select(1)
            
        # Tab 2 on input_frame
        elif (selection.get() == 'lst_sw'):            
            
            master.frames['input_frame'].notebooks['input_notebook'].tab(0, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(1, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].tab(2, state = 'normal')
            master.frames['input_frame'].notebooks['input_notebook'].tab(3, state = 'hidden')
            master.frames['input_frame'].notebooks['input_notebook'].select(2)
        
        self.clear_output_fields(master)
        
        
    # Clean the output areas and disable the button
    def clear_output_fields(self, master):        
        
        # Clear the output frames (output andn status)
        master.frames['status_frame'].widgets['status_text'].delete('1.0', 'end')
        master.frames['output_frame'].widgets['output_text'].delete('1.0', 'end')