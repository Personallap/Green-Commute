from app import db

class TransitStop(db.Model):
    __tablename__ = 'transit_stops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    stop_type = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'stop_type': self.stop_type
        }

class TransitLine(db.Model):
    __tablename__ = 'transit_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(100), nullable=False)
    line_number = db.Column(db.String(50))
    mode = db.Column(db.String(50), nullable=False)
    cost_per_km = db.Column(db.Float, nullable=False)
    avg_speed_kmh = db.Column(db.Float, nullable=False)
    co2_per_km = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20))
    is_electric = db.Column(db.Boolean, default=False)
    service_provider = db.Column(db.String(100))
    vehicle_type = db.Column(db.String(50))
    
    segments = db.relationship('RouteSegment', backref='transit_line', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'line_name': self.line_name,
            'line_number': self.line_number,
            'mode': self.mode,
            'cost_per_km': self.cost_per_km,
            'avg_speed_kmh': self.avg_speed_kmh,
            'co2_per_km': self.co2_per_km,
            'color': self.color,
            'is_electric': self.is_electric,
            'service_provider': self.service_provider,
            'vehicle_type': self.vehicle_type
        }

class StopConnection(db.Model):
    __tablename__ = 'stop_connections'
    
    id = db.Column(db.Integer, primary_key=True)
    from_stop_id = db.Column(db.Integer, db.ForeignKey('transit_stops.id'), nullable=False)
    to_stop_id = db.Column(db.Integer, db.ForeignKey('transit_stops.id'), nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey('transit_lines.id'), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Float, nullable=False)
    
    from_stop = db.relationship('TransitStop', foreign_keys=[from_stop_id])
    to_stop = db.relationship('TransitStop', foreign_keys=[to_stop_id])
    line = db.relationship('TransitLine')
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_stop': self.from_stop.to_dict() if self.from_stop else None,
            'to_stop': self.to_stop.to_dict() if self.to_stop else None,
            'line': self.line.to_dict() if self.line else None,
            'distance_km': self.distance_km,
            'duration_minutes': self.duration_minutes
        }
