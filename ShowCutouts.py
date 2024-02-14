'''
Connor Auge - Created Feb. 13, 2024
Class to display several fits images (HST, HSC, JWST, etc.) side by side.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.io import fits


def main(fnames,path):
    Cut_Plot = CutoutPlot(fnames,path)


class CutoutPlot():

    def __init__(self,fnames,path=None,hdul_shape=[0]):
        self.fnames = np.asarray(fnames) # a singe or list of the fits files to read and plot
        self.fshape = len(self.fnames)
        self.hdul_shape = hdul_shape
        if path is None:
            path = np.asarray(['/Users/connor_auge/Research/Disertation/morphology/visual/'])
        else:
            self.path = np.asarray(path)

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

    
    def read(self,inf,path,hdul_shape):

        with fits.open(f'{path}{inf}') as hdul:
            data = hdul[hdul_shape].data
        return data
    
        
    def plot(self,nrows=1,ncols=1,savestring=' ',show=False,save=False,title=[' '],stretch=[0.1],figsize=[8,8]):
        fig = plt.figure(figsize=(figsize[0],figsize[1]))
        gs = fig.add_gridspec(nrows=nrows,ncols=ncols,wspace=0.1,hspace=0.05,left=0.02,right=0.98,bottom=0.02,top=0.99)
        self.pull_data()
        for i in range(self.fshape):
            ax1 = fig.add_subplot(gs[i])
            self.plot_im(ax1,self.pdata[i],title=title[i],stretch=stretch[i])
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
        if save:
            plt.savefig(f'/Users/connor_auge/Research/Disertation/morphology/visual/{savestring}_fits.pdf')
        if show:
            plt.show()
            

    def pull_data(self):
        pdata = []
        for i in range(self.fshape):

            data = self.read(self.fnames[i],self.path[i],self.hdul_shape[i])
            data[data<0]=np.min(data[data>0])
            pdata.append(data)

        self.pdata = pdata

    def plot_im(self,ax,dat,title = '',stretch=0.01):
        # ax.set_title(title)
        self.im = ax.imshow(dat,norm=LogNorm(vmin=stretch,vmax=np.max(dat)),cmap='gray')
        ax.text(0.05,0.9,title,color='white',bbox=dict(facecolor='k',edgecolor='white'),transform=ax.transAxes)



        
