'''
Connor Auge - Created Nov. 26, 2023
Script to use read_vis_class.py and Morph_Plots.py to read in data and make plots for visual galaxy classifications.
'''

import numpy as np
from astropy.io import fits, ascii
from read_vis_class import Read_File
from Morph_Plots import Plotter
from Morph_Shape_Plots import Shape_Plotter
from Morph_Display import Display
from Comp_plots import Morph_Compare
from Morph_Display import main
from match import match

with fits.open('/Users/connor_auge/Research/Disertation/catalogs/AHA_SEDs_out_ALL_F6_FINAL8.fits') as hdul:
    sed_cols = hdul[1].columns
    sed_data = hdul[1].data 

sed_field = sed_data['field']
sed_id = sed_data['id']#[sed_field == 'S82X']
sed_z = sed_data['z']#[sed_field == 'S82X']
sed_x = sed_data['x']#[sed_field == 'S82X']
sed_y = sed_data['y']#[sed_field == 'S82X']
sed_Lx = sed_data['Lx']#[sed_field == 'S82X']
sed_norm = sed_data['norm']#[sed_field == 'S82X']
sed_shape = sed_data['shape']#[sed_field == 'S82X']
check_sed = sed_data['check6']#[sed_field == 'S82X']

sed_field = sed_field#[sed_field == 'S82X']

sed_field = sed_field[check_sed == 'GOOD']
sed_id = np.asarray(sed_id[check_sed == 'GOOD'],dtype=float)
sed_z = sed_z[check_sed == 'GOOD'] 
sed_x = sed_x[check_sed == 'GOOD']
sed_y = sed_y[check_sed == 'GOOD']
sed_Lx = sed_Lx[check_sed == 'GOOD']
sed_norm = sed_norm[check_sed == 'GOOD']
sed_shape = sed_shape[check_sed == 'GOOD']
check_sed = check_sed[check_sed == 'GOOD']

with fits.open('/Users/connor_auge/Research/Disertation/xcigale/results/sample_read_out.fits') as hdul:
    cigale_cols = hdul[1].columns
    cigale_data = hdul[1].data 

cigale_ID = cigale_data['ID']
cigale_Lx = cigale_data['Lx']
cigale_Lagn = cigale_data['Lagn']
cigale_Lagn_fir = cigale_data['Lfir_agn']
cigale_sfr = cigale_data['SFR']
cigale_m = cigale_data['Mstar']
cigale_Lfir = cigale_data['Lfir']

sed_id[sed_field == 'COSMOS'] += 0.1
sed_id[sed_field == 'S82X'] += 0.2
sed_id[sed_field == 'GOODS-N'] += 0.3
sed_id[sed_field == 'GOODS-S'] += 0.4

ix, iy = match(cigale_ID, sed_id)

cigale_ID = cigale_ID[ix]
cigale_Lx = cigale_Lx[ix]
cigale_Lagn = cigale_Lagn[ix]
cigale_Lagn_fir = cigale_Lagn_fir[ix]
cigale_Lfir = cigale_Lfir[ix]
cigale_sfr = cigale_sfr[ix]
cigale_m = cigale_m[ix]

sed_field = sed_field[iy]
sed_id = sed_id[iy]
sed_z = sed_z[iy] 
sed_x = sed_x[iy]
sed_y = sed_y[iy]
sed_Lx = sed_Lx[iy]
sed_norm = sed_norm[iy]
sed_shape = sed_shape[iy]
check_sed = check_sed[iy]

sed_id = np.asarray(sed_id,dtype=float)

# inf = Read_File('S82X_Classifications_read.xlsx')
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

# print('check: ID', morph_ID[0:20])
# print('check: Disk', dict_out['Disk'][0:20])
# print('check: blank', dict_out['Blank'][0:20])

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

print(dict_out['Disk-Spheroid'][morph_ID == 66])

inf_jwst = Read_File('All_JWST_read.xlsx')
inf_jwst.open(type='xlsx')

cols_jwst = inf_jwst.columns()
data_jwst = inf_jwst.data()
ID_jwst = inf_jwst.IDs()
field_jwst = inf_jwst.field()

