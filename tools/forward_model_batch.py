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
# Last Modified Date  : July 6, 2018
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

# Process the SceneIDs and print results to a file
def batch_f_model(scene_txt, scenes, output_txt, display_image):

    if (output_txt == 'results.txt'):
        output_txt = 'output/' + scene_txt[7:] + '.out'

    fileExists = test_paths.testFile(output_txt)

    if not (fileExists):
        f = open(output_txt, 'w+')
        f.close()

    with open(output_txt, 'w') as f:
        
        graph_data_band10 = np.zeros([1,3])
        graph_data_band11 = np.zeros([1,3])
                
        f.write('Scene_ID, Date, Buoy_ID, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod1, mod2, img1, img2, error1, error2\n')
        f.flush()
        
        # For each SceneID, process and write to txt file
        for i, scene_id in enumerate(scenes):

            # Ensure there are no spaces or new line characters after any scene id
            if scene_id[-2:] == ' \n' or scene_id[-1] == ' ':
                scene_id = scene_id[:(scene_id.index(' '))]
            elif scene_id[-1] == '\n':
                scene_id = scene_id[:-1]
            
            print("\n Starting analysis of scene {}".format(scene_id))

            ret = forward_model.main([scene_id, '-c forward_model_batch', '-n' + display_image])

            sys.stdout.write("\r Analysis completed for scene {}\n\n".format(scene_id))
            
            print(scene_id.replace('\n', ','),ret)

            for key in ret.keys():
                if(ret[key][1] == "failed"):
                    if (ret[key][2] == "buoy"):
                        error_message = "No buoys in the scene"
                    elif (ret[key][2] == "data"):
                        error_message = "No data available for buoy"
                    elif (ret[key][2]== "image"):
                        error_message = "No Landsat Image Available For Download"
                    elif (ret[key][2] == "merra_layer1_temperature"):
                        error_message = "Zero reading at Merra layer1 temperature for buoy"
                    else:
                        error_message = ret[key][2]
            
                if (ret[key][1] != "failed"):
                    buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, mod_ltoa, error, img_ltoa, date = ret[key]
                    
                    for band in error:
                        difference = (mod_ltoa[band] - img_ltoa[band])
                        
                        if band == 10:
                            graph_data_band10 = np.vstack((graph_data_band10, [date, difference, error[band]]))
                        elif band == 11:
                            graph_data_band11 = np.vstack((graph_data_band11, [date, difference, error[band]]))
                        
                    print(scene_id.replace('\n', ''), date.strftime('%Y/%m/%d'), buoy_id, bulk_temp, skin_temp, buoy_lat, buoy_lon, \
                        *mod_ltoa.values(), *img_ltoa.values(), *error.values(), file=f, sep=', ')
                else:
                    if ((ret[key][2] == "data") or
                        (ret[key][2] == "merra_layer1_temperature")):
                        print(scene_id.replace('\n', ''), error_message, ret[key][0], file=f, sep=', ')
                    else:
                        print(scene_id.replace('\n', ''), error_message, file=f, sep=', ')

            f.flush()
    
    graph_data_band10 = np.delete(graph_data_band10, (0), axis=0)
    graph_data_band11 = np.delete(graph_data_band11, (0), axis=0)
    
    graph = graph_generator.Graph_Generator()
    
    graph_title = scene_txt[scene_txt.index('/') + 1:][:scene_txt[scene_txt.index('/') + 1:].index('.')]
    
    graph.generate_graph(
            graph_title + " - Band 10",                                         # Graph title
            "Date",                                                             # X-axis label
            "Buoy - Landsat \n[w/m$^2$/sr/$\\mu$m]",                              # Y-axis label
            graph_data_band10,                                                  # Error array
            ("output/" + scene_txt[7:] + "_band10"))                            # Output file name (no extension)
    
    graph.generate_graph(
            graph_title + " - Band 11",                                         # Graph title
            "Date",                                                             # X-axis label
            "Buoy - Landsat \n[w/m$^2$/sr/$\\mu$m]",                              # Y-axis label
            graph_data_band11,                                                  # Error array
            ("output/" + scene_txt[7:] + "_band11"))                            # Output file name (no extension)


# Read the supplied batch file
def buildModel(args):

    scenes = open(args.scene_txt).readlines()
    
    batch_f_model(args.scene_txt, scenes, args.save, args.display_image)


# Parse the arguments received during program launch
def parseArgs(args):

    import argparse

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('scene_txt')
    parser.add_argument('-a', '--atmo', default='merra', choices=['merra', 'narr'], help='Choose atmospheric data source, choices:[narr, merra].')
    parser.add_argument('-s', '--save', default='results.txt')
    # Allow ability to disable image display
    parser.add_argument('-n', '--display_image', default='true')

    return parser.parse_args(args)


# Only execute code when it is requested, not at import statement
def main(args):

    buildModel(parseArgs(args))


# Only execute the code if the program is being run by itself
if __name__ == '__main__':

    args = main(sys.argv[1:])
