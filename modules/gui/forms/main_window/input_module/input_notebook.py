###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Contains the input frame
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 29, 2019
# Filename            : input_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_notebook import Gui_Notebook
from gui.forms.main_window.input_module.input_sub_frames.input_buoy_sc_frame import Input_Buoy_Sc_Frame
from gui.forms.main_window.input_module.input_sub_frames.input_toa_sc_frame import Input_Toa_Sc_Frame
from gui.forms.main_window.input_module.input_sub_frames.input_lst_sw_frame import Input_Lst_Sw_Frame
from gui.forms.main_window.input_module.input_sub_frames.input_batch_frame import Input_Batch_Frame
import pdb

class Input_Notebook(Gui_Notebook):
    
    # Input Notebook constructor
    def __init__(self, master, frame_name):
        
        Gui_Notebook.__init__(self, master, 'input_notebook')
        self.create_notebook(master)
        
        
    # Create the input_notebook object that will contain all the tabs
    def create_notebook(self, master):                                      
        
        # Create Full Single frame - tab 0 on input_frame as referenced in header_frame
        Input_Buoy_Sc_Frame(master.notebooks[self.notebook_name])

        # Create Partial Single frame - tab 1 on input_frame as referenced in header_frame
        Input_Toa_Sc_Frame(master.notebooks[self.notebook_name])
        
        # Create lst_sw frame - tab 1 on input_frame as referenced in header_frame
        Input_Lst_Sw_Frame(master.notebooks[self.notebook_name])

        # Create Batch frame - tab 2 on input_frame as referenced in header_frame
        Input_Batch_Frame(master.notebooks[self.notebook_name])
        
        # Add this notebook to the master notebooks list
        master.notebooks[self.notebook_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)