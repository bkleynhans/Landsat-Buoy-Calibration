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
# Filename            : input_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import time
import threading
from gui.forms.general.progress_bar import Progress_Bar
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
from gui.forms.main_window.input_module.input_notebook import Input_Notebook
import menu
import forward_model
import pdb


class Input_Frame(Gui_Label_Frame):
    
    # Input Frame constructor
    def __init__(self, master):
        
        Gui_Label_Frame.__init__(self, master, "input_frame", "Input")
        self.create_input_frame(master)
        
    
    # Create the actual Frame
    def create_input_frame(self, master):        
        
        master.frames[self.frame_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
        # Add the input notebook to the frame
        Input_Notebook(master.frames[self.frame_name], self.frame_name)
        
        self.add_process_button(master)
        
        
    # Add process button
    def add_process_button(self, master):
        
        self.process_button = ttk.Button(master.frames[self.frame_name], text = "Process")
        self.process_button.pack(anchor = 'e', padx = 10, pady = (0, 10))
        self.process_button.config(command = lambda: self.process_full_single(master))
        
        
    def step_progressbar(self):
                    
        while not self.process_complete:
            
            self.progressbar.progressbar.step()
            
            time.sleep(0.02)
            
        self.progressbar.progressbar_window.destroy()
    
    
    def process_scene_id(self, master, scene_id, show_images, parameterized_logfile, logfile_absolute_path):
        
        from gui.tools.file_watcher import File_Watcher
        # Instantiate the watcher and pass the master object (containing required functions) and path to file
        self.watchdog = File_Watcher(master, logfile_absolute_path)
        self.watchdog.event_notifier.start()
        
        forward_model.main([scene_id, show_images, parameterized_logfile])
        
        self.process_complete = True
        
        self.watchdog.event_notifier.stop()
    
        
    # Define process for full_single
    def process_full_single(self, master):
        
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].input_values['scene_id'].get()
        
        if (scene_id != None):
        
            if (menu.is_valid_id(scene_id)):
                
                show_images = messagebox.askyesno(
                        title = "Display Images",
                        message = "Do you wish to display each image as it is processing?")
                
                if show_images == True:
                    show_images = '-ntrue'
                else:
                    show_images = '-nfalse'
                
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
            
                # Create a logger instance
                logfile_name = str(scene_id) + "_" + str(current_datetime) + ".out"
                logfile_relative_path_and_filename = ("single/" + logfile_name)
                logfile_absolute_path = (master.project_root + "/logs/single/")
                parameterized_logfile = ("-l" + logfile_relative_path_and_filename)
            
                # Create a progress bar to show activity
                self.progressbar = Progress_Bar(master, 'Processing Scene ' + scene_id)
                self.progressbar.progressbar.config(mode = 'indeterminate')
                
                # Progressbar start and stop work with program loop, so manual loop is required for progression
                self.process_complete = False
                
                progressbar_thread = threading.Thread(target = self.step_progressbar)
                progressbar_thread.start()
                
                # Launch single scene ID process job in own thread
                cis_tarca_thread = threading.Thread(
                        target = self.process_scene_id, args = (
                                [master, 
                                 scene_id, 
                                 show_images, 
                                 parameterized_logfile, 
                                 logfile_absolute_path, ]
                        )
                )
                        
                cis_tarca_thread.start()
                                
            else:
                
                messagebox.showwarning(
                        title = "Invalid Input",
                        message = "The scene id you entered is of an incorrect format.\n\n"
                                    "Please try again")
                
        
    # Define process for partial_single
    def process_partial_single(self, master):
        
        pass
    
    
    # Define process for batch
    def process_batch(self, master):
        
        pass