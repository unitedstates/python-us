from __future__ import print_function
import requests
import sqlite3
import fiona
from os import remove

TEMP_DATA_FILE = u'county_shapefile.zip'
SHP_URL = u'http://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_us_county10.zip'
SHP_FILENAME = u'tl_2010_us_county10.shp'

def download_county_data():
    r = requests.get(SHP_URL)
    with open(TEMP_DATA_FILE, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)


def feature_data(f):
    p = 'properties'
    return (f[p][u'COUNTYFP10'],
            f[p][u'STATEFP10'],
            f[p][u'NAMELSAD10'],
            f[p][u'NAME10'],
            f[p][u'LSAD10'])


def load_county_data():
    with fiona.open('/{}'.format(SHP_FILENAME), vfs='zip://{}'.format(TEMP_DATA_FILE)) as c:
        data = [feature_data(feature) for feature in c]

    with sqlite3.connect('data.db') as con:
        q = "INSERT INTO counties(fips, state_fips, name, short_name, lsad) VALUES(?, ?, ?, ?, ?);"
        con.executemany(q, data)


if __name__ == '__main__':
        download_county_data()
        load_county_data()
        remove(TEMP_DATA_FILE)
