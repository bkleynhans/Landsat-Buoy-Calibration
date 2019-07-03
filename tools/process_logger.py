#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Logger module for program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 6, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 6, 2019
# Filename            : process_logger.py
#
###

# Imports
import os
from os.path import join, abspath
import test_paths

PACKAGE_BASE = abspath(join(__file__, '../..'))

class Process_Logger():
    
    # Main Gui Frame constructor
    def __init__(self, filename):
        
        self.filename = os.path.join(PACKAGE_BASE, filename)
        
        self.check_required_directories()
        
        
    # Create any folders that are required and not currently available
    def check_required_directories(self):
            
        self.required_directories = {
                'logs',
                'logs/status',
                'logs/status/single',
                'logs/status/partial_single',
                'logs/status/batch',
                'logs/status/partial_batch',
                'logs/output',
                'logs/output/single',
                'logs/output/partial_single',
                'logs/output/batch',
                'logs/output/partial_batch'
            }
        
        for directory in self.required_directories:
            if not test_paths.main([os.path.join(PACKAGE_BASE, directory), "-tdirectory"]):
                test_paths.createDirectory(os.path.join(PACKAGE_BASE,directory))
        
    
    # Create the log file
    def __create_file(self):
        
        file = open(self.filename, 'w+')
        file.close()
        
        
    # Remove the old log file
    def __delete_file(self):
        
        if os.path.isfile(self.filename):
            # unlink is ux version of delete for files
            os.unlink(self.filename)
    
    # Append to the log file
    def __append_to_log(self, input_text):
        
        file = open(self.filename, 'a')
        file.write(input_text)
        file.write('\n')
            
        file.close()
    
    
    # Replace the contets of the log file
    def __update_log(self, input_text):
        
        file = open(self.filename, 'w')
        file.write(input_text)
        
        file.close()
        
    
    # If the file exists, append to the file.  If it
    # does not exist, create it and then append to it
    def write(self, input_text, newline = True):
        
        if not os.path.exists(self.filename):
            self.__create_file()
            
        if newline:
            self.__append_to_log(input_text)
        else:
            self.__update_log(input_text)