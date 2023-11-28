'''
Connor Auge - Created Nov. 26, 2023
Class to read in visual morphology classifications from .csv file (fromatted like excel/google sheets)
'''

import numpy as np
import argparse
import pandas as pd
from astropy.io import fits
from astropy.io import ascii

def main(fname,path='None'):
    inf = Read_File(fname,path)

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
                self.fcols = hdul[1].columns
                self.fdata = hdul[1].data 

        elif type == 'csv':
            self.fdata = ascii.read(self.path+self.fname)
            self.fcols = self.data.columns

        elif type =='xlsx':
            hdul = pd.read_excel(self.path+self.fname)
            self.fnotes = hdul['Notes'].to_numpy()
            self.fID = hdul['ID'].to_numpy()
            hdul_no_notes = hdul.drop(labels='Notes',axis=1)
            hdul_short = hdul_no_notes.drop(labels='ID',axis=1)
            self.fcols = hdul_short.columns.to_numpy()
            self.fdata = hdul_short.to_numpy()

            self.fdata_long = hdul_no_notes.to_numpy()
            self.fcols_long = hdul_no_notes.columns.to_numpy()

    def columns(self,long=False):
        if long: 
            return self.fcols_long
        else:
            return self.fcols

    def data(self,long=False):
        if long: 
            return self.fdata_long
        else:
            return self.fdata
    
    def notes(self):
        return self.fnotes
    
    def IDs(self):
        return self.fID
    
    def x_to_one(self,array):
        array[array == 'x'] = 1.0
        array = np.asarray(array,dtype=float)

    def make_dict(self,keys,array,transpose=False):
        dict_out = dict.fromkeys(keys)

        if transpose:
            dict_data = array.T
        
        for i in range(len(keys)):
            dict_out[keys[i]] = dict_data[i]

        return dict_out




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to read the visual classification csv files and format them for analysis')
    parser.add_argument('fname','-f',help='file name')
    parser.add_argument('--path','-path',help='optional argument, path to input file. Default set to ./visual/classifications/')

    args = parser.parse_args()
    main(args.file,args.path)
