import os
import pydicom
import pandas as pd

DATA_DIR = "./data/"
OUTPUT_FILE = "./outputs/metadata.csv"

def extract_metadata():
    metadata_list = []
    series_slice_count = {}

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".dcm"):
                file_path = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(file_path)
                    patient_id = ds.get("PatientID", "Unknown")
                    study_uid = ds.get("StudyInstanceUID", "Unknown")
                    series_uid = ds.get("SeriesInstanceUID", "Unknown")

                    # Count slices per series
                    series_slice_count[series_uid] = series_slice_count.get(series_uid, 0) + 1

                    metadata_list.append({
                        "PatientID": patient_id,
                        "StudyInstanceUID": study_uid,
                        "SeriesInstanceUID": series_uid,
                        "SliceThickness": ds.get("SliceThickness", "Unknown"),
                        "PixelSpacing": ds.get("PixelSpacing", "Unknown"),
                        "StudyDate": ds.get("StudyDate", "Unknown"),
                        "AcquisitionDate": ds.get("AcquisitionDate", "Unknown"),
                        "FilePath": file_path
                    })

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Convert metadata to DataFrame
    metadata_df = pd.DataFrame(metadata_list)

    # Add NumberOfSlices column using SeriesInstanceUID
    metadata_df["NumberOfSlices"] = metadata_df["SeriesInstanceUID"].map(series_slice_count).fillna(0).astype(int)

    # Save to CSV
    metadata_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Metadata extracted for {len(metadata_df)} DICOM files and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_metadata()
