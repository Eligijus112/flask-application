from flask_restful import Resource, reqparse
from models.LogisticModel import LogisticModel 
from flask import request
import numpy as np 


class GetPrediction(Resource):

    def get(self, version):
        args = request.args

        # Getting the model version 
        model = LogisticModel.query.filter_by(version=version).all()

        # Getting the features - coef dict 
        modelDict = {x.feature : x.coef for x in model if x.feature!='intercept'} 

        # Forecasting 
        try:
            x = np.sum([float(args.get(x)) * modelDict.get(x) for x in modelDict.keys()])
            x += [x.coef for x in model if x.feature=='intercept'][0]
            p = 1 / (1 + np.exp(-x))

            return {'probability': p}, 200 
        except Exception as e:
            return {'error': str(e)}, 400
