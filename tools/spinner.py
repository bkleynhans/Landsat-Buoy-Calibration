#!/usr/bin/env python3
###
#
# Module for displaying images in seperate threads
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 25, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 25, 2019
# Filename            : spinner.py
#
###

# Imports
import sys, itertools
import threading
import time

class Spinner():
    
    SPINNER = itertools.cycle(['-','/','|','\\'])
    THREAD_NAME = 'spinner'
    
    def __init__(self):
        
        self.active = True
                
        self.spinner_thread = threading.Thread(target=self.make_spinner)
        
        
    # Start the spinner
    def make_spinner(self):
        
        while self.active:
            sys.stdout.write(next(self.SPINNER))
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(0.1)
            
    
    # Start the spinner
    def start_spinner(self):
        
        self.spinner_thread.start()


    # Stop the spinner
    def stop_spinner(self):
        
        self.active = False
        sys.stdout.write('\n\b >>>  done')
        sys.stdout.flush()
        