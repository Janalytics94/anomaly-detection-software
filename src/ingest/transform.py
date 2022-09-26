# Imports 
from sklearn import preprocessing
import numpy as np

class Tranformer():
    """
    Different methods to normalize Data
    """

    def __init__(self) -> None:
        pass
    
    def standard(self, x):
        """
        Scaled data has zero mean and unit variance 

        Params:

        Returns:
        
        """

        scaler = preprocessing.StandardScaler()
        x_scaled = scaler.fit_transform(x)

        return x_scaled

    def min_max(self, x):
        """
        Scaling features between a given minimum and a maximum value

        Params:

        Returns:
        
        """

        min_max_scaler = preprocessing.MinMaxScaler()
        x_min_max = min_max_scaler.fit_transform(x)

        return x_min_max
    
    def max_abs(self, x):
        """
        Divides through the largest maximum value in each feature. Meant for data that is already centered at zero or sparse data

        Params:

        Returns:
        
        """

        max_abs_scaler = preprocessing.MaxAbsScaler()
        x_max_abs = max_abs_scaler.fit_transform(x)

        return x_max_abs

    
    def power(self, x, method):
        """
        Maps to a Gaussian Distribution, in order to minimize skewness and stabilize variance

        - Yeo-Johnson transformation
        - Box-Cox transformation (strictly positive data)

        Params:

        Returns:
        """

        if method == "box-cox":
            pt = preprocessing.PowerTransformer(method=method, standardize=False)
        
        if method == "yeo-johnson":
            pt = preprocessing.PowerTransformer(method=method, standardize=False)

        x_new = pt.fit_transform(x)

        return x_new


    




