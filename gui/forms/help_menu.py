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
# Filename            : progress_bar.py
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
     
    
    def open_webpage(self, url, progressbar_window):
        
        import webbrowser
        
        webbrowser.open_new(url)
        
        time.sleep(5)
        
        progressbar_window.progressbar.stop()
        progressbar_window.withdraw()
                
    
    def open_help(self, master):
        
        master.progressbar_window.progressbar.config(mode = 'indeterminate')
        
        master.progressbar_window.deiconify()
        master.progressbar_window.progressbar.start()
        
        threading.Thread(target=self.open_webpage, args=(self.GITHUB_PATH, master.progressbar_window, )).start()
        
        
    def __init__(self, master):
        
        self.open_help(master)
