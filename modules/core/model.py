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
import shutil, warnings
from buoycalib import settings
from tools.process_logger import Process_Logger
from modules.core.landsat.landsat_single import Landsat_Single
from modules.core.landsat.landsat_batch import Landsat_Batch

class Model:
    
#    def __init__(self, caller, args):
    def __init__(self, caller, process, source, atmo_source, display_image, project_root, verbose):
        
        warnings.filterwarnings("ignore")
        
        self.args = {}
        
        self.args['caller'] = caller
        self.args['process'] = process
        
        if process == 'single':
            self.args['scene_id'] = source
        elif process == 'batch':
            self.args['batch_file_name'] = source
        
        self.args['atmo_source'] = atmo_source
        self.args['display_image'] = display_image
        self.args['project_root'] = project_root
        self.args['output_directory'] = os.path.join(project_root, 'output')
        self.args['verbose'] = verbose
        
        # Create an instance copy of arguments
#        self.args = args
        
#        self.args['output_directory'] = os.path.join(project_root, 'output')
        
        self.create_loggers()
        
        self.process_arguments()
    
    
    # Create the data loggers for gui display
    def create_loggers(self):
        
        # Initialize the loggers for process feedback        
        self.status_logger = Process_Logger(settings.DEFAULT_STATUS_LOG)
        self.output_logger = Process_Logger(settings.DEFAULT_OUTPUT_LOG)
    
    
    def process_arguments(self):
        
        if self.args['process'] == 'single':
            
            self.args['savefile'] = settings.DEFAULT_SINGLE_SAVE_FILE
        
            if self.args['scene_id'][0:3] in ('LC8', 'LC0'):   # Landsat Scene
                    
                self.results = Landsat_Single(self.args)
        
            elif self.args['scene_id'][0:3] == 'MOD':  # Modis Scene
                pass        
        
        elif self.args['process'] == 'batch':
            
            self.args['savefile'] = settings.DEFAULT_BATCH_SAVE_PATH
            
            self.analyze_batch()
            
                    
    def analyze_batch(self):
        
        self.args['landsat_scenes'] = []
        self.args['modis_scenes'] = []
        
        # Read the file getting rid of all leading and trailing whitespace including newline characters
        self.scenes = [line.strip() for line in open(self.args['batch_file_name'])]
        
        for scene in self.scenes:
            if scene[0:3] in ('LC8', 'LC0'):   # Landsat Scene
    
                self.args['landsat_scenes'].append(scene)
                
            elif scene[0:3] == 'MOD':
            
                self.args['modis_scenes'].append(scene)
        
        
        if (len(self.args['landsat_scenes']) > 0):
            self.results = Landsat_Batch(self.args)
            
        if (len(self.args['modis_scenes']) > 0):
            pass
            
    
    def clear_downloads(self, status_logger):
    
        print("\n\n  Cleaning up the downloaded items folder...")
        
        directory = settings.DATA_BASE
        
        for file_or_folder in os.listdir(directory):
            file_path = os.path.join(directory, file_or_folder)
            
            log_text = (" Deleting %s..." % (file_or_folder))
            
            try:
                if self.get_size(file_path) > settings.FOLDER_SIZE_FOR_REPORTING:
                    if os.path.isfile(file_path):                    
                        if (self.args['caller'] != 'tarca_gui'):
                            sys.stdout.write("\r" + log_text)
                        else:
                            status_logger.write(log_text)
                        
                        
                        os.unlink(file_path)
                        
                    elif os.path.isdir(file_path):                    
                        if (self.args['caller'] != 'tarca_gui'):
                            sys.stdout.write("\r" + log_text)
                        else:
                            status_logger.write(log_text)
                        
                        
                        shutil.rmtree(file_path)
                else:
                    if os.path.isfile(file_path):
                        # unlink is ux version of delete for files
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
        log_text = "Cleanup completed!!!"
        
        if (self.args['caller'] != 'tarca_gui'):
            sys.stdout.write("\r" + log_text + "\n\n")
    
        status_logger.write(log_text)
    
    
    # Convert error codes to error messages for user feedback    
    def get_error_message(self, key):
        
        error_message = None
        
        if (key == "buoy"):
            error_message = "No buoys in the scene"
        elif (key == "data"):
            error_message = "No data in data file for this buoy on this date"
        elif (key == "file"):
            error_message = "No data file to download for this buoy for this period"
        elif (key== "image"):
            error_message = "No Landsat Image Available For Download"
        elif (key == "merra_layer1_temperature"):
            error_message = "Zero reading at Merra layer1 temperature for buoy"
        else:
            error_message = key
        
        return error_message
    
    
    # Get the size of a file
    def get_size(self, start_path):
        
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(start_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                total_size += os.path.getsize(file_path)
        
        # Divide by 1 000 000 to get a MegaByte size equivalent 
        total_size = total_size / 1000000
        
        return total_size
    
    
## Process initialization arguments
#def parseArgs(args):
#
#    import argparse
#
#    parser = argparse.ArgumentParser(description='Compute and compare the radiance values of \
#     a landsat image to the propogated radiance of a NOAA buoy, using atmospheric data and MODTRAN. ')
#
##    parser.add_argument('scene_id', help='LANDSAT or MODIS scene ID. Examples: LC08_L1TP_017030_20170703_20170715_01_T1, MOD021KM.A2011154.1650.006.2014224075807.hdf')
##    parser.add_argument('-a', '--atmo_source', default = 'merra', choices=['merra', 'narr'], help='Source of atmospheric data')
##    parser.add_argument('-v', '--verbose', default=False, action='store_true')
##    parser.add_argument('-s', '--savefile', default='output/single/results.txt')
##    parser.add_argument('-d', '--project_root', help='Working directory of the program')
##    parser.add_argument('-p', '--process', default = 'single', choices=['single', 'batch'])
##    parser.add_argument('-w', '--warnings', default=False, action='store_true')
##    parser.add_argument('-o', '--output_directory', default = '', help = 'Output directory for results')
## Allow ability to disable image display
##    parser.add_argument('-n', '--display_image', default='true')
## Add caller information
##    parser.add_argument('-c', '--caller', help='The name or reference of the file calling this function')
## Add log file locations
##    parser.add_argument('-t', '--statuslog', default = 'logs/status/default.status', help='Status file directory')
##    parser.add_argument('-u', '--outputlog', default = 'logs/output/default.output', help='Output file directory')
#
#    return parser.parse_args(args)
#
#
## Program entry from different source
#def main(args):
#
#    Model(parseArgs(args))
#
#
## Command line program entry
#if __name__ == '__main__':
#
#    args = main(sys.argv[1:])