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

    def match_flags(self,main_class,flag,out='main',output='array'):

        loc = (main_class == 1) & (flag == 1)
        if output == 'array':
            if out == 'main':
                out_array = main_class[loc]
                return out_array
            elif out == 'flag':
                out_array = flag[loc]
                return out_array
            else:
                print('options for out= paramter are    main    flag')
                return
        elif output == 'loc':
            return loc


    def bar(self,savestring,flag='None',save=True):
        xlabels = self.main_classes
        xticks = np.linspace(0,21,len(xlabels))

        plt.figure(figsize=(12,12),facecolor='w')
        ax = plt.subplot(111)
        ax.set_xticks(xticks,xlabels)
        plt.xticks(rotation=30, ha='right')
        ax.bar(xticks[0],np.nansum(self.disk),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[1],np.nansum(self.disk_sph),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[2],np.nansum(self.sph),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[3],np.nansum(self.irrg),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[4],np.nansum(self.ps),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)

        if flag == 'tf' or flag == 'TF':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg[self.match_flags(self.irrg,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.tf_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()

        elif flag == 'ps' or flag == 'PS':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg[self.match_flags(self.irrg,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.ps_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()

        elif flag == 'merger' or flag == 'Merger':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg[self.match_flags(self.irrg,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()


        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')

    args = parser.parse_args()
    main(args.classes,args.input_dict)
