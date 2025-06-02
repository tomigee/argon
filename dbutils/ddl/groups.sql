CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    group_type TEXT,
    group_description TEXT,
    group_label TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id),
    UNIQUE (nct_id, group_type, group_description, group_label)
);

CREATE INDEX IF NOT EXISTS idx_nct_id ON groups(nct_id);
CREATE INDEX IF NOT EXISTS idx_group_type ON groups(group_type);
