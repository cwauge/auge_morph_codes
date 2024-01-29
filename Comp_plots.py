'''
Connor Auge - Created Dec. 12, 2023
Class to generate plots to compare different morphology classifications
'''

import numpy as np 
import matplotlib.pyplot as plt 
from match import match
from Morph_Plots import Plotter

def main(in_dict):
    comp_plots = Morph_Compare(in_dict)


class Morph_Compare(Plotter):

    '''
    Need a function to translate each of the variety of classifications used for different clssifiers
    '''

    def __init__(self,in_dict):
        self.in_dict = in_dict
        self.auge_keys = ['Disk','Disk-Spheroid','Spheroid','Irregular','PS','Unclassifiable','Blank','Merger_flag','TF_flag','PS_flag']

    def Jarvis_to_Auge(self):
        Jarvis_keys = list(self.in_dict.keys())


    
    def Wolf_to_Auge(self):
        Wolf_keys = list(self.in_dict.keys())



    def Candels_to_Auge(self):
        Candels_keys = list(self.in_dict.keys())

