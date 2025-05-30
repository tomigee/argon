CREATE TABLE IF NOT EXISTS facility (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    name TEXT,
    status TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    country TEXT,
    contacts JSONB,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX idx_facility_nct_id ON facility(nct_id);