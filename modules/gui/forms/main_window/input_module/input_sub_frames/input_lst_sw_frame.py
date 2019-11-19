###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The frame that displays and accepts user input when a Split Window process is run
#                       to calculate Land Surface Temperature using user supplied data and a landsat image.
# Created By          : Benjamin Kleynhans
# Creation Date       : July 16, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 16, 2019
# Filename            : input_lst_sw_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from datetime import date
from gui.forms.base_classes.gui_frame import Gui_Frame
from gui.forms.main_window.input_module.input_sub_frames.input_lst_sw_gb_frame import Input_Lst_Sw_Gb_Frame
from buoycalib import settings
import pdb

class Input_Lst_Sw_Frame(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "input_lst_sw_frame")
        
        # Add properties for gain and bias        
        master.frames[self.frame_name].input_values = {
                        'scene_id': '',
                        'lat': '',
                        'lon': '',
                        'emissivity_b10': '',
                        'emissivity_b11': '',
                        'add_gain_bias': False                        
                    }
            
        self.create_lst_sw_frame(master)
        
        
    # Create the actual frame as a separate window
    def create_lst_sw_frame(self, master):
                
        master.add(master.frames[self.frame_name], text = "Single")
        master.tab(2, state = 'hidden')
        
        self.create_scene_id(master)
        self.create_lat(master)
        self.create_lon(master)
        self.create_emissivity(master)
        
        # Create Input LandSufaceTemperature, SplitWindow GainBias frame
        Input_Lst_Sw_Gb_Frame(master.frames[self.frame_name])
        
        self.create_ask_gain_bias(master)
    
    # Create Scene ID text entry area with examples in frame
    def create_scene_id(self, master):
        
        # Read in the scene id
        ttk.Label(
                master.frames[self.frame_name],
                text = 'ID : ',
                width = 20).grid(
                        row = 0,
                        column = 0,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        master.frames[self.frame_name].input_values['scene_id'] = ttk.Entry(master.frames[self.frame_name], width = 80)
        master.frames[self.frame_name].input_values['scene_id'].grid(
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
                width = 20).grid(
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
                width = 30).grid(
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
                width = 30).grid(
                        row = 2,
                        column = 1,
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )
        
        self.scene_id = Text(master.frames[self.frame_name], height = 1, width = 40, borderwidth = 0)
        self.scene_id.insert(1.0, "LC08_L1TP_017030_20160614_20170220_01_T1")
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
        
    
    # Create Latitude entry area in frame
    def create_lat(self, master):
        
        # Read in the latitude
        ttk.Label(master.frames[self.frame_name], text = 'Latitude (dec) : ', width = 20).grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['lat'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['lat'].grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'e')
    
    
    # Create Longtitude entry area in frame
    def create_lon(self, master):
        
        # Read in the longtitude
        ttk.Label(master.frames[self.frame_name], text = 'Longtitude (dec) : ', width = 20).grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['lon'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['lon'].grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'e')
    
    
    # Create Latitude entry area in frame
    def create_emissivity(self, master):
        
        # Read in the latitude
        ttk.Label(master.frames[self.frame_name], text = 'Emissivity Band 10 : ', width = 20).grid(row = 3, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['emissivity_b10'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['emissivity_b10'].insert('end', settings.DEFAULT_EMIS_B10)
        master.frames[self.frame_name].input_values['emissivity_b10'].grid(row = 3, column = 3, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the longtitude
        ttk.Label(master.frames[self.frame_name], text = 'Emissivity Band 11 : ', width = 20).grid(row = 4, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['emissivity_b11'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['emissivity_b11'].insert('end', settings.DEFAULT_EMIS_B11)
        master.frames[self.frame_name].input_values['emissivity_b11'].grid(row = 4, column = 3, padx = 10, pady = 10, sticky = 'e')
    
    
    # Create checkbox to ask for usage of gain and bias
    def create_ask_gain_bias(self, master):

        add_gain_bias = ttk.Checkbutton(
                            master.frames[self.frame_name], 
                            text = "Add Gain and Bias to Calculation", 
                            variable = master.frames[self.frame_name].input_values['add_gain_bias'],
                            command = lambda: self.change_frame_state(master))
        
        add_gain_bias.grid(row = 5, column = 0, padx = 10, pady = (10, 0), sticky = 'w')
    
    
    # Change the state of the gain and bias properties
    def change_frame_state(self, master):
        
        master.frames[self.frame_name].input_values['add_gain_bias'] = not master.frames[self.frame_name].input_values['add_gain_bias']
        
        if master.frames[self.frame_name].input_values['add_gain_bias']:
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['gain_b10'].configure(state = 'normal')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['gain_b11'].configure(state = 'normal')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['bias_b10'].configure(state = 'normal')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['bias_b11'].configure(state = 'normal')
        else:
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['gain_b10'].configure(state = 'disabled')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['gain_b11'].configure(state = 'disabled')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['bias_b10'].configure(state = 'disabled')
            master.frames[self.frame_name].frames['input_lst_sw_gb_frame'].input_values['bias_b11'].configure(state = 'disabled')