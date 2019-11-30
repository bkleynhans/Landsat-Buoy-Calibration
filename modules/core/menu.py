###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Terminal based menu for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 11, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 2, 2019
# Filename            : menu.py
#
###

# Imports

import sys
import os
import cv2
import subprocess as sp
from buoycalib import settings
from modules.core.model import Model

# Erases a line of output without adding a newline
ERASE_LINE = '\x1b[2K'    

# Request name of text file containing batch process scene IDs
def model_batch_sc_buoy(project_root):
    
    import test_paths
    
    display_images = display_processed_images(True)
    
    batchFileDirectory = 'input/batches/'
    batchFileName = input("\n Please enter the name of the batch file or 'X' to exit : ")
    batchFile = os.path.join(batchFileDirectory, batchFileName)
    
    if (batchFile[(batchFile.rfind('/') + 1):].upper()) != 'X':
        valid_data = test_paths.main([batchFile, "-tfile"])
        
        if not valid_data:
            batchFile = input("\n The batch file you entered is invalid, please try again ('X' - exit): ")
            
            if batchFile.upper() != 'X':
                valid_data = test_paths.main([batchFile, "-tfile"])
            
    
        if batchFile.upper() != 'X':
            
            # Read in the file
            scenes = open(batchFile).readlines()
            
            counter = 0
            error_list = {"errors":[]}
            
            for scene in scenes:
                
                counter += 1
                
                if not is_valid_id(scene):
                    
                    error = {}
                    error["idx"] = counter
                    error["scene"] = scene
                    
                    error_list["errors"].append(error)
            
            
            if (len(error_list['errors']) > 0):
                
                sys.stdout.write("\n\n*********************************************************************\n")
                sys.stdout.write("*  !!!   The following errors were found in your batch file   !!!   *\n")
                sys.stdout.write("*********************************************************************\n")
            
                for error in error_list['errors']:
                    sys.stdout.write("  line : %5s         scene : %s" % (error['idx'], error['scene']))
                    
                sys.stdout.write("\n\n")
                
                input("Press Enter to continue...")
                    
            else:
            
                # Launch batch process job
                Model('menu', 'batch', 'sc', 'buoy', batchFile, 'merra', display_images, project_root, False, None)


# Request Scene ID for single scene to calculate
def model_single_sc_buoy(project_root):
    
    display_images = display_processed_images(False)
    
    sceneId = input("\n Please enter the Scene ID to continue or 'X' to exit : ")
    
    if sceneId.upper() != 'X':
        valid_data = is_valid_id(sceneId)
    
        if not valid_data:
            while not valid_data:
                sceneId = input("\n The Scene ID you entered is invalid, please try again ('X' - exit) : ")
                
                if sceneId.upper() != 'X':
                    valid_data = is_valid_id(sceneId)
                else:
                    break
    
        if sceneId.upper() != 'X':            
            
            # Launch single scene ID process job
            Model('menu', 'single', 'sc', 'buoy', sceneId, 'merra', display_images, project_root, False, None)


