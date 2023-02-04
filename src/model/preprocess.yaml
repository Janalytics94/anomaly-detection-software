
    def scale(df: pd.DataFrame, method: str):
        """
        Params:
            - methods : standard, min_max, max_abs, power
            - x : columns that should be scaled in df.

        Returns:
            - x_scaled : scaled value according to chosen method

        """

        columns = df.columns.tolist()
        columns = [column for column in columns if column not in ("dates", "times", "container_name", "exploit", "timestamp_container_ready" , "timestamp_trick_admin" , "timestamp_execute_reverse_shell" , "timestamp_warmup_end")]
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

        return df_scal

      

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
