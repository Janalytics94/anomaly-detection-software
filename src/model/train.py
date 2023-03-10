#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
import logging
import pickle
from clize import run

from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE
from sklearn.cluster import KMeans, DBSCAN


def train(src:str,  target:str, scenario: str, model_type: str):

    """
    Load data, training, saved model
    """
    
    _logger = logging.getLogger(__name__)
   
    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/params.yaml"))
    X = pd.read_csv(src + "/" + scenario + "/train.csv", sep=';')
    X.pop("Unnamed: 0")
    X = X.fillna(0)
    
    _logger.warning(f"Training: {model_type}")
    if model_type == 'IForest': 
        hyper_parameter = hyper_params[model_type] #dictionary of hyper_params 
        model = IForest(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))
       
    if model_type == 'LOF':
        hyper_parameter = hyper_params[model_type]
        # add preprocess data 
        standard_scaler = StandardScaler()
        X_standard = standard_scaler.fit_transform(X)
        model_standard = LOF(**hyper_parameter).fit(X_standard)
        _logger.warning(f"Saving model Standard Scaling: {model_type}")
        pickle.dump(model_standard, open(target+ '/' + model_type +'_standard.pkl', 'wb'))

        minmax_scaler= MinMaxScaler()
        X_minmax = minmax_scaler.fit_transform(X)
        model_minxmax = LOF(**hyper_parameter).fit(X_minmax)
        _logger.warning(f"Saving model Min Max Scaling: {model_type}")
        pickle.dump(model_minxmax, open(target+ '/' + model_type +'_minmax.pkl', 'wb'))

        maxabsscaler = MaxAbsScaler()
        X_maxabs = maxabsscaler.fit_transform(X)
        model_maxabs = LOF(**hyper_parameter).fit(X_maxabs)
        _logger.warning(f"Saving model MaxAbs Scaling: {model_type}")
        pickle.dump(model_maxabs, open(target+ '/' + model_type +'_maxabs.pkl', 'wb'))
        

    if model_type == 'VAE':
        hyper_parameter = hyper_params[model_type]
        model = VAE(**hyper_parameter).fit(X)
        _logger.warning(f"Saving model: {model_type}")
        pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))


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
