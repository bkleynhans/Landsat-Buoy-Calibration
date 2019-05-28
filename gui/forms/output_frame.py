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
# Filename            : output_form.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui
from gui.forms import notebook

class Output_Frame(tarca_gui.Tarca_Gui):
    
    def create_output_frame(self, master):
        
        output_frame = ttk.Frame(master)
        master.output_frame = output_frame
        
        output_frame.pack(anchor = 'w')
        
        notebook.Notebook(master)
        
    
    def __init__(self, master):
        
        self.create_output_frame(master)