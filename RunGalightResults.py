import numpy as np
import os
from astropy.io import fits 
from Read_Galight_results import Read_Pickle
from read_vis_class import Read_File
from Morph_Plots import Plotter
from match import match
import matplotlib.pyplot as plt

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





path ='/Users/connor_auge/Research/Disertation/morphology/galight/galight/COSMOS_pickle_output/'
dir = os.listdir(path)

check = np.asarray([359852,397900,403058,428515,448411,459421,459617,461943,465458,469052,471165,599333,625595,630287,637663,673615,729517,769368,791433,828282,529855,577597,793979,577761,734950,631014],dtype='str')

BT, BT_ps = [], []
n, n_ps = [], []
name_n, name_nps = [], []
ID_n, ID_nps = [], []
ID_bt, ID_btps = [], []

for i in range(len(dir)):
    if dir[i] == 'mc': # skip extra directory in dir
        continue
    # elif dir[i][:6] in check:
    #     continue
    elif '_ps_' in dir[i]:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n_ps.append(pic.sersic())
            name_nps.append(dir[i])
            ID_nps.append(dir[i].split('_', 1)[0]+'.1')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT_ps.append(pic.BtoT())
            ID_btps.append(dir[i].split('_', 1)[0]+'.1')
    else:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n.append(pic.sersic())
            name_n.append(dir[i])
            ID_n.append(dir[i].split('_', 1)[0]+'.1')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT.append(pic.BtoT())
            ID_bt.append(dir[i].split('_', 1)[0]+'.1')


path ='/Users/connor_auge/Research/Disertation/morphology/galight/galight/GOODSN_pickle_output/' 
dir = os.listdir(path)

for i in range(len(dir)):
    if dir[i] == 'mc': # skip extra directory in dir
        continue
    # elif dir[i][:6] in check:
    #     continue
    elif '_ps_' in dir[i]:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n_ps.append(pic.sersic())
            name_nps.append(dir[i])
            ID_nps.append(dir[i].split('_', 1)[0]+'.3')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT_ps.append(pic.BtoT())
            ID_btps.append(dir[i].split('_', 1)[0]+'.3')
    else:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n.append(pic.sersic())
            name_n.append(dir[i])
            ID_n.append(dir[i].split('_', 1)[0]+'.3')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT.append(pic.BtoT())
            ID_bt.append(dir[i].split('_', 1)[0]+'.3')


path ='/Users/connor_auge/Research/Disertation/morphology/galight/galight/GOODSS_pickle_output/' 
dir = os.listdir(path)

for i in range(len(dir)):
    if dir[i] == 'mc': # skip extra directory in dir
        continue
    # elif dir[i][:6] in check:
    #     continue
    elif '_ps_' in dir[i]:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n_ps.append(pic.sersic())
            name_nps.append(dir[i])
            ID_nps.append(dir[i].split('_', 1)[0]+'.4')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT_ps.append(pic.BtoT())
            ID_btps.append(dir[i].split('_', 1)[0]+'.4')
    else:
        if dir[i][-5] == '1':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            n.append(pic.sersic())
            name_n.append(dir[i])
            ID_n.append(dir[i].split('_', 1)[0]+'.4')
        elif dir[i][-5] == '2':
            pic = Read_Pickle(dir[i],path = path)
            pic.read()
            BT.append(pic.BtoT())
            ID_bt.append(dir[i].split('_', 1)[0]+'.4')


n, n_ps = np.asarray(n), np.asarray(n_ps)
BT, BT_ps = np.asarray(BT), np.asarray(BT_ps)
name_n, name_nps = np.asarray(name_n), np.asarray(name_nps)

ID_n, ID_nps, ID_bt, ID_btps = np.asarray(ID_n,dtype=float), np.asarray(ID_nps,dtype=float), np.asarray(ID_bt,dtype=float), np.asarray(ID_btps,dtype=float)

plot = Plotter(cols,dict_out)


# print(len(n),len(name_n))

# plt.hist(n,bins=np.arange(0,10,0.25))
# plt.show()

print(ID_n)
print(morph_ID)


ix_n, iy_n = match(ID_n,morph_ID)
ix_nps, iy_nps = match(ID_nps,morph_ID)
ix_bt, iy_bt = match(ID_bt,morph_ID)
ix_btps, iy_btps = match(ID_btps,morph_ID)

vis_class = plot.Full_classification()

n_match = n[ix_n]
vis_class_n_match = vis_class[iy_n]

nps_match = n_ps[ix_nps]
vis_class_nps_match = vis_class[iy_nps]

BT_match = BT[ix_bt]
vis_class_bt_match = vis_class[iy_bt]

BTps_match = BT_ps[ix_btps]
vis_class_BTps_match = vis_class[iy_btps]

# print(n_match)
# print(n_match[vis_class_n_match == 'Disk'])
print(len(morph_ID),len(vis_class))
# print(vis_class_n_match)
# print(len(n_match[vis_class_n_match == 'Disk']))

print(len(ID_n),len(ID_btps))
# for i in range(len(morph_ID)):
#     print(morph_ID[i],vis_class[i])

# print(len(n_match),len(morph_ID[iy_n]),len(vis_class_n_match),len(n_match),len(nps_match),len(BT_match),len(BTps_match),len(vis_class_BTps_match),len(ID_btps[ix_btps]))
# for i in range(len(n_match)):
#     # print(morph_ID[iy_btps][i],morph_ID[iy_bt][i],morph_ID[iy_nps][i],morph_ID[iy_n][i],vis_class_n_match[i],n_match[i],nps_match[i],BT_match[i],BTps_match[i])
#     print(i,morph_ID[iy_n][i],ID_n[ix_n][i],vis_class_n_match[i],n_match[i],nps_match[i],BT_match[i],BTps_match[i])

