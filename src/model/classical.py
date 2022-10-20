from sklearn import metrics
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans 
import dvc.api
import pandas as pd


#TODO:Pfade anpassen ohne hard coding
# Figure out how to deal with train and test data.
# Zusätzliche Features -> Literature!

def train(method):
    params = dvc.api.params_show('src/model/params.yml')

    random_state = params['IsolationForest']['random_state']

    df = pd.read_pickle('data/interim/scaled/train_standard.pkl')
    columns = df.columns.tolist()

    #call and fit model
    if method == "IsolationForest": 
        model = IsolationForest(random_state=random_state).fit(df[columns])
    if method == "KMeans":
        model = KMeans(random_state=random_state)

# get score functions 
    df['scores'] = model.decision_function(df[columns])





