import numpy as np
import pickle
import argparse

def main(fname,path='None'):
    inf = Read_Pickle(fname,path)


class Read_Pickle():

    def __init__(self,fname,path='None'):
        self.fname = fname

        if path == 'None':
            self.path = '/Users/connor_auge/Research/Disertation/morphology/galight/galight/COSMOS_pickle_output/'
        else:
            self.path = path

    
    def read(self):
        self.results = pickle.load(open(f'{self.path}{self.fname}','rb'))

    def sersic(self,component=0):
        n = self.results.final_result_galaxy[component]['n_sersic']
        return n
    
    def BtoT(self):
        data = self.results.fitting_specify_class.kwargs_data['image_data']
        noise = self.results.fitting_specify_class.kwargs_data['noise_map']
        galaxy_list = self.results.image_host_list
        galaxy_total_image = np.zeros_like(galaxy_list[0])
        for i in range(len(galaxy_list)):
            galaxy_total_image = galaxy_total_image+galaxy_list[i]
        model = galaxy_total_image
        norm_residual = (data - model)/noise
        flux_list_2d = [data, model, norm_residual]
        label_list_2d = ['data', 'model', 'normalized residual']
        flux_list_1d = [data, galaxy_list[0], galaxy_list[1]]
        label_list_1d = ['data', 'bulge', 'disk']

        BT = np.sum(galaxy_list[0])/(np.sum(galaxy_list[0])+np.sum(galaxy_list[1]))

        return BT
    
    def plot_options(self):
        print('model_plot     plot_final_galaxy_fit     plot_final_qso_fit    final_result_galaxy')

    def plot(self,plot_type,save=False):
        self.results.plot_type(save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Class to read the visual classification csv files and format them for analysis')
    parser.add_argument('fname','-f',help='file name')
    parser.add_argument('--path','-path',help='optional argument, path to input file. Default set to ./visual/classifications/')

    args = parser.parse_args()
    main(args.file,args.path)