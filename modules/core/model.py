#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : This is the base entry class for all models
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 30, 2019
# Filename            : model.py
#
###

# Imports
import sys, os, pdb
import shutil, warnings
from datetime import datetime
from buoycalib import settings
from tools.process_logger import Process_Logger
from tools import test_paths
from modules.core.landsat.landsat_single_sc_buoy import Landsat_Single_Sc_Buoy
from modules.core.landsat.landsat_single_sc_toa import Landsat_Single_Sc_Toa
from modules.core.landsat.landsat_batch_sc_buoy import Landsat_Batch_Sc_Buoy
from modules.core.landsat.landsat_single_sw_lst import Landsat_Single_Sw_Lst

class Model:
    
    # Constructor
    def __init__(self, caller, qty, algorithm, process, source, atmo_source, display_image, project_root, verbose, partial_data=None, status_log=None, output_log=None):
        
        warnings.filterwarnings("ignore")
        
        # Build an arguments tree with all required data for processing
        self.args = {}
        
        self.args['caller'] = caller                # Is this being called from the GUI or the terminal
        self.args['process'] = process              # Is this a buoy, TOA or LST process
        self.args['qty'] = qty                      # Are we processing a single element or a batch
        
        if (qty == 'single'):                       # If we are processing a single element, the source is the Scene ID
            if (algorithm == 'sc') or (algorithm == 'sw'):
                self.args['scene_id'] = source
                
        elif (qty == 'batch'):                      # If we are processing a batch, the source is the batch file name
            self.args['input_file'] = source
            input_filename = source[source.rfind('/') + 1:]
            self.args['batch_file_name'] = input_filename[:input_filename.rfind('.')]
        
        self.args['algorithm'] = algorithm          # Only two algorithms have been implemented, (sc - single channel; sw - split window)
        self.args['atmo_source'] = atmo_source
        self.args['display_image'] = display_image
        self.args['project_root'] = project_root
        self.args['output_directory'] = os.path.join(project_root, 'output')
        self.args['verbose'] = verbose        
        self.args['partial_data'] = partial_data
        self.args['status_log'] = status_log
        self.args['output_log'] = output_log
        
        self.create_loggers()                       # Are used to log to the GUI status frame
        
        self.process_arguments()
        
        if self.args['caller'] == 'menu':            
            input("\n\n  Press Enter to continue...")


    # Create the data loggers for gui display
    def create_loggers(self):
        
        # Initialize the loggers for process feedback
        if self.args['status_log'] == None:
            self.status_logger = Process_Logger(settings.DEFAULT_STATUS_LOG)
        else:
            self.args['status_logger'] = Process_Logger(self.args['status_log'])
            
        if self.args['output_log'] == None:
            self.output_logger = Process_Logger(settings.DEFAULT_OUTPUT_LOG)
        else:
            self.args['output_logger'] = Process_Logger(self.args['output_log'])


    def process_arguments(self):
        
        self.args['savefile'] = settings.DEFAULT_OUTPUT_PATH
        
        self.build_file_paths()
        
        if self.args['qty'] == 'single':            
            if self.args['process'] == 'buoy':        
                if self.args['scene_id'][0:3] in ('LC8', 'LC0'):   # Landsat Scene
                        
                    self.results = Landsat_Single_Sc_Buoy(self.args)
            
                elif self.args['scene_id'][0:3] == 'MOD':  # Modis Scene
                    pass
                
            elif self.args['process'] == 'toa':                
                if self.args['scene_id'][0:3] in ('LC8', 'LC0'):   # Landsat Scene
                    
                    self.results = Landsat_Single_Sc_Toa(self.args)
            
                elif self.args['scene_id'][0:3] == 'MOD':  # Modis Scene
                    pass
                
            elif self.args['process'] == 'lst':
                
                self.results = Landsat_Single_Sw_Lst(self.args)
        
        elif self.args['qty'] == 'batch':
            
            self.analyze_batch()


    # Builds the paths to the output files and stores them in args['savefile'] index
    def build_file_paths(self):
        
        default_output_path = self.args['savefile'][:self.args['savefile'].rfind('/')]
        
        if self.args['qty'] == 'single':        
            self.args['savefile'] = os.path.join(
                    default_output_path,
                    self.args['qty'], 
                    self.args['algorithm'],
                    self.args['process'],
                    self.args['scene_id'] + '.out'
                )
            
        elif self.args['qty'] == 'batch':
            self.args['savefile'] = os.path.join(
                    default_output_path,
                    self.args['qty'],
                    'data',
                    self.args['algorithm'],
                    self.args['process'],
                    self.args['batch_file_name'] + '.out'
                )
        
        
        self.delete_file(self.args['savefile'])


    # Analyzes the batch file and breaks it into landsat and modis lists.  Modis has not yet been 
    # implemented.  Processes the lists.
    def analyze_batch(self):
        
        self.args['landsat_scenes'] = []
        self.args['modis_scenes'] = []
        
        # Read the file getting rid of all leading and trailing whitespace including newline characters
        self.scenes = [line.strip() for line in open(self.args['input_file'])]
        
        for scene in self.scenes:
            if scene[0:3] in ('LC8', 'LC0'):   # Landsat Scene
    
                self.args['landsat_scenes'].append(scene)
                
            elif scene[0:3] == 'MOD':
            
                self.args['modis_scenes'].append(scene)
        
        
        if (len(self.args['landsat_scenes']) > 0):
            self.results = Landsat_Batch_Sc_Buoy(self.args)
            
        if (len(self.args['modis_scenes']) > 0):
            pass


    # Erases all data from the downloads directory to ensure we don't consume all the disk space
    # This option can be enabled and disabled in the buoycalib/settings.py file
    def clear_downloads(self, status_logger=None):
    
        log_text = ("\n\n  Cleaning up the downloaded items folder...")
        
        if (self.args['caller'] != 'tarca_gui'):
            sys.stdout.write("\r" + log_text + "\n\n")
        else:
            status_logger.write(log_text)
        
        directory = settings.DATA_BASE
        
        for file_or_folder in os.listdir(directory):
            file_path = os.path.join(directory, file_or_folder)
            
            log_text = ("   Deleting %s data..." % (file_or_folder))
            
            try:
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

            except Exception as e:
                # [Errno 39] Directory not empty is a known error associated with shutil.rmtree
                # there is currently no solution (other than a workaround)
#                print(e)
                pass
        
        log_text = "  Cleanup completed!!!            "
        
        if (self.args['caller'] != 'tarca_gui'):
            sys.stdout.write("\r" + log_text + "\n\n")
        else:
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


    # Delete file either by relative or absolute path    
    def delete_file(self, filename):
        
        if os.path.isfile(filename):
            # unlink is ux version of delete for files
            os.unlink(filename)