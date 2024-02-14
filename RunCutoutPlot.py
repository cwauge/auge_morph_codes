import numpy as np
from ShowCutouts import CutoutPlot

P = '/Users/connor_auge/Research/Disertation/morphology/'
path = [P+'cosmos_jwst/jwst_f150_cutouts_sample/',P+'visual/COSMOS/cosmos_cutouts_sample_published/',P+'/visual/COSMOS/HSC_g/arch-231213-021026/']
obj = 685399
fnames = [f'{obj}.fits',f'lid_0{obj}.fits',f'{obj}.fits']

cutplot = CutoutPlot(fnames,path,hdul_shape=[0,0,1])
cutplot.plot(1,3,'figs/Fits_comp',show=True,save=True,title=['JWST','HST','HSC'],stretch=[0.01,1,0.02],figsize=[12,4])



P = '/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/'
path = [P,P,P,P,P]
obj = [215929,325165,242550,268863,280576]
fnames = [f'lid_0{obj[0]}.fits',f'lid_0{obj[1]}.fits',f'lid_0{obj[2]}.fits',f'lid_0{obj[3]}.fits',f'lid_0{obj[4]}.fits']

cutplot = CutoutPlot(fnames,path,hdul_shape=[0,0,0,0,0])
cutplot.plot(1,5,'figs/Classifications',show=True,save=True,title=['Disk','Disk-Sph','Irregular','Spheroid','Point Source'],stretch=[1,1,1,1,1],figsize=[15,3])


P = '/Users/connor_auge/Research/Disertation/morphology/visual/COSMOS/cosmos_cutouts_sample_published/'
path = [P,P,P,P,P,P,P,P,P,P]
obj = [215929,325165,242550,268863,280576,
       725161,227400,310302,361363,709134]
fnames = [f'lid_0{obj[0]}.fits',f'lid_0{obj[1]}.fits',f'lid_0{obj[2]}.fits',f'lid_0{obj[3]}.fits',f'lid_0{obj[4]}.fits',f'lid_0{obj[5]}.fits',f'lid_0{obj[6]}.fits',f'lid_0{obj[7]}.fits',f'lid_0{obj[8]}.fits',f'lid_0{obj[9]}.fits']

cutplot = CutoutPlot(fnames,path,hdul_shape=[0,0,0,0,0,0,0,0,0,0])
cutplot.plot(2,5,'figs/Classifications2',show=True,save=True,title=['Disk','Disk-Sph','Irregular','Spheroid','Point Source','Disk / Tidal','Disk-Sph / Tidal','Irregular / Merger','Spheroid / Merger','Point Source / Tidal'],stretch=[1,1,1,1,1,1,1,1,1,1],figsize=[15,6])