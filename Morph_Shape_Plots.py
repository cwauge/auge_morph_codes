'''
Connor Auge - Created Nov. 27, 2023
Class to generate plots for visual morpholgy classifications binned by SED shape. 
Input data will be read in from read_vis_class.py and fits file of main SED results
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse
from match import match
from Morph_Plots import Plotter


def main(classes,input_dict,morph_id,shape_id,shape,sed_field,morph_field):
    shape_plot = Shape_Plotter(classes,input_dict,morph_id,shape_id,shape,sed_field,morph_field)


class Shape_Plotter(Plotter):

    def __init__(self,classes,input_dict,morph_id,shape_id,shape,sed_field,morph_field):

        self.classes = classes
        self.dict = input_dict
        self.morph_id = morph_id
        self.morph_field = morph_field

        self.shape_id = shape_id
        self.shape = shape
        self.sed_field = sed_field

        self.main_classes = np.asarray([i for i in classes if 'flag' not in i])
        self.flag_classes = np.asarray([i for i in classes if 'flag' in i])

        self.ix_morph, self.iy_shape = match(self.morph_id,self.shape_id)

        self.disk = self.dict['Disk']
        self.disk_sph = self.dict['Disk-Spheroid']
        self.sph = self.dict['Spheroid']
        self.irrg = self.dict['Irregular']
        self.ps = self.dict['PS']
        self.unc = self.dict['Unclassifiable']
        self.blank = self.dict['Blank']
        self.merger_f = self.dict['Merger_flag']
        self.tf_f = self.dict['TF_flag']
        self.ps_f = self.dict['PS_flag']

        plt.rcParams['font.size'] = 21
        plt.rcParams['axes.linewidth'] = 3.5
        plt.rcParams['xtick.major.size'] = 5
        plt.rcParams['xtick.major.width'] = 4
        plt.rcParams['ytick.major.size'] = 5
        plt.rcParams['ytick.major.width'] = 4
        plt.rcParams['xtick.minor.size'] = 3.
        plt.rcParams['xtick.minor.width'] = 2.
        plt.rcParams['ytick.minor.size'] = 3.
        plt.rcParams['ytick.minor.width'] = 2.
        plt.rcParams['hatch.linewidth'] = 2.


    def match_class(self,main):
        out_array = main[self.ix_morph]   
        self.shape_match = self.shape[self.iy_shape]

        return out_array

    def shape_class_bar(self,savestring,flag='None',bins='shape',fractional='None',save=True,error=False,err_subset=None,error_array=None,err_subset_var=None):

        # Match the morphology classification arrays to the shape IDs from the match class
        disk_match     = self.match_class(self.disk)
        disk_sph_match = self.match_class(self.disk_sph)
        sph_match      = self.match_class(self.sph)
        irrg_match     = self.match_class(self.irrg)
        ps_match       = self.match_class(self.ps)
        unc_match      = self.match_class(self.unc)
        blank_match    = self.match_class(self.blank)
        tf_f_match     = self.match_class(self.tf_f)
        merg_f_match   = self.match_class(self.merger_f)
        ps_f_match     = self.match_class(self.ps_f)

        if error:
            err_scale = np.asarray(error_array)/2 # divide by 2 to lower the top of the bar to the middle of the uncertain region, error bar will then spread above and below this level. 
            if err_subset is None:
                subset = np.full(np.shape(self.disk), True)
            else:
                subset = err_subset == err_subset_var
        else:
            err_scale = np.zeros(5) # Number of classifications being plotted
            subset = np.full(np.shape(self.disk), True) 


        if bins == 'shape':
            b1 = self.shape_match == 1
            b2 = self.shape_match == 2
            b3 = self.shape_match == 3
            b4 = self.shape_match == 4
            b5 = self.shape_match == 5

        else:
            print('Invalid bins optionl. Options are:   shape')

        # Separate each classification by the 5 bins defined earlier in the function. 
        disk_b1,     disk_b2,     disk_b3,     disk_b4,    disk_b5     = disk_match[b1],     disk_match[b2],     disk_match[b3],     disk_match[b4],     disk_match[b5]
        disk_sph_b1, disk_sph_b2, disk_sph_b3, disk_sph_b4, disk_sph_b5 = disk_sph_match[b1], disk_sph_match[b2], disk_sph_match[b3], disk_sph_match[b4], disk_sph_match[b5] 
        sph_b1,      sph_b2,      sph_b3,      sph_b4,      sph_b5      = sph_match[b1],      sph_match[b2],      sph_match[b3],      sph_match[b4],      sph_match[b5]
        irrg_b1,     irrg_b2,     irrg_b3,     irrg_b4,     irrg_b5     = irrg_match[b1],     irrg_match[b2],     irrg_match[b3],     irrg_match[b4],     irrg_match[b5]
        ps_b1,       ps_b2,       ps_b3,       ps_b4,       ps_b5       = ps_match[b1],       ps_match[b2],       ps_match[b3],       ps_match[b4],       ps_match[b5]
        unc_b1,      unc_b2,      unc_b3,      unc_b4,      unc_b5      = unc_match[b1],      unc_match[b2],      unc_match[b3],      unc_match[b4],      unc_match[b5]
        blank_b1,    blank_b2,    blank_b3,    blank_b4,    blank_b5    = blank_match[b1],    blank_match[b2],    blank_match[b3],    blank_match[b4],    blank_match[b5]
        tf_f_b1,     tf_f_b2,     tf_f_b3,     tf_f_b4,     tf_f_b5     = tf_f_match[b1],     tf_f_match[b2],     tf_f_match[b3],     tf_f_match[b4],     disk_match[b5]
        merg_f_b1,   merg_f_b2,   merg_f_b3,   merg_f_b4,   merg_f_b5   = merg_f_match[b1],   merg_f_match[b2],   merg_f_match[b3],   merg_f_match[b4],   merg_f_match[b5]
        ps_f_b1,     ps_f_b2,     ps_f_b3,     ps_f_b4,     ps_f_b5     = ps_f_match[b1],     ps_f_match[b2],     ps_f_match[b3],     ps_f_match[b4],     ps_f_match[b5]
        subset_b1, subset_b2, subset_b3, subset_b4, subset_b5 = subset[b1], subset[b2], subset[b3], subset[b4], subset[b5]

        if fractional == 'bin':
            factor_b1 = len(self.shape_match[b1])
            factor_b2 = len(self.shape_match[b2])
            factor_b3 = len(self.shape_match[b3])
            factor_b4 = len(self.shape_match[b4])
            factor_b5 = len(self.shape_match[b5])

        elif fractional == 'total':
            factor_b1 = len(self.shape_match)
            factor_b2 = len(self.shape_match)
            factor_b3 = len(self.shape_match)
            factor_b4 = len(self.shape_match)
            factor_b5 = len(self.shape_match)
        
        elif fractional == 'None':
            factor_b1 = 1.0
            factor_b2 = 1.0
            factor_b3 = 1.0
            factor_b4 = 1.0
            factor_b5 = 1.0

        tf_flag_frac1 =((np.nansum(disk_b1[self.match_flags(disk_b1,tf_f_b1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,tf_f_b1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,tf_f_b1,output='loc')])+np.nansum(irrg_b1)+np.nansum(ps_b1[self.match_flags(ps_b1,tf_f_b1,output='loc')])+np.nansum(unc_b1[self.match_flags(unc_b1,tf_f_b1,output='loc')])+np.nansum(blank_b1[self.match_flags(blank_b1,tf_f_b1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1)+np.nansum(unc_b1)+np.nansum(blank_b1))*100
        tf_flag_frac2 =((np.nansum(disk_b2[self.match_flags(disk_b2,tf_f_b2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,tf_f_b2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,tf_f_b2,output='loc')])+np.nansum(irrg_b2)+np.nansum(ps_b2[self.match_flags(ps_b2,tf_f_b2,output='loc')])+np.nansum(unc_b2[self.match_flags(unc_b2,tf_f_b2,output='loc')])+np.nansum(blank_b2[self.match_flags(blank_b2,tf_f_b2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2)+np.nansum(unc_b2)+np.nansum(blank_b2))*100
        tf_flag_frac3 =((np.nansum(disk_b3[self.match_flags(disk_b3,tf_f_b3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,tf_f_b3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,tf_f_b3,output='loc')])+np.nansum(irrg_b3)+np.nansum(ps_b3[self.match_flags(ps_b3,tf_f_b3,output='loc')])+np.nansum(unc_b3[self.match_flags(unc_b3,tf_f_b3,output='loc')])+np.nansum(blank_b3[self.match_flags(blank_b3,tf_f_b3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3)+np.nansum(unc_b3)+np.nansum(blank_b3))*100
        tf_flag_frac4 =((np.nansum(disk_b4[self.match_flags(disk_b4,tf_f_b4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,tf_f_b4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,tf_f_b4,output='loc')])+np.nansum(irrg_b4)+np.nansum(ps_b4[self.match_flags(ps_b4,tf_f_b4,output='loc')])+np.nansum(unc_b4[self.match_flags(unc_b4,tf_f_b4,output='loc')])+np.nansum(blank_b4[self.match_flags(blank_b4,tf_f_b4,output='loc')])))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4)+np.nansum(unc_b4)+np.nansum(blank_b3))*100
        tf_flag_frac5 =((np.nansum(disk_b5[self.match_flags(disk_b5,tf_f_b5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,tf_f_b5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,tf_f_b5,output='loc')])+np.nansum(irrg_b5)+np.nansum(ps_b5[self.match_flags(ps_b5,tf_f_b5,output='loc')])+np.nansum(unc_b5[self.match_flags(unc_b5,tf_f_b5,output='loc')])+np.nansum(blank_b5[self.match_flags(blank_b5,tf_f_b5,output='loc')])))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5)+np.nansum(unc_b5)+np.nansum(blank_b4))*100

        ps_flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,ps_f_b1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,ps_f_b1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,ps_f_b1,output='loc')])+np.nansum(irrg_b1[self.match_flags(irrg_b1,ps_f_b1,output='loc')])+np.nansum(ps_b1[self.match_flags(ps_b1,ps_f_b1,output='loc')])+np.nansum(unc_b1[self.match_flags(unc_b1,ps_f_b1,output='loc')])+np.nansum(blank_b1[self.match_flags(blank_b1,ps_f_b1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1)+np.nansum(unc_b1)+np.nansum(blank_b1))*100
        ps_flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,ps_f_b2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,ps_f_b2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,ps_f_b2,output='loc')])+np.nansum(irrg_b2[self.match_flags(irrg_b2,ps_f_b2,output='loc')])+np.nansum(ps_b2[self.match_flags(ps_b2,ps_f_b2,output='loc')])+np.nansum(unc_b2[self.match_flags(unc_b2,ps_f_b2,output='loc')])+np.nansum(blank_b2[self.match_flags(blank_b2,ps_f_b2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2)+np.nansum(unc_b2)+np.nansum(blank_b2))*100
        ps_flag_frac3 = ((np.nansum(disk_b3[self.match_flags(disk_b3,ps_f_b3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,ps_f_b3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,ps_f_b3,output='loc')])+np.nansum(irrg_b3[self.match_flags(irrg_b3,ps_f_b3,output='loc')])+np.nansum(ps_b3[self.match_flags(ps_b3,ps_f_b3,output='loc')])+np.nansum(unc_b3[self.match_flags(unc_b3,ps_f_b3,output='loc')])+np.nansum(blank_b3[self.match_flags(blank_b3,ps_f_b3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3)+np.nansum(unc_b3)+np.nansum(blank_b3))*100
        ps_flag_frac4 = ((np.nansum(disk_b4[self.match_flags(disk_b4,ps_f_b4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,ps_f_b4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,ps_f_b4,output='loc')])+np.nansum(irrg_b4[self.match_flags(irrg_b4,ps_f_b4,output='loc')])+np.nansum(ps_b4[self.match_flags(ps_b4,ps_f_b4,output='loc')])+np.nansum(unc_b4[self.match_flags(unc_b4,ps_f_b4,output='loc')])+np.nansum(blank_b4[self.match_flags(blank_b4,ps_f_b4,output='loc')])))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4)+np.nansum(unc_b4)+np.nansum(blank_b3))*100
        ps_flag_frac5 = ((np.nansum(disk_b5[self.match_flags(disk_b5,ps_f_b5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,ps_f_b5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,ps_f_b5,output='loc')])+np.nansum(irrg_b5[self.match_flags(irrg_b5,ps_f_b5,output='loc')])+np.nansum(ps_b5[self.match_flags(ps_b5,ps_f_b5,output='loc')])+np.nansum(unc_b5[self.match_flags(unc_b5,ps_f_b5,output='loc')])+np.nansum(blank_b5[self.match_flags(blank_b5,ps_f_b5,output='loc')])))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5)+np.nansum(unc_b5)+np.nansum(blank_b4))*100

        merg_flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,merg_f_b1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,merg_f_b1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,merg_f_b1,output='loc')])+np.nansum(irrg_b1[self.match_flags(irrg_b1,merg_f_b1,output='loc')])+np.nansum(ps_b1[self.match_flags(ps_b1,merg_f_b1,output='loc')])+np.nansum(unc_b1[self.match_flags(unc_b1,merg_f_b1,output='loc')])+np.nansum(blank_b1[self.match_flags(blank_b1,merg_f_b1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1)+np.nansum(unc_b1)+np.nansum(blank_b1))*100
        merg_flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,merg_f_b2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,merg_f_b2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,merg_f_b2,output='loc')])+np.nansum(irrg_b2[self.match_flags(irrg_b2,merg_f_b2,output='loc')])+np.nansum(ps_b2[self.match_flags(ps_b2,merg_f_b2,output='loc')])+np.nansum(unc_b2[self.match_flags(unc_b2,merg_f_b2,output='loc')])+np.nansum(blank_b2[self.match_flags(blank_b2,merg_f_b2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2)+np.nansum(unc_b2)+np.nansum(blank_b2))*100
        merg_flag_frac3 = ((np.nansum(disk_b3[self.match_flags(disk_b3,merg_f_b3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,merg_f_b3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,merg_f_b3,output='loc')])+np.nansum(irrg_b3[self.match_flags(irrg_b3,merg_f_b3,output='loc')])+np.nansum(ps_b3[self.match_flags(ps_b3,merg_f_b3,output='loc')])+np.nansum(unc_b3[self.match_flags(unc_b3,merg_f_b3,output='loc')])+np.nansum(blank_b3[self.match_flags(blank_b3,merg_f_b3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3)+np.nansum(unc_b3)+np.nansum(blank_b3))*100
        merg_flag_frac4 = ((np.nansum(disk_b4[self.match_flags(disk_b4,merg_f_b4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,merg_f_b4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,merg_f_b4,output='loc')])+np.nansum(irrg_b4[self.match_flags(irrg_b4,merg_f_b4,output='loc')])+np.nansum(ps_b4[self.match_flags(ps_b4,merg_f_b4,output='loc')])+np.nansum(unc_b4[self.match_flags(unc_b4,merg_f_b4,output='loc')])+np.nansum(blank_b4[self.match_flags(blank_b4,merg_f_b4,output='loc')])))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4)+np.nansum(unc_b4)+np.nansum(blank_b3))*100
        merg_flag_frac5 = ((np.nansum(disk_b5[self.match_flags(disk_b5,merg_f_b5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,merg_f_b5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,merg_f_b5,output='loc')])+np.nansum(irrg_b5[self.match_flags(irrg_b5,merg_f_b5,output='loc')])+np.nansum(ps_b5[self.match_flags(ps_b5,merg_f_b5,output='loc')])+np.nansum(unc_b5[self.match_flags(unc_b5,merg_f_b5,output='loc')])+np.nansum(blank_b5[self.match_flags(blank_b5,merg_f_b5,output='loc')])))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5)+np.nansum(unc_b5)+np.nansum(blank_b4))*100


        # Set up figure
        fig = plt.figure(figsize=(10,20),facecolor='w')
        gs = fig.add_gridspec(nrows=5, ncols=1, left=0.1, right=0.9, top=0.99, bottom=0.075, hspace=0.05)

        xlabels = self.main_classes[:-2]
        xlabels = ['Disk','Disk-Sph','Irregular','Spheroid','PS']
        xticks = np.linspace(0,15,len(xlabels))

        ### set up subplot 1
        ax1 = fig.add_subplot(gs[0])
        ax1.set_xticks(xticks)
        ax1.set_xticklabels([])
        ax1.text(0.05, 0.82, f'N = {len(self.shape_match[b1])}', transform=ax1.transAxes)
        ax1.grid()

        # plot subplot data 
        ax1.bar(xticks[0],np.nansum(disk_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[1],np.nansum(disk_sph_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[3],np.nansum(sph_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[2],np.nansum(irrg_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[4],np.nansum(ps_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[5],np.nansum(unc_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        # # ax1.bar(xticks[6],np.nansum(blank_b1)/factor_b1,color='gray',alpha=0.75,width=1.5)


        # ax1.bar(xticks[0],np.nansum(disk_b1) + np.nansum(sph_b1[subset_b1])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[1],np.nansum(disk_sph_b1) + np.nansum(sph_b1[subset_b1])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[2],np.nansum(irrg_b1) - np.nansum(irrg_b1[subset_b1])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[3],np.nansum(sph_b1) - np.nansum(sph_b1[subset_b1])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[4],np.nansum(ps_b1) - np.nansum(ps_b1[subset_b1])*err_scale[4],color='gray',alpha=0.75,width=1.5)

        # if flag == 'tf' or flag == 'TF':
        #     ax1.bar(xticks[0],np.nansum(disk_b1[self.match_flags(disk_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
        #     ax1.bar(xticks[1],np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[2],np.nansum(irrg_b1[self.match_flags(sph_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[3],np.nansum(sph_b1)/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[4],np.nansum(ps_b1[self.match_flags(ps_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax1.bar(xticks[5],np.nansum(unc_b1[self.match_flags(unc_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax1.bar(xticks[6],np.nansum(blank_b1[self.match_flags(blank_b1,tf_f_b1,output='loc')])/factor_b1,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.text(0.05, 0.7, f'n/N = {np.round(tf_flag_frac1)}%', transform=ax1.transAxes,color='r')

        # elif flag == 'ps' or flag == 'PS':
        #     ax1.bar(xticks[0],np.nansum(disk_b1[self.match_flags(disk_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
        #     ax1.bar(xticks[1],np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[2],np.nansum(irrg_b1[self.match_flags(sph_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[3],np.nansum(sph_b1[self.match_flags(irrg_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[4],np.nansum(ps_b1[self.match_flags(ps_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[5],np.nansum(unc_b1[self.match_flags(unc_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[6],np.nansum(blank_b1[self.match_flags(blank_b1,ps_f_b1,output='loc')])/factor_b1,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.text(0.05, 0.7, f'n = {np.round(ps_flag_frac1)}', transform=ax1.transAxes,color='b')

        # elif flag == 'merger' or flag == 'Merger':
        #     ax1.bar(xticks[0],np.nansum(disk_b1[self.match_flags(disk_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
        #     ax1.bar(xticks[1],np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[2],np.nansum(irrg_b1[self.match_flags(sph_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[3],np.nansum(sph_b1[self.match_flags(irrg_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[4],np.nansum(ps_b1[self.match_flags(ps_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[5],np.nansum(unc_b1[self.match_flags(unc_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.bar(xticks[6],np.nansum(blank_b1[self.match_flags(blank_b1,merg_f_b1,output='loc')])/factor_b1,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax1.text(0.05, 0.7, f'n = {np.round(merg_flag_frac1)}', transform=ax1.transAxes,color='g')


        ### set up subplot 2
        ax2 = fig.add_subplot(gs[1])
        ax2.set_xticks(xticks)
        ax2.set_xticklabels([])
        ax2.text(0.05, 0.82, f'N = {len(self.shape_match[b2])}', transform=ax2.transAxes)
        ax2.grid()

        # plot subplot data
        ax2.bar(xticks[0],np.nansum(disk_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[1],np.nansum(disk_sph_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[3],np.nansum(sph_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[2],np.nansum(irrg_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[4],np.nansum(ps_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[5],np.nansum(unc_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[6],np.nansum(blank_b2)/factor_b2,color='gray',alpha=0.75,width=1.5)

        # ax2.bar(xticks[0],np.nansum(disk_b2) + np.nansum(sph_b2[subset_b2])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[1],np.nansum(disk_sph_b2) + np.nansum(sph_b2[subset_b2])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[2],np.nansum(irrg_b2) - np.nansum(irrg_b2[subset_b2])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[3],np.nansum(sph_b2) - np.nansum(sph_b2[subset_b2])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[4],np.nansum(ps_b2) - np.nansum(ps_b2[subset_b2])*err_scale[4],color='gray',alpha=0.75,width=1.5)




        # if flag == 'tf' or flag == 'TF':
        #     ax2.bar(xticks[0],np.nansum(disk_b2[self.match_flags(disk_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
        #     ax2.bar(xticks[1],np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[2],np.nansum(irrg_b2[self.match_flags(irrg_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[3],np.nansum(sph_b2)/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[4],np.nansum(ps_b2[self.match_flags(ps_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax2.bar(xticks[5],np.nansum(unc_b2[self.match_flags(unc_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax2.bar(xticks[6],np.nansum(blank_b2[self.match_flags(blank_b2,tf_f_b2,output='loc')])/factor_b2,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.text(0.05, 0.7, f'n/N = {np.round(tf_flag_frac2)}%', transform=ax2.transAxes,color='r')


        # elif flag == 'ps' or flag == 'PS':
        #     ax2.bar(xticks[0],np.nansum(disk_b2[self.match_flags(disk_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
        #     ax2.bar(xticks[1],np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[2],np.nansum(irrg_b2[self.match_flags(irrg_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[3],np.nansum(sph_b2[self.match_flags(sph_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[4],np.nansum(ps_b2[self.match_flags(ps_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[5],np.nansum(unc_b2[self.match_flags(unc_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[6],np.nansum(blank_b2[self.match_flags(blank_b2,ps_f_b2,output='loc')])/factor_b2,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.text(0.05, 0.7, f'n = {np.round(ps_flag_frac2)}', transform=ax2.transAxes,color='b')


        # elif flag == 'merger' or flag == 'Merger':
        #     ax2.bar(xticks[0],np.nansum(disk_b2[self.match_flags(disk_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
        #     ax2.bar(xticks[1],np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[2],np.nansum(irrg_b2[self.match_flags(irrg_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[3],np.nansum(sph_b2[self.match_flags(sph_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.bar(xticks[4],np.nansum(ps_b2[self.match_flags(ps_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax2.bar(xticks[5],np.nansum(unc_b2[self.match_flags(unc_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax2.bar(xticks[6],np.nansum(blank_b2[self.match_flags(blank_b2,merg_f_b2,output='loc')])/factor_b2,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax2.text(0.05, 0.7, f'n = {np.round(merg_flag_frac2)}', transform=ax2.transAxes,color='g')


        
        ### set up subplot 3
        ax3 = fig.add_subplot(gs[2])
        ax3.set_xticks(xticks)
        ax3.set_xticklabels([])
        ax3.text(0.05, 0.82, f'N = {len(self.shape_match[b3])}', transform=ax3.transAxes)
        ax3.grid()

        # plot subplot data
        ax3.bar(xticks[0],np.nansum(disk_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[1],np.nansum(disk_sph_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[3],np.nansum(sph_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[2],np.nansum(irrg_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[4],np.nansum(ps_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[5],np.nansum(unc_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[6],np.nansum(blank_b3)/factor_b3,color='gray',alpha=0.75,width=1.5)

        # ax3.bar(xticks[0],np.nansum(disk_b3) + np.nansum(sph_b3[subset_b3])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[1],np.nansum(disk_sph_b3) + np.nansum(sph_b3[subset_b3])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[2],np.nansum(irrg_b3) - np.nansum(irrg_b3[subset_b3])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[3],np.nansum(sph_b3) - np.nansum(sph_b3[subset_b3])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[4],np.nansum(ps_b3) - np.nansum(ps_b3[subset_b3])*err_scale[4],color='gray',alpha=0.75,width=1.5)


        # if flag == 'tf' or flag == 'TF':
        #     ax3.bar(xticks[0],np.nansum(disk_b3[self.match_flags(disk_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
        #     ax3.bar(xticks[1],np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[2],np.nansum(irrg_b3[self.match_flags(irrg_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[3],np.nansum(sph_b3)/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[4],np.nansum(ps_b3[self.match_flags(ps_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax3.bar(xticks[5],np.nansum(unc_b3[self.match_flags(unc_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax3.bar(xticks[6],np.nansum(blank_b3[self.match_flags(blank_b3,tf_f_b3,output='loc')])/factor_b3,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.text(0.05, 0.7, f'n/N = {np.round(tf_flag_frac3)}%', transform=ax3.transAxes,color='r')

        # elif flag == 'ps' or flag == 'PS':
        #     ax3.bar(xticks[0],np.nansum(disk_b3[self.match_flags(disk_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
        #     ax3.bar(xticks[1],np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[2],np.nansum(irrg_b3[self.match_flags(irrg_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[3],np.nansum(sph_b3[self.match_flags(sph_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[4],np.nansum(ps_b3[self.match_flags(ps_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[5],np.nansum(unc_b3[self.match_flags(unc_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[6],np.nansum(blank_b3[self.match_flags(blank_b3,ps_f_b3,output='loc')])/factor_b3,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.text(0.05, 0.7, f'n = {np.round(ps_flag_frac3)}', transform=ax3.transAxes,color='b')

        # elif flag == 'merger' or flag == 'Merger':
        #     ax3.bar(xticks[0],np.nansum(disk_b3[self.match_flags(disk_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
        #     ax3.bar(xticks[1],np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[2],np.nansum(irrg_b3[self.match_flags(irrg_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[3],np.nansum(sph_b3[self.match_flags(sph_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[4],np.nansum(ps_b3[self.match_flags(ps_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[5],np.nansum(unc_b3[self.match_flags(unc_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.bar(xticks[6],np.nansum(blank_b3[self.match_flags(blank_b3,merg_f_b3,output='loc')])/factor_b3,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax3.text(0.05, 0.7, f'n = {np.round(merg_flag_frac3)}', transform=ax3.transAxes,color='g')


        ### set up subplot 4
        ax4 = fig.add_subplot(gs[3])
        ax4.set_xticks(xticks)
        ax4.set_xticklabels([])
        ax4.text(0.05, 0.82, f'N = {len(self.shape_match[b4])}', transform=ax4.transAxes)
        ax4.grid()

        # plot subplot data
        ax4.bar(xticks[0],np.nansum(disk_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        ax4.bar(xticks[1],np.nansum(disk_sph_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        ax4.bar(xticks[3],np.nansum(sph_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        ax4.bar(xticks[2],np.nansum(irrg_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        ax4.bar(xticks[4],np.nansum(ps_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[5],np.nansum(unc_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[6],np.nansum(blank_b4)/factor_b4,color='gray',alpha=0.75,width=1.5)

        # ax4.bar(xticks[0],np.nansum(disk_b4) + np.nansum(sph_b4[subset_b4])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[1],np.nansum(disk_sph_b4) + np.nansum(sph_b4[subset_b4])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[2],np.nansum(irrg_b4) - np.nansum(irrg_b4[subset_b4])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[3],np.nansum(sph_b4) - np.nansum(sph_b4[subset_b4])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax4.bar(xticks[4],np.nansum(ps_b4) - np.nansum(ps_b4[subset_b4])*err_scale[4],color='gray',alpha=0.75,width=1.5)


        # if flag == 'tf' or flag == 'TF':
        #     ax4.bar(xticks[0],np.nansum(disk_b4[self.match_flags(disk_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
        #     ax4.bar(xticks[1],np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[2],np.nansum(irrg_b4[self.match_flags(irrg_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[3],np.nansum(sph_b4)/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[4],np.nansum(ps_b4[self.match_flags(ps_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax4.bar(xticks[5],np.nansum(unc_b4[self.match_flags(unc_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax4.bar(xticks[6],np.nansum(blank_b4[self.match_flags(blank_b4,tf_f_b4,output='loc')])/factor_b4,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.text(0.05, 0.7, f'n/N = {np.round(tf_flag_frac4)}%', transform=ax4.transAxes,color='r')

        # elif flag == 'ps' or flag == 'PS':
        #     ax4.bar(xticks[0],np.nansum(disk_b4[self.match_flags(disk_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
        #     ax4.bar(xticks[1],np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[2],np.nansum(irrg_b4[self.match_flags(irrg_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[3],np.nansum(sph_b4[self.match_flags(sph_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[4],np.nansum(ps_b4[self.match_flags(ps_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[5],np.nansum(unc_b4[self.match_flags(unc_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[6],np.nansum(blank_b4[self.match_flags(blank_b4,ps_f_b4,output='loc')])/factor_b4,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.text(0.05, 0.7, f'n = {np.round(ps_flag_frac4)}', transform=ax4.transAxes,color='b')

        # elif flag == 'merger' or flag == 'Merger':
        #     ax4.bar(xticks[0],np.nansum(disk_b4[self.match_flags(disk_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
        #     ax4.bar(xticks[1],np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[2],np.nansum(irrg_b4[self.match_flags(irrg_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[3],np.nansum(sph_b4[self.match_flags(sph_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[4],np.nansum(ps_b4[self.match_flags(ps_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[5],np.nansum(unc_b4[self.match_flags(unc_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.bar(xticks[6],np.nansum(blank_b4[self.match_flags(blank_b4,merg_f_b4,output='loc')])/factor_b4,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax4.text(0.05, 0.7, f'n = {np.round(merg_flag_frac4)}', transform=ax4.transAxes,color='g')



        ### set up subplot 5
        ax5 = fig.add_subplot(gs[4])
        ax5.set_xticks(xticks)
        ax5.set_xticklabels(xlabels)
        ax5.text(0.05, 0.82, f'N = {len(self.shape_match[b5])}', transform=ax5.transAxes)
        ax5.grid()

        # plot subplot data
        ax5.bar(xticks[0],np.nansum(disk_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        ax5.bar(xticks[1],np.nansum(disk_sph_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        ax5.bar(xticks[3],np.nansum(sph_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        ax5.bar(xticks[2],np.nansum(irrg_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        ax5.bar(xticks[4],np.nansum(ps_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[5],np.nansum(unc_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[6],np.nansum(blank_b5)/factor_b5,color='gray',alpha=0.75,width=1.5)

        # ax5.bar(xticks[0],np.nansum(disk_b5) + np.nansum(sph_b5[subset_b5])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[1],np.nansum(disk_sph_b5) + np.nansum(sph_b5[subset_b5])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[2],np.nansum(irrg_b5) - np.nansum(irrg_b5[subset_b5])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[3],np.nansum(sph_b5) - np.nansum(sph_b5[subset_b5])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax5.bar(xticks[4],np.nansum(ps_b5) - np.nansum(ps_b5[subset_b5])*err_scale[4],color='gray',alpha=0.75,width=1.5)


        # if flag == 'tf' or flag == 'TF':
        #     ax5.bar(xticks[0],np.nansum(disk_b5[self.match_flags(disk_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
        #     ax5.bar(xticks[1],np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[2],np.nansum(irrg_b5[self.match_flags(irrg_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[3],np.nansum(sph_b5)/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[4],np.nansum(ps_b5[self.match_flags(ps_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax5.bar(xticks[5],np.nansum(unc_b5[self.match_flags(unc_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     # ax5.bar(xticks[6],np.nansum(blank_b5[self.match_flags(blank_b5,tf_f_b5,output='loc')])/factor_b5,color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.text(0.05, 0.7, f'n/N = {np.round(tf_flag_frac5)}%', transform=ax5.transAxes,color='r')

        # elif flag == 'ps' or flag == 'PS':
        #     ax5.bar(xticks[0],np.nansum(disk_b5[self.match_flags(disk_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
        #     ax5.bar(xticks[1],np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[2],np.nansum(irrg_b5[self.match_flags(irrg_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[3],np.nansum(sph_b5[self.match_flags(sph_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[4],np.nansum(ps_b5[self.match_flags(ps_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[5],np.nansum(unc_b5[self.match_flags(unc_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[6],np.nansum(blank_b5[self.match_flags(blank_b5,ps_f_b5,output='loc')])/factor_b5,color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.text(0.05, 0.7, f'n = {np.round(ps_flag_frac5)}', transform=ax5.transAxes,color='b')

        # elif flag == 'merger' or flag == 'Merger':
        #     ax5.bar(xticks[0],np.nansum(disk_b5[self.match_flags(disk_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
        #     ax5.bar(xticks[1],np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[2],np.nansum(irrg_b5[self.match_flags(irrg_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[3],np.nansum(sph_b5[self.match_flags(sph_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[4],np.nansum(ps_b5[self.match_flags(ps_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[5],np.nansum(unc_b5[self.match_flags(unc_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.bar(xticks[6],np.nansum(blank_b5[self.match_flags(blank_b5,merg_f_b5,output='loc')])/factor_b5,color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
        #     ax5.text(0.05, 0.7, f'n = {np.round(merg_flag_frac5)}', transform=ax5.transAxes,color='g')


        for i in range(len(flag)):
            if flag[i] == 'tf' or flag[i] == 'TF':
                flag_var1 = self.tf_f[b1]
                flag_var2 = self.tf_f[b2]
                flag_var3 = self.tf_f[b3]
                flag_var4 = self.tf_f[b4]
                flag_var5 = self.tf_f[b5]

                cflag = 'r'
                label_flag = 'Tidal Features'
                nplace = 0.75

            elif flag[i] == 'ps' or flag[i] == 'PS':
                flag_var1 = self.ps_f[b1]
                flag_var2 = self.ps_f[b2]
                flag_var3 = self.ps_f[b3]
                flag_var5 = self.ps_f[b4]
                flag_var5 = self.ps_f[b5]

                cflag = 'b'
                label_flag = 'Point Source'
                nplace = 0.65

            elif flag[i] == 'merger' or flag[i] == 'Merger':
                flag_var1 = self.merger_f[b1]
                flag_var2 = self.merger_f[b2]
                flag_var3 = self.merger_f[b3]
                flag_var4 = self.merger_f[b4]
                flag_var5 = self.merger_f[b5]

                cflag = 'g'
                label_flag = 'Major Merger'
                nplace = 0.55


            if flag[i] == 'tf' or 'TF':
                flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,flag_var1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,flag_var1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,flag_var1,output='loc')])+np.nansum(irrg_b1)+np.nansum(ps_b1[self.match_flags(ps_b1,flag_var1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1))*100
                flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,flag_var2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,flag_var2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,flag_var2,output='loc')])+np.nansum(irrg_b2)+np.nansum(ps_b2[self.match_flags(ps_b2,flag_var2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2))*100
                flag_frac3 = ((np.nansum(disk_b3[self.match_flags(disk_b3,flag_var3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,flag_var3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,flag_var3,output='loc')])+np.nansum(irrg_b3)+np.nansum(ps_b3[self.match_flags(ps_b3,flag_var3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3))*100
                flag_frac4 = ((np.nansum(disk_b4[self.match_flags(disk_b4,flag_var4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,flag_var4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,flag_var4,output='loc')])+np.nansum(irrg_b4)+np.nansum(ps_b4[self.match_flags(ps_b4,flag_var4,output='loc')])))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4))*100
                flag_frac5 = ((np.nansum(disk_b5[self.match_flags(disk_b5,flag_var5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,flag_var5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,flag_var5,output='loc')])+np.nansum(irrg_b5)+np.nansum(ps_b5[self.match_flags(ps_b5,flag_var5,output='loc')])))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5))*100
            if flag[i] == 'ps' or 'PS':
                flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,flag_var1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,flag_var1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,flag_var1,output='loc')])+np.nansum(irrg_b1[self.match_flags(irrg_b1,flag_var1,output='loc')])+np.nansum(ps_b1)))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1))*100
                flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,flag_var2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,flag_var2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,flag_var2,output='loc')])+np.nansum(irrg_b2[self.match_flags(irrg_b2,flag_var2,output='loc')])+np.nansum(ps_b2)))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2))*100
                flag_frac3 = ((np.nansum(disk_b3[self.match_flags(disk_b3,flag_var3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,flag_var3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,flag_var3,output='loc')])+np.nansum(irrg_b3[self.match_flags(irrg_b3,flag_var3,output='loc')])+np.nansum(ps_b3)))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3))*100
                flag_frac4 = ((np.nansum(disk_b4[self.match_flags(disk_b4,flag_var4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,flag_var4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,flag_var4,output='loc')])+np.nansum(irrg_b4[self.match_flags(irrg_b4,flag_var4,output='loc')])+np.nansum(ps_b4)))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4))*100
                flag_frac5 = ((np.nansum(disk_b5[self.match_flags(disk_b5,flag_var5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,flag_var5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,flag_var5,output='loc')])+np.nansum(irrg_b5[self.match_flags(irrg_b5,flag_var5,output='loc')])+np.nansum(ps_b5)))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5))*100
            if flag[i] == 'merger' or 'Merger':
                flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,flag_var1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,flag_var1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,flag_var1,output='loc')])+np.nansum(irrg_b1)+np.nansum(ps_b1[self.match_flags(ps_b1,flag_var1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1))*100
                flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,flag_var2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,flag_var2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,flag_var2,output='loc')])+np.nansum(irrg_b2)+np.nansum(ps_b2[self.match_flags(ps_b2,flag_var2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2))*100
                flag_frac3 = ((np.nansum(disk_b3[self.match_flags(disk_b3,flag_var3,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,flag_var3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,flag_var3,output='loc')])+np.nansum(irrg_b3)+np.nansum(ps_b3[self.match_flags(ps_b3,flag_var3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3))*100
                flag_frac4 = ((np.nansum(disk_b4[self.match_flags(disk_b4,flag_var4,output='loc')])+np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,flag_var4,output='loc')])+np.nansum(sph_b4[self.match_flags(sph_b4,flag_var4,output='loc')])+np.nansum(irrg_b4)+np.nansum(ps_b4[self.match_flags(ps_b4,flag_var4,output='loc')])))/(np.nansum(disk_b4)+np.nansum(disk_sph_b4)+np.nansum(sph_b4)+np.nansum(irrg_b4)+np.nansum(ps_b4))*100
                flag_frac5 = ((np.nansum(disk_b5[self.match_flags(disk_b5,flag_var5,output='loc')])+np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,flag_var5,output='loc')])+np.nansum(sph_b5[self.match_flags(sph_b5,flag_var5,output='loc')])+np.nansum(irrg_b5)+np.nansum(ps_b5[self.match_flags(ps_b5,flag_var5,output='loc')])))/(np.nansum(disk_b5)+np.nansum(disk_sph_b5)+np.nansum(sph_b5)+np.nansum(irrg_b5)+np.nansum(ps_b5))*100
            # else:
            #     flag_frac1 = ((np.nansum(disk_b1[self.match_flags(disk_b1,flag_var1,output='loc')])+np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,flag_var1,output='loc')])+np.nansum(sph_b1[self.match_flags(sph_b1,flag_var1,output='loc')])+np.nansum(irrg_b1[self.match_flags(irrg_b1,flag_var1,output='loc')])+np.nansum(ps_b1[self.match_flags(ps_b1,flag_var1,output='loc')])))/(np.nansum(disk_b1)+np.nansum(disk_sph_b1)+np.nansum(sph_b1)+np.nansum(irrg_b1)+np.nansum(ps_b1))*100
            #     flag_frac2 = ((np.nansum(disk_b2[self.match_flags(disk_b2,flag_var2,output='loc')])+np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,flag_var2,output='loc')])+np.nansum(sph_b2[self.match_flags(sph_b2,flag_var2,output='loc')])+np.nansum(irrg_b2[self.match_flags(irrg_b1,flag_var1,output='loc')])+np.nansum(ps_b2[self.match_flags(ps_b2,flag_var2,output='loc')])))/(np.nansum(disk_b2)+np.nansum(disk_sph_b2)+np.nansum(sph_b2)+np.nansum(irrg_b2)+np.nansum(ps_b2))*100
            #     flag_frac3 = ((np.nansum(disk_b5[self.match_flags(disk_b5,flag_var5,output='loc')])+np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,flag_var3,output='loc')])+np.nansum(sph_b3[self.match_flags(sph_b3,flag_var3,output='loc')])+np.nansum(irrg_b3[self.match_flags(irrg_b1,flag_var1,output='loc')])+np.nansum(ps_b3[self.match_flags(ps_b3,flag_var3,output='loc')])))/(np.nansum(disk_b3)+np.nansum(disk_sph_b3)+np.nansum(sph_b3)+np.nansum(irrg_b3)+np.nansum(ps_b3))*100

            ax1.bar(xticks[0],np.nansum(disk_b1[self.match_flags(disk_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax1.bar(xticks[1],np.nansum(disk_sph_b1[self.match_flags(disk_sph_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[3],np.nansum(sph_b1[self.match_flags(sph_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                    ax1.bar(xticks[2],np.nansum(irrg_b1)/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax1.bar(xticks[4],np.nansum(ps_b1[self.match_flags(ps_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                    ax1.bar(xticks[2],np.nansum(irrg_b1[self.match_flags(irrg_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax1.bar(xticks[4],np.nansum(ps_b1)/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                    ax1.bar(xticks[4],np.nansum(ps_b1[self.match_flags(ps_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax1.bar(xticks[2],np.nansum(irrg_b1[self.match_flags(irrg_b1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.text(0.05, nplace, f'n/N = {np.round(flag_frac1)}%', transform=ax1.transAxes,color=cflag)


            ax2.bar(xticks[0],np.nansum(disk_b2[self.match_flags(disk_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax2.bar(xticks[1],np.nansum(disk_sph_b2[self.match_flags(disk_sph_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[3],np.nansum(sph_b2[self.match_flags(sph_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                    ax2.bar(xticks[2],np.nansum(irrg_b2)/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax2.bar(xticks[4],np.nansum(ps_b2[self.match_flags(ps_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                    ax2.bar(xticks[2],np.nansum(irrg_b2[self.match_flags(irrg_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax2.bar(xticks[4],np.nansum(ps_b2)/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                    ax2.bar(xticks[4],np.nansum(ps_b2[self.match_flags(ps_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax2.bar(xticks[2],np.nansum(irrg_b2[self.match_flags(irrg_b2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.text(0.05, nplace, f'n/N = {np.round(flag_frac2)}%', transform=ax2.transAxes,color=cflag)



            ax3.bar(xticks[0],np.nansum(disk_b3[self.match_flags(disk_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax3.bar(xticks[1],np.nansum(disk_sph_b3[self.match_flags(disk_sph_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.bar(xticks[3],np.nansum(sph_b3[self.match_flags(sph_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                    ax3.bar(xticks[2],np.nansum(irrg_b3)/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax3.bar(xticks[4],np.nansum(ps_b3[self.match_flags(ps_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                    ax3.bar(xticks[2],np.nansum(irrg_b3[self.match_flags(irrg_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax3.bar(xticks[4],np.nansum(ps_b3)/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                    ax3.bar(xticks[4],np.nansum(ps_b3[self.match_flags(ps_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax3.bar(xticks[2],np.nansum(irrg_b3[self.match_flags(irrg_b3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.text(0.05, nplace, f'n/N = {np.round(flag_frac3)}%', transform=ax3.transAxes,color=cflag)



            ax4.bar(xticks[0],np.nansum(disk_b4[self.match_flags(disk_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax4.bar(xticks[1],np.nansum(disk_sph_b4[self.match_flags(disk_sph_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax4.bar(xticks[3],np.nansum(sph_b4[self.match_flags(sph_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                    ax4.bar(xticks[2],np.nansum(irrg_b4)/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax4.bar(xticks[4],np.nansum(ps_b4[self.match_flags(ps_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                    ax4.bar(xticks[2],np.nansum(irrg_b4[self.match_flags(irrg_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax4.bar(xticks[4],np.nansum(ps_b4)/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                    ax4.bar(xticks[4],np.nansum(ps_b4[self.match_flags(ps_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax4.bar(xticks[2],np.nansum(irrg_b4[self.match_flags(irrg_b4,flag_var4,output='loc')])/factor_b4,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax4.text(0.05, nplace, f'n/N = {np.round(flag_frac4)}%', transform=ax4.transAxes,color=cflag)


            ax5.bar(xticks[0],np.nansum(disk_b5[self.match_flags(disk_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax5.bar(xticks[1],np.nansum(disk_sph_b5[self.match_flags(disk_sph_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax5.bar(xticks[3],np.nansum(sph_b5[self.match_flags(sph_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                    ax5.bar(xticks[2],np.nansum(irrg_b5)/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax5.bar(xticks[4],np.nansum(ps_b5[self.match_flags(ps_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                    ax5.bar(xticks[2],np.nansum(irrg_b5[self.match_flags(irrg_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax5.bar(xticks[4],np.nansum(ps_b5)/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                    ax5.bar(xticks[4],np.nansum(ps_b5[self.match_flags(ps_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                    ax5.bar(xticks[2],np.nansum(irrg_b5[self.match_flags(irrg_b5,flag_var5,output='loc')])/factor_b5,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax5.text(0.05, nplace, f'n/N = {np.round(flag_frac5)}%', transform=ax5.transAxes,color=cflag)





        ax1.legend()
   
        if fractional == 'None':
            ax1.set_ylim(0,300)    
            ax2.set_ylim(0,300)    
            ax3.set_ylim(0,300)    
            ax4.set_ylim(0,300)    
            ax5.set_ylim(0,300)
        
        elif fractional == 'bin':
            ax1.set_ylim(0,0.7)    
            ax2.set_ylim(0,0.7)    
            ax3.set_ylim(0,0.7)    
            ax4.set_ylim(0,0.7)    
            ax5.set_ylim(0,0.7)

        elif fractional == 'total':
            ax1.set_ylim(0,0.2)    
            ax2.set_ylim(0,0.2)    
            ax3.set_ylim(0,0.2)    
            ax4.set_ylim(0,0.2)    
            ax5.set_ylim(0,0.2) 

        plt.xticks(rotation=30, ha='right')
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')
    parser.add_argument('-morph_id','--mid',help='ID of morphology dictionary')
    parser.add_argument('-shape_id','--sid',help='ID of from main SED output file.')
    parser.add_argument('-shape','--shape',help='Shape of SED. 1 - 5 defined in Auge et al. 2023')

    args = parser.parse_args()
    main(args.classes,args.input_dict,args.morph_id,args.shape_id,args.shape)