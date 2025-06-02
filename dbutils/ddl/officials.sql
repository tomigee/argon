CREATE TABLE IF NOT EXISTS officials (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    "name" TEXT,
    "role" TEXT,
    affiliation TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id),
    UNIQUE ("nct_id", "name", "role", "affiliation")
);

CREATE INDEX IF NOT EXISTS idx_officials_nct_id ON officials(nct_id);
