-- Connect to your database (ensure the database exists or create it if needed)

CREATE TABLE IF NOT EXISTS table1 (
    int_attr INTEGER PRIMARY KEY,
    string_attr VARCHAR(50) UNIQUE NOT NULL,
    longer_attr VARCHAR(100) UNIQUE NOT NULL,
    date_attr TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS table2 (
    id SERIAL PRIMARY KEY,
    int_attr INTEGER NOT NULL,
    date_attr TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    other_int_attr INTEGER
);