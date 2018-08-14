from os.path import join, abspath

PACKAGE_BASE = abspath(join(__file__, '..'))

# Program properties
# Constants for use in directory cleanup
CLEAN_FOLDER_ON_COMPLETION = False
FOLDER_SIZE_FOR_REPORTING = 500 # IN MEGABYTE

# Will the program be using MySQL?
USE_MYSQL = True

# static data used to make calculations
STATIC = join(PACKAGE_BASE, 'data')

MISC_FILES = join(STATIC, 'modtran')
HEAD_FILE_TEMP = join(MISC_FILES, 'head.txt')  # tape5 templates
TAIL_FILE_TEMP = join(MISC_FILES, 'tail.txt')
STAN_ATMO = join(MISC_FILES, 'stanAtm.txt')
WATER_TXT = join(MISC_FILES, 'water_emis.txt')

MERRA_PTS = join(STATIC, 'merra_points.npz')
BUOY_TXT = join(STATIC, 'noaa', 'buoy_height.txt')
STATION_TXT = join(STATIC, 'noaa', 'station_table.txt')

# relative spectral response files
RSR_L8 = {
    10: join(STATIC, 'landsat', 'L8_B10.rsp'),
    11: join(STATIC, 'landsat', 'L8_B11.rsp'),
}
RSR_MODIS = {i:join(STATIC, 'modis', 'rsr.{0}.inb.final'.format(i)) for i in range(36)}

# shapefile-like things
WRS2 = join(STATIC, 'wrs2', 'wrs2_descending.shp')
MODIS_TILE = join(STATIC, 'modis', 'sn_bound_10deg.txt')
SWATH2GRID_PRM = join(STATIC, 'modis', 'swath2grid_template.prm')

# downloading directories
DATA_BASE = 'downloaded_data'
MERRA_DIR = join(DATA_BASE, 'merra')
NARR_DIR = join(DATA_BASE, 'narr')
NOAA_DIR = join(DATA_BASE, 'noaa')
LANDSAT_DIR = join(DATA_BASE, 'landsat')
MODIS_DIR = join(DATA_BASE, 'modis')
MODTRAN_DIR = join(DATA_BASE, 'modtran')

MODTRAN_DATA = '/dirs/pkg/Mod4v3r1/DATA'
MODTRAN_EXE = '/dirs/pkg/Mod4v3r1/Mod4v3r1.exe'

# servers
MERRA_SERVER = 'https://goldsmr5.gesdisc.eosdis.nasa.gov'
NARR_SERVER = 'ftp://ftp.cdc.noaa.gov'
NOAA_SERVER = 'https://www.ndbc.noaa.gov'
LANDSAT_S3_SERVER = 'https://landsat-pds.s3.amazonaws.com'
LANDSAT_EE_SERVER = 'https://earthexplorer.usgs.gov'
#MODIS_SERVER = 'ftp://ladsweb.nascom.nasa.gov'

# urls
# TODO switch to new format strings
#  -- address changed --  MERRA_URL = 'https://goldsmr5.sci.gsfc.nasa.gov/data/s4pa/MERRA2/M2I3NPASM.5.12.4/%s/%s/MERRA2_400.inst3_3d_asm_Np.%s.nc4'
MERRA_URL = 'https://goldsmr5.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I3NPASM.5.12.4/%s/%s/MERRA2_400.inst3_3d_asm_Np.%s.nc4'
NARR_URLS = ['ftp://ftp.cdc.noaa.gov/Datasets/NARR/pressure/air.%s.nc',
             'ftp://ftp.cdc.noaa.gov/Datasets/NARR/pressure/hgt.%s.nc',
             'ftp://ftp.cdc.noaa.gov/Datasets/NARR/pressure/shum.%s.nc']
#NOAA_URLS = ['http://www.ndbc.noaa.gov/data/historical/stdmet/%sh%s.txt.gz',
#             'http://www.ndbc.noaa.gov/data/stdmet/%s%s%s2017.txt.gz']
NOAA_URLS = ['https://www.ndbc.noaa.gov/data/historical/stdmet/%sh%s.txt.gz',
             'https://www.ndbc.noaa.gov/data/stdmet/%s/%s%s%s.txt.gz']
LANDSAT_S3_URL = 'https://landsat-pds.s3.amazonaws.com'
LANDSAT_EE_URL = 'https://earthexplorer.usgs.gov/download/12864/{0}/STANDARD/EE'
#MODIS_URL = 'ftp://ladsweb.nascom.nasa.gov/allData/6'
#MODIS_URL = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6'

# authorizations / logins
# username, password
# EARTH_EXPLORER_LOGIN = ('nid4986', 'Carlson89')   # https://ers.cr.usgs.gov/login
# MERRA_LOGIN = ('nid4986', 'Carlson89')   # https://disc.gsfc.nasa.gov/


# authorizations / logins
# username, password
EARTH_EXPLORER_LOGIN = ('cisthermal','C15Th3rmal')  # https://ers.cr.usgs.gov/logins
MERRA_LOGIN = ('cisthermal','C15Th3rmal')           # https://disc.gsfc.nasa.gov/

# Database configuration details
SQL_USER = ('cisthermal')           # https://disc.gsfc.nasa.gov/
SQL_PASSWORD = ('C15Th3rmal')
SQL_SERVER = ('roc.kleynhans.poweredbyclear.com')
SQL_PORT = ('33066')
SQL_DATABASE = ('cis_tarca')
