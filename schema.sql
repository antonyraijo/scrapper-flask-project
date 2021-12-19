DROP TABLE IF EXISTS job;

CREATE TABLE job (
    job_id TEXT PRIMARY KEY,
    job_types TEXT NOT NULL,
    company_name TEXT NOT NULL,
    benefits TEXT NOT NULL,
    address TEXT NOT NULL,
    apply_url TEXT NOT NULL
);