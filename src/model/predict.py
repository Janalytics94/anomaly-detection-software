import dvc.api

# models of interest 
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

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
    if model_type == 'IsolationForest': 
        hyper_parameter = hyper_params['IsolationForest'] #dictionary of hyper_params 
        model = IsolationForest(**hyper_parameter).fit(X)
    
    if model_type == 'LocalOutlierFactor':
        hyper_parameter = hyper_params['LocalOutlierFactor']
        model = LocalOutlierFactor(**hyper_parameter).fit(X)

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

def evaluate():


    return



        # Method evalutate mit validation data 

        # calcualte f1 score
        # confusion matrix 
    