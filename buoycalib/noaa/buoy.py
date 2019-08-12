###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Buoy module - Contains all buoy information
# Created By          : Benjamin Kleynhans
# Creation Date       : August 28, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 7, 2018
# Filename            : buoy.py
#
###

# Imports
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from buoycalib.noaa import weather_stations
import settings
from tools import download
import numpy as np
import pdb
import datetime
import math
import gzip

''' 
    This class is used to manage individual weather station calculations for stations
    that are used by NOAA.
    
    - The Constant contains the local file path for files containing
        the required data
'''

WEATHER_STATION_DATA_FILES_LOCAL = 'downloaded_data/noaa/'

class Buoy(weather_stations.Weather_Stations):

    # Class Attributes
    __id = None
    __hull_type = None
    __lat = None
    __lon = None
    __thermometer_depth = None
    __height = None
    __data_source = None
    __data_metadata_dict = {
            'date': 0,
            'wdir': 1,
            'wspd': 2,
            'gst': 3,
            'wvht': 4,
            'dpd': 5,
            'apd': 6,
            'mwd': 7,
            'pres': 8,
            'atmp': 9,
            'wtmp': 10,
            'dewp': 11,
            'vis': 12,
            'ptdy': 13,
            'tide': 14          
        }
    
    _overpass_date = None
    _data = np.empty
    
    _skin_temp = None
    _bulk_temp = None
    _surf_press = None
    _surf_airtemp = None
    _surf_rh = None        
    #_url = None
    _filename = None

    # Initializer / Instance Attributes
    def __init__(self, buoy_id, overpass_date):
        super().__init__()
        
        self.__id = buoy_id
        self._overpass_date = overpass_date
        self._get_buoy_metadata(self)
        self._get_buoy_data(self)
    
    
    @staticmethod
    def _get_buoy_metadata(self):
        
        self.__hull_type = super(Buoy, self)._get_hull_type(self, self.__id)
        self.__lat, self.__lon = super(Buoy, self)._get_lat_lon(self, self.__id)
        self.__thermometer_depth = super(Buoy, self)._get_thermometer_depth(self, self.__id)
        self.__data_source = super(Buoy, self)._get_data_source(self, self.__id)
        
        if not self.__data_source == 'No_Data':
            self._get_buoy_sensor_data(self)
        
        pass
    
    
    @staticmethod
    def _get_buoy_sensor_data(self):
        
        #pdb.set_trace()
        
        pass
    
    @staticmethod
    def _get_buoy_data(self):
        
        #pdb.set_trace()

        # TEMP FOR TESTING
        self._overpass_date = datetime.datetime.strptime(self._overpass_date, '%Y%m%d')

        if self._overpass_date.year < datetime.date.today().year:
            url = settings.NOAA_URLS[0] % (id, self._overpass_date.year)
        else:
            url = settings.NOAA_URLS[1] % (self._overpass_date.strftime('%b'), id, self._overpass_date.strftime('%-m'), datetime.datetime.now().strftime('%Y'))
        
        self._filename = url[url.rfind('/'):]
        
        download.main([url, '-o{}'.format(WEATHER_STATION_DATA_FILES_LOCAL)])
        
        self._read_data_from_zip_file(self)
    
    
    @staticmethod
    def _read_data_from_zip_file(self):
        
        #pdb.set_trace()
        
        dates = []
        lines = []
        
        with gzip.open(WEATHER_STATION_DATA_FILES_LOCAL + self._filename, 'rb') as file:
            header= file.readline()
            unit = file.readline()
            
            for line in file:
                date_str = ' '.join(line.split()[:5])
                
                if len(line.split()[0]) == 4:
                    date_dt = datetime.datetime.strptime(date_str, '%Y %m %d %H %M')
                elif len(line.split()[0]) == 2:
                    date_dt = datetime.datetime.strptime(date_str, '%y %m %d %H %M')
                    
                try:
                    data = self._filter(self, line.split()[5:])
                except ValueError:
                    print(line)
                    
                lines.append(data)
                dates.append(date_dt)
                
        headers = header.split()[5:]
        units = unit.split()[5:]
        lines = np.asarray(lines)
        
        return lines, headers, dates, units
        

    @staticmethod
    def _filter(self, iter):
        # NOAA NDBC uses 99.0 and 999.0 as a placeholder for no data
        new = []
        for item in iter:
            i = float(item)
            if i == 99 or i == 999:
                new.append(np.nan)
            else:
                new.append(i)
        return new
