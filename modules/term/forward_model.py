import warnings
import inspect
import sys
import os
import shutil

# Python Debugger - Ben
import pdb
import threading
###

from buoycalib import (sat, buoy, atmo, radiance, modtran, settings, download, display, error_bar)

import numpy
import cv2
#from modules.db import db_operations

from datetime import datetime

def modis(scene_id, atmo_source='merra', verbose=False, bands=[31, 32]):
    image = display.modis_preview(scene_id)
    
    cv2.imshow('MODIS Preview', image)
    cv2.waitKey(50)
    cv2.imwrite('preview_{0}.tif'.format(scene_id), image)

    overpass_date, directory, metadata, [granule_filepath, geo_ref_filepath] = sat.modis.download(scene_id)
    rsrs = {b:settings.RSR_MODIS[b] for b in bands}

    corners = sat.modis.corners(metadata)
    buoys = buoy.datasets_in_corners(corners)

    if not buoys:
        raise buoy.BuoyDataException('no buoys in scene')

    data = {}

    for buoy_id in buoys:        
        try:
            buoy_file = buoy.download(buoy_id, overpass_date)
            buoy_lat, buoy_lon, buoy_depth, bulk_temp, skin_temp, lower_atmo = buoy.info(buoy_id, buoy_file, overpass_date)
        except download.RemoteFileException:
            warnings.warn('Buoy {0} does not have data for this date.'.format(buoy_id), RuntimeWarning)
            continue
        except buoy.BuoyDataException as e:
            warnings.warn(str(e), RuntimeWarning)
            continue

        # Atmosphere
        if atmo_source == 'merra':
            atmosphere = atmo.merra.process(overpass_date, buoy_lat, buoy_lon, verbose)
        elif atmo_source == 'narr':
            atmosphere = atmo.narr.process(overpass_date, buoy_lat, buoy_lon, verbose)
        else:
            raise ValueError('atmo_source is not one of (narr, merra)')

        # MODTRAN
        #print('Running MODTRAN:')
        modtran_directory = '{0}/{1}_{2}'.format(settings.MODTRAN_BASH_DIR, scene_id, buoy_id)
        wavelengths, upwell_rad, gnd_reflect, transmission = modtran.process(atmosphere, buoy_lat, buoy_lon, overpass_date, modtran_directory, skin_temp)

        # LTOA calcs
        #print('Ltoa Spectral Calculations:')
        mod_ltoa_spectral = radiance.calc_ltoa_spectral(wavelengths, upwell_rad, gnd_reflect, transmission, skin_temp)

        img_ltoa, units = sat.modis.calc_ltoa_direct(granule_filepath, geo_ref_filepath, buoy_lat, buoy_lon, bands)

        mod_ltoa = {}
        for b in bands:
            RSR_wavelengths, RSR = sat.modis.load_rsr(rsrs[b])
            mod_ltoa[b] = radiance.calc_ltoa(wavelengths, mod_ltoa_spectral, RSR_wavelengths, RSR)

        error = error_bar.error_bar(scene_id, buoy_id, skin_temp, 0.35, overpass_date, buoy_lat, buoy_lon, rsrs, bands)
        print((buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, overpass_date))
        data[buoy_id] = (buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, overpass_date)
    
    return data


# Display the image to the screen for 60 seconds, or until the window is closed.
def open_image(image):
        
    cv2.imshow('Landsat Preview', image)
    cv2.waitKey(0)
        

def landsat8(scene_id, display_image, caller, status_logger, project_root, atmo_source='merra', verbose=False, bands=[10, 11], db_operator=None):
    
    output_directory = os.path.join(project_root, 'output')
        
    image, file_downloaded = display.landsat_preview(scene_id, '')
    
    # Save image to file and/or display image
    if display_image == 'true':
        display_image_thread = threading.Thread(target=open_image, args=(image, ))
        display_image_thread.start()
        
    image_file = '{0}.tif'.format(scene_id)
    image_directory = os.path.join(output_directory, 'processed_images')
    absolute_image_directory = os.path.join(project_root, image_directory)
    absolute_image_path = os.path.join(absolute_image_directory, image_file)
    cv2.imwrite(absolute_image_path, image)
        
    data = {}
    
    if file_downloaded:
        # satelite download
        # [:] thing is to shorthand to make a shallow copy
        
        overpass_date, directory, metadata, file_downloaded = sat.landsat.download(scene_id, bands[:])
        
        rsrs = {b:settings.RSR_L8[b] for b in bands}
        
        corners = sat.landsat.corners(metadata)
        buoys = buoy.datasets_in_corners(corners)
        
        if not buoys:
            raise buoy.BuoyDataException('no buoys in scene')
    
    
        for buoy_id in buoys:
            
            log_text = ("  Processing buoy %s" % (buoy_id))
            
            if ((caller == 'menu') or (caller == 'forward_model_batch')):
                sys.stdout.write("\r" + log_text)
            elif ((caller == 'tarca_gui') or (caller == 'tarca_gui_batch')):
                status_logger.write(log_text)
            
            sys.stdout.flush()
            
            try:
                buoy_file = buoy.download(buoy_id, overpass_date) ##To this point is fine - to use method in new class when completed - create new buoy object as this point
                buoy_lat, buoy_lon, buoy_depth, bulk_temp, skin_temp, lower_atmo = buoy.info(buoy_id, buoy_file, overpass_date)
                
            except download.RemoteFileException:
                warnings.warn('Buoy {0} does not have data for this date.'.format(buoy_id), RuntimeWarning)
                data[buoy_id] = (
                        buoy_id,
                        0,
                        0,
                        0,
                        0,
                        {10:0,11:0},
                        {10:0,11:0},
                        {10:0,11:0},
                        overpass_date,
                        'failed',
                        'file'
                    )
                continue
            except buoy.BuoyDataException as e:
                warnings.warn(str(e), RuntimeWarning)
                data[buoy_id] = (
                        buoy_id,
                        0,
                        0,
                        0,
                        0,
                        {10:0,11:0},
                        {10:0,11:0},
                        {10:0,11:0},
                        overpass_date,
                        'failed',
                        str(e)
                    )
                continue
