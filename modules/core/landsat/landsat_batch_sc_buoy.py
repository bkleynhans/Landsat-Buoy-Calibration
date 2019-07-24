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
import os, sys, pdb
from modules.core.landsat.landsat_single_sc_buoy import Landsat_Single_Sc_Buoy
from modules.core import model


class Landsat_Batch_Sc_Buoy(Landsat_Single_Sc_Buoy):
    
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
        
        
#    def build_file_paths(self):
#        
#        # Build the output file path from the input file path
#        batchfile_name = self.args['batch_file_name'][(self.args['batch_file_name'].rfind('/') + 1):]        
#        self.args['savefile'] = self.args['savefile'][:self.args['savefile'].rfind('/') + 1] + batchfile_name[:batchfile_name.rfind('.')] + '.out'
#        
#        self.delete_file(self.args['savefile'])
        
        
    def process_scene(self):
        
        self.print_and_save_output()