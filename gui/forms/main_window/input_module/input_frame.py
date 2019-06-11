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
import os
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
        
        
    def delete_log_files(self, file_absolute_path, file_name):
        
        os.unlink((file_absolute_path + file_name))# unlink is ux version of delete
    
        
    def step_progressbar(self):
                    
        while not self.process_complete:
            
            self.progressbar.progressbar.step()            
            time.sleep(0.02)
            
            
        self.progressbar.progressbar_window.destroy()
        
        self.process_button.config(state = 'normal')
    
    
    def process_scene_id(self, master, scene_id, show_images, parameterized_statusfile, statusfile_absolute_path, statusfile_name,
                         parameterized_outputfile, outputfile_absolute_path, outputfile_name):
        
        from gui.tools.file_watcher import File_Watcher
        # Instantiate the watcher and pass the master object (containing required functions) and path to file
        self.status_watchdog = File_Watcher(master, statusfile_absolute_path)
        self.output_watchdog = File_Watcher(master, outputfile_absolute_path)
        
        self.status_watchdog.event_notifier.start()
        self.output_watchdog.event_notifier.start()
        
        forward_model.main([scene_id, show_images, "-ctarca_gui", parameterized_statusfile, parameterized_outputfile])
        
        self.process_complete = True
        
        self.status_watchdog.event_notifier.stop()
        self.output_watchdog.event_notifier.stop()
        
        #self.delete_log_files(statusfile_absolute_path, statusfile_name)
        #self.delete_log_files(outputfile_absolute_path, outputfile_name)
    
        
    # Define process for full_single
    def process_full_single(self, master):
        
        self.process_button.config(state = 'disabled')
        
        master.frames['status_frame'].widgets['status_text'].delete('1.0', 'end')
        master.frames['output_frame'].widgets['output_text'].delete('1.0', 'end')
        
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
                
                relative_status_path = 'logs/status/single'
                relative_output_path = 'logs/output/single'
            
                # Create a status logger instance
                statusfile_name = str(scene_id) + "_" + str(current_datetime) + ".status"
                statusfile_relative_path_and_filename = os.path.join(relative_status_path, statusfile_name)
                statusfile_absolute_path = os.path.join(master.project_root, relative_status_path)
                parameterized_statusfile = ("-t" + statusfile_relative_path_and_filename)
                
                # Create a output logger instance
                outputfile_name = str(scene_id) + "_" + str(current_datetime) + ".output"
                outputfile_relative_path_and_filename = os.path.join(relative_output_path, outputfile_name)
                outputfile_absolute_path = os.path.join(master.project_root, relative_output_path)
                parameterized_outputfile = ("-u" + outputfile_relative_path_and_filename)
            
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
                                 parameterized_statusfile, 
                                 statusfile_absolute_path,
                                 statusfile_name,
                                 parameterized_outputfile, 
                                 outputfile_absolute_path,
                                 outputfile_name, ]
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