#!/usr/bin/env python
import os
import dvc.api
import pandas as pd
import logging
import pickle


from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.vae import VAE

from clize import run


def train(src: str, target: str, scenario: str, model_type: str):

    """
    Load data, training, saved model
    """

    _logger = logging.getLogger(__name__)

    hyper_params = dvc.api.params_show(
        os.path.join(os.path.dirname(__file__), "..", "..", "src/model/params.yaml")
    )
    X = pd.read_csv(src + "/" + scenario + "/train.csv", sep=";")
    X.pop("Unnamed: 0")
    X = X.fillna(0)

    # Scaler
    standard_scaler = StandardScaler()
    _logger.warning("##############################")
    _logger.warning(f"Training: {model_type}")
    _logger.warning("##############################")

    if model_type == "IForest":
        hyper_parameter = hyper_params[model_type]  # dictionary of hyper_params
        model = IForest(**hyper_parameter).fit(X)
        _logger.warning("##############################")
        _logger.warning(f"Saving model: {model_type}")
        _logger.warning("##############################")
        pickle.dump(model, open(target + scenario + "/" + model_type + ".pkl", "wb"))

    if model_type == "LOF":
        hyper_parameter = hyper_params[model_type]
        # add preprocess data
        X = standard_scaler.fit_transform(X)
        model = LOF(**hyper_parameter).fit(X)
        _logger.warning("##############################")
        _logger.warning(f"Saving model: {model_type}")
        _logger.warning("##############################")
        pickle.dump(model, open(target + "/" + scenario + "/" + model_type + ".pkl", "wb"))


    if model_type == "VAE":
            hyper_parameter = hyper_params[model_type]
            model = VAE(**hyper_parameter).fit(X)
            _logger.warning("##############################")
            _logger.warning(f"Make Predictions: {model_type}")
            _logger.warning("##############################")
            # read in test data to make predictions
            X_test = pd.read_csv(src + "/" + scenario + "/test.csv", sep=";")
            X_test.pop("Unnamed: 0")
            X_test = X_test.fillna(0)
            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            X_test["predictions"] = predictions
            X_test["scores"] = scores
            _logger.warning(f"Saving predictions: {model_type}")
            target = "data/predictions"
            X_test.to_csv(
                target + "/" + scenario + "/predictions_" + model_type + ".csv",
                sep=";",
            )

    return


if __name__ == "__main__":
    run(train)
