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
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id),
    UNIQUE (nct_id, name, status, city, state, zip, country)
);

CREATE INDEX IF NOT EXISTS idx_facility_nct_id ON facility(nct_id);