CREATE TABLE IF NOT EXISTS status (
    nct_id TEXT PRIMARY KEY,
    status_verified_date DATE,
    overall_status TEXT,
    last_known_status TEXT,
    why_stopped TEXT,
    start_date DATE, -- yyyy-mm or yyyy-mm-dd, should standardize
    primary_completion_date DATE,
    completion_date DATE,
    study_first_submit_date DATE,
    study_first_submit_qc_date DATE,
    study_first_post_date DATE,
    results_waived BOOLEAN,
    results_first_submit_date DATE,
    results_first_submit_qc_date DATE,
    results_first_post_date DATE,
    last_update_submit_date DATE,
    last_update_post_date DATE,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX IF NOT EXISTS idx_status_overall_status ON status (overall_status);
