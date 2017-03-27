from __future__ import unicode_literals
import pickle
import re
import states

COUNTY_FIPS_RE = re.compile(r'^\d{3}$')
STATE_FIPS_RE = re.compile(r'^\d{2}$')
STATE_ABBR_RE = re.compile(r'^[a-zA-Z]{2}$')
FULL_FIPS_RE = re.compile(r'^\d{5}$')

COUNTIES = []

_lookup_cache = {}

class County(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.state = None # States linked later

    def __repr__(self):
        return "<County:%s>" % self.name

    def __str__(self):
        return self.name

def load_counties():

    from pkg_resources import resource_stream

    with resource_stream(__name__, 'counties.pkl') as pklfile:
        for c in pickle.load(pklfile):

            COUNTIES.append(County(**c))

def lookup(val, field=None, use_cache=True):
    """ County lookup.

          * two digits will search by state FIPS codes (e.g. '27')
          * three digits will search by county FIPS code (e.g. '053' -- not very useful since
            they're only unique within each state)
          * five digits will search by combined state+county FIPS code (e.g. '27053')
          * anything else will try to match the metaphone of county names (in their "short"
            form --- that is, omitting trailing 'County', 'Parish', etc.)

        County lookups always return a list, even when only one county is matched. When
        no counties are matched, an empty list is returned.
    """

    import jellyfish

    if field is None:
        if COUNTY_FIPS_RE.match(val):
            field = 'fips'
        elif STATE_FIPS_RE.match(val):
            field = 'state_fips'
        elif STATE_ABBR_RE.match(val):
            field = 'state_abbr'
        elif FULL_FIPS_RE.match(val):
            field = 'full_fips'
        else:
            val = jellyfish.metaphone(val)
            field = 'name_metaphone'

    # see if results is in cache
    cache_key = "%s:%s" % (field, val)
    if use_cache and cache_key in _lookup_cache:
        return _lookup_cache[cache_key]

    # search by state
    if (field == 'state_fips' or field == 'state_abbr'):
        matches = states.lookup(val).counties
        _lookup_cache[cache_key] = matches
        return matches

    # search by county fields
    matches = []
    for county in COUNTIES:
        if val == getattr(county, field):
            matches.append(county)
    _lookup_cache[cache_key] = matches
    return matches


load_counties()