###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : May 23, 2019
# Filename            : menu_bar.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import tarca_gui
import help_menu
from gui.forms import settings_frame

class Menu_Bar(tarca_gui.Tarca_Gui):
    
    def create_menu_bar(self, master):
        
        # Create menubar
        self.menu_bar = Menu(master)
        master.config(menu = self.menu_bar)
        master.menu_bar = self.menu_bar
    
        # Define the main menu options
        self.file_menu = Menu(self.menu_bar)
        self.edit_menu = Menu(self.menu_bar)
        self.help_menu = Menu(self.menu_bar)
        
        self.menu_bar.add_cascade(menu = self.file_menu, label = 'File')
        self.menu_bar.add_cascade(menu = self.edit_menu, label = 'Edit')
        
         # Define the File menu options
        self.file_menu.add_command(label = 'Exit', command = lambda: tarca_gui.on_closing(master))
        self.file_menu.entryconfig('Exit', accelerator = 'Ctrl+Q')
    
        # Define the Edit menu options
        self.edit_menu.add_command(label = 'Preferences', command = lambda: settings_frame.Settings_Frame(master))
    
        # Define the Help menu options        
        self.menu_bar.add_command(
                label = 'Help', 
                command = lambda: help_menu.Help_Menu(master)) # Open the readme file on the GitHub page for the project
    
    def __init__(self, master):
        
        self.create_menu_bar(master)
