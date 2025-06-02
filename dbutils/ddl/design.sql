CREATE TABLE IF NOT EXISTS design (
    nct_id TEXT PRIMARY KEY,
    study_type TEXT,
    expanded_access_individual BOOLEAN,
    expanded_access_intermediate BOOLEAN,
    expanded_access_treatment BOOLEAN,
    patient_registry BOOLEAN,
    num_phases INTEGER,
    allocation TEXT,
    intervention_model TEXT,
    primary_purpose TEXT,
    observational_model TEXT,
    biospec_retention TEXT,
    biospec_description TEXT,
    enrollment_count INTEGER
);

CREATE INDEX IF NOT EXISTS idx_study_type ON design(study_type);
