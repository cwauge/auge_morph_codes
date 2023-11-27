'''
Connor Auge - Created Nov. 26, 2023
Class to generate plots for visual morphology classifications. 
Input data will be read in from read_vis_class.py
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(classes,input_dict):
    plot = Plotter(classes,input_dict)

class Plotter():

    def __init__(self,classes,input_dict):

        self.classes = classes # classification options. Act as keys into the input dictionary
        self.dict = input_dict # input dictionary. keys are the classifications. Values are arrays in order of IDs (IDs may be included).

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

    def match_flags(self,main_class,flag,out='main'):

        loc = (main_class == 1) & (flag == 1)
        if out == 'main':
            out_array = main_class[loc]
            return out_array
        elif out == 'flag':
            out_array = flag[loc]
            return out_array
        else:
            print('options for out= paramter are    main    flag')
            return


    def hist(self):

        xlabels = self.main_classes
        xticks = np.linspace(0,21,len(xlabels))

        plt.figure(figsize=(12,12),facecolor='w')
        ax = plt.subplot(111)
        ax.set_xticks(xticks,xlabels)
        plt.xticks(rotation=30, ha='right')
        ax.bar(xticks[0],np.nansum(self.disk),color='gray')
        ax.bar(xticks[1],np.nansum(self.disk_sph),color='gray')
        ax.bar(xticks[2],np.nansum(self.sph),color='gray')
        ax.bar(xticks[3],np.nansum(self.irrg),color='gray')
        ax.bar(xticks[4],np.nansum(self.ps),color='gray')
        ax.bar(xticks[5],np.nansum(self.unc),color='gray')
        ax.bar(xticks[6],np.nansum(self.blank),color='gray')
        plt.show()





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')

    args = parser.parse_args()
    main(args.classes,args.input_dict)
