###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The frame that displays and accepts user input when a Single Channel Batch Buoy process is run
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 30, 2019
# Filename            : input_batch_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from gui.forms.base_classes.gui_frame import Gui_Frame
import pdb

class Input_Batch_Frame(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "input_batch_frame")
        
        master.frames[self.frame_name].input_values = {'batch_file' : ''}
        
        self.create_batch_frame(master)
            
    
    # Display file dialog so user may select the batch file with required data
    def display_file_dialog(self, master):
        
        master.frames[self.frame_name].input_values['batch_file'].delete(0, END)
        
        file_path = filedialog.askopenfile(
                initialdir = (master.master.master.project_root + "/input/batches"),
                title = "Select the batch file",
                filetypes = (
                    ("BATCH files", "*.batch"),
                    ("CSV files", "*.csv"),
                    ("TXT files", "*.txt"),
                    ("All files", "*.*")
                )
        )
                
        if (file_path != None):
            
            master.frames[self.frame_name].input_values['batch_file'].insert(0, file_path.name)
                        
            
    # Set up the tab requried for processing of Batches.  Type is determined by radio button
    def create_batch_frame(self, master):
        
        master.add(master.frames[self.frame_name], text = "Batch")
        master.tab(3, state = 'normal')
        
        # Read in the source file location
        ttk.Label(
                master.frames[self.frame_name],
                text = 'Source File : ',
                width = 20).grid(
                        row = 0,
                        column = 0,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        master.frames[self.frame_name].input_values['batch_file'] = ttk.Entry(master.frames[self.frame_name], width = 60)
        master.frames[self.frame_name].input_values['batch_file'].grid(row = 0, column = 1, columnspan = 3, padx = 10, pady = 10, sticky = 'nsew')
        
        self.browse_button = ttk.Button(
                master.frames[self.frame_name],
                text = 'Browse',
                command = lambda: self.display_file_dialog(master)).grid(
                        row = 0,
                        column = 4,
                        padx = 10,
                        pady = 10,
                        sticky = 'w'
                )