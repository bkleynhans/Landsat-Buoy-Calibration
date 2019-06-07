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
import db_operations

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
        modtran_directory = '{0}/{1}_{2}'.format(settings.MODTRAN_DIR, scene_id, buoy_id)
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
def save_cv2_image(display_image, scene_id, image):
    
    if display_image == 'true':
        cv2.imshow('Landsat Preview', image)
        cv2.waitKey(0)
        
    cv2.imwrite('output/processed_images/{0}.tif'.format(scene_id), image)
        

def landsat8(scene_id, display_image, status_logger, atmo_source='merra', verbose=False, bands=[10, 11], db_operator=None):
    
    scene_id_index = None
    image_index = None
    date_index = None
    buoy_id_index = None
    path_to_output_folder = None
    
    path_to_working_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_directory_index = path_to_working_directory.rfind('/')
    
    if (path_to_working_directory[parent_directory_index + 1:] == 'Landsat-Buoy-Calibration'):
        
        path_to_output_folder = (path_to_working_directory + '/output/')
        
    elif (path_to_working_directory[parent_directory_index + 1:] == 'gui'):
        
        inner_index = path_to_working_directory[:parent_directory_index].rfind('/')
        path_to_output_folder = (path_to_working_directory[:inner_index] + '/output/')
        
    if settings.USE_MYSQL:
        # Add Scene ID to database
        scene_id_index = db_operator.insert_single_value('t_scene_ids', scene_id)
    
    image, file_downloaded = display.landsat_preview(scene_id, '')
    
    # Save image to file and/or display image
    #threading.Thread(target=save_cv2_image, args=(display_image, scene_id, image, )).start()
    
    if display_image == 'true':
        cv2.imshow('Landsat Preview', image)
        cv2.waitKey(0)
        
    #pdb.set_trace()
        
    cv2.imwrite((path_to_output_folder + 'processed_images/{0}.tif').format(scene_id), image)
    
    if settings.USE_MYSQL:
        # Write image to database
        image_index = db_operator.insert_image(scene_id)
    
    data = {}
    
    if file_downloaded:
        # satelite download
        # [:] thing is to shorthand to make a shallow copy
        
        overpass_date, directory, metadata, file_downloaded = sat.landsat.download(scene_id, bands[:])
        
        if settings.USE_MYSQL:
            # Write date to database
            date_index = db_operator.insert_single_value('t_dates', overpass_date)
        
        rsrs = {b:settings.RSR_L8[b] for b in bands}
        
        corners = sat.landsat.corners(metadata)
        buoys = buoy.datasets_in_corners(corners)
        
        if not buoys:
            raise buoy.BuoyDataException('no buoys in scene')
    
        for buoy_id in buoys:
            
            #pdb.set_trace()
            
            if settings.USE_MYSQL:
                # Write Buoy ID to database
                buoy_id_index = db_operator.insert_single_value('buoy_ids', buoy_id)
            
            log_text = ("  Processing buoy %s" % (buoy_id))
#            sys.stdout.write("\r  Processing buoy %s" % (buoy_id))
            sys.stdout.write("\r" + log_text)
            status_logger.write(log_text)
            sys.stdout.flush()
            
            #pdb.set_trace();
            
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
                        'file',
                        scene_id_index,
                        date_index,
                        buoy_id_index,
                        image_index
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
                        #'data',
                        str(e),
                        scene_id_index,
                        date_index,
                        buoy_id_index,
                        image_index
                    )#e.args[0] + ' for buoy ' + buoy_id)
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
                        'merra_layer1_temperature',
                        scene_id_index,
                        date_index,
                        buoy_id_index,
                        image_index
                    )
                continue            
            else:
                # MODTRAN
                modtran_directory = '{0}/{1}_{2}'.format(settings.MODTRAN_DIR, scene_id, buoy_id)
    
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
                        '',
                        scene_id_index,
                        date_index,
                        buoy_id_index,
                        image_index
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
                'image',
                scene_id_index,
                date_index,
                buoy_id_index,
                image_index
            )
    
    return data

