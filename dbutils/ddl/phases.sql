CREATE TABLE IF NOT EXISTS phases (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    phase TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id),
    UNIQUE (nct_id, phase)
);

CREATE INDEX IF NOT EXISTS idx_phases_nct_id ON phases(nct_id);
