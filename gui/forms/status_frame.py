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
# Filename            : status_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui


class Status_Frame(tarca_gui.Tarca_Gui):
    
    # Status Frame constructor
    def __init__(self, master):
        
        self.create_status_frame(master)
        
    
    # Create the status frame object
    def create_status_frame(self, master):
        
        self.status_frame = ttk.LabelFrame(master, text = 'Status')
        master.status_frame = self.status_frame
        
        self.status_frame.pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)