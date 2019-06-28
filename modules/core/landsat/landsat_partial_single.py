#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 26, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 26, 2019
# Filename            : landsat_partial_single.py
#
###

# Imports
import sys, pdb
from modules.core.landsat.landsat_base import Landsat_Base
from modules.stp.sw.split_window import Split_Window
from buoycalib import settings

class Landsat_Partial_Single(Landsat_Base):
    
    def __init__(self, args):
        
        super(Landsat_Partial_Single, self).__init__(args)
        
        self.build_single_file_path()
        
        self.download_image(self.args['scene_id'])
        
        self.get_atmosphere()
        self.get_modtran()
        self.get_ltoa()
        self.calculate_split_window(
                self.img_ltoa[10],
                self.img_ltoa[11],
                self.args['partial_data']['emis_b10'],
                self.args['partial_data']['emis_b11']
            )
        
        sys.stdout.write('\n')
        self.print_report_headings()
        sys.stdout.write('\n')
        sys.stdout.flush()
        
        self.print_and_save_output()
        
        self.finalize()
        
    
    def get_atmosphere(self):
        
        self.calculate_atmosphere(
                self.args['atmo_source'],
                self.image_data['overpass_date'],
                self.args['partial_data']['lat'],
                self.args['partial_data']['lon']
            )
        
        
    def get_modtran(self):
        modtran_output_file = '{0}'.format(self.args['scene_id'])
        
        self.modtran_data = self.run_modtran(
                settings.MODTRAN_BASH_DIR,
                modtran_output_file,
                self.args['partial_data']['lat'],
                self.args['partial_data']['lon'],
                self.image_data['overpass_date'],
                self.args['partial_data']['skin_temp']
            )
        
        
    def get_ltoa(self):
        
        self.img_ltoa = {}
        self.mod_ltoa = {}
        
        self.rsrs = {b:settings.RSR_L8[b] for b in self.BANDS}
        
        # Pass in paramteres directly because run_ltao receives requests from other sources also
        self.img_ltoa, self.mod_ltoa = self.run_ltoa(
                self.modtran_data,
                self.img_ltoa,
                self.mod_ltoa,
                self.args['partial_data']['skin_temp'],
                self.args['partial_data']['lat'],
                self.args['partial_data']['lon']
            )
    
    
    def calculate_split_window(self, img_ltoa10, img_ltoa11, emis_b10, emis_b11):
        
        self.data[self.args['scene_id']] = Split_Window(img_ltoa10, img_ltoa11, emis_b10, emis_b11).data
        
        
    def print_report_headings(self):
        
        # img1 / img2 - radiance from satellite image
        # mod1 / mod2 - modeled / calculated radiance
        # emis_10 / emis_11     - emissivity entered at launch defaults are b10: 0.988 b11: 0.98644
        
        report_headings = "Scene_ID, Date, skin_temp, lat, lon, mod1, mod2, img1, img2, emis_10, emis_11, LST_SW, status, reason"
        
        self.log('output', report_headings)
        
    
    def print_and_save_output(self):
        
        error_message = None
        
        if self.image_data['file_downloaded']:
            
            error_message = None
            
        else:
            
            error_message = 'The source image could not be downloaded.'
            
        # Convert tuple to text and remove first and last parentheses
        log_text = str(self.args['scene_id']) + ', '                                        # scene_id
        log_text += str(self.image_data['overpass_date'].strftime('%Y/%m/%d')) + ', '       # date
        log_text += str(self.args['partial_data']['skin_temp']) + ', '                      # skin_temp
        log_text += str(self.args['partial_data']['lat']) + ', '                            # lat
        log_text += str(self.args['partial_data']['lon']) + ', '                            # lon
        log_text += str(self.mod_ltoa[10]) + ', '                                           # mod_ltoa band 10
        log_text += str(self.mod_ltoa[11]) + ', '                                           # mod_ltoa band 11
        log_text += str(self.img_ltoa[10]) + ', '                                           # img_ltoa band 10
        log_text += str(self.img_ltoa[11]) + ', '                                           # img_ltoa band 11
        log_text += str(self.args['partial_data']['emis_b10']) + ', '                       # emissivity band 10
        log_text += str(self.args['partial_data']['emis_b11']) + ', '                       # emissivity band 11
        log_text += str(self.data[self.args['scene_id']]['LST_SW']) + ', '                  # Land Surface Temperature Split Window
        log_text += str(error_message)                                                      # reason
        
        self.log('output', log_text)
        self.save_output_to_file(log_text)