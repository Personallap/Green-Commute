import sqlite3

db_path = 'instance/greencommute.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 100)
print("GREEN COMMUTE DATABASE - COMPREHENSIVE VIEWER")
print("=" * 100)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [table[0] for table in cursor.fetchall()]
print(f"\n[*] DATABASE TABLES ({len(tables)}):")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  - {table}: {count} records")

print("\n" + "=" * 100)
print("[USERS]")
print("=" * 100)
cursor.execute("SELECT id, username, email, total_co2_saved FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user[0]} | Username: {user[1]:20} | Email: {user[2]:30} | CO2 Saved: {user[3]:.1f}g")

print("\n" + "=" * 100)
print("[TRANSIT STOPS]")
print("=" * 100)
cursor.execute("SELECT id, name, latitude, longitude, stop_type FROM transit_stops ORDER BY id")
stops = cursor.fetchall()
for stop in stops:
    print(f"  ID: {stop[0]:2} | {stop[1]:35} | Lat: {stop[2]:.4f} | Lng: {stop[3]:.4f} | Type: {stop[4]}")

print("\n" + "=" * 100)
print("[TRANSIT LINES]")
print("=" * 100)
cursor.execute("""
    SELECT id, line_name, line_number, mode, cost_per_km, avg_speed_kmh, 
           co2_per_km, color, is_electric, service_provider, vehicle_type 
    FROM transit_lines ORDER BY id
""")
lines = cursor.fetchall()
for line in lines:
    electric_icon = "[E]" if line[8] else "[D]"
    print(f"  ID: {line[0]:2} | {line[1]:30} | #{line[2]:10}")
    print(f"      Mode: {line[3]:8} | Provider: {line[9] or 'N/A':20} | Vehicle: {line[10] or 'N/A':20}")
    print(f"      Cost: ${line[4]:.2f}/km | Speed: {line[5]:.0f}km/h | CO2: {line[6]:.0f}g/km {electric_icon}")
    print()

print("=" * 100)
print("[STOP CONNECTIONS - Transit Network]")
print("=" * 100)
cursor.execute("""
    SELECT sc.id, 
           ts1.name as from_stop, 
           ts2.name as to_stop, 
           tl.line_name,
           tl.line_number,
           sc.distance_km, 
           sc.duration_minutes,
           tl.is_electric
    FROM stop_connections sc
    JOIN transit_stops ts1 ON sc.from_stop_id = ts1.id
    JOIN transit_stops ts2 ON sc.to_stop_id = ts2.id
    JOIN transit_lines tl ON sc.line_id = tl.id
    ORDER BY sc.id
""")
connections = cursor.fetchall()
for conn in connections:
    electric_icon = "[E]" if conn[7] else "[D]"
    print(f"  ID: {conn[0]:2} | {conn[1]:30} -> {conn[2]:30}")
    print(f"      Line: {conn[3]:30} (#{conn[4]:10}) | {conn[5]:.1f}km | {conn[6]:.0f}min {electric_icon}")
    print()

print("=" * 100)
print("[ROUTES]")
print("=" * 100)
cursor.execute("""
    SELECT id, name, origin, destination, total_distance_km, 
           total_duration_minutes, total_cost, total_transfers 
    FROM routes
""")
routes = cursor.fetchall()
if routes:
    for route in routes:
        print(f"  ID: {route[0]} | {route[1]}")
        print(f"     From: {route[2]} → To: {route[3]}")
        print(f"     Distance: {route[4]}km | Duration: {route[5]:.0f}min | Cost: ${route[6]:.2f} | Transfers: {route[7]}")
        
        cursor.execute("""
            SELECT segment_order, mode, distance_km, duration_minutes, cost 
            FROM route_segments 
            WHERE route_id = ?
        """, (route[0],))
        segments = cursor.fetchall()
        if segments:
            print(f"     Segments:")
            for seg in segments:
                print(f"       {seg[0]}. {seg[1]:8} - {seg[2]:.1f}km, {seg[3]:.0f}min, ${seg[4]:.2f}")
        print()
else:
    print("  No pre-defined routes. Routes are generated dynamically via API.")

