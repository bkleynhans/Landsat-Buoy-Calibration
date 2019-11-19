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
# Last Modified Date  : October 30, 2019
# Filename            : settings_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gui.forms.base_classes.gui_notebook import Gui_Notebook
from gui.forms.settings.notebook_frames.general_settings_frame import General_Settings_Frame
import pdb

class Settings_Notebook(Gui_Notebook):
    
    # Preferences
    preferences = {
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
    
    # Settings Notebook constructor
    def __init__(self, master):
        
        Gui_Notebook.__init__(self, master, "settings_notebook")
        self.create_settings_notebook(master)
        
        
    # Create the settings_notebook object that will contain all the tabs
    def create_settings_notebook(self, master):
        
        master.notebooks[self.notebook_name].preferences = Settings_Notebook.preferences
        
        master.notebooks[self.notebook_name].pack(anchor = 'w', fill = BOTH, expand = True, padx = 10, pady = 10)
        
#        pdb.set_trace()
        # Add the General frame to the notebook
#        General_Settings_Frame(master.notebooks[self.notebook_name
        master.notebooks[self.notebook_name].add(General_Settings_Frame(master.notebooks[self.notebook_name]), text = "General")
        master.notebooks[self.notebook_name].tab(0, state = 'normal')
#        self.add(General_Settings_Frame(master.notebooks[self.notebook_name]), text = "General")
#        master.notebooks[self.notebook_name].add(ttk.Button(master.notebooks[self.notebook_name], text = "Click Me"))
        
#        General_Settings_Frame(self.settings_notebook)
        
#        self.general = ttk.Frame(self.settings_notebook)
#        self.settings_notebook.general = self.general
#        self.setup_general(self.settings_notebook)
        
        #self.settings_notebook.pack()
        

#   # Set up the tab containing general properties
#    def setup_general(self, settings_notebook):
#        
#        settings_notebook.add(settings_notebook.general, text = "General")
#        settings_notebook.tab(0, state = 'normal')
#        
#        # Read in the scene id
#        ttk.Label(settings_notebook.general, text = 'Clean Folders : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
#        
#        settings_notebook.input_values['general']['clean_folders'] = ttk.Entry(settings_notebook.general, width = 30)
#        settings_notebook.input_values['general']['clean_folders'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
#        
#        
#    # Set up the tab containing data sources
#    def setup_data_sources(self, settings_notebook):
#        
#        pass
#    
#    
#    # Set up the tab containing ModTran settings
#    def setup_modtran(self, settings_notebook):
#        
#        pass
#    
#    
#    # Set up the tab containing credentials
#    def setup_credentials(self, settings_notebook):
#        
#        pass
#        
#        
#    # Set up the tab containing database properties
#    def setup_database(self, settings_notebook):
#        
#        pass