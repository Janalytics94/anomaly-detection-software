#!/usr/bin/env python

import pandas as pd
import json 

from clize import run


def table(src:str):

    '''Visualize results'''
     
    data = open(src)
    data = json.load(data)
    df = pd.DataFrame.from_dict(data, orient="index", columns=['results'])
    print(df.to_markdown(tablefmt="grid"))

    return

if __name__ == "__main__":
    run(table)
