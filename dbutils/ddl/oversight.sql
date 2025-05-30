CREATE TABLE IF NOT EXISTS oversight (
    nct_id TEXT PRIMARY KEY,
    oversight_has_dmc BOOLEAN,
    is_fda_regulated_drug BOOLEAN,
    is_fda_regulated_device BOOLEAN,
    is_unapproved_device BOOLEAN,
    is_ppsd BOOLEAN,
    is_us_export BOOLEAN,
    is_fda_violation BOOLEAN,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);
