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

    def Auge_to_Auge(self):
        Auge_keys = list(self.in_dict.keys())



    def Jarvis_to_Auge(self):
        Jarvis_keys = list(self.in_dict.keys())


    
    def Wolf_to_Auge(self):
        Wolf_keys = list(self.in_dict.keys())



    def Candels_to_Auge(self):
        Candels_keys = list(self.in_dict.keys())

    def prep_dict(self):
        dict_vaues = list(self.in_dict.values()) # I don't think I need this. 
        # I think I need a 1 d array for each classifier, where every index is a differnt source
        # and every value in the index is a string or number that corresponds to the classification. 
        # I currently have individual arrays for each classification now (from Plotter class)
        # and a dictionary of these same arrays for my new input class
        # Take each array and add a value to it to change each classification to it's own number
        # Then collapse or concatinate the arrays together for a single, 1-D array. 


    def hist_comp_2D(self):

        fig = plt.figure(figsize=(9,9))
        gs = fig.add_gridspec(nrows=1,ncols=2,width_ratios=[3,0.15])

        ax = fig.add_subplot(gs[0])

    