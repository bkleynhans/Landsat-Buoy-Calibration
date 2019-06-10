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
# Filename            : gui_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import pdb

class Gui_Notebook():
    
    # Main Gui Frame constructor
    def __init__(self, master, notebook_name):
        
        self.notebook_name = notebook_name
        
        self.create_gui_notebook(master)
        
    
    # Create the actual Frame
    def create_gui_notebook(self, master):
        
        self.gui_notebook = ttk.Notebook(master)
        
        self.frames = {}
        self.gui_notebook.frames = self.frames
        
        self.widgets = {}
        self.gui_notebook.widgets = self.widgets
        
        master.notebooks[self.notebook_name] = self.gui_notebook