# Request information to perform partial calculation
# scene_id, latitude, lontitude, surface temperature, emissivity band 10, emissivity band 11
def model_single_sc_toa(project_root):
    
    display_images = False
    partial_data = {}
    
    sceneId = input("\n Please enter the Scene ID to continue or 'X' to exit : ")
    
    if sceneId.upper() != 'X':
        valid_data = is_valid_id(sceneId)
    
        if not valid_data:
            while not valid_data:
                sceneId = input("\n The Scene ID you entered is invalid, please try again ('X' - exit) : ")
                
                if sceneId.upper() != 'X':
                    valid_data = is_valid_id(sceneId)
                else:
                    break
    
        if sceneId.upper() != 'X':
            
            # Get skin temperature from user
            skin_temp = input("\n Please enter the surface temperature : ")
            
            # Perform data validation (200 - 350 K)
            if not is_valid_temp(skin_temp):
                while not is_valid_temp(skin_temp):
                    skin_temp = input("\n The skin temperature you entered is not in the valid range of 200 to 350, please try again : ")
            
            skin_temp = float(skin_temp)
        
            partial_data['skin_temp'] = skin_temp
            
            # Get latitude from user
            lat = input("\n Please enter the latitude for the supplied surface temperature (decimal range -90 to 90) : ")
            
            # Perform data validation        
            if not is_valid_latitude(lat):
                while not is_valid_latitude(lat):
                    lat = input("\n The Latitude you entered is not in the valid range of -90 to 90, please try again : ")
            
            lat = float(lat)
            
            partial_data['lat'] = lat
            
            # Get longitude from user
            lon = input("\n Please enter the longitude for the supplied surface temperature (decimal range -180  to 180) : ")
            
            # Perform data validation
            if not is_valid_longitude(lon):
                while not is_valid_longitude(lon):
                    lon = input("\n The Longitude you entered is not in the valid range of -180 to 180, please try again : ")
            
            lon = float(lon)
        
            partial_data['lon'] = lon
        
            # Get band 10 emissivity from user
            emis_b10 = input("\n Please enter the emissivity for Band 10 (Press enter for default %s) : " % settings.DEFAULT_EMIS_B10)
            
            # Perform data validation
            if data_entered(emis_b10):
                if not is_valid_emissivity(emis_b10):
                    while not is_valid_emissivity(emis_b10):
                        emis_b10 = input("\n The Emissivity you entered for Band 10 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_EMIS_B10)
                        
                        if not data_entered(emis_b10):
                            emis_b10 = settings.DEFAULT_EMIS_B10
                else:
                    emis_b10 = float(emis_b10)
            else:
                emis_b10 = settings.DEFAULT_EMIS_B10
            
            partial_data['emis_b10'] = emis_b10
            
            # Get band 11 emissivity from user
            emis_b11 = input("\n Please enter the emissivity for Band 11 (Press enter for default %s) : " % settings.DEFAULT_EMIS_B11)
    
            # Perform data validation
            if data_entered(emis_b11):
                if not is_valid_emissivity(emis_b11):
                    while not is_valid_emissivity(emis_b11):
                        emis_b11 = input("\n The Emissivity you entered for Band 11 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_EMIS_B11)
                        
                        if not data_entered(emis_b11):
                            emis_b11 = settings.DEFAULT_EMIS_B10
                else:
                    emis_b11 = float(emis_b11)
            else:
                emis_b11 = settings.DEFAULT_EMIS_B11
            
            partial_data['emis_b11'] = emis_b11
            
            # Launch single scene ID process job
            Model('menu', 'single', 'sc', 'toa', sceneId, 'merra', display_images, project_root, False, partial_data)


# Request information to perform partial calculation
# scene_id, latitude, lontitude, surface temperature, emissivity band 10, emissivity band 11
def model_single_sw_lst(project_root):
    
    display_images = False
    partial_data = {}
    
    sceneId = input("\n Please enter the Scene ID to continue or 'X' to exit : ")
    
    if sceneId.upper() != 'X':
        valid_data = is_valid_id(sceneId)
    
        if not valid_data:
            while not valid_data:
                sceneId = input("\n The Scene ID you entered is invalid, please try again ('X' - exit) : ")
                
                if sceneId.upper() != 'X':
                    valid_data = is_valid_id(sceneId)
                else:
                    break
    
        if sceneId.upper() != 'X':
            
            # Get latitude from user
            lat = input("\n Please enter the latitude to use for processing (decimal range -90 to 90) : ")
            
            # Perform data validation        
            if not is_valid_latitude(lat):
                while not is_valid_latitude(lat):
                    lat = input("\n The Latitude you entered is not in the valid range of -90 to 90, please try again : ")
            
            lat = float(lat)
            
            partial_data['lat'] = lat
            
            # Get longitude from user
            lon = input("\n Please enter the longitude to use for processing (decimal range -180  to 180) : ")
            
            # Perform data validation
            if not is_valid_longitude(lon):
                while not is_valid_longitude(lon):
                    lon = input("\n The Longitude you entered is not in the valid range of -180 to 180, please try again : ")
            
            lon = float(lon)
        
            partial_data['lon'] = lon
        
            # Get band 10 emissivity from user
            emis_b10 = input("\n Please enter the emissivity for Band 10 (Press enter for default %s) : " % settings.DEFAULT_EMIS_B10)
            
            # Perform data validation
            if data_entered(emis_b10):
                if not is_valid_emissivity(emis_b10):
                    while not is_valid_emissivity(emis_b10):
                        emis_b10 = input("\n The Emissivity you entered for Band 10 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_EMIS_B10)
                        
                        if not data_entered(emis_b10):
                            emis_b10 = settings.DEFAULT_EMIS_B10
                else:
                    emis_b10 = float(emis_b10)
            else:
                emis_b10 = settings.DEFAULT_EMIS_B10
            
            partial_data['emis_b10'] = emis_b10
            
            # Get band 11 emissivity from user
            emis_b11 = input("\n Please enter the emissivity for Band 11 (Press enter for default %s) : " % settings.DEFAULT_EMIS_B11)
    
            # Perform data validation
            if data_entered(emis_b11):
                if not is_valid_emissivity(emis_b11):
                    while not is_valid_emissivity(emis_b11):
                        emis_b11 = input("\n The Emissivity you entered for Band 11 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_EMIS_B11)
                        
                        if not data_entered(emis_b11):
                            emis_b11 = settings.DEFAULT_EMIS_B10
                else:
                    emis_b11 = float(emis_b11)
            else:
                emis_b11 = settings.DEFAULT_EMIS_B11
            
            partial_data['emis_b11'] = emis_b11
            
            # Ask if gain and bias needs to be added to the equasion
            if add_gain_bias():
                
                partial_data['add_gain_bias'] = True
                
                # Get band 10 gain from user
                gain_b10 = input("\n Please enter the gain for Band 10 (Press enter for default %s) : " % settings.DEFAULT_GAIN_B10)
        
                # Perform data validation
                if data_entered(gain_b10):
                    if not is_number(gain_b10):
                        while not is_number(gain_b10):
                            gain_b10 = input("\n The Gain you entered for Band 10 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_GAIN_B10)
                            
                            if not data_entered(gain_b10):
                                gain_b10 = settings.DEFAULT_GAIN_B10
                    else:
                        gain_b10 = float(gain_b10)
                else:
                    gain_b10 = settings.DEFAULT_GAIN_B10
                
                partial_data['gain_b10'] = gain_b10
                
                # Get band 10 bias from user
                bias_b10 = input("\n Please enter the bias for Band 10 (Press enter for default %s) : " % settings.DEFAULT_BIAS_B10)
        
                # Perform data validation
                if data_entered(bias_b10):
                    if not is_number(bias_b10):
                        while not is_number(bias_b10):
                            bias_b10 = input("\n The Gain you entered for Band 10 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_BIAS_B10)
                            
                            if not data_entered(bias_b10):
                                bias_b10 = settings.DEFAULT_BIAS_B10
                    else:
                        bias_b10 = float(bias_b10)
                else:
                    bias_b10 = settings.DEFAULT_BIAS_B10
                
                partial_data['bias_b10'] = bias_b10
                
                # Get band 11 gain from user
                gain_b11 = input("\n Please enter the gain for Band 11 (Press enter for default %s) : " % settings.DEFAULT_GAIN_B11)
        
                # Perform data validation
                if data_entered(gain_b11):
                    if not is_number(gain_b11):
                        while not is_number(gain_b11):
                            gain_b11 = input("\n The Gain you entered for Band 11 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_GAIN_B11)
                            
                            if not data_entered(gain_b11):
                                gain_b11 = settings.DEFAULT_GAIN_B11
                    else:
                        gain_b11 = float(gain_b11)
                else:
                    gain_b11 = settings.DEFAULT_GAIN_B11
                
                partial_data['gain_b11'] = gain_b11
                
                # Get band 11 bias from user
                bias_b11 = input("\n Please enter the bias for Band 11 (Press enter for default %s) : " % settings.DEFAULT_BIAS_B11)
        
                # Perform data validation
                if data_entered(bias_b11):
                    if not is_number(bias_b11):
                        while not is_number(bias_b11):
                            bias_b11 = input("\n The Gain you entered for Band 11 is invalid, please try again (Press enter for default %s) : " % settings.DEFAULT_BIAS_B11)
                            
                            if not data_entered(bias_b11):
                                bias_b11 = settings.DEFAULT_BIAS_B11
                    else:
                        bias_b11 = float(bias_b11)
                else:
                    bias_b11 = settings.DEFAULT_BIAS_B11
                
                partial_data['bias_b11'] = bias_b11
            
            else:
                
                partial_data['add_gain_bias'] = False
                
                partial_data['gain_b10'] = 0
                partial_data['gain_b11'] = 0
                partial_data['bias_b10'] = 0
                partial_data['bias_b11'] = 0
                
            
            # Launch single scene ID process job
            Model('menu', 'single', 'sw', 'lst', sceneId, 'merra', display_images, project_root, False, partial_data)


# Checks to see if any data was entered into the variable supplied and returns true or false
def data_entered(input_value):
    
    returnValue = False
    
    if input_value != '':
        returnValue = True
    
    return returnValue


# Test if the supplied latitude is within the valid range
def is_valid_latitude(input_value):
    
    returnValue = False
    
    if data_entered(input_value):
        try:
            input_value = float(input_value)
            
            if ((input_value >= -90) and (input_value <= 90)):
                returnValue = True
            
        except ValueError:            
            pass
    
    return returnValue


# Test if the supplied longitude is within the valid range
def is_valid_longitude(input_value):
    
    returnValue = False
    
    if data_entered(input_value):
        try:
            input_value = float(input_value)
            
            if ((input_value >= -180) and (input_value <= 180)):
                returnValue = True            
                
        except ValueError:
            pass
    
    return returnValue


# Test if the supplied surface temperature is within the valid range
def is_valid_temp(input_value):
    
    returnValue = False
    
    if data_entered(input_value):
        try:
            input_value = float(input_value)
            
            if ((input_value >= 200) and (input_value <= 350)):
                returnValue = True            
                
        except ValueError:
            pass
    
    return returnValue


# Test if the supplied emissivities are within valid ranges
def is_valid_emissivity(input_value):
    
    returnValue = False
    
    try:
        input_value = float(input_value)
        
        if ((input_value >= 0.8) and (input_value <= 1)):
            returnValue = True
            
    except ValueError:
        pass
                
    return returnValue


# Test if the user provided a value of the correct data type
def is_number(input_value):
    
    returnValue = False
    
    try:
        float(input_value)
        
        returnValue = True
        
    except ValueError:
        pass
    
    return returnValue


# Test if the input format matches the required input format
def is_valid_id(input_value):
    
    returnValue = False
    
    # import regular expression module
    import re
    
    # Scene ID format                       - LC80140372017307LGN00 
    scene_id_regex_string = ('(L)'                                              # Landsat (L)
                            '(C|O|T|E|M)'                                       # Sensor ("C" = OLI/TIRS Combined, "O" = OLI-only, "T" = TIRS-only and TM, "E" = ETM+, "M" = MSS)
                            '(7|8)'                                             # Satellite (7 - 8)
                            '([0-9][0-9][0-9])'                                 # WRS path (000 - 999)
                            '([0-9][0-9][0-9])'                                 # WRS row (000 - 999)
                            '((19[7-9][0-9])|(2[0-2][0-9][0-9]))'               # Year (1970 - 2299)
                            '(([0-2][0-9][0-9])|(3[0-5][0-9])|(36[0-6]))'       # Julian day of year (1 - 366)
                            '([A-Z][A-Z][A-Z])'                                 # Ground station identifier (AAA - ZZZ)
                            '([0-2][0-9])')                                     # Archive version number (00 - 29)
                            
    re_scene_id = re.compile(scene_id_regex_string)
    
    # Landsat Product Identifier format     - LC08_L1GT_029030_20151209_20160131_01_RT
    lan_prod_id_regex_string =  ('('                                            # --> LC08
                                '(L)'                                           # Landsat (L)
                                '(C|O|T|E|M)'                                   # Sensor ("C" = OLI/TIRS Combined, "O" = OLI-only, "T" = TIRS-only and TM, "E" = ETM+, "M" = MSS)
                                '(07|08)'                                       # Satellite (7-8)
                                ')_('                                           # --> L1GT
                                '(L1TP|L1GT|L1GS)'                              # Processing ccorrection level ("L1TP" = Precision Terrain, "L1GT" = Systematic Terrain, "L1GS" = Systematic)
                                ')_('                                           # --> 029030
                                '([0-9][0-9][0-9])'                             # WRS path (000 - 999)
                                '([0-9][0-9][0-9])'                             # WRS row (000 - 999)
                                ')_('                                           # --> 20151209
                                '((19[7-9][0-9])|(2[0-2][0-9][0-9]))'           # Acquisition date (1970 - 2299)
                                '(0[0-9]|1[0-2])([0-2][0-9]|3[0-1])' 
                                ')_('                                           # --> 20160131
                                '((19[7-9][0-9])|(2[0-2][0-9][0-9]))'           # Processing date (1970 - 2299)
                                '(0[0-9]|1[0-2])([0-2][0-9]|3[0-1])' 
                                ')_('                                           # --> 01
                                '([0-2][0-9])'                                  # Collection number (00 - 29)
                                ')_('                                           # --> RT
                                '(RT|T1|T2)'                                     # Collection category ("RT" = Real-Time, "T1" = Tier 1, "T2" = Tier 2)
                                ')')
    
    re_lan_prod_id = re.compile(lan_prod_id_regex_string)
    
    if re_scene_id.match(input_value) or re_lan_prod_id.match(input_value):
            returnValue = True
    
    return returnValue


# Test if the database server is available
def testDb():

    from modules.db import db_connection
    
    db_test_con = db_connection.Db_Connection()

    db_status = db_test_con.db_available()
    
    from modules.db import db_construction
    
    constructor = db_construction.Db_Construction()
    
    constructor.prepare_database()
    
    print()
    
    return db_status


# Test if the terminal session allows export of display
def export_display_available():
    
    returnValue = False
    
    if "DISPLAY" in os.environ:
        returnValue = True
    
    return returnValue


# Ask the user if they want to display each image as it is processed
def add_gain_bias():
    
    gain_bias = False
    
    question = "\n Do you want to add gain and bias to the calculation? (Y/N) (Press enter for default Y): "
    
    add_gb = input(question)
    add_gb = add_gb.upper()
    
    # Perform data validation
    if data_entered(add_gb):
        while len(add_gb) < 1 or (add_gb[0] != "Y" and add_gb[0] != "N"):
            add_gb = input(" Your entry is invalid, please select Y for YES or N for NO : ")
            add_gb = add_gb.upper()
        
            if not data_entered(add_gb):
                add_gb = "Y"
            else:
                add_gb = add_gb.upper()
    else:
        add_gb = "Y"
                    
        
    if add_gb[0] == "Y":
        gain_bias = True
    else:
        gain_bias = False
        
    return gain_bias


# Ask the user if they want to display each image as it is processed
def display_processed_images(batch):
    
    display_images = False
    
    if batch:
        question = "\n Do you want to display each image after it has been processed? (Y/N): "
    else:
        question = "\n Do you want to display the image after it has been processed? (Y/N): "
    
    if export_display_available():
        display_images = input(question)
        display_images = display_images.upper()
        
        while len(display_images) < 1 or (display_images[0] != "Y" and display_images[0] != "N"):
            display_images = input(" Your entry is invalid, please select Y for YES or N for NO : ")
            display_images = display_images.upper()
        
        if display_images[0] == "Y":
            display_images = True
        else:
            display_images = False
    else:
        print("\n Your terminal session does not support the display of images.  If you want to see "
              "processed images please launch the program from a terminal that has X display support.")
        display_images = False
        
    return display_images


# Display main menu
def menu():

    print()
    print(" *********************************************************************")
    print(" *                                                                   *")
    print(" *                       Landsat Buoy Calibration                    *")
    print(" *                                                                   *")
    print(" *********************************************************************")
    print(" *                                                                   *")
    print(" *           Please select from one of the following options         *")
    print(" *                                                                   *")
    print(" *                                                                   *")
    print(" *                         ***  SINGLE JOB  ***                      *")
    print(" *                                                                   *")    
    print(" *    1. Single Scene - Single Channel using Buoys                   *")
    print(" *                                                                   *")
    print(" *    2. Single Scene - Single Channel using Supplied Surface Temp   *")
    print(" *                                                                   *")
    print(" *    3. Single Scene - Split Window using Supplied values           *")
    print(" *                                                                   *")
    print(" *                                                                   *")
    print(" *                         ***  BATCH JOBS  ***                      *")
    print(" *                                                                   *")
    print(" *    5. Batch Scenes - Single Channel using Buoys                   *")
#    print(" *                                                       *")
#    print(" *                                                       *")
#    print(" *              ***  TROUBLESHOOTING  ***                *")
#    print(" *                                                       *")
#    print(" *    D. Create database tables                          *")
    print(" *                                                                   *")
    print(" *    X. Exit                                                        *")
    print(" *                                                                   *")
    print(" *********************************************************************")
    print()
    menuInput = input("  Selection : ")

    menuInput = menuInput.upper()

    return menuInput


# This is the main entry to the menu
def main(project_root):
    
    sp.call('clear', shell = True)
    
    result = ""
    
    successful_entry = None
    
    while result != "X" and successful_entry != True:
        
        result = menu().upper()

        if (result == "1"):
            model_single_sc_buoy(project_root)
            
        elif (result == "2"):
            model_single_sc_toa(project_root)
            
        elif (result == "3"):
            model_single_sw_lst(project_root)

        elif (result == "5"):
            model_batch_sc_buoy(project_root)

        elif (result == "D"):
            print("\n Please wait while we test the database connection\n")

            testDb()

        elif (result == "X"):
            successful_entry = True
            cv2.destroyAllWindows()
            print("\n Thank you for using the Landsat Buoy Calibration program\n")
            
        else:
            successful_entry = False
            print("\n The value you entered is invalid, please try again\n")
            
        sp.call('clear', shell = True)
        cv2.destroyAllWindows()
                