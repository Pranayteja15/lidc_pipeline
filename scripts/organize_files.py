import os
import shutil
import pandas as pd

METADATA_FILE = "./outputs/metadata.csv"  # Path to the metadata CSV
DATA_DIR = "./data/LIDC-IDRI-0401/01-01-2000-CT LUNG SCREEN-27699/84519"                     # Base directory containing DICOM files
OUTPUT_DIR = "./organized_data/"         # Output directory for reorganized files
LOG_FILE = "./outputs/organize_log.txt"  # Log file for duplicate/conflict handling

def organize_files():
    """
    Reorganize DICOM files into a logical folder structure: <PatientID>/<StudyInstanceUID>/<DICOM Files>.
    Handles duplicates and logs conflicts.
    """
    if not os.path.exists(METADATA_FILE):
        print(f"Metadata file not found: {METADATA_FILE}")
        return

    # Load metadata
    metadata_df = pd.read_csv(METADATA_FILE)

    # Ensure necessary columns are present
    required_columns = {"PatientID", "StudyInstanceUID", "FilePath"}
    if not required_columns.issubset(metadata_df.columns):
        print(f"Missing required columns in metadata: {required_columns - set(metadata_df.columns)}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(LOG_FILE, "w") as log_file:
        for _, row in metadata_df.iterrows():
            try:
                patient_id = str(row["PatientID"])
                study_instance_uid = str(row["StudyInstanceUID"])
                source_path = row["FilePath"]

                # Skip rows with missing or invalid data
                if not patient_id or not study_instance_uid or not os.path.exists(source_path):
                    log_file.write(f"Skipping file with missing data or invalid path: {source_path}\n")
                    continue

                # Define target directory and path
                target_dir = os.path.join(OUTPUT_DIR, patient_id, study_instance_uid)
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
