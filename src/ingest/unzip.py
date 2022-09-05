#! /usr/bin/env python3

import os 
import glob
import zipfile 
import json 
from clize import run


source = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw'

def unzip_train_data(source:str):


    """
    Unzips training data.
    Parameter:
    source (str): source path of training data
    """

    TRAINING = 'training'

    training_files = glob.glob(source + f'/{TRAINING}/*.zip')
    target = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/'+ f'{TRAINING}/unzipped'


    for training_file in training_files:
        with zipfile.ZipFile(training_file, 'r') as zip_ref:
            zip_ref.extractall(target)

    return

def unzip_test_data(source:str, behaviour:bool):
    
    
    """
    Unzips test data.
    Parameter:
    source (str): source path of test data
    behaviour (bool): If set to TRUE only the test data for the recorded normal behaviour will be accessed, 
    """

    TEST = 'test'
   

    if behaviour == True:
        NORMAL = 'normal'
        target = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/'+ f'{TEST}/{NORMAL}/unzipped'
    
        test_files = glob.glob(source + f'/{TEST}/{NORMAL}/*.zip')
        for test_file in test_files:
            with zipfile.ZipFile(test_file, 'r') as zip_ref:
                zip_ref.extractall(target)
        
    else:
        NORMAL_AND_ATTACK = 'normal_and_attack'
        target = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/' + f'{TEST}/{NORMAL_AND_ATTACK}/unzipped'
    
        test_files = glob.glob(source + f'/{TEST}/{NORMAL}/*.zip')
        for test_file in test_files:
            with zipfile.ZipFile(test_file, 'r') as zip_ref:
                zip_ref.extractall(target)

    return

def unzip_validation_data(source:str):

     
    """
    Unzips validation data.
    Parameter:
    source (str): source path of test data
    """

    VALIDATION = 'validation'
    validation_files = glob.glob(source + f'/{VALIDATION}/*.zip')
    target = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/' + f'{VALIDATION}/unzipped'

    for validation_file in validation_files:
        with zipfile.ZipFile(validation_file, 'r') as zip_ref:
            zip_ref.extractall(target)


    return

#TODO SCHÖNER MACHEN!
unzip_validation_data(source=source)
unzip_test_data(source=source, behaviour=True)
unzip_test_data(source)
#if __name__=='__main__':
#    run(unzip_train_data, unzip_test_data, unzip_validation_data)
    