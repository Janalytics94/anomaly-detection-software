import dvc.api
import os 
# models of interest 
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm


def load_model(model_type, X):
    
    """
    Selects chosen Model, reads in hyperparameters from params.yaml and returns the designated model fitted to data X.

    Params:
    - model_type: Chose a model_type from the following: IsoLationForest, LocalOutlierDetection
    - X: trainings data

    Returns:
    - model: Fitted model
    """

    hyper_params = dvc.api.params_show('params.yaml')
    if model_type == 'KNN':
        hyper_parameter = hyper_params[model_type]
        model = KNeighborsClassifier(**hyper_parameter).fit(X) # fitted model

    if model_type == 'IsolationForest': 
        hyper_parameter = hyper_params[model_type] #dictionary of hyper_params 
        model = IsolationForest(**hyper_parameter).fit(X)
    
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

def predict_(model, data):

    """
    Predicts if data point is a anomaly, calculates score function and adds it to the dataframe.

    Params:
    - model: fitted model
    - data: data which the prediction should be made for.

    Returns:
    - predictions: class predcitions, if data point is anomalous or not (0 = normal / 1 = anomaly)
    - score: score functions for each data point
    - data: predicitions and scores added as a column to the dataframe

    """
    data_new = data.copy()
    predictions = model.predict(data_new)
    score = model.decision_function(data_new)
    data_new['anomaly']= predictions
    data_new['score'] = score
    data_new['anomaly'] = data_new['anomaly'].mask(data_new['anomaly']==1, 0) # one is zero now and represents normal data points
    data_new['anomaly'] = data_new['anomaly'].mask(data_new['anomaly']==-1, 1) # -1 is 1 now and represents unnormal data points
    predictions = data_new['anomaly']
    return predictions, score, data_new
