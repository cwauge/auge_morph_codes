'''
Connor Auge - Created Nov. 26, 2023
Class to generate plots for visual morphology classifications. 
Input data will be read in from read_vis_class.py
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse
import pickle
from match import match

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
            elif i == 2:
                class_out.append('Disk_sph')
            elif i == 4:
                class_out.append('Sph')
            elif i == 3:
                class_out.append('Irrg')
            elif i == 5:
                class_out.append('PS')
            elif i == 6:
                class_out.append('Unc')
            elif i == 7:
                class_out.append('None')

            else:
                class_out.append('None')

        

        return np.asarray(class_out)


    # def class_error(self,true_dict,comp_dict):


    def bar(self,savestring,flag='None',save=True,error=False,err_subset=None,error_array=None,err_subset_var=None,fractional=False):
        xlabels = self.main_classes[:-2]
        xticks = np.linspace(0,15,len(xlabels))
        xlabels = ['Disk','Disk-Sph','Irregular','Spheroid','PS']

        if fractional:
            frac = len(self.disk)
            # frac = 305
            ymax = 0.7
            nplace_tot = 0.85
        else:
            frac = 1
            ymax = np.nansum(self.sph)+0.15*np.nansum(self.sph)
            nplace_tot = 0.65

        if error:
            err_scale = np.asarray(error_array) # divide by 2 to lower the top of the bar to the middle of the uncertain region, error bar will then spread above and below this level. 
            if err_subset is None:
                subset = np.full(np.shape(self.disk), True)
            else:
                subset = err_subset == err_subset_var
        else:
            err_scale = np.zeros(5) # Number of classifications being plotted
            subset = np.full(np.shape(self.disk), True) 
        err_sample =  len(self.disk[subset]) 
        err_sample1 = np.nansum(self.disk[subset])
        err_sample2 = np.nansum(self.disk_sph[subset])
        err_sample3 = np.nansum(self.irrg[subset])
        err_sample4 = np.nansum(self.sph[subset])
        err_sample5 = np.nansum(self.ps[subset])
        err_sample6 = np.nansum(self.blank[subset])

        
        plt.figure(figsize=(12,12),facecolor='w')
        ax = plt.subplot(111)
        ax.set_xticks(xticks,xlabels)
        plt.xticks(rotation=25, ha='right')

        ax.bar(xticks[0],np.nansum(self.disk)/frac,color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[1],np.nansum(self.disk_sph)/frac,color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[2],np.nansum(self.irrg)/frac,color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[3],np.nansum(self.sph)/frac,color='gray',alpha=0.75,width=1.5)
        ax.bar(xticks[4],np.nansum(self.ps)/frac,color='gray',alpha=0.75,width=1.5)

        if error:
            yerr1 = [[err_sample1/frac*err_scale[0][0]],[err_sample/frac*err_scale[0][1]]]
            yerr2 = [[err_sample2/frac*err_scale[1][0]],[err_sample/frac*err_scale[1][1]]]
            yerr3 = [[err_sample3/frac*err_scale[2][0]],[err_sample/frac*err_scale[2][1]]]
            yerr4 = [[err_sample4/frac*err_scale[3][0]],[err_sample/frac*err_scale[3][1]]]
            yerr5 = [[err_sample5/frac*err_scale[4][0]],[err_sample/frac*err_scale[4][1]]]
            yerr6 = [[err_sample6/frac*err_scale[5][0]],[err_sample/frac*err_scale[5][1]]]

            ax.errorbar(xticks[0],np.nansum(self.disk)/frac,yerr=yerr1,fmt='o',color='k')
            ax.errorbar(xticks[1],np.nansum(self.disk_sph)/frac,yerr=yerr2,fmt='o',color='k')
            ax.errorbar(xticks[2],np.nansum(self.irrg)/frac,yerr=yerr3,fmt='o',color='k')
            ax.errorbar(xticks[3],np.nansum(self.sph)/frac,yerr=yerr4,fmt='o',color='k')
            ax.errorbar(xticks[4],np.nansum(self.ps)/frac,yerr=yerr5,fmt='o',color='k')
        

        ax.text(0.025,nplace_tot,f'N = {len(self.disk)}', transform=ax.transAxes)

        for i in range(len(flag)):
            if flag[i] == 'tf' or flag[i] == 'TF':
                flag_var = self.tf_f
                cflag = 'r'
                label_flag = 'Tidal Features'
                nplace = 0.8
                flag_frac = ((np.nansum(self.disk[self.match_flags(self.disk,flag_var,output='loc')])+np.nansum(self.disk_sph[self.match_flags(self.disk_sph,flag_var,output='loc')])+np.nansum(self.sph[self.match_flags(self.sph,flag_var,output='loc')])+np.nansum(self.irrg)+np.nansum(self.ps[self.match_flags(self.ps,flag_var,output='loc')])+np.nansum(self.unc[self.match_flags(self.unc,flag_var,output='loc')])+np.nansum(self.blank[self.match_flags(self.blank,flag_var,output='loc')])))/(np.nansum(self.disk)+np.nansum(self.disk_sph)+np.nansum(self.sph)+np.nansum(self.irrg)+np.nansum(self.ps)+np.nansum(self.unc)+np.nansum(self.blank))*100


            elif flag[i] == 'ps' or flag[i] == 'PS':
                flag_var = self.ps_f
                cflag = 'b'
                label_flag = 'Point Source'
                nplace = 0.7
                flag_frac = ((np.nansum(self.disk[self.match_flags(self.disk,flag_var,output='loc')])+np.nansum(self.disk_sph[self.match_flags(self.disk_sph,flag_var,output='loc')])+np.nansum(self.sph[self.match_flags(self.sph,flag_var,output='loc')])+np.nansum(self.irrg[self.match_flags(self.irrg,flag_var,output='loc')])+np.nansum(self.ps)+np.nansum(self.unc[self.match_flags(self.unc,flag_var,output='loc')])+np.nansum(self.blank[self.match_flags(self.blank,flag_var,output='loc')])))/(np.nansum(self.disk)+np.nansum(self.disk_sph)+np.nansum(self.sph)+np.nansum(self.irrg)+np.nansum(self.ps)+np.nansum(self.unc)+np.nansum(self.blank))*100

            elif flag[i] == 'merger' or flag[i] == 'Merger':
                flag_var = self.merger_f
                cflag = 'g'
                label_flag = 'Major Merger/Double source'
                nplace = 0.75
                flag_frac = ((np.nansum(self.disk[self.match_flags(self.disk,flag_var,output='loc')])+np.nansum(self.disk_sph[self.match_flags(self.disk_sph,flag_var,output='loc')])+np.nansum(self.sph[self.match_flags(self.sph,flag_var,output='loc')])+np.nansum(self.irrg[self.match_flags(self.irrg,flag_var,output='loc')])+np.nansum(self.ps[self.match_flags(self.ps,flag_var,output='loc')])+np.nansum(self.unc[self.match_flags(self.unc,flag_var,output='loc')])+np.nansum(self.blank[self.match_flags(self.blank,flag_var,output='loc')])))/(np.nansum(self.disk)+np.nansum(self.disk_sph)+np.nansum(self.sph)+np.nansum(self.irrg)+np.nansum(self.ps)+np.nansum(self.unc)+np.nansum(self.blank))*100

            ax.bar(xticks[0],np.nansum(self.disk[self.match_flags(self.disk,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax.bar(xticks[1],np.nansum(self.disk_sph[self.match_flags(self.disk_sph,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax.bar(xticks[3],np.nansum(self.sph[self.match_flags(self.sph,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                ax.bar(xticks[2],np.nansum(self.irrg)/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)            
                ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)

            elif flag[i] == 'ps' or flag[i] == 'PS':
                ax.bar(xticks[4],np.nansum(self.ps)/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax.bar(xticks[2],np.nansum(self.irrg[self.match_flags(self.irrg,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)            
           
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                ax.bar(xticks[2],np.nansum(self.irrg[self.match_flags(self.irrg,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)            
                ax.bar(xticks[4],np.nansum(self.ps[self.match_flags(self.ps,flag_var,output='loc')])/frac,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)

            ax.text(0.025, nplace, f'n/N = {np.round(flag_frac)}%', transform=ax.transAxes,color=cflag)
            
        plt.legend()
        plt.ylim(0,ymax)
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()


    def bar_3bins(self,savestring,flag='None',save=True,var=None,lim=[np.nan,np.nan],fractional='None',var_name='None',error=False,err_subset=None,error_array=None,err_subset_var=None,ID_match=True,ID_morph=None,ID=None):

        print('here')
        print(ID_morph)
        print(ID)

        if ID_match:
            ix, iy = match(ID_morph,ID)

            disk_match = self.disk[ix]
            disk_sph_match = self.disk_sph[ix]
            sph_match = self.sph[ix]
            irrg_match = self.irrg[ix]
            ps_match = self.ps[ix]

            tf_f_match = self.tf_f[ix]
            ps_f_match = self.ps_f[ix]
            merger_f_match = self.merger_f[ix]
            
            var = var[iy]
            err_subset = err_subset[iy]


        disk1 = disk_match[var < lim[0]]
        disk_sph1 = disk_sph_match[var < lim[0]]
        sph1 = sph_match[var < lim[0]]
        irrg1 = irrg_match[var < lim[0]]
        ps1 = ps_match[var < lim[0]]

        disk2 = disk_match[(lim[0] < var) & (var < lim[1])]
        disk_sph2 = disk_sph_match[(lim[0] < var) & (var < lim[1])]
        sph2 = sph_match[(lim[0] < var) & (var < lim[1])]
        irrg2 = irrg_match[(lim[0] < var) & (var < lim[1])]
        ps2 = ps_match[(lim[0] < var) & (var < lim[1])]

        disk3 = disk_match[lim[1] < var]
        disk_sph3 = disk_sph_match[lim[1] < var]
        sph3 = sph_match[lim[1] < var]
        irrg3 = irrg_match[lim[1] < var]
        ps3 = ps_match[lim[1] < var]

        if fractional == 'bin':
            factor_b1 = len(var[var < lim[0]])
            factor_b2 = len(var[(lim[0] < var) & (var < lim[1])])
            factor_b3 = len(var[lim[1] < var])

            ylim = 0.5

        elif fractional == 'total':
            factor_b1 = len(var)
            factor_b2 = len(var)
            factor_b3 = len(var)
            
            ylim=0.3
        
        elif fractional == 'None':
            factor_b1 = 1.0
            factor_b2 = 1.0
            factor_b3 = 1.0

            ylim=225

        if error:
            err_scale = np.asarray(error_array) # divide by 2 to lower the top of the bar to the middle of the uncertain region, error bar will then spread above and below this level. 
            if err_subset is None:
                subset_b1 = np.full(np.shape(disk1), True)
                subset_b2 = np.full(np.shape(disk2), True)
                subset_b3 = np.full(np.shape(disk3), True)
            else:
                subset_b1 = err_subset[var < lim[0]] == err_subset_var
                subset_b2 = err_subset[(lim[0] < var) & (var < lim[1])] == err_subset_var
                subset_b3 = err_subset[lim[1] < var] == err_subset_var
        else:
            err_scale = np.zeros(5) # Number of classifications being plotted
            subset_b1 = np.full(np.shape(disk1), True)
            subset_b2 = np.full(np.shape(disk2), True)
            subset_b3 = np.full(np.shape(disk3), True) 

        err_sample_b1 = len(disk1[subset_b1])
        err_sample_b2 = len(disk2[subset_b2])
        err_sample_b3 = len(disk3[subset_b3])

        err_sample_b1_1 = np.nansum(disk1[subset_b1])
        err_sample_b1_2 = np.nansum(disk_sph1[subset_b1])
        err_sample_b1_3 = np.nansum(irrg1[subset_b1])
        err_sample_b1_4 = np.nansum(sph1[subset_b1])
        err_sample_b1_5 = np.nansum(ps1[subset_b1])

        err_sample_b2_1 = np.nansum(disk2[subset_b2])
        err_sample_b2_2 = np.nansum(disk_sph2[subset_b2])
        err_sample_b2_3 = np.nansum(irrg2[subset_b2])
        err_sample_b2_4 = np.nansum(sph2[subset_b2])
        err_sample_b2_5 = np.nansum(ps2[subset_b2])

        err_sample_b3_1 = np.nansum(disk3[subset_b3])
        err_sample_b3_2 = np.nansum(disk_sph3[subset_b3])
        err_sample_b3_3 = np.nansum(irrg3[subset_b3])
        err_sample_b3_4 = np.nansum(sph3[subset_b3])
        err_sample_b3_5 = np.nansum(ps3[subset_b3])
        
        xlabels = self.main_classes[:-2]
        xlabels = ['Disk','Disk-Sph','Irregular','Spheroid','PS']
        xticks = np.linspace(0,15,len(xlabels))

        fig = plt.figure(figsize=(20,10),facecolor='w')
        gs = fig.add_gridspec(nrows=1,ncols=3,left=0.05,right=0.95,top=0.9,bottom=0.15)
        
        ax1 = plt.subplot(gs[0])
        ax1.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax1.bar(xticks[0],np.nansum(disk1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[1],np.nansum(disk_sph1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[2],np.nansum(irrg1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[3],np.nansum(sph1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        ax1.bar(xticks[4],np.nansum(ps1)/factor_b1,color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax1.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax1.text(0.05,0.9,f'N = {int(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))}', transform=ax1.transAxes)
        ax1.set_title(f'{var_name} < {lim[0]}')
        ax1.set_ylim(0,ylim)

        ax2 = plt.subplot(gs[1])
        ax2.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax2.bar(xticks[0],np.nansum(disk2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[1],np.nansum(disk_sph2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[2],np.nansum(irrg2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[3],np.nansum(sph2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        ax2.bar(xticks[4],np.nansum(ps2)/factor_b2,color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax2.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax2.text(0.05,0.9,f'N = {int(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))}', transform=ax2.transAxes)
        ax2.set_title(f'{lim[0]} < {var_name} < {lim[1]}')
        ax2.set_ylim(0,ylim)

        ax3 = plt.subplot(gs[2])
        ax3.set_xticks(xticks,xlabels,rotation=25, ha='right')
        ax3.bar(xticks[0],np.nansum(disk3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[1],np.nansum(disk_sph3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[2],np.nansum(irrg3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[3],np.nansum(sph3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        ax3.bar(xticks[4],np.nansum(ps3)/factor_b3,color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[5],np.nansum(self.unc),color='gray',alpha=0.75,width=1.5)
        # ax3.bar(xticks[6],np.nansum(self.blank),color='gray',alpha=0.75,width=1.5)
        ax3.text(0.05,0.9,f'N = {int(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))}', transform=ax3.transAxes)
        ax3.set_title(f'{lim[1]} < {var_name}')
        ax3.set_ylim(0,ylim)

        print(np.nansum(irrg1),np.nansum(irrg2),np.nansum(irrg3))
        print(err_sample_b1,err_scale[2][0],err_sample_b1*err_scale[2][0])
        print(err_sample_b2,err_scale[2][0],err_sample_b2*err_scale[2][0])
        print(err_sample_b3,err_scale[2][0],err_sample_b3*err_scale[2][0])

        if error:
            print(factor_b1)
            yerr1_b1 = [[(err_sample_b1_1/factor_b1)*err_scale[0][0]],[(err_sample_b1/factor_b1)*err_scale[0][1]]]
            yerr2_b1 = [[(err_sample_b1_2/factor_b1)*err_scale[1][0]],[(err_sample_b1/factor_b1)*err_scale[1][1]]]
            yerr3_b1 = [[(err_sample_b1_3/factor_b1)*err_scale[2][0]],[(err_sample_b1/factor_b1)*err_scale[2][1]]]
            yerr4_b1 = [[(err_sample_b1_4/factor_b1)*err_scale[3][0]],[(err_sample_b1/factor_b1)*err_scale[3][1]]]
            yerr5_b1 = [[(err_sample_b1_5/factor_b1)*err_scale[4][0]],[(err_sample_b1/factor_b1)*err_scale[4][1]]]

            yerr1_b2 = [[err_sample_b2_1/factor_b2*err_scale[0][0]],[err_sample_b2/factor_b2*err_scale[0][1]]]
            yerr2_b2 = [[err_sample_b2_2/factor_b2*err_scale[1][0]],[err_sample_b2/factor_b2*err_scale[1][1]]]
            yerr3_b2 = [[err_sample_b2_3/factor_b2*err_scale[2][0]],[err_sample_b2/factor_b2*err_scale[2][1]]]
            yerr4_b2 = [[err_sample_b2_4/factor_b2*err_scale[3][0]],[err_sample_b2/factor_b2*err_scale[3][1]]]
            yerr5_b2 = [[err_sample_b2_5/factor_b2*err_scale[4][0]],[err_sample_b2/factor_b2*err_scale[4][1]]]

            yerr1_b3 = [[err_sample_b3_1/factor_b3*err_scale[0][0]],[err_sample_b3/factor_b3*err_scale[0][1]]]
            yerr2_b3 = [[err_sample_b3_2/factor_b3*err_scale[1][0]],[err_sample_b3/factor_b3*err_scale[1][1]]]
            yerr3_b3 = [[err_sample_b3_3/factor_b3*err_scale[2][0]],[err_sample_b3/factor_b3*err_scale[2][1]]]
            yerr4_b3 = [[err_sample_b3_4/factor_b3*err_scale[3][0]],[err_sample_b3/factor_b3*err_scale[3][1]]]
            yerr5_b3 = [[err_sample_b3_5/factor_b3*err_scale[4][0]],[err_sample_b3/factor_b3*err_scale[4][1]]]

            print(yerr3_b1,yerr3_b2,yerr3_b3)

            ax1.errorbar(xticks[0],np.nansum(disk1)/factor_b1,yerr=yerr1_b1,fmt='o',color='k')
            ax1.errorbar(xticks[1],np.nansum(disk_sph1)/factor_b1,yerr=yerr2_b1,fmt='o',color='k')
            ax1.errorbar(xticks[2],np.nansum(irrg1)/factor_b1,yerr=yerr3_b1,fmt='o',color='k')
            ax1.errorbar(xticks[3],np.nansum(sph1)/factor_b1,yerr=yerr4_b1,fmt='o',color='k')
            ax1.errorbar(xticks[4],np.nansum(ps1)/factor_b1,yerr=yerr5_b1,fmt='o',color='k')

            ax2.errorbar(xticks[0],np.nansum(disk2)/factor_b2,yerr=yerr1_b2,fmt='o',color='k')
            ax2.errorbar(xticks[1],np.nansum(disk_sph2)/factor_b2,yerr=yerr2_b2,fmt='o',color='k')
            ax2.errorbar(xticks[2],np.nansum(irrg2)/factor_b2,yerr=yerr3_b2,fmt='o',color='k')
            ax2.errorbar(xticks[3],np.nansum(sph2)/factor_b2,yerr=yerr4_b2,fmt='o',color='k')
            ax2.errorbar(xticks[4],np.nansum(ps2)/factor_b2,yerr=yerr5_b2,fmt='o',color='k')

            ax3.errorbar(xticks[0],np.nansum(disk3)/factor_b3,yerr=yerr1_b3,fmt='o',color='k')
            ax3.errorbar(xticks[1],np.nansum(disk_sph3)/factor_b3,yerr=yerr2_b3,fmt='o',color='k')
            ax3.errorbar(xticks[2],np.nansum(irrg3)/factor_b3,yerr=yerr3_b3,fmt='o',color='k')
            ax3.errorbar(xticks[3],np.nansum(sph3)/factor_b3,yerr=yerr4_b3,fmt='o',color='k')
            ax3.errorbar(xticks[4],np.nansum(ps3)/factor_b3,yerr=yerr5_b3,fmt='o',color='k')

        for i in range(len(flag)):
            if flag[i] == 'tf' or flag[i] == 'TF':
                flag_var1 = tf_f_match[var < lim[0]]
                flag_var2 = tf_f_match[(lim[0] < var) & (var < lim[1])]
                flag_var3 = tf_f_match[lim[1] < var]

                cflag = 'r'
                label_flag = 'Tidal Features'
                nplace = 0.85

            elif flag[i] == 'ps' or flag[i] == 'PS':
                flag_var1 = ps_f_match[var < lim[0]]
                flag_var2 = ps_f_match[(lim[0] < var) & (var < lim[1])]
                flag_var3 = ps_f_match[lim[1] < var]

                cflag = 'b'
                label_flag = 'Point Source'
                nplace = 0.75

            elif flag[i] == 'merger' or flag[i] == 'Merger':
                flag_var1 = merger_f_match[var < lim[0]]
                flag_var2 = merger_f_match[(lim[0] < var) & (var < lim[1])]
                flag_var3 = merger_f_match[lim[1] < var]

                cflag = 'g'
                label_flag = 'Major Merger'
                nplace = 0.8

            if flag[i] == 'tf' or 'TF':
                flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1)+np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
                flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2)+np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
                flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3)+np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100
            if flag[i] == 'ps' or 'PS':
                flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps1)))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
                flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2[self.match_flags(irrg2,flag_var2,output='loc')])+np.nansum(ps2)))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
                flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3[self.match_flags(irrg3,flag_var3,output='loc')])+np.nansum(ps3)))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100

            if flag[i] == 'merger' or 'Merger':
                flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1)+np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
                flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2)+np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
                flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3)+np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100
            else:
                flag_frac1 = ((np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])+np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])+np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])+np.nansum(irrg1[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])))/(np.nansum(disk1)+np.nansum(disk_sph1)+np.nansum(sph1)+np.nansum(irrg1)+np.nansum(ps1))*100
                flag_frac2 = ((np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])+np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])+np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])+np.nansum(irrg2[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])))/(np.nansum(disk2)+np.nansum(disk_sph2)+np.nansum(sph2)+np.nansum(irrg2)+np.nansum(ps2))*100
                flag_frac3 = ((np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])+np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])+np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])+np.nansum(irrg3[self.match_flags(irrg1,flag_var1,output='loc')])+np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])))/(np.nansum(disk3)+np.nansum(disk_sph3)+np.nansum(sph3)+np.nansum(irrg3)+np.nansum(ps3))*100

            ax1.bar(xticks[0],np.nansum(disk1[self.match_flags(disk1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax1.bar(xticks[1],np.nansum(disk_sph1[self.match_flags(disk_sph1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.bar(xticks[3],np.nansum(sph1[self.match_flags(sph1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                ax1.bar(xticks[2],np.nansum(irrg1)/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax1.bar(xticks[4],np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                ax1.bar(xticks[2],np.nansum(irrg1[self.match_flags(irrg1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax1.bar(xticks[4],np.nansum(ps1)/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                ax1.bar(xticks[4],np.nansum(ps1[self.match_flags(ps1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax1.bar(xticks[2],np.nansum(irrg1[self.match_flags(irrg1,flag_var1,output='loc')])/factor_b1,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax1.text(0.05, nplace, f'n/N = {np.round(flag_frac1)}%', transform=ax1.transAxes,color=cflag)

            ax2.bar(xticks[0],np.nansum(disk2[self.match_flags(disk2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax2.bar(xticks[1],np.nansum(disk_sph2[self.match_flags(disk_sph2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.bar(xticks[3],np.nansum(sph2[self.match_flags(sph2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':
                ax2.bar(xticks[2],np.nansum(irrg2)/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax2.bar(xticks[4],np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                ax2.bar(xticks[2],np.nansum(irrg2[self.match_flags(irrg2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax2.bar(xticks[4],np.nansum(ps2)/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                ax2.bar(xticks[2],np.nansum(irrg2[self.match_flags(irrg2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax2.bar(xticks[4],np.nansum(ps2[self.match_flags(ps2,flag_var2,output='loc')])/factor_b2,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax2.text(0.05, nplace, f'n/N = {np.round(flag_frac2)}%', transform=ax2.transAxes,color=cflag)

            ax3.bar(xticks[0],np.nansum(disk3[self.match_flags(disk3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5,label=label_flag)
            ax3.bar(xticks[1],np.nansum(disk_sph3[self.match_flags(disk_sph3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            ax3.bar(xticks[3],np.nansum(sph3[self.match_flags(sph3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            if flag[i] == 'tf' or flag[i] == 'TF':    
                ax3.bar(xticks[2],np.nansum(irrg3)/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax3.bar(xticks[4],np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'ps' or flag[i] == 'PS':
                ax3.bar(xticks[2],np.nansum(irrg3[self.match_flags(irrg3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax3.bar(xticks[4],np.nansum(ps3)/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
            elif flag[i] == 'merger' or flag[i] == 'Merger':
                ax3.bar(xticks[2],np.nansum(irrg3[self.match_flags(irrg3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)
                ax3.bar(xticks[4],np.nansum(ps3[self.match_flags(ps3,flag_var3,output='loc')])/factor_b3,color='none',edgecolor=cflag,linewidth=2.5,alpha=0.75,width=1.5)   
            ax3.text(0.05, nplace, f'n/N = {np.round(flag_frac3)}%', transform=ax3.transAxes,color=cflag)

        ax1.legend(fontsize=20)
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

        ax.text(0.025,0.9,f'N = {len(x)}', transform=ax.transAxes)

        
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/galight_figs/{savestring}.pdf')
        plt.show()


    def bin_frac(self,x,val,bins,remove=False,remove_in=None):
        out_frac = []
        bin_loc = []
        for i in range(len(bins)-1):
            val_bins = val[(bins[i] < x) & (x < bins[i+1])]
            if remove:
                val_remove = remove_in[(bins[i] < x) & (x < bins[i+1])]
            else:
                val_remove = np.asarray([0])
            frac = np.nansum(val_bins)/(len(val_bins)-np.nansum(val_remove))
            out_frac.append(frac)
            bin_loc.append((bins[i]+bins[i+1])/2)

        return np.asarray(out_frac), np.asarray(bin_loc)

    def bin_frac_err(self,x,val,bins,subset=None,subset_val=None,err_array=None,remove=False,remove_in=None):
        out_err  = []
        out_frac = []
        bin_loc  = [] 

        err_scale = np.asarray(err_array)
        if subset is None:
            for i in range(len(bins)-1):
                subset = np.full(np.shape(subset_val[(bins[i] < x) & (x < bins[i+1])]),True)

        else:
            for i in range(len(bins)-1):
                val_bins = val[(bins[i] < x) & (x < bins[i+1])]
                if remove:
                    val_remove = remove_in[(bins[i] < x) & (x < bins[i+1])]
                else:
                    val_remove = np.asarray([0]) 
                subset_use = (subset[(bins[i] < x) & (x < bins[i+1])] == subset_val)
                frac = np.nansum(val_bins)/(len(val_bins)-np.nansum(val_remove))
                frac_subset = np.nansum(val_bins[subset_use])/(len(val_bins[subset_use])-np.nansum(val_remove[subset_use])) 
                len_subset = len(val_bins[subset_use])-np.nansum(val_remove[subset_use]) 
                print('low: ',frac_subset,err_scale[0])
                print('up: ',len_subset,err_scale[1])
                lowerr = frac_subset*err_scale[0]
                upper = len_subset/(len(val_bins)-np.nansum(val_remove))*err_scale[1]
                out_err.append([lowerr,upper])
                out_frac.append(frac)
                bin_loc.append((bins[i]+bins[i+1])/2)
        out_err = np.asarray(out_err)
        out_frac = np.asarray(out_frac)
        bin_loc = np.asarray(bin_loc)

        return out_frac, bin_loc, out_err

    
    def scatter_fraction(self,savestring,x,xlabel=' ',bins=np.arange(0,10,1),xlim=[0,10],ylim=[0,1.025],save=False,ID_match = True, morph_ID=None,IDm=None,flags=False,errors=False,error_vals=None,subset_var=None,err_subset=None,subplot=False,):

        ix, iy = match(morph_ID, IDm)
        disk_match = self.disk[ix]
        disk_sph_match = self.disk_sph[ix]
        irrg_match = self.irrg[ix]
        sph_match = self.sph[ix]
        ps_match = self.ps[ix]
        unc_match = self.unc[ix]

        tf_f_match = self.tf_f[ix]
        ps_f_match = self.ps_f[ix]
        merg_match = self.merger_f[ix]

        x_match = x[iy]
        err_subset = err_subset[ix]

        # disk_frac, disk_x = self.bin_frac(x_match,disk_match,bins=bins,remove=True,remove_in=unc_match)
        # disk_sph_frac, disk_sph_x = self.bin_frac(x_match,disk_sph_match,bins=bins,remove=True,remove_in=unc_match)
        # irrg_frac, irrg_x = self.bin_frac(x_match,irrg_match,bins=bins,remove=True,remove_in=unc_match)
        # sph_frac, sph_x = self.bin_frac(x_match,sph_match,bins=bins,remove=True,remove_in=unc_match)
        # ps_frac, ps_x = self.bin_frac(x_match,ps_match,bins=bins,remove=True,remove_in=unc_match)

        disk_frac, disk_x, disk_err = self.bin_frac_err(x_match,disk_match,bins=bins,remove=True,remove_in=unc_match,subset_val=subset_var,subset=err_subset,err_array=error_vals[0])
        disk_sph_frac, disk_sph_x, disk_sph_err = self.bin_frac_err(x_match,disk_sph_match,bins=bins,remove=True,remove_in=unc_match,subset_val=subset_var,subset=err_subset,err_array=error_vals[0])
        irrg_frac, irrg_x, irrg_err = self.bin_frac_err(x_match,irrg_match,bins=bins,remove=True,remove_in=unc_match,subset_val=subset_var,subset=err_subset,err_array=error_vals[0])
        sph_frac, sph_x, sph_err = self.bin_frac_err(x_match,sph_match,bins=bins,remove=True,remove_in=unc_match,subset_val=subset_var,subset=err_subset,err_array=error_vals[0])
        ps_frac, ps_x, ps_err = self.bin_frac_err(x_match,ps_match,bins=bins,remove=True,remove_in=unc_match,subset_val=subset_var,subset=err_subset,err_array=error_vals[0])

        tf_f_frac, tf_f_x = self.bin_frac(x_match,tf_f_match,bins=np.arange(43.,47.5,0.25))
        ps_f_frac, ps_f_x = self.bin_frac(x_match,ps_f_match,bins=bins)
        merg_f_frac, merg_f_x = self.bin_frac(x_match,merg_match,bins=bins)

        tot_disk_err = np.sqrt(disk_err**2 + disk_sph_err**2)

        fig = plt.figure(figsize=(12,6))
        gs = fig.add_gridspec(nrows=1,ncols=1)

        ax1 = fig.add_subplot(gs[0])

        ax1.errorbar(disk_x-0.02,disk_frac+disk_sph_frac,yerr=tot_disk_err.T,color='b',capsize=5,alpha=0.5,ls='')
        ax1.errorbar(irrg_x,irrg_frac,yerr=irrg_err.T,color='green',capsize=5,alpha=0.5,ls='')
        ax1.errorbar(sph_x+0.02,sph_frac,yerr=sph_err.T,color='red',capsize=5,alpha=0.5,ls='')
        ax1.errorbar(ps_x+0.04,ps_frac,yerr=ps_err.T,color='k',capsize=5,alpha=0.5,ls='')

        ax1.plot(disk_x-0.02,disk_frac+disk_sph_frac,'^',color='b',ms=13,label='Disk/Disk-Sph',alpha=0.85)
        # ax1.plot(disk_sph_x,disk_sph_frac,'x',color='cyan',label='Disk-Sph')
        ax1.plot(irrg_x,irrg_frac,'s',color='green',ms=13,label='Irrg',alpha=0.85)
        ax1.plot(sph_x+0.02,sph_frac,'.',color='red',ms=13,label='Sph',alpha=0.85)
        ax1.plot(ps_x+0.04,ps_frac,'*',color='k',ms=13,label='PS',alpha=0.85)
        ax1.plot(tf_f_x,tf_f_frac,color='gray',lw=6,alpha=0.5,label='tidal features flag')



        print(disk_frac[0]+disk_sph_frac[0]+irrg_frac[0]+sph_frac[0]+ps_frac[0])
        print(disk_frac[1]+disk_sph_frac[1]+irrg_frac[1]+sph_frac[1]+ps_frac[1])
        print(disk_frac[2]+disk_sph_frac[2]+irrg_frac[2]+sph_frac[2]+ps_frac[2])
        print(disk_frac[3]+disk_sph_frac[3]+irrg_frac[3]+sph_frac[3]+ps_frac[3])
        
        
        ax1.set_xlim(xlim[0],xlim[1])
        ax1.set_ylim(ylim[0],ylim[1])
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel('Fraction')
        
        plt.legend(fontsize=16)
        plt.grid()
        plt.tight_layout()

        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/figs/{savestring}.pdf')
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')

    args = parser.parse_args()
    main(args.classes,args.input_dict)
