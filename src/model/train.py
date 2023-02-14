#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
import logging
import pickle 
import typer
from clize import run

from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE


def train(src:str,  target:str, preprocess=False, scenario: str = typer.Argument(envvar="SCENARIO"), model_type: str = typer.Argument(envvar="MODEL_TYPE")):

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
       
    if model_type == 'LOF':
        hyper_parameter = hyper_params[model_type]
        # add preprocess data 
        if preprocess == True:
            X_standard = StandardScaler.fit_transform(X)
            model_standard = LOF(**hyper_parameter).fit(X_standard)
            pickle.dump(model_standard, open(target+ '/' + model_type +'_standard.pkl', 'wb'))
        
            X_minmax = MinMaxScaler.fit_transform(X)
            model_minxmax = LOF(**hyper_parameter).fit(X_minmax)
            pickle.dump(model_minxmax, open(target+ '/' + model_type +'_minmax.pkl', 'wb'))

            X_maxabs = MaxAbsScaler.fit_transform(X)
            model_maxabs = LOF(**hyper_parameter).fit(X_maxabs)
            pickle.dump(model_maxabs, open(target+ '/' + model_type +'_maxabs.pkl', 'wb'))

    if model_type == 'VAE':
        hyper_parameter = hyper_params[model_type]
        model = VAE(**hyper_parameter).fit(X)
    _logger.warning(f"Saving model: {model_type}")

    pickle.dump(model, open(target+ '/' + model_type +'.pkl', 'wb'))

    
    return 


if __name__ == "__main__":
    run(train)
