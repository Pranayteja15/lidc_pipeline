import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "./outputs/dicom_metadata.db"  # SQLite database file

def generate_summary():
    """
    Generate a summary of the dataset, including statistics and visualizations.
    """
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)

    # Load data into Pandas DataFrames
    studies_df = pd.read_sql_query("SELECT * FROM studies;", conn)
    series_df = pd.read_sql_query("SELECT * FROM series;", conn)

    # Close the connection
    conn.close()

    # Generate Summary Statistics
    total_studies = len(studies_df)
    total_slices = series_df["number_of_slices"].sum()
    avg_slices_per_study = total_slices / total_studies if total_studies > 0 else 0
    slice_thickness_distribution = series_df["slice_thickness"].value_counts()

    # Print Summary
    print("Summary Statistics:")
    print(f"Total number of studies: {total_studies}")
    print(f"Total slices across all scans: {total_slices}")
    print(f"Average number of slices per study: {avg_slices_per_study:.2f}")
    print("\nSlice Thickness Distribution:")
    print(slice_thickness_distribution)

    # Visualization: Slice Thickness Distribution
    plt.figure(figsize=(8, 6))
    slice_thickness_distribution.plot(kind="bar")
    plt.title("Slice Thickness Distribution")
    plt.xlabel("Slice Thickness")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("./outputs/slice_thickness_distribution.png")
    plt.show()

if __name__ == "__main__":
    generate_summary()
