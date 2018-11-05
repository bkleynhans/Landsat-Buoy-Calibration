###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Database connection module
# Created By          : Benjamin Kleynhans
# Creation Date       : August 29, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 5, 2018
# Filename            : download.py
#
###

import os
import sys
import pdb
import time
from time import mktime
from time import strptime
from io import BytesIO
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from ftplib import FTP

import test_paths

CHUNK = 1024 * 1024 * 8     # 1MB
downloaded = 0

class RemoteFileException(Exception):
    pass
    

# Test if the destination directory exists, create if it doesn't
def confirm_destination_path(download_path):
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

# Downloads a file from an FTP server. Supports both anonymous and secure
    # downloads
def download_ftp(args):
    """ download a http or https resource using requests. """
    
    server_address = None
    
    total_size = 0
    files_are_equal = False
    
    server_address = args.path[6:args.path[6:].index('/') + 6]
    filename = args.path[len(args.path) - args.path[::-1].index('/'):]
    output_file = args.output + filename
    retrieve_command = 'RETR ' + filename
    
    file_exists = test_paths.main([output_file, '-tfile'])
    
    if file_exists:
        files_are_equal = compare_files_from_ftp(args, server_address, filename, output_file)
    
    if not files_are_equal:
        with FTP(server_address) as ftp:
            resp = ftp.login(args.username, args.password)
            
            # for FTP a response code of 230 is successful
            if (resp.startswith('230')):
                total_size = ftp.size(filename)
                
                with open(output_file, 'wb') as out_file:
                    print()
                    
                    # lambda redirects the callback from ftp.retrbinary to the write_file
                    # method below for file writing and feedback to screen
                    ftp.retrbinary(retrieve_command, lambda block: write_file(block, total_size, out_file, filename))
                    
            restore_ftp_file_date(ftp, filename, output_file)
                
            print("\n")
        
    return args.output, filename


# Used by FTP module to write chunk/block to file and profide download status
    # update to user
def write_file(chunk, total_size, out_file, filename):
        
    global downloaded
    
    out_file.write(chunk)
    downloaded += len(chunk)
    divisor = 1000000
    units = 'MB'
    
    if (total_size < divisor):
        divisor = 1000
        units = 'KB'
    
    if total_size == 0:
        sys.stdout.write(" Downloading %s - File size unknown - Downloaded : %.1f%s\r" % (filename, (downloaded / divisor), units))
        sys.stdout.flush()
    else:            
        sys.stdout.write(" Downloading %s - %.1f%s of %.1f%s\r" % (filename, (downloaded / divisor), units, (total_size / divisor), units))
        sys.stdout.flush()
    

# Downloads a file from HTTP and HTTPS servers. Supports both open and
    # secure servers
def download_http(args):
    """ download a http or https resource using requests. """
    
    global downloaded
    
    total_size = 0
    files_are_equal = False
    
    #resource = None
    
    filename = args.path[len(args.path) - args.path[::-1].index('/'):]
    output_file = args.output + filename
    
    file_exists = test_paths.main([output_file, '-tfile'])
    
    if file_exists:
        files_are_equal, total_size = compare_files_from_http(args, output_file)
    
    if not files_are_equal:
        with requests.Session() as session:
            req = session.request('get', args.path, auth=(args.username, args.password), stream=True)
            
            if not file_exists:
                total_size = get_online_file_size_http(req)
            #total_size = int(req.headers.get('Content-Length').strip())
            #total_size = int(remove_spaces(req.headers.get('Content-Length', 'NULL')))
            
            #resource = session.get(req.url, stream = True)
            #########resource = session.get(req.url)
    
            #if resource.status_code != 200:
            if req.status_code != 200:
                raise RemoteFileException('url: {0} does not exist'.format(args.path))
        
            with open(output_file, 'wb') as out_file:
                print()
                
                #for chunk in resource.iter_content(CHUNK):
                for chunk in req.iter_content(CHUNK):
                    write_file(chunk, total_size, out_file, filename)
            
            restore_http_file_date(req, output_file)
                
            print("\n")
        
    return args.output, filename


