#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
import logging
import pickle
import joblib


from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE
from pyod.models.knn import KNN
from sklearn.cluster import KMeans, DBSCAN

from clize import run

def train(src:str,  target:str, scenario: str, model_type: str):

    """
    Load data, training, saved model
    """
    
    _logger = logging.getLogger(__name__)
   
    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/params.yaml"))
    X = pd.read_csv(src + "/" + scenario + "/train.csv", sep=';')
    X.pop("Unnamed: 0")
    X = X.fillna(0)

    # Scaler
    standard_scaler = StandardScaler()
    
    _logger.warning(f"Training: {model_type}")
    if model_type == 'IForest': 
        hyper_parameter = hyper_params[model_type] #dictionary of hyper_params 
        model = IForest(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))
       
    if model_type == 'LOF':
        hyper_parameter = hyper_params[model_type]
        # add preprocess data 
        X = standard_scaler.fit_transform(X)
        model = LOF(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))

        
    if model_type == 'KNN':
        hyper_parameter = hyper_params[model_type]
        X = standard_scaler.fit_transform(X)
        model = KNN(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model Standard Scaling: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))


    if model_type == 'VAE':
        hyper_parameter = hyper_params[model_type]
        model = VAE(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        joblib.dump(model, open(target+ '/' + model_type +'.h5', 'wb'))


    if model_type == "KMEANS":
        hyper_parameter = hyper_params[model_type]
        model = KMeans(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))

    if model_type == "DBSCAN":
        hyper_parameter = hyper_params[model_type]
        model = DBSCAN(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))

    
    return 


if __name__ == "__main__":
    run(train)
