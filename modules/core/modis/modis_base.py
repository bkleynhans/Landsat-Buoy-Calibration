#!/usr/bin/env python3
###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : GUI for the Landsat Buoy Calibration program
# Created By          : Benjamin Kleynhans
# Creation Date       : June 21, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : June 21, 2019
# Filename            : model.py
#
###

# Imports
import sys


class Landsat_Base():
    
    BANDS = [31, 32]
    
    def __init__(self, master):
        
        pass

        
# Process initialization arguments
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


# Program entry from different source
def main(args):

    Landsat_Base(parseArgs(args))


# Command line program entry
if __name__ == '__main__':

    args = main(sys.argv[1:])