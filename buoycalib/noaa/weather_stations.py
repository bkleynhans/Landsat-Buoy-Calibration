###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Weather Station Module - Manages weather station calculations
# Created By          : Benjamin Kleynhans
# Creation Date       : September 7, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : September 7, 2018
# Filename            : weather_stations.py
#
###

# Imports
import collections
import inspect
import os
import sys
import pdb
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
import numpy as np

from tools import download

''' 
    This class is used to manage metadata for all weather stations
    that are used by NOAA.
    
    - The Constants contain the address and filenames of files containing
        the required data
'''

NOAA_DATA_FILES_WEB = 'https://www.ndbc.noaa.gov/data/stations/'
NOAA_DATA_FILES_LOCAL = 'data/noaa/'

NDBC_BUOY_FILE = 'buoyht.txt'
NDBC_STATIONS_FILE = 'cmanht.txt'
NON_NDBC_STATIONS_FILE = 'non_ndbc_heights.txt'
ALL_STATION_OWNERS_FILE = 'station_owners.txt'
ALL_STATION_METADATA_FILE = 'station_table.txt'

# The depth data is not accurately available in a file, it is configured from the NOAA
# website based on hull type.  https://www.ndbc.noaa.gov/bht.shtml
THERMOMETER_DEPTH_DATA = {
    '2.4-meter discus buoy' : 0.7,
    '2.6-meter discus buoy' : 0,
    '3-meter discus buoy'   : 0, 
    '3-meter foam buoy'     : 0.75,
    '6-meter NOMAD buoy'    : 0
}