print("=" * 100)
print("[TRIPS]")
print("=" * 100)
cursor.execute("""
    SELECT t.id, u.username, t.origin, t.destination, t.distance_km, 
           t.duration_minutes, t.cost, t.transfers, t.co2_saved 
    FROM trips t
    LEFT JOIN users u ON t.user_id = u.id
""")
trips = cursor.fetchall()
if trips:
    for trip in trips:
        username = trip[1] if trip[1] else "Anonymous"
        print(f"  ID: {trip[0]} | User: {username:20} | {trip[2]:25} → {trip[3]:25}")
        print(f"     Distance: {trip[4]:.1f}km | Time: {trip[5]:.0f}min | Cost: ${trip[6]:.2f} | Transfers: {trip[7]} | CO2 Saved: {trip[8]:.0f}g")
        print()
else:
    print("  No trips recorded yet.")

print("=" * 100)
print("[STATISTICS]")
print("=" * 100)

cursor.execute("SELECT SUM(total_co2_saved) FROM users")
total_user_co2 = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(co2_saved) FROM trips")
total_trip_co2 = cursor.fetchone()[0] or 0

cursor.execute("SELECT AVG(distance_km), AVG(cost) FROM trips")
avg_stats = cursor.fetchone()
avg_distance = avg_stats[0] or 0
avg_cost = avg_stats[1] or 0

cursor.execute("SELECT COUNT(*) FROM trips WHERE transfers > 0")
trips_with_transfers = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM transit_lines WHERE is_electric = 1")
electric_lines = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM transit_lines WHERE is_electric = 0")
non_electric_lines = cursor.fetchone()[0]

print(f"  Total CO2 Saved (Users): {total_user_co2:.1f}g")
print(f"  Total CO2 Saved (Trips): {total_trip_co2:.1f}g")
print(f"  Average Trip Distance: {avg_distance:.1f}km")
print(f"  Average Trip Cost: ${avg_cost:.2f}")
print(f"  Trips with Transfers: {trips_with_transfers}/{len(trips)}")
print(f"  Electric Transit Lines: {electric_lines}")
print(f"  Non-Electric Transit Lines: {non_electric_lines}")

print("\n" + "=" * 100)
print("[ENVIRONMENTAL IMPACT]")
print("=" * 100)

cursor.execute("""
    SELECT tl.vehicle_type, tl.is_electric, 
           AVG(tl.co2_per_km) as avg_co2,
           COUNT(sc.id) as num_connections
    FROM transit_lines tl
    LEFT JOIN stop_connections sc ON tl.id = sc.line_id
    GROUP BY tl.vehicle_type, tl.is_electric
    ORDER BY avg_co2
""")
vehicle_impact = cursor.fetchall()
for vehicle in vehicle_impact:
    electric_status = "Electric [E]" if vehicle[1] else "Non-Electric [D]"
    print(f"  {vehicle[0] or 'Unknown':25} ({electric_status:20}) | Avg CO2: {vehicle[2]:.1f}g/km | Connections: {vehicle[3]}")

print("\n" + "=" * 100)
print("[POPULAR ROUTES - Based on Connections]")
print("=" * 100)

cursor.execute("""
    SELECT ts.name, COUNT(sc.id) as connection_count
    FROM transit_stops ts
    JOIN stop_connections sc ON (ts.id = sc.from_stop_id OR ts.id = sc.to_stop_id)
    GROUP BY ts.name
    ORDER BY connection_count DESC
    LIMIT 10
""")
popular_stops = cursor.fetchall()
for idx, stop in enumerate(popular_stops, 1):
    print(f"  {idx:2}. {stop[0]:40} | {stop[1]} connections")

print("\n" + "=" * 100)
print("[AVAILABLE ROUTE PAIRS]")
print("=" * 100)
print("  1. Connaught Place -> Noida City Center (Metro Blue Line)")
print("  2. Connaught Place -> Dwarka Sector 21 (Metro Blue Line)")
print("  3. Connaught Place -> Gurgaon Cyber City (Metro Yellow Line)")
print("  4. Kashmere Gate -> Anand Vihar ISBT (DTC Bus)")
print("  5. Connaught Place -> Saket Metro (Metro Yellow Line)")
print("\n  Plus many combinations with:")
print("  - Electric Scooters (Rapido, Uber Moto)")
print("  - Electric Cars (Uber Premier, BluSmart)")
print("  - Electric Buses (DTC E1, E2)")

print("\n" + "=" * 100)
print(f"[SUCCESS] Database location: {db_path}")
print("=" * 100)

conn.close()
