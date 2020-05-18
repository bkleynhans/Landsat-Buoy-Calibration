import gzip
import pdb
import os
import re
import sys
import shutil
import tarfile
import urllib.error
import urllib.parse
import urllib.request
import warnings
import time

import requests
#import forward_model

CHUNK = 1024 * 1024 * 8   # 1 MB


class RemoteFileException(Exception):
    pass


def url_download(url, out_dir, shared_args, _filename=None, auth=None):
    """ download a file (ftp or http), optional auth in (user, pass) format """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    filename = _filename if _filename else url.split('/')[-1]
    filepath = os.path.join(out_dir, filename)

    if os.path.isfile(filepath):
        return filepath

    if url[0:3] == 'ftp':
        download_ftp(url, filepath, shared_args)
    else:
        download_http(url, filepath, shared_args, auth)

    return filepath


def download_http(url, filepath, shared_args, auth=None):
    """ download a http or https resource using requests. """
        
    with requests.Session() as session:
        output_string = "\n    Opening session to %s" % (url[:url.find('/', 9, len(url))])
        print_output(shared_args, output_string)
            
        req = session.request('get', url)

        if auth:
            resource = session.get(req.url, auth=auth)
    
            if resource.status_code != 200:
                error_string = '\n    url: {0} does not exist, trying other sources\n'.format(url)
                    
                raise RemoteFileException(error_string)
                
            else:
                output_string = "\n     Session opened successfully"
                print_output(shared_args, output_string)
        
        else:
            resource = session.get(req.url)
            
            if resource.status_code != 200:
                error_string = '\n    url: {0} does not exist, trying other sources\n'.format(url)
                    
                raise RemoteFileException(error_string)
                
            else:
                output_string = "\n     Session opened successfully"
                print_output(shared_args, output_string)
                
        with open(filepath, 'wb') as f:
            output_string = "\n    Downloading %s " % (filepath[filepath.rfind('/') + 1:])            
            print_output(shared_args, output_string)
            
            f.write(resource.content)
            
            output_string = "\n     Download completed..."
            print_output(shared_args, output_string)

    return filepath


def print_output(shared_args, output_string):
    
    if shared_args['caller'] == 'tarca_gui':        
        shared_args['log_status'].write(output_string, True)
    elif shared_args['caller'] == 'menu':
#        sys.stdout.write(output_string + '\n')
        sys.stdout.write(output_string)
        sys.stdout.flush()


def download_ftp(url, filepath, shared_args):
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
        while True:
            output_string = "    Downloading %s - %.1fMB of %.1fMB\r" % (filename, (downloaded / 1000000), (total_size / 1000000))
            
            print_output(shared_args, output_string)
                        
            chunk = request.read(CHUNK)
            if not chunk:
                break
            fileobj.write(chunk)
            downloaded += len(chunk)

        output_string = "\n     Download completed..."
        print_output(shared_args, output_string)
        

    return filepath


def ungzip(filepath):
    """ un-gzip a file (equivalent `gzip -d filepath`) """
    
    new_filepath = filepath.replace('.gz', '')

    with open(new_filepath, 'wb') as f_out, gzip.open(filepath, 'rb') as f_in:
        try:
           shutil.copyfileobj(f_in, f_out)
        except OSError as e:
            warnings.warn(str(e) + filepath, RuntimeWarning)
            shutil.copyfile(filepath, new_filepath)
            os.remove(filepath)

    return new_filepath


def untar(filepath, directory):
    """ extract all files from a tar archive (equivalent `tar -xvf filepath directory`)"""
    
    scene_filename = ''
    
    with tarfile.open(filepath, 'r') as tf:
        scene_filename = tf.getmembers()[0].name[:(tf.getmembers()[0].name).rfind('.')]
        tf.extractall(directory)

    return directory, scene_filename


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
        directory = filepath[:filepath.rfind('/')]
        filename = filepath[len(filepath) - filepath[::-1].index('/'):]
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filepath, 'wb') as fp:
            print()
            
            while True:
                output_string = "    Downloading %s - %.1fMB of %.1fMB\r" % (filename, (downloaded / 1000000), (total_size / 1000000))
                
                print_output(shared_args, output_string)
                    
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
