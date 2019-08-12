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
            #pdb.set_trace()
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
            #pdb.set_trace()
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
    

def product2entityid(product_id, version='00'):
    """ convert product landsat ID to entity ID

    Ex:
    LC08_L1TP_017030_20131129_20170307_01_T1 ->
    LC80170302013333LGN01
    """
    if len(product_id) == 21:
        return product_id[:-2] + version

    sat = 'c{0}/L{1}'.format(product_id[-4], product_id[3])
    path = product_id[10:13]
    row = product_id[13:16]

    date = datetime.datetime.strptime(product_id[17:25], '%Y%m%d')

    return 'LC8{path}{row}{date}LGN{vers}'.format(path=path, row=row, date=date.strftime('%Y%j'), vers=version)


def amazon_s3_url(scene_id, band):
    """ Format a url to download an image from Amazon S3 Landsat. """
    info = parse_L8(scene_id)

    if band != 'MTL':
        filename = '%s_B%s.TIF' % (info['id'], band)
    else:
        filename = '%s_%s.txt' % (info['id'], band)

    return '/'.join([settings.LANDSAT_S3_URL, info['sat'], info['path'], info['row'], info['id'], filename])


def earthexplorer_url(scene_id):
    """Format a url to download an image from EarthExplorer. """
    return settings.LANDSAT_EE_URL.format(scene_id)


def url_download(url, out_dir, _filename=None, auth=None):
    """ download a file (ftp or http), optional auth in (user, pass) format """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    filename = _filename if _filename else url.split('/')[-1]
    filepath = os.path.join(out_dir, filename)

    if os.path.isfile(filepath):
        return filepath

    if url[0:3] == 'ftp':
        download_ftp(url, filepath)
    else:
        download_http(url, filepath, auth)

    return filepath


def download_http(url, filepath, auth=None):
    """ download a http or https resource using requests. """
        
    with requests.Session() as session:
        req = session.request('get', url)

        if auth:
            resource = session.get(req.url, auth=auth)
    
            if resource.status_code != 200:
                error_string = '\n    url: {0} does not exist, trying other sources\n'.format(url)
                    
                raise RemoteFileException(error_string)
        else:
            resource = session.get(req.url)
            
            if resource.status_code != 200:
                error_string = '\n    url: {0} does not exist, trying other sources\n'.format(url)
                    
                raise RemoteFileException(error_string)
            
        with open(filepath, 'wb') as f:
            f.write(resource.content)

    return filepath


def download_ftp(url, filepath):
    """ download an FTP resource. """
    
    total_size = 0
    
    try:
        request = urllib.request.urlopen(url)
        total_size = int(request.getheader('Content-Length').strip())
    except urllib.error.URLError as e:
        print(url)
        error_string = '\n    url: {0} does not exist, trying other sources\n'.format(url)
                    
        raise RemoteFileException(error_string)
        
    downloaded = 0
    filename = filepath[len(filepath) - filepath[::-1].index('/'):]

    with open(filepath, 'wb') as fileobj:
        print()
        
        while True:
            output_string = "   Downloading %s - %.1fMB of %.1fMB\r" % (filename, (downloaded / 1000000), (total_size / 1000000))
            
            sys.stdout.write(output_string)
            sys.stdout.flush()
            
            chunk = request.read(CHUNK)
            if not chunk:
                break
            fileobj.write(chunk)
            downloaded += len(chunk)

    print("\n")

    return filepath


def build_url(args):
    
    bands = [10, 11, 'MTL']
    
    landsat_versions = ['00', '01', '02', '03', '04',  # Will have to find a way to determine the number of versions available
                        '05', '06', '07', '08', '09']
    
    file_downloaded = None
    
    directory = directory_ + '/' + scene_id
    
    try:   
        for band in bands:
            # get url for the band
            url = amazon_s3_url(args.input, band)   # amazon s3 only has stuff from 2017 on
            fp = url_download(url, directory)
            file_downloaded = True

    except RemoteFileException:   # try to use EarthExplorer

        if connect_earthexplorer_no_proxy(*settings.EARTH_EXPLORER_LOGIN):
            for version in landsat_versions:

                entity_id = product2entityid(scene_id, version)
                url = earthexplorer_url(entity_id)
                
                try:
                    targzfile = download_earthexplorer(url, directory+'/'+entity_id+'.tar.gz', shared_args)
                    file_downloaded = True

                except RemoteFileException:
                    continue
                
                output_string = ("   Extracting {}\n".format(targzfile))
            
                if shared_args['caller'] == 'tarca_gui':
                    shared_args['log_status'].write(output_string, True)
                elif shared_args['caller'] == 'menu':
                    sys.stdout.write(output_string)
                    sys.stdout.flush()
                
                tarfile = ungzip(targzfile)
                os.remove(targzfile)
                directory['scene_filename'] = untar(tarfile, directory)
                os.remove(tarfile)
                
                break
            
        else:
            raise RuntimeError('EarthExplorer Authentication Failed. Check username, \
                password, and if the site is up (https://earthexplorer.usgs.gov/).')


