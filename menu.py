###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Menu program for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 11, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 6, 2018
# Filename            : menu.py
#
###

# Imports

import inspect
import sys
import os
import time
import cv2
import subprocess as sp
from os.path import join, abspath
import datetime
import pdb

ERASE_LINE = '\x1b[2K'

PROGRAM_ROOT = 'Landsat-Buoy-Calibration/'
GUI_ROOT = join(PROGRAM_ROOT, 'gui/')

# Calculate fully qualified path to location of program execution
def get_module_path():
    
    filename = inspect.getfile(inspect.currentframe())
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    return path, filename


# Set environment variables to locate current execution path
def set_path_variables():
    
    path, filename = get_module_path()

    sys.path.append(path)
    sys.path.append(path + "/buoycalib")
    sys.path.append(path + "/downloaded_data")
    sys.path.append(path + "/tools")
    sys.path.append(path + "/output")
    sys.path.append(path + "/processed_images")


# Create any folders that are required and not currently available
def check_required_directories():
    
    import test_paths
        
    required_directories = {
            'input',
            'input/batches',
            'output',
            'output/processed_images',
            'output/single',
            'output/batches',
            'output/batches/data',            
            'output/batches/graphs',
            'logs',
            'logs/status',
            'logs/status/single',
            'logs/status/batch',
            'logs/output',
            'logs/output/single',
            'logs/output/batch'}
    
    for directory in required_directories:
        if not test_paths.main([directory, "-tdirectory"]):
            test_paths.createDirectory(directory)
    

# Request name of text file containing batch process scene IDs
def f_model_batch_merra():
    
    import test_paths
    
    display_images = display_processed_images(True)
    
    batchFile = 'input/batches/'
    batchFile += input("\n Please enter the name of the batch file or 'X' to exit : ")
    
    if (batchFile[(batchFile.rfind('/') + 1):].upper()) != 'X':
        valid_data = test_paths.main([batchFile, "-tfile"])
        
        if not valid_data:
            batchFile = input("\n The batch file you entered is invalid, please try again ('X' - exit): ")
            
            if batchFile.upper() != 'X':
                valid_data = test_paths.main([batchFile, "-tfile"])
            
    
        if batchFile.upper() != 'X':
            # Launch batch process job
            forward_model_batch.main([batchFile, display_images])


# Request Scene ID for single scene to calculate
def f_model():
    
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
            
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
            
            # Create a logger instance
            logfile = ("-lsingle/" + str(sceneId) + "_" + str(current_datetime) + ".txt")
            
            # Launch single scene ID process job
            forward_model.main([sceneId, display_images, logfile])
            

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


# Test if the database server is avialable
def testDb():

    import db_connection

    db_test_con = db_connection.Db_Connection()

    db_status = db_test_con.db_available()
    
    import db_construction
    
    constructor = db_construction.Db_Construction()
    
    constructor.prepare_database()
    
    print()
    
    return db_status
    
    
## Timer to display activity during tests
#def path_test_timer():
#    
#    sys.stdout.write(" ")
#    
#    for i in range(0, 5, 1):
#        sys.stdout.write(".")
#        sys.stdout.flush()
#        
#        time.sleep(0.5)
#        
#    time.sleep(0.5)
        

# Tests whether the online data sources are available
def source_test(address, missing_sources):
    
    import test_paths    
            
    if not test_paths.main([address, '-tserver']):
        #sys.stdout.write("\r " + address)
        
        #path_test_timer()
        
        sys.stdout.write(" --> NOT AVAILABLE!!!")
        sys.stdout.flush()
        
        missing_sources.append(address)
    else:
        #sys.stdout.write(ERASE_LINE)
        #sys.stdout.write('\r ' + address)
        
        #path_test_timer()
        
        sys.stdout.write(" >>> available.")
        sys.stdout.flush()
        
        missing_sources = None
        
    time.sleep(0.5)
        
    return missing_sources

