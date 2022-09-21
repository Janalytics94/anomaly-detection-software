#!/usr/bin/env python
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
    "validation": dataloader.validation_data()
    }

  # necessary features from the .res file 
  timestamps_l = []
  cpu_usage_l = []
  memory_usage_l = []
  network_received_l = []
  network_send_l = []
  storage_read_l = []
  storage_written_l = []

  if type_of_data == "train":
    recordings = raw["train"]

  if type_of_data == "test":
    recordings = raw["test"]

  if type_of_data == "validation":
    recordings = raw["validation"]
  

  for i in range(0,len(recordings)):
    for resource_stats in recordings[i].resource_stats():
      timestamps_l.append(resource_stats.timestamp_datetime())
      cpu_usage_l.append(resource_stats.cpu_usage())
      memory_usage_l.append(resource_stats.memory_usage())
      network_received_l.append(resource_stats.network_received())
      network_send_l.append(resource_stats.network_send())
      storage_read_l.append(resource_stats.storage_read())
      storage_written_l.append(resource_stats.storage_written())


  resources = { 
    "timestamp": timestamps_l, "cpu_usage": cpu_usage_l,
    "memory_usage": memory_usage_l, "network_received": network_received_l,
    "network_send": network_send_l, 
    "storage_read": storage_read_l, "storage_written": storage_written_l
  }
  
  resources = pd.DataFrame(resources)
  resources.to_pickle(target + '/'+ type_of_data + '.pkl')
  
  return resources


if __name__ == '__main__':
 run(load)