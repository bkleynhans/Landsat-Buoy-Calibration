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
# Filename            : file_watcher.py
#
###

### This module created with help from the article by Md. Sabuj Sarker(http://sabuj.me/)
##  https://www.linode.com/docs/development/monitor-filesystem-events-with-pyinotify/

# Imports
import os
import pyinotify
from event_processor import Event_Processor


class File_Watcher():
    
    # File Watcher constructor
    def __init__(self, path):
        
        self.event_processor = Event_Processor()
        
        for method in Event_Processor._methods:
            self.process_generator(Event_Processor, method)
        
        self.watch_manager = pyinotify.WatchManager()
        self.event_notifier = pyinotify.ThreadedNotifier(self.watch_manager, Event_Processor())
        
        self.watch_this = path
        self.watch_manager.add_watch(self.watch_this, pyinotify.IN_MODIFY)
        self.event_notifier.start()
        
    
    def process_generator(self, cls, method):
        def _method_name(self, event):
            print("Method name: process_{}()\n"
                   "Path name: {}\n"
                   "Event Name: {}\n".format(method, event.pathname, event.maskname))
            
            
        _method_name.__name__ = "process_{}".format(method)
        setattr(cls, _method_name.__name__, _method_name)