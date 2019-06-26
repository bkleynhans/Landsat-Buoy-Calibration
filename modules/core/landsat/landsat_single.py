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
# Filename            : landsat_single.py
#
###

# Imports
import sys, pdb
from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)
from modules.core.landsat.landsat_base import Landsat_Base
from modules.core import model
import datetime

class Landsat_Single(Landsat_Base):
    
    def __init__(self, args):
        
        super(Landsat_Single, self).__init__(args)
        
        self.download_image(self.args['scene_id'])
        
        self.analyze_image()
        
        self.process_scene()
        
        self.finalize()
        
        
    def analyze_image(self):
        
        if self.image_data['file_downloaded']:
            
            self.rsrs = {b:settings.RSR_L8[b] for b in self.BANDS}
            self.corners = sat.landsat.corners(self.image_data['metadata'])
            self.buoys = buoy.datasets_in_corners(self.corners)
            
            if not self.buoys:
                raise buoy.BuoyDataException('no buoys in scene')
                
            self.process_buoys()
            
        else:
            self.image_data['overpass_date']= datetime(1, 1, 1, 0, 0)
            self.data[self.args['scene_id']][0] = (
                    0,
                    0,
                    0,
                    0,
                    0,
                    {10:0,11:0},
                    {10:0,11:0},
                    {10:0,11:0},
                    self.image_data['overpass_date'],
                    'failed',
                    'No Landsat image available'
                )
    
    
    def process_scene(self):
        
        self.args['savefile'] = self.args['savefile'][:self.args['savefile'].rfind('/') + 1] + self.args['scene_id'] + '.txt'
        report_headings = "Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason"

        self.log(report_headings)
        
        self.print_output_to_screen()