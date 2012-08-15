import pickle
import re

FIPS_RE = re.compile(r'^\d{2}$')
ABBR_RE = re.compile(r'^[a-zA-Z]{2}$')

STATES = []
TERRITORIES = []
STATES_AND_TERRITORIES = []

_lookup_cache = {}


class State(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __repr__(self):
        return "<State:%s>" % self.name

    def __str__(self):
        return self.name

    def shapefile_urls(self, region=None):
        base_url = "http://www2.census.gov/geo/tiger/TIGER2010"
        urls = {
            'tract': base_url + '/TRACT/2010/tl_2010_%s_tract10.zip' % self.fips,
            'cd': base_url + '/CD/111/tl_2010_%s_cd111.zip' % self.fips,
            'county': base_url + '/COUNTY/2010/tl_2010_%s_county10.zip' % self.fips,
            'state': base_url + '/STATE/2010/tl_2010_%s_state10.zip' % self.fips,
            'zcta': base_url + '/ZCTA5/2010/tl_2010_%s_zcta510.zip' % self.fips,
        }
        if region and region in urls:
            return urls[region]
        return urls


def load_states():
    """ Load state data from pickle file distributed with this package.

        Creates lists of states, territories, and combined states and
        territories. Also adds state abbreviation attribute access
        to the package: us.states.MD
    """

    from pkg_resources import resource_stream

    # load state data from pickle file
    with resource_stream(__name__, 'states.pkl') as pklfile:
        for s in pickle.load(pklfile):

            state = State(**s)  # create state object

            # create separate lists for states and territories
            if state.is_territory:
                TERRITORIES.append(state)
            else:
                STATES.append(state)

            # also create list of all states and territories
            STATES_AND_TERRITORIES.append(state)

            # provide package-level abbreviation access: us.states.MD
            globals()[state.abbr] = state


def lookup(val, field=None, use_cache=True):
    """ Semi-fuzzy state lookup. This method will make a best effort
        attempt at finding the state based on the lookup value provided.

          * two digits will search for FIPS code
          * two letters will search for state abbreviation
          * anything else will try to match the metaphone of state names

        Metaphone is used to allow for incorrect, but phonetically accurate,
        spelling of state names.

        Exact matches can be done on any attribute on State objects by passing
        the `field` argument. This skips the fuzzy-ish matching and does an
        exact, case-sensitive comparison against the specified field.

        This method caches non-None results, but can the cache can be bypassed
        with the `use_cache=False` argument.
    """

    from metaphone import doublemetaphone

    if field is None:
        if FIPS_RE.match(val):
            field = 'fips'
        elif ABBR_RE.match(val):
            val = val.upper()
            field = 'abbr'
        else:
            val = doublemetaphone(val)[0]
            field = 'name_metaphone'

    # see if result is in cache
    cache_key = "%s:%s" % (field, val)
    if use_cache and cache_key in _lookup_cache:
        return _lookup_cache[cache_key]

    for state in STATES_AND_TERRITORIES:
        if val == getattr(state, field):
            _lookup_cache[cache_key] = state
            return state

load_states()
