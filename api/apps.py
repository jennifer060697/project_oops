from django.apps import AppConfig
from api.deep_model import combined_model
import pandas as pd


class SearchConfig(AppConfig):
    name = 'api'
    model = combined_model
    df = pd.read_csv('stores_info.csv')
    stores_inf = df.to_dict('records')