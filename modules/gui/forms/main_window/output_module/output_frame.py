###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The output frame contains all the RESULTS from the program.  Whenever a
#                       process has finished, its results will be displayed int he output frame
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 29, 2019
# Filename            : output_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
import pdb


class Output_Frame(Gui_Label_Frame):
    
    # Output Frame constructor
    def __init__(self, master):
        
        Gui_Label_Frame.__init__(self, master, "output_frame", "Output")
        self.create_output_frame(master)
        
    
    # Create Output Frame object
    def create_output_frame(self, master):
        
        self.add_output_textbox(master.frames[self.frame_name])
                
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        
    # Add a text widget to display the processing status
    def add_output_textbox(self, master):
                
        self.output_text = Text(master, height = 5, width = 5, font=('Courier', 8))
        
        self.widgets['output_text'] = self.output_text
        
        self.output_text.config(wrap = 'word')
        self.output_text.pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        