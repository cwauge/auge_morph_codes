'''
Connor Auge - Created Nov. 26, 2023
Script to use read_vis_class.py and Morph_Plots.py to read in data and make plots for visual galaxy classifications.
'''

import numpy as np
from astropy.io import fits 
from read_vis_class import Read_File
from Morph_Plots import Plotter
from Morph_Shape_Plots import Shape_Plotter

with fits.open('/Users/connor_auge/Research/Disertation/catalogs/AHA_SEDs_out_ALL_F6_FINAL5.fits') as hdul:
    sed_cols = hdul[1].columns
    sed_data = hdul[1].data 

sed_field = sed_data['field']
sed_id = sed_data['id'][sed_field == 'COSMOS']
sed_z = sed_data['z'][sed_field == 'COSMOS']
sed_x = sed_data['x'][sed_field == 'COSMOS']
sed_y = sed_data['y'][sed_field == 'COSMOS']
sed_Lx = sed_data['Lx'][sed_field == 'COSMOS']
sed_norm = sed_data['norm'][sed_field == 'COSMOS']
sed_shape = sed_data['shape'][sed_field == 'COSMOS']


inf = Read_File('Auge_COSMOS_Classifications_read.xlsx')
inf.open(type='xlsx')

cols = inf.columns() # Columns of file. Name of classification
data = inf.data()    # Data of file. Array of nans and Xs. No IDs or notes
morph_ID = inf.IDs()       # ID column of file

inf.x_to_one(data)   # Turn the Xs in the data array to 1s

# Make a dictionary with Keys as classification and values as arrays for classification of each source
dict_out = inf.make_dict(cols,data,transpose=True)

print('Disk:          ',len(dict_out['Disk']),np.nansum(dict_out['Disk']))
print('Disk-Spheroid: ',len(dict_out['Disk-Spheroid']),np.nansum(dict_out['Disk-Spheroid']))
print('Spheroid:      ',len(dict_out['Spheroid']),np.nansum(dict_out['Spheroid']))
print('Irregular:     ',len(dict_out['Irregular']),np.nansum(dict_out['Irregular']))
print('PS:            ',len(dict_out['PS']),np.nansum(dict_out['PS']))
print('Unclassifiable:',len(dict_out['Unclassifiable']),np.nansum(dict_out['Unclassifiable']))
print('Blank:         ',len(dict_out['Blank']),np.nansum(dict_out['Blank']))
print('Merger_flag:   ',len(dict_out['Merger_flag']),np.nansum(dict_out['Merger_flag']))
print('TF_flag:       ',len(dict_out['TF_flag']),np.nansum(dict_out['TF_flag']))
print('PS_flag:       ',len(dict_out['PS_flag']),np.nansum(dict_out['PS_flag']))


plot = Plotter(cols,dict_out)
plot_shape = Shape_Plotter(cols,dict_out,morph_ID,sed_id,sed_shape)

plot_shape.shape_class_bar('_new/bar_shape',flag='tf',bins='shape',save=True)
plot_shape.shape_class_bar('_new/bar_shape_frac',flag='tf',bins='shape',fractional='bin',save=True)
plot_shape.shape_class_bar('_new/bar_shape_frac_tot',flag='tf',bins='shape',fractional='total',save=True)


# plot.bar('_new/total_bar_tf',flag='tf',save=False)
# plot.bar('_new/total_bar_ps',flag='PS',save=False)
# plot.bar('_new/total_bar_merg',flag='merger',save=False)