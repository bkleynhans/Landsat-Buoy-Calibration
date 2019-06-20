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
# Filename            : input_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_notebook import Gui_Notebook
from gui.forms.main_window.input_module.input_sub_frames.input_full_single import Input_Full_Single
from gui.forms.main_window.input_module.input_sub_frames.input_partial_single import Input_Partial_Single
from gui.forms.main_window.input_module.input_sub_frames.input_batch import Input_Batch
import pdb

class Input_Notebook(Gui_Notebook):
    
    # Input Notebook constructor
    def __init__(self, master, frame_name):
        
        Gui_Notebook.__init__(self, master, 'input_notebook')
        self.create_notebook(master)
        
        
    # Create the input_notebook object that will contain all the tabs
    def create_notebook(self, master):
        
        master.notebooks[self.notebook_name].input_values = {'batch_file': '',
                                      'scene_id_full_single': '',
                                      'scene_id_partial_single': '',
                                      'date_frame_container': {
                                              'frame': '',
                                              'date_picker': '',
                                              'date_label': '',
                                              'date': ''},
                                      'lat': '',
                                      'lon': '',
                                      'emissivity_b10': '',
                                      'emissivity_b11': '',
                                      'surface_temp': ''}
                                      

        Input_Full_Single(master.notebooks[self.notebook_name])

        Input_Partial_Single(master.notebooks[self.notebook_name])

        Input_Batch(master.notebooks[self.notebook_name])
        
        master.notebooks[self.notebook_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)