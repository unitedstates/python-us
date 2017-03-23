CREATE TABLE counties (
    fips TEXT,
    state_fips TEXT,
    name TEXT,
    short_name TEXT,
    lsad TEXT,
    UNIQUE (state_fips, fips)
);