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
# Filename            : gui.py
#
###

# Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pdb
import utilities
import time
import threading

class Tarca_Gui:
    
    def __init__(self, master):
        
        # Create the root Tkinter object
        master.title('CIS Top Of Atmosphere Radiance Calibration System')
        master.geometry('800x600')
        master.resizable(False, False)
        #master.configure(background = '#FFFFFF')
        
        master.option_add('*tearOff', False)
        
        # Create menubar
        self.menubar = Menu(master)
        master.config(menu = self.menubar)

        # Define the main menu options
        self.file = Menu(self.menubar)
        self.edit = Menu(self.menubar)
        self.help_ = Menu(self.menubar)
        
        self.menubar.add_cascade(menu = self.file, label = 'File')
        self.menubar.add_cascade(menu = self.edit, label = 'Edit')
        #self.menubar.add_cascade(menu = self.help_, label = 'Help')            # See "Define the Help menu options" for the current help menu
        
        # Create the progressbar object
        self.progressbar_window = Toplevel(master)                              # Create a progressbar toplevel window
        master.progressbar_window = self.progressbar_window                # Add the progressbar window to the master window as object variable
        
        self.progressbar_label = ttk.Label(self.progressbar_window, text = 'Loading Help Page ... ')
        self.progressbar_window.progressbar_label = self.progressbar_label
        
        self.progressbar_label.pack(anchor = 'sw', padx = 10, pady = (10, 0))
        
        self.progressbar = ttk.Progressbar(self.progressbar_window, orient = HORIZONTAL, length = 200)  # Create a progressbar
        self.progressbar_window.progressbar = self.progressbar                  # Add the progressbar to the progressbar window as object variable
                
        self.progressbar.pack(anchor = 'nw', padx = 10, pady = (0, 10))
        self.progressbar_window.withdraw()

        # Define the File menu options
        self.file.add_command(label = 'Exit', command = lambda: print('Clicked Exit'))
        self.file.entryconfig('Exit', accelerator = 'Ctrl+Q')

        # Define the Edit menu options
        self.edit.add_command(label = 'Preferences', command = lambda: print('Clicked Preferences'))

        # Define the Help menu options
        self.menubar.add_command(
                label = 'Help', 
                command = lambda: self.open_help(self.progressbar_window)) # open the readme file on the GitHub page for the project

        # Create the Header frame
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        # Add Radio Buttons to Header frame
        self.process_type = StringVar()
        ttk.Radiobutton(                
                self.frame_header,
                text = 'Full Process',
                variable = self.process_type,
                value = 'full').grid(
                        row = 0,
                        column = 0)

        ttk.Radiobutton(
                self.frame_header,
                text = 'Partial Process',
                variable = self.process_type,
                value = 'partial').grid(
                        row = 0,
                        column = 1)

        # Add the Content frame
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

    
    def open_help(self, progressbar_window):
        
        import webbrowser

        def open_webbrowser(self, url):
            
            webbrowser.open_new(url)
            
            time.sleep(5)
            progressbar_window.progressbar.stop()
            progressbar_window.withdraw()
            

        url_to_github_readme = 'https://github.com/bkleynhans/Landsat-Buoy-Calibration/blob/master/README.md'

        progressbar_window.progressbar.config(mode = 'indeterminate')        
        progressbar_window.deiconify()        
        progressbar_window.progressbar.start()
        
        threading.Thread(target=open_webbrowser, args=(self, url_to_github_readme, )).start()
        
        

def main():
    
    root = Tk()
    tarca_gui = Tarca_Gui(root)
    root.mainloop()
    
    
if __name__ == "__main__": main()
