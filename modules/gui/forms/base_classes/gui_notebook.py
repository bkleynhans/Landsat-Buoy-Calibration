###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Base class for all Notebooks in the GUI
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 29, 2019
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
        
        # Create notebook container to easily access notebooks from other areas in the gui
        self.notebooks = {}
        self.gui_notebook.notebooks = self.notebooks
        
        # Create frame container to easily access frames from other areas in the gui
        self.frames = {}
        self.gui_notebook.frames = self.frames
        
        # Create widgets container to easily access widgets from other areas in the gui
        self.widgets = {}
        self.gui_notebook.widgets = self.widgets
        
        master.notebooks[self.notebook_name] = self.gui_notebook