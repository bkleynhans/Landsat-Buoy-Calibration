#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 21, 2019
# Filename            : model.py
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
    
    def __init__(self, args):

        self.data = {}
        self.args = args
    

    # Acquire, save and display image if requested
    def download_image(self, scene_id):
        
        self.args['scene_id'] = scene_id        
        self.data[self.args['scene_id']] = {}
        self.image_data = display.landsat_preview(scene_id ,'')
        
        if self.args['display_image']:
            image_data = {
                    'title': self.args['scene_id'],
                    'image': self.image_data['image']
                }
            
            Display_Image(image_data)
        
        image_file = '{0}.tif'.format(self.args['scene_id'])
        image_directory = os.path.join(self.args['output_directory'], 'processed_images')
        absolute_image_directory = os.path.join(self.args['project_root'], image_directory)
        absolute_image_path = os.path.join(absolute_image_directory, image_file)
        cv2.imwrite(absolute_image_path, self.image_data['image'])
        

    def process_buoys(self):
        
        self.buoy_process_monitor = dict.fromkeys(self.buoys, False)
        
        # Process one buoy at a time
        for buoy_id in self.buoys:
            self.buoy_process_monitor[buoy_id] = Spinner()
            self.buoy_processor(buoy_id)
        
#        # Process all buoys using threads
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
    
    
    def log(self, log_text):
        
        sys.stdout.write('\n')
        
        if (self.args['caller'] == 'menu'):
            
            sys.stdout.write("\r" + log_text)
        
        elif (self.args['caller'] == 'tarca_gui'):
        
            self.args['status_logger'].write(log_text)
                    
        sys.stdout.flush
        
    def buoy_processor(self, buoy_id):
                    
        self.log("    Processing buoy %s  " % (buoy_id))
        self.buoy_process_monitor[buoy_id].start_spinner()
        
        try :
            self.buoy_file = buoy.download(buoy_id, self.image_data['overpass_date'])
            
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
             
            self.buoy_process_monitor[buoy_id].stop_spinner()
            
            return
         
        self.calculate_atmosphere()
                    
        modtran_data = self.run_modtran(buoy_id)
        
        img_ltoa = {}
        mod_ltoa = {}
        
        img_ltoa, mod_ltoa = self.run_ltoa(modtran_data, img_ltoa, mod_ltoa)
        
        error = error_bar.error_bar(
                        self.args['scene_id'], 
                        buoy_id,
                        self.buoy_data['skin_temp'],
                        0.305,
                        self.image_data['overpass_date'],
                        self.buoy_data['buoy_lat'],
                        self.buoy_data['buoy_lon'],
                        self.rsrs,
                        self.BANDS
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
        
        self.buoy_process_monitor[buoy_id].stop_spinner()
        
        
    def calculate_atmosphere(self):
        
        # Atmosphere
        if self.args['atmo_source'] == 'merra':             
            self.atmosphere = atmo.merra.process(
                    self.image_data['overpass_date'],
                    self.buoy_data['buoy_lat'],
                    self.buoy_data['buoy_lon'],
                    self.args['verbose']
                )         
        elif self.args['atmo_source'] == 'narr':
                    self.atmosphere = atmo.narr.process(
                    self.image_data['overpass_date'],
                    self.buoy_data['buoy_lat'],
                    self.buoy_data['buoy_lon'],
                    self.args['verbose']
                 )
        else:
            raise ValueError('atmo_source is not one of (narr, merra)')
            
        
     # MODTRAN
    def run_modtran(self, buoy_id):
        
        modtran_directory = '{0}/{1}_{2}'.format(settings.MODTRAN_BASH_DIR, self.args['scene_id'], buoy_id)
        
        modtran_data = modtran.process(
                            self.atmosphere,
                            self.buoy_data['buoy_lat'],
                            self.buoy_data['buoy_lon'],
                            self.image_data['overpass_date'],
                            modtran_directory,
                            self.buoy_data['skin_temp']
                        )
    
        return modtran_data
    
    # LTOA calcs
    def run_ltoa(self, modtran_data, img_ltoa, mod_ltoa):
        
        mod_ltoa_spectral = radiance.calc_ltoa_spectral(
                                        modtran_data['wavelengths'],
                                        modtran_data['upwell_rad'],
                                        modtran_data['gnd_reflect'],
                                        modtran_data['transmission'],
                                        self.buoy_data['skin_temp'])
        
        try:
            for b in self.BANDS:
                RSR_wavelengths, RSR = numpy.loadtxt(self.rsrs[b], unpack=True)
                img_ltoa[b] = sat.landsat.calc_ltoa(
                                        self.image_data['directory'],
                                        self.image_data['metadata'],
                                        self.buoy_data['buoy_lat'],
                                        self.buoy_data['buoy_lon'],
                                        b
                                    )
                mod_ltoa[b] = radiance.calc_ltoa(modtran_data['wavelengths'], mod_ltoa_spectral, RSR_wavelengths, RSR)
                
        except RuntimeError:# as e:
#                warnings.warn(str(e), RuntimeWarning)
#                
#                return
            pass
            
        return img_ltoa, mod_ltoa
    
    def print_output_to_screen(self):
        
        error_message = None
                
        for key in self.data[self.args['scene_id']].keys():
            if(self.data[self.args['scene_id']][key][9] == "failed"):
                error_message = model.Model.get_error_message(self, self.data[self.args['scene_id']][key][10])
            else:
                error_message = None
                buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason = self.data[self.args['scene_id']][key]
            
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
            
            self.log(log_text)
            self.save_output_to_file(log_text)
            
    
    def save_output_to_file(self, current_line):
        
        self.output_file_created = False
        
        # test_paths checks whether a file exists or not returning True if it exists and False if it does not exist
        if not (test_paths.main([self.args['savefile'], "-tfile"])):
            output_file = open(self.args['savefile'], 'w+')
            output_file.write('#Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason\n')
            output_file.write("%s\n" % current_line)
            output_file.close()
        else:
            output_file = open(self.args['savefile'], 'a+')
            output_file.write("%s\n" % current_line)
            output_file.close()
            
            
    def finalize(self):
        
        self.stop_spinners()            
        self.clean_folders()
    
    def clean_folders(self):
        
        # Erases all the downloaded data if configured
        if settings.CLEAN_FOLDER_ON_COMPLETION:
                self.clear_downloads(self.args['status_logger'])
                
    def stop_spinners(self):
        
        # Stop all spinners that could still be running
        for buoy_id in self.buoys:
            if self.buoy_process_monitor[buoy_id].active:
                self.buoy_process_monitor[buoy_id].stop_spinner()