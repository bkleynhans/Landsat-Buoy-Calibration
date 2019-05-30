#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 23, 2019
# Filename            : gui.py
#
###

# Imports
from tkinter import *
from tkinter import messagebox
import inspect
import sys
import os
import pdb

class Tarca_Gui:
    
    def __init__(self, master):
        
        # Import gui paths
        from forms import progress_bar
        from forms import menu_bar
        from forms import header_frame
        from forms import input_frame
        from forms import output_frame
        from forms import status_frame
        
        # Create the root Tkinter object
        master.title('CIS Top Of Atmosphere Radiance Calibration System')
        master.geometry('800x600')
        master.resizable(False, False)
        #master.configure(background = '#FFFFFF')
        
        master.option_add('*tearOff', False)
        
        # Create the Progressbar window - accessed via master.progressbar_window.progress_bar
        progress_bar.Progress_Bar(master)
        
        # Create the Menubar - accessed via master.menu_bar
        menu_bar.Menu_Bar(master)
        
        # Create the Header - accessed via master.header_frame
        header_frame.Header_Frame(master)
        
        # Create the Input Frame - accessed via master.
        input_frame.Input_Frame(master)
        
        # Create the Input Frame - accessed via master.
        output_frame.Output_Frame(master)
        
        # Create the Input Frame - accessed via master.
        status_frame.Status_Frame(master)
        
        

# Calculate fully qualified path to location of program execution
def get_module_path():
    
    filename = inspect.getfile(inspect.currentframe())
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    return path, filename


# Set environment variables to locate current execution path
def set_path_variables():
    
    path, filename = get_module_path()
    
    # find the Calibration program path
    path_index = path.rfind('/')
    
    # append gui paths
    sys.path.append(path[:path_index])
    sys.path.append(path)
    sys.path.append(path + "/forms")
    
    
def on_closing(root):
    
    if messagebox.askyesno("Quit", "Do you really wish to quit?"):
        root.destroy()
    

def main():
    
    set_path_variables()
    
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    tarca_gui = Tarca_Gui(root)
    root.mainloop()
    
    
if __name__ == "__main__": main()
