###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Split window claculation
# Created By          : Benjamin Kleynhans
# Creation Date       : June 18, 2019
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 15, 2019
# Filename            : split_window.py
#
###

# Imports
import inspect, os
import numpy as np
import csv
from modules.stp.stp_base import STP_Base
import pdb

FILENAME = 'Coeff_RH90_quad.csv'

class Split_Window(STP_Base):
    
    def __init__(self, rad_b10, rad_b11, emis_b10, emis_b11):
        
        self.coeff_rh90 = []
        self.data = {}
        
        self.read_coefficients()
        
        # Supplied Band 10 and Band 11 Radiance values
        self.rad_val = {10: float(rad_b10),
                        11: float(rad_b11)}
        
        # Supplied Band 10 and Band 11 Emmissivity
        self.emis_val = {10: float(emis_b10),
                         11: float(emis_b11)}
        
        # TIRS Radiance to Apparent Temperature conversion coefficients
        self.conv_coeffs = {'K1_10': float(774.8853),
                            'K2_10': float(1321.0789),
                            'K1_11': float(480.8883),
                            'K2_11': float(1201.1442)}
        
        # Apparent temperatures
        self.apparent_temps = {'T10': '',
                               'T11': ''}
        
        # Perform calculations
        self.calc_apparent_temp()
        self.calc_split_window()
        
        self.data['radiance'] = self.rad_val
        self.data['emissivity'] = self.emis_val
        self.data['conv_coeffs'] = self.conv_coeffs
        self.data['apparent_temps'] = self.apparent_temps
        
    
    def read_coefficients(self):
        
        current_path = inspect.getfile(inspect.currentframe())
        current_path = current_path[:current_path.rfind('/')]
        
        coeff_file = os.path.join(current_path, FILENAME)
        
        with open(coeff_file) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                self.coeff_rh90.extend(row)
                
        
        self.coeff_rh90 = [float(i) for i in self.coeff_rh90]
        
    
    def calc_apparent_temp(self):
        
        self.apparent_temps['T10'] = float(self.conv_coeffs['K2_10'] / np.log(self.conv_coeffs['K1_10'] / self.rad_val[10] + 1))
        self.apparent_temps['T11'] = float(self.conv_coeffs['K2_11'] / np.log(self.conv_coeffs['K1_11'] / self.rad_val[11] + 1))
    
    
    def calc_split_window(self):
        
        self.data['T_plus'] = float((self.apparent_temps['T10'] + self.apparent_temps['T11']) / 2)
        self.data['T_min'] = float((self.apparent_temps['T10'] - self.apparent_temps['T11']) / 2)
        self.data['e_min'] = float(((1 - (self.emis_val[10] + self.emis_val[11]) / 2) / ((self.emis_val[10] + self.emis_val[11]) / 2)))
        self.data['e_change'] = float((self.emis_val[10] - self.emis_val[11]) / (((self.emis_val[10] + self.emis_val[11]) / 2) ** 2))
        self.data['T_quad'] = float((self.apparent_temps['T10'] - self.apparent_temps['T11']) ** 2)
                
        lst_0 = self.coeff_rh90[0]
        lst_1 = self.data['T_plus'] * (self.coeff_rh90[1] + self.coeff_rh90[2] * self.data['e_min'] + self.coeff_rh90[3] * self.data['e_change'])
        lst_2 = (self.data['T_min'] * (self.coeff_rh90[4] + self.coeff_rh90[5] * self.data['e_min'] + self.coeff_rh90[6] * self.data['e_change']) + self.coeff_rh90[7] * self.data['T_quad'])
        
        self.data['LST_SW'] = lst_0 + lst_1 + lst_2