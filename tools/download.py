###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Database connection module
# Created By          : Benjamin Kleynhans
# Creation Date       : Autust 29, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 29, 2018
# Filename            : download.py
#
###

import sys
import pdb
#import urllib
#import urllib.error
#import urllib.parse
#import urllib.request
#import warnings
import requests
#import re

from pathlib import Path

import test_paths

CHUNK = 1024 * 1024 * 8     # 1MB
downloaded = 0

class RemoteFileException(Exception):
    pass
    

def download_ftp(args):
    """ download a http or https resource using requests. """
    
    from ftplib import FTP
    
    server_address = None
    
    total_size = 0
    
    server_address = args.path[6:args.path[6:].index('/') + 6]
    filename = args.path[len(args.path) - args.path[::-1].index('/'):]
    output_file = args.output + filename
    retrieve_command = 'RETR ' + filename
    
    with FTP(server_address) as ftp:
        resp = ftp.login(args.username, args.password)
        
        # for FTP a response code of 230 is successful
        if (resp.startswith('230')):
            total_size = ftp.size(filename)
            
            with open(output_file, 'wb') as out_file:
                print()
                
                ftp.retrbinary(retrieve_command, lambda block: write_file(block, total_size, out_file, filename))
            
        print("\n")
        
    return args.output, filename


def write_file(chunk, total_size, out_file, filename):
        
    global downloaded
    
    out_file.write(chunk)
    downloaded += len(chunk)
    
    
    sys.stdout.write(" Downloading %s - %.1fMB of %.1fMB\r" % (filename, (downloaded / 1000000), (total_size / 1000000)))
    sys.stdout.flush()
    

def download_http(args):
    """ download a http or https resource using requests. """
    
    total_size = 0
    global downloaded
    
    resource = None
    
    filename = args.path[len(args.path) - args.path[::-1].index('/'):]
    output_file = args.output + filename
    
    with requests.Session() as session:
        req = session.request('get', args.path, auth=(args.username, args.password))
        
        total_size = int(req.headers.get('Content-Length').strip())
        
        resource = session.get(req.url, stream = True)

        if resource.status_code != 200:
            raise RemoteFileException('url: {0} does not exist'.format(args.path))
    
        with open(output_file, 'wb') as out_file:
            print()
            
            for chunk in resource.iter_content(CHUNK):
                write_file(chunk, total_size, out_file, filename)
            
        print("\n")
        
    return args.output, filename


def download(args):
    
    downloaded_filename = None
    local_path_to_file = None
    
    if not isinstance(args.path, str):
        args.path = args.path[0]
        
    if not isinstance(args.username, str):
        args.username = args.username[0]
        
    if not isinstance(args.password, str):
        args.password = args.password[0]
    
    if (args.path[:3] == 'ftp'):
        
        local_path_to_file, downloaded_filename = download_ftp(args)
        
    elif (args.path[:4] == 'http'):
        
        local_path_to_file, downloaded_filename = download_http(args)
    
    return local_path_to_file, downloaded_filename


# Parse the arguments supplied at program launch to determine whether a url
    # or a file path is being tested
def parseArgs(args):

    import argparse
    
    home_directory = str(Path.home()) + '/'

    parser = argparse.ArgumentParser(description='Download a file from a remote location.')

    parser.add_argument('path', help='Web link to file.  Example: https://landsat-pds.s3.amazonaws.com/c1/L8/016/030/LC08_L1TP_016030_20180629_20180630_01_RT/LC08_L1TP_016030_20180629_20180630_01_RT_B10.TIF')
    parser.add_argument('-o', '--output', default=home_directory, help='Specify the destination directory for the downloaded file.')
    parser.add_argument('-u', '--username', default='anonymous', help='Username if site requires authentication.')
    parser.add_argument('-p', '--password', default='a.b@c.com', help='Password if the site requires authentication.')

    return parser.parse_args(args)


# Used when calling program from another module/function
def main(args):

    local_path_to_file = None
    downloaded_file = None
    print_value = None
    
    parsed_args = parseArgs(args)
    
    test_type = "-turl"
    username = "-u" + parsed_args.username
    password = "-p" + parsed_args.password
    
    file_available = test_paths.main([parsed_args.path, test_type, username, password])
        
    if file_available:
        local_path_to_file, downloaded_file = download(parsed_args)
        print_value = local_path_to_file + downloaded_file
    else:
        print_value = "File not available for download."
    
    if __name__ == '__main__':
        print(print_value)

    return local_path_to_file, downloaded_file
    

# Application launch
if __name__ == '__main__':

    args = main(sys.argv[1:])
