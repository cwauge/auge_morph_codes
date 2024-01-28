'''
Connor Auge - Created Dec. 12, 2023
Class to generate plots to compare different morphology classifications
'''

import numpy as np 
import matplotlib.pyplot as plt 
from match import match
from Morph_Plots import Plotter

def main(fcomp):
    comp_plots = Morph_Compare(fcomp)


class Morph_Compare(Plotter):

    def __init__(self,fcomp):
        self.fcomp = fcomp

