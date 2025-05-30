CREATE TABLE IF NOT EXISTS outcome (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    type TEXT, -- enum (primary, secondary, other)
    measure TEXT,
    description TEXT,
    time_frame TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX idx_outcome_nct_id ON outcome(nct_id);
