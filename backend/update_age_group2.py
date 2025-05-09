import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv('DATABASE_URL')

# Extract connection details from DATABASE_URL
# Format: postgres://username:password@host:port/database
url_parts = DATABASE_URL.split('//')[1].split('@')
auth_parts = url_parts[0].split(':')
host_port = url_parts[1].split('/')  # Split host:port from database name
host_parts = host_port[0].split(':')

conn_params = {
    'dbname': host_port[1],
    'user': auth_parts[0],
    'password': auth_parts[1],
    'host': host_parts[0],
    'port': host_parts[1]
}

try:
    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Execute the ALTER TABLE command
    cursor.execute("ALTER TABLE story ALTER COLUMN age_group TYPE VARCHAR(100)")
    
    print("Successfully updated age_group column length to 100 characters")
    
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
