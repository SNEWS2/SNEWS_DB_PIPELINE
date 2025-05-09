-- Connect to your database (ensure the database exists or create it if needed)
CREATE TABLE IF NOT EXISTS all_mgs (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    received_time TEXT,
    message_type TEXT,
    message TEXT,
    expiration TEXT
);

CREATE TABLE IF NOT EXISTS sig_tier_archive (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    schema_version REAL,
    detector_name TEXT,
    p_vals TEXT,
    t_bin_width_sec REAL,
    is_test INTEGER,
    sent_time_utc TEXT,
    machine_time_utc TEXT,
    meta TEXT,
    expiration TEXT
);

CREATE TABLE IF NOT EXISTS time_tier_archive (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    schema_version REAL,
    detector_name TEXT,
    p_val REAL,
    t_bin_width_sec REAL,
    timing_series TEXT,
    sent_time_utc TEXT,
    machine_time_utc TEXT,
    meta TEXT,
    expiration TEXT
);

CREATE TABLE IF NOT EXISTS coincidence_tier_archive (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    schema_version REAL,
    detector_name TEXT,
    p_val REAL,
    neutrino_time_utc TEXT,
    sent_time_utc TEXT,
    machine_time_utc TEXT,
    meta TEXT,
    expiration TEXT
);

CREATE TABLE IF NOT EXISTS coincidence_tier_alerts (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    alert_type TEXT,
    server_tag TEXT,
    false_alarm_prob TEXT,
    detector_names TEXT,
    sent_time_utc TEXT,
    p_vals TEXT,
    neutrino_times TEXT,
    p_vals_average TEXT,
    sub_list_number INTEGER
);

CREATE TABLE IF NOT EXISTS cached_heartbeats (
    id SERIAL PRIMARY KEY,
    received_time_utc TIMESTAMP,
    detector TEXT,
    stamped_time_utc TIMESTAMP,
    latency BIGINT,
    time_after_last BIGINT,
    status TEXT
);