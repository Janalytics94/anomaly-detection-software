#!/usr/bin/env python
import logging
import pandas as pd

import pickle
from clize import run
from sklearn.cluster import DBSCAN



def predict(src: str, target:str, scenario: str, model_type: str ):

    '''Predict anomalous or normal data'''

    _logger = logging.getLogger(__name__)
    X = pd.read_csv(src + "/" + scenario + "/test.csv", sep=';')
    X.pop("Unnamed: 0")
    X = X.fillna(0)

    algorithms = ["IForest", "LOF", "VAE"]
    if model_type in algorithms:
        #model = pickle.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "data/model/"+ scenario + "/" + model_type + ".pkl", "rb")))
        _logger.warning(f"Load model: {model_type}")
        model = pickle.load(open('data/model/'+ scenario + '/' + model_type + '.pkl', 'rb'))

        _logger.warning(f"Predict...: {model_type}")
        predictions = model.predict(X)
        scores = model.decision_function(X)
        X['predictions'] = predictions
        X['scores'] = scores
    
    if model_type == "KMEANS":
        _logger.warning(f"Load model: {model_type}")
        model = pickle.load(open('data/model/'+ scenario + '/' + model_type + '.pkl', 'rb'))
        _logger.warning(f"Predict...: {model_type}")
        labels = model.labels_
        predictions = model.predict(X) #Predict the closest cluster each sample in X belongs to. 
        scores = model.score(X) # Opposite of the value of X on the K-means objective.
        X['lables'] = labels
        X['predictions'] = predictions
        X['scores'] = scores


    if model_type == "DBSCAN":
        _logger.warning(f"Load model: {model_type}")
        model = pickle.load(open('data/model/'+ scenario + '/' + model_type + '.pkl', 'rb'))
        _logger.warning(f"Predict...: {model_type}")
        predictions = model.fit_predict(X) #Compute clusters from a data or distance matrix and predict labels.
        labels = model.labels_
        X['predictions'] = predictions
        X['lables'] = labels

    _logger.warning(f"Saving...: {model_type}")
    X.to_csv(target+'/'+ scenario + '/predictions.csv', sep=';')
    
    


if __name__ == "__main__":
    run(predict)
