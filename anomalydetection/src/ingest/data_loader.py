import os
import json
import glob



class DataLoader():
    """
    Recieves data paths for heartbleed bug scenario.
    """

    def __init__(self) -> None:
        pass



    TRAINING = 'training'
    VALIDATION = 'validation'
    TEST = 'test'



    # def read_res():
    # first read in one file
    path = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/training/unzipped/abundant_mcclintock_1777.res'

    # get .res and .json'
    path_json = '/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw/training/unzipped/abundant_mcclintock_1777.json'


    def get_file_name(path: str) -> str:
        
        """
            Return file name without path and extension
            Parameter:
            path (str): path of file
            Returns:
            str: file name
        """
        return os.path.splitext(os.path.basename(path))[0]



    def read_res_files(path: str, mode: str) -> list: #train default #TODO extend for vlaidation and test data

        """

        """

        if mode == 'train':
            train_res_files = glob.glob(path + f'/{TRAINING}/*.res')

            return train_res_files
        





    def read_json_files(path: str) -> list:
        
        """
        """
        
        

    def extract_res_file(path: str) -> list:
        
        """
        Extracts features which are stored in .res file for each recording
        Parameter:
        path (str): path of .res file
        Returns:
        list: list of features 
        """

        values = []
        timestamps = []
        cpu_usage = []
        memory_usage = []
        network_received = []
        newtwork_send = []
        storage_read = []
        storage_written = []

        with open(path) as f:
            for line in f:
                values.append(list(line.strip().split(',', 7)))
        # delete header row
        values.pop(0)

        for i in range(0,len(values)):
            timestamps.append(values[i][0])
            cpu_usage.append(values[i][1])
            memory_usage.append(values[i][2])
            network_received.append(values[i][3])
            newtwork_send.append(values[i][4])
            storage_read.append(values[i][5])
            storage_written.append(values[i][6])
        features = [timestamps, cpu_usage, memory_usage, network_received, newtwork_send, storage_read, storage_written]
        
        return  features

    def extract_json_file(path: str) -> list:
        
        """
        """
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        return data




            
