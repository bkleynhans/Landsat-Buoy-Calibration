###
#
# CIS Top of Atmosphere Radiance Calibration
#
# Program Description : Generates a graph from a text file or a list
# Created By          : Benjamin Kleynhans
# Creation Date       : June 25, 2018
# Authors             : Benjamin Kleynhans
#
# Last Modified By    : Benjamin Kleynhans
# Last Modified Date  : August 2, 2018
# Filename            : graph_generator.py
#
###

#import numpy as np
import matplotlib.pyplot as plt
import pdb
#import pandas as pd

class Graph_Generator:
    
    #Class Attributes
    x_axis_values = []  # date
    y_axis_values = []  # difference between landsat and noaa
    
    error = []
    
    # Initializer / Instance Attributes
    def __init__(self):
        pass
    
    # Graph data needs to be a numpy array of shape np.zeros([1,4]) !!! REMEMBER .zeros fills the first row in the table with zeros
    def generate_graph(self, title, x_label, y_label, graph_data, output_file):
        
        # Assign values data ranges
        self.x_axis_values = graph_data[:,0]
        self.y_axis_values = graph_data[:,1].astype(float)
        self.error = graph_data[:,2]
        
        # Generate graph output name
        output_filename = output_file[:-(output_file.index('.') + 1)]
        
        # Apply formatting to graph
        plt.title(title)
        plt.xlabel(x_label, rotation=1)
        plt.ylabel(y_label)
        plt.grid(True, linestyle=':')
                
        # Create graph plot
        plt.scatter(self.x_axis_values, self.y_axis_values, s=10)
        plt.errorbar(self.x_axis_values, self.y_axis_values, yerr=self.error, capsize=2, ls='none')
        
        # Save figure to different variable to allow further manipulation (like show())
        this_graph = plt.gcf()
        this_graph.set_size_inches(14.4, 9)
        this_graph.savefig(output_filename + ".png")
        
        #plt.show()
        
        
        
    
