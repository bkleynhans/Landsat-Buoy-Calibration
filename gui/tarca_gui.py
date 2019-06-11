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
# Filename            : tarca_gui.py
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
        from forms.main_window.menu_bar import Menu_Bar
        from forms.main_window.header_frame import Header_Frame
        from forms.main_window.input_module.input_frame import Input_Frame
        from forms.main_window.output_module.output_frame import Output_Frame
        from forms.main_window.status_module.status_frame import Status_Frame
        
        # Create the root Tkinter object
        master.title('CIS Top Of Atmosphere Radiance Calibration System')
        master.geometry('1024x768')
        master.resizable(False, False)
        #master.configure(background = '#FFFFFF')
        
        master.option_add('*tearOff', False)
        
        # Create the Menubar - accessed via master.menu_bar
        Menu_Bar(master)
        
        # Create frame container
        frames = {}
        master.frames = frames 
        
        # Create window container
        windows = {}
        master.windows = windows
        
        # Create the Header - accessed via master.header_frame
        Header_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Input_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Output_Frame(master)
        
        # Create the Input Frame - accessed via master.
        Status_Frame(master)
        
        # Test if data sources are available
                

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
    
    # append the Calibration program paths
    sys.path.append(path[:path_index])
    sys.path.append(path[:path_index] + "/buoycalib")
    sys.path.append(path[:path_index] + "/downloaded_data")
    sys.path.append(path[:path_index] + "/tools")
    sys.path.append(path[:path_index] + "/output")
    sys.path.append(path[:path_index] + "/processed_images")
        
    # append gui paths
    sys.path.append(path)
    sys.path.append(path + "/forms")
    
    return path[:path_index]
    
    
def on_closing(root):
    
    if messagebox.askyesno("Quit", "Do you really wish to quit?"):
        root.destroy()
    

def main():    
    
    project_root = set_path_variables()
    
    import menu    
    menu.check_required_directories()
        
    root = Tk()
    root.project_root = project_root
    #root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    tarca_gui = Tarca_Gui(root)
    
    root.mainloop()
    
    
if __name__ == "__main__": main()
