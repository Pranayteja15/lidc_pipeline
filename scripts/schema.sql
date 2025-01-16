-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    other_patient_metadata TEXT
);

-- Studies table
CREATE TABLE IF NOT EXISTS studies (
    study_instance_uid TEXT PRIMARY KEY,
    patient_id TEXT,
    study_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);

-- Series table
CREATE TABLE IF NOT EXISTS series (
    series_instance_uid TEXT PRIMARY KEY,
    study_instance_uid TEXT,
    slice_thickness REAL,
    pixel_spacing TEXT,
    number_of_slices INTEGER,
    FOREIGN KEY (study_instance_uid) REFERENCES studies (study_instance_uid)
);
