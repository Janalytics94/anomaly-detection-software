
import pandas as pd 
import dvc.api

# models of interest 
from sklearn.ensemble import IsolationForest


# read in yaml
params = dvc.api.params_show('src/model/params.yml')

#if model = 'IsolationForest': 


# read in the data 
data = pd.read_pickle(path)

def fit_(model, data):
    return model.fit(data)

def predict_(model, data):
    predictions = model.predict(data)
    score = model.decision_function(data)
    data['anomaly']= predictions
    data ['score'] = score
    return predictions, score, data





# Method evalutate mit validation data 

# calcualte f1 score
# confusion matrix 