import os
import psycopg2
from urllib.parse import urlparse

def check_prod_db():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set.")
        return

    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("Connected to production database.")
        
        # Check TransitStops
        cursor.execute("SELECT COUNT(*) FROM transit_stops;")
        stop_count = cursor.fetchone()[0]
        print(f"Transit Stops count: {stop_count}")
        
        if stop_count > 0:
            print("Sample stops:")
            cursor.execute("SELECT name FROM transit_stops LIMIT 5;")
            for row in cursor.fetchall():
                print(f"- {row[0]}")
        else:
            print("Transit Stops table is empty.")

        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    check_prod_db()
