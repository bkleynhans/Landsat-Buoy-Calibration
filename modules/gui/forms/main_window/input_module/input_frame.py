###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The input frame consists of multiple tabs and takes all the input for the program. Different tabs are enabled and disabled
#                       based on selections made by the user on the header frame.
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 8, 2019
# Filename            : input_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os, sys
import datetime
import time
import threading
from gui.forms.general.progress_bar import Progress_Bar
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
from gui.forms.main_window.input_module.input_notebook import Input_Notebook
from gui.forms.general.error_module.error_window import Error_Window
from modules.core import menu
from modules.core.model import Model
from tools import test_paths
import pdb


class Input_Frame(Gui_Label_Frame):
    
    # Input Frame constructor
    def __init__(self, master):
                
        self.path_dictionary = {
                'relative_status_log_path': '',
                'relative_output_log_path': '',
                'statusfile_name': '',
                'statusfile_relative_path_and_filename': '',
                'statusfile_absolute_path': '',
                'statusfile_absolute_path_and_filename': '',
                'outputfile_name': '',
                'outputfile_relative_path_and_filename': '',
                'outputfile_absolute_path': '',
                'outputfile_absolute_path_and_filename': ''
        }
        
        self.current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
                    
        Gui_Label_Frame.__init__(self, master, "input_frame", "Input")
        self.create_input_frame(master)
        
    
    # Create the actual Frame
    def create_input_frame(self, master):        
        
        master.frames[self.frame_name].pack(anchor = 'w', fill = 'both', expand = True, padx = 10, pady = 10)
        
        # Add the input notebook to the frame
        Input_Notebook(master.frames[self.frame_name], self.frame_name)
        
        self.add_process_button(master)
        
        
    # Perform processes based on active tab
    def process_active_tab(self, master):
        
        active_tab = master.frames['input_frame'].notebooks['input_notebook'].index(master.frames['input_frame'].notebooks['input_notebook'].select())
        
        self.path_dictionary['relative_status_log_path'] = 'logs/status'
        self.path_dictionary['relative_output_log_path'] = 'logs/output'
        
        if (active_tab == 0) or (active_tab == 1):
            self.path_dictionary['relative_status_log_path'] = os.path.join(self.path_dictionary['relative_status_log_path'], 'single')
        elif (active_tab == 2):
            self.path_dictionary['relative_status_log_path'] = os.path.join(self.path_dictionary['relative_status_log_path'], 'batch')
        
        if (active_tab == 0): # Single Buoy Single Channel
            self.path_dictionary['relative_output_log_path'] = os.path.join(self.path_dictionary['relative_output_log_path'], 'single')
            self.process_single_buoy_sc(master)
        elif (active_tab == 1): # Single ToA Single Channel
            self.path_dictionary['relative_output_log_path'] = os.path.join(self.path_dictionary['relative_output_log_path'], 'single')
            self.process_single_toa_sc(master)
        elif (active_tab == 2): # Single Land Surface Temperature Split Window
            self.path_dictionary['relative_output_log_path'] = os.path.join(self.path_dictionary['relative_output_log_path'], 'single')
            self.process_single_lst_sw(master)
        elif (active_tab == 3): # Batch Buoy Single Channel
            self.path_dictionary['relative_output_log_path'] = os.path.join(self.path_dictionary['relative_output_log_path'], 'batch')
            self.process_batch_buoy_sc(master)
            
        
    # Add process button
    def add_process_button(self, master):
        
        self.process_button = ttk.Button(master.frames[self.frame_name], text = "Process")
        self.process_button.pack(anchor = 'e', padx = 10, pady = (0, 10))
        
        self.process_button.config(command = lambda: self.process_active_tab(master))
        
    
    # Delete the specififed file
    def delete_file(self, absolute_path_and_file_name):
        
        # Test if the file exists before deleting it
        file_exists = test_paths.main([absolute_path_and_file_name, "-tfile"])
        
        if file_exists:
            os.unlink(absolute_path_and_file_name)# unlink is ux version of delete
    
    
    # Used to step the progressbar
    def step_progressbar(self):
                    
        while not self.process_complete:
            
            self.progressbar.progressbar.step()
            time.sleep(0.02)
            
            
        self.progressbar.progressbar_window.destroy()
        
        self.process_button.config(state = 'normal')
        
    
    # Create the watchdogs that watch the log files which are used to provide feedback to the user in the GUI
    def create_watchdogs(self, master, statusfile_absolute_path, outputfile_absolute_path):
        
        from gui.tools.file_watcher import File_Watcher
        # Instantiate the watcher and pass the master object (containing required functions) and path to file
        self.status_watchdog = File_Watcher(master, statusfile_absolute_path)
        self.output_watchdog = File_Watcher(master, outputfile_absolute_path)
        
        self.status_watchdog.event_notifier.start()
        self.output_watchdog.event_notifier.start()
        
    
    # Destroy the watchdog agents
    def kill_watchdogs(self):
        
        self.status_watchdog.event_notifier.stop()
        self.output_watchdog.event_notifier.stop()
        
        
    # Build/Define the path variables as used by the program
    def build_paths(self, master):
        
        # Create status logger instance paths
        self.path_dictionary['statusfile_relative_path_and_filename'] = os.path.join(
                self.path_dictionary['relative_status_log_path'], 
                self.path_dictionary['statusfile_name']
        )        
        self.path_dictionary['statusfile_absolute_path'] = os.path.join(
                master.project_root,
                self.path_dictionary['relative_status_log_path']
        )        
        self.path_dictionary['statusfile_absolute_path_and_filename'] = os.path.join(
                master.project_root,
                self.path_dictionary['statusfile_relative_path_and_filename']
        )
        
        # Create a output logger instance paths
        self.path_dictionary['outputfile_relative_path_and_filename'] = os.path.join(
                self.path_dictionary['relative_output_log_path'], 
                self.path_dictionary['outputfile_name']
        )
        self.path_dictionary['outputfile_absolute_path'] = os.path.join(
                master.project_root, 
                self.path_dictionary['relative_output_log_path']
        )
        self.path_dictionary['outputfile_absolute_path_and_filename'] = os.path.join(
                master.project_root,
                self.path_dictionary['outputfile_relative_path_and_filename']
        )
    
    
    # Delete the log files used to provide feedback to the user in the GUI
    def clear_watch_files(self, master):
        
        self.delete_file(self.path_dictionary['statusfile_absolute_path_and_filename'])
        self.delete_file(self.path_dictionary['outputfile_absolute_path_and_filename'])
        
    
    # Convert a value to a float
    def convert_to_float(self, value):
        
        try:
            value = float(value)
        except ValueError:
            print("Invalid lat")
            
        return value
    
    
    # Process a scene id
    def process_scene_id(self, master, scene_id, show_images):
        
        self.create_watchdogs(
                master, 
                self.path_dictionary['statusfile_absolute_path'], 
                self.path_dictionary['outputfile_absolute_path']
        )
        
        Model(
             'tarca_gui',
             'single',
             'sc',
             'buoy',
             scene_id,
             'merra',
             show_images,
             master.project_root,
             False,
             None,
             self.path_dictionary['statusfile_absolute_path_and_filename'], 
             self.path_dictionary['outputfile_absolute_path_and_filename']
        )
        
        self.process_complete = True
        
        self.kill_watchdogs()
        
        self.clear_watch_files(master)
        
        
    # Process split window
    def process_lst_sw(self, master, scene_id, show_images, partial_data):
        
        self.create_watchdogs(
                master, 
                self.path_dictionary['statusfile_absolute_path'], 
                self.path_dictionary['outputfile_absolute_path']
        )
        
        Model(
             'tarca_gui',
             'single',
             'sw',
             'lst',
             scene_id,
             'merra',
             show_images,
             master.project_root,
             False,
             partial_data,
             self.path_dictionary['statusfile_absolute_path_and_filename'], 
             self.path_dictionary['outputfile_absolute_path_and_filename']
        )
                
        self.process_complete = True
        
        self.kill_watchdogs()
        
        self.clear_watch_files(master)
        
    
    # Perform a partial operation where the user provides lat, lon, surface temperature(Ts)
    def process_toa_sc(self, master, scene_id, show_images, partial_data):
                
        self.create_watchdogs(
                master, 
                self.path_dictionary['statusfile_absolute_path'], 
                self.path_dictionary['outputfile_absolute_path']
        )
        
        Model(
             'tarca_gui',
             'single',
             'sc',
             'toa',
             scene_id,
             'merra',
             show_images,
             master.project_root,
             False,
             partial_data,
             self.path_dictionary['statusfile_absolute_path_and_filename'], 
             self.path_dictionary['outputfile_absolute_path_and_filename']
        )
        
        self.process_complete = True
        
        self.kill_watchdogs()
        
        self.clear_watch_files(master)
        
    
    # Process a batch of ID's
    def process_batch_buoy_sc_ids(self, master, source_file, show_images):
        
        self.create_watchdogs(
                master,
                self.path_dictionary['statusfile_absolute_path'],
                self.path_dictionary['outputfile_absolute_path']
        )
        
        Model(
             'tarca_gui',
             'batch',
             'sc',
             'buoy',
             source_file,
             'merra',
             show_images,
             master.project_root,
             False,
             None,
             self.path_dictionary['statusfile_absolute_path_and_filename'], 
             self.path_dictionary['outputfile_absolute_path_and_filename']
        )
        
        self.process_complete = True
        
        self.kill_watchdogs()
    
        self.clear_watch_files(master)
        
        
    # Clean the output areas and disable the button
    def prepare_window(self, master):
        
        # Disable the process button
        self.process_button.config(state = 'disabled')
        
        # Clear the output frames (output andn status)
        master.frames['status_frame'].widgets['status_text'].delete('1.0', 'end')
        master.frames['output_frame'].widgets['output_text'].delete('1.0', 'end')
        
        
    # Ask the user if they want to see each image as it is processed
    def ask_show_images(self):
        
        show_images = messagebox.askyesno(
                title = "Display Images",
                message = "Do you wish to display each image as it is processing?")
    
        return show_images
        
        
    # Define process for processing a single scene of Buoy Top of Atmosphere Radiance using Single Channel
    def process_single_buoy_sc(self, master):
        
        # Clear output windows and disable process button
        self.prepare_window(master)
        
        # Read the scene_id from the form
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_buoy_sc_frame'].input_values['scene_id'].get()
        
        if (scene_id != None):
        
            if (menu.is_valid_id(scene_id)):
                
                #  !!! Temporarily disabled due to multithreading issues with GTK+ !!!
                show_images = False #self.ask_show_images()
            
                # Create a status logger instance
                self.path_dictionary['statusfile_name'] = str(scene_id) + "_" + str(self.current_datetime) + ".status"

                # Create a output logger instance
                self.path_dictionary['outputfile_name'] = str(scene_id) + "_" + str(self.current_datetime) + ".output"
            
                self.build_paths(master)
                
                # Create a progress bar to show activity
                self.progressbar = Progress_Bar(master, 'Processing Scene ' + scene_id)
                self.progressbar.progressbar.config(mode = 'indeterminate')
                
                # Progressbar start and stop work with program loop, so manual loop is required for progression
                self.process_complete = False
                
