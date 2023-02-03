#!/usr/bin/env python
from dataloader.dataloader_factory import dataloader_factory
import pandas as pd
import numpy as np
import os
from datetime import datetime
from clize import run
    

def load(src, scenario , type, target):

    """
    Function to load .res files from selected scenario

    Parameters:
    src (str): path to data scenarios 
    type_of_data (str): resources, test or validation data files

    Returns:
    pd.Dataframe for each recording
    """
   
    dataloader = dataloader_factory(src+'/'+scenario)
    
    if type =='train':
        RAW = {
            scenario: dataloader.training_data()
        }
    if type == 'test':
        RAW = {
            scenario: dataloader.test_data()
        }
    if type == 'validation':
        RAW = {
            scenario: dataloader.validation_data(),
        }

    container_names = []
    resource_stats_l = []
    jsons = []

 
    for i in range(0, len(RAW[scenario])):
        container_names.append(RAW[scenario][i].name)
        resource_stats_l.append(RAW[scenario][i].resource_stats())
        jsons.append(RAW[scenario][i].metadata())
    
    resource_stats = {}
    for h in range(0,len(container_names)):
        resource_stats[container_names[h]] = {
                "timestamp": [resource_stats_l[h][q].timestamp_datetime() for q in range(0,len(resource_stats_l[h]))],
                "cpu_usage": [resource_stats_l[h][q].cpu_usage() for q in range(0,len(resource_stats_l[h]))],
                "memory_usage": [resource_stats_l[h][q].memory_usage() for q in range(0,len(resource_stats_l[h]))],
                "network_received": [resource_stats_l[h][q].network_received() for q in range(0,len(resource_stats_l[h]))],
                "network_send": [resource_stats_l[h][q].network_send() for q in range(0,len(resource_stats_l[h]))],
                "storage_read": [resource_stats_l[h][q].storage_read() for q in range(0,len(resource_stats_l[h]))],
                "storage_written": [resource_stats_l[h][q].storage_written() for q in range(0,len(resource_stats_l[h]))],
                "exploit": np.repeat(jsons[h]['exploit'], len(resource_stats_l[h])),
                "timestamp_container_ready": np.repeat(datetime.fromtimestamp(jsons[h]["time"]["container_ready"]["absolute"]), len(resource_stats_l[h])),
                "timestamp_warmup_end": np.repeat(datetime.fromtimestamp(jsons[h]["time"]["warmup_end"]["absolute"]), len(resource_stats_l[h]))
        }
    resources = pd.DataFrame(resource_stats)
    resources = resources.transpose()
    resources = resources.explode(resources.columns.tolist())
    # get container names
    resources["container_name"] = resources.index
    # split timestamp 
    resources["dates"] = resources["timestamp"].dt.date
    resources["times"] = resources["timestamp"].dt.time
    
    #len(resources.timestamp.unique()) # all unique so we can use it as index 
    resources = resources.set_index('timestamp')
    # make sure eveything has the same dtype
    resources["cpu_usage"] = resources["cpu_usage"].astype(float)
    resources["memory_usage"] = resources["memory_usage"].astype(int)
    resources["network_received"] = resources["network_received"].astype(int)
    resources["network_send"] = resources["network_send"].astype(int)
    resources["storage_read"] = resources["storage_read"].astype(int)
    resources["storage_written"] = resources["storage_written"].astype(int)

   
    resources.to_csv(target, sep=';')
    return 


if __name__ == "__main__":
    run(load)