ID_jwst[field_jwst == 'GOODSS'] += 0.5

inf_jwst.x_to_one(data_jwst)
dict_jwst = inf.make_dict(cols_jwst,data_jwst,transpose=True)

inf_hsc = Read_File('COSMOS_HSC_read.xlsx')
inf_hsc.open(type='xlsx')

cols_hsc = inf_hsc.columns()
data_hsc = inf_hsc.data()
morph_ID_hsc = inf_hsc.IDs()
# morph_field2 = inf2.field()
inf_hsc.x_to_one(data_hsc)

dict_out_hsc = inf_hsc.make_dict(cols_hsc,data_hsc,transpose=True)


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

lilly_inf = Read_File('Lilly_classifications2.csv',path='/Users/connor_auge/Research/Disertation/morphology/visual/classifications/')
lilly_inf.open(type='csv')
lilly_cols = lilly_inf.columns()
lilly_data = lilly_inf.data()
lilly_ID = lilly_inf.IDs()

lilly_dict = lilly_inf.make_dict(lilly_cols,lilly_data,transpose=True)


plot = Plotter(cols,dict_out)
# plot_shape = Shape_Plotter(cols,dict_out,morph_ID,sed_id,sed_shape,sed_field,morph_field)

# hsc_plot_comp = Morph_Compare(dict_out,dict_out_hsc)
# auge_x, auge_y = hsc_plot_comp.Auge_to_Auge()
# hsc_plot_comp.hist_comp_2D('hsc_comp2',auge_x,auge_y,xlabel='COSMOS HST',ylabel='COSMOS HSC',IDx=morph_ID,IDy=morph_ID_hsc,match_IDs=True)
# hsc_plot_comp.hist_comp_2D_split('hsc_comp_zbin2',auge_x, auge_y, xlabel='HST Classifications', ylabel='HSC Classifications', IDx=morph_ID, IDy=morph_ID_hsc,match_IDs=True,cond=True,cond_var=sed_z,cond_lim=0.5)


# jwst_plot_comp = Morph_Compare(dict_out,dict_jwst)
# auge_x, jwst_y = jwst_plot_comp.Auge_to_Auge()
# jwst_plot_comp.hist_comp_2D('jwst_comp',auge_x, jwst_y, xlabel='HST Classifications', ylabel='JWST Classifications', IDx=morph_ID, IDy=ID_jwst,match_IDs=True)
# jwst_plot_comp.hist_comp_2D_split('jwst_comp_zbin',auge_x, jwst_y, xlabel='HST Classifications', ylabel='JWST Classifications', IDx=morph_ID, IDy=ID_jwst,match_IDs=True,cond=True,cond_var=sed_z,cond_lim=0.5)

# wolf_plot_comp = Morph_Compare(dict_out,wolf_dict)
# wolf_x, wolf_y = wolf_plot_comp.Wolf_to_Auge()
# wolf_plot_comp.hist_comp_2D('wolf_comp',wolf_x,wolf_y,xlabel='Auge Classifications',ylabel='Wolf Classifications',IDx=morph_ID,IDy=wolf_ID_out,match_IDs=True)

# lilly_plot_comp = Morph_Compare(dict_out,lilly_dict)
# lilly_x, lilly_y = lilly_plot_comp.Lilly_to_Auge()
# lilly_plot_comp.hist_comp_2D('lilly_comp',lilly_x,lilly_y,xlabel='Auge Classifications',ylabel='Lilly Classifications',IDx=morph_ID,IDy=lilly_ID,match_IDs=True)

# wolf_plot_comp.hist_comp_2D('wolf_lilly_comp',wolf_y,lilly_y,xlabel='Wolf Classifications',ylabel='Lilly Classifications',IDx=wolf_ID_out,IDy=lilly_ID,match_IDs=True)
# wolf_plot_comp.hist_comp_2D('Multi_comp_frac2',wolf_x,wolf_y,xlabel='Auge Classifications',ylabel='Other Classifiers',IDx=morph_ID,IDy=wolf_ID_out,match_IDs=True,multi=True,x_in2=lilly_x,y_in2=lilly_y,IDx2=morph_ID,IDy2=lilly_ID)