class Weather_Stations:

    # Class Attributes
    __this_path = None
    __data_file_path = None
    __stations = []
    __station_sensors = []
    __data_files = [
            NDBC_STATIONS_FILE,
            NDBC_BUOY_FILE,
            NON_NDBC_STATIONS_FILE,
            ALL_STATION_OWNERS_FILE,
            ALL_STATION_METADATA_FILE
        ]
    
    __all_station_owners_metadata_heading_dict = {
            0: 'owner_code',
            1: 'owner_name',
            2: 'owner_country_code'
        }
    
    __all_station_owners_metadata_dict = {}
    
    __all_stations_metadata_heading_dict = {
            0: 'station_id',
            1: 'owner',
            2: 'station_type',      # Using station type for hull type determination
            3: 'hull_type',         # since many don't have a hull type specified
            4: 'name',
            5: 'payload',
            6: 'location',
            7: 'timezone',
            8: 'forecast',
            9: 'note'
        }
    
    __all_stations_metadata_dict = {}
    
    __ndbc_buoy_sensor_metadata_heading_dict = {
            0: 'station_id',
            1: 'site_elevation',
            2: 'air_temp_elevation',
            3: 'anemometer_elevation',
            4: 'barometer_elevation'
        }
    
    __ndbc_buoy_sensor_metadata_dict = {}
    
    __ndbc_station_sensor_metadata_heading_dict = {
            0: 'station_id',
            1: 'site_elevation',
            2: 'air_temp_elevation',
            3: 'anemometer_elevation',
            4: 'tide_reference',
            5: 'barometer_elevation'
        }
    
    __ndbc_station_sensor_metadata_dict = {}
    
    __non_ndbc_station_sensor_metadata_heading_dict = {
            0: 'station_id',
            1: 'site_elevation',
            2: 'air_temp_elevation',
            3: 'anemometer_elevation',
            4: 'tide_reference',
            5: 'barometer_elevation',
            6: 'water_temperature_elevation',
            7: 'water_depth',
            8: 'watch_circle'
        }
    
    __non_ndbc_station_sensor_metadata_dict = {}
    
    __sensor_data_dictionaries = [
            __ndbc_buoy_sensor_metadata_dict,
            __ndbc_station_sensor_metadata_dict,
            __non_ndbc_station_sensor_metadata_dict
        ]

    # Initializer / Instance Attributes
    def __init__(self):
        
        sys.stdout.write(" Please be patient while the weather station metadata files are updated\n")
        
        self.__this_path = self.get_module_path(self)
        self.__data_file_path = self.__this_path[:len(self.__this_path) - 4] + NOAA_DATA_FILES_LOCAL
        
        self._update_data_files(self)
        
        self._read_all_station_owners_file(self)
        self._read_all_stations_file(self)
        self._read_ndbc_buoy_sensor_file(self)
        self._read_ndbc_station_sensor_file(self)
        self._read_non_ndbc_station_sensor_file(self)
        
        
    # Calculate fully qualified path to location of program execution
    @staticmethod
    def get_module_path(self):
        
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    
        return path
    
    
    # Download that NOAA weather station metadata files
    @staticmethod
    def _update_data_files(self):
                
        for file in self.__data_files:
            sys.stdout.write(" Updating %s...\n" % (file))
            full_path = NOAA_DATA_FILES_WEB + file
            download.main([full_path, '-o{}'.format(self.__data_file_path)])
            
    
    @staticmethod
    def _read_all_station_owners_file(self):
        
        with open((self.__data_file_path + ALL_STATION_OWNERS_FILE)) as file:
            file.readline()
            file.readline()
            
            for line in file:
                
                current_line_data = line.rstrip('\n')
                current_line_index = current_line_data[
                                    0:current_line_data.find('|')].strip(' \t\n\r')
                
                first_delimiter_index = 0
                second_delimiter_index = 0
                
                for i in range(0, 3):                    
                    if i == 0:         
                        
                        self.__all_station_owners_metadata_dict[current_line_index] = {}
                        
                        first_delimiter_index = current_line_data.find('|') + 1
                        
                    else:
                        
                        second_delimiter_index = current_line_data.find('|', first_delimiter_index)
                        
                        self.__all_station_owners_metadata_dict[current_line_index][self.__all_station_owners_metadata_heading_dict[i]] = (current_line_data[first_delimiter_index:second_delimiter_index]).strip(' \t\n\r')
                                
                        first_delimiter_index = second_delimiter_index + 1
    

    @staticmethod
    def _read_all_stations_file(self):
        
        with open((self.__data_file_path + ALL_STATION_METADATA_FILE)) as file:
            file.readline()
            
            for line in file:
                
                current_line_data = line.rstrip('\n')
                current_line_index = current_line_data[
                                    0:current_line_data.find('|')].strip(' \t\n\r')
                
                first_delimiter_index = 0
                second_delimiter_index = 0
                
                for i in range(0, 10):
                    if i == 0:         
                        
                        self.__all_stations_metadata_dict[current_line_index] = {}
                        
                        first_delimiter_index = current_line_data.find('|') + 1
                        
                    else:
                        
                        second_delimiter_index = current_line_data.find('|', first_delimiter_index)
                        
                        self.__all_stations_metadata_dict[current_line_index][self.__all_stations_metadata_heading_dict[i]] = (current_line_data[first_delimiter_index:second_delimiter_index]).strip(' \t\n\r')
                                
                        first_delimiter_index = second_delimiter_index + 1
            
    
    @staticmethod
    def _read_ndbc_buoy_sensor_file(self):
        
        with open((self.__data_file_path + NDBC_BUOY_FILE)) as file:
            for header_lines in range(0, 7):
                file.readline()
            
            for line in file:
                
                current_line_data = line.rstrip('\n')
                current_line_array = current_line_data.split()
                current_line_index = current_line_array[0]
                
                for i in range(0, len(current_line_array)):
                    if i == 0:         
                        
                        self.__ndbc_buoy_sensor_metadata_dict[current_line_index] = {}
                        
                    else:
                        
                        self.__ndbc_buoy_sensor_metadata_dict[current_line_index][self.__ndbc_buoy_sensor_metadata_heading_dict[i]] = current_line_array[i].strip(' \t\n\r')


    @staticmethod
    def _read_ndbc_station_sensor_file(self):
        
        with open((self.__data_file_path + NDBC_STATIONS_FILE)) as file:
            for header_lines in range(0, 7):
                file.readline()
            
            for line in file:
                
                current_line_data = line.rstrip('\n')
                current_line_array = current_line_data.split()
                current_line_index = current_line_array[0]
                
                for i in range(0, len(current_line_array)):
                    if i == 0:         
                        
                        self.__ndbc_station_sensor_metadata_dict[current_line_index] = {}
                        
                    else:
                        
                        self.__ndbc_station_sensor_metadata_dict[current_line_index][self.__ndbc_station_sensor_metadata_heading_dict[i]] = current_line_array[i].strip(' \t\n\r')
    
    @staticmethod
    def _read_non_ndbc_station_sensor_file(self):
        
        with open((self.__data_file_path + NON_NDBC_STATIONS_FILE)) as file:
            for header_lines in range(0, 6):
                file.readline()
            
            for line in file:
                
                current_line_data = line.rstrip('\n')
                current_line_array = current_line_data.split()
                current_line_index = current_line_array[0]
                
                for i in range(0, len(current_line_array)):
                    if i == 0:         
                        
                        self.__non_ndbc_station_sensor_metadata_dict[current_line_index] = {}
                        
                    else:
                        
                        self.__non_ndbc_station_sensor_metadata_dict[current_line_index][self.__non_ndbc_station_sensor_metadata_heading_dict[i]] = current_line_array[i].strip(' \t\n\r')
                        
    @staticmethod
    def _get_hull_type(self, buoy_id):
        
        hull_type = self.__all_stations_metadata_dict[buoy_id]['hull_type']
        
        # If the hull type value is empty, supply default value of unknown
        if hull_type == '':
            hull_type = "unknown"
        
        return hull_type
    
    @staticmethod
    def _get_lat_lon(self, buoy_id):
        
        lat_lon = self.__all_stations_metadata_dict[buoy_id]['location']
        
        # If the hull type value is empty, supply default value of unknown
        if lat_lon == '':
            lat_lon= "unknown"
        else:
            lat_lon = lat_lon.split(' (')[0]
            lat_lon = lat_lon.split()
            
            if lat_lon[1] == 'S':
                lat = float(lat_lon[0]) * (-1)
            else:
                lat = float(lat_lon[0])

            if lat_lon[3] == 'W':
                lon = float(lat_lon[2]) * (-1)
            else:
                lon = float(lat_lon[2])
        
        return lat, lon
    
    @staticmethod
    def _get_data_source(self, buoy_id):
    
        found_station = False
        data_source = None
        
        for dictionary in self._Weather_Stations__sensor_data_dictionaries:
            if (buoy_id in dictionary):
                data_source = dictionary
                found_station = True
                
                if found_station:
                    break
                
        if not found_station:
            data_source = 'No_Data'
        
        return data_source
    
    @staticmethod
    def _get_thermometer_depth(self, buoy_id):
        
        
        
        pass