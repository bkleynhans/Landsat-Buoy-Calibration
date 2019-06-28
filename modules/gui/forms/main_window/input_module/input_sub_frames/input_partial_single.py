###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 30, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 30, 2019
# Filename            : input_full_single.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
#from tkinter import messagebox
#from tkcalendar import Calendar, DateEntry
from datetime import date
from gui.forms.base_classes.gui_frame import Gui_Frame
from buoycalib import settings
import pdb

class Input_Partial_Single(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "input_partial_single")
        self.create_partial_single_frame(master)
        
    
    # Update the dates in the date_picker variable as well as the date variable
    def update_dates(self, date_frame_container):
        
        date_frame_container['date_picker'].set_date(date.today())
        date_frame_container['date'] = date_frame_container['date_picker'].get_date()
        
    
    #### --> Date Picker removed, will now get date from LandSat ID
#    # Create an instance of the datepicker and place it on the tab
#    def setup_date_picker(self, date_frame_container):
#        
#        calendar_style = ttk.Style(date_frame_container['frame'])
#        calendar_style.theme_use('clam')
#        
#        date_frame_container['date_label'] = ttk.Label(
#                date_frame_container['frame'],
#                anchor='w',
#                text='Today: %s' % date.today().strftime('%x'))
#        date_frame_container['date_label'].pack(side = LEFT, anchor = 'w', fill='x')
#        
#        date_frame_container['date_picker'] = DateEntry(date_frame_container['frame'])
#        date_frame_container['date_picker'].pack(side = RIGHT, anchor = 'e', padx = 10, pady = 10)
#                
#        date_frame_container['date_label'].bind("<Button-1>", lambda e : self.update_dates(date_frame_container))
        
        
    # Create the actual frame as a separate window
    def create_partial_single_frame(self, master):
                
        master.add(master.frames[self.frame_name], text = "Single")
        master.tab(1, state = 'hidden')
        
        self.create_scene_id(master)
        self.create_lat(master)
        self.create_lon(master)
        self.create_emissivity(master)
        self.create_surface_temperature(master)
        
        
        #### --> Date Picker removed, will now get date from LandSat ID
#        # Read in the date
#        ttk.Label(master.frames[self.frame_name], text = 'Date : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
#        
#        master.input_values['date_frame_container']['frame'] = ttk.Frame(master.frames[self.frame_name])
#        master.input_values['date_frame_container']['frame'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
#        self.setup_date_picker(master.master.notebooks['input_notebook'].input_values['date_frame_container'])
    
    
    # Create Scene ID text entry area with examples in frame
    def create_scene_id(self, master):
        
        # Read in the scene id
        ttk.Label(
                master.frames[self.frame_name],
                text = 'ID : ',
                width = 15).grid(
                        row = 0,
                        column = 0,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        master.input_values['scene_id_partial_single'] = ttk.Entry(master.frames[self.frame_name], width = 60)
        master.input_values['scene_id_partial_single'].grid(
                row = 0, 
                column = 1, 
                columnspan = 3,
                padx = 10,
                pady = 10,
                sticky = 'nsew'
        )
            
        # Header for examples        
        self.reference_label = ttk.Label(
                master.frames[self.frame_name],
                text = 'Example IDs :',
                width = 15).grid(
                        row = 1,
                        column = 0,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
                
        # Valid format examples
        ttk.Label(
                master.frames[self.frame_name],
                text = 'Scene Id :',
                width = 20).grid(
                        row = 1,
                        column = 1,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        self.scene_id = Text(master.frames[self.frame_name], height = 1, width = 40, borderwidth = 0)
        self.scene_id.insert(1.0, "LC80110312017350LGN00")
        self.scene_id.configure(
                state = 'disabled',
                inactiveselectbackground = self.scene_id.cget('selectbackground'))
        self.scene_id.grid(
                        row = 1,
                        column = 2,
                        columnspan = 2, 
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        ttk.Label(
                master.frames[self.frame_name],
                text = 'Landsat Product Identifier :',
                width = 20).grid(
                        row = 2,
                        column = 1,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        self.scene_id = Text(master.frames[self.frame_name], height = 1, width = 40, borderwidth = 0)
        self.scene_id.insert(1.0, "LC08_L1GT_029030_20151209_20160131_01_RT")
        self.scene_id.configure(
                state = 'disabled',
                inactiveselectbackground = self.scene_id.cget('selectbackground'))
        self.scene_id.grid(
                        row = 2,
                        column = 2,
                        columnspan = 2, 
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
    
    # Create Surface Temperature entry area in frame
    def create_surface_temperature(self, master):
        
        # Read in the surface temperature
        ttk.Label(master.frames[self.frame_name], text = 'Surface Temperature (K) : ', width = 20).grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['surface_temp'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['surface_temp'].grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        
    # Create Latitude entry area in frame
    def create_lat(self, master):
        
        # Read in the latitude
        ttk.Label(master.frames[self.frame_name], text = 'Latitude (dec) : ', width = 20).grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['lat'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['lat'].grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'e')
    
    
    # Create Longtitude entry area in frame
    def create_lon(self, master):
        
        # Read in the longtitude
        ttk.Label(master.frames[self.frame_name], text = 'Longtitude (dec) : ', width = 20).grid(row = 5, column = 0, padx = 10, pady = (10, 0), sticky = 'w')
        
        master.input_values['lon'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['lon'].grid(row = 5, column = 1, padx = 10, pady = (10, 0), sticky = 'e')
    
    
    # Create Latitude entry area in frame
    def create_emissivity(self, master):
        
        # Read in the latitude
        ttk.Label(master.frames[self.frame_name], text = 'Emissivity Band 10 : ', width = 20).grid(row = 4, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['emissivity_b10'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['emissivity_b10'].insert('end', settings.DEFAULT_EMIS_B10)
        master.input_values['emissivity_b10'].grid(row = 4, column = 3, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the longtitude
        ttk.Label(master.frames[self.frame_name], text = 'Emissivity Band 11 : ', width = 20).grid(row = 5, column = 2, padx = 10, pady = (10, 0), sticky = 'w')
        
        master.input_values['emissivity_b11'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['emissivity_b11'].insert('end', settings.DEFAULT_EMIS_B11)
        master.input_values['emissivity_b11'].grid(row = 5, column = 3, padx = 10, pady = (10, 0), sticky = 'e')
    
    
    