### Continue from here
                #********** Break for separate calculation here **********
            # Atmosphere
            if atmo_source == 'merra':
                atmosphere = atmo.merra.process(overpass_date, buoy_lat, buoy_lon, verbose)
            elif atmo_source == 'narr':
                atmosphere = atmo.narr.process(overpass_date, buoy_lat, buoy_lon, verbose)
            else:
                raise ValueError('atmo_source is not one of (narr, merra)')
    
            if not atmosphere:
                data[buoy_id] = (
                        buoy_id, 
                        bulk_temp, 
                        skin_temp, 
                        buoy_lat, 
                        buoy_lon,
                        { 10:0, 11:0 },
                        { 10:0, 11:0 },
                        { 10:0, 11:0 },
                        overpass_date,
                        'failed',
                        'merra_layer1_temperature'
                    )
                continue            
            else:
                # MODTRAN
                modtran_directory = '{0}/{1}_{2}'.format(settings.MODTRAN_BASH_DIR, scene_id, buoy_id)
                wavelengths, upwell_rad, gnd_reflect, transmission = modtran.process(atmosphere, buoy_lat, buoy_lon, overpass_date, modtran_directory, skin_temp)
                
                # LTOA calcs
                mod_ltoa_spectral = radiance.calc_ltoa_spectral(wavelengths, upwell_rad, gnd_reflect, transmission, skin_temp)
        
                img_ltoa = {}
                mod_ltoa = {}
                
                try:
                    for b in bands:
                        RSR_wavelengths, RSR = numpy.loadtxt(rsrs[b], unpack=True)
                        img_ltoa[b] = sat.landsat.calc_ltoa(directory, metadata, buoy_lat, buoy_lon, b)
                        mod_ltoa[b] = radiance.calc_ltoa(wavelengths, mod_ltoa_spectral, RSR_wavelengths, RSR)
                except RuntimeError as e:
                    warnings.warn(str(e), RuntimeWarning)
                    continue
        
                error = error_bar.error_bar(scene_id, buoy_id, skin_temp, 0.305, overpass_date, buoy_lat, buoy_lon, rsrs, bands)
        
                data[buoy_id] = (
                        buoy_id,
                        bulk_temp,
                        skin_temp,
                        buoy_lat,
                        buoy_lon,
                        mod_ltoa,
                        error,
                        img_ltoa,
                        overpass_date,
                        'success',
                        ''
                    )
            
    else:
        overpass_date = datetime(1, 1, 1, 0, 0) 
        data[0] = (
                0,
                0,
                0,
                0,
                0,
                {10:0,11:0},
                {10:0,11:0},
                {10:0,11:0},
                overpass_date,
                'failed',
                'image'
            )
    
    return data


