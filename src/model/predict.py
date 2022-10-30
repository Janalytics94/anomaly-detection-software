
import pandas as pd 
import dvc.api

# models of interest 
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class A_Model():
    
    def __init__(self, model_type):
        self.model_type = model_type # -> think of possible model_types 
        self.hyper_params = dvc.api.params_show('/Users/janavihs/projects/anomaly-detection-software/src/model/params.yml')
        
    def load_model(self):
        if self.model_type == 'IsolationForest': 
            hyper_parameter = self.hyper_params['IsolationForest'] #dictionary of hyper_params 
            model = IsolationForest(hyper_parameter)
        
        if self.model_type == 'LocalOutlierFactor':
            hyper_parameter = self.hyper_params['LocalOutlierFactor']
            model = LocalOutlierFactor(hyper_parameter)
        
        return model

    def fit_(self, model, data):
        """
        Returns fitted model 
        
        """
        # Gefittet des model noch abspeichern für Fraunhofer?
        return model.fit(data)

    def predict_(self, model, data):

        """
        Predicts if data point is a anomaly, calculates score function and adds it to the dataframe.


        """

        predictions = model.predict(data)
        score = model.decision_function(data)
        data['anomaly']= predictions
        data ['score'] = score
        data['anomaly'] = data['anomaly'].mask(data['anomaly']==1, 0) # one is zero now and represents normal data points
        data['anomaly'] = data['anomaly'].mask(data['anomaly']==-1, 1) # -1 is 1 now and represents unnormal data points
        
        return predictions, score, data

    def evaluate(self):


        return



        # Method evalutate mit validation data 

        # calcualte f1 score
        # confusion matrix 
    