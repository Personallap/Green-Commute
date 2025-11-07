from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Trip, Route, RouteSegment, TransitStop, TransitLine, StopConnection
from app.utils import calculate_co2_saved, RouteOptimizer, calculate_distance
from datetime import datetime
import heapq

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'GreenCommute API is running'}), 200

@bp.route('/routes/search', methods=['POST'])
def search_routes():
    data = request.get_json()
    
    origin = data.get('origin')
    destination = data.get('destination')
    
    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400
    
    start_stop = _find_stop_by_name(origin)
    end_stop = _find_stop_by_name(destination)
    
    if not start_stop:
        return jsonify({
            'error': f'Transit stop not found for origin: {origin}',
            'available_stops': [stop.name for stop in TransitStop.query.all()]
        }), 404
    
    if not end_stop:
        return jsonify({
            'error': f'Transit stop not found for destination: {destination}',
            'available_stops': [stop.name for stop in TransitStop.query.all()]
        }), 404
    
    routes = _find_all_routes(start_stop, end_stop, origin, destination)
    
    if not routes:
        distance_km = calculate_distance(
            start_stop.latitude, start_stop.longitude,
            end_stop.latitude, end_stop.longitude
        )
        routes = _generate_sample_routes(
            origin, destination, 
            start_stop.latitude, start_stop.longitude, 
            end_stop.latitude, end_stop.longitude, 
            distance_km
        )
    
    best_route = _select_best_route(routes)
    
    return jsonify({
        'routes': routes,
        'best_route': best_route,
        'start_stop': start_stop.to_dict(),
        'end_stop': end_stop.to_dict()
    }), 200

@bp.route('/stops', methods=['GET'])
def get_all_stops():
    stops = TransitStop.query.all()
    return jsonify({
        'stops': [{'id': stop.id, 'name': stop.name} for stop in stops]
    }), 200

@bp.route('/trips', methods=['POST'])
def save_trip():
    data = request.get_json()
    
    try:
        trip = Trip(
            user_id=data.get('user_id'),
            origin=data['origin'],
            destination=data['destination'],
            origin_lat=data.get('origin_lat'),
            origin_lng=data.get('origin_lng'),
            dest_lat=data.get('dest_lat'),
            dest_lng=data.get('dest_lng'),
            distance_km=data['distance_km'],
            duration_minutes=data['duration_minutes'],
            cost=data['cost'],
            transfers=data.get('transfers', 0),
            co2_saved=data['co2_saved'],
            transit_co2=data['transit_co2'],
            car_co2=data['car_co2']
        )
        
        db.session.add(trip)
        
        if data.get('user_id'):
            user = User.query.get(data['user_id'])
            if user:
                user.total_co2_saved += data['co2_saved']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip saved successfully',
            'trip': trip.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/trips/<int:user_id>', methods=['GET'])
def get_user_trips(user_id):
    trips = Trip.query.filter_by(user_id=user_id).order_by(Trip.created_at.desc()).all()
    
    return jsonify({
        'trips': [trip.to_dict() for trip in trips],
        'total_trips': len(trips)
    }), 200

