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
# Last Modified Date  : May 28, 2019
# Filename            : notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms import input_frame

class Notebook(input_frame.Input_Frame):
    
    def setup_full_single(self, notebook):
        
        notebook.add(notebook.full_single, text = "Full")
        
        
    def setup_partial_single(self, notebook):
        
        notebook.add(notebook.partial_single, text = "Partial")
    
    
    #def setup_full_batch(self, notebook):
    def setup_batch(self, notebook):
        
        notebook.add(notebook.full_batch, text = "Full")
        
        
#    def setup_partial_batch(self, notebook):
#        
#        notebook.add(notebook.partial_batch, text = "Partial")
    
    
    def create_notebook(self, master_frame):
        
        self.notebook = ttk.Notebook(master_frame)
        master_frame.notebook = self.notebook
        
        self.full_single = ttk.Frame(self.notebook)
        self.notebook.full_single = self.full_single
        self.setup_full_single(self.notebook)
        
        self.partial_single = ttk.Frame(self.notebook)
        self.notebook.partial_single = self.partial_single
        self.setup_partial_single(self.notebook)
        
        self.full_batch = ttk.Frame(self.notebook)
        self.notebook.full_batch = self.full_batch
        #self.setup_full_batch(self.notebook)
        self.setup_batch(self.notebook)
        
#        self.partial_batch = ttk.Frame(self.notebook)
#        self.notebook.partial_batch = self.partial_batch
#        self.setup_partial_batch(self.notebook)
        
        
        self.notebook.pack()    
        
    
    def __init__(self, master):
        
        self.create_notebook(master.input_frame)