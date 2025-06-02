CREATE TABLE IF NOT EXISTS identification (
    nct_id TEXT PRIMARY KEY,
    nct_id_alias TEXT[],
    num_nct_aliases INT,
    org_study_id TEXT,
    org_study_id_type TEXT,
    org_study_id_link TEXT,
    num_secondary_ids INT,
    brief_title TEXT,
    official_title TEXT,
    acronym TEXT,
    org_name TEXT,
    org_class TEXT,
    brief_summary TEXT,
    detailed_description TEXT,
    num_conditions INTEGER
);

CREATE INDEX IF NOT EXISTS idx_identification_org_study_id_type ON identification (org_study_id_type);
