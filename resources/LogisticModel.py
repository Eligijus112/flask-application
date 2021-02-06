from flask_restful import Resource, reqparse
from models.LogisticModel import LogisticModel 
from flask import request
import numpy as np 
import pickle 
import pandas as pd

model_dicts = {
    'v1': pickle.load(open(f"LRmodels/model_v1.sav", 'rb')),
    'v2': pickle.load(open(f"LRmodels/model_v2.sav", 'rb'))
}


class GetPrediction(Resource):

    def get(self, version):
        args = request.args

        # Getting the model version 
        model = model_dicts.get(version)

        # Getting the feature names 
        features_names = model.feature_names

        # Preprocesing input
        input_frame = pd.DataFrame(args, index=[0])

        # Cheking if all values are present 
        if input_frame.isnull().values.any():
            return 'Some input values are NaN', 422

        # Ensuring that there are no missing features used in the model creation 
        if len(set(input_frame.columns).intersection(set(features_names))) != len(features_names):
            return 'Missing some features; please refer to API docs', 422

        # Ensuring that the features have the same order as in the model creation phase
        input_frame = input_frame[features_names]

        # Converting to appropriate types 
        try:
            input_frame = input_frame.astype(float)
        except Exception as e: 
            return "Cannot convert to float some features", 422

        # Getting the probability of a heart attack
        p = model.predict_proba(input_frame)[0][1]

        # Returning the probability
        return {'probability': p}, 200 
