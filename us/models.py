import jellyfish


class State(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.name_metaphone = jellyfish.metaphone(self.name)

    def __repr__(self):
        return "<State:%s>" % self.name

    def __str__(self):
        return self.name

    def shapefile_urls(self, region=None):
        if not self.fips:
            return {}

        base_url = "https://www2.census.gov/geo/tiger/TIGER2010"
        urls = {
            'tract': '{0}/TRACT/2010/tl_2010_{1}_tract10.zip'.format(
                base_url, self.fips),
            'cd': '{0}/CD/111/tl_2010_{1}_cd111.zip'.format(
                base_url, self.fips),
            'county': '{0}/COUNTY/2010/tl_2010_{1}_county10.zip'.format(
                base_url, self.fips),
            'state': '{0}/STATE/2010/tl_2010_{1}_state10.zip'.format(
                base_url, self.fips),
            'zcta': '{0}/ZCTA5/2010/tl_2010_{1}_zcta510.zip'.format(
                base_url, self.fips),
            'block': '{0}/TABBLOCK/2010/tl_2010_{1}_tabblock10.zip'.format(
                base_url, self.fips),
            'blockgroup': '{0}/BG/2010/tl_2010_{1}_bg10.zip'.format(
                base_url, self.fips),
        }

        if region and region in urls:
            return urls[region]

        return urls
