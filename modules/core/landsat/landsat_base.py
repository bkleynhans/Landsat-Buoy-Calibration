#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Base module for entire landsat-based program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 5, 2019
# Filename            : landsat_base.py
#
###

# Imports
import sys, os, pdb
import cv2, threading
import numpy
from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)
from tools.display_image import Display_Image
from tools import test_paths
from modules.core import model
from tools.spinner import Spinner

class Landsat_Base():
    
    BANDS = [10, 11]
    
    # Constructor
    def __init__(self, args):

        self.data = {}
        self.args = args
        self.args['threads'] = []
        
        # Partial single and partial batch processes don't use buoys for calculation
        if (self.args['process'] == 'toa') or (self.args['process'] == 'lst'):
            self.buoys = None
    

    # Acquire, save and display image if requested
    def download_image(self, scene_id):
        
        self.args['scene_id'] = scene_id        
        self.data[self.args['scene_id']] = {}
        
        # Set the arguments according to the requirements of the module calling the function
        # menu --> terminal
        # tarca_gui --> tkinter gui
        if self.args['caller'] == 'menu':
            self.shared_args = {
                'log_status': None,
                'log_output': None,
                'caller': self.args['caller'],
                'scene_filename': '',
                'bands': self.BANDS
            }            
        elif self.args['caller'] == 'tarca_gui':
            self.shared_args = {
                'log_status': self.args['status_logger'],
                'log_output': self.args['output_logger'],
                'caller': self.args['caller'],
                'scene_filename': '',
                'bands': self.BANDS
            }

        # Download the image file and read the metadata into self.image_data
        self.image_data = display.landsat_preview(scene_id, '', self.shared_args)
        
        # Checks if the user wanted to have the images displayed
        if self.args['display_image']:
            image_data = {
                    'title': self.args['scene_id'],
                    'image': self.image_data['image']
                }
            
            # Open the image in a new window using a thread
            self.args['threads'].append(Display_Image(image_data))
        
        image_file = '{0}.tif'.format(self.args['scene_id'])
        image_directory = os.path.join(self.args['output_directory'], 'processed_images')
        absolute_image_directory = os.path.join(self.args['project_root'], image_directory)
        absolute_image_path = os.path.join(absolute_image_directory, image_file)
        cv2.imwrite(absolute_image_path, self.image_data['image'])
        

    # Perform required processing on each buoy in the list
    def process_buoys(self):
        
        self.buoy_process_monitor = dict.fromkeys(self.buoys, False)
        
        # Process one buoy at a time
        for buoy_id in self.buoys:

            if self.args['caller'] == 'menu':
                self.buoy_process_monitor[buoy_id] = Spinner()
                
                self.args['threads'].append(self.buoy_process_monitor[buoy_id])
            
            self.buoy_processor(buoy_id)
        
# -->> NOT THIS
#        # Process all buoys using threads !!! This section is WIP.  This section can be enabled with the previous section
#            disabled, but it messes up the process output !!!
#        buoy_threads = []
#        
#        for buoy_id in self.buoys:
#            new_thread = threading.Thread(target = self.buoy_processor, args=[buoy_id, ])
#            buoy_threads.append(new_thread)
#            
#        for thread in buoy_threads:
#            thread.start()
#            
#        for thread in buoy_threads:
#            thread.join()
# -->> NOT THIS
    
    # Add to log for functions that are part of this OOP design
    def log(self, log_type, log_text, add_newline = True):
        
        sys.stdout.write('\n')
        
        if (self.args['caller'] == 'menu'):
            
            sys.stdout.write("\r" + log_text)
        
        elif (self.args['caller'] == 'tarca_gui'):
            if log_type == 'status':
                self.args['status_logger'].write(log_text, add_newline)
            elif log_type == 'output':
                self.args['output_logger'].write(log_text, add_newline)
                    
        sys.stdout.flush
    
    
    # Processes the buoys, one at a time
    def buoy_processor(self, buoy_id):
        
        # Displays the number of the buoy that is being processed
        self.log('status', "\n   Processing buoy %s  " % (buoy_id))
        
        # Displays a progress spinner behind the buoy if it was called from the menu
        if self.args['caller'] == 'menu':
            self.buoy_process_monitor[buoy_id].start_spinner()
        
        try :
            # User status update
            self.log('status', "     Downloading buoy data file... ")
            
            self.buoy_file = buoy.download(buoy_id, self.image_data['overpass_date'], self.shared_args)
            
            # User status update
            self.log('status', "     Extracting buoy metadata for buoy %s  " % (buoy_id))
            
            self.buoy_data = buoy.info(buoy_id, self.buoy_file, self.image_data['overpass_date'])
            
        except download.RemoteFileException:
