#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Single Channel Top of Atmosphere Radiance process for landsat module with user supplied data
# Created By          : Benjamin Kleynhans
# Creation Date       : June 26, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 8, 2019
# Filename            : landsat_single_sc_toa.py
#
###

# Imports
import sys, pdb
from modules.core import model
from modules.core.landsat.landsat_base import Landsat_Base
from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)
import numpy

class Landsat_Single_Sc_Toa(Landsat_Base):
    
    # Constructor
    def __init__(self, args):
        
        super(Landsat_Single_Sc_Toa, self).__init__(args)
        
        self.download_image(self.args['scene_id'])
        
        self.get_atmosphere()
        
        if hasattr(self, 'error_message'):
            self.get_modtran()
            self.get_ltoa()
        else:
            self.populate_defaults()
        
        sys.stdout.write('\n')
        self.print_report_headings()
        sys.stdout.write('\n')
        sys.stdout.flush()
        
        self.print_and_save_output()
        
        self.finalize()
        

    # Calculate atmosphere data
    def get_atmosphere(self):
        
        self.calculate_atmosphere(
                self.args['atmo_source'],
                self.image_data['overpass_date'],
                self.args['partial_data']['lat'],
                self.args['partial_data']['lon']
            )


    # Calculate MODTRAN data
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


    # Calculate Top of Atmosphere Radiance data
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


    # LTOA calcs
    def run_ltoa(self, modtran_data, img_ltoa, mod_ltoa, skin_temp, lat, lon):
        
        spec_ref = {
            10: self.args['partial_data']['emis_b10'],
            11: self.args['partial_data']['emis_b11']
        }
        
        try:
            for b in self.BANDS:
                
                mod_ltoa_spectral = radiance.calc_ltoa_spectral(
                                        spec_ref[b],
                                        modtran_data['wavelengths'],
                                        modtran_data['upwell_rad'],
                                        modtran_data['gnd_reflect'],
                                        modtran_data['transmission'],
                                        skin_temp
                                    )
                
                RSR_wavelengths, RSR = numpy.loadtxt(self.rsrs[b], unpack=True)
                img_ltoa[b] = sat.landsat.calc_ltoa(
                                    self.image_data['directory'],
                                    self.image_data['metadata'],
                                    lat,
                                    lon,
                                    b
                                )
                
                mod_ltoa[b] = radiance.calc_ltoa(modtran_data['wavelengths'], mod_ltoa_spectral, RSR_wavelengths, RSR)
                
        except RuntimeError:# as e:
#                warnings.warn(str(e), RuntimeWarning)
#                
#                return
            pass
            
        return img_ltoa, mod_ltoa
    
    # Populate default values if there was an error with the supplied lat/lon coordinates
    def populate_defaults(self):
        
        self.img_ltoa = {}
        self.mod_ltoa = {}
        
        self.mod_ltoa[10] = 0
        self.mod_ltoa[11] = 0
        self.img_ltoa[10] = 0
        self.img_ltoa[11] = 0


    # Display the report headings
    def print_report_headings(self):
        
        # img1 / img2 - radiance from satellite image
        # mod1 / mod2 - modeled / calculated radiance
        # emis_10 / emis_11     - emissivity entered at launch defaults are b10: 0.988 b11: 0.98644
        
        report_headings = "Scene_ID, Date, Skin_Temp, Lat, Lon, Modelled_B10, Modelled_B11, Image_B10, Image_B11, Emissivity_B10, Emissivity_B11, Status, Reason"
        
        self.log('output', report_headings)

    # Display the output on screen and write it to file
    def print_and_save_output(self):
        
        error_message = None
        
        if self.image_data['file_downloaded']:
            if hasattr(self, 'error_message'):
                error_message = self.error_message
            else:
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
        log_text += str(error_message)                                                      # reason
        
        self.log('output', log_text)
        self.save_output_to_file(log_text)