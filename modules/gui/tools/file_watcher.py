###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Part of the event_processor.py module.  This module does the actual watching
#                       of the output files and generates the events which are handles by the event_processor
# Created By          : Benjamin Kleynhans
# Creation Date       : June 7, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 10, 2019
# Filename            : file_watcher.py
#
###

### This module created with help from the article by Md. Sabuj Sarker(http://sabuj.me/)
##  https://www.linode.com/docs/development/monitor-filesystem-events-with-pyinotify/

# Imports
import os
import pyinotify
import pdb


class File_Watcher():
    
    # File Watcher constructor
    def __init__(self, master, path):
        
        from gui.tools.event_processor import Event_Processor
        self.event_processor = Event_Processor(master)
        
        # For each event generated, run the processor.  Also pass the master
        # which contains the parent object which contains all required methods
        # and accessors
        for method in Event_Processor._methods:
            self.event_processor.process_generator(Event_Processor, method)
        
        self.watch_manager = pyinotify.WatchManager()
        self.event_notifier = pyinotify.ThreadedNotifier(self.watch_manager, Event_Processor(master))
        
        self.watch_this = path
        self.watch_manager.add_watch(self.watch_this, pyinotify.IN_MODIFY)
        
        # After creating an instance of the watcher, you have to start and top it
        # my_watcher = File_Watcher("path_to_file") !!! NOTE THIS IS THE DIRECTORY OF THE FILE, DO NOT INCLUDE FILE NAME
        # my_watcher.event_notifier.start()
        # --> run processes <--
        # my_watcher.event_notifier.stop()
        #
        # !!->> Define the actions for each event in the event_processor