# wolf_plot_comp.hist_comp_2D_split('wolf_comp_zbin',wolf_x, wolf_y, xlabel='Auge Classifications', ylabel='Wolf Classifications', IDx=morph_ID, IDy=wolf_ID,match_IDs=True,cond=True,cond_var=sed_z,cond_lim=0.5)

# cosmos_disp = Display(cols,dict_out,morph_ID,sed_id,sed_shape,sed_x,sed_y,sed_z,sed_Lx,'/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/')
# main(sed_id,cols,dict_out,morph_ID,sed_id,sed_shape,sed_x,sed_y,sed_z,sed_Lx,'/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/')

# plot_shape.shape_class_bar('_new/total_bar_shape_mg2',flag='merger',bins='shape',save=True)
# plot_shape.shape_class_bar('_new/total_bar_shape_ps',flag='ps',bins='shape',save=True)
# plot_shape.shape_class_bar('_new/total_bar_shape_merger',flag='merger',bins='shape',save=True)

# plot_shape.shape_class_bar('_new/total_bar_shape_frac2',flag='tf',bins='shape',fractional='bin',save=True)
# plot_shape.shape_class_bar('_new/_total_bar_shape_frac_tot_err',flag=['tf','ps','merger'],bins='shape',fractional='None',save=True,err_subset=morph_field,err_subset_var='S821',error_array=[0.,0.,0.,0.0,0.0])


# # plot.bar('_new/total_bar_tf_s82xerr',flag='tf',save=True,error=True,err_subset_var=morph_ID,error_array=[0.38,0.62,0.47,0.0,0.0])
# # plot.bar('_new/total_bar_tf_s82xerr2',flag='tf',save=True,error=True,err_subset_var=morph_ID,error_array=[0.47,0.47,0.72,0.0,0.0])
# plot.bar('_new/total_bar_tf_s82xerr3',flag='tf',save=True,error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.0065,0.164],[0.0655,0.105],[0.2,0.077],[0.285,0.144],[0.111,0.082],[0.0885,0.180]])

## [[0.0065,0.164],[0.0655,0.105],[0.2,0.077],[0.285,0.144],[0.111,0.082],[0.0885,0.180]] 
# plot.bar('_new/total_bar_frac_all_checkerr2',flag=['tf','merger'],save=True,fractional=True,error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]])
# plot.bar('_new/total_bar_all_checkerr3',flag=['tf','ps','merger'],save=True,fractional=False,error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]])

# plot.bar('_new/total_bar_tf',flag='tf',save=True,error=False,err_subset=morph_field,err_subset_var='S821',error_array=[0.38,0.62,0.47,0.0,0.0])

# plot.bar('_new/total_bar_tf_s82x',flag='tf',save=True)
# plot.bar('_new/total_bar_ps',flag='PS',save=True)
# plot.bar('_new/total_bar_merg',flag='merger',save=True)
# plot.bar_3bins('_new/total_bar_zbin',save=True,var=sed_z,lim=[0.4,0.8],var_name='z',flag='tf')



# plot.bar_3bins('_new/total_bar_zbin_frac_all2',save=True,var=sed_z,lim=[0.4,0.8],fractional='bin',flag=['tf','merger'],var_name=r'z',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=sed_id)
# plot.bar_3bins('_new/total_bar_zbin_all2',save=True,var=sed_z,lim=[0.4,0.8],fractional='None',flag=['tf','merger'],var_name=r'z',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=sed_id)

# plot.bar_3bins('_final/total_bar_Lxbin_frac_all2',save=True,var=sed_Lx,lim=[43.75,44.5],var_name=r'$L_{\rm X}$',flag=['tf','merger'],fractional='bin',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=sed_id)
# plot.bar_3bins('_final/total_bar_Lxbin_all2',save=True,var=sed_Lx,lim=[43.75,44.5],var_name=r'$L_{\rm X}$',fractional='None',flag=['tf','merger'],error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=sed_id)

