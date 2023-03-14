#!/usr/bin/venv python
import joblib
import pickle
import pandas as pd
from keras.models import load_model

#TODO: "Load and Save VAE MODEL
def validate(src:str):

    """Script to validate VAE"""


    src = "data/model/CVE-2012-2122/VAE.h5"
    vae = load_model(src)






    return 