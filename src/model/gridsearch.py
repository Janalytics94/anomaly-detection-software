#!/usr/bin/env python
import os
import pandas as pd
import dvc.api
import logging
import random
import json
from sklearn import preprocessing

from sklearn.metrics import (
    roc_curve, auc, confusion_matrix, 
    )

from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LocalOutlierFactor
from pyod.models.knn import KNN
from pyod.models.vae import VAE
from clize import run

def gridsearch(src: str, target: str, scenario: str, model_type: str, iteration: int):

    """
    Script for Hyperparameter Tuning
    
    Regarding the validation of the VAE please check validate.py
    
    """


    _logger = logging.getLogger(__name__)

    hyper_params = dvc.api.params_show(os.path.join(os.path.dirname(__file__), "..", "..", "src/model/gridsearch.yaml"))
    #hyper_params = dvc.api.params_show("src/model/gridsearch.yaml")
    # Scaler
    standard_scaler = StandardScaler()
    

    _logger.warning("Load relevant data...")
    X_train = pd.read_csv(src + "/" + scenario + "/train.csv", sep=';')
    X_train.pop("Unnamed: 0")
    X_train = X_train.fillna(0)

    X_test = pd.read_csv(src + "/" + scenario + "/test.csv", sep=';')
    X_test.pop("Unnamed: 0")
    X_test = X_test.fillna(0)

    y_true = pd.read_csv(src+ "/" + scenario + "/y_test.csv", sep=';')
    y_true = y_true.fillna(0)
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

       
        # chose Hyperparams randomly
        for i in range(0, iteration):
            model = IForest(n_estimators = random.choice(n_estimators) , max_samples=max_samples, 
                            contamination=random.choice(contamination), max_features=random.choice(max_features),
                            bootstrap=random.choice(bootstrap), n_jobs=n_jobs,
                            random_state=random_state, verbose=verbose).fit(X_train)
            

            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            
            #_logger.warning("Start evaluating performance measures...")
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
            dict_ = {
            "round":i,
            "model":model_type, 
            "params": model.get_params(),
            "FPR":FPR,
            "FNR" : FNR,
            "RCL" : RCL,
            "PRC" : PRC,
            "ACC" : ACC,
            "F1" : F1,
            "AUC": AUC
            }
            with open(target + "/" + scenario + "/gridsearch_" + model_type + ".txt", "a") as outfile:
                outfile.write(str(dict_))
                outfile.write("\n")
            
    if model_type == "KNN":
        hyper_parameter = hyper_params[model_type]
        contamination =  hyper_parameter['contamination']
        n_neighbours =  hyper_parameter['n_neighbours']
        method =  hyper_parameter['method']
        radius =  hyper_parameter['radius']
        algorithm = hyper_parameter['algorithm']
        leaf_size =  hyper_parameter['leaf_size']
        metric =  hyper_parameter['metric']
        p =  hyper_parameter['p']
        n_jobs =  hyper_parameter['n_jobs']

        X_train = standard_scaler.fit_transform(X_train)

        for i in range(0, iteration):
            # chose Hyperparams randomly
            model = KNN(contamination= random.choice(contamination), n_neighbors=random.choice(n_neighbours), 
                            method=random.choice(method), radius=random.choice(radius),
                            algorithm=random.choice(algorithm), leaf_size=random.choice(leaf_size),
                            metric=random.choice(metric), p=random.choice(p), n_jobs=n_jobs).fit(X_train)
            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            
            #_logger.warning("Start evaluating performance measures...")
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
            dict_ = {
                "round":i,
                "model":model_type, 
                "params": model.get_params(),
                "FPR":FPR,
                "FNR" : FNR,
                "RCL" : RCL,
                "PRC" : PRC,
                "ACC" : ACC,
                "F1" : F1,
                "AUC": AUC
            }
            with open(target + "/" + scenario + "/gridsearch_" + model_type + ".txt", "a") as outfile:
                outfile.write(str(dict_))
                outfile.write("\n")
                    
           
    if model_type == "LOF":
        hyper_parameter = hyper_params[model_type]
        n_neighbors= hyper_parameter['n_neighbors']
        algorithm = hyper_parameter['algorithm']
        leaf_size = hyper_parameter['leaf_size']
        p = hyper_parameter['p']
        contamination = hyper_parameter['contamination']
        novelty = hyper_parameter['novelty']
        n_jobs = hyper_parameter['n_jobs']

        X_train = standard_scaler.fit_transform(X_train)
        for i in range(0, iteration):
            model = LocalOutlierFactor(n_neighbors=random.choice(n_neighbors), algorithm=algorithm,
                            leaf_size=random.choice(leaf_size), p=random.choice(p), contamination=random.choice(contamination),
                            novelty=novelty, n_jobs=n_jobs).fit(X_train)
            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            
            #_logger.warning("Start evaluating performance measures...")
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
            dict_ = {
                "round":i,
                "model":model_type, 
                "params": model.get_params(),
                "FPR":FPR,
                "FNR" : FNR,
                "RCL" : RCL,
                "PRC" : PRC,
                "ACC" : ACC,
                "F1" : F1,
                "AUC": AUC
            }
            with open(target + "/" + scenario + "/gridsearch_" + model_type + ".txt", "a") as outfile:
                outfile.write(str(dict_))
                outfile.write("\n")
    
    if model_type == "VAE":
        hyper_parameter = hyper_params[model_type]
        encoder_neurons = hyper_parameter['encoder_neurons']
        decoder_neurons = hyper_parameter['decoder_neurons']
        hidden_activation = hyper_parameter['hidden_activation']
        output_activation = hyper_parameter['output_activation']
        optimizer = hyper_parameter['optimizer']
        epochs = hyper_parameter['epochs']
        batch_size = hyper_parameter['batch_size']
        dropout_rate = hyper_parameter['dropout_rate']
        contamination = hyper_parameter['contamination']
        l2_regularizer =  hyper_parameter['l2_regularizer']
        validation_size =  hyper_parameter['validation_size']
        preprocessing = hyper_parameter['preprocessing']
        verbose = hyper_parameter['verbose']
        random_state = hyper_parameter['random_state']
        gamma = hyper_parameter['gamma']
        capacity = hyper_parameter['capacity']


        X_train = standard_scaler.fit_transform(X_train)
        for i in range(0, iteration):
            model = VAE(encoder_neurons=encoder_neurons, decoder_neurons=decoder_neurons,
                        hidden_activation=hidden_activation, output_activation=output_activation,
                        optimizer= optimizer, epochs=random.choice(epochs),
                        batch_size=random.choice(batch_size), dropout_rate=random.choice(dropout_rate),
                        l2_regularizer=random.choice(l2_regularizer), validation_size=random.choice(validation_size),
                        preprocessing=preprocessing, verbose=verbose, random_state=random_state,
                        contamination=random.choice(contamination), gamma=gamma, capacity=capacity).fit(X_train)
            predictions = model.predict(X_test)
            scores = model.decision_function(X_test)
            
            #_logger.warning("Start evaluating performance measures...")
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
            dict_ = {
                "round":i,
                "model":model_type, 
                "params": model.get_params(),
                "FPR":FPR,
                "FNR" : FNR,
                "RCL" : RCL,
                "PRC" : PRC,
                "ACC" : ACC,
                "F1" : F1,
                "AUC": AUC
            }
            with open(target + "/" + scenario + "/gridsearch_" + model_type + ".txt", "a") as outfile:
                outfile.write(str(dict_))
                outfile.write("\n")
                    
                
                    
                
    return

if __name__ == "__main__":
    run(gridsearch)