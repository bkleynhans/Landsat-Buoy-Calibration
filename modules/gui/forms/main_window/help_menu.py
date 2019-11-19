###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : The Help menu is very limited in this revision and only opens a link
#                       to the GitHub markdown readme file
# Created By          : Benjamin Kleynhans
# Creation Date       : May 23, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : October 29, 2019
# Filename            : help_menu.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import time
import threading
from gui.forms.general.progress_bar import Progress_Bar
import pdb


class Help_Menu():
    
    GITHUB_PATH = 'https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/master/README.md'
     
    # Help Menu constructor
    def __init__(self, master):
        
        self.open_help(master)
        
    
    # Open in github as a thread
    def open_webpage(self, url):
        
        import webbrowser
        
        webbrowser.open_new(url)
        
        time.sleep(10)
        
        self.progressbar.progressbar.stop()
        self.progressbar.progressbar_window.destroy()
                
    
    # Open the Help page from github
    def open_help(self, master):
        
        self.progressbar = Progress_Bar(master, 'Loading Help Page ... ')
        self.progressbar.progressbar.config(mode = 'indeterminate')
        
        self.progressbar.progressbar_window.deiconify()
        self.progressbar.progressbar.start()
        
        threading.Thread(target = self.open_webpage, args = (self.GITHUB_PATH, )).start()