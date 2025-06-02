CREATE TABLE IF NOT EXISTS interventions (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    intervention_type TEXT,
    intervention_name TEXT,
    intervention_description TEXT,
    group_label TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id),
    UNIQUE (nct_id, intervention_type, intervention_name, intervention_description, group_label)
);

CREATE INDEX IF NOT EXISTS idx_interventions_nct_id ON interventions(nct_id);
CREATE INDEX IF NOT EXISTS idx_interventions_intervention_type ON interventions(intervention_type);
