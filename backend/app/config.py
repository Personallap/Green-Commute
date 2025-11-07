import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///greencommute.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CO2_PER_KM_CAR = 120
    CO2_PER_KM_BUS = 30
    CO2_PER_KM_METRO = 20
    CO2_PER_KM_TRAIN = 25
    
    AVG_SPEED_BUS = 25
    AVG_SPEED_METRO = 40
    AVG_SPEED_TRAIN = 60
    TRANSFER_TIME_MINUTES = 5
