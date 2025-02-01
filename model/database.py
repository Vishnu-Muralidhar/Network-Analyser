import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "network_analysis",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432,
}

def initialize_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            source VARCHAR(255),
            destination VARCHAR(255),
            protocol VARCHAR(50),
            length INT
        )
    """)
    conn.commit()
    conn.close()

def save_packet(packet):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO packets (timestamp, source, destination, protocol, length)
        VALUES (%s, %s, %s, %s, %s)
    """, (packet.timestamp, packet.source, packet.destination, packet.protocol, packet.length))
    conn.commit()
    conn.close()

def fetch_all_packets():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM packets")
    packets = cursor.fetchall()
    conn.close()
    return packets

def clear_packets():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM packets")
    conn.commit()
    conn.close()