# Test if all data sources specified in buoycalib/settings.py are present
def check_sources():
    
    import settings
    
    sources_available = True
    
    sources = []
    
    sources.append(settings.MERRA_SERVER)
    sources.append(settings.NARR_SERVER)
    sources.append(settings.NOAA_SERVER)
    sources.append(settings.LANDSAT_S3_SERVER)
    sources.append(settings.LANDSAT_EE_SERVER)
    
    if settings.USE_MYSQL:
        sources.append(settings.SQL_SERVER)
    
    missing_sources = []
    
    for source in sources:
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write('\r Testing >>> ' + source)
        source = source_test(source, missing_sources)
            
    if (len(missing_sources)):
        sources_available = False
        
    return sources_available, missing_sources

# Test if the terminal session allows export of display
def export_display_available():
    
    returnValue = False
    
    if "DISPLAY" in os.environ:
        returnValue = True
    
    return returnValue

# Ask the user if they want to display each image as it is processed
def display_processed_images(batch):
    
    display_images = None
    
    if batch:
        question = "\n Do you want to display each image after it has been processed? (Y/N): "
    else:
        question = "\n Do you want to display the image after it has been processed? (Y/N): "
    
    if export_display_available():
        display_images = input(question)
        display_images = display_images.upper()
        
        while display_images[0] != "Y" and display_images[0] != "N":
            display_images = input(" Your entry is invalid, please select Y for YES or N for NO : ")
            display_images = display_images.upper()
        
        if display_images[0] == "Y":
            display_images = '-ntrue'
        else:
            display_images = '-nfalse'
    else:
        print("\n Your terminal session does not support the display of images.  If you want to see "
              "processed images please launch the program from a terminal that has X display support.")
        display_images = '-nfalse'
        
    return display_images


# Display main menu
def menu():

    print()
    print(" ***************************************************")
    print(" *                                                 *")
    print(" *           Landsat Buoy Calibration              *")
    print(" *                                                 *")
    print(" ***************************************************")
    print(" *                                                 *")
    print(" * Please select from one of the following options *")
    print(" *                                                 *")
    print(" *                                                 *")
    print(" *              ***  SINGLE JOB  ***               *")
    print(" *                                                 *")
    print(" * 1. Forward model calculation (MERRA2 / MODIS)   *")
    print(" *                                                 *")
    print(" *                                                 *")
    print(" *              ***  BATCH JOBS  ***               *")
    print(" *                                                 *")
    print(" * 5. Forward model calculation (MERRA2)           *")
    print(" *                                                 *")
    print(" *                                                 *")
    print(" *           ***  TROUBLESHOOTING  ***             *")
    print(" *                                                 *")
    print(" * D. Create database tables                       *")
    print(" *                                                 *")
    print(" * X. Exit                                         *")
    print(" *                                                 *")
    print(" ***************************************************")
    print()
    menuInput = input("  Selection : ")

    menuInput = menuInput.upper()

    return menuInput


# Application launch
if __name__ == '__main__':
    
    sp.call('clear', shell = True)

    set_path_variables()

    import forward_model
    import forward_model_batch

    menuInput = ""
    result = ""
    
    print()
    print(" Please be patient while we test if the required data sources are available")
    print()
    
    data_sources_available, missing_sources = check_sources()
    
    if (data_sources_available):
        
        check_required_directories()
        
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write("\r     --> All data sources are accounted for <--")
        print()
        
        successful_entry = None
        
        while result != "X" and successful_entry != True:
            
            result = menu().upper()
    
            if (result == "1"):
                f_model()
    
            elif (result == "5"):
                f_model_batch_merra()
    
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
                
    else:        
        print("\n\n!!!")
        print("!")
        print("! The program has quit because the following data source/s are currently " \
                "not available !")
        print("!")
        print("!!!")
        print("!")
                
        for source in missing_sources:
            print("!    >>  {}".format(source))
        
        print("!")
        print("!!!\n")
    
