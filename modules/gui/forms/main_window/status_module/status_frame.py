###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The status frame displays the current status of a process.  It displays
#                       data from text files which are created during output, and are monitored
#                       by the gui/tools/event_processor.py and gui/tools/event_watcher.py modules.
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 28, 2019
# Filename            : status_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
import pdb


class Status_Frame(Gui_Label_Frame):
    
    # Status Frame constructor
    def __init__(self, master):
        
        Gui_Label_Frame.__init__(self, master, "status_frame", "Status")
        self.create_status_frame(master)
        
    
    # Create the status frame object
    def create_status_frame(self, master):
        
        self.add_status_textbox(master.frames[self.frame_name])
                
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        
    # Add a text widget to display the processing status
    def add_status_textbox(self, master):
        
        self.status_text = Text(master, height = 5, width = 5)
        
        self.widgets['status_text'] = self.status_text
        
        self.status_text.config(wrap = 'word')
        self.status_text.pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        