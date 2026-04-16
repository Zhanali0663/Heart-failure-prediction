import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro
import sklearn as skl
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
import joblib
from catboost import CatBoostClassifier

model = joblib.load('models/catboost.cbm')
scaler = joblib.load('models/scaler.joblib')

healthy_person = [74, 'F', 'NAP', 125, 215, 0, 'Normal', 150, 'N', 0.0, 'Up']
sick_person = [26, 'M', 'ASY', 140, 290, 1, 'ST', 130, 'Y', 1.8, 'Flat']
columns = [
    'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
    'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 
    'Oldpeak', 'ST_Slope'
]
number = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
expected_columns = model.feature_names_

from fastapi import FastAPI
import random
from pydantic import BaseModel
app = FastAPI()

from typing import Literal
import shap
explainer = shap.TreeExplainer(model)

class ClientData(BaseModel):
    Age: int
    Sex: Literal['M', 'F']
    ChestPainType: Literal['ASY', 'ATA', 'NAP', 'TA']
    RestingBP: int
    Cholesterol: int
    FastingBS: Literal[0, 1]
    RestingECG: Literal['Normal', 'ST', 'LVH']
    MaxHR: int
    ExerciseAngina: Literal['N', 'Y']
    Oldpeak: float
    ST_Slope: Literal['Up', 'Flat', 'Down']


@app.post('/score')
def score(data : ClientData):
    fs = [data.Age, data.Sex, data.ChestPainType, data.RestingBP, data.Cholesterol, data.FastingBS, data.RestingECG, data.MaxHR, data.ExerciseAngina, data.Oldpeak, data.ST_Slope]
    df = pd.DataFrame([fs], columns=columns)

    
    
    df = pd.get_dummies(df, columns=['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope'], dtype=int)
    df = df.reindex(columns=expected_columns, fill_value=0)
    df[number] = scaler.transform(df[number])


    HeartDisease = model.predict(df)[0].item()  
    probability = model.predict_proba(df)[0][1].item()

    shap_values = explainer.shap_values(df)
    feature_importance = dict(zip(expected_columns, shap_values[0]))
    sorted_importance = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
    top_factors = sorted_importance[:3] 

    return {
        'HeartDisease': HeartDisease,
        'Probability': round(probability * 100, 2),
        'TopFactors': top_factors 
    }




