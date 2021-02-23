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

        # Getting the feature names 
        features_names = model.feature_names

        # Categorical features 
        categorical_features = model.categorical_features

        # Preprocesing input
        input_frame = pd.DataFrame(args, index=[0])

        # Leaving only the present categorical features 
        categorical_features = set(categorical_features).intersection(set(input_frame.columns))

        # Creating additional categorical feature values 
        for categorical_feature in categorical_features:
            input_frame[f'{categorical_feature}_{input_frame[categorical_feature].values[0]}'] = 1

        # Cheking if all values are present 
        if input_frame.isnull().values.any():
            return 'Some input values are NaN', 422

        # Filling missing categorical features 
        missing_cols = set(features_names) - set(input_frame.columns)
        for col in missing_cols:
            input_frame[col] = 0 

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
