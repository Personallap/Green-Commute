from app import create_app, db
from app.models import User, TransitStop, TransitLine, StopConnection

def seed_database():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("Creating sample users...")
        users_data = [
            {'username': 'rahul_student', 'email': 'rahul@example.com', 'password': 'password123', 'total_co2_saved': 250.5},
            {'username': 'shreya_tech', 'email': 'shreya@example.com', 'password': 'password123', 'total_co2_saved': 180.3},
            {'username': 'karan_eco', 'email': 'karan@example.com', 'password': 'password123', 'total_co2_saved': 420.7},
            {'username': 'priya_commuter', 'email': 'priya@example.com', 'password': 'password123', 'total_co2_saved': 350.0},
            {'username': 'amit_green', 'email': 'amit@example.com', 'password': 'password123', 'total_co2_saved': 290.8}
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                total_co2_saved=user_data['total_co2_saved']
            )
            user.set_password(user_data['password'])
            users.append(user)
        
        for user in users:
            db.session.add(user)
        
        print("Creating transit stops...")
        stops = [
            TransitStop(name='Connaught Place', latitude=28.6304, longitude=77.2177, stop_type='metro'),
            TransitStop(name='Rajiv Chowk Metro', latitude=28.6328, longitude=77.2197, stop_type='metro'),
            TransitStop(name='New Delhi Railway Station', latitude=28.6431, longitude=77.2197, stop_type='train'),
            TransitStop(name='Kashmere Gate', latitude=28.6668, longitude=77.2282, stop_type='metro'),
            TransitStop(name='ISBT Kashmere Gate', latitude=28.6675, longitude=77.2295, stop_type='bus'),
            
            TransitStop(name='Dwarka Sector 21 Metro', latitude=28.5521, longitude=77.0590, stop_type='metro'),
            TransitStop(name='Dwarka Sector 9', latitude=28.5690, longitude=77.0730, stop_type='metro'),
            TransitStop(name='Dwarka Sector 10', latitude=28.5850, longitude=77.0650, stop_type='metro'),
            TransitStop(name='Dwarka Main Market', latitude=28.5600, longitude=77.0620, stop_type='bus'),
            
            TransitStop(name='Noida City Center', latitude=28.5748, longitude=77.3560, stop_type='metro'),
            TransitStop(name='Noida Sector 18', latitude=28.5694, longitude=77.3271, stop_type='metro'),
            TransitStop(name='Noida Sector 52', latitude=28.5860, longitude=77.3560, stop_type='metro'),
            TransitStop(name='Botanical Garden Metro', latitude=28.5638, longitude=77.3346, stop_type='metro'),
            TransitStop(name='Noida Electronic City', latitude=28.5900, longitude=77.3600, stop_type='bus'),
            
            TransitStop(name='Gurgaon Cyber City', latitude=28.4950, longitude=77.0870, stop_type='metro'),
            TransitStop(name='MG Road Metro Gurgaon', latitude=28.4817, longitude=77.0873, stop_type='metro'),
            TransitStop(name='Sikanderpur Metro', latitude=28.4816, longitude=77.0932, stop_type='metro'),
            TransitStop(name='IFFCO Chowk', latitude=28.4728, longitude=77.0688, stop_type='metro'),
            TransitStop(name='Gurgaon Sector 29', latitude=28.4620, longitude=77.0560, stop_type='bus'),
            
            TransitStop(name='Nehru Place Metro', latitude=28.5494, longitude=77.2501, stop_type='metro'),
            TransitStop(name='Kalkaji Mandir', latitude=28.5496, longitude=77.2588, stop_type='metro'),
            TransitStop(name='Greater Kailash', latitude=28.5417, longitude=77.2422, stop_type='bus'),
            TransitStop(name='South Extension', latitude=28.5700, longitude=77.2230, stop_type='bus'),
            
            TransitStop(name='Anand Vihar ISBT', latitude=28.6469, longitude=77.3158, stop_type='bus'),
            TransitStop(name='Anand Vihar Railway Station', latitude=28.6472, longitude=77.3161, stop_type='train'),
            TransitStop(name='Laxmi Nagar Metro', latitude=28.6348, longitude=77.2777, stop_type='metro'),
            TransitStop(name='Preet Vihar', latitude=28.6407, longitude=77.2977, stop_type='metro'),
            
            TransitStop(name='Saket Metro', latitude=28.5244, longitude=77.2066, stop_type='metro'),
            TransitStop(name='Malviya Nagar', latitude=28.5355, longitude=77.2053, stop_type='metro'),
            TransitStop(name='Hauz Khas Metro', latitude=28.5494, longitude=77.2067, stop_type='metro'),
            TransitStop(name='Green Park Metro', latitude=28.5598, longitude=77.2067, stop_type='metro')
        ]
        
        for stop in stops:
            db.session.add(stop)
        
        db.session.flush()
        
        print("Creating transit lines...")
        lines = [
            TransitLine(
                line_name='Yellow Line',
                line_number='YL',
                mode='metro',
                cost_per_km=2.0,
                avg_speed_kmh=40,
                co2_per_km=20,
                color='#FFFF00',
                is_electric=True,
                service_provider='Delhi Metro',
                vehicle_type='Metro Train'
            ),
            TransitLine(
                line_name='Blue Line',
                line_number='BL',
                mode='metro',
                cost_per_km=2.0,
                avg_speed_kmh=40,
                co2_per_km=20,
                color='#0000FF',
                is_electric=True,
                service_provider='Delhi Metro',
                vehicle_type='Metro Train'
            ),
            TransitLine(
                line_name='Red Line',
                line_number='RL',
                mode='metro',
                cost_per_km=2.0,
                avg_speed_kmh=40,
                co2_per_km=20,
                color='#FF0000',
                is_electric=True,
                service_provider='Delhi Metro',
                vehicle_type='Metro Train'
            ),
            TransitLine(
                line_name='Magenta Line',
                line_number='ML',
                mode='metro',
                cost_per_km=2.0,
                avg_speed_kmh=40,
                co2_per_km=18,
                color='#FF00FF',
                is_electric=True,
                service_provider='Delhi Metro',
                vehicle_type='Metro Train'
            ),
            TransitLine(
                line_name='DTC Electric Bus E1',
                line_number='E1',
                mode='bus',
                cost_per_km=1.2,
                avg_speed_kmh=28,
                co2_per_km=15,
                color='#00CC00',
                is_electric=True,
                service_provider='DTC',
                vehicle_type='Electric Bus'
            ),
            TransitLine(
                line_name='DTC Electric Bus E2',
                line_number='E2',
                mode='bus',
                cost_per_km=1.2,
                avg_speed_kmh=28,
                co2_per_km=15,
                color='#00CC00',
                is_electric=True,
                service_provider='DTC',
                vehicle_type='Electric Bus'
            ),
            TransitLine(
                line_name='DTC Bus 764',
                line_number='764',
                mode='bus',
                cost_per_km=1.5,
                avg_speed_kmh=25,
                co2_per_km=30,
                color='#00AA00',
                is_electric=False,
                service_provider='DTC',
                vehicle_type='Diesel Bus'
            ),
            TransitLine(
                line_name='DTC Bus 534',
                line_number='534',
                mode='bus',
                cost_per_km=1.5,
                avg_speed_kmh=25,
                co2_per_km=30,
                color='#00AA00',
                is_electric=False,
                service_provider='DTC',
                vehicle_type='Diesel Bus'
            ),
            TransitLine(
                line_name='Rapido E-Bike',
                line_number='RAPIDO',
                mode='bike',
                cost_per_km=3.5,
                avg_speed_kmh=30,
                co2_per_km=5,
                color='#FFA500',
                is_electric=True,
                service_provider='Rapido',
                vehicle_type='Electric Scooter'
            ),
            TransitLine(
                line_name='Uber Moto E-Scooter',
                line_number='UBER-E',
                mode='bike',
                cost_per_km=4.0,
                avg_speed_kmh=32,
                co2_per_km=5,
                color='#000000',
                is_electric=True,
                service_provider='Uber',
                vehicle_type='Electric Scooter'
            ),
            TransitLine(
                line_name='Uber Premier Electric',
                line_number='UBER-PREM',
                mode='car',
                cost_per_km=8.5,
                avg_speed_kmh=35,
                co2_per_km=10,
                color='#000000',
                is_electric=True,
                service_provider='Uber',
                vehicle_type='Electric Car'
            ),
            TransitLine(
                line_name='BluSmart Electric Cab',
                line_number='BLUSMART',
                mode='car',
                cost_per_km=7.5,
                avg_speed_kmh=35,
                co2_per_km=8,
                color='#0066CC',
                is_electric=True,
                service_provider='BluSmart',
                vehicle_type='Electric Car'
            ),
            TransitLine(
                line_name='Rajdhani Express',
                line_number='RE',
                mode='train',
                cost_per_km=2.5,
                avg_speed_kmh=60,
                co2_per_km=25,
                color='#FF8800',
                is_electric=False,
                service_provider='Indian Railways',
                vehicle_type='Train'
            ),
            TransitLine(
                line_name='Local Train',
                line_number='LOCAL',
                mode='train',
                cost_per_km=1.8,
                avg_speed_kmh=45,
                co2_per_km=22,
                color='#888888',
                is_electric=False,
                service_provider='Indian Railways',
                vehicle_type='Train'
            )
        ]
        
        for line in lines:
            db.session.add(line)
        
        db.session.flush()
        
        print("Creating stop connections...")
        
        connections = [
            StopConnection(from_stop_id=1, to_stop_id=2, line_id=1, distance_km=0.5, duration_minutes=2),
            StopConnection(from_stop_id=2, to_stop_id=4, line_id=1, distance_km=3.2, duration_minutes=8),
            StopConnection(from_stop_id=4, to_stop_id=26, line_id=1, distance_km=7.5, duration_minutes=18),
            StopConnection(from_stop_id=26, to_stop_id=27, line_id=1, distance_km=2.8, duration_minutes=7),
            StopConnection(from_stop_id=27, to_stop_id=10, line_id=2, distance_km=8.5, duration_minutes=20),
            
            StopConnection(from_stop_id=1, to_stop_id=31, line_id=1, distance_km=4.2, duration_minutes=10),
            StopConnection(from_stop_id=31, to_stop_id=30, line_id=1, distance_km=1.8, duration_minutes=5),
            StopConnection(from_stop_id=30, to_stop_id=29, line_id=1, distance_km=2.1, duration_minutes=6),
            StopConnection(from_stop_id=29, to_stop_id=28, line_id=1, distance_km=2.5, duration_minutes=7),
            
            StopConnection(from_stop_id=2, to_stop_id=13, line_id=2, distance_km=12.5, duration_minutes=30),
            StopConnection(from_stop_id=13, to_stop_id=11, line_id=2, distance_km=3.8, duration_minutes=9),
            StopConnection(from_stop_id=11, to_stop_id=10, line_id=2, distance_km=4.2, duration_minutes=10),
            
            StopConnection(from_stop_id=2, to_stop_id=20, line_id=1, distance_km=6.5, duration_minutes=16),
            StopConnection(from_stop_id=20, to_stop_id=21, line_id=1, distance_km=1.5, duration_minutes=4),
            
            StopConnection(from_stop_id=1, to_stop_id=17, line_id=1, distance_km=15.8, duration_minutes=38),
            StopConnection(from_stop_id=17, to_stop_id=16, line_id=1, distance_km=1.2, duration_minutes=3),
            StopConnection(from_stop_id=16, to_stop_id=15, line_id=1, distance_km=2.5, duration_minutes=6),
            StopConnection(from_stop_id=16, to_stop_id=18, line_id=1, distance_km=1.8, duration_minutes=5),
            
            StopConnection(from_stop_id=1, to_stop_id=6, line_id=2, distance_km=18.5, duration_minutes=44),
            StopConnection(from_stop_id=6, to_stop_id=7, line_id=2, distance_km=2.8, duration_minutes=7),
            StopConnection(from_stop_id=7, to_stop_id=8, line_id=2, distance_km=1.5, duration_minutes=4),
            
            StopConnection(from_stop_id=5, to_stop_id=24, line_id=7, distance_km=14.2, duration_minutes=34),
            StopConnection(from_stop_id=24, to_stop_id=27, line_id=7, distance_km=4.5, duration_minutes=11),
            
            StopConnection(from_stop_id=1, to_stop_id=22, line_id=8, distance_km=5.8, duration_minutes=14),
            StopConnection(from_stop_id=22, to_stop_id=23, line_id=8, distance_km=2.5, duration_minutes=6),
            StopConnection(from_stop_id=23, to_stop_id=28, line_id=8, distance_km=3.2, duration_minutes=8),
            
            StopConnection(from_stop_id=9, to_stop_id=6, line_id=5, distance_km=2.5, duration_minutes=5),
            StopConnection(from_stop_id=14, to_stop_id=10, line_id=5, distance_km=1.8, duration_minutes=4),
            StopConnection(from_stop_id=19, to_stop_id=15, line_id=5, distance_km=3.2, duration_minutes=7),
            
            StopConnection(from_stop_id=3, to_stop_id=25, line_id=14, distance_km=12.8, duration_minutes=17),
            
            StopConnection(from_stop_id=1, to_stop_id=9, line_id=9, distance_km=18.5, duration_minutes=37),
            StopConnection(from_stop_id=1, to_stop_id=14, line_id=9, distance_km=21.2, duration_minutes=42),
            StopConnection(from_stop_id=1, to_stop_id=19, line_id=9, distance_km=16.5, duration_minutes=33),
            
            StopConnection(from_stop_id=1, to_stop_id=9, line_id=10, distance_km=18.5, duration_minutes=35),
            StopConnection(from_stop_id=1, to_stop_id=14, line_id=10, distance_km=21.2, duration_minutes=40),
            
            StopConnection(from_stop_id=1, to_stop_id=6, line_id=11, distance_km=18.5, duration_minutes=32),
            StopConnection(from_stop_id=1, to_stop_id=10, line_id=11, distance_km=24.5, duration_minutes=42),
            StopConnection(from_stop_id=1, to_stop_id=15, line_id=11, distance_km=16.8, duration_minutes=29),
            
            StopConnection(from_stop_id=2, to_stop_id=6, line_id=12, distance_km=18.3, duration_minutes=31),
            StopConnection(from_stop_id=2, to_stop_id=10, line_id=12, distance_km=24.3, duration_minutes=42),
            StopConnection(from_stop_id=2, to_stop_id=15, line_id=12, distance_km=16.5, duration_minutes=28)
        ]
        
        # Add connections in both directions for bidirectional routing
        print("Creating bidirectional connections...")
        for connection in connections:
            # Add original direction
            db.session.add(connection)
            # Add reverse direction
            reverse_connection = StopConnection(
                from_stop_id=connection.to_stop_id,
                to_stop_id=connection.from_stop_id,
                line_id=connection.line_id,
                distance_km=connection.distance_km,
                duration_minutes=connection.duration_minutes
            )
            db.session.add(reverse_connection)
        
        db.session.commit()
        
        total_connections = len(connections) * 2  # Count both directions
        
        print("\n" + "=" * 80)
        print("Database seeded successfully!")
        print("=" * 80)
        print(f"[+] Created {len(users)} users")
        print(f"[+] Created {len(stops)} transit stops")
        print(f"[+] Created {len(lines)} transit lines")
        print(f"[+] Created {total_connections} stop connections (bidirectional)")
        print("\n[*] Major Route Pairs Available:")
        print("  1. Connaught Place -> Noida City Center")
        print("  2. Connaught Place -> Dwarka Sector 21")
        print("  3. Connaught Place -> Gurgaon Cyber City")
        print("  4. Kashmere Gate -> Anand Vihar ISBT")
        print("  5. Connaught Place -> Saket Metro")
        print("\n[*] Transit Options:")
        print("  - Delhi Metro (Yellow, Blue, Red, Magenta Lines)")
        print("  - Electric Buses (DTC E1, E2)")
        print("  - Diesel Buses (DTC 764, 534)")
        print("  - Electric Scooters (Rapido, Uber Moto)")
        print("  - Electric Cars (Uber Premier, BluSmart)")
        print("  - Trains (Rajdhani Express, Local)")
        print("=" * 80)

if __name__ == '__main__':
    seed_database()
