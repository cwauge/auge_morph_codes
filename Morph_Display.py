'''
Connor Auge - Created Nov. 27, 2023
Class to display the SED from Auge et al. 2023 with the HST cutout visual morphology classification. 
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from match import match
from matplotlib.colors import LogNorm
from astropy.io import fits
from Morph_Shape_Plots import Shape_Plotter

def main(target_id,classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path):
    disp = Display(target_id,classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path)
    disp.find_fits('COSMOS',target_id)
    disp.plot(f'COSMOS/display_figs/',save=True,show=False)

class Display(Shape_Plotter):

    def __init__(self,target_id,classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path):
        self.target_id = target_id
        self.classes = classes
        self.dict = input_dict
        self.morph_id = morph_id
        self.shape_id = shape_id
        self.shape = shape
        self.x = x
        self.y = y
        self.z = z
        self.L = L

        self.path = path # Path to the directory of the .fits cutous

        self.main_classes = np.asarray([i for i in classes if 'flag' not in i])
        self.flag_classes = np.asarray([i for i in classes if 'flag' in i])


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


        plt.rcParams['font.size'] = 18
        plt.rcParams['axes.linewidth'] = 3.5
        plt.rcParams['xtick.major.size'] = 5
        plt.rcParams['xtick.major.width'] = 4
        plt.rcParams['ytick.major.size'] = 5
        plt.rcParams['ytick.major.width'] = 4
        plt.rcParams['xtick.minor.size'] = 3.
        plt.rcParams['xtick.minor.width'] = 2.
        plt.rcParams['ytick.minor.size'] = 3.
        plt.rcParams['ytick.minor.width'] = 2.
        plt.rcParams['hatch.linewidth'] = 2.5


    def find_class(self,id):
        # print(self.disk[self.morph_id == id])
        if self.disk[self.morph_id == id] == 1:
            self.classification = 'Disk'
        elif self.disk_sph[self.morph_id == id] == 1:
            self.classification = 'Disk-Spheroid'
        elif self.sph[self.morph_id == id] == 1:
            self.classification = 'Spheriod'
        elif self.irrg[self.morph_id == id] == 1:
            self.classification = 'Irregular'
        elif self.ps[self.morph_id == id] == 1:
            self.classification = 'Point Source'
        elif self.unc[self.morph_id == id] == 1:
            self.classification = 'Unclassifiable'
        elif self.blank[self.morph_id == id] == 1:
            self.classification = 'Blank'
        else:
            self.classification = 'None'
        if self.tf_f[self.morph_id == id] == 1:
            self.tf_flag = 'Tidal Feature'
        else:
            self.tf_flag = 'None'
        if self.merger_f[self.morph_id == id] == 1:
            self.mg_flag = 'Major Merger'
        else:
            self.mg_flag = 'None'
        if self.ps_f[self.morph_id == id] == 1:
            self.ps_flag = 'Point Source' 
        else:
            self.ps_flag = 'None'

        return self.classification, self.tf_flag, self.mg_flag, self.ps_flag


    def find_fits(self,field,id):
        id = np.asarray(id)
        item = os.listdir(self.path)
        if field == 'COSMOS':
            item_id = np.array([int(i[4:-5]) for i in item])

        elif field == 'GOODS-N':
            item_id = item  

        fits_name = []
        target_name = []
        out_match = []
        classification_out = []
        tf_flag_out = []
        mg_flag_out = []
        ps_flag_out = []
        for i in id:
            ind = np.where(item_id == int(i))[0]
            if len(ind) == 1:
                c,t,m,ps = self.find_class(i)
                classification_out.append(c)
                tf_flag_out.append(t)
                mg_flag_out.append(m)
                ps_flag_out.append(ps)
                fits_name.append(item[ind[0]])
                target_name.append(i)
                out_match.append('match')
            else:
                out_match.append('no match')
                classification_out.append(np.nan)
                tf_flag_out.append(np.nan)
                mg_flag_out.append(np.nan)
                ps_flag_out.append(np.nan)
                fits_name.append(np.nan)
                target_name.append(np.nan)

        self.fits_name = np.asarray(fits_name)
        self.target_name = np.asarray(target_name)
        self.check_match = np.asarray(out_match)
        self.classification_out = np.asarray(classification_out)
        self.tf_flag_out = np.asarray(tf_flag_out)
        self.mg_flag_out = np.asarray(mg_flag_out)
        self.ps_flag_out = np.asarray(ps_flag_out)

    def open_fits(self,name,data_extension=0):
        with fits.open(self.path+name) as hdul:
            self.data = hdul[data_extension].data

    
    def sed(self,Id,ax):
        ax.plot(self.x[self.shape_id == Id][0],self.y[self.shape_id == Id][0],color='b',lw=2.5)
        ax.grid()
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.text(0.1,0.875,f'SED Shape: {int(self.shape[self.shape_id == Id][0])}',transform=ax.transAxes)
        ax.text(0.1,0.8,r'log L$_{\rm X}$ = '+str(np.round(self.L[self.shape_id == Id][0],2))+'erg/s',transform=ax.transAxes)
        ax.text(0.1,0.725,f'z = {np.round(self.z[self.shape_id == Id][0],2)}',transform=ax.transAxes)
        ax.set_title(self.shape_id[self.shape_id == Id][0])

        ax.set_ylim(5E-4,2E2)
        ax.set_xlim(7E-5,700)


    def cutout(self,Id,ax):
        self.im = ax.imshow(self.data,norm=LogNorm(vmin=0.01,vmax=np.nanmax(self.data)+1))
        ax.set_title(self.morph_id[self.morph_id == Id][0])
        ax.text(-0.05,-0.125,f'Vis Class: {self.classification_out[self.morph_id == Id][0]}',transform=ax.transAxes)
        ax.text(-0.05,-0.2127,f'Flags: ',transform=ax.transAxes)
        if self.tf_flag_out[self.morph_id == Id][0] != 'None':
            ax.text(-0.05,-0.2127,f'          {self.tf_flag_out[self.morph_id == Id][0]}',transform=ax.transAxes)
        if self.mg_flag_out[self.morph_id == Id][0] != 'None':
            ax.text(-0.05,-0.2127,f'                                {self.mg_flag_out[self.morph_id == Id][0]}',transform=ax.transAxes)
        if self.ps_flag_out[self.morph_id == Id][0] != 'None':
            ax.text(-0.05,-0.2127,f'                                                          {self.ps_flag_out[self.morph_id == Id][0]}',transform=ax.transAxes)


    def make_fig(self,Id,savestring,save,show):
        fig = plt.figure(figsize=(15,10))
        gs1 = fig.add_gridspec(nrows=1,ncols=1,left=0.075,right=0.425,top=0.8,bottom=0.25)
        gs2 = fig.add_gridspec(nrows=1,ncols=2,left=0.5,right=0.9,top=0.9,bottom=0.15,wspace=0.05,width_ratios=[3,0.15])
        ax1 = fig.add_subplot(gs1[0])
        ax2 = fig.add_subplot(gs2[0])
        self.sed(Id,ax1)
        self.cutout(Id,ax2)
        cbar_ax = fig.add_subplot(gs2[:,-1:])
        fig.colorbar(self.im,cax=cbar_ax,orientation='vertical')
        plt.gca().invert_yaxis()
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/{savestring}/{Id}_display.pdf')
        if show:
            plt.show()

    def plot(self,savestring,save=False,show=False):
        for i in range(len(self.fits_name)):
            if self.check_match[i] == 'match':
                self.open_fits(self.fits_name[i])
                self.make_fig(self.target_name[i],savestring,save,show)
            else:
                continue



    




    
