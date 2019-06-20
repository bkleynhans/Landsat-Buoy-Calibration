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
from gui.forms.base_classes.gui_frame import Gui_Frame
import pdb

class Input_Full_Single(Gui_Frame):
    
    # Settings Frame constructor
    def __init__(self, master):
        
        Gui_Frame.__init__(self, master, "input_full_single")
        self.create_full_single_frame(master)
        
    
    # Create the actual frame as a separate window
    def create_full_single_frame(self, master):
                
        master.add(master.frames[self.frame_name], text = "Single")
        master.tab(0, state = 'normal')
        
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
        
        master.input_values['scene_id_full_single'] = ttk.Entry(master.frames[self.frame_name], width = 60)
        master.input_values['scene_id_full_single'].grid(
                row = 0, 
                column = 1, 
                columnspan = 2,
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
                        padx = 10,
                        pady = 10,
                        sticky = 'nsew'
                )