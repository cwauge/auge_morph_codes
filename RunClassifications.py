'''
Connor Auge - Created Nov. 26, 2023
Script to use read_vis_class.py and Morph_Plots.py to read in data and make plots for visual galaxy classifications.
'''

import numpy as np
from astropy.io import fits 
from read_vis_class import Read_File
from Morph_Plots import Plotter


inf = Read_File('Auge_COSMOS_Classifications_read.xlsx')
inf.open(type='xlsx')

cols = inf.columns() # Columns of file. Name of classification
data = inf.data()    # Data of file. Array of nans and Xs. No IDs or notes
ID = inf.IDs()       # ID column of file

inf.x_to_one(data)   # Turn the Xs in the data array to 1s

# Make a dictionary with Keys as classification and values as arrays for classification of each source
dict_out = inf.make_dict(cols,data,transpose=True)

plot = Plotter(cols,dict_out)

plot.hist()