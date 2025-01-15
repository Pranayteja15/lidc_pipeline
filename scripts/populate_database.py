import sqlite3
import pandas as pd

# File paths
METADATA_FILE = "./outputs/metadata.csv"  # Path to the metadata CSV
DB_FILE = "./outputs/dicom_metadata.db"  # SQLite database file

def validate_and_clean_data(metadata_df):
    """
    Validate and clean the metadata DataFrame.

    Args:
        metadata_df (pd.DataFrame): DataFrame containing metadata.

    Returns:
        pd.DataFrame: Cleaned and validated DataFrame.
    """
    # Drop rows with missing essential fields
    essential_columns = ["PatientID", "StudyInstanceUID", "SeriesInstanceUID", "FilePath"]
    metadata_df = metadata_df.dropna(subset=essential_columns)

    # Replace missing optional fields with default values
    metadata_df["SliceThickness"] = metadata_df["SliceThickness"].fillna(0.0)
    metadata_df["PixelSpacing"] = metadata_df["PixelSpacing"].fillna("Unknown")
    metadata_df["StudyDate"] = metadata_df["StudyDate"].fillna("Unknown")
    metadata_df["NumberOfSlices"] = metadata_df["NumberOfSlices"].fillna(0).astype(int)

    return metadata_df

def populate_database():
    """
    Populate the SQLite database with metadata from the CSV file.
    """
    # Read metadata from CSV
    metadata_df = pd.read_csv(METADATA_FILE)

    # Validate and clean data
    metadata_df = validate_and_clean_data(metadata_df)

    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert data into tables
    for _, row in metadata_df.iterrows():
        # Insert into patients table
        cursor.execute("""
        INSERT OR IGNORE INTO patients (patient_id, other_patient_metadata)
        VALUES (?, ?);
        """, (row["PatientID"], "Additional metadata"))

        # Insert into studies table
        cursor.execute("""
        INSERT OR IGNORE INTO studies (study_instance_uid, patient_id, study_date)
        VALUES (?, ?, ?);
        """, (row["StudyInstanceUID"], row["PatientID"], row["StudyDate"]))

        # Insert into series table
        cursor.execute("""
        INSERT OR IGNORE INTO series (series_instance_uid, study_instance_uid, slice_thickness, pixel_spacing, number_of_slices)
        VALUES (?, ?, ?, ?, ?);
        """, (
            row["SeriesInstanceUID"],
            row["StudyInstanceUID"],
            row["SliceThickness"],
            str(row["PixelSpacing"]),
            row["NumberOfSlices"]
        ))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    populate_database()
