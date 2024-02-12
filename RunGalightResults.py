import numpy as np
import os
from astropy.io import fits 
from Read_Galight_results import Read_Pickle
from read_vis_class import Read_File
from Morph_Plots import Plotter
from match import match

with fits.open('/Users/connor_auge/Research/Disertation/catalogs/AHA_SEDs_out_ALL_F6_FINAL8.fits') as hdul:
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

sed_field = sed_field[check_sed == 'GOOD']
sed_id = sed_id[check_sed == 'GOOD']
sed_z = sed_z[check_sed == 'GOOD'] 
sed_x = sed_x[check_sed == 'GOOD']
sed_y = sed_y[check_sed == 'GOOD']
sed_Lx = sed_Lx[check_sed == 'GOOD']
sed_norm = sed_norm[check_sed == 'GOOD']
sed_shape = sed_shape[check_sed == 'GOOD']
check_sed = check_sed[check_sed == 'GOOD']

sed_id = np.asarray(sed_id,dtype=float)

sed_id[sed_field == 'COSMOS'] += 0.1
sed_id[sed_field == 'S82X'] += 0.2
sed_id[sed_field == 'GOODS-N'] += 0.3
sed_id[sed_field == 'GOODS-S'] += 0.4

### Need to read in visual classifications as well
# inf = Read_File('Auge_COSMOS_Classifications_read.xlsx')
inf = Read_File('Auge_Classifications_read_total.xlsx')
inf.open(type='xlsx')

cols = inf.columns() # Columns of file. Name of classification
data = inf.data()    # Data of file. Array of nans and Xs. No IDs or notes
morph_ID = inf.IDs()       # ID column of file
morph_field = inf.field()

morph_ID[morph_field == 'COSMOS'] += 0.1
morph_ID[morph_field == 'S821'] += 0.2
morph_ID[morph_field == 'GOODSN'] += 0.3
morph_ID[morph_field == 'GOODSS'] += 0.4

inf.x_to_one(data)   # Turn the Xs in the data array to 1s

# Make a dictionary with Keys as classification and values as arrays for classification of each source
dict_out = inf.make_dict(cols,data,transpose=True)




path ='/Users/connor_auge/Research/Disertation/morphology/galight/galight/COSMOS_pickle_output' 
dir = os.listdir(path)

BT, BT_ps = [], []
n, n_ps = [], []

for i in range(len(dir)):
    if dir[i] == 'mc': # skip extra directory in dir
        continue
    elif '_ps_' in dir[i]:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i])
            pic.read()
            n_ps.append(pic.sersic())
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i])
            pic.read()
            BT_ps.append(pic.BtoT())
    else:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i])
            pic.read()
            n.append(pic.sersic())
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i])
            pic.read()
            BT.append(pic.BtoT())

n, n_ps = np.asarray(n), np.asarray(n_ps)
BT, BT_ps = np.asarray(BT), np.asarray(BT_ps)


plot = Plotter(cols,dict_out)

plot.hist('sersic',n,bins=[0,11,0.25],xlim=[0,10],ylim=20,xlabel='Sersic Index N')

        
