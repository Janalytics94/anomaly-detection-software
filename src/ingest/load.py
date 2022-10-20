#!/usr/bin/env python
from re import A
from dataloader.dataloader_factory import dataloader_factory
import pandas as pd
from clize import run


def load(src, target, type_of_data):

    """
    Function to load .res files from the scenario CVE-2020-23839

    Parameters:
    src (str): path to data scenario: currently : CVE-2020-23839
    type_of_data (str): train, test or validation data files

    Returns:
    pd.Dataframe for each recording
    """
    # iterate the data
    dataloader = dataloader_factory(src)
    raw = {
        "train": dataloader.training_data(),
        "test": dataloader.test_data(),
        "validation": dataloader.validation_data(),
    }

    container_names = []
    resource_stats_l = []

    if type_of_data == "train":
        recordings = raw["train"]

    if type_of_data == "test":
        recordings = raw["test"]

    if type_of_data == "validation":
        recordings = raw["validation"]

    # get meta data 
    meta = {}
    for i in range(0, len(recordings)):
        container_names.append(recordings[i].name)
        resource_stats_l.append(recordings[i].resource_stats())

    for h in range(0,len(container_names)):
        #for q in range(0,len(resource_stats_l[h])):
        meta[container_names[h]] = {
                "timestamp": [resource_stats_l[h][q].timestamp_datetime() for q in range(0,len(resource_stats_l[h]))],
                "cpu_usage": [resource_stats_l[h][q].cpu_usage() for q in range(0,len(resource_stats_l[h]))],
                "memory_usage": [resource_stats_l[h][q].memory_usage() for q in range(0,len(resource_stats_l[h]))],
                "network_received": [resource_stats_l[h][q].network_received() for q in range(0,len(resource_stats_l[h]))],
                "network_send": [resource_stats_l[h][q].network_send() for q in range(0,len(resource_stats_l[h]))],
                "storage_read": [resource_stats_l[h][q].storage_read() for q in range(0,len(resource_stats_l[h]))],
                "storage_written": [resource_stats_l[h][q].storage_written() for q in range(0,len(resource_stats_l[h]))],
        }

    resources = pd.DataFrame(meta)
    resources = resources.transpose()
    resources.to_pickle(target + "/" + type_of_data + ".pkl")

    return resources


if __name__ == "__main__":
    run(load)
