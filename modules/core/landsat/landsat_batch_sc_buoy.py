#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Single Channel Batch process for landsat module
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 5, 2019
# Filename            : landsat_batch_sc_buoy.py
#
###

# Imports
import os, sys, pdb
from modules.core.landsat.landsat_single_sc_buoy import Landsat_Single_Sc_Buoy
from modules.core import model


class Landsat_Batch_Sc_Buoy(Landsat_Single_Sc_Buoy):
    
    # Constructor
    def __init__(self, args):
        
        super(Landsat_Single_Sc_Buoy, self).__init__(args)
        
        heading_counter = 0
        
        for scene in self.args['landsat_scenes']:
            sys.stdout.write('\n')
            self.log('status', " Starting analysis of scene {}".format(scene))
            sys.stdout.write('\n')
            
            self.download_image(scene)
            self.analyze_image()
            
            sys.stdout.write('\n')
            self.log('status', " Analysis completed for scene {}".format(scene))
            sys.stdout.write('\n')
            sys.stdout.flush()
            
            if self.args['caller'] == 'tarca_gui':
                if heading_counter == 0:
                    heading_counter += 1
                    self.print_report_headings()
            else:
                self.print_report_headings()
            
            self.process_scene()
            self.finalize()

        
    def process_scene(self):
        
        self.print_and_save_output()