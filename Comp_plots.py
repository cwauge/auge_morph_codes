'''
Connor Auge - Created Dec. 12, 2023
Class to generate plots to compare different morphology classifications
'''

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
from matplotlib.collections import LineCollection
import matplotlib.patheffects as PathEffects
from match import match
from Morph_Plots import Plotter
import scipy.stats

def main(auge_dict, in_dict):
    comp_plots = Morph_Compare(auge_dict, in_dict)


class Morph_Compare(Plotter):

    '''
    Need a function to translate each of the variety of classifications used for different clssifiers
    '''

    def __init__(self,auge_dict,in_dict,in_file=None):
        self.in_dict = in_dict
        self.auge_keys = list(auge_dict.keys())
        self.dict = auge_dict
        self.in_file = in_file

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

    def Jarvis_to_Auge(self):
        Jarvis_keys = list(self.in_dict.keys())
        Jarvis_values = list(self.in_dict.values())
        self.keys = Jarvis_keys
        self.values = Jarvis_values

    def Lilly_to_Auge(self):
        
        # lilly_id = np.asarray(self.in_file['ID'])
        # lilly_class = np.asarray(self.in_file['class'])

        # lilly_class[lilly_class == 'disk'] = 1
        # lilly_class[lilly_class == 'disk_sph'] = 2
        # lilly_class[lilly_class == 'sph'] = 3
        # lilly_class[lilly_class == 'irrg'] = 4
        # lilly_class[lilly_class == 'ps'] = 5

        Lilly_keys = list(self.in_dict.keys())
        Lilly_values = list(self.in_dict.values())
        self.keys = Lilly_keys
        self.values = Lilly_values

        in_disk = self.in_dict['disk']
        in_disk_sph = self.in_dict['disk_sph']
        in_sph = self.in_dict['sph']
        in_irrg = self.in_dict['irrg']
        in_ps = self.in_dict['ps']
        in_unc = np.zeros(np.shape(self.in_dict['disk']))

        in_disk_sph[in_disk_sph == 1] += 1
        in_sph[in_sph == 1] += 3
        in_irrg[in_irrg == 1] += 2
        in_ps[in_ps == 1] += 4
        in_unc[in_unc == 1] += 5

        # self.disk_sph += 1
        # self.sph += 2
        # self.irrg += 3
        # self.ps += 4
        # self.unc += 5
        # self.blank += 5
        # self.merger_f += 7
        # self.tf_f += 8
        # self.ps_f += 9

        auge_numb_array = np.array([self.disk,self.disk_sph,self.sph,self.irrg,self.ps,self.unc,self.blank],dtype=float)
        auge_numb_array[np.isnan(auge_numb_array)] = 0
        auge_numb_1d = np.sum(auge_numb_array,axis=0)

        # auge_numb_1d = np.concatenate(auge_numb_array)
        in_numb_array = np.array([in_disk,in_disk_sph,in_sph,in_irrg,in_ps,in_unc],dtype=float)
        in_numb_array[np.isnan(in_numb_array)] = 0
        in_numb_1d = np.sum(in_numb_array,axis=0)
        # in_numb_1d = np.concatenate(in_numb_array)

        return auge_numb_1d, in_numb_1d



    
    def Wolf_to_Auge(self):
        Wolf_keys = list(self.in_dict.keys())
        Wolf_values = list(self.in_dict.values())
        self.keys = Wolf_keys
        self.values = Wolf_values


        mc = []
        for i in range(len(Wolf_values[0])):
            if ~np.isnan(self.in_dict['Unclassifiable'][i]):
                mc.append(6) # unc
            
            elif ~np.isnan(self.in_dict['Disk'][i]):
                if np.isnan(self.in_dict['Sph_prom'][i]) & np.isnan(self.in_dict['Sph_notic'][i]):
                    mc.append(1) # disk
                elif ~np.isnan(self.in_dict['Sph_prom'][i]) & np.isnan(self.in_dict['Sph_notic'][i]):
                    mc.append(2) # disk sph
                elif np.isnan(self.in_dict['Sph_prom'][i]) & ~np.isnan(self.in_dict['Sph_notic'][i]):
                    mc.append(1) # disk

            elif np.isnan(self.in_dict['Disk'][i]):
                if np.isnan(self.in_dict['Sph_prom'][i]) & np.isnan(self.in_dict['Sph_notic'][i]):
                    if ~np.isnan(self.in_dict['Merger'][i]):
                        mc.append(3) # irreg
                    elif ~np.isnan(self.in_dict['ps'][i]) & np.isnan(self.in_dict['Merger'][i]):
                        mc.append(5) # ps
                    else:
                        mc.append(-99)

                elif ~np.isnan(self.in_dict['Sph_prom'][i]) & np.isnan(self.in_dict['Sph_notic'][i]):
                    mc.append(4) # sph
                elif np.isnan(self.in_dict['Sph_prom'][i]) & ~np.isnan(self.in_dict['Sph_notic'][i]):
                    mc.append(4) # sph
            else:
                mc.append(7)

        mc = np.asarray(mc,dtype=float)

        self.disk_sph += 1
        self.sph += 3
        self.irrg += 2
        self.ps += 4
        self.unc += 5
        self.blank += 5
        self.merger_f += 7
        self.tf_f += 8
        self.ps_f += 9
        # for i in range(len(self.disk)):
            # print(self.disk[i],self.disk_sph[i],self.sph[i],self.irrg[i],self.ps[i],self.unc[i])

        auge_numb_array = np.array([self.disk,self.disk_sph,self.sph,self.irrg,self.ps,self.unc,self.blank],dtype=float)
        auge_numb_array[np.isnan(auge_numb_array)] = 0
        auge_numb_1d = np.sum(auge_numb_array,axis=0)

        return auge_numb_1d, mc

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


    def Auge_to_Auge(self):
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
        in_sph = self.in_dict['Spheroid']+3
        in_irrg = self.in_dict['Irregular']+2
        in_ps = self.in_dict['PS']+4
        in_unc = self.in_dict['Unclassifiable']+5
        in_blank = self.in_dict['Blank']+5
        # in_merger_f = self.in_dict['Merger_flag']+7
        # in_tf_f = self.in_dict['TF_flag']+8
        # in_ps_f = self.in_dict['PS_flag']+9
        self.disk_sph += 1
        self.sph += 3
        self.irrg += 2
        self.ps += 4
        self.unc += 5
        self.blank += 5
        self.merger_f += 7
        self.tf_f += 8
        self.ps_f += 9
        # for i in range(len(self.disk)):
            # print(self.disk[i],self.disk_sph[i],self.sph[i],self.irrg[i],self.ps[i],self.unc[i])

        auge_numb_array = np.array([self.disk,self.disk_sph,self.sph,self.irrg,self.ps,self.unc,self.blank],dtype=float)
        auge_numb_array[np.isnan(auge_numb_array)] = 0
        auge_numb_1d = np.sum(auge_numb_array,axis=0)

        # auge_numb_1d = np.concatenate(auge_numb_array)
        in_numb_array = np.array([in_disk,in_disk_sph,in_sph,in_irrg,in_ps,in_unc],dtype=float)
        in_numb_array[np.isnan(in_numb_array)] = 0
        in_numb_1d = np.sum(in_numb_array,axis=0)
        # in_numb_1d = np.concatenate(in_numb_array)

        return auge_numb_1d, in_numb_1d

    def Wolf_match_Lilly(self,wolf_array):
        fill_array = np.zerops(np.shape(wolf_array))
        

    def hist_comp_2D(self,savestring,x_in,y_in,xlabel='',ylabel='',match_IDs=False,IDx=None,IDy=None,
                     multi=False,x_in2=None,y_in2=None,IDx2=None,IDy2=None):

        if match_IDs:
            ix, iy = match(IDx,IDy)
            x = x_in[ix]
            y = y_in[iy]
            IDx, IDy = IDx[ix], IDy[iy]

            if multi:
                ix2, iy2 = match(IDx2,IDy2)
                x2 = x_in2[ix2]
                y2 = y_in2[iy2]

                x = np.append(x,x2)
                y = np.append(y,y2)
        else:
            x = x_in
            y = y_in

        x = x[y != 0]
        y = y[y != 0]

        xticks = [1.5,2.5,3.5,4.5,5.5,6.5]
        xlabels=['Disk','Disk-Sph','Irregular','Spheroid','PS','Unc']

        fig = plt.figure(figsize=(10,10))

        ax = fig.add_subplot(111)
        hh, xx, yy, ii = plt.hist2d(x,y,bins=np.arange(1,8))
        for i in range(len(yy)-1):
            for j in range(len(xx)-1):
                txt = ax.text(xx[j]+0.5,yy[i]+0.5,hh.T[i,j],color='w',ha='center',va='center',fontweight='bold')
                # txt = ax.text(xx[j]+0.5,yy[i]+0.5,np.round((hh.T[i,j]/np.sum(hh[j])),2),color='w',ha='center',va='center',fontweight='bold')
                txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
        ax.set_xticklabels(xlabels,fontsize=18)
        ax.set_yticklabels(xlabels,fontsize=18)
        ax.set_xticks(xticks)
        ax.set_yticks(xticks)
        plt.title(f'N = {len(x)}')
        plt.xlim(1,7)
        plt.ylim(1,7)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=35, ha='center')
        plt.yticks(rotation=35, ha='right')

        plt.colorbar()
        plt.tight_layout()
        plt.savefig(f'/Users/connor_auge/Desktop/morph_comp/{savestring}')
        plt.show()


    def hist_comp_2D_split(self,savestring,x_in,y_in,xlabel='',ylabel='',match_IDs=False,IDx=None,IDy=None,cond=False,cond_var=None,cond_lim=None):

        if match_IDs:
            ix, iy = match(IDx,IDy)
            x = x_in[ix]
            y = y_in[iy]
            IDx, IDy = IDx[ix], IDy[iy]
            cond_var_match = cond_var[ix]
        else:
            x = x_in
            y = y_in

        if cond:
            split_sample_upper = cond_var_match > cond_lim
            split_sample_lower = cond_var_match < cond_lim

            x1 = x[split_sample_lower]
            y1 = y[split_sample_lower]

            x2 = x[split_sample_upper]
            y2 = y[split_sample_upper]


        x = x[y != 0]
        y = y[y != 0]

        xticks = [1.5,2.5,3.5,4.5,5.5,6.5]
        xlabels=['Disk','Disk-Sph','Irregular','Spheroid','Point Source','Unc']

        fig = plt.figure(figsize=(18,8))
        gs = fig.add_gridspec(nrows=1,ncols=4,width_ratios=[3,0.25,3,0.25],wspace=0.35)

        ax1 = fig.add_subplot(gs[0])
        h11,x11,y11,i11 = ax1.hist2d(x1,y1,bins=np.arange(0,8))
        ax1.set_xticklabels(xlabels)
        ax1.set_yticklabels(xlabels)
        ax1.set_xticks(xticks)
        ax1.set_yticks(xticks)
        ax1.set_title(f'z < {cond_lim}')
        ax1.set_xlim(1,7)
        ax1.set_ylim(1,7)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)

        cb_ax1 = fig.add_subplot(gs[1])
        cb1 = fig.colorbar(i11, cax=cb_ax1)
        cb1.mappable.set_clim(0,5)


        ax2 = fig.add_subplot(gs[2])
        h22,x22,y22,i22 = ax2.hist2d(x2,y2,bins=np.arange(0,8))
        ax2.set_xticklabels(xlabels)
        ax2.set_yticklabels(xlabels)
        ax2.set_xticks(xticks)
        ax2.set_yticks(xticks)
        ax2.set_title(f'{cond_lim} < z')
        ax2.set_xlim(1,7)
        ax2.set_ylim(1,7)
        ax2.set_xlabel(xlabel)
        # ax2.set_ylabel(ylabel)
        
        cb_ax2 = fig.add_subplot(gs[3])
        cb2 = fig.colorbar(i22,cax=cb_ax2)
        cb2.mappable.set_clim(0,10)
        plt.savefig(f'/Users/connor_auge/Desktop/morph_comp/{savestring}')
        plt.show()






    