# plot.bar_3bins('_final/total_bar_Lagn_frac_all',save=True,var=np.log10(cigale_Lagn),lim=[44.5,45.5],fractional='bin',flag=['tf','merger'],var_name=r'$L_{\rm AGN}$',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))
# plot.bar_3bins('_final/total_bar_Lagn_all',save=True,var=np.log10(cigale_Lagn),lim=[44.5,45.5],fractional='None',flag=['tf','merger'],var_name=r'$L_{\rm AGN}$',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))

# plot.bar_3bins('_final/total_bar_Mstar_frac_all',save=True,var=np.log10(cigale_m),lim=[10.25,10.75],var_name=r'log $M_\star$',flag=['tf','merger'],fractional='bin',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))
# plot.bar_3bins('_final/total_bar_Mstar_all',save=True,var=np.log10(cigale_m),lim=[10.25,10.75],var_name=r'log $M_\star$',fractional='None',flag=['tf','merger'],error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))

# plot.bar_3bins('_final/total_bar_SFR_frac_all',save=True,var=np.log10(cigale_sfr),lim=[0,1],var_name=r'log SFR',flag=['tf','merger'],fractional='bin',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))
# plot.bar_3bins('_final/total_bar_SFR_all',save=True,var=np.log10(cigale_sfr),lim=[0,1],var_name=r'log SFR',fractional='None',flag=['tf','merger'],error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))

# plot.bar_3bins('_final/total_bar_LagnFIR_frac_all',save=True,var=np.log10(cigale_Lagn_fir),lim=[43.5,44.5],var_name=r'$L_{\rm FIR, \, AGN}$',flag=['tf','merger'],fractional='bin',error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))
# plot.bar_3bins('_final/total_bar_LagnFIR_all',save=True,var=np.log10(cigale_Lagn_fir),lim=[43.5,44.5],var_name=r'$L_{\rm FIR, \, AGN}$',fractional='None',flag=['tf','merger'],error=True,err_subset=morph_field,err_subset_var='S821',error_array=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]],ID_morph=morph_ID,ID=np.asarray(cigale_ID))


# plot.scatter_fraction('_final/frac_morph_Lx',sed_Lx,r'log $L_{X}$ [erg/s]',np.arange(42.75,46.25,0.25),xlim=[42.75,46],morph_ID=morph_ID,IDm=sed_id,save=True)
# plot.scatter_fraction('_final/frac_morph_z',sed_z,r'redshift',np.arange(0,1.3,0.1),xlim=[0,1.3],morph_ID=morph_ID,IDm=sed_id,save=True)
plot.scatter_fraction('_final/frac_morph_Lagn_err',np.log10(cigale_Lagn),r'log $L_{AGN}$ [erg/s]',np.arange(43.,47.5,0.25),xlim=[43,47.5],morph_ID=morph_ID,IDm=sed_id,save=True,subset_var='S821',err_subset=morph_field,errors=True,error_vals=[[0.4,0.165],[0.95,0.108],[0.82,0.082],[0.7,0.164],[0.63,0.088],[0.74,0.87]])
# plot.scatter_fraction('_final/frac_morph_Lfir_agn',np.log10(cigale_Lagn_fir),r'log $L_{FIR, AGN}$ [erg/s]',np.arange(42,46.25,0.25),xlim=[42,46.25],morph_ID=morph_ID,IDm=sed_id,save=True)
# plot.scatter_fraction('_final/frac_morph_Lfir',np.log10(cigale_Lfir),r'log $L_{FIR}$ [erg/s]',np.arange(42,46.5,0.25),xlim=[42,46.5],morph_ID=morph_ID,IDm=sed_id,save=True)

# plot.scatter_fraction('_final/frac_morph_Mstar',np.log10(cigale_m),r'log $M_{\star}$',np.arange(8.5,11.5,0.5),xlim=[8.5,11.5],morph_ID=morph_ID,IDm=sed_id,save=True)
# plot.scatter_fraction('_final/frac_morph_SFR',np.log10(cigale_sfr),r'log SFR',np.arange(-2,3,0.5),xlim=[-2,3],morph_ID=morph_ID,IDm=sed_id,save=True)

