from datetime import datetime
from app import db

class Trip(db.Model):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    origin = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    origin_lat = db.Column(db.Float)
    origin_lng = db.Column(db.Float)
    dest_lat = db.Column(db.Float)
    dest_lng = db.Column(db.Float)
    distance_km = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    transfers = db.Column(db.Integer, default=0)
    co2_saved = db.Column(db.Float, nullable=False)
    transit_co2 = db.Column(db.Float, nullable=False)
    car_co2 = db.Column(db.Float, nullable=False)
    mode = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'origin': self.origin,
            'destination': self.destination,
            'origin_lat': self.origin_lat,
            'origin_lng': self.origin_lng,
            'dest_lat': self.dest_lat,
            'dest_lng': self.dest_lng,
            'distance_km': self.distance_km,
            'duration_minutes': self.duration_minutes,
            'cost': self.cost,
            'transfers': self.transfers,
            'co2_saved': self.co2_saved,
            'transit_co2': self.transit_co2,
            'car_co2': self.car_co2,
            'mode': self.mode,
            'created_at': self.created_at.isoformat()
        }
