###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The error frame is contained in the error window and provides the user with error information
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 30, 2019
# Filename            : error_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gui.forms.base_classes.gui_frame import Gui_Frame
import pdb

class Error_Frame(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master, frame_name, message):
        
        self.message = message
        
        Gui_Frame.__init__(self, master, frame_name)
        self.create_frame(master)
        
    
    # Create the actual frame as a separate window
    def create_frame(self, master):
        
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        # Add the settings notebook to the frame
        ttk.Label(master.frames[self.frame_name], text = self.message).pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        