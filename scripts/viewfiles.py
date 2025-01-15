import os

DATA_DIR = "./data/lidc_small_dset/LIDC-IDRI-0401/01-01-2000-CT LUNG SCREEN-27699/84519"  # Directory to view files

def view_files(directory, file_extension=None):
    """
    List and view files in a directory.

    Args:
        directory (str): Path to the directory to list files.
        file_extension (str): Optional file extension filter (e.g., '.dcm').
    """
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return

    print(f"Listing files in: {directory}\n")
    for root, _, files in os.walk(directory):
        for file in files:
            # Check for file extension filter
            if file_extension and not file.lower().endswith(file_extension.lower()):
                continue
            
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path) / (1024 ** 2)  # File size in MB
            print(f"File: {file}\nPath: {file_path}\nSize: {file_size:.2f} MB\n")

if __name__ == "__main__":
    # View all files in the directory
    view_files(DATA_DIR)

    # Uncomment below to filter for DICOM files only (with .dcm extension)
    # view_files(DATA_DIR, file_extension=".dcm")
