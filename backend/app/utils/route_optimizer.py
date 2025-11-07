import heapq
from typing import List, Dict, Tuple
from app.utils.distance_calculator import calculate_distance, calculate_duration
from app.utils.co2_calculator import calculate_co2_emission

class RouteOptimizer:
    def __init__(self, transit_network):
        self.transit_network = transit_network
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = {}
        
        for stop in self.transit_network.get('stops', []):
            graph[stop['id']] = []
        
        for line in self.transit_network.get('lines', []):
            stops = line.get('stops', [])
            for i in range(len(stops) - 1):
                start_stop = stops[i]
                end_stop = stops[i + 1]
                
                distance = calculate_distance(
                    start_stop['lat'], start_stop['lng'],
                    end_stop['lat'], end_stop['lng']
                )
                duration = calculate_duration(distance, line['mode'])
                
                graph[start_stop['id']].append({
                    'to': end_stop['id'],
                    'distance': distance,
                    'duration': duration,
                    'cost': distance * line['cost_per_km'],
                    'mode': line['mode'],
                    'line_id': line['id'],
                    'co2': calculate_co2_emission(distance, line['mode'])
                })
        
        return graph
    
    def find_optimal_route(self, start_stop_id, end_stop_id, optimize_by='time'):
        if start_stop_id not in self.graph or end_stop_id not in self.graph:
            return None
        
        distances = {node: float('infinity') for node in self.graph}
        distances[start_stop_id] = 0
        
        previous = {node: None for node in self.graph}
        visited = set()
        
        priority_queue = [(0, start_stop_id, [])]
        
        while priority_queue:
            current_cost, current_node, path = heapq.heappop(priority_queue)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end_stop_id:
                return self._reconstruct_path(path, optimize_by)
            
            for edge in self.graph.get(current_node, []):
                neighbor = edge['to']
                
                if neighbor in visited:
                    continue
                
                if optimize_by == 'time':
                    weight = edge['duration']
                elif optimize_by == 'cost':
                    weight = edge['cost']
                elif optimize_by == 'co2':
                    weight = edge['co2']
                else:
                    weight = edge['duration']
                
                new_cost = current_cost + weight
                
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_node
                    new_path = path + [edge]
                    heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
        
        return None
    
    def _reconstruct_path(self, edges, optimize_by):
        if not edges:
            return None
        
        total_distance = sum(e['distance'] for e in edges)
        total_duration = sum(e['duration'] for e in edges)
        total_cost = sum(e['cost'] for e in edges)
        total_co2 = sum(e['co2'] for e in edges)
        
        transfers = self._count_transfers(edges)
        
        return {
            'segments': edges,
            'total_distance': round(total_distance, 2),
            'total_duration': round(total_duration, 2),
            'total_cost': round(total_cost, 2),
            'total_co2': round(total_co2, 2),
            'transfers': transfers
        }
    
    def _count_transfers(self, edges):
        if len(edges) <= 1:
            return 0
        
        transfers = 0
        for i in range(len(edges) - 1):
            if edges[i]['line_id'] != edges[i + 1]['line_id']:
                transfers += 1
        
        return transfers
    
    def get_multiple_routes(self, start_stop_id, end_stop_id):
        routes = []
        
        for optimize_by in ['time', 'cost', 'co2']:
            route = self.find_optimal_route(start_stop_id, end_stop_id, optimize_by)
            if route:
                route['optimized_for'] = optimize_by
                routes.append(route)
        
        return routes
