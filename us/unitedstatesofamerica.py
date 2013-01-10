name = 'United States of America'
abbr = 'US'


def shapefile_urls(region=None):

    base_url = "http://www2.census.gov/geo/tiger/TIGER2012"

    urls = {
        'cd': base_url + '/CD/tl_2012_us_cd112.zip',
        'county': base_url + '/COUNTY/tl_2012_us_county.zip',
        'state': base_url + '/STATE/tl_2012_us_state.zip',
        'zcta': base_url + '/ZCTA5/tl_2012_us_zcta510.zip',
    }

    if region:

        if region in ('tract',):
            raise ValueError('the specified region is available only at the state level for 2012')

        if region in urls:
            return urls[region]

    return urls
