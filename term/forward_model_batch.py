###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Batch processing module for forward model builder
# Created By          : Nathan Dileas
# Creation Date       : 2018
# Authors             : Nathan Dileas
#                       Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 6, 2018
# Filename            : forward_model_batch.py
#
###

import os.path
import sys
import pdb
import forward_model
import test_paths
import graph_generator
import datetime
import numpy as np
import cv2
#from modules.db import db_operations
import settings


# Process the SceneIDs and print results to a file
def batch_f_model(args, scene_txt, scenes, output_txt, display_image, caller, status_logger, output_logger, db_operator=None):

    output_txt += scene_txt[scene_txt.rfind('/') + 1:scene_txt.rfind('.')] + '.out'
    
    fileExists = test_paths.main([output_txt, "-tfile"])

    if not (fileExists):
        f = open(output_txt, 'w+')
        f.close()

    with open(output_txt, 'w') as f:
        
        report_headers = ('Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2, status, reason')
        
        print(report_headers, file = f)
        
        print_data(caller, report_headers, output_logger)
        
        graph_data_band10 = np.zeros([1,3])
        graph_data_band11 = np.zeros([1,3])
        
        # For each SceneID, process and write to txt file
        for i, scene_id in enumerate(scenes):

            # Ensure there are no spaces or new line characters after any scene id
            if scene_id[-2:] == ' \n' or scene_id[-1] == ' ':
                scene_id = scene_id[:(scene_id.index(' '))]
            elif scene_id[-1] == '\n':
                scene_id = scene_id[:-1]

            log_text = "Starting analysis of scene {}".format(scene_id)
            
            print_data(caller, log_text, status_logger)
            
            ret = forward_model.main([scene_id, ('-c' + caller), ('-n' + display_image),('-t' + args.statuslog), ('-u' + args.outputlog), ('-d' + args.project_root)])

            log_text = "Analysis completed for scene {}".format(scene_id)
            
            print_data(caller, log_text, status_logger)

            for key in ret.keys():
                if(ret[key][9] == "failed"):
                    error_message = forward_model.get_error_message(ret[key][10])
                else:
                    error_message = None
                 
#                buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason, scene_id_index, date_index, buoy_id_index, image_index = ret[key]
                buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date, status, reason = ret[key]
                
#                if settings.USE_MYSQL:
#                    # Write row of data to database
#                    db_operator.insert_data_row(scene_id_index,
#                                            date_index,
#                                            buoy_id_index,
#                                            [bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, img_ltoa, error],
#                                            image_index,
#                                            status,
#                                            error_message)
                    
                for band in error:
                    difference = (mod_ltoa[band] - img_ltoa[band])
                    
                    if band == 10:
                        graph_data_band10 = np.vstack((graph_data_band10, [date, difference, error[band]]))
                    elif band == 11:
                        graph_data_band11 = np.vstack((graph_data_band11, [date, difference, error[band]]))
                
#                print(scene_id.replace('\n', ''), date.strftime('%Y/%m/%d'), buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, \
#                    *mod_ltoa.values(), *img_ltoa.values(), *error.values(), status, error_message, file=f, sep=', ')
                        # Convert tuple to text and remove first and last parentheses
                
                # Create a formatted tuple with the required data
                processed_data = (scene_id.replace('\n', ''), date.strftime('%Y/%m/%d'), buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, *mod_ltoa.values(), *img_ltoa.values(), *error.values(), status, error_message)
                # Convert tuple to text and remove first and last parentheses
                processed_data = "".join(str(processed_data))[1:-1]
                
                # Save the processed data to the output file
                print(processed_data, file = f)
                
                print_data(caller, processed_data, output_logger)
                
            f.flush()
    
    graph_data_band10 = np.delete(graph_data_band10, (0), axis=0)
    graph_data_band11 = np.delete(graph_data_band11, (0), axis=0)
    
    graph = graph_generator.Graph_Generator()
    
    graph_title = scene_txt[scene_txt.index('/') + 1:][:scene_txt[scene_txt.index('/') + 1:].index('.')]
    
    output_file_no_band = "output/batches/graphs/" + scene_txt[scene_txt.rfind('/') + 1:scene_txt.rfind('.')]
    
    graph.generate_graph(
            graph_title + " - Band 10",                                         # Graph title
            "Date",                                                             # X-axis label
            "Buoy - Landsat \n[w/m$^2$/sr/$\\mu$m]",                            # Y-axis label
            graph_data_band10,                                                  # Error array
            output_file_no_band + "_band10")                                    # Output file name (no extension)
    
    graph.generate_graph(
            graph_title + " - Band 11",                                         # Graph title
            "Date",                                                             # X-axis label
            "Buoy - Landsat \n[w/m$^2$/sr/$\\mu$m]",                            # Y-axis label
            graph_data_band11,                                                  # Error array
            output_file_no_band + "_band11")                                    # Output file name (no extension)


def print_data(caller, data, logger):
    
    if caller == 'forward_model_batch':
        
        print_to_screen("\n" + data + "\n")
        
    elif caller == 'tarca_gui_batch':
                
        logger.write(data)


def print_to_screen(data):

    sys.stdout.write("\n" + data)


# Read the supplied batch file
def buildModel(args):
    
    from process_logger import Process_Logger    
    
    status_logger = Process_Logger(args.statuslog)
    output_logger = Process_Logger(args.outputlog)
    
    if (args.caller == 'menu'):
        args.caller = 'forward_model_batch'
            
#    if settings.USE_MYSQL:
#        db_operator = db_operations.Db_Operations()

    scenes = open(args.scene_txt).readlines()
        
#    if settings.USE_MYSQL:
#        db_operator = db_operations.Db_Operations()
#        batch_f_model(args, args.scene_txt, scenes, args.save, args.display_image, db_operator, args.caller, status_logger, output_logger, args.project_root)
#    else:
    batch_f_model(args, args.scene_txt, scenes, args.save, args.display_image, args.caller, status_logger, output_logger, args.project_root)



# Parse the arguments received during program launch
def parseArgs(args):

    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('scene_txt')
    parser.add_argument('-a', '--atmo', default='merra', choices=['merra', 'narr'], help='Choose atmospheric data source, choices:[narr, merra].')
    parser.add_argument('-s', '--save', default='output/batches/data/')
    # Allow ability to disable image display
    parser.add_argument('-n', '--display_image', default='true')
    parser.add_argument('-d', '--project_root', help='Working directory of the program')
# Add caller information
    parser.add_argument('-c', '--caller', help='The name or reference of the file calling this function')
# Add log file locations
    parser.add_argument('-t', '--statuslog', default = 'logs/status/default.status', help='Status file directory')
    parser.add_argument('-u', '--outputlog', default = 'logs/output/default.output', help='Output file directory')

    return parser.parse_args(args)


# Only execute code when it is requested, not at import statement
def main(args):

    buildModel(parseArgs(args))


# Only execute the code if the program is being run by itself
if __name__ == '__main__':

    args = main(sys.argv[1:])
