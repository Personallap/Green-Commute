import math
from app.config import Config

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return round(distance, 2)

def calculate_duration(distance_km, mode):
    speed_map = {
        'bus': Config.AVG_SPEED_BUS,
        'metro': Config.AVG_SPEED_METRO,
        'train': Config.AVG_SPEED_TRAIN,
        'walk': 5
    }
    
    speed = speed_map.get(mode.lower(), Config.AVG_SPEED_BUS)
    duration_hours = distance_km / speed
    duration_minutes = duration_hours * 60
    
    return round(duration_minutes, 2)

def add_transfer_time(duration_minutes, num_transfers):
    return duration_minutes + (num_transfers * Config.TRANSFER_TIME_MINUTES)
