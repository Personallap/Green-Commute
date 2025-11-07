from datetime import datetime
from app import db

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    origin = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    total_distance_km = db.Column(db.Float, nullable=False)
    total_duration_minutes = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    total_transfers = db.Column(db.Integer, default=0)
    total_co2 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    segments = db.relationship('RouteSegment', backref='route', lazy=True, cascade='all, delete-orphan')
    trips = db.relationship('Trip', backref='route', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'origin': self.origin,
            'destination': self.destination,
            'total_distance_km': self.total_distance_km,
            'total_duration_minutes': self.total_duration_minutes,
            'total_cost': self.total_cost,
            'total_transfers': self.total_transfers,
            'total_co2': self.total_co2,
            'segments': [segment.to_dict() for segment in self.segments]
        }

class RouteSegment(db.Model):
    __tablename__ = 'route_segments'
    
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    segment_order = db.Column(db.Integer, nullable=False)
    transit_line_id = db.Column(db.Integer, db.ForeignKey('transit_lines.id'), nullable=True)
    start_stop_id = db.Column(db.Integer, db.ForeignKey('transit_stops.id'), nullable=True)
    end_stop_id = db.Column(db.Integer, db.ForeignKey('transit_stops.id'), nullable=True)
    distance_km = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    mode = db.Column(db.String(50), nullable=False)
    co2_emission = db.Column(db.Float, nullable=False)
    
    # Relationships (transit_line backref already defined in TransitLine model)
    start_stop = db.relationship('TransitStop', foreign_keys=[start_stop_id])
    end_stop = db.relationship('TransitStop', foreign_keys=[end_stop_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'segment_order': self.segment_order,
            'transit_line': self.transit_line.to_dict() if self.transit_line else None,
            'start_stop': self.start_stop.to_dict() if self.start_stop else None,
            'end_stop': self.end_stop.to_dict() if self.end_stop else None,
            'distance_km': self.distance_km,
            'duration_minutes': self.duration_minutes,
            'cost': self.cost,
            'mode': self.mode,
            'co2_emission': self.co2_emission
        }
