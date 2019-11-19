###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Module Description  : This module is used as a subframe within the input_lst_sw frame specifically to 
#                       request data relating to gain and bias that is an optional argument
# Created By          : Benjamin Kleynhans
# Creation Date       : July 19, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 19, 2019
# Filename            : input_lst_sw_gb_frame.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from datetime import date
from gui.forms.base_classes.gui_label_frame import Gui_Label_Frame
from buoycalib import settings
import pdb

class Input_Lst_Sw_Gb_Frame(Gui_Label_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Label_Frame.__init__(self, master, "input_lst_sw_gb_frame", "Gain / Bias")
        
        master.frames[self.frame_name].input_values = {
                        'gain_b10': '',
                        'gain_b11': '',
                        'bias_b10': '',
                        'bias_b11': ''
                    }
        
        self.create_lst_sw_gb_frame(master)
        
        # Create the actual frame as a separate window
    def create_lst_sw_gb_frame(self, master):
                
        master.frames[self.frame_name].grid(row = 6, column = 0, columnspan = 4, padx = 10, pady = 10, sticky = 'nsew')
                
        # Add gain and bias as subframe within current frame
        self.create_gain_bias_b10(master)
        self.create_gain_bias_b11(master)
        
        
        # Create Gain and Bias entry area in frame for band 10
    def create_gain_bias_b10(self, master):
        
        # Read in the gain for band 10 row 5
        ttk.Label(master.frames[self.frame_name], text = 'Gain Band 10 : ', width = 20).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['gain_b10'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['gain_b10'].insert('end', settings.DEFAULT_GAIN_B10)
        master.frames[self.frame_name].input_values['gain_b10'].configure(state = 'disabled')
        master.frames[self.frame_name].input_values['gain_b10'].grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the bias for band 10 
        ttk.Label(master.frames[self.frame_name], text = 'Bias Band 10 : ', width = 20).grid(row = 0, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['bias_b10'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['bias_b10'].insert('end', settings.DEFAULT_BIAS_B10)
        master.frames[self.frame_name].input_values['bias_b10'].configure(state = 'disabled')
        master.frames[self.frame_name].input_values['bias_b10'].grid(row = 0, column = 3, padx = 10, pady = 10, sticky = 'e')
        
    # Create Gain and Bias entry area in frame for band 11
    def create_gain_bias_b11(self, master):
        
        # Read in the gain for band 11 row 6
        ttk.Label(master.frames[self.frame_name], text = 'Gain Band 11 : ', width = 20).grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['gain_b11'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['gain_b11'].insert('end', settings.DEFAULT_GAIN_B11)
        master.frames[self.frame_name].input_values['gain_b11'].configure(state = 'disabled')
        master.frames[self.frame_name].input_values['gain_b11'].grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'e')
        
        # Read in the bias for band 11
        ttk.Label(master.frames[self.frame_name], text = 'Bias Band 11 : ', width = 20).grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
        
        master.frames[self.frame_name].input_values['bias_b11'] = ttk.Entry(master.frames[self.frame_name], width = 30)
        master.frames[self.frame_name].input_values['bias_b11'].insert('end', settings.DEFAULT_BIAS_B11)
        master.frames[self.frame_name].input_values['bias_b11'].configure(state = 'disabled')
        master.frames[self.frame_name].input_values['bias_b11'].grid(row = 1, column = 3, padx = 10, pady = 10, sticky = 'e')