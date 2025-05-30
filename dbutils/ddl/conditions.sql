CREATE TABLE IF NOT EXISTS conditions (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX idx_conditions_nct_id ON conditions(nct_id);
