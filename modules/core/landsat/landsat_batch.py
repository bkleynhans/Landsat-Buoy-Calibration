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
# Filename            : landsat_batch.py
#
###

# Imports
import sys, pdb
from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)
from modules.core.landsat.landsat_single import Landsat_Single
from modules.core import model
#from tools import test_paths
import datetime


class Landsat_Batch(Landsat_Single):
    
    def __init__(self, args):
        
        super(Landsat_Single, self).__init__(args)
        
        for scene in self.args['landsat_scenes']:
            sys.stdout.write('\n')
            self.log("  Starting analysis of scene {}".format(scene))
            sys.stdout.write('\n')
            
            self.download_image(scene)
            self.analyze_image()
            
            sys.stdout.write('\n')
            self.log("  Analysis completed for scene {}".format(scene))
            sys.stdout.write('\n')
            sys.stdout.flush()
            
            self.process_scene()
            self.finalize()
        
        
    def process_scene(self):
        
        # Build the output file path from the input file path
        batchfile_name = self.args['batch_file_name'][(self.args['batch_file_name'].rfind('/') + 1):]        
        self.args['savefile'] = self.args['savefile'][:self.args['savefile'].rfind('/') + 1] + batchfile_name[:batchfile_name.rfind('.')] + '.out'
        
        report_headings = "Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason"
        
        self.log(report_headings)
        
        self.print_output_to_screen()