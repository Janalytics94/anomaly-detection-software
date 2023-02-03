#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
from clize import run

from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE


def train(model, scenario):

    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/params.yaml"))
    X = pd.read_csv(os.path.dirname(__file__), "..", "..", "data/interim/" + scenario + "train.csv")
    if model == 'IsolationForest': 
        hyper_parameter = hyper_params[model] #dictionary of hyper_params 
        model = IForest(**hyper_parameter).fit(X)
    
    if model == 'LocalOutlierFactor':
        hyper_parameter = hyper_params[model]
        model = LOF(**hyper_parameter).fit(X)
    
    if model == 'VariationalAutoencoder':
        hyper_parameter = hyper_params[model]
        model = VAE(**hyper_parameter).fit(X)
    
    return model


if __name__ == "__main__":
    run(train)
