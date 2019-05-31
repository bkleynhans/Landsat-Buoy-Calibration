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
# Last Modified Date  : May 29, 2019
# Filename            : help_menu.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
import time
import threading
import menu_bar


class Help_Menu(menu_bar.Menu_Bar):
    
    GITHUB_PATH = 'https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/master/README.md'
     
    # Help Menu constructor
    def __init__(self, master):
        
        self.open_help(master)
        
    
    # Open in github as a thread
    def open_webpage(self, url, progressbar_window):
        
        import webbrowser
        
        webbrowser.open_new(url)
        
        time.sleep(5)
        
        progressbar_window.progressbar.stop()
        progressbar_window.withdraw()
                
    
    # Open the Help page from github
    def open_help(self, master):
        
        master.progressbar_window.progressbar.config(mode = 'indeterminate')
        
        master.progressbar_window.deiconify()
        master.progressbar_window.progressbar.start()
        
        threading.Thread(target=self.open_webpage, args=(self.GITHUB_PATH, master.progressbar_window, )).start()