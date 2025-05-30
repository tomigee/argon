CREATE TABLE IF NOT EXISTS eligibility (
    nct_id TEXT PRIMARY KEY,
    accepts_healthy_volunteers BOOLEAN,
    gender TEXT,
    gender_based BOOLEAN,
    min_age INTERVAL,
    max_age INTERVAL,
    population_description TEXT,
    sampling_method TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);
