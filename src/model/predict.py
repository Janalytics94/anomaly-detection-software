import os
import dvc.api
from model.helpers import *

# models of interest
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE


def load_model(
    model_type: str,
    train_data: dict,
    test_data: dict,
    scenario: str,
    contamination_rate: False,
):

    """
    Selects chosen Model, reads in hyperparameters from params.yaml and returns the designated model fitted to data X.

    Params:
    - model_type: Chose a model_type from the following: IsoLationForest, LocalOutlierDetection
    - data: dictionary with designated data
    - scenario: choose which scneario you want to examine

    Returns:
    - model: Fitted model

    """
    # Select scenario
    X = train_data[scenario]
    X = select_columns_for_modelling(X)
    base = os.path.dirname(__file__)
    # read in hyper_parameter
    hyper_params = dvc.api.params_show(
        os.path.join(base, "..", "..", "src/model/params.yaml")
    )

    if model_type == "IsolationForest":
        hyper_parameter = hyper_params[model_type]  # dictionary of hyper_params
        if contamination_rate == True:
            # calculate anaomalus rate
            X_test = test_data[scenario]
            cr = calculate_anomalous_rate(X_test)
            if cr > 0.5:
                cr = 0.5
            hyper_parameter["contamination"] = cr
            print(scenario + ":" + str(cr))
        model = IForest(**hyper_parameter).fit(X)

    if model_type == "LocalOutlierFactor":
        hyper_parameter = hyper_params[model_type]
        if contamination_rate == True:
            # calculate anaomalus rate
            X_test = test_data[scenario]
            cr = calculate_anomalous_rate(X_test)
            if cr > 0.5:
                cr = 0.5
            hyper_parameter["contamination"] = cr
            print(scenario + ":" + str(cr))
        model = LOF(**hyper_parameter).fit(X)

    if model_type == "VariationalAutoencoder":
        hyper_parameter = hyper_params[model_type]
        if contamination_rate == True:
            # calculate anaomalus rate
            X_test = test_data[scenario]
            cr = calculate_anomalous_rate(X_test)
            hyper_parameter["contamination"] = cr
            if cr > 0.5:
                cr = 0.5
            hyper_parameter["contamination"] = cr
            print(scenario + ":" + str(cr))
        model = VAE(**hyper_parameter).fit(X)

    return model


def predict_(model, model_type: str, data: dict, scenario: str):

    """
    Predicts if data point is a anomaly, calculates score function and adds it to the dataframe.

    Params:
    - model: fitted model
    - data: data which the prediction should be made for.

    Returns:
    - predictions: class predcitions, if data point is anomalous or not (0 = normal / 1 = anomaly) -> depends on the algorithm needs to be checked again
    - score: score functions for each data point
    - data: predicitions and scores added as a column to the dataframe

    """
    X_test = data[scenario]
    X_test = select_columns_for_modelling(X_test)

    predictions = model.predict(X_test)

    scores = model.decision_function(X_test)
    # add results to dataframe
    X_test[model_type + "_predictions"] = predictions
    X_test[model_type + "_scores"] = scores

    return predictions, scores, X_test
