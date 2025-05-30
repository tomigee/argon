CREATE TABLE IF NOT EXISTS contact (
    id SERIAL PRIMARY KEY,
    nct_id TEXT NOT NULL,
    name TEXT,
    role TEXT,
    phone TEXT,
    email TEXT,
    FOREIGN KEY (nct_id) REFERENCES identification (nct_id)
);

CREATE INDEX idx_contact_nct_id ON contact(nct_id);
