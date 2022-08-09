#! /usr/bin/env python3

import sys
import pandas as pd
sys.path.append('.')
from src.ingest.data_loader import DataLoader




def convert(source: str, target: str):

        data_loader = DataLoader()

        with open('test.json', 'w') as output_file:
                json.dump(
                        {get_file_name(path):
                        {
                        'timestamp': timestamps, 'cpu_usage': cpu_usage, 
                        'memory_usage': memory_usage, 'network_received': network_received, 
                        'network_send': newtwork_send, 'storage_read': storage_read, 
                        'storage_written': storage_written
                        }
                    }, output_file, indent=4
                )


