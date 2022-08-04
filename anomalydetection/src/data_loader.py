# This method is adapted from the following source code: 
# https://github.com/LID-DS/LID-DS/blob/2e52f8f776b9e49ecc26707690455666d7ce0e01/dataloader/data_loader_2021.py#L205

import os 
import glob 
import zipfile 


TRAINING = 'training'
VALIDATION = 'validation'
TEST = 'test'

data_path = 'anomalydetection/data/CVE-2014-0160'

class DataLoader():

    def __init__(self) -> str:
        


    def collect_data() -> dict:


        meta_data = {
            'training': {},
            'validation': {},
            'test': {}
        }

        training_files = glob.glob(self.data_path + f'/{TRAINING}/*.zip')
        validation_files = glob.glob(self.data_path + f'/{VALIDATION}/*.zip')
        test_files = glob.glob(self.data_path + f'/{TEST}/*.zip')



                