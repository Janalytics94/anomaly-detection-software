import os
import dvc.api
from model.helpers import *
# models of interest 
from pyod.models import iforest
from pyod.models import lof
from pyod.models.vae import VAE


def load_model(model_type: str, data: dict, scenario: str):
    
    """
    Selects chosen Model, reads in hyperparameters from params.yaml and returns the designated model fitted to data X.

    Params:
    - model_type: Chose a model_type from the following: IsoLationForest, LocalOutlierDetection
    - data: dictionary with designated data 
    - scenario: choose which scneario you want to examine

    Returns:
    - model: Fitted model
   
    """
    X = data[scenario]
    
    X = select_columns_for_modelling(X)
    
    #hyper_params = dvc.api.params_show('../../../src/model/params.yaml')
    base = os.path.dirname(__file__)

    hyper_params = dvc.api.params_show(os.path.join(base, "..", "..", "src/model/params.yaml"))

    if model_type == 'IsolationForest': 
        hyper_parameter = hyper_params[model_type] #dictionary of hyper_params 
        model = iforest.IForest(**hyper_parameter).fit(X)

    if model_type == 'LocalOutlierFactor':
        hyper_parameter = hyper_params[model_type]
        model = lof.LOF(**hyper_parameter).fit(X)
    
    if model_type == 'VariationalAutoencoder':
        hyper_parameter = hyper_params[model_type]
        model = VAE(**hyper_parameter).fit(X)

    return model

def predict_(model, model_type: str,  data: dict, scenario: str):

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
        

    #if model_type in ["IsolationForest", "LocalOutlierFactor", "VariationalAutoencoder"]:
    scores = model.decision_function(X_test)
    # add results to dataframe
    X_test[model_type + "_predictions"] = predictions
    X_test[model_type + "_scores"] = scores

   #if model_type == 'VariationalAutoencoder': #remember 0 = inliners, 1 = outliers
   #     X_test[model_type + "_predictions"] = X_test[model_type + "_predictions"].mask(X_test[model_type + "_predictions"]==1, -1) # 1 to  -1 outliers
   #     X_test[model_type + "_predictions"] = X_test[model_type + "_predictions"].mask(X_test[model_type + "_predictions"]==0,  1) # 0 to  1 = inliners
 
    return predictions, scores, X_test
