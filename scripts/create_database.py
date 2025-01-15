import sqlite3
import pandas as pd

METADATA_FILE = "./outputs/metadata.csv"  # Path to the metadata CSV
DB_FILE = "./outputs/dicom_metadata.db"  # SQLite database file

def create_database():
    """
    Create the SQLite database and tables for storing DICOM metadata.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        other_patient_metadata TEXT
    );
    """)

    # Create studies table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS studies (
        study_instance_uid TEXT PRIMARY KEY,
        patient_id TEXT,
        study_date DATE,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    );
    """)

    # Create series table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_instance_uid TEXT PRIMARY KEY,
        study_instance_uid TEXT,
        slice_thickness REAL,
        pixel_spacing TEXT,
        number_of_slices INTEGER,
        FOREIGN KEY (study_instance_uid) REFERENCES studies (study_instance_uid)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database created at {DB_FILE}")

def populate_database():
    """
    Populate the SQLite database with metadata from the CSV file.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Load metadata from CSV
    metadata_df = pd.read_csv(METADATA_FILE)

    # Insert data into tables
    for _, row in metadata_df.iterrows():
        # Insert into patients
        cursor.execute("""
        INSERT OR IGNORE INTO patients (patient_id, other_patient_metadata)
        VALUES (?, ?);
        """, (row["PatientID"], "Additional metadata"))

        # Insert into studies
        cursor.execute("""
        INSERT OR IGNORE INTO studies (study_instance_uid, patient_id, study_date)
        VALUES (?, ?, ?);
        """, (row["StudyInstanceUID"], row["PatientID"], row["StudyDate"]))

        # Insert into series
        cursor.execute("""
        INSERT OR IGNORE INTO series (series_instance_uid, study_instance_uid, slice_thickness, pixel_spacing, number_of_slices)
        VALUES (?, ?, ?, ?, ?);
        """, (
            row["SeriesInstanceUID"],
            row["StudyInstanceUID"],
            row["SliceThickness"],
            str(row["PixelSpacing"]),
            row.get("NumberOfSlices", 0)
        ))

    conn.commit()
    conn.close()
    print("Database populated with metadata.")

if __name__ == "__main__":
    create_database()
    populate_database()
