import pandas as pd
import json



def to_json(Dataset: pd.DataFrame)->json:
	#'''
	#Conversion du Dataset en format json
	#'''
    return Dataset.to_json(orient="index")