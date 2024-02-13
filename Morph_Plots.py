'''
Connor Auge - Created Nov. 26, 2023
Class to generate plots for visual morphology classifications. 
Input data will be read in from read_vis_class.py
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse
import pickle

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

        plt.rcParams['font.size'] = 22
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
        

    def Full_classification(self):
        # I think I need a 1 d array for each classifier, where every index is a differnt source
        # and every value in the index is a string or number that corresponds to the classification. 
        # I currently have individual arrays for each classification now (from Plotter class)
        # and a dictionary of these same arrays for my new input class
        # Take each array and add a value to it to change each classification to it's own number
        # Then collapse or concatinate the arrays together for a single, 1-D array. 
          
        # For this to work I need a different function that will change the keys of the in_dict 
        # to match my classification scheme
        # in_disk = self.in_dict['Disk']
        # in_disk_sph = self.in_dict['Disk-Spheroid']+1
        # in_sph = self.in_dict['Spheroid']+2
        # in_irrg = self.in_dict['Irregular']+3
        # in_ps = self.in_dict['PS']+4
        # in_unc = self.in_dict['Unclassifiable']+5
        # in_blank = self.in_dict['Blank']+5
        # in_merger_f = self.in_dict['Merger_flag']+7
        # in_tf_f = self.in_dict['TF_flag']+8
        # in_ps_f = self.in_dict['PS_flag']+9
        self.disk_sph += 1
        self.sph += 2
        self.irrg += 3
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

        print('auge array')
        print(auge_numb_array)
        print(auge_numb_1d)
        print(np.shape(auge_numb_1d))
        print(auge_numb_1d[0])

        # auge_numb_1d = np.concatenate(auge_numb_array)
        # in_numb_array = np.array([in_disk,in_disk_sph,in_sph,in_irrg,in_ps,in_unc],dtype=float)
        # in_numb_array[np.isnan(in_numb_array)] = 0
        # in_numb_1d = np.sum(in_numb_array,axis=0)
        # # in_numb_1d = np.concatenate(in_numb_array)


        class_out = []
        for i in auge_numb_1d:
            if i == 1:
                class_out.append('Disk')
            if i == 2:
                class_out.append('Disk_sph')
            if i == 3:
                class_out.append('Sph')
            if i == 4:
                class_out.append('Irrg')
            if i == 5:
                class_out.append('PS')
            if i == 6:
                class_out.append('Unc')
            if i == 7:
                class_out.append('None')

        return np.asarray(class_out)


    # def class_error(self,true_dict,comp_dict):


    def bar(self,savestring,flag='None',save=True,error=False,err_subset=None,error_array=None,err_subset_var=None):
        xlabels = self.main_classes[:-2]
        xticks = np.linspace(0,15,len(xlabels))

        plt.figure(figsize=(12,12),facecolor='w')
        ax = plt.subplot(111)
        ax.set_xticks(xticks,xlabels)
        plt.xticks(rotation=25, ha='right')

        if error:
            err_scale = np.asarray(error_array)/2 # divide by 2 to lower the top of the bar to the middle of the uncertain region, error bar will then spread above and below this level. 
            if err_subset is None:
                subset = np.full(np.shape(self.disk), True)
            else:
                subset = err_subset == err_subset_var
        else:
            err_scale = np.zeros(5) # Number of classifications being plotted
            subset = np.full(np.shape(self.disk), True) 


        ax.bar(xticks[0],np.nansum(self.disk) + np.nansum(self.sph[subset])*err_scale[0],color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[1],np.nansum(self.disk_sph) + np.nansum(self.sph[subset])*err_scale[1],color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[2],np.nansum(self.sph) - np.nansum(self.sph[subset])*err_scale[2],color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[3],np.nansum(self.irrg) - np.nansum(self.irrg[subset])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[4],np.nansum(self.ps) - np.nansum(self.ps[subset])*err_scale[4],color='gray',alpha=0.75,width=1.5)

        ax.errorbar(xticks[0],np.nansum(self.disk) + np.nansum(self.sph[subset])*err_scale[0],yerr=np.nansum(self.sph[subset])*err_scale[0],fmt='o',color='k')
        ax.errorbar(xticks[1],np.nansum(self.disk_sph) + np.nansum(self.sph[subset])*err_scale[1],yerr=np.nansum(self.sph[subset])*err_scale[1],fmt='o',color='k')
        ax.errorbar(xticks[2],np.nansum(self.sph) - np.nansum(self.sph[subset])*err_scale[2],yerr=np.nansum(self.sph[subset])*err_scale[2],fmt='o',color='k')
        ax.errorbar(xticks[3],np.nansum(self.irrg) - np.nansum(self.irrg[subset])*err_scale[3],yerr=np.nansum(self.irrg[subset])*err_scale[3],fmt='o',color='k')
        ax.errorbar(xticks[4],np.nansum(self.ps) - np.nansum(self.ps[subset])*err_scale[4],yerr=np.nansum(self.ps[subset])*err_scale[4],fmt='o',color='k')
        
        # ax.bar(xticks[0],np.nansum(self.disk[subset]) + 13/2,color='gray',alpha=0.75,width=1.5)
        # ax.bar(xticks[1],np.nansum(self.disk_sph[subset]) + 11/2,color='gray',alpha=0.75,width=1.5)
        # ax.bar(xticks[2],np.nansum(self.sph[subset]) - 24/2,color='gray',alpha=0.75,width=1.5)
        # ax.bar(xticks[3],np.nansum(self.irrg[subset]) - np.nansum(self.irrg[subset])*err_scale[3],color='gray',alpha=0.75,width=1.5)
        # ax.bar(xticks[4],np.nansum(self.ps[subset]) - np.nansum(self.ps[subset])*err_scale[4],color='gray',alpha=0.75,width=1.5)

        # ax.errorbar(xticks[0],np.nansum(self.disk[subset]) + 13/2,yerr=np.nansum(self.sph[subset])*err_scale[0],fmt='o',color='k')
        # ax.errorbar(xticks[1],np.nansum(self.disk_sph[subset]) +11/2,yerr=np.nansum(self.sph[subset])*err_scale[1],fmt='o',color='k')
        # ax.errorbar(xticks[2],np.nansum(self.sph[subset]) - 24,yerr=np.nansum(self.sph[subset])*err_scale[2],fmt='o',color='k')
        # ax.errorbar(xticks[3],np.nansum(self.irrg[subset]) - np.nansum(self.irrg[subset])*err_scale[3],yerr=np.nansum(self.irrg[subset])*err_scale[3],fmt='o',color='k')
        # ax.errorbar(xticks[4],np.nansum(self.ps[subset]) - np.nansum(self.ps[subset])*err_scale[4],yerr=np.nansum(self.ps[subset])*err_scale[4],fmt='o',color='k')
        

        ax.text(0.1,0.8,f'N = {len(self.disk)}', transform=ax.transAxes)
        # ax.text(0.1,0.7,f'N = {int(np.nansum(self.disk)+np.nansum(self.disk_sph)+np.nansum(self.sph)+np.nansum(self.irrg)+np.nansum(self.ps))}', transform=ax.transAxes)


        # else:
        #     ax.bar(xticks[0],np.nansum(self.disk),color='gray',alpha=0.75,width=1.5)
        #     ax.bar(xticks[1],np.nansum(self.disk_sph),color='gray',alpha=0.75,width=1.5)
        #     ax.bar(xticks[2],np.nansum(self.sph),color='gray',alpha=0.75,width=1.5)
        #     ax.bar(xticks[3],np.nansum(self.irrg),color='gray',alpha=0.75,width=1.5)
        #     ax.bar(xticks[4],np.nansum(self.ps),color='gray',alpha=0.75,width=1.5)
        #     # ax.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        #     # ax.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        #     ax.text(0.1,0.8,f'N = {len(self.disk)}', transform=ax.transAxes)
        #     ax.text(0.1,0.7,f'N = {int(np.nansum(self.disk)+np.nansum(self.disk_sph)+np.nansum(self.sph)+np.nansum(self.irrg)+np.nansum(self.ps))}', transform=ax.transAxes)

        if flag == 'tf' or flag == 'TF':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5,label='Tidal Features')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.tf_f,output='loc')]),color='none',edgecolor='r',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()

        elif flag == 'ps' or flag == 'PS':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5,label='PS')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg[self.match_flags(self.irrg,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.ps_f,output='loc')]),color='none',edgecolor='g',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()

        elif flag == 'merger' or flag == 'Merger':
            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5,label='Major Merger')
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[2],np.nansum(self.sph[self.match_flags(self.sph,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.irrg[self.match_flags(self.irrg,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[5],np.nansum(self.unc[self.match_flags(self.unc,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            # ax.bar(xticks[6],np.nansum(self.blank[self.match_flags(self.blank,self.merger_f,output='loc')]),color='none',edgecolor='b',linewidth=2.5,alpha=0.75,width=1.5)
            plt.legend()


        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()


    def bar_3bins(self,savestring,flag='None',save=True,var=None,lim=[np.nan,np.nan],fractional='None',var_name='None'):

        disk1 = self.disk[var < lim[0]]
        disk_sph1 = self.disk_sph[var < lim[0]]
        sph1 = self.sph[var < lim[0]]
        irrg1 = self.irrg[var < lim[0]]
        ps1 = self.ps[var < lim[0]]

        disk2 = self.disk[(lim[0] < var) & (var < lim[1])]
        disk_sph2 = self.disk_sph[(lim[0] < var) & (var < lim[1])]
        sph2 = self.sph[(lim[0] < var) & (var < lim[1])]
        irrg2 = self.irrg[(lim[0] < var) & (var < lim[1])]
        ps2 = self.ps[(lim[0] < var) & (var < lim[1])]

        disk3 = self.disk[lim[1] < var]
        disk_sph3 = self.disk_sph[lim[1] < var]
        sph3 = self.sph[lim[1] < var]
        irrg3 = self.irrg[lim[1] < var]
        ps3 = self.ps[lim[1] < var]

        if fractional == 'bin':
            factor_b1 = len(var[var < lim[0]])
            factor_b2 = len(var[(lim[0] < var) & (var < lim[1])])
            factor_b3 = len(var[lim[1] < var])

            ylim = 0.4

        elif fractional == 'total':
            factor_b1 = len(var)
            factor_b2 = len(var)
            factor_b3 = len(var)
            
            ylim=0.3
        
        elif fractional == 'None':
            factor_b1 = 1.0
            factor_b2 = 1.0
            factor_b3 = 1.0

            ylim=200

        if flag == 'tf' or flag == 'TF':
            flag_var1 = self.tf_f[var < lim[0]]
            flag_var2 = self.tf_f[(lim[0] < var) & (var < lim[1])]
            flag_var3 = self.tf_f[lim[1] < var]

            cflag = 'r'
            label_flag = 'Tidal Features'

        elif flag == 'ps' or flag == 'PS':
            flag_var1 = self.ps_f[var < lim[0]]
            flag_var2 = self.ps_f[(lim[0] < var) & (var < lim[1])]
            flag_var3 = self.ps_f[lim[1] < var]

            cflag = 'b'
            label_flag = 'Point Source'

        elif flag == 'merger' or flag == 'Merger':
            flag_var1 = self.merger_f[var < lim[0]]
            flag_var2 = self.merger_f[(lim[0] < var) & (var < lim[1])]
            flag_var3 = self.merger_f[lim[1] < var]

            cflag = 'g'
            label_flag = 'Major Merger'

        if flag == 'tf' or 'TF':
            flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1)+np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
            flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2)+np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
            flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3)+np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100

        else:
            flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
            flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
            flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100


        xlabels = self.main_classes[:-2]
        xticks = np.linspace(0,15,len(xlabels))

        fig = plt.figure(figsize=(20,10),facecolor='w')
        gs = fig.add_gridspec(nrows=1,ncols=3,left=0.05,right=0.95,top=0.9,bottom=0.15)
        
        ax1 = plt.subplot(gs[0])
        ax1.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax1.bar(xticks[0],np.nansum(disk1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[1],np.nansum(disk_sph1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[2],np.nansum(sph1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[3],np.nansum(irrg1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[4],np.nansum(ps1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax1.text(0.1,0.8,f'N = {int(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))}', transform=ax1.transAxes)
        ax1.set_title(f'{var_name} < {lim[0]}')
        ax1.set_ylim(0,ylim)
        ax1.text(0.05, 0.7, f'n/N = {np.round(flag_frac1)}%', transform=ax1.transAxes,color=cflag)

        ax2 = plt.subplot(gs[1])
        ax2.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax2.bar(xticks[0],np.nansum(disk2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[1],np.nansum(disk_sph2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[2],np.nansum(sph2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[3],np.nansum(irrg2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[4],np.nansum(ps2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax2.text(0.1,0.8,f'N = {int(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))}', transform=ax2.transAxes)
        ax2.set_title(f'{lim[0]} < {var_name} < {lim[1]}')
        ax2.set_ylim(0,ylim)
        ax2.text(0.05, 0.7, f'n/N = {np.round(flag_frac2)}%', transform=ax2.transAxes,color=cflag)

        ax3 = plt.subplot(gs[2])
        ax3.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax3.bar(xticks[0],np.nansum(disk3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[1],np.nansum(disk_sph3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[2],np.nansum(sph3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[3],np.nansum(irrg3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[4],np.nansum(ps3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax3.text(0.1,0.8,f'N = {int(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))}', transform=ax3.transAxes)
        ax3.set_title(f'{lim[1]} < {var_name}')
        ax3.set_ylim(0,ylim)
        ax3.text(0.05, 0.7, f'n/N = {np.round(flag_frac3)}%', transform=ax3.transAxes,color=cflag)


        if flag != 'None':
            ax1.bar(xticks[0],np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax1.bar(xticks[1],np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[2],np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[3],np.nansum(irrg1)/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[4],np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.legend()

            ax2.bar(xticks[0],np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax2.bar(xticks[1],np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.bar(xticks[2],np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.bar(xticks[3],np.nansum(irrg2[self.match_flags(irrg2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.bar(xticks[4],np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)

            ax3.bar(xticks[0],np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax3.bar(xticks[1],np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.bar(xticks[2],np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.bar(xticks[3],np.nansum(irrg3[self.match_flags(irrg3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.bar(xticks[4],np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)

        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()


    def hist(self,savestring,x,bins=[0,1,0.1],xlim=[0,1],ylim=10,xlabel='',save=False,title=' '):

        fig = plt.figure(figsize=(8,8))
        ax = plt.subplot(111)

        plt.hist(x,bins=np.arange(bins[0],bins[1],bins[2]),color='gray')
        plt.xlabel(xlabel)
        plt.xlim(xlim[0],xlim[1])
        # plt.ylim(0,ylim)
        plt.title(title)
        
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/galight_figs/{savestring}.pdf')
        plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')

    args = parser.parse_args()
    main(args.classes,args.input_dict)
