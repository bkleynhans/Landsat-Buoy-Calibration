###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 28, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 29, 2019
# Filename            : input_notebook.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gui.forms import input_frame
from tkcalendar import Calendar, DateEntry
from datetime import date


class Input_Notebook(input_frame.Input_Frame):
    
    # Input Notebook constructor
    def __init__(self, master):
        
        self.create_notebook(master.input_frame)
        
        
    # Create the input_notebook object that will contain all the tabs
    def create_notebook(self, input_frame):
        
        self.input_notebook = ttk.Notebook(input_frame)
        input_frame.input_notebook = self.input_notebook
        
        self.input_notebook.input_values = {'batch_file': '',
                                      'scene_id': '',
                                      'date_frame_container': {
                                              'frame': '',
                                              'date_picker': '',
                                              'date_label': '',
                                              'date': ''},
                                      'lat': '',
                                      'lon': '',
                                      'surface_temp': ''}
        
        self.full_single = ttk.Frame(self.input_notebook)
        self.input_notebook.full_single = self.full_single
        self.setup_full_single(self.input_notebook)
        
        self.partial_single = ttk.Frame(self.input_notebook)
        self.input_notebook.partial_single = self.partial_single
        self.setup_partial_single(self.input_notebook)
        
        self.full_batch = ttk.Frame(self.input_notebook)
        self.input_notebook.full_batch = self.full_batch
        self.setup_batch(self.input_notebook)        
        
        self.input_notebook.pack()
        
        
    # Update the dates in the date_picker variable as well as the date variable
    def update_dates(self, date_frame_container):
        
        date_frame_container['date_picker'].set_date(date.today())
        date_frame_container['date'] = date_frame_container['date_picker'].get_date()
        
    
    # Create an instance of the datepicker and place it on the tab
    def setup_date_picker(self, date_frame_container):
        
        calendar_style = ttk.Style(date_frame_container['frame'])
        calendar_style.theme_use('clam')
        
        date_frame_container['date_label'] = ttk.Label(
                date_frame_container['frame'],
                anchor='w',
                text='Today: %s' % date.today().strftime('%x'))
        date_frame_container['date_label'].pack(side = LEFT, anchor = 'w', fill='x')
        
        date_frame_container['date_picker'] = DateEntry(date_frame_container['frame'])
        date_frame_container['date_picker'].pack(side = RIGHT, anchor = 'e', padx = 10, pady = 10)
                
        date_frame_container['date_label'].bind("<Button-1>", lambda e : self.update_dates(date_frame_container))
        
    
    # Display file dialog so user may select the batch file with required data
    def display_file_dialog(self, input_notebook):
        
        input_notebook.input_values['batch_file'].delete(0, END)
        
        file_path = filedialog.askopenfile().name
        
        if (file_path != None):
            
            input_notebook.input_values['batch_file'].insert(0, file_path)
        
    
    # Set up the tab required for full processing of single Scene ID
    def setup_full_single(self, input_notebook):
        
        input_notebook.add(input_notebook.full_single, text = "Single")
        input_notebook.tab(0, state = 'hidden')
        
        # Read in the scene id
        ttk.Label(input_notebook.full_single, text = 'Scene ID : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['scene_id'] = ttk.Entry(input_notebook.full_single, width = 30)
        input_notebook.input_values['scene_id'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
        
    
    # Set up the tab required for partial processing of single Scene ID
    def setup_partial_single(self, input_notebook):
        
        input_notebook.add(input_notebook.partial_single, text = "Single")
        input_notebook.tab(1, state = 'hidden')
        
        # Read in the date
        ttk.Label(input_notebook.partial_single, text = 'Date : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['date_frame_container']['frame'] = ttk.Frame(input_notebook.partial_single)
        input_notebook.input_values['date_frame_container']['frame'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
        self.setup_date_picker(input_notebook.input_values['date_frame_container'])
        
        
        # Read in the latitude
        ttk.Label(input_notebook.partial_single, text = 'Latitude (dec) : ', width = 20).grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['lat'] = ttk.Entry(input_notebook.partial_single, width = 30)
        input_notebook.input_values['lat'].grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the lontitude
        ttk.Label(input_notebook.partial_single, text = 'Lontitude (dec) : ', width = 20).grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['lon'] = ttk.Entry(input_notebook.partial_single, width = 30)
        input_notebook.input_values['lon'].grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the surface temperature
        ttk.Label(input_notebook.partial_single, text = 'Surface Temperature (K) : ', width = 20).grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['surface_temp'] = ttk.Entry(input_notebook.partial_single, width = 30)
        input_notebook.input_values['surface_temp'].grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'e')
    
    
    # Set up the tab requried for processing of Batches.  Type is determined by radio button
    def setup_batch(self, input_notebook):
        
        input_notebook.add(input_notebook.full_batch, text = "Batch")
        input_notebook.tab(2, state = 'hidden')
        
        # Read in the source file location
        ttk.Label(input_notebook.full_batch, text = 'Source File : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        input_notebook.input_values['batch_file'] = ttk.Entry(input_notebook.full_batch, width = 30)
        input_notebook.input_values['batch_file'].grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = 10, sticky = 'w')
        
        
        self.browse_button = ttk.Button(
                input_notebook.full_batch,
                text = 'Browse',
                command = lambda: self.display_file_dialog(input_notebook)).grid(
                        row = 0,
                        column = 3,
                        padx = 10,
                        pady = 10,
                        sticky = 'w'
                )