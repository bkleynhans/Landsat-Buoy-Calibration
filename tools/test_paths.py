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
def testDirectory(args):

    import os.path

    returnValue = False

    # os.path.isfile is an internal function that returns True if a file
    # or path exists and returns False if it does not
    if (os.path.isdir(args.path)):
        returnValue = True

    return returnValue


# Create a folder relative to current execution path
def createDirectory(cdirectory):
        
    import os.path

    if not os.path.exists(cdirectory):
        os.makedirs(cdirectory)      
        

# Tests a file
def testFile(args):

    import os.path

    returnValue = False

    # os.path.isfile is an internal function that returns True if a file
    # or path exists and returns False if it does not
    if (os.path.isfile(args.path)):
        returnValue = True

    return returnValue

# Test a server
def testServer(args):
    
    returnValue = False
    
    # extract the first three characters from the url to determine if it is a
    # FTP or HTTP url.  Test the url according to the type of url.
    if (args.path[:3].upper() == 'FTP'):        
        from ftplib import FTP
                
        ftp = FTP(args.path[6:])
        resp = ftp.login()
        
        # for FTP a response code of 230 is successful
        if (resp.startswith('230')):
            returnValue = True
            
    else:
        resp = requests.head(args.path)
    
        # for HTTP a response code of 200 is successful
        if resp.status_code == 200:
            returnValue = True

    return returnValue


# Tests a url
def testUrl(args):
    
    returnValue = False
    ftp_server = False
    translated_path = None
    server_address = None
    
    if isinstance(args.path, str):
        translated_path = args.path
    else:
        translated_path = args.path[0]
    
    # Extract server address if FTP for use with ftplib
    if (translated_path[:3].upper() == 'FTP'):
        server_address = translated_path[6:translated_path[6:].index('/') + 6]
        ftp_server = True        
    
    # extract the first three characters from the url to determine if it is a
    # FTP or HTTP url.  Test the url according to the type of url.
    if ftp_server:
        from ftplib import FTP
    
        with FTP(server_address) as ftp:
            resp = ftp.login(args.username, args.password)
            
            # for FTP a response code of 230 is successful
            if (resp.startswith('230')):
                file_exists_list = ftp.nlst(translated_path[translated_path[6:].index('/') + 7:])
                
                if len(file_exists_list) != 0:
                    returnValue = True
            
    else:
        resp = requests.head(translated_path)
        
        # for HTTP a response code of 200 is successful
        if resp.status_code == 200:
            returnValue = True

    return returnValue


# Launch the appropriate testing function for either file or url
def testPaths(args):

    returnValue = None

    if (args.type == 'server'):
        returnValue = testServer(args)
    elif (args.type == 'url'):
        returnValue = testUrl(args)
    elif (args.type == 'file'):
        returnValue = testFile(args)
    elif (args.type == 'directory'):
        returnValue = testDirectory(args)

    return returnValue, args.path


# Parse the arguments supplied at program launch to determine whether a url
    # or a file path is being tested
def parseArgs(args):

    import argparse

    parser = argparse.ArgumentParser(description='Determine if the required file is available for download')

    parser.add_argument('path', help='Web link to file.  Example: https://landsat-pds.s3.amazonaws.com/c1/L8/016/030/LC08_L1TP_016030_20180629_20180630_01_RT/LC08_L1TP_016030_20180629_20180630_01_RT_B10.TIF')
    parser.add_argument('-t', '--type', default='server', choices=['server', 'url', 'file', 'directory'], help='Choose the type of path we are checking, choices:[server, url, file, directory]')
    parser.add_argument('-u', '--username', default='anonymous', help='Username if site requires authentication.')
    parser.add_argument('-p', '--password', default='a.b@c.com', help='Password if the site requires authentication.')

    return parser.parse_args(args)


# Used when calling program from another module/function
def main(args):

    parsed_args = parseArgs(args)
    
    returnValue, path = testPaths(parsed_args)

    if __name__ == '__main__':
        print(returnValue)

    return returnValue
    

# Application launch
if __name__ == '__main__':

    args = main(sys.argv[1:])
