import datetime
import glob
import pdb
import sys

from osgeo import gdal, osr
import ogr
import utm

from .. import settings
from ..download import *
from . import image_processing as img

from tools import test_paths

def download(scene_id, shared_args, directory_=settings.LANDSAT_DIR):
    """ Download a landsat image and load its metadata.

    Amazon S3 is faster but only has images from 2017 - present
    Website: https://aws.amazon.com/public-datasets/landsat/
    EarthExplorer is slower: https://earthexplorer.usgs.gov/
    """
    
    bands = shared_args['bands'].copy()
    
    landsat_versions = ['00', '01', '02', '03', '04',  # Will have to find a way to determine the number of versions available
                        '05', '06', '07', '08', '09']
    
    file_downloaded = None
    
    directory = directory_ + '/' + scene_id
        
    if (len(glob.glob('{0}/*_MTL.txt'.format(directory))) == 0 or
        len(glob.glob('{0}/*_B10.TIF'.format(directory))) == 0 or
        len(glob.glob('{0}/*_B11.TIF'.format(directory))) == 0):
        
        output_string = ("   The required files are not available and will now be downloaded")
        print_output(shared_args, output_string)
        
        if test_paths.main([directory + "/" + scene_id + ".tar.gz", "-tfile"]):
            
            targzfile = directory + "/" + scene_id + ".tar.gz"
            
            try:
                output_string = ("   Extracting {}.tar.gz\n".format(scene_id))
                print_output(shared_args, output_string)
                
                tarfile = ungzip(targzfile)
                os.remove(targzfile)
                directory, shared_args['scene_filename'] = untar(tarfile, directory)
                os.remove(tarfile)
                
                file_downloaded = True
                
            except EOFError:
                
                file_downloaded = False
    else:        
        output_string = ("   The required files are available and do NOT need to be downloaded")
        print_output(shared_args, output_string)
            
        file_downloaded = True
                
    if not file_downloaded:
        if 'MTL' not in bands:
            bands.append('MTL')
    
        #### Remove Amazon Web services for testing - the Amazon data seems faulty
#        try:   
#            for band in bands:
#                # get url for the band
#                url = amazon_s3_url(scene_id, band)   # amazon s3 only has stuff from 2017 on
#                
#                try:
#                    fp = url_download(url, directory, shared_args)
#                    file_downloaded = True
#                except:
#                    pass
#    
#        except RemoteFileException:   # try to use EarthExplorer
    
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
                print_output(shared_args, output_string)
                
                try:                        
                    tarfile = ungzip(targzfile)
                except EOFError:
                    raise RuntimeError("The file source file for {} is corrupt".format(entity_id))
                    
                os.remove(targzfile)
                directory, shared_args['scene_filename'] = untar(tarfile, directory)
                os.remove(tarfile)
                
                break
            
        else:
            raise RuntimeError('EarthExplorer Authentication Failed. Check username, \
                password, and if the site is up (https://earthexplorer.usgs.gov/).')

    # Pull glob value from folder
    glob_value = glob.glob('{0}/*_MTL.txt'.format(directory))
    
    # Test if the file exists before accessing its data
    if len(glob_value) != 0:
        if (test_paths.main([glob.glob('{0}/*_MTL.txt'.format(directory))[0],'-tfile'])):
            meta_file = glob.glob('{0}/*_MTL.txt'.format(directory))[0]
            metadata = read_metadata(meta_file)
        else:
            metadata = {'date':(0)}
    else:
        file_downloaded = False
        metadata = {'date':(0)}
        
    return metadata['date'], directory, metadata, file_downloaded

def print_output(shared_args, output_string):
    
    if shared_args['caller'] == 'tarca_gui':
        shared_args['log_status'].write(output_string, True)
    elif shared_args['caller'] == 'menu':
        sys.stdout.write(output_string + '\n')
        sys.stdout.flush()
        
        
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


def parse_L8(scene_id):
    parsed = {}

    if len(scene_id) == 21:   # entity ID
        parsed['sat'] = 'L' + scene_id[2:3]
        parsed['path'] = scene_id[3:6]
        parsed['row'] = scene_id[6:9]
        parsed['id'] = scene_id
    elif len(scene_id) == 40:   # product ID
        parsed['sat'] = 'c{0}/L{1}'.format(scene_id[-4], scene_id[3])
        parsed['path'] = scene_id[10:13]
        parsed['row'] = scene_id[13:16]
        parsed['id'] = scene_id
    else:
        raise Exception('Received incorrect scene: {0}'.format(scene_id))

    return parsed

def read_metadata(filename):
    """
    Read landsat metadata from MTL file and return a dict with the values.

    Args:
        filename: absolute file location of metadata file

    Returns:
        metadata: dict of landsat metadata from _MTL.txt file.
    """
    def _replace(string, chars):
        for c in chars:
            string = string.replace(c, '')
        return string

    # TODO make really robust
    chars = ['\n', '"', '\'']    # characters to remove from lines
    metadata = {}

    with open(filename, 'r') as mtl_file:
        for line in mtl_file:
            try:
                info = _replace(line.strip(' '), chars).split(' = ')
                if 'GROUP' in info or 'END_GROUP' in info or 'END' in info:
                    continue
                info[1] = _replace(info[1], chars)
                metadata[info[0]] = float(info[1])
            except ValueError:
                metadata[info[0]] = info[1]

    dt_str = metadata['DATE_ACQUIRED'] + ' ' + metadata['SCENE_CENTER_TIME'][:8]
    metadata['date'] = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

    return metadata


def corners(metadata):
    """" ur_lat, ll_lat, ur_lon, ll_lon """
    return metadata['CORNER_UR_LAT_PRODUCT'], metadata['CORNER_LL_LAT_PRODUCT'], \
           metadata['CORNER_UR_LON_PRODUCT'], metadata['CORNER_LL_LON_PRODUCT']


def calc_ltoa(directory, metadata, lat, lon, band):
    """
    Calculate image radiance from metadata

    Args:
        metadata: landsat scene metadata
        lat: point of interest latitude
        lon: point of interest longitude
        band: image band to calculate form

    Returns:
        radiance: L [W m-2 sr-1 um-1] of the image at the buoy location
    """
    img_file = directory + '/' + metadata['FILE_NAME_BAND_' + str(band)]

    dataset = gdal.Open(img_file)   # open image
    geotransform = dataset.GetGeoTransform()   # get data transform

    # change lat_lon to same projection
    l_x, l_y, l_zone, l_zone_let = utm.from_latlon(lat, lon)

    if metadata['UTM_ZONE'] != l_zone:
        l_x, l_y = img.convert_utm_zones(l_x, l_y, l_zone, metadata['UTM_ZONE'])

    # calculate pixel locations: http://www.gdal.org/gdal_datamodel.html
    x = int((l_x - geotransform[0]) / geotransform[1])   # latitude
    y = int((l_y - geotransform[3]) / geotransform[5])   # longitude

    # TODO check if x, y are within bounds

    # calculate digital count average of 3x3 area around poi
    # TODO add ROI width parameter
    image_data = dataset.ReadAsArray()
    #print(image_data, image_data.shape, image_data.mean(), y, x)
    dc_avg = image_data[y-1:y+2, x-1:x+2].mean()
    
    if dc_avg == 0:
        raise RuntimeError('buoy falls outside of image (in the corner)')

    add = metadata['RADIANCE_ADD_BAND_' + str(band)]
    mult = metadata['RADIANCE_MULT_BAND_' + str(band)]

    radiance = dc_avg * mult + add
    #print(dc_avg, mult, add)

    return radiance
