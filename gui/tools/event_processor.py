###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 7, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 7, 2019
# Filename            : event_processor.py
#
###

### This module created with help from the article by Md. Sabuj Sarker(http://sabuj.me/)
##  https://www.linode.com/docs/development/monitor-filesystem-events-with-pyinotify/

# Imports
import pyinotify


class Event_Processor(pyinotify.ProcessEvent):
    
    _methods = ["IN_CREATE",
                "IN_OPEN",
                "IN_ACCESS",
                "IN_ATTRIB",
                "IN_CLOSE_NOWRITE",
                "IN_CLOSE_WRITE",
                "IN_DELETE",
                "IN_DELETE_SELF",
                "IN_IGNORED",
                "IN_MODIFY",
                "IN_MOVE_SELF",
                "IN_MOVED_FROM",
                "IN_MOVED_TO",
                "IN_Q_OVERFLOW",
                "IN_UNMOUNT",
                "default"]
    
    # Event Processor constructor
    def __init__(self):
        
        pass