###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Creates a pop-up window that contains the error_frame. Errors
#                       are populated to the error frame and displayed in this window.
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 30, 2019
# Filename            : error_window.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from gui.forms.base_classes.gui_window import Gui_Window
from gui.forms.general.error_module.error_frame import Error_Frame
import pdb

class Error_Window(Gui_Window):    
    
    # Settings Window constructor
    def __init__(self, master, window_name, window_title, message_header, message_body):
        
        self.message_header = message_header
        self.message_body = message_body
        
        Gui_Window.__init__(self, master, window_name, window_title)
        self.create_error_window(master)
        
    
    # Create the actual window as a separate window
    def create_error_window(self, master):
        
        master.windows[self.window_name].protocol("WM_DELETE_WINDOW", lambda: self.on_closing(master))

        # Add the header frame to the errorwindow
        Error_Frame(master.windows[self.window_name], "error_header_frame", self.message_header)
        
        # Add the body frame to the error window
        Error_Frame(master.windows[self.window_name], "error_body_frame", self.message_body)
        

    # Action to perform when settings window is closed
    def on_closing(self, master):
    
        master.windows[self.window_name].destroy()