def _remote_file_exists(url, auth=None):
    """ Check if remote resource exists. does not work for FTP. """
    if auth:
        resp = requests.get(url, auth=auth)
        status = resp.status_code
    else:
        status = requests.head(url).status_code

    if status != 200:
        return False

    return True


def connect_earthexplorer_no_proxy(username, password):
    """ connect to earthexplorer without a proxy server. """
    
    # inspired by: https://github.com/olivierhagolle/LANDSAT-Download
    cookies = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookies)
    urllib.request.install_opener(opener)
    
    data = urllib.request.urlopen("https://ers.cr.usgs.gov").read()
    data = data.decode('utf-8')
    m = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data)
    if m:
        token = m.group(1)
    else:
        raise RemoteFileException("EarthExplorer authentication CSRF_Token not found")
        
    params = urllib.parse.urlencode(dict(username=username, password=password, csrf_token=token)).encode('utf-8')
    request = urllib.request.Request("https://ers.cr.usgs.gov/login", params, headers={})
    f = urllib.request.urlopen(request)

    data = f.read()
    f.close()
    if data.decode('utf-8').find('You must sign in as a registered user to download data or place orders for USGS EROS products')>0:
        warnings.warn('EarthExplorer Authentication Failed. Check username, password, and if the site is up (https://earthexplorer.usgs.gov/).')
        return False

    return True


def download_earthexplorer(url, filepath, shared_args):
    """ 
    Slightly lower level downloading implemenation that handles earthexplorer's redirection.
    inspired by: https://github.com/olivierhagolle/LANDSAT-Download
    """ 

    try:
        req = urllib.request.urlopen(url)
    
        #if downloaded file is html
        if (req.info().get_content_type() == 'text/html'):
            raise RemoteFileException("error : file is in html and not an expected binary file, url: {0}".format(url))

        #if file too small           
        total_size = int(req.getheader('Content-Length').strip())
        if (total_size<50000):
           raise RemoteFileException("Error: The file is too small to be a Landsat Image, url: {0}".format(url))

        downloaded = 0
        filename = filepath[len(filepath) - filepath[::-1].index('/'):]
        
        with open(filepath, 'wb') as fp:
            print()
            
            while True:
                output_string = "   Downloading %s - %.1fMB of %.1fMB\r" % (filename, (downloaded / 1000000), (total_size / 1000000))
                
                if shared_args['caller'] == 'tarca_gui':
                    shared_args['log_status'].write(output_string, True)
                elif shared_args['caller'] == 'menu':
                    sys.stdout.write(output_string)
                    sys.stdout.flush()
                    
                chunk = req.read(CHUNK)
                if not chunk: break
                fp.write(chunk)
                downloaded += len(chunk)
    except urllib.error.HTTPError as e:
        if e.code == 500:
            raise RemoteFileException("File doesn't exist url: {0}".format(url))
        else:
            raise RemoteFileException("HTTP Error:" + e.code + url)
    
    except urllib.error.URLError as e:
        raise RemoteFileException("URL Error: {1} url: {0}".format(url, e.reason))
        
    print("\n")

    return filepath


# Parse the arguments supplied at program launch to determine whether a url
    # or a file path is being tested
def parseArgs(args):

    import argparse
    
    home_directory = str(Path.home()) + '/'

    parser = argparse.ArgumentParser(description='Download a file from a remote location.')

    parser.add_argument('input', help='Web link to file.  Example: https://landsat-pds.s3.amazonaws.com/c1/L8/016/030/LC08_L1TP_016030_20180629_20180630_01_RT/LC08_L1TP_016030_20180629_20180630_01_RT_B10.TIF')
    parser.add_argument('-t', '--type', default='url', choices=['url', 'id'], help='Specify the type of objection being downloaded.  Options are "url" and "id"')
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
    
    if parsed_args.type == 'url':
        test_type = "-turl"
        username = "-u" + parsed_args.username
        password = "-p" + parsed_args.password
    
        file_available = test_paths.main([parsed_args.path, test_type, username, password])
        
    elif parsed_args.type == 'id':
        url = build_url(args)
        
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