# pic_check = Read_Pickle('376362_ps_2.pkl')
# pic_check.read()
# print(pic_check.BtoT())


# plot.hist('sersic_Disk',n_match[vis_class_n_match == 'Disk'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Disk',save=True)
# plot.hist('sersic_Disk_ps',nps_match[vis_class_nps_match == 'Disk'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Disk - PS',save=True)

# plot.hist('sersic_DiskSph',n_match[vis_class_n_match == 'Disk_sph'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Disk Sph',save=True)
# plot.hist('sersic_DiskSph_ps',nps_match[vis_class_nps_match == 'Disk_sph'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Disk Sph - PS',save=True)

# plot.hist('sersic_Sph',n_match[vis_class_n_match == 'Sph'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Sph',save=True)
# plot.hist('sersic_Sph_ps',nps_match[vis_class_nps_match == 'Sph'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Sph - PS',save=True)

# plot.hist('sersic_Irrg',n_match[vis_class_n_match == 'Irrg'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Irrg',save=True)
# plot.hist('sersic_Irrg_ps',nps_match[vis_class_nps_match == 'Irrg'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='Irrg - PS',save=True)

# plot.hist('sersic_PS',n_match[vis_class_n_match == 'PS'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='PS',save=True)
# plot.hist('sersic_PS_ps',nps_match[vis_class_nps_match == 'PS'],bins=[0,11,0.35],xlim=[0,10],ylim=25,xlabel='Sersic Index N',title='PS - PS',save=True)
# print(len(BT_ps))
# print(len(BTps_match))
# print(len(BTps_match[vis_class_BTps_match == 'Disk']))

plot.hist('BT_Disk_ALL',BT_match[vis_class_bt_match == 'Disk'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',title='Disk',save=True)
plot.hist('BT_Disk_ps2_ALL',BTps_match[vis_class_BTps_match == 'Disk'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',title='Disk - PS',save=True)

plot.hist('BT_DiskSph_ALL',BT_match[vis_class_bt_match == 'Disk_sph'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',title='Disk Sph',save=True)
plot.hist('BT_DiskSph_ps2_ALL',BTps_match[vis_class_BTps_match == 'Disk_sph'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',title='Disk Sph - PS',save=True)

plot.hist('BT_Sph_ALL',BT_match[vis_class_bt_match == 'Sph'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',title='Sph',save=True)
plot.hist('BT_Sph_ps2_ALL',BTps_match[vis_class_BTps_match == 'Sph'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',title='Sph - PS',save=True)

plot.hist('BT_Irrg_ALL',BT_match[vis_class_bt_match == 'Irrg'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',title='Irrg',save=True)
plot.hist('BT_Irrg_ps2_ALL',BTps_match[vis_class_BTps_match == 'Irrg'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',title='Irrg - PS',save=True)

plot.hist('BT_PS_ALL',BT_match[vis_class_bt_match == 'PS'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',title='PS',save=True)
plot.hist('BT_PS_ps2_ALL',BTps_match[vis_class_BTps_match == 'PS'],bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',title='PS - PS',save=True)

plot.hist('sersic_Disk_ALL',n_match[vis_class_n_match == 'Disk'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N',title='Disk',save=True)
plot.hist('sersic_Disk_ps2_ALL',nps_match[vis_class_nps_match == 'Disk'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N PS subtracted',title='Disk - PS',save=True)

plot.hist('sersic_DiskSph_ALL',n_match[vis_class_n_match == 'Disk_sph'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N',title='Disk Sph',save=True)
plot.hist('sersic_DiskSph_ps2_ALL',nps_match[vis_class_nps_match == 'Disk_sph'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N PS subtracted',title='Disk Sph - PS',save=True)

plot.hist('sersic_Sph_ALL',n_match[vis_class_n_match == 'Sph'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N',title='Sph',save=True)
plot.hist('sersic_Sph_ps2_ALL',nps_match[vis_class_nps_match == 'Sph'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N PS subtracted',title='Sph - PS',save=True)

plot.hist('sersic_Irrg_ALL',n_match[vis_class_n_match == 'Irrg'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N',title='Irrg',save=True)
plot.hist('sersic_Irrg_ps2_ALL',nps_match[vis_class_nps_match == 'Irrg'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N PS subtracted',title='Irrg - PS',save=True)

plot.hist('sersic_PS_ALL',n_match[vis_class_n_match == 'PS'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N',title='PS',save=True)
plot.hist('sersic_PS_ps2_ALL',nps_match[vis_class_nps_match == 'PS'],bins=[0,11,0.5],xlim=[0,10],ylim=25,xlabel='N PS subtracted',title='PS - PS',save=True)
            

plot.hist('sersic_tot_ALL2',n,bins=[0,11,0.25],xlim=[0,10],ylim=25,xlabel='Sersic Index N',save=True)
plot.hist('sersic_tot_ps_ALL2',n_ps,bins=[0,11,0.25],xlim=[0,10],ylim=25,xlabel='Sersic Index N PS subtracted',save=True)

plot.hist('BT_tots_ALL2',BT,bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T',save=True)
plot.hist('BT_tots_ps_ALL2',BT_ps,bins=[-0.1,1.2,0.1],xlim=[-0.1,1.1],ylim=25,xlabel='B/T PS subtracted',save=True)
  
