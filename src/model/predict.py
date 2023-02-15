#!/usr/bin/env python
import logging
import pandas as pd
import typer

import pickle
from clize import run



def predict(src: str, target:str, scenario: str, model_type: str ):

    '''Predict anomalous or normal data'''

    _logger = logging.getLogger(__name__)
    X = pd.read_csv(src + "/" + scenario + "/test.csv", sep=';')
    X.pop("Unnamed: 0")
    X = X.fillna(0)
    
    if model_type == 'IForest' or "LOF" or "VAE":
        #model = pickle.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "data/model/"+ scenario + "/" + model_type + ".pkl", "rb")))
        _logger.warning(f"Load model: {model_type}")
        model = pickle.load(open('data/model/'+ scenario + '/' + model_type + '.pkl', 'rb'))

        _logger.warning(f"Predict...: {model_type}")
        predictions = model.predict(X)
        scores = model.decision_function(X)
        X['predictions'] = predictions
        X['scores'] = scores
    
    _logger.warning(f"Saving...: {model_type}")
    X.to_csv(target+'/'+ scenario + '/predictions.csv', sep=';')
    
    


if __name__ == "__main__":
    run(predict)
