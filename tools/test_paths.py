###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Tests whether a web (http/ftp) or local (file) target
#                       exists
# Created By          : Benjamin Kleynhans
# Creation Date       : June 11, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : July 24, 2018
# Filename            : test_paths.py
#
###

import warnings
import sys
import pdb

import requests

ERASE_LINE = '\x1b[2K'

# Tests a Directory
def testDirectory(tdirectory):

    import os.path

    returnValue = False

    # os.path.isfile is an internal function that returns True if a file
    # or path exists and returns False if it does not
    if (os.path.isdir(tdirectory)):
        returnValue = True

    return returnValue


# Create a folder relative to current execution path
def createDirectory(cdirectory):
        
    import os.path

    if not os.path.exists(cdirectory):
        os.makedirs(cdirectory)      
        

# Tests a file
def testFile(tfile):

    import os.path

    returnValue = False

    # os.path.isfile is an internal function that returns True if a file
    # or path exists and returns False if it does not
    if (os.path.isfile(tfile)):
        returnValue = True

    return returnValue

# Test a server
def testServer(tserver):
    
    returnValue = False
    
    # extract the first three characters from the url to determine if it is a
    # FTP or HTTP url.  Test the url according to the type of url.
    if (tserver[:3] == 'ftp'):
        from ftplib import FTP
                
        ftp = FTP(tserver[6:])
        resp = ftp.login()
        
        # for FTP a response code of 230 is successful
        if (resp.startswith('230')):
            returnValue = True
            
    else:
        pdb.set_trace()
        resp = requests.head(tserver)
    
        # for HTTP a response code of 200 is successful
        if resp.status_code == 200:
            returnValue = True

    return returnValue


# Tests a url
def testUrl(turl):
    
    returnValue = False
    
    ftp_server = turl[6:turl[6:].index('/') + 6]
    
    # extract the first three characters from the url to determine if it is a
    # FTP or HTTP url.  Test the url according to the type of url.
    if (turl[:3] == 'ftp'):
        from ftplib import FTP
                
        ftp = FTP(ftp_server)
        resp = ftp.login()
        
        # for FTP a response code of 230 is successful
        if (resp.startswith('230')):
            file_exists_list = ftp.nlst(turl[turl[6:].index('/') + 7:])
            
            if len(file_exists_list) != 0:
                returnValue = True
            
    else:
        resp = requests.head(turl)
    
        # for HTTP a response code of 200 is successful
        if resp.status_code == 200:
            returnValue = True

    return returnValue


# Launch the appropriate testing function for either file or url
def testPaths(args):

    returnValue = None

    if (args.type == 'server'):
        returnValue = testServer(args.path)
    elif (args.type == 'url'):
        returnValue = testServer(args.path)
    elif (args.type == 'file'):
        returnValue = testFile(args.path)
    elif (args.type == 'directory'):
        returnValue = testDirectory(args.path)

    return returnValue, args.path


# Parse the arguments supplied at program launch to determine whether a url
    # or a file path is being tested
def parseArgs(args):

    import argparse

    parser = argparse.ArgumentParser(description='Determine if the required file is available for download')

    parser.add_argument('path', help='Web link to file.  Example: https://landsat-pds.s3.amazonaws.com/c1/L8/016/030/LC08_L1TP_016030_20180629_20180630_01_RT/LC08_L1TP_016030_20180629_20180630_01_RT_B10.TIF')
    parser.add_argument('-t', '--type', default='server', choices=['server', 'url', 'file', 'directory'], help='Choose the type of path we are checking, choices:[server, url, file, directory]')

    return parser.parse_args(args)


# Used when calling program from another module/function
def main(args):

    returnValue, path = testPaths(parseArgs(args))

    if __name__ == '__main__':
        print(returnValue)

    return returnValue
    

# Application launch
if __name__ == '__main__':

    args = main(sys.argv[1:])
