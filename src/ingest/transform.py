#!/usr/bin/env python
from sklearn import preprocessing
import numpy as np
import pandas as pd
from clize import run

#TODO: maybe quantile transformation mit dazu?

def scale(src, method, type_of_data, target):
    """
    Standard: Scaled data has zero mean and unit variance

    Params:
        - methods : standard, min_max, max_abs, power
        - x : columns that should be scaled in df.

    Returns:
        - x_scaled : scaled value according to chosen method

    """
    df = pd.read_pickle(src)
    df = df.set_index("timestamp")
    columns = df.columns.tolist()
    df_scaled = df.copy()

    if method == "standard":
        scaler = preprocessing.StandardScaler()
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])

    if method == "min_max":
        scaler = preprocessing.MinMaxScaler()
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])

    if method == "max_abs":
        scaler = preprocessing.MaxAbsScaler()
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])

    if (
        method == "power"
    ):  # default is Yeo-Johnson, Box-Cox Tranformation is not applicable
        scaler = preprocessing.PowerTransformer(method="yeo-johnson", standardize=False)
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])

    df_scaled.to_pickle(target + "/" + type_of_data + "_" + method + ".pkl")
    return df_scaled


if __name__ == "__main__":
    run(scale)
