from __future__ import unicode_literals
import pickle
import re

FIPS_RE = re.compile(r'^\d{2}$')
ABBR_RE = re.compile(r'^[a-zA-Z]{2}$')

STATES = []
STATES_CONTIGUOUS = []
STATES_CONTINENTAL = []
TERRITORIES = []
OBSOLETE = []
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

        if not self.fips:
            return {}

        base_url = "http://www2.census.gov/geo/tiger/TIGER2010"
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

            # create separate lists for obsolete, states, and territories
            if state.is_obsolete:
                OBSOLETE.append(state)
            elif state.is_territory:
                TERRITORIES.append(state)
            else:
                STATES.append(state)

                if state.is_contiguous:
                    STATES_CONTIGUOUS.append(state)
                if state.is_continental:
                    STATES_CONTINENTAL.append(state)

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

    import jellyfish

    if field is None:
        if FIPS_RE.match(val):
            field = 'fips'
        elif ABBR_RE.match(val):
            val = val.upper()
            field = 'abbr'
        else:
            val = jellyfish.metaphone(val)
            field = 'name_metaphone'

    # see if result is in cache
    cache_key = "%s:%s" % (field, val)
    if use_cache and cache_key in _lookup_cache:
        return _lookup_cache[cache_key]

    for state in STATES_AND_TERRITORIES:
        if val == getattr(state, field):
            _lookup_cache[cache_key] = state
            return state


def mapping(from_field, to_field, states=None):
    if states is None:
        states = STATES_AND_TERRITORIES
    return dict((getattr(s, from_field), getattr(s, to_field)) for s in states)


load_states()
