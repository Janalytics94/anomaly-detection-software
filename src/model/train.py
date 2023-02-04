#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
import logging
import pickle 
from clize import run

from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE


def train(src, model, scenario, target):

    """
    Load data, training, saved model
    """

    _logger = logging.getLogger(__name__)
    _logger.warning(f"Training: {model}")
    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/params.yaml"))
    X = pd.read_csv(src + "/" + scenario + "/train.csv", sep=';')
    if model == 'IsolationForest': 
        hyper_parameter = hyper_params[model] #dictionary of hyper_params 
        model = IForest(**hyper_parameter).fit(X)
    
    if model == 'LocalOutlierFactor':
        hyper_parameter = hyper_params[model]
        model = LOF(**hyper_parameter).fit(X)
    
    if model == 'VariationalAutoencoder':
        hyper_parameter = hyper_params[model]
        model = VAE(**hyper_parameter).fit(X)
    _logger.warning(f"Saving model: {model}")

    with open(target, 'w') as file:
        pickle.dump(model, file)
    
    return 


if __name__ == "__main__":
    run(train)
