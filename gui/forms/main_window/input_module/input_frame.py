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
from buoycalib import (sat, atmo, radiance, modtran, settings)
from gui.forms.general.progress_bar import Progress_Bar
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
from gui.forms.main_window.input_module.input_notebook import Input_Notebook
from gui.forms.general.error_module.error_window import Error_Window
import menu
import forward_model
import forward_model_batch
import os, sys
import numpy
import warnings
from modules.stp.sw.split_window import Split_Window
import pdb


class Input_Frame(Gui_Label_Frame):
    
    # Input Frame constructor
    def __init__(self, master):
                
        self.path_dictionary = {
                'relative_status_path': 'logs/status/batch',
                'relative_output_path': 'logs/output/single',
                'statusfile_name': '',
                'statusfile_relative_path_and_filename': '',
                'statusfile_absolute_path': '',
                'parameterized_statusfile': '',
                'outputfile_name': '',
                'outputfile_relative_path_and_filename': '',
                'outputfile_absolute_path': '',
                'parameterized_outputfile': ''
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
        
        if (active_tab == 0):
            self.process_full_single(master)
        elif (active_tab == 1):
            self.process_partial_single(master)
        elif (active_tab == 2):
            self.process_batch(master)
            
        
    # Add process button
    def add_process_button(self, master):
        
        self.process_button = ttk.Button(master.frames[self.frame_name], text = "Process")
        self.process_button.pack(anchor = 'e', padx = 10, pady = (0, 10))
        
        self.process_button.config(command = lambda: self.process_active_tab(master))
        
        
    def delete_log_files(self, file_absolute_path, file_name):
        
        os.unlink(os.path.join(file_absolute_path, file_name))# unlink is ux version of delete
    
        
    def step_progressbar(self):
                    
        while not self.process_complete:
            
            self.progressbar.progressbar.step()            
            time.sleep(0.02)
            
            
        self.progressbar.progressbar_window.destroy()
        
        self.process_button.config(state = 'normal')
        
    
    def create_watchdogs(self, master, statusfile_absolute_path, outputfile_absolute_path):
        
        from gui.tools.file_watcher import File_Watcher
        # Instantiate the watcher and pass the master object (containing required functions) and path to file
        self.status_watchdog = File_Watcher(master, statusfile_absolute_path)
        self.output_watchdog = File_Watcher(master, outputfile_absolute_path)
        
        self.status_watchdog.event_notifier.start()
        self.output_watchdog.event_notifier.start()
        
    
    def kill_watchdogs(self):
        
        self.status_watchdog.event_notifier.stop()
        self.output_watchdog.event_notifier.stop()
        
        
    def build_paths(self, master):
        
        # Create status logger instance paths
        self.path_dictionary['statusfile_relative_path_and_filename'] = os.path.join(
                self.path_dictionary['relative_status_path'], 
                self.path_dictionary['statusfile_name']
        )        
        self.path_dictionary['statusfile_absolute_path'] = os.path.join(
                master.project_root,
                self.path_dictionary['relative_status_path']
        )        
        self.path_dictionary['parameterized_statusfile'] = ("-t" + self.path_dictionary['statusfile_relative_path_and_filename'])
        
        # Create a output logger instance paths
        self.path_dictionary['outputfile_relative_path_and_filename'] = os.path.join(
                self.path_dictionary['relative_output_path'], 
                self.path_dictionary['outputfile_name']
        )
        self.path_dictionary['outputfile_absolute_path'] = os.path.join(
                master.project_root, 
                self.path_dictionary['relative_output_path']
        )
        self.path_dictionary['parameterized_outputfile'] = ("-u" + self.path_dictionary['outputfile_relative_path_and_filename'])
    
    
    def clear_watch_files(self, master):#, statusfile_absolute_path, statusfile_name, outputfile_absolute_path, outputfile_name):
        
        self.delete_log_files(self.path_dictionary['statusfile_absolute_path'], self.path_dictionary['statusfile_name'])
        self.delete_log_files(self.path_dictionary['outputfile_absolute_path'], self.path_dictionary['outputfile_name'])
        
    
    def convert_to_float(self, value):
        
        try:
            value = float(value)
        except ValueError:
            print("Invalid lat")
            
        return value
    
    def process_scene_id(self, master, scene_id, show_images):
        
        self.create_watchdogs(
                master, 
                self.path_dictionary['statusfile_absolute_path'], 
                self.path_dictionary['outputfile_absolute_path']
        )
        
        forward_model.main([
                scene_id,
                show_images,
                "-ctarca_gui",
                ('-d' + master.project_root),
                self.path_dictionary['parameterized_statusfile'],
                self.path_dictionary['parameterized_outputfile']
        ])
        
        self.process_complete = True
        
        self.kill_watchdogs()
        
        self.clear_watch_files(master)
        
    
    def process_batch_ids(self, master, source_file, show_images):
        
        self.create_watchdogs(
                master,
                self.path_dictionary['statusfile_absolute_path'],
                self.path_dictionary['outputfile_absolute_path']
        )
        
        forward_model_batch.main([
                source_file,
                show_images,
                "-ctarca_gui_batch",
                ('-d' + master.project_root),
                self.path_dictionary['parameterized_statusfile'],
                self.path_dictionary['parameterized_outputfile']
        ])
        
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
        
        
    # Define process for full_single
    def process_full_single(self, master):
        
        # Clear output windows and disable process button
        self.prepare_window(master)
        
        # Read the scene_id from the form
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].input_values['scene_id_full_single'].get()
        
        if (scene_id != None):
        
            if (menu.is_valid_id(scene_id)):
                
                show_images = self.ask_show_images()
            
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
    
    
    def ask_show_images(self):
        
        show_images = messagebox.askyesno(
                title = "Display Images",
                message = "Do you wish to display each image as it is processing?")
        
        if show_images == True:
            show_images ='-ntrue'
        else:
            show_images = '-nfalse'
    
        return show_images
    
    
    # Define process for partial_single
    def process_partial_single(self, master, bands=[10, 11]):

        # Clear output windows and disable process button
        self.prepare_window(master)
        
        # Read the scene_id from the form
        scene_id = master.frames[self.frame_name].notebooks['input_notebook'].input_values['scene_id_partial_single'].get()
        lat = master.frames[self.frame_name].notebooks['input_notebook'].input_values['lat'].get()
        lon = master.frames[self.frame_name].notebooks['input_notebook'].input_values['lon'].get()
        emissivity_b10 = master.frames[self.frame_name].notebooks['input_notebook'].input_values['emissivity_b10'].get()
        emissivity_b11 = master.frames[self.frame_name].notebooks['input_notebook'].input_values['emissivity_b11'].get()
        skin_temp = master.frames[self.frame_name].notebooks['input_notebook'].input_values['surface_temp'].get()
        
        lat = self.convert_to_float(lat)
        lon = self.convert_to_float(lon)
        emissivity_b10 = self.convert_to_float(emissivity_b10)
        emissivity_b11 = self.convert_to_float(emissivity_b11)
        skin_temp = self.convert_to_float(skin_temp)
        
        overpass_date, directory, metadata, file_downloaded = sat.landsat.download(scene_id, bands[:])
        
        atmosphere = atmo.merra.process(overpass_date, lat, lon)
        
        # MODTRAN
        modtran_directory = '{0}/{1}'.format(settings.MODTRAN_GUI_DIR, scene_id)
        wavelengths, upwell_rad, gnd_reflect, transmission = modtran.process(atmosphere,lat, lon, overpass_date, modtran_directory, skin_temp)
        
        # LTOA calcs
        mod_ltoa_spectral = radiance.calc_ltoa_spectral(wavelengths, upwell_rad, gnd_reflect, transmission, skin_temp)

        img_ltoa = {}
        mod_ltoa = {}
        rsrs = {b:settings.RSR_L8[b] for b in bands}
        
        try:
            for b in bands:
                RSR_wavelengths, RSR = numpy.loadtxt(rsrs[b], unpack=True)
                img_ltoa[b] = sat.landsat.calc_ltoa(directory, metadata, lat, lon, b)
                mod_ltoa[b] = radiance.calc_ltoa(wavelengths, mod_ltoa_spectral, RSR_wavelengths, RSR)
        except RuntimeError as e:
            warnings.warn(str(e), RuntimeWarning)
        
        # split window
        sw = Split_Window(img_ltoa[10], img_ltoa[11], emissivity_b10, emissivity_b11)
        
        pdb.set_trace()
            
    
    # Define process for batch
    def process_batch(self, master):
        
        # Clear output windows and disable process button
        self.prepare_window(master)
                
        # Get the batch file from the form
        source_file = master.frames[self.frame_name].notebooks['input_notebook'].input_values['batch_file'].get()
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
                sys.stdout.write("NO ERRORS!!! \n")
            
            
                self.process_button.config(state = 'normal')
                
            
                if (len(scenes) > 0):
                    
                    # Ask user if they want to display each image during processing
                    show_images = self.ask_show_images()
                    
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
                            target = self.process_batch_ids, args = (
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
