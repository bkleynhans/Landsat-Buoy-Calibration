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
from tkinter import messagebox
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
from gui.forms.main_window.input.input_notebook import Input_Notebook
import menu
import forward_model
import pdb


class Input_Frame(Gui_Label_Frame):
    
    # Input Frame constructor
    def __init__(self, master):
        
        Gui_Label_Frame.__init__(self, master, "input_frame", "Input")
        self.create_input_frame(master)
        
    
    # Create the actual Frame
    def create_input_frame(self, master):
        
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        # Add the input notebook to the frame
        Input_Notebook(master.frames[self.frame_name], self.frame_name)
        
        self.add_process_button(master)
        
        
    # Add process button
    def add_process_button(self, master):
        
        self.process_button = ttk.Button(master.frames[self.frame_name], text = "Process")
        self.process_button.pack(anchor = 'e', padx = 10, pady = (0, 10))
        self.process_button.config(command = lambda: self.process_full_single(master))
        
    # Define process for full_single
    def process_full_single(self, master):
        
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].input_values['scene_id'].get()
        
        if (scene_id != None):
        
            if (menu.is_valid_id(scene_id)):
                
                forward_model.main([scene_id, '-nfalse'])
                
            else:
                
                messagebox.showwarning(
                        title = "Invalid Input",
                        message = "The scene id you entered is of an incorrect format.\n\n"
                                    "Please try again")
                
        
    # Define process for partial_single
    def process_partial_single(self, master):
        
        pass
    
    
    # Define process for batch
    def process_batch(self, master):
        
        pass