#                self.process_scene_id(master, scene_id, show_images)
                progressbar_thread = threading.Thread(target = self.step_progressbar)
                progressbar_thread.start()
                
                # Launch single scene ID process job in own thread
                cis_tarca_thread = threading.Thread(
                        target = self.process_scene_id, args = (
                                [master, 
                                 scene_id, 
                                 show_images, ]
                        )
                )
                        
                cis_tarca_thread.start()
                                
            else:
                
                messagebox.showwarning(
                        title = "Invalid Input",
                        message = "The scene id you entered is of an incorrect format.\n\n"
                                    "Please try again")
                
                self.process_button.config(state = 'normal')

    
    # Define process for batch processing Buoy Top of Atmosphere Radiance using Single Channel
    def process_batch_buoy_sc(self, master):
        
        # Clear output windows and disable process button
        self.prepare_window(master)
                
        # Get the batch file from the form
        source_file = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_batch_frame'].input_values['batch_file'].get()
        source_file_name = source_file[(source_file.rfind('/') + 1):]
        
        
        if (source_file == ''):
            messagebox.showwarning(
                title = "Invalid Input",
                message = "No file specified, please select a file and try again.")
            
            self.process_button.config(state = 'normal')
            
        else:
            # Read in the file
            scenes = open(source_file).readlines()
            
            counter = 0
            error_list = {"errors":[]}
            
            for scene in scenes:
                
                counter += 1
                
                if not menu.is_valid_id(scene):
                    
                    error = {}
                    error["idx"] = counter
                    error["scene"] = scene
                    
                    error_list["errors"].append(error)
            
            
            if (len(error_list['errors']) > 0):
                
                asterisk = '*'
                nr_asterisks = 65
                
                space = ' '
                nr_spaces = 5
                
                header1 = ''.join([char*nr_asterisks for char in asterisk])
                header1 += '\n'
                header2 = ''.join([char*nr_spaces for char in space])
                header2 += '!!!   The following errors were found in your batch file   !!!'
                header2 += ''.join([char*nr_spaces for char in space])
                header2 += '\n'
                header3 = ''.join([char*nr_asterisks for char in asterisk])
                
                message_header = header1 + header2 + header3
                                
                message_body = ""
                
                for error in error_list['errors']:
                    message_body = message_body + "  line : %5s         scene : %40s\n" % (error['idx'], error['scene'])
                
                message_body = message_body[:-2]
                
                Error_Window(master, "batch_error_window", "Batch File Errors", message_header, message_body)
                
                
                self.process_button.config(state = 'normal')
                    
            else:                
            
                if (len(scenes) > 0):
                    
                    # Ask user if they want to display each image during processing
                    #  !!! Temporarily disabled due to multithreading issues with GTK+ !!!
                    show_images = False #self.ask_show_images()
                    
                    # Define a status logger file
                    self.path_dictionary['statusfile_name'] = source_file[source_file.rfind('/') + 1:source_file.rfind('.')] + "_" + str(self.current_datetime) + ".status"
                    
                    # Define a output logger file
                    self.path_dictionary['outputfile_name'] = source_file[source_file.rfind('/') + 1:source_file.rfind('.')] + "_" + str(self.current_datetime) + ".output"
                    
                    # Define all logger paths
                    self.build_paths(master)
                
                    # Create a progress bar to show activity
                    self.progressbar = Progress_Bar(master, 'Processing Batch: ' + source_file_name)
                    self.progressbar.progressbar.config(mode = 'indeterminate')
                    
                    # Progressbar start and stop work with program loop, so manual loop is required for progression
                    self.process_complete = False
                    
                    progressbar_thread = threading.Thread(target = self.step_progressbar)
                    progressbar_thread.start()
                    
                    # Launch single scene ID process job in own thread
                    cis_tarca_thread = threading.Thread(
                            target = self.process_batch_buoy_sc_ids, args = (
                                    [master, 
                                     source_file, 
                                     show_images, ]
                            )
                    )
                            
                    cis_tarca_thread.start()
                                    
                else:
                    
                    messagebox.showwarning(
                            title = "Invalid Input",
                            message = "The file you specified is empty, please select a non-empty file.")
                    
                    self.process_button.config(state = 'normal')
    
    
    # Define process for Top of Atmosphere Radiance data using Single Channel and manual input values
    def process_single_toa_sc(self, master, bands=[10, 11]):

        # Keep track of all the invalid entries
        error_message_list = {
                'scene_id': ' is not a valid Scene ID',
                'skin_temp': ' does not fall within the range of 200 to 350 kelvin for a valid skin temperature',
                'lat': ' does not fall within the range of -90 to 90 degrees for a valid latitude',
                'lon': ' does not fall within the range of -180 to 180 degrees for a valid longitude',
                'emis_b10': ' does not fall within the range of 0.8 to 1.0 for a valid emissivity',
                'emis_b11': ' does not fall within the range of 0.8 to 1.0 for a valid emissivity'
            }
        
        error_list = {}
        
        # Clear output windows and disable process button
        self.prepare_window(master)
        
        # Define dictionary for required values
        partial_data = {}
                
        # Read the scene_id from the form
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['scene_id'].get()
        partial_data['skin_temp'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['surface_temp'].get()
        partial_data['lat'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['lat'].get()
        partial_data['lon'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['lon'].get()
        partial_data['emis_b10'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['emissivity_b10'].get()
        partial_data['emis_b11'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_toa_sc_frame'].input_values['emissivity_b11'].get()
        
        partial_data['skin_temp'] = self.convert_to_float(partial_data['skin_temp'])
        partial_data['lat'] = self.convert_to_float(partial_data['lat'])
        partial_data['lon'] = self.convert_to_float(partial_data['lon'])
        partial_data['emis_b10'] = self.convert_to_float(partial_data['emis_b10'])
        partial_data['emis_b11'] = self.convert_to_float(partial_data['emis_b11'])
        
        
        # Check if the scene id is valid
        if (scene_id != None):        
            if not menu.is_valid_id(scene_id):
                
                error_list['scene_id'] = scene_id
        
        # Check if the skin temperature is valid
        if (partial_data['skin_temp'] != None):
            if not menu.is_valid_temp(partial_data['skin_temp']):
                
                error_list['skin_temp'] = partial_data['skin_temp']  
        
        # Check if the latitude is valid
        if (partial_data['lat'] != None):
            if not menu.is_valid_latitude(partial_data['lat']):
                
                error_list['lat'] = partial_data['lat']
                
        # Check if the longitude is valid
        if (partial_data['lon'] != None):
            if not menu.is_valid_longitude(partial_data['lon']):
                    
                error_list['lon'] = partial_data['lon']
                
                
        # Check if the emissivity for band 10 is valid
        if (partial_data['emis_b10'] != None):
            if not menu.is_valid_emissivity(partial_data['emis_b10']):
                
                error_list['emis_b10'] = partial_data['emis_b10']
                
                
        # Check if the emissivity for band 11 is valid
        if (partial_data['emis_b11'] != None):
            if not menu.is_valid_emissivity(partial_data['emis_b11']):
                
                error_list['emis_b11'] = partial_data['emis_b11']
                
        
        if len(error_list) == 0:
            
            # Create a status logger instance
            self.path_dictionary['statusfile_name'] = str(scene_id) + "_" + str(self.current_datetime) + ".status"

            # Create a output logger instance
            self.path_dictionary['outputfile_name'] = str(scene_id) + "_" + str(self.current_datetime) + ".output"
        
            self.build_paths(master)
            
            # Create a progress bar to show activity
            self.progressbar = Progress_Bar(master, 'Processing Scene ' + scene_id)
            self.progressbar.progressbar.config(mode = 'indeterminate')
            
            # Progressbar start and stop work with program loop, so manual loop is required for progression
            self.process_complete = False
            
            progressbar_thread = threading.Thread(target = self.step_progressbar)
            progressbar_thread.start()
                
            # Launch single scene ID process job in own thread
            cis_tarca_thread = threading.Thread(
                    target = self.process_toa_sc, args = (
                            [master,
                             scene_id,
                             False,
                             partial_data, ]
                    )
            )
                    
            cis_tarca_thread.start()
            
        else:
            
            asterisk = '*'
            nr_asterisks = 65
            
            space = ' '
            nr_spaces = 5
            
            header1 = ''.join([char*nr_asterisks for char in asterisk])
            header1 += '\n'
            header2 = ''.join([char*nr_spaces for char in space])
            header2 += '!!!   The following data you entered is incorrect.   !!!'
            header2 += ''.join([char*nr_spaces for char in space])
            header2 += '\n'
            header3 = ''.join([char*nr_asterisks for char in asterisk])
            
            message_header = header1 + header2 + header3
                            
            message_body = ""
            
            for error in error_list:
                
                if error_list[error] == '':
                    message_body += "You did not enter a value for %s\n" % error
                else:
                    message_body += "%s %s\n" % (error_list[error], error_message_list[error])
           
            Error_Window(master, "partial_single_error_window", "Data Input Errors", message_header, message_body)
            
            self.process_button.config(state = 'normal')
            

    # Define process for Land Surface Temperature using Split Window
    def process_single_lst_sw(self, master):
        
        # Keep track of all the invalid entries
        error_message_list = {
                'scene_id': ' is not a valid Scene ID',
                'lat': ' does not fall within the range of -90 to 90 degrees for a valid latitude',
                'lon': ' does not fall within the range of -180 to 180 degrees for a valid longitude',
                'emis_b10': ' does not fall within the range of 0.8 to 1.0 for a valid emissivity',
                'emis_b11': ' does not fall within the range of 0.8 to 1.0 for a valid emissivity'
            }
        
        error_list = {}
        
        # Clear output windows and disable process button
        self.prepare_window(master)
        
        # Define dictionary for required values
        partial_data = {}
        
        # Read the scene_id from the form
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['scene_id'].get()
        partial_data['lat'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['lat'].get()
        partial_data['lon'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['lon'].get()
        partial_data['emis_b10'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['emissivity_b10'].get()
        partial_data['emis_b11'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['emissivity_b11'].get()
        
        # There is no .get() method for the ttk.Checkbutton object, therefore an even listener is added to the element 
        # and the value in the variable changed based on the "change" event from the checkbutton
        partial_data['add_gain_bias'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].input_values['add_gain_bias']
        
        # Convert all entered data to float values
        partial_data['lat'] = self.convert_to_float(partial_data['lat'])
        partial_data['lon'] = self.convert_to_float(partial_data['lon'])
        partial_data['emis_b10'] = self.convert_to_float(partial_data['emis_b10'])
        partial_data['emis_b11'] = self.convert_to_float(partial_data['emis_b11'])
        
        if partial_data['add_gain_bias']:
            partial_data['gain_b10'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].frames['input_lst_sw_gb_frame'].input_values['gain_b10'].get()
            partial_data['bias_b10'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].frames['input_lst_sw_gb_frame'].input_values['bias_b10'].get()
            partial_data['gain_b11'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].frames['input_lst_sw_gb_frame'].input_values['gain_b11'].get()
            partial_data['bias_b11'] = master.frames[self.frame_name].notebooks['input_notebook'].frames['input_lst_sw_frame'].frames['input_lst_sw_gb_frame'].input_values['bias_b11'].get()
            
            partial_data['gain_b10'] = self.convert_to_float(partial_data['gain_b10'])
            partial_data['bias_b10'] = self.convert_to_float(partial_data['bias_b10'])
            partial_data['gain_b11'] = self.convert_to_float(partial_data['gain_b11'])
            partial_data['bias_b11'] = self.convert_to_float(partial_data['bias_b11'])
        else:
            partial_data['gain_b10'] = 0
            partial_data['bias_b10'] = 0
            partial_data['gain_b11'] = 0
            partial_data['bias_b11'] = 0
        
        # Check if the scene id is valid
        if (scene_id != None):
            if not menu.is_valid_id(scene_id):
                
                error_list['scene_id'] = scene_id
        
        # Check if the latitude is valid
        if (partial_data['lat'] != None):
            if not menu.is_valid_latitude(partial_data['lat']):
                
                error_list['lat'] = partial_data['lat']
                
        # Check if the longitude is valid
        if (partial_data['lon'] != None):
            if not menu.is_valid_longitude(partial_data['lon']):
                    
                error_list['lon'] = partial_data['lon']
        
        # Check if the emissivity for band 10 is valid
        if (partial_data['emis_b10'] != None):
            if False:
                error_list['emis_b10'] = partial_data['emis_b10']
                
        # Check if the emissivity for band 11 is valid
        if (partial_data['emis_b11'] != None):
            if False:
                error_list['emis_b11'] = partial_data['emis_b11']
                
        if len(error_list) == 0:
            
            # Create a status logger instance
            self.path_dictionary['statusfile_name'] = "Split_Window_" + str(self.current_datetime) + ".status"

            # Create a output logger instance
            self.path_dictionary['outputfile_name'] = "Split_Window_" + str(self.current_datetime) + ".output"
        
            self.build_paths(master)
            
            # Create a progress bar to show activity
            self.progressbar = Progress_Bar(master, 'Processing... ')
            self.progressbar.progressbar.config(mode = 'indeterminate')
            
            # Progressbar start and stop work with program loop, so manual loop is required for progression
            self.process_complete = False
            
            progressbar_thread = threading.Thread(target = self.step_progressbar)
            progressbar_thread.start()
                
            # Launch single process job in own thread
            cis_tarca_thread = threading.Thread(
                    target = self.process_lst_sw, args = (
                            [master,
                             scene_id,
                             False,
                             partial_data, ]
                    )
            )
                    
            cis_tarca_thread.start()
            
        else:
            
            asterisk = '*'
            nr_asterisks = 65
            
            space = ' '
            nr_spaces = 5
            
            header1 = ''.join([char*nr_asterisks for char in asterisk])
            header1 += '\n'
            header2 = ''.join([char*nr_spaces for char in space])
            header2 += '!!!   The following data you entered is incorrect.   !!!'
            header2 += ''.join([char*nr_spaces for char in space])
            header2 += '\n'
            header3 = ''.join([char*nr_asterisks for char in asterisk])
            
            message_header = header1 + header2 + header3
                            
            message_body = ""
            
            for error in error_list:
                
                if error_list[error] == '':
                    message_body += "You did not enter a value for %s\n" % error
                else:
                    message_body += "%s %s\n" % (error_list[error], error_message_list[error])
           
            Error_Window(master, "partial_single_error_window", "Data Input Errors", message_header, message_body)
            
            self.process_button.config(state = 'normal')