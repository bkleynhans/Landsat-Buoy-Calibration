###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Menu program for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 11, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : July 3, 2018
# Filename            : menu.py
#
###

import itertools
import threading
import time
import sys

class Animation:
    
    # Class attributes
    status = None
    animation_thread = None
    
    
    # Initializer / Instance Attributes
    def __init__(self):
        self.status = "stopped"
    
    # here is the animation
    def animate(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.status == "stopped":
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDone!   ')
    
    def start_animation(self):
        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.daemon = True
        
        self.status = "running"
        
        self.animate()
        
    def stop_animation(self):
        self.status= "stopped"
