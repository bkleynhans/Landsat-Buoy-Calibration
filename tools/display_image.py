#!/usr/bin/env python3
###
#
# Module for displaying images in seperate threads
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 21, 2019
# Filename            : display_image.py
#
###

# Imports
import threading
import cv2


class Display_Image():
    
    def __init__(self, data):
        
        display_image_thread = threading.Thread(target=self.open_image, args=(data, ))
        display_image_thread.start()

    # Display the image to the screen for 60 seconds, or until the window is closed.
    def open_image(self, data):
            
        window_title = 'Scene : ' + data['title']
        
        cv2.imshow(window_title, data['image'])
        cv2.waitKey(0)