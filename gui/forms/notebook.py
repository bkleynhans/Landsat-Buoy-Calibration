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
# Filename            : notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gui.forms import input_frame
import pdb

class Notebook(input_frame.Input_Frame):
    
    # Display file dialog so user may select the batch file with required data
    def display_file_dialog(self, notebook):
        
        notebook.batch_file_entry.delete(0, END)
        notebook.batch_file_entry.insert(0, filedialog.askopenfile().name)        
        
    
    # Set up the tab required for full processing of single Scene ID
    def setup_full_single(self, notebook):
        
        notebook.add(notebook.full_single, text = "Single")
        notebook.tab(0, state = 'hidden')
        
        ttk.Label(notebook.full_single, text = 'Scene ID : ').pack(side = LEFT, padx = 10, pady = 10)
        
        self.scene_id = ttk.Entry(notebook.full_single, width = 30)
        self.scene_id.pack(side = LEFT, padx = 10, pady = 10)
        
    
    # Set up the tab required for partial processing of single Scene ID
    def setup_partial_single(self, notebook):
        
        notebook.add(notebook.partial_single, text = "Single")
        notebook.tab(1, state = 'hidden')
        
        ttk.Label(notebook.partial_single, text = 'Date')
    
    
    # Set up the tab requried for processing of Batches.  Type is determined by radio button
    def setup_batch(self, notebook):
        
        notebook.add(notebook.full_batch, text = "Batch")
        notebook.tab(2, state = 'hidden')
        
        ttk.Label(notebook.full_batch, text = 'Source File : ').grid(row = 0, column = 0, sticky = 'w')
        batch_file_entry = ttk.Entry(notebook.full_batch, width = 50)
        notebook.batch_file_entry = batch_file_entry
        
        batch_file_entry.grid(row = 0, column = 1, columnspan = 2, sticky = 'w')
        
        self.browse_button = ttk.Button(
                notebook.full_batch,
                text = 'Browse',
                command = lambda: self.display_file_dialog(notebook)).grid(
                        row = 0,
                        column = 3,
                        padx = 10,
                        pady = 10,
                        sticky = 'w'
                )
        
    
    # Create the notebook object that will contain all the tabs
    def create_notebook(self, input_frame):
        
        self.notebook = ttk.Notebook(input_frame)
        input_frame.notebook = self.notebook
        
        self.full_single = ttk.Frame(self.notebook)
        self.notebook.full_single = self.full_single
        self.setup_full_single(self.notebook)
        
        self.partial_single = ttk.Frame(self.notebook)
        self.notebook.partial_single = self.partial_single
        self.setup_partial_single(self.notebook)
        
        self.full_batch = ttk.Frame(self.notebook)
        self.notebook.full_batch = self.full_batch
        self.setup_batch(self.notebook)        
        
        self.notebook.pack()    
        
    
    def __init__(self, master):
        
        self.create_notebook(master.input_frame)