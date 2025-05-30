CREATE TABLE IF NOT EXISTS collaborators (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    responsible_party_type TEXT,
    investigator_name TEXT,
    investigator_affiliation TEXT,
    collaborator_name TEXT,
    collaborator_class TEXT,
    collaborator_type TEXT, -- enum: lead sponsor, collaborator (my custom column)
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX idx_collaborators_nct_id ON collaborators(nct_id);
CREATE INDEX idx_collaborators_collaborator_class ON collaborators(collaborator_class);
