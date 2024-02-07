'''
Connor Auge - Created Nov. 26, 2023
Script to use read_vis_class.py and Morph_Plots.py to read in data and make plots for visual galaxy classifications.
'''

import numpy as np
from astropy.io import fits 
from read_vis_class import Read_File
from Morph_Plots import Plotter
from Morph_Shape_Plots import Shape_Plotter
from Morph_Display import Display
from Comp_plots import Morph_Compare
from Morph_Display import main

with fits.open('/Users/connor_auge/Research/Disertation/catalogs/AHA_SEDs_out_ALL_F6_FINAL5.fits') as hdul:
    sed_cols = hdul[1].columns
    sed_data = hdul[1].data 

sed_field = sed_data['field']
sed_id = sed_data['id']#[sed_field == 'COSMOS']
sed_z = sed_data['z']#[sed_field == 'COSMOS']
sed_x = sed_data['x']#[sed_field == 'COSMOS']
sed_y = sed_data['y']#[sed_field == 'COSMOS']
sed_Lx = sed_data['Lx']#[sed_field == 'COSMOS']
sed_norm = sed_data['norm']#[sed_field == 'COSMOS']
sed_shape = sed_data['shape']#[sed_field == 'COSMOS']
check_sed = sed_data['check6']#[sed_field == 'COSMOS']

sed_id = sed_id[check_sed == 'GOOD']
sed_z = sed_z[check_sed == 'GOOD'] 
sed_x = sed_x[check_sed == 'GOOD']
sed_y = sed_y[check_sed == 'GOOD']
sed_Lx = sed_Lx[check_sed == 'GOOD']
sed_norm = sed_norm[check_sed == 'GOOD']
sed_shape = sed_shape[check_sed == 'GOOD']
check_sed = check_sed[check_sed == 'GOOD']

# inf = Read_File('Auge_COSMOS_Classifications_read.xlsx')
inf = Read_File('Auge_COSMOS_Classifications_read.xlsx')
inf.open(type='xlsx')

cols = inf.columns() # Columns of file. Name of classification
data = inf.data()    # Data of file. Array of nans and Xs. No IDs or notes
morph_ID = inf.IDs()       # ID column of file
morph_field = inf.field()

inf.x_to_one(data)   # Turn the Xs in the data array to 1s

# Make a dictionary with Keys as classification and values as arrays for classification of each source
dict_out = inf.make_dict(cols,data,transpose=True)

print('check: ID', morph_ID[0:20])
print('check: Disk', dict_out['Disk'][0:20])
print('check: blank', dict_out['Blank'][0:20])

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

inf2 = Read_File('COSMOS_HSC_read.xlsx')
inf2.open(type='xlsx')

cols2 = inf2.columns()
data2 = inf2.data()
morph_ID2 = inf2.IDs()
# morph_field2 = inf2.field()

dict_out2 = inf2.make_dict(cols2,data2,transpose=True)


wolf_inf = Read_File('read_Aurelie_Classifications_all.xlsx',path='/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/')
wolf_inf.open(type='xlsx')
wolf_cols = wolf_inf.columns()
wolf_data = wolf_inf.data()
wolf_ID = wolf_inf.IDs()

wolf_ID_out = []
for i in range(len(wolf_ID)):
    if type(wolf_ID[i]) == str:
        wolf_ID_out.append(wolf_ID[i][4:])
    else:
        np.delete(wolf_data,i,0)
wolf_ID_out = np.asarray(wolf_ID_out,dtype=int)

wolf_dict = wolf_inf.make_dict(wolf_cols,wolf_data,transpose=True)


plot = Plotter(cols,dict_out)
plot_shape = Shape_Plotter(cols,dict_out,morph_ID,sed_id,sed_shape,sed_field,morph_field)

# plot_comp = Morph_Compare(dict_out,dict_out2)
# auge_x, auge_y = plot_comp.Auge_to_Auge()
# plot_comp.hist_comp_2D(auge_x,auge_y,xlabel='COSMOS HST',ylabel='COSMOS HSC',IDx=morph_ID,IDy=morph_ID2)

wolf_plot_comp = Morph_Compare(dict_out,wolf_dict)
wolf_x, wolf_y = wolf_plot_comp.Wolf_to_Auge()
wolf_plot_comp.hist_comp_2D(wolf_x,wolf_y,xlabel='Auge Classifications',ylabel='Wolf Classifications',IDx=morph_ID,IDy=wolf_ID_out,match_IDs=True)

# cosmos_disp = Display(cols,dict_out,morph_ID,sed_id,sed_shape,sed_x,sed_y,sed_z,sed_Lx,'/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/')
# main(sed_id,cols,dict_out,morph_ID,sed_id,sed_shape,sed_x,sed_y,sed_z,sed_Lx,'/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/')

# plot_shape.shape_class_bar('_new/total_bar_shape_tf2',flag='tf',bins='shape',save=True)
# plot_shape.shape_class_bar('_new/total_bar_shape_ps',flag='ps',bins='shape',save=True)
# plot_shape.shape_class_bar('_new/total_bar_shape_merger',flag='merger',bins='shape',save=True)

# plot_shape.shape_class_bar('_new/total_bar_shape_frac',flag='tf',bins='shape',fractional='bin',save=True)
# plot_shape.shape_class_bar('_new/total_bar_shape_frac_tot',flag='tf',bins='shape',fractional='total',save=True)


# plot.bar('_new/total_bar_tf',flag='tf',save=True)
# plot.bar('_new/total_bar_ps',flag='PS',save=True)
# plot.bar('_new/total_bar_merg',flag='merger',save=True)

