#! /usr/bin/env python3
from dataloader.dataloader_factory import dataloader_factory

# iterate the data
dataloader = dataloader_factory("/Users/janavihs/projects/anomaly-detection-software/anomalydetection/data/LIDS/CVE-2014-0160/raw")

for recording in dataloader.training_data():
  for syscall in recording.syscalls():
    print(syscall.process_name() + " called " + syscall.name())