def buildModel(args):
    
    from process_logger import Process_Logger    
    status_logger = Process_Logger(args.statuslog)
    output_logger = Process_Logger(args.outputlog)
        
    if not args.warnings:
        warnings.filterwarnings("ignore")
        
    if args.scene_id[0:3] in ('LC8', 'LC0'):   # Landsat 8
        bands = [int(b) for b in args.bands] if args.bands is not None else [10, 11]
        
        ret = landsat8(args.scene_id, args.display_image, args.caller, status_logger, args.project_root, args.atmo, args.verbose, bands)

    elif args.scene_id[0:3] == 'MOD':   # Modis
        bands = [int(b) for b in args.bands] if args.bands is not None else [31, 32]
        ret = modis(args.scene_id, args.atmo, args.verbose, bands)

    else:
        raise ValueError('Scene ID is not a valid format for (landsat8, modis)')
    
    if ((args.caller == 'menu') or (args.caller == 'tarca_gui')):
        # Change the name of the output file to <scene_id>.txt
        args.savefile = args.savefile[:args.savefile.rfind('/') + 1] + args.scene_id + '.txt'
        report_headings = "Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason"
        
        if (args.caller == 'tarca_gui'):
            output_logger.write(report_headings)
        elif ((args.caller == 'menu') or (args.caller == 'forward_model_batch')):
            sys.stdout.write("\r" + report_headings + "\n")
        
        error_message = None
        
        for key in ret.keys():
            if(ret[key][9] == "failed"):
                error_message = get_error_message(ret[key][10])
            else:
                error_message = None
                            
                buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason = ret[key]
            
            
            # Convert tuple to text and remove first and last parentheses
            log_text = "".join(str(ret[key]))[1:-1]
            
            if (args.caller == 'tarca_gui'):
                output_logger.write(log_text)
            elif (args.caller == 'menu'):
                sys.stdout.write("\r" + log_text + "\n")

        # Erases all the downloaded data if configured
        if settings.CLEAN_FOLDER_ON_COMPLETION:
                clear_downloads(status_logger)
        
        # Saves results to the output folder in the specified file
        if args.savefile:
            with open(args.savefile, 'w') as f:
                print('#Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason', file=f, sep=', ')
                for key in ret.keys():
                    if (ret[key][9] == "failed"):
                        error_message = get_error_message(ret[key][10])
                    else:
                        error_message = None
                    
                    buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason = ret[key]
                    print(args.scene_id, date.strftime('%Y/%m/%d'), buoy_id, bulk_temp, skin_temp, buoy_lat, \
                        buoy_lon, *mod_ltoa.values(), *img_ltoa.values(), *error.values(), status, error_message, file=f, sep=', ')
            
        else:
            return ret
    
    else:
        if settings.CLEAN_FOLDER_ON_COMPLETION:
            clear_downloads(status_logger)
               
        return ret

def clear_downloads(status_logger):
    
    print("\n\n  Cleaning up the downloaded items folder...")
    
    directory = settings.DATA_BASE
    
    for file_or_folder in os.listdir(directory):
        file_path = os.path.join(directory, file_or_folder)
        
        log_text = (" Deleting %s..." % (file_or_folder))
        
        try:
            if get_size(file_path) > settings.FOLDER_SIZE_FOR_REPORTING:
                if os.path.isfile(file_path):                    
                    if (args.caller != 'tarca_gui'):
                        sys.stdout.write("\r" + log_text)
                    else:
                        status_logger.write(log_text)
                    
                    
                    os.unlink(file_path)
                    
                elif os.path.isdir(file_path):                    
                    if (args.caller != 'tarca_gui'):
                        sys.stdout.write("\r" + log_text)
                    else:
                        status_logger.write(log_text)
                    
                    
                    shutil.rmtree(file_path)
            else:
                if os.path.isfile(file_path):
                    # unlink is ux version of delete for files
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    
    log_text = "Cleanup completed!!!"
    
    if (args.caller != 'tarca_gui'):
        sys.stdout.write("\r" + log_text + "\n\n")

    status_logger.write(log_text)

# Convert error codes to error messages for user feedback    
def get_error_message(key):
    
    error_message = None
    
    if (key == "buoy"):
        error_message = "No buoys in the scene"
    elif (key == "data"):
        error_message = "No data in data file for this buoy on this date"
    elif (key == "file"):
        error_message = "No data file to download for this buoy for this period"
    elif (key== "image"):
        error_message = "No Landsat Image Available For Download"
    elif (key == "merra_layer1_temperature"):
        error_message = "Zero reading at Merra layer1 temperature for buoy"
    else:
        error_message = key
    
    return error_message

# Get the size of a file
def get_size(start_path):
    
    total_size = 0
    
    for dirpath, dirnames, filenames in os.walk(start_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    
    # Divide by 1 000 000 to get a MegaByte size equivalent 
    total_size = total_size / 1000000
    
    return total_size

def parseArgs(args):

    import argparse

    parser = argparse.ArgumentParser(description='Compute and compare the radiance values of \
     a landsat image to the propogated radiance of a NOAA buoy, using atmospheric data and MODTRAN. ')

    parser.add_argument('scene_id', help='LANDSAT or MODIS scene ID. Examples: LC08_L1TP_017030_20170703_20170715_01_T1, MOD021KM.A2011154.1650.006.2014224075807.hdf')
    parser.add_argument('-a', '--atmo', default='merra', choices=['merra', 'narr'], help='Choose atmospheric data source, choices:[narr, merra].')
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-s', '--savefile', default='output/single/results.txt')
    parser.add_argument('-w', '--warnings', default=False, action='store_true')
    parser.add_argument('-b', '--bands', nargs='+')
    parser.add_argument('-d', '--project_root', help='Working directory of the program')
# Allow ability to disable image display
    parser.add_argument('-n', '--display_image', default='true')
# Add caller information
    parser.add_argument('-c', '--caller', help='The name or reference of the file calling this function')
# Add log file locations
    parser.add_argument('-t', '--statuslog', default = 'logs/status/default.status', help='Status file directory')
    parser.add_argument('-u', '--outputlog', default = 'logs/output/default.output', help='Output file directory')

    return parser.parse_args(args)


def main(args):

    return buildModel(parseArgs(args))

if __name__ == '__main__':

    args = main(sys.argv[1:])
