'''
Connor Auge - Created Nov. 26, 2023
Class to generate plots for visual morphology classifications. 
Input data will be read in from read_vis_class.py
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(classes,input_dict):
    plot = Plotter(classes,input_dict)

class Plotter():

    def __init__(self,classes,input_dict):

        self.classes = classes # classification options. Act as keys into the input dictionary
        self.dict = input_dict # input dictionary. keys are the classifications. Values are arrays in order of IDs (IDs may be included).



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to gnerate plots for visual morphology classifications.')
    parser.add_argument('classes','-class',help='classifications options. Also act as keys into dict')
    parser.add_argument('-input_dict','-dict',help='input dictionary. Keys are classifications. Values are arrays of nans or 1.')

    args = parser.parse_args()
    main(args.classes,args.input_dict)
