
      

def calculate_anomalous_rate(df:pd.DataFrame) -> float:

    """
    Gives percentage of anamoly data
    Usuful for contanimation_rate in hyper_params

    Params:
    - df: dataframe with data
    Returns:
    - percentage: float percentage rate
    """
    number_normal_recodings = df[df['exploit']!=True].shape[0]
    number_anomalous_recordings = df[df['exploit']==True].shape[0]

    percentage = number_anomalous_recordings/number_normal_recodings


    return percentage
