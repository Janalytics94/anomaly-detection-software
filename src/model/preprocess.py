#!/usr/bin/env python
import pandas as pd
from clize import run


def preprocess(path, data):

    '''
    
    '''

    df = pd.read_csv(path)

    # encode 
    df["exploit"] = df["exploit"].astype(int)
    # select columns for modeling
    df = df[['cpu_usage','memory_usage']]#'network_received','network_send','storage_read','storage_written']]	

    # create y_values
    y_true = df["exploit"]

    # Outlier Trunctuate 
    Q1=df.quantile(0.25)
    Q3=df.quantile(0.75)
    IQR=Q3-Q1
    df =df[~((df<(Q1-1.5*IQR)) | (df>(Q3+1.5*IQR)))]

    return 


if __name__ == "__main__":
    run(preprocess)

        


    

    