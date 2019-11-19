#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : July 16, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 25, 2019
# Filename            : landsat_single_sw_lst.py
#
###

# Imports
import sys, pdb
from modules.core import model
from modules.core.landsat.landsat_base import Landsat_Base
from modules.stp.sw.split_window import Split_Window
from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)
import numpy

class Landsat_Single_Sw_Lst(Landsat_Base):
    
    # Constructor
    def __init__(self, args):
        
        super(Landsat_Single_Sw_Lst, self).__init__(args)
        
        self.download_image(self.args['scene_id'])
        
        self.get_image_ltoa()
        
        self.add_gain_bias()
        
        self.calculate_split_window(
                self.adjusted_ltoa[10],
                self.adjusted_ltoa[11],
                self.args['partial_data']['emis_b10'],
                self.args['partial_data']['emis_b11']
            )
        
        sys.stdout.write('\n')
        self.print_report_headings()
        sys.stdout.write('\n')
        sys.stdout.flush()
        
        self.print_and_save_output()
        
        self.finalize()

    # Calculate Top of Atmosphere Radiance
    def get_image_ltoa(self):
        
        self.img_ltoa = {}
        
        self.rsrs = {b:settings.RSR_L8[b] for b in self.BANDS}
        
        # Pass in paramteres directly because run_ltao receives requests from other sources also
        self.img_ltoa = self.run_image_ltoa(
                self.img_ltoa,
                self.args['partial_data']['lat'],
                self.args['partial_data']['lon']
            )
    
    
    # LTOA calcs
    def run_image_ltoa(self, img_ltoa, lat, lon):
                
        try:
            for b in self.BANDS:
                
                img_ltoa[b] = sat.landsat.calc_ltoa(
                        self.image_data['directory'],
                        self.image_data['metadata'],
                        lat,
                        lon,
                        b
                    )
                
        except RuntimeError:# as e:
#                warnings.warn(str(e), RuntimeWarning)
#                
#                return
            pass
            
        return img_ltoa


    # Add gain and bias if required
    def add_gain_bias(self):
        
        self.adjusted_ltoa = {}
        
        if self.args['partial_data']['add_gain_bias']:     
            self.adjusted_ltoa = {
                    10: ((self.img_ltoa[10] * self.args['partial_data']['gain_b10']) + self.args['partial_data']['bias_b10']),
                    11: ((self.img_ltoa[11] * self.args['partial_data']['gain_b11']) + self.args['partial_data']['bias_b11'])
                }
            
        else:
            self.adjusted_ltoa = {
                    10: self.img_ltoa[10],
                    11: self.img_ltoa[11]
                }
    
    
    # Calculate split window
    def calculate_split_window(self, img_ltoa10, img_ltoa11, emis_b10, emis_b11):
        
        self.data[self.args['scene_id']] = Split_Window(img_ltoa10, img_ltoa11, emis_b10, emis_b11).data
        
    
    # Print headings to scree and file
    def print_report_headings(self):
        
        report_headings = "Scene_ID, Date, Lat, Lon, Radiance_B10, Radiance_B11, Emissivity_B10, Emissivity_B11, LST_SW, Errors"
        
        self.log('output', report_headings)
        
    
    # Print output to screen and save in file
    def print_and_save_output(self):
        
        error_message = None
        
        if self.image_data['file_downloaded']:            
            error_message = None            
        else:            
            error_message = 'The source image could not be downloaded.'
            
        # Convert tuple to text and remove first and last parentheses
        log_text = str(self.args['scene_id']) + ', '                                        # scene_id
        log_text += str(self.image_data['overpass_date'].strftime('%Y/%m/%d')) + ', '       # date
        log_text += str(self.args['partial_data']['lat']) + ', '                            # lat
        log_text += str(self.args['partial_data']['lon']) + ', '                            # lon
        log_text += str(self.data[self.args['scene_id']]['radiance'][10]) + ', '            # img_ltoa band 10
        log_text += str(self.data[self.args['scene_id']]['radiance'][11]) + ', '            # img_ltoa band 11
        log_text += str(self.data[self.args['scene_id']]['emissivity'][10]) + ', '          # emissivity band 10
        log_text += str(self.data[self.args['scene_id']]['emissivity'][11]) + ', '          # emissivity band 11
        log_text += str(self.data[self.args['scene_id']]['LST_SW']) + ', '                  # Land Surface Temperature Split Window
        log_text += str(error_message)                                                      # reason
        
        self.log('output', log_text)
        self.save_output_to_file(log_text)