from flask_restful import Resource, reqparse
from models.LogisticModel import LogisticModel 
from flask import request
import numpy as np 
import pickle 
import pandas as pd
from models.Users import Users
from models.Requests import Requests, RequestsInfo
from hashlib import md5
import os 
import datetime

model_dicts = {
    'v1': pickle.load(open(f"LRmodels/model_v1.sav", 'rb')),
    'v2': pickle.load(open(f"LRmodels/model_v2.sav", 'rb')),
    'v3': pickle.load(open(f"LRmodels/model_v3.sav", 'rb'))
}


class GetPrediction(Resource):

    def get(self, version):
        # Getting username and password 
        username = request.args.get("username", request.form.get("username"))
        password = request.args.get("password", request.form.get("password"))

        # Checking if the correct credentials are sent in the request form
        usr = Users.query.filter_by(username=username).first()

        if not usr:
            return {"message": "User not found"}, 400

        psw_hash = md5(f"{password}{os.environ['SECRET_KEY']}".encode()).hexdigest()
        if usr.password != psw_hash:
            return {"message": "User password is incorect"}, 400

        # Getting the GET arguments 
        args = request.args

        # Getting the model version 
        model = model_dicts.get(version)

        # Getting the feature names; These feature names need to be present in order to get 
        # predictions 
        features_names = model.feature_names

        # Preprocesing input
        input_frame = pd.DataFrame(args, index=[0])

        # Extracting categorical feature list  
        categorical_features = []
        try:
            categorical_features = model.categorical_features

            # Checking if all the categorical features are present in the request
            missing_categoricals = set(categorical_features) - set(input_frame.columns)
            if len(missing_categoricals) > 0:
                return {"message": f"Missing the following categorical features: {missing_categoricals}"}, 400
        except: 
            pass 

        # Extracting numerical feature list 
        numeric_features = []
        try:
            numeric_features = model.numeric_features

            # Checking if all the numeric features are present in the request
            numeric_features = set(numeric_features) - set(input_frame.columns)
            if len(numeric_features) > 0:
                return {"message": f"Missing the following numeric features: {numeric_features}"}, 400
        except: 
            pass

        # Dealing with categorical variables if the model has them 
        if len(categorical_features)!=0:
            
            # Getting the categorical features sent in request 
            categorical_features_sent = set(categorical_features).intersection(set(input_frame.columns))

            # Creating additional categorical feature values 
            for feature in categorical_features_sent:
                input_frame[f'{feature}_{input_frame[feature].values[0]}'] = 1

        # Cheking if all values are present 
        if input_frame.isnull().values.any():
            return 'Some input values are NaN', 422

        # Filling missing feature values; This will only adjust the categorical features 
        missing_cols = set(features_names) - set(input_frame.columns)
        for col in missing_cols:
            input_frame[col] = 0 

        # Ensuring that the features have the same order as in the model creation phase
        input_frame = input_frame[features_names]

        # Converting to appropriate types 
        try:
            input_frame = input_frame.astype(float)
        except Exception as e: 
            return f"Cannot convert to float some features {e}", 422

        # Getting the probability of a heart attack
        p = model.predict_proba(input_frame)[0][1]

        # Saving the information to the requests table 
        req = Requests(usr.id, datetime.datetime.now())
        req.save_to_db()

        # Saving a more in depth information about request 
        input_frame = input_frame.melt()
        for _, row in input_frame.iterrows():
            obj = RequestsInfo(
                req.id, 
                version,
                row['variable'],
                row['value']
            )
            obj.save_to_db()

        # Returning the probability
        return {'probability': p}, 200 
