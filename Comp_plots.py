'''
Connor Auge - Created Dec. 12, 2023
Class to generate plots to compare different morphology classifications
'''

import numpy as np 
import matplotlib.pyplot as plt 
from match import match
from Morph_Plots import Plotter

def main(in_dict):
    comp_plots = Morph_Compare(in_dict)


class Morph_Compare(Plotter):

    '''
    Need a function to translate each of the variety of classifications used for different clssifiers
    '''

    def __init__(self,in_dict):
        self.in_dict = in_dict
        self.auge_keys = ['Disk','Disk-Spheroid','Spheroid','Irregular','PS','Unclassifiable','Blank','Merger_flag','TF_flag','PS_flag']

    def Auge_to_Auge(self):
        Auge_keys = list(self.in_dict.keys())
        Auge_values = list(self.in_dict.values())
        self.keys = Auge_keys
        self.values = Auge_values

    def Jarvis_to_Auge(self):
        Jarvis_keys = list(self.in_dict.keys())
        Jarvis_values = list(self.in_dict.values())
        self.keys = Jarvis_keys
        self.values = Jarvis_values
    
    def Wolf_to_Auge(self):
        Wolf_keys = list(self.in_dict.keys())
        Wolf_values = list(self.in_dict.values())
        self.keys = Wolf_keys
        self.values = Wolf_values

    def Candels_to_Auge(self):
        Candels_keys = list(self.in_dict.keys())
        Candels_values = list(self.in_dict.values())
        self.keys = Candels_keys
        self.values = Candels_values

    def change_keys(self):
        for i in range(len(self.keys)):
            if 'Disk' in self.keys[i]:
                self.keys[i] == 'Disk'
                # etc. 


    def prep_dict(self):
        dict_vaues = list(self.in_dict.values()) # I don't think I need this. 
        # I think I need a 1 d array for each classifier, where every index is a differnt source
        # and every value in the index is a string or number that corresponds to the classification. 
        # I currently have individual arrays for each classification now (from Plotter class)
        # and a dictionary of these same arrays for my new input class
        # Take each array and add a value to it to change each classification to it's own number
        # Then collapse or concatinate the arrays together for a single, 1-D array. 
          
        # For this to work I need a different function that will change the keys of the in_dict 
        # to match my classification scheme
        in_disk = self.in_dict['Disk']
        in_disk_sph = self.in_dict['Disk-Spheroid']+1
        in_sph = self.in_dict['Spheroid']+2
        in_irrg = self.in_dict['Irregular']+3
        in_ps = self.in_dict['PS']+4
        in_unc = self.in_dict['Unclassifiable']+5
        in_blank = self.in_dict['Blank']+6
        in_merger_f = self.in_dict['Merger_flag']+7
        in_tf_f = self.in_dict['TF_flag']+8
        in_ps_f = self.in_dict['PS_flag']+9

        self.disk = self.disk+0
        self.disk_sph += 1
        self.sph += 2
        self.irrg += 3
        self.ps += 4
        self.unc += 5
        self.blank += 6
        self.merger_f += 7
        self.tf_f += 8
        self.ps_f += 9

        auge_numb_array = np.array([self.disk,self.disk_sph,self.sph,self.irrg,self.ps,self.unc])
        auge_numb_1d = np.sum(auge_numb_array,axis=0)

        in_numb_array = np.array([in_disk,in_disk_sph,in_sph,in_irrg,in_ps,in_unc])
        in_numb_1d = np.sum(in_numb_array)

        return auge_numb_1d, in_numb_1d





    def hist_comp_2D(self,x,y):

        fig = plt.figure(figsize=(9,9))
        # gs = fig.add_gridspec(nrows=1,ncols=2,width_ratios=[3,0.15])

        ax = fig.add_subplot(gs[0])
        plt.hist2d(x,y)
        plt.colorbar()
        plt.show()

        # cax = fig.add_subplot(gs[1])



    