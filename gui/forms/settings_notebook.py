###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Module Description  : Creates the settings_notebook that exists on the Settings Frame.  Also
#                       handles all data input from the Settings Frame
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 30, 2019
# Filename            : settings_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Settings_Notebook():
    
    # Settings Notebook constructor
    def __init__(self, master, frame_name):
        
        self.create_notebook(master.frames[frame_name])
        
        
    # Create the settings_notebook object that will contain all the tabs
    def create_notebook(self, settings_frame):
        
        self.settings_notebook = ttk.Notebook(settings_frame)
        settings_frame.settings_notebook = self.settings_notebook
        
        self.settings_notebook.input_values = {
                'general': {
                        'clean_folders': 'False',
                        'folder_size': '500'},
                'scene_id': '',
                'date_frame_container': {
                    'frame': '',
                    'date_picker': '',
                    'date_label': '',
                    'date': ''},
                'lat': '',
                'lon': '',
                'surface_temp': ''
        }
                
        self.general = ttk.Frame(self.settings_notebook)
        self.settings_notebook.general = self.general
        self.setup_general(self.settings_notebook)
        
        self.settings_notebook.pack()
        

   # Set up the tab required for full processing of single Scene ID
    def setup_general(self, settings_notebook):
        
        settings_notebook.add(settings_notebook.general, text = "General")
        settings_notebook.tab(0, state = 'normal')
        
        # Read in the scene id
        ttk.Label(settings_notebook.general, text = 'Clean Folders : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        settings_notebook.input_values['general']['clean_folders'] = ttk.Entry(settings_notebook.general, width = 30)
        settings_notebook.input_values['general']['clean_folders'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        
    