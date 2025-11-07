from app.config import Config

def calculate_co2_emission(distance_km, mode):
    co2_rates = {
        'car': Config.CO2_PER_KM_CAR,
        'bus': Config.CO2_PER_KM_BUS,
        'metro': Config.CO2_PER_KM_METRO,
        'train': Config.CO2_PER_KM_TRAIN
    }
    
    rate = co2_rates.get(mode.lower(), Config.CO2_PER_KM_BUS)
    return distance_km * rate

def calculate_co2_saved(distance_km, transit_mode='bus'):
    car_emission = calculate_co2_emission(distance_km, 'car')
    transit_emission = calculate_co2_emission(distance_km, transit_mode)
    
    return {
        'car_co2': round(car_emission, 2),
        'transit_co2': round(transit_emission, 2),
        'co2_saved': round(car_emission - transit_emission, 2)
    }

def calculate_route_co2(segments):
    total_co2 = 0
    for segment in segments:
        total_co2 += calculate_co2_emission(segment['distance_km'], segment['mode'])
    return round(total_co2, 2)
