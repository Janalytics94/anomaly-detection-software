#!/usr/bin/env python
import pandas as pd


def calc_time_delta(df) -> pd.DataFrame:
    """
    Calculates Time Delta between different rows

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
    
    """
    cn_dfs = []
    container_names = df["container_name"].unique().tolist()
    for i in range(0,len(container_names)):
        cn_dfs.append(df[df["container_name"]==container_names[i]])


    return cn_dfs