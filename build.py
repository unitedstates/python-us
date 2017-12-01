import os
import pickle
import sqlite3

import jellyfish

PWD = os.path.abspath(os.path.dirname(__file__))

def parse_area_code(area_codes):
    """Converts string of area codes to a dict mapping cities to their area code

    For Alabama, area code from database is '205:Birmingham, Tuscaloosa/251:Mobile, Jackson, Gulf Shores/256,938:Huntsville, Anniston, Florence/334:Montgomery, Dothan, Selma'.
    The output is:
    {
    'Mobile, Jackson, Gulf Shores': ['251'],
    'Huntsville, Anniston, Florence': ['256', '938'],
    'Montgomery, Dothan, Selma': ['334'],
    'Birmingham, Tuscaloosa': ['205']
    },
    [205, 251, 256, 334, 938]

    Args:
        area_codes: A string of area codes and their cities.

    Returns:
        A dict mapping cities to their area code:
            cities[String]: area code(s)[Array of Int]

        A list of area codes:
            [Array of Int]
    """

    full_area_code = {y:[int(x) for x in x.split(',')] for x,y in [z.split(':') for z in area_codes.split('/')]}

    plain_area_code = sorted([code for code_list in full_area_code.values() for code in code_list])

    return [full_area_code, plain_area_code]

def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


def pickle_data():

    dbpath = os.path.abspath(os.path.join(PWD, 'data.db'))

    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute("""SELECT * FROM states WHERE fips IS NOT NULL ORDER BY name""")

    states = []

    for row in c:
        row['name_metaphone'] = jellyfish.metaphone(row['name'])
        row['is_territory'] = row['is_territory'] == 1
        row['is_obsolete'] = row['is_obsolete'] == 1
        row['is_contiguous'] = row['is_contiguous'] == 1
        row['is_continental'] = row['is_continental'] == 1
        row['time_zones'] = row['time_zones'].split(',')
        row['full_area_code'], row['plain_area_code'] = parse_area_code(row['area_code']) if row['area_code'].strip() else [None, None]
        states.append(row)

    pkl_path = os.path.abspath(os.path.join(PWD, 'us', 'states.pkl'))

    with open(pkl_path, 'wb') as pkl_file:
        pickle.dump(states, pkl_file)


def build():
    pickle_data()


if __name__ == '__main__':
    build()
