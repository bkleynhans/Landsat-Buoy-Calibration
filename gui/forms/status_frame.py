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
# Filename            : status_form.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui
from gui.forms import notebook

class Status_Frame(tarca_gui.Tarca_Gui):
    
    def create_status_frame(self, master):
        
        status_frame = ttk.Frame(master)
        master.status_frame = status_frame
        
        status_frame.pack(anchor = 'w')
        
        notebook.Notebook(master)
        
    
    def __init__(self, master):
        
        self.create_status_frame(master)