import numpy as np
from ShowCutouts import CutoutPlot

P = '/Users/connor_auge/Research/Disertation/morphology/'
path = [P+'cosmos_jwst/jwst_f150_cutouts_sample/',P+'visual/COSMOS/cosmos_cutouts_sample_published/',P+'/visual/COSMOS/HSC_g/arch-231213-021026/']
obj = 685399
fnames = [f'{obj}.fits',f'lid_0{obj}.fits',f'{obj}.fits']

cutplot = CutoutPlot(fnames,path,hdul_shape=[0,0,1])
cutplot.plot(1,3,'figs/Fits_comp.pdf',show=True,save=True,title=['JWST','COSMOS','HSC'],stretch=[0.01,1,0.02],figsize=[12,5])