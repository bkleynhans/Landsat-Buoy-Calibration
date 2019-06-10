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
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from datetime import date
from gui.forms.base_classes.gui_frame import Gui_Frame
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
        
        
    # Create the actual frame as a separate window
    def create_partial_single_frame(self, master):
                
        master.add(master.frames[self.frame_name], text = "Single")
        master.tab(1, state = 'hidden')
        
        # Read in the date
        ttk.Label(master.frames[self.frame_name], text = 'Date : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['date_frame_container']['frame'] = ttk.Frame(master.frames[self.frame_name])
        master.input_values['date_frame_container']['frame'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
        self.setup_date_picker(master.master.notebooks['input_notebook'].input_values['date_frame_container'])
        
        
        # Read in the latitude
        ttk.Label(master.frames[self.frame_name], text = 'Latitude (dec) : ', width = 20).grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['lat'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['lat'].grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the lontitude
        ttk.Label(master.frames[self.frame_name], text = 'Lontitude (dec) : ', width = 20).grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.input_values['lon'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['lon'].grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the surface temperature
        ttk.Label(master.frames[self.frame_name], text = 'Surface Temperature (K) : ', width = 20).grid(row = 3, column = 0, padx = 10, pady = (10, 0), sticky = 'w')
        
        master.input_values['surface_temp'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.input_values['surface_temp'].grid(row = 3, column = 1, padx = 10, pady = (10, 0), sticky = 'e')