def buildModel(args):
    
    from tools.process_logger import Process_Logger
    
    status_logger = Process_Logger(args.logfile)
        
    if settings.USE_MYSQL:
        db_operator = db_operations.Db_Operations()

    if not args.warnings:
        warnings.filterwarnings("ignore")
        
    if args.scene_id[0:3] in ('LC8', 'LC0'):   # Landsat 8
        bands = [int(b) for b in args.bands] if args.bands is not None else [10, 11]
        
        if settings.USE_MYSQL:
            ret = landsat8(args.scene_id, args.display_image, status_logger, db_operator, args.atmo, args.verbose, bands)
        else:
            ret = landsat8(args.scene_id, args.display_image, status_logger, args.atmo, args.verbose, bands)

    elif args.scene_id[0:3] == 'MOD':   # Modis
        bands = [int(b) for b in args.bands] if args.bands is not None else [31, 32]
        ret = modis(args.scene_id, args.atmo, args.verbose, bands)

    else:
        raise ValueError('Scene ID is not a valid format for (landsat8, modis)')
    
    if (args.caller == 'menu'):
        # Change the name of the output file to <scene_id>.txt
        args.save = args.save[:args.save.rfind('/') + 1] + args.scene_id + '.txt'
        
        report_headings = "Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason"
        #sys.stdout.write("\rScene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason\n")
        sys.stdout.write("\r" + report_headings + "\n")
        status_logger.write(report_headings)
        
        error_message = None
        
        for key in ret.keys():
            if(ret[key][9] == "failed"):
                error_message = get_error_message(ret[key][10])
            else:
                error_message = None
                            
            buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason, scene_id_index, date_index, buoy_id_index, image_index = ret[key]
                        
            if settings.USE_MYSQL:
                # Write row of data to database
                db_operator.insert_data_row(scene_id_index,
                                            date_index,
                                            buoy_id_index,
                                            [
                                                bulk_temp,
                                                skin_temp,
                                                buoy_lat,
                                                buoy_lon,
                                                mod_ltoa,
                                                img_ltoa,
                                                error
                                            ],
                                            image_index,
                                            status,
                                            error_message)
            
            
            # Convert tuple to text and remove first and last parentheses
            log_text = "".join(str(ret[key]))[1:-1]
            print(log_text)
            
            status_logger.write(log_text)
#            print(args.scene_id, date.strftime('%Y/%m/%d'), buoy_id, bulk_temp, skin_temp, buoy_lat, \
#                buoy_lon, *mod_ltoa.values(), *img_ltoa.values(), *error.values(), status, error_message)

        # Erases all the downloaded data if configured
        if settings.CLEAN_FOLDER_ON_COMPLETION:
                clear_downloads(status_logger)

        # Saves results to the output folder in the specified file
        if args.save:
            with open(args.save, 'w') as f:
                print('#Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason', file=f, sep=', ')
                for key in ret.keys():
                    if (ret[key][9] == "failed"):
                        error_message = get_error_message(ret[key][10])
                    else:
                        error_message = None
                    
                    buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason, scene_id_index, date_index, buoy_id_index, image_index = ret[key]
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
        
        try:
            if get_size(file_path) > settings.FOLDER_SIZE_FOR_REPORTING:
                if os.path.isfile(file_path):
                    log_text = (" Deleting %s..." % (file_or_folder))
#                    sys.stdout.write("\r Deleting %s..." % (file_or_folder))
                    sys.stdout.write("\r" + log_text)
                    status_logger.write(log_text)
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    log_text = (" Deleting %s..." % (file_or_folder))
#                    sys.stdout.write("\r Deleting %s..." % (file_or_folder))
                    sys.stdout.write("\r" + log_text)
                    status_logger.write(log_text)
                    shutil.rmtree(file_path)
            else:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    
    sys.stdout.write("\r  Cleanup completed!!!\n\n")
    

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
    parser.add_argument('-s', '--save', default='output/single/results.txt')
    parser.add_argument('-w', '--warnings', default=False, action='store_true')
    parser.add_argument('-d', '--bands', nargs='+')
# Allow ability to disable image display
    parser.add_argument('-n', '--display_image', default='true')
# Add caller information
    parser.add_argument('-c', '--caller', default='menu')
# Add log file location
    parser.add_argument('-l', '--logfile', default = 'logs/', help='Directory and name of log file')

    return parser.parse_args(args)


def main(args):

    return buildModel(parseArgs(args))

if __name__ == '__main__':

    args = main(sys.argv[1:])
