#!/usr/bin/env python
import pandas as pd

# Functions 
def calc_time_delta(df) -> pd.DataFrame:
    """
    Calculates Time Delta between different rows of Timestamp index 

    Params:
    - df: pd.DataFrame as input

    Returns:
    - df: with new columns tvalue and tdelta
    """
    df['tvalue'] = df.index
    df['tdelta'] = (df['tvalue']-df['tvalue'].shift())
    
    return df


def split_by_container(df) -> list:
    """
    Creates a dataframe for each container and saves them in a list

    Params:
    - df: pd.DataFrame as input

    Returns: 
    - cn_dfs: list with saved df's for each container 
    """
    cn_dfs = []
    container_names = df["container_name"].unique().tolist()
    for i in range(0,len(container_names)):
        cn_dfs.append(df[df["container_name"]==container_names[i]])


    return cn_dfs

def encode(df) -> pd.DataFrame:
    """
    Encodes column "exploit" of dataframe and encodes true false values to int64

    Params: 
    - df: pd.DataFrame as input

    Returns:
    - df: pd.DataFrame

    """

    df["exploit"] = df["exploit"].astype(int)

    return df

def select_columns_for_modelling(df) -> pd.DataFrame:

    """
    Selects only the columns of interest for the model
    
    Params: 
    - df: pd.DataFrame as input

    Returns:
    - df: pd.DataFrame
    """


    df = df[['cpu_usage','memory_usage', 'network_received','network_send','storage_read','storage_written']]	

    return df

def create_y_values(df) -> pd.Series:
    
    """
    Gets the true labels of the data

     Params: 
    - df: pd.DataFrame as input

    Returns:
    - y_true: pd.Series
    """


    y_true = df["exploit"]


    return y_true

def calculate_anomalous_rate(df):

    """
    Gives percentage of anamoly data
    Usuful for contanimation_rate in hyper_params

    """
    number_normal_recodings = df[df['exploit']!=True].shape[0]
    number_anomalous_recordings = df[df['exploit']==True].shape[0]

    percentage = number_anomalous_recordings/number_normal_recodings


    return percentage

def classify_anomalies(df, feature):
    df['feature_name'] = feature
        
    df.sort_values(by='timestamp', ascending=False)

    #Categorise anomalies as 0-no anomaly, 1- low anomaly , 2 - high anomaly
    df['anomaly'].loc[df['anomaly'] == 1] = 0
    df['anomaly'].loc[df['anomaly'] == -1] = 2
    df['anomaly_class'] = df['anomaly']
    max_anomaly_score = df['score'].loc[df['anomaly_class'] == 2].max()
    print('Maximaler Anomaly Score for {0}: '.format(feature)) 
    print(max_anomaly_score)
    medium_percentile = df['score'].quantile(0.24)
    print('Medium Percentile for {0}: '.format(feature)) 
    print(medium_percentile)
    df['anomaly_class'].loc[(df['score'] > max_anomaly_score) & (df['score'] <= medium_percentile)] = 1
    return df