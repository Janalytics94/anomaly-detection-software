#!/usr/bin/env python
import pandas as pd
from sklearn import preprocessing

# Functions
def calc_time_delta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Time Delta between different rows of Timestamp index

    Params:
    - df: pd.DataFrame as input

    Returns:
    - df: with new columns tvalue and tdelta
    """
    df["tvalue"] = df.index
    df["tdelta"] = df["tvalue"] - df["tvalue"].shift()

    return df


def split_by_container(df: pd.DataFrame) -> list:
    """
    Creates a dataframe for each container and saves them in a list

    Params:
    - df: pd.DataFrame as input

    Returns:
    - cn_dfs: list with saved df's for each container
    """
    cn_dfs = []
    container_names = df["container_name"].unique().tolist()
    for i in range(0, len(container_names)):
        cn_dfs.append(df[df["container_name"] == container_names[i]])

    return cn_dfs


def encode(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes column "exploit" of dataframe and encodes true false values to int64

    Params:
    - df: pd.DataFrame as input

    Returns:
    - df: pd.DataFrame

    """

    df["exploit"] = df["exploit"].astype(int)

    return df


def select_columns_for_modelling(df: pd.DataFrame) -> pd.DataFrame:

    """
    Selects only the columns of interest for the model

    Params:
    - df: pd.DataFrame as input

    Returns:
    - df: pd.DataFrame
    """

    df = df[
        ["cpu_usage", "memory_usage"]
    ]  #'network_received','network_send','storage_read','storage_written']]

    return df


def select_columns_outlier_truncate(df: pd.DataFrame) -> pd.DataFrame:

    """
    Selects only the columns of interest for the model

    Params:
    - df: pd.DataFrame as input

    Returns:
    - df: pd.DataFrame
    """

    df = df[
        ["cpu_usage", "memory_usage", "exploit"]
    ]  #'network_received','network_send','storage_read','storage_written']]

    return df


def create_y_values(df: pd.DataFrame) -> pd.Series:

    """
    Gets the true labels of the data

     Params:
    - df: pd.DataFrame as input

    Returns:
    - y_true: pd.Series
    """

    y_true = df["exploit"]

    return y_true


def calculate_anomalous_rate(df: pd.DataFrame) -> float:

    """
    Gives percentage of anamoly data
    Usuful for contanimation_rate in hyper_params

    Params:
    - df: dataframe with data
    Returns:
    - percentage: float percentage rate
    """
    number_normal_recodings = df[df["exploit"] != True].shape[0]
    number_anomalous_recordings = df[df["exploit"] == True].shape[0]

    percentage = number_anomalous_recordings / number_normal_recodings

    return percentage


def outlier_truncate(df: pd.DataFrame) -> pd.DataFrame:
    """
    As we have skewed distributions (see EDA) we will use IQR
    Make sure you apply it only on test data!
    """
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    no_outliers = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))]

    return no_outliers


def scale(df: pd.DataFrame, method: str):
    """
    Params:
        - methods : standard, min_max, max_abs, power
        - x : columns that should be scaled in df.

    Returns:
        - x_scaled : scaled value according to chosen method

    """

    columns = df.columns.tolist()
    columns = [
        column
        for column in columns
        if column
        not in (
            "dates",
            "times",
            "container_name",
            "exploit",
            "timestamp_container_ready",
            "timestamp_trick_admin",
            "timestamp_execute_reverse_shell",
            "timestamp_warmup_end",
        )
    ]
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

    return df_scaled
