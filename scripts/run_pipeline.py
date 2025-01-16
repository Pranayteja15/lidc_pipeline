import subprocess
import logging
import os

# Ensure logs directory exists
LOG_DIR = "../outputs/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting the LIDC pipeline execution...")

# List of scripts to run in order
scripts = [
    "extract_metadata.py",
    "organize_files.py",
    "create_database.py",
    "populate_database.py",
    "reporting.py",
    "visualizations.py"
]

for script in scripts:
    try:
        logging.info(f"Running {script}...")
        subprocess.run(["python", f"./scripts/{script}"], check=True)
        logging.info(f"Successfully executed {script}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {script}: {e}")

logging.info("Pipeline execution completed.")
