# ./data/LIDC-IDRI-0401/01-01-2000-CT LUNG SCREEN-27699/84519
import os
import pydicom
import pandas as pd
from collections import defaultdict

DATA_DIR = "./data/lidc_small_dset/LIDC-IDRI-0401/01-01-2000-CT LUNG SCREEN-27699/84519" 
OUTPUT_FILE = "./outputs/metadata.csv"  # Path to save extracted metadata

def extract_dicom_metadata():
    """
    Extract metadata from DICOM headers for all files in the data directory.
    """
    metadata_list = []
    series_slice_count = defaultdict(int)  # To count slices per series

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Read the DICOM file
                ds = pydicom.dcmread(file_path)
                
                # Extract relevant metadata
                metadata = {
                    "PatientID": ds.get("PatientID", "Unknown"),
                    "StudyInstanceUID": ds.get("StudyInstanceUID", "Unknown"),
                    "SeriesInstanceUID": ds.get("SeriesInstanceUID", "Unknown"),
                    "SliceThickness": ds.get("SliceThickness", "Unknown"),
                    "PixelSpacing": ds.get("PixelSpacing", "Unknown"),
                    "StudyDate": ds.get("StudyDate", "Unknown"),
                    "AcquisitionDate": ds.get("AcquisitionDate", "Unknown"),
                    "FilePath": file_path
                }
                metadata_list.append(metadata)

                # Increment slice count for the series if SeriesInstanceUID exists
                if metadata["SeriesInstanceUID"] != "Unknown":
                    series_slice_count[metadata["SeriesInstanceUID"]] += 1

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Create a DataFrame for metadata
    metadata_df = pd.DataFrame(metadata_list)

    # Ensure SeriesInstanceUID column exists
    if "SeriesInstanceUID" in metadata_df.columns:
        # Map the slice count to the DataFrame
        metadata_df["NumberOfSlices"] = metadata_df["SeriesInstanceUID"].map(series_slice_count).fillna(0).astype(int)
    else:
        # Add a default NumberOfSlices column if SeriesInstanceUID is missing
        metadata_df["NumberOfSlices"] = 0

    # Save the metadata to a CSV file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    metadata_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Metadata extracted and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_dicom_metadata()
