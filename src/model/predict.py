#!/usr/bin/env python
import os
import dvc.api
from clize import run


def predict(model, model_type: str,  data: dict, scenario: str):

    
    X_test = data[scenario]
   
    predictions = model.predict(X_test)
        

    scores = model.decision_function(X_test)
    # add results to dataframe
    X_test[model_type + "_predictions"] = predictions
    X_test[model_type + "_scores"] = scores

    return predictions, scores, X_test


if __name__ == "__main__":
    run(predict)
