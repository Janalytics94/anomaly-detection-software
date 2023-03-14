#!/usr/bin/env python
import os
import pandas as pd
import dvc.api
import logging
import random
import json
import jsonlines

from sklearn.metrics import (
    roc_curve, auc, confusion_matrix, 
    )

from pyod.models.iforest import IForest
from clize import run 

def gridsearch(src: str, target: str, scenario: str, model_type: str):

    """Script for Hyperparameter Tuning"""


    _logger = logging.getLogger(__name__)
    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/gridsearch.yaml"))
    #hyper_params = dvc.api.params_show("src/model/gridsearch.yaml")
   

    _logger.warning("Load relevant data...")
    X_train = pd.read_csv(src + "/" + scenario + "/train.csv", sep=';')
    X_train.pop("Unnamed: 0")
    X_train = X_train.fillna(0)

    X_test = pd.read_csv(src + "/" + scenario + "/test.csv", sep=';')
    X_test.pop("Unnamed: 0")
    X_test = X_test.fillna(0)

    y_true = pd.read_csv(src+ "/" + scenario + "/y_test.csv", sep=';')
    y_true.pop("Unnamed: 0")

    _logger.warning("Start GridSearch...")

    if model_type == 'IForest':
        hyper_parameter = hyper_params[model_type]
        n_estimators = hyper_parameter['n_estimators']
        max_samples = hyper_parameter['max_samples']
        contamination = hyper_parameter['contamination']
        max_features = hyper_parameter['max_features']
        bootstrap = hyper_parameter['bootstrap']
        n_jobs = hyper_parameter['n_jobs']
        random_state = hyper_parameter['random_state']
        verbose = hyper_parameter['verbose']

        for i in range(0,100):
            # chose Hyperparams randomly
            model = IForest(n_estimators = random.choice(n_estimators) , max_samples=max_samples, 
                            contamination=random.choice(contamination), max_features=random.choice(max_features),
                            bootstrap=random.choice(bootstrap), n_jobs=n_jobs,
                            random_state=random_state, verbose=verbose).fit(X_train)
            
            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            
            _logger.warning("Start evaluating performance measures...")
            # Confusion Matrix
            cm = confusion_matrix(y_true=y_true, y_pred=predictions)
            true_negative = cm[0,0]
            false_positive = cm[0,1]
            false_negative = cm[1,0]
            true_positive = cm[1,1]

            # Metrics
            FPR = false_positive/(false_positive+true_negative)
            FNR = false_negative/(true_positive+false_negative)
            RCL = true_positive/(true_positive+false_negative)
            PRC = true_positive/(true_positive+false_positive)
            ACC = (true_positive+true_negative)/(true_positive+false_positive+false_negative+true_negative)
            F1 = 2*(PRC*RCL)/ (PRC+RCL)
            fpr_, tpr_, _ = roc_curve(y_true, scores)
            AUC = auc(fpr_, tpr_)
            dictionary = {
                    "Round": i,
                    "model" : model_type,
                    "params" : model.get_params(),
                    "FPR" : FPR,
                    "FNR" : FNR,
                    "RCL" : RCL,
                    "PRC" : PRC,
                    "ACC" : ACC,
                    "F1" : F1,
                    "AUC": AUC
            }


            _logger.warning("Save chosen model paarmeters and results...")
            with open(target + "/gridsearch.txt", "w") as output:
                    output.write(str(dictionary))
                    output.write("\n")









        
    return

if __name__ == "__main__":
    run(gridsearch)