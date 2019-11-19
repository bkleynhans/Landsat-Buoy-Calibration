 #!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Single Channel Single Scene process for landsat module
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 25, 2019
# Filename            : landsat_single_sc_buoy.py
#
###

# Imports
import sys, pdb
from buoycalib import (sat, buoy, settings)
from modules.core.landsat.landsat_base import Landsat_Base
from modules.core import model
import datetime

class Landsat_Single_Sc_Buoy(Landsat_Base):
    
    # Constructor
    def __init__(self, args):
        
        super(Landsat_Single_Sc_Buoy, self).__init__(args)
        
        self.args = args
        self.download_image(self.args['scene_id'])
        
        self.analyze_image()
        
        sys.stdout.write('\n')
        self.print_report_headings()
        sys.stdout.write('\n')
        sys.stdout.flush()
        
        self.process_scene()
        
        self.finalize()
        
    
    # Analyze the individual image
    def analyze_image(self):
        
        if self.image_data['file_downloaded']:
            
            self.rsrs = {b:settings.RSR_L8[b] for b in self.BANDS}
            self.corners = sat.landsat.corners(self.image_data['metadata'])
            self.buoys = buoy.datasets_in_corners(self.corners)
            
            if not self.buoys:
                self.image_data['overpass_date'] = datetime.datetime(1, 1, 1, 0, 0)
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
                    'No Buoys in Scene'
                )
#                raise buoy.BuoyDataException('no buoys in scene')
                
            self.process_buoys()
            
        else:
            self.image_data['overpass_date'] = datetime.datetime(1, 1, 1, 0, 0)
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
        
        self.print_and_save_output()