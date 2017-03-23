import os
import pickle
import sqlite3

import jellyfish

PWD = os.path.abspath(os.path.dirname(__file__))


def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


def pickle_state_data():

    dbpath = os.path.abspath(os.path.join(PWD, 'data.db'))

    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute("""SELECT * FROM states ORDER BY name""")

    states = []

    for row in c:
        row['name_metaphone'] = jellyfish.metaphone(row['name'])
        row['is_territory'] = row['is_territory'] == 1
        row['is_obsolete'] = row['is_obsolete'] == 1
        row['is_contiguous'] = row['is_contiguous'] == 1
        row['is_continental'] = row['is_continental'] == 1
        row['time_zones'] = row['time_zones'].split(',')
        states.append(row)

    pkl_path = os.path.abspath(os.path.join(PWD, 'us', 'states.pkl'))

    with open(pkl_path, 'wb') as pkl_file:
        pickle.dump(states, pkl_file)


def pickle_county_data():

    dbpath = os.path.abspath(os.path.join(PWD, 'data.db'))

    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute("""SELECT * FROM counties ORDER BY state_fips, name""")

    counties = []

    for row in c:
        row['name_metaphone'] = jellyfish.metaphone(row['name'])
        counties.append(row)

    pkl_path = os.path.abspath(os.path.join(PWD, 'us', 'counties.pkl'))

    with open(pkl_path, 'wb') as pkl_file:
        pickle.dump(counties, pkl_file)


def build():
    pickle_state_data()
    pickle_county_data()


if __name__ == '__main__':
    build()
