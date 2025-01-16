import os
import shutil
import pandas as pd

METADATA_FILE = "./outputs/metadata.csv"
DATA_DIR = "./data/"
OUTPUT_DIR = "./organized_data/"
LOG_FILE = "./outputs/organize_log.txt"

def organize_files():
    """
    Reorganize DICOM files into <PatientID>/<StudyInstanceUID>/<SeriesInstanceUID>/ structure.
    Handle duplicates and log conflicts.
    """
    if not os.path.exists(METADATA_FILE):
        print(f"Metadata file not found: {METADATA_FILE}")
        return

    # Load metadata
    metadata_df = pd.read_csv(METADATA_FILE)

    # Ensure necessary columns exist
    required_columns = {"PatientID", "StudyInstanceUID", "SeriesInstanceUID", "FilePath"}
    if not required_columns.issubset(metadata_df.columns):
        print(f"Missing required columns: {required_columns - set(metadata_df.columns)}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(LOG_FILE, "w") as log_file:
        for _, row in metadata_df.iterrows():
            try:
                patient_id = str(row["PatientID"])
                study_uid = str(row["StudyInstanceUID"])
                series_uid = str(row["SeriesInstanceUID"])
                source_path = row["FilePath"]

                if not patient_id or not study_uid or not series_uid or not os.path.exists(source_path):
                    log_file.write(f"Skipping file with missing data or invalid path: {source_path}\n")
                    continue

                # Define target directory
                target_dir = os.path.join(OUTPUT_DIR, patient_id, study_uid, series_uid)
                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, os.path.basename(source_path))

                # Handle duplicates
                if os.path.exists(target_path):
                    log_file.write(f"Duplicate file skipped: {source_path} -> {target_path}\n")
                    continue

                # Move the file
                shutil.copy2(source_path, target_path)
                print(f"Moved: {source_path} -> {target_path}")

            except Exception as e:
                log_file.write(f"Error processing file {row['FilePath']}: {e}\n")
                print(f"Error processing file {row['FilePath']}: {e}")

    print(f"File organization completed. Logs saved to {LOG_FILE}")

if __name__ == "__main__":
    organize_files()
