import sqlite3

# Paths
DB_FILE = "./outputs/dicom_metadata.db"  # Path to SQLite database
SCHEMA_FILE = "./scripts/schema.sql"    # Path to schema.sql file

def create_database():
    """
    Create the SQLite database and apply the schema defined in schema.sql.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Read schema from the schema.sql file
    try:
        with open(SCHEMA_FILE, "r") as f:
            schema = f.read()
        print("Applying schema...")
        cursor.executescript(schema)  # Execute the schema
        print(f"Database schema applied successfully to {DB_FILE}")
    except Exception as e:
        print(f"Error applying schema: {e}")
    finally:
        # Commit and close the connection
        conn.commit()
        conn.close()

if __name__ == "__main__":
    create_database()