# Analyse link to file to determine if FTP or HTTP is used and route accordingly
def download(args):
    
    global downloaded
    downloaded = 0
        
    downloaded_filename = None
    local_path_to_file = None
    
    # If the args.? variables are not of type string, extract them from the list
    # and reassign as strings
    if not isinstance(args.path, str):
        args.path = args.path[0]
        
    if not isinstance(args.username, str):
        args.username = args.username[0]
        
    if not isinstance(args.password, str):
        args.password = args.password[0]
        
    confirm_destination_path(args.output)
    
    if (args.path[:3] == 'ftp'):
        
        local_path_to_file, downloaded_filename = download_ftp(args)
        
    elif (args.path[:4] == 'http'):
        
        local_path_to_file, downloaded_filename = download_http(args)
    
    return local_path_to_file, downloaded_filename


# During download, the original file modifed date is lost, this restores the date
# to the one on the server
def restore_ftp_file_date(ftp, filename, output_file):    
    
    online_file_modified_date = ftp.sendcmd('MDTM ' + filename)[4:12]
    online_file_modified_date = mktime(strptime(online_file_modified_date, "%a, %d %b %Y %H:%M:%S GMT"))
    
    os.utime(output_file, (online_file_modified_date, online_file_modified_date))


# During download, the original file modifed date is lost, this restores the date
# to the one on the server
def restore_http_file_date(req, output_file):    
    
    online_file_modified_date = remove_spaces(req.headers.get('Last-Modified', 'NULL'))
    online_file_modified_date = mktime(strptime(online_file_modified_date, "%a, %d %b %Y %H:%M:%S GMT"))
    
    os.utime(output_file, (online_file_modified_date, online_file_modified_date))
    

# Strips all spaces from beginning and end of input value
def remove_spaces(value):
    
    if value != 'NULL':
        value = value.strip()
    else:
        value = 0
        
    return value

# Test if the file exists and is different to the one that is online before downloading
#
## It is not possible to test
def compare_files_from_http(args, output_file):
    
    files_are_equal = False
    
    online_file_size = 0
    online_file_modified_date = None
    
    local_file_size = 0
    local_file_modified_date = None
    
    with requests.Session() as session:
        req = session.request('get', args.path, auth=(args.username, args.password), stream = True)
        
        resource = session.get(req.url)
    
        if resource.status_code != 200:
            raise RemoteFileException('url: {0} does not exist'.format(args.path))
            
        try:
            online_file_size = get_online_file_size_http(req)
                
            online_file_modified_date = remove_spaces(req.headers.get('Last-Modified', 'NULL'))
        except Exception as e:
            pdb.set_trace()
            print()
    
    local_file_size = os.path.getsize(output_file)
    local_file_modified_date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(os.path.getmtime(output_file)))
    
    if (online_file_size == local_file_size and
        online_file_modified_date[:16] == local_file_modified_date[:16]):
        
        files_are_equal = True
    
    return files_are_equal, online_file_size

# Get the online file size.  If the file is compressed, get the uncrompressed size
def get_online_file_size_http(req):
    
    try:
        if (req.headers['Content-Encoding'] == 'gzip'):
            req.raw._fp = BytesIO(req.raw.read())
            online_file_size = len(req.content)
        else:
            online_file_size = int(remove_spaces(req.headers.get('Content-Length', 'NULL')))
    except Exception as e:
            pdb.set_trace()
            print()
            
    return online_file_size


# Test if the file exists and is different to the one that is online before downloading
#
## It is not possible to test
def compare_files_from_ftp(args, server_address, filename, output_file):
    
    files_are_equal = False
    
    online_file_size = 0
    online_file_modified_date = None
    
    local_file_size = 0
    local_file_modified_date = None
    
    with FTP(server_address) as ftp:
        resp = ftp.login(args.username, args.password)
        
        # for FTP a response code of 230 is successful
        if (resp.startswith('230')):
            
            online_file_size = ftp.size(filename)
            online_file_modified_date = ftp.sendcmd('MDTM ' + filename)[4:12]
    
    local_file_size = os.path.getsize(output_file)
    local_file_modified_date = time.strftime('%Y%m%d', time.gmtime(os.path.getmtime(output_file)))
    
    if (online_file_size == local_file_size and
        online_file_modified_date == local_file_modified_date):
        
        files_are_equal = True
    
    return files_are_equal
    

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
