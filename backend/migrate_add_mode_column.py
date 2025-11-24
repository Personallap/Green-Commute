"""
Migration script to add the 'mode' column to the trips table
"""
import sqlite3
import os

# Path to your database file
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'greencommute.db')

def migrate():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(trips)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'mode' not in columns:
            print("Adding 'mode' column to trips table...")
            # Add the mode column
            cursor.execute("ALTER TABLE trips ADD COLUMN mode VARCHAR(50)")
            conn.commit()
            print("✓ Successfully added 'mode' column to trips table")
        else:
            print("'mode' column already exists in trips table")
        
        conn.close()
        print("\nMigration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.close()

if __name__ == '__main__':
    migrate()
