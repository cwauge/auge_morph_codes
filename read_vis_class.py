'''
Connor Auge - Created Nov. 26, 2023
Class to read in visual morphology classifications from .csv file (fromatted like excel/google sheets)
'''

import numpy as np
from astropy.io import fits
from astropy.io import ascii

def main(fname):
    f = Read_File(fname)

class Read_File():
    
    def __init__(self,fname):
        self.fname = fname

