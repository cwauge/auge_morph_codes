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

def main(classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path):
    disp = Display(classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path)


class Display(Shape_Plotter):

    def __init__(self,classes,input_dict,morph_id,shape_id,shape,x,y,z,L,path):
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


    def open_image(self,field,id):
        item = os.listdir(self.path)
        if field == 'COSMOS':
            item_id = np.array([int(i[4:-5]) for i in item])

        return item_id
    



    
