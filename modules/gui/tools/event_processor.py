###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : This module monitors the output and status files for changes, and displays
#                       the changes to the user as they happen
# Created By          : Benjamin Kleynhans
# Creation Date       : June 7, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 7, 2019
# Filename            : event_processor.py
#
###

### This module created with help from the article by Md. Sabuj Sarker(http://sabuj.me/)
##  https://www.linode.com/docs/development/monitor-filesystem-events-with-pyinotify/

# Imports
from tkinter import *
import pyinotify
import pdb


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

    master = None
    
    # Event Processor constructor
    def __init__(self, master):
        
        self.master = master
    
    
    # Processes events that are generated
    def process_generator(self, cls, method):
        # Insert the line into the gui
        def write_new_line_to_gui(self, frame_name, widget_name, text):
            
            if (frame_name == 'status_frame'):
                self.master.frames[frame_name].widgets[widget_name].insert('end', text)
                self.master.frames[frame_name].widgets[widget_name].see('end')
            elif (frame_name == 'output_frame'):
                self.master.frames[frame_name].widgets[widget_name].insert('end', text)
        
        
        # Open and read the output file
        def read_updated_file(filename):
            
            line_list = None
            
            for line in open(filename, 'r'):
                line_list = line
                
            
            return line_list
            
        
        # Handles the actual event.  Receives the method, path and event name
        def _method_name(self, event):
            
            new_line = read_updated_file(event.pathname)
                        
            if (event.pathname[event.pathname.rfind('status'):] == 'status'):
                write_new_line_to_gui(self, 'status_frame', 'status_text', new_line)
            elif (event.pathname[event.pathname.rfind('output'):] == 'output'):
                write_new_line_to_gui(self, 'output_frame', 'output_text', new_line)
            
#             #Information about method and event.  Uncomment to see events as they are generated
#            print("Method name: process_{}()\n"
#                   "Path name: {}\n"
#                   "Event Name: {}\n".format(method, event.pathname, event.maskname))
            
        
        _method_name.__name__ = "process_{}".format(method)
        setattr(cls, _method_name.__name__, _method_name)