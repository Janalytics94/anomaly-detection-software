import dvc.api
from model.helpers import *
# models of interest 
import eif
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn import svm


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
    #contamination_rate = calculate_anomalous_rate(X)
    X = select_columns_for_modelling(X)
    hyper_params = dvc.api.params_show('../../../src/model/params.yaml')
    if model_type == 'KMEANS':
        hyper_parameter = hyper_params[model_type]
        model = KMeans(**hyper_parameter).fit(X) # fitted model

    if model_type == 'IsolationForest': 
        hyper_parameter = hyper_params[model_type] #dictionary of hyper_params 
        model = IsolationForest(**hyper_parameter).fit(X)
    
    if model_type == 'ExtendedIsolationForest': #ExtensionLevel=0 is the same as regular Isolation Forest
        X = np.array(X)
        hyper_parameter = hyper_params[model_type]
        model = eif.iForest(X, **hyper_parameter)

    if model_type == 'LocalOutlierFactor':
        hyper_parameter = hyper_params[model_type]
        model = LocalOutlierFactor(**hyper_parameter).fit(X)
    
    if model_type == 'DBSCAN':
        hyper_parameter = hyper_params[model_type]
        model = DBSCAN(**hyper_parameter).fit(X)

    if model_type == 'SVM':
        hyper_parameter = hyper_params[model_type]
        model = svm.OneClassSVM(**hyper_parameter).fit(X)

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

    if model_type in ["IsolationForest", "LocalOutlierFactor"]: #"DBSCAN", "SVM"]:
        scores = model.decision_function(X_test)
    # add results to dataframe
    X_test[model_type + "_predictions"] = predictions
    X_test[model_type + "_scores"] = scores
    #data_new['anomaly'] = data_new['anomaly'].mask(data_new['anomaly']==1, 0) # one is zero now and represents normal data points
    #data_new['anomaly'] = data_new['anomaly'].mask(data_new['anomaly']==-1, 1) # -1 is 1 now and represents unnormal data points
    #predictions = data_new['anomaly']
    return predictions, scores, X_test
