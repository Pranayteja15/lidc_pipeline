import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "./outputs/dicom_metadata.db"  # SQLite database file
OUTPUT_DIR = "./outputs/"  # Directory to save visualizations

def generate_visualizations():
    """
    Generate visualizations for the dataset:
    - Histogram of slice thickness.
    - Bar chart of slices per series.
    """
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)

    # Load data into Pandas DataFrames
    series_df = pd.read_sql_query("SELECT * FROM series;", conn)

    # Close the connection
    conn.close()

    # Ensure output directory exists
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Visualization 1: Histogram of Slice Thickness
    plt.figure(figsize=(8, 6))
    series_df["slice_thickness"].plot(kind="hist", bins=10, alpha=0.7, color="blue", edgecolor="black")
    plt.title("Histogram of Slice Thickness")
    plt.xlabel("Slice Thickness")
    plt.ylabel("Frequency")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}histogram_slice_thickness.png")
    plt.show()

    # Visualization 2: Bar Chart of Slices Per Series
    plt.figure(figsize=(10, 6))
    series_slices = series_df.set_index("series_instance_uid")["number_of_slices"]
    series_slices.plot(kind="bar", color="green", alpha=0.8)
    plt.title("Number of Slices Per Series")
    plt.xlabel("Series Instance UID")
    plt.ylabel("Number of Slices")
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}bar_chart_slices_per_series.png")
    plt.show()

    print(f"Visualizations saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_visualizations()
