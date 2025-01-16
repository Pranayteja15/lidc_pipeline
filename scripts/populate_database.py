import sqlite3
import pandas as pd

# Paths
METADATA_FILE = "./outputs/metadata.csv"
DB_FILE = "./outputs/dicom_metadata.db"

def populate_database():
    """Populate the SQLite database with metadata extracted from DICOM files."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Load metadata from CSV
    metadata_df = pd.read_csv(METADATA_FILE)

    # Insert data into tables
    for _, row in metadata_df.iterrows():
        cursor.execute("INSERT OR IGNORE INTO patients (patient_id, other_patient_metadata) VALUES (?, ?);",
                       (row["PatientID"], "Additional metadata"))

        cursor.execute("INSERT OR IGNORE INTO studies (study_instance_uid, patient_id, study_date) VALUES (?, ?, ?);",
                       (row["StudyInstanceUID"], row["PatientID"], row["StudyDate"]))

        cursor.execute("INSERT OR IGNORE INTO series (series_instance_uid, study_instance_uid, slice_thickness, pixel_spacing, number_of_slices) VALUES (?, ?, ?, ?, ?);",
                       (row["SeriesInstanceUID"], row["StudyInstanceUID"], row["SliceThickness"], str(row["PixelSpacing"]), row["NumberOfSlices"]))

    conn.commit()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    populate_database()
