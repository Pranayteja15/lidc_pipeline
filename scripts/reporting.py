from fpdf import FPDF
import sqlite3
import pandas as pd

DB_FILE = "./outputs/dicom_metadata.db"
OUTPUT_PDF = "./outputs/Summary_Report.pdf"

def generate_summary():
    """Generate a summary report and save as PDF."""
    conn = sqlite3.connect(DB_FILE)
    series_df = pd.read_sql_query("SELECT * FROM series;", conn)
    conn.close()

    total_studies = len(series_df["study_instance_uid"].unique())
    total_slices = series_df["number_of_slices"].sum()
    avg_slices_per_study = total_slices / total_studies if total_studies > 0 else 0
    slice_thickness_distribution = series_df["slice_thickness"].value_counts()

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "LIDC Pipeline - Summary Report", ln=True, align="C")
    pdf.ln(10)

    # Summary statistics
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total number of studies: {total_studies}", ln=True)
    pdf.cell(0, 10, f"Total slices across all scans: {total_slices}", ln=True)
    pdf.cell(0, 10, f"Average number of slices per study: {avg_slices_per_study:.2f}", ln=True)
    pdf.ln(10)

    # Slice Thickness Distribution
    pdf.cell(0, 10, "Slice Thickness Distribution:", ln=True)
    for thickness, count in slice_thickness_distribution.items():
        pdf.cell(0, 10, f"  {thickness} mm: {count} slices", ln=True)

    # Save PDF
    pdf.output(OUTPUT_PDF)
    print(f"Summary report saved to {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_summary()
