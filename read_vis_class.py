'''
Connor Auge - Created Nov. 26, 2023
Class to read in visual morphology classifications from .csv file (fromatted like excel/google sheets)
'''

import numpy as np
import argparse
from astropy.io import fits
from astropy.io import ascii

def main(fname,path='None'):
    f = Read_File(fname,path)

class Read_File():
    
    def __init__(self,fname,path='None'):
        self.fname = fname

        if path == 'None':
            self.path = '/Users/connor_auge/Research/Disertation/morphology/visual/classifications/'
        else:
            self.path = path

    def open(self,type):
        if type == 'fits':
            with fits.open(self.path+self.fname) as hdul:
                self.cols = hdul[1].columns
                self.data = hdul[1].data 

        elif type == 'csv':
            self.data = ascii.read(self.path+self.fname)


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to read the visual classification csv files and format them for analysis')
    parser.add_argument('fname','-f',help='file name')
    parser.add_argument('--path','-path',help='optional argument, path to input file. Default set to ./visual/classifications/')

    args = parser.parse_args()
    main(args.file,args.path)