@bp.route('/trips/stats/<int:user_id>', methods=['GET'])
def get_trip_stats(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    trips = Trip.query.filter_by(user_id=user_id).all()
    
    total_trips = len(trips)
    total_distance = sum(trip.distance_km for trip in trips)
    total_co2_saved = sum(trip.co2_saved for trip in trips)
    total_cost = sum(trip.cost for trip in trips)
    
    return jsonify({
        'user_id': user_id,
        'username': user.username,
        'total_trips': total_trips,
        'total_distance_km': round(total_distance, 2),
        'total_co2_saved': round(total_co2_saved, 2),
        'total_cost': round(total_cost, 2),
        'average_co2_per_trip': round(total_co2_saved / total_trips, 2) if total_trips > 0 else 0
    }), 200

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400
    
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409
    
    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@bp.route('/transit/stops', methods=['GET'])
def get_transit_stops():
    stops = TransitStop.query.all()
    return jsonify({'stops': [stop.to_dict() for stop in stops]}), 200

@bp.route('/transit/lines', methods=['GET'])
def get_transit_lines():
    lines = TransitLine.query.all()
    return jsonify({'lines': [line.to_dict() for line in lines]}), 200

@bp.route('/co2/compare', methods=['POST'])
def compare_co2():
    data = request.get_json()
    
    distance_km = data.get('distance_km')
    transit_mode = data.get('transit_mode', 'bus')
    
    if not distance_km:
        return jsonify({'error': 'Distance is required'}), 400
    
    result = calculate_co2_saved(distance_km, transit_mode)
    
    return jsonify(result), 200

def _get_transit_network():
    stops = TransitStop.query.all()
    lines = TransitLine.query.all()
    
    return {
        'stops': [stop.to_dict() for stop in stops],
        'lines': [{
            **line.to_dict(),
            'stops': []
        } for line in lines]
    }

def _generate_sample_routes(origin, destination, origin_lat, origin_lng, dest_lat, dest_lng, distance_km):
    routes = []
    
    modes = [
        {'name': 'Metro + Bus', 'mode': 'metro', 'speed': 40, 'cost_per_km': 2, 'co2_per_km': 20},
        {'name': 'Bus Direct', 'mode': 'bus', 'speed': 25, 'cost_per_km': 1.5, 'co2_per_km': 30},
        {'name': 'Train + Metro', 'mode': 'train', 'speed': 60, 'cost_per_km': 2.5, 'co2_per_km': 25}
    ]
    
    for idx, mode_info in enumerate(modes):
        duration_hours = distance_km / mode_info['speed']
        duration_minutes = duration_hours * 60
        
        if idx > 0:
            duration_minutes += 5
        
        cost = distance_km * mode_info['cost_per_km']
        transit_co2 = distance_km * mode_info['co2_per_km']
        car_co2 = distance_km * 120
        co2_saved = car_co2 - transit_co2
        
        routes.append({
            'name': mode_info['name'],
            'mode': mode_info['mode'],
            'distance_km': round(distance_km, 2),
            'duration_minutes': round(duration_minutes, 2),
            'cost': round(cost, 2),
            'transfers': idx,
            'transit_co2': round(transit_co2, 2),
            'car_co2': round(car_co2, 2),
            'co2_saved': round(co2_saved, 2),
            'segments': [
                {
                    'mode': mode_info['mode'],
                    'distance_km': round(distance_km, 2),
                    'duration_minutes': round(duration_minutes, 2),
                    'cost': round(cost, 2)
                }
            ]
        })
    
    return routes

def _find_stop_by_name(location_name):
    location_lower = location_name.lower().strip()
    
    stops = TransitStop.query.all()
    
    for stop in stops:
        if stop.name.lower() == location_lower:
            return stop
    
    for stop in stops:
        if location_lower in stop.name.lower() or stop.name.lower() in location_lower:
            return stop
    
    return None

def _find_nearest_stop(lat, lng):
    stops = TransitStop.query.all()
    if not stops:
        return None
    
    min_distance = float('inf')
    nearest_stop = None
    
    for stop in stops:
        distance = calculate_distance(lat, lng, stop.latitude, stop.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop
    
    return nearest_stop

def _find_all_routes(start_stop, end_stop, origin_name, dest_name):
    all_routes = []
    
    route_by_time = _find_optimal_route(start_stop.id, end_stop.id, 'time')
    if route_by_time:
        route_by_time['optimization_type'] = 'Fastest'
        route_by_time['origin'] = origin_name
        route_by_time['destination'] = dest_name
        all_routes.append(route_by_time)
    
    route_by_cost = _find_optimal_route(start_stop.id, end_stop.id, 'cost')
    if route_by_cost and route_by_cost not in all_routes:
        route_by_cost['optimization_type'] = 'Cheapest'
        route_by_cost['origin'] = origin_name
        route_by_cost['destination'] = dest_name
        all_routes.append(route_by_cost)
    
    route_by_co2 = _find_optimal_route(start_stop.id, end_stop.id, 'co2')
    if route_by_co2 and route_by_co2 not in all_routes:
        route_by_co2['optimization_type'] = 'Eco-Friendly'
        route_by_co2['origin'] = origin_name
        route_by_co2['destination'] = dest_name
        all_routes.append(route_by_co2)
    
    return all_routes

def _find_optimal_route(start_stop_id, end_stop_id, optimize_by='time'):
    graph = {}
    connections = StopConnection.query.all()
    
    for conn in connections:
        if conn.from_stop_id not in graph:
            graph[conn.from_stop_id] = []
        
        cost = conn.distance_km * conn.line.cost_per_km
        co2 = conn.distance_km * conn.line.co2_per_km
        
        graph[conn.from_stop_id].append({
            'to': conn.to_stop_id,
            'connection': conn,
            'time': conn.duration_minutes,
            'cost': cost,
            'co2': co2,
            'distance': conn.distance_km
        })
    
    if start_stop_id not in graph:
        return None
    
    distances = {node: float('infinity') for node in graph}
    distances[start_stop_id] = 0
    
    previous = {}
    visited = set()
    
    priority_queue = [(0, start_stop_id, [])]
    
    while priority_queue:
        current_weight, current_node, path = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_node == end_stop_id:
            return _reconstruct_route(path, optimize_by)
        
        for edge in graph.get(current_node, []):
            neighbor = edge['to']
            
            if neighbor in visited:
                continue
            
            if optimize_by == 'time':
                weight = edge['time']
            elif optimize_by == 'cost':
                weight = edge['cost']
            elif optimize_by == 'co2':
                weight = edge['co2']
            else:
                weight = edge['time']
            
            new_weight = current_weight + weight
            
            if new_weight < distances[neighbor]:
                distances[neighbor] = new_weight
                previous[neighbor] = current_node
                new_path = path + [edge]
                heapq.heappush(priority_queue, (new_weight, neighbor, new_path))
    
    return None

def _reconstruct_route(edges, optimize_by):
    if not edges:
        return None
    
    segments = []
    total_distance = 0
    total_duration = 0
    total_cost = 0
    total_co2 = 0
    transfers = 0
    last_line_id = None
    
    for edge in edges:
        conn = edge['connection']
        segments.append({
            'from_stop': conn.from_stop.name,
            'to_stop': conn.to_stop.name,
            'line': conn.line.line_name,
            'line_number': conn.line.line_number,
            'mode': conn.line.mode,
            'distance_km': edge['distance'],
            'duration_minutes': edge['time'],
            'cost': edge['cost'],
            'co2': edge['co2'],
            'is_electric': conn.line.is_electric,
            'service_provider': conn.line.service_provider,
            'vehicle_type': conn.line.vehicle_type
        })
        
        total_distance += edge['distance']
        total_duration += edge['time']
        total_cost += edge['cost']
        total_co2 += edge['co2']
        
        if last_line_id is not None and last_line_id != conn.line_id:
            transfers += 1
        last_line_id = conn.line_id
    
    car_co2 = total_distance * 120
    co2_saved = car_co2 - total_co2
    
    return {
        'segments': segments,
        'total_distance_km': round(total_distance, 2),
        'total_duration_minutes': round(total_duration, 2),
        'total_cost': round(total_cost, 2),
        'total_co2': round(total_co2, 2),
        'car_co2': round(car_co2, 2),
        'co2_saved': round(co2_saved, 2),
        'transfers': transfers,
        'optimized_by': optimize_by
    }

def _select_best_route(routes):
    if not routes:
        return None
    
    best_route = None
    best_score = float('inf')
    
    for route in routes:
        cost_weight = 0.3
        co2_weight = 0.5
        time_weight = 0.2
        
        normalized_cost = route.get('total_cost', route.get('cost', 0))
        normalized_co2 = route.get('total_co2', route.get('transit_co2', 0))
        normalized_time = route.get('total_duration_minutes', route.get('duration_minutes', 0))
        
        score = (cost_weight * normalized_cost + 
                co2_weight * normalized_co2 + 
                time_weight * normalized_time)
        
        if score < best_score:
            best_score = score
            best_route = route
    
    return best_route
