# LIDC Pipeline

A pipeline for downloading, parsing, and analyzing DICOM files from the LIDC dataset.

## Features
- **Download**: Retrieve DICOM files from SharePoint or other sources.
- **Metadata Extraction**: Extract key metadata from DICOM headers.
- **Database Storage**: Store metadata in a structured SQLite database.
- **Reporting**: Generate summary statistics and visualizations.
- **Scalability**: Designed for large-scale datasets.

## Project Structure

lidc_pipeline/ ├── scripts/ │ ├── download.py # Download DICOM files │ ├── extract_metadata.py # Extract metadata from DICOM headers │ ├── create_database.py # Create the SQLite database schema │ ├── populate_database.py # Populate the database with metadata │ ├── reporting.py # Generate summary statistics │ ├── visualizations.py # Create visualizations ├── outputs/ # Outputs (CSV, logs, plots) ├── data/ # Raw DICOM files ├── requirements.txt # Python dependencies ├── README.md # Project documentation  └── .gitignore # Files and folders to ignore in Git


## Getting Started
### Prerequisites
- Python 3.8 or later
- `pip` for dependency management

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/lidc_pipeline.git
   cd lidc_pipeline

pip install -r requirements.txt

mkdir data outputs

Usage

Run each script step by step:

Download DICOM files:

python scripts/download.py

Extract metadata:

python scripts/extract_metadata.py

Create and populate the database:

python scripts/create_database.py
python scripts/populate_database.py

Generate reports and visualizations:

python scripts/reporting.py
python scripts/visualizations.py

Scalability & Monitoring:
For large datasets, use parallel processing, cloud storage, and distributed databases.
Logs and metrics are captured for error tracking and performance monitoring.