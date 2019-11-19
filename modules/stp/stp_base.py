###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Split window claculation
# Created By          : Benjamin Kleynhans
# Creation Date       : June 18, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : November 18, 2019
# Filename            : stp_base.py
#
###

# Imports
import inspect, sys, os
from os.path import join, abspath

class STP_Base():
    
    def __init__(self):
        
        self.set_path_variables()
        
    
    # Calculate fully qualified path to location of program execution
    def get_module_path(self):
        
        filename = inspect.getfile(inspect.currentframe())
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    
        return path, filename
    
    
    # Set environment variables to locate current execution path
    def set_path_variables(self):
        
        path, filename = self.get_module_path()
    
        sys.path.append(path)
        sys.path.append(path + "/buoycalib")
        sys.path.append(path + "/downloaded_data")
        sys.path.append(path + "/tools")
        sys.path.append(path + "/output")
        sys.path.append(path + "/processed_images")
        sys.path.append(path + "/modules")