#             warnings.warn('Buoy {0} does not have data for this date.'.format(buoy_id), RuntimeWarning)
             
            self.data[self.args['scene_id']][buoy_id] = (
                     buoy_id,
                     0,
                     0,
                     0,
                     0,
                     {10:0,11:0},
                     {10:0,11:0},
                     {10:0,11:0},
                     self.image_data['overpass_date'],
                     'failed',
                     'file'
                )
            
            if self.args['caller'] == 'menu':
                self.buoy_process_monitor[buoy_id].stop_spinner()
            
            return
         
        except buoy.BuoyDataException as e:
#             warnings.warn(str(e), RuntimeWarning)
             
            self.data[self.args['scene_id']][buoy_id] = (
                     buoy_id,
                     0,
                     0,
                     0,
                     0,
                     {10:0,11:0},
                     {10:0,11:0},
                     {10:0,11:0},
                     self.image_data['overpass_date'],
                     'failed',
                     str(e)
                )

            if self.args['caller'] == 'menu':
                self.buoy_process_monitor[buoy_id].stop_spinner()
            
            return
        
        # User status update
        self.log('status', "      Calculating atmospheric data...\n")
        
        try:
            # Pass in parameters directly because calculate_atmosphere receives requests from other sources also
            self.calculate_atmosphere(
                    self.args['atmo_source'],
                    self.image_data['overpass_date'],
                    self.buoy_data['buoy_lat'],
                    self.buoy_data['buoy_lon'],
                    self.args['verbose']
                )
        except ValueError as e:
            self.data[self.args['scene_id']][buoy_id] = (
                    buoy_id,
                     0,
                     0,
                     0,
                     0,
                     {10:0,11:0},
                     {10:0,11:0},
                     {10:0,11:0},
                     self.image_data['overpass_date'],
                     'failed',
                     str(e)
                )
            
            return
       
        modtran_output_file = '{0}_{1}'.format(self.args['scene_id'], buoy_id)
        
        # User status update
        self.log('status', "      Calculating Top of Atmosphere Radiance using MODTRAN ")
        
        # Pass in paramteres directly because run_modtran receives requests from other sources also
        modtran_data = self.run_modtran(
                settings.MODTRAN_BASH_DIR,
                modtran_output_file,
                self.buoy_data['buoy_lat'],
                self.buoy_data['buoy_lon'],
                self.image_data['overpass_date'],
                self.buoy_data['skin_temp']
            )
        
        img_ltoa = {}
        mod_ltoa = {}
        
        try:
            # Pass in parameters directly because run_ltao receives requests from other sources also
            img_ltoa, mod_ltoa = self.run_ltoa(
                    modtran_data,
                    img_ltoa,
                    mod_ltoa,
                    self.buoy_data['skin_temp'],
                    self.buoy_data['buoy_lat'],
                    self.buoy_data['buoy_lon']
                )
            
        except RuntimeError as e:
            self.data[self.args['scene_id']][buoy_id] = (
                    buoy_id,
                     0,
                     0,
                     0,
                     0,
                     {10:0,11:0},
                     {10:0,11:0},
                     {10:0,11:0},
                     self.image_data['overpass_date'],
                     'failed',
                     str(e)
                )
            
            return
        
        error = error_bar.error_bar(
            None,
            self.args['scene_id'], 
            buoy_id,
            self.buoy_data['skin_temp'],
            0.305,
            self.image_data['overpass_date'],
            self.buoy_data['buoy_lat'],
            self.buoy_data['buoy_lon'],
            self.rsrs,
            self.BANDS,
            self.shared_args
        )
        
        self.data[self.args['scene_id']][buoy_id] = (
                    buoy_id,
                    self.buoy_data['bulk_temp'],
                    self.buoy_data['skin_temp'],
                    self.buoy_data['buoy_lat'],
                    self.buoy_data['buoy_lon'],
                    mod_ltoa,
                    error,
                    img_ltoa,
                    self.image_data['overpass_date'],
                    'success',
                    ''
                )
        
        if self.args['caller'] == 'menu':
            self.buoy_process_monitor[buoy_id].stop_spinner()
        
    
    # Calculates the atmosphere based on supplied data
    def calculate_atmosphere(self, source, overpass_date, lat, lon, verbose = False):
        
        # Atmosphere
        if source == 'merra':
            self.atmosphere = atmo.merra.process(
                    overpass_date,
                    lat,
                    lon,
                    self.shared_args,
                    verbose
                )
            
            if self.atmosphere == False:
                raise ValueError('lat/lon out of range')
            
        elif source == 'narr':
            pass
        
        else:
            raise ValueError('atmo_source is not one of (narr, merra)')
            
        
     # MODTRAN
    def run_modtran(self, output_directory, output_file, lat, lon, overpass_date, skin_temp):
        
        modtran_directory = '{0}/{1}'.format(output_directory, output_file)
        
        modtran_data = modtran.process(
                            self.atmosphere,
                            lat,
                            lon,
                            overpass_date,
                            modtran_directory,
                            skin_temp
                        )
    
        return modtran_data


    # LTOA calcs
    def run_ltoa(self, modtran_data, img_ltoa, mod_ltoa, skin_temp, lat, lon):
        
        mod_ltoa_spectral = radiance.calc_ltoa_spectral(
            None,                                                           # Do not supply emissivities, use the values in the water file
            modtran_data['wavelengths'],
            modtran_data['upwell_rad'],
            modtran_data['gnd_reflect'],
            modtran_data['transmission'],
            skin_temp
        )
        
        try:
            for b in self.BANDS:
                RSR_wavelengths, RSR = numpy.loadtxt(self.rsrs[b], unpack=True)
                img_ltoa[b] = sat.landsat.calc_ltoa(
                                        self.image_data['directory'],
                                        self.image_data['metadata'],
                                        lat,
                                        lon,
                                        b
                                    )
                mod_ltoa[b] = radiance.calc_ltoa(
                                        modtran_data['wavelengths'], 
                                        mod_ltoa_spectral, 
                                        RSR_wavelengths, RSR
                                    )
                
        except RuntimeError as e:            
            raise RuntimeError(str(e))
            
        return img_ltoa, mod_ltoa


    # Write the report headings to screen or frame
    def print_report_headings(self):
        
        report_headings = "Scene_ID, Date, Buoy_ID, Bulk_Temp, Skin_Temp, Buoy_Lat, Buoy_Lon, Modelled_B10, Modelled_B11, Image_B10, Image_B11, Error_B10, Error_B11, Status, Reason"
        
        self.log('output', report_headings)


    # Print the output to the scfeen and save it to file
    def print_and_save_output(self):
        
        error_message = None
                
        for key in self.data[self.args['scene_id']].keys():
            
            if(self.data[self.args['scene_id']][key][9] == "failed"):
                error_message = model.Model.get_error_message(self, self.data[self.args['scene_id']][key][10])
            else:
                error_message = None
            
            # Convert tuple to text and remove first and last parentheses
            log_text = str(self.args['scene_id']) + ', '                         # scene_id
            log_text += str(self.data[self.args['scene_id']][key][8].strftime('%Y/%m/%d')) + ', '     # date
            log_text += str(self.data[self.args['scene_id']][key][0]) + ', '     # buoy_id
            log_text += str(self.data[self.args['scene_id']][key][1]) + ', '     # bulk_temp
            log_text += str(self.data[self.args['scene_id']][key][2]) + ', '     # skin_temp
            log_text += str(self.data[self.args['scene_id']][key][3]) + ', '     # buoy_lat
            log_text += str(self.data[self.args['scene_id']][key][4]) + ', '     # buoy_lon
            log_text += str(self.data[self.args['scene_id']][key][5][10]) + ', ' # mod_ltoa band 10
            log_text += str(self.data[self.args['scene_id']][key][5][11]) + ', ' # mod_ltoa band 11
            log_text += str(self.data[self.args['scene_id']][key][7][10]) + ', ' # img_ltoa band 10
            log_text += str(self.data[self.args['scene_id']][key][7][11]) + ', ' # img_ltoa band 11
            log_text += str(self.data[self.args['scene_id']][key][6][10]) + ', ' # error band 10
            log_text += str(self.data[self.args['scene_id']][key][6][11]) + ', ' # error band 11
            log_text += str(self.data[self.args['scene_id']][key][9]) + ', '     # status
            log_text += str(error_message)                                       # reason
            
            self.log('output', log_text)
            self.save_output_to_file(log_text)


    # Save the output to a file
    def save_output_to_file(self, current_line):
        
        self.output_file_created = False
        
        if (self.args['process'] == 'partial_single') or (self.args['process'] == 'partial_batch'):
            
            # test_paths checks whether a file exists or not returning True if it exists and False if it does not exist
            if not (test_paths.main([self.args['savefile'], "-tfile"])):
                output_file = open(self.args['savefile'], 'w+')
                output_file.write('Scene_ID, Date, Skin_Temp, Lat, Lon, Modelled_B10, Modelled_B11, Image_B10, Image_B11, Emissivity_B10, Emissivity_B11, Status, Reason\n')
                output_file.write("%s\n" % current_line)
                output_file.close()
            else:
                output_file = open(self.args['savefile'], 'a+')
                output_file.write("%s\n" % current_line)
                output_file.close()
        
        else:
        
            # test_paths checks whether a file exists or not returning True if it exists and False if it does not exist
            if not (test_paths.main([self.args['savefile'], "-tfile"])):
                output_file = open(self.args['savefile'], 'w+')
                output_file.write('Scene_ID, Date, Buoy_ID, Bulk_Temp, Skin_Temp, Buoy_Lat, Buoy_Lon, Modelled_B10, Modelled_B11, Image_B10, Image_B11, Error_B10, Error_B11, Status, Reason\n')
                output_file.write("%s\n" % current_line)
                output_file.close()
            else:
                output_file = open(self.args['savefile'], 'a+')
                output_file.write("%s\n" % current_line)
                output_file.close()


    # Stop all the spinners and remove all the threads
    def finalize(self):
        
        if self.args['caller'] == 'menu':
            self.stop_spinners()

        self.clean_folders()
        
        for thread in self.args['threads']:            
            if thread.THREAD_NAME == 'image':                
                thread.display_image_thread.join()


    # Clean the process folders
    def clean_folders(self):
        
        # Erases all the downloaded data if configured
        if settings.CLEAN_FOLDER_ON_COMPLETION:
            if self.args['caller'] == 'tarca_gui':
                model.Model.clear_downloads(self, self.args['status_logger'])
            else:
                model.Model.clear_downloads(self)


    # Stop the spinners
    def stop_spinners(self):
        
        # Stop all spinners that could still be running
        if self.buoys != None:
            for buoy_id in self.buoys:
                if self.buoy_process_monitor[buoy_id] != False:
                    if self.buoy_process_monitor[buoy_id].active:
                        self.buoy_process_monitor[buoy_id].stop_spinner()


    # Destructor.  Usually not needed but in this case required to get rid of threads        
    def __del__(self):
            
        for thread in self.args['threads']:
            if thread.THREAD_NAME == 'spinner':
                if thread.spinner_thread.isAlive():
                    thread.spinner_thread.join()
                