import re
from itertools import chain

import jellyfish  # type: ignore
import pytest  # type: ignore
import pytz

import us
from us.states import County

# attribute


def test_attribute():
    for state in us.STATES_AND_TERRITORIES:
        assert state == getattr(us.states, state.abbr)


def test_valid_timezones():
    for state in us.STATES_AND_TERRITORIES:
        if state.capital:
            assert pytz.timezone(state.capital_tz)
        for tz in state.time_zones:
            assert pytz.timezone(tz)
        # During migration from SQLite to Python classes, a duplicate
        # time zone had been found
        assert len(state.time_zones) == len(set(state.time_zones))


# maryland lookup


def test_fips():
    assert us.states.lookup("24") == us.states.MD
    assert us.states.lookup("51") != us.states.MD


def test_abbr():
    assert us.states.lookup("MD") == us.states.MD
    assert us.states.lookup("md") == us.states.MD
    assert us.states.lookup("VA") != us.states.MD
    assert us.states.lookup("va") != us.states.MD


def test_name():
    assert us.states.lookup("Maryland") == us.states.MD
    assert us.states.lookup("maryland") == us.states.MD
    assert us.states.lookup("Maryland", field="name") == us.states.MD
    assert us.states.lookup("maryland", field="name") is None
    assert us.states.lookup("murryland") == us.states.MD
    assert us.states.lookup("Virginia") != us.states.MD


# lookups


def test_abbr_lookup():
    for state in us.STATES:
        assert us.states.lookup(state.abbr) == state


def test_fips_lookup():
    for state in us.STATES:
        assert us.states.lookup(state.fips) == state


def test_name_lookup():
    for state in us.STATES:
        assert us.states.lookup(state.name) == state


def test_obsolete_lookup():
    for state in us.OBSOLETE:
        assert us.states.lookup(state.name) is None


# clean_name


def test_clean_name():
    assert us.states.clean_name(" The state OF idaho ") == "idaho"
    assert us.states.clean_name("Idaho!") == "idaho"
    assert us.states.clean_name("idaho") == "idaho"
    assert us.states.clean_name("") == ""
    assert us.states.clean_name("the state of") == ""
    assert us.states.clean_name("New York") == "new york"
    assert us.states.clean_name("new_york") == "new york"


# fallback_func / startswith_fallback


def test_startswith_fallback():
    california = us.states.lookup("CA")
    assert us.states.startswith_fallback("calif") == california
    assert us.states.startswith_fallback("CALIF") == california
    assert us.states.startswith_fallback("zzz") is None
    assert us.states.startswith_fallback("") is None


def test_lookup_fallback_func():
    california = us.states.lookup("CA")
    idaho = us.states.lookup("ID")

    # a garbage value that normally misses resolves via the fallback
    assert us.states.lookup("calif", use_cache=False, fallback_func=us.states.startswith_fallback) == california

    # without a fallback the same value still returns None
    assert us.states.lookup("calif", use_cache=False) is None
    assert us.states.lookup("calif", use_cache=False, fallback_func=None) is None

    def boom(val):
        raise AssertionError("fallback_func should not be called on a match")

    # the fallback is not consulted when the normal scan matches
    assert us.states.lookup("idaho", use_cache=False, fallback_func=boom) == idaho

    # ...nor when a cache hit short-circuits the lookup
    us.states.lookup("idaho")  # prime the cache
    assert us.states.lookup("idaho", fallback_func=boom) == idaho


def test_lookup_fallback_caching():
    california = us.states.lookup("CA")

    calls = []

    def counting_fallback(val):
        calls.append(val)
        return us.states.startswith_fallback(val)

    # a fallback hit is cached: the second call is served without re-invoking
    assert us.states.lookup("califo", fallback_func=counting_fallback) == california
    assert us.states.lookup("califo", fallback_func=counting_fallback) == california
    assert calls == ["califo"]

    # the cached fallback hit does NOT leak into a no-fallback lookup
    assert us.states.lookup("califo") is None

    # ...nor into a lookup using a different fallback
    other_calls = []

    def other_fallback(val):
        other_calls.append(val)
        return None

    assert us.states.lookup("califo", fallback_func=other_fallback) is None
    assert other_calls == ["califo"]

    # use_cache=False neither reads nor writes the cache: the fallback runs
    # on every call
    calls.clear()
    assert us.states.lookup("califo", use_cache=False, fallback_func=counting_fallback) == california
    assert us.states.lookup("califo", use_cache=False, fallback_func=counting_fallback) == california
    assert calls == ["califo", "califo"]


def test_lookup_cache_hit_short_circuit():
    # poison the cache with a deliberately wrong answer; if the cache-hit
    # short-circuit works, lookup returns it without scanning the state list
    cache = us.states._lookup_cache
    cache["abbr:MD"] = us.states.CA
    try:
        assert us.states.lookup("MD") == us.states.CA
    finally:
        cache.pop("abbr:MD", None)


# test metaphone


def test_jellyfish_metaphone():
    for state in chain(us.STATES_AND_TERRITORIES, us.OBSOLETE):
        assert state.name_metaphone == jellyfish.metaphone(state.name)


# mappings


def test_mapping():
    states = us.STATES[:5]
    assert us.states.mapping("abbr", "fips", states=states) == dict((s.abbr, s.fips) for s in states)


def test_obsolete_mapping():
    mapping = us.states.mapping("abbr", "fips")
    for state in us.states.OBSOLETE:
        assert state.abbr not in mapping


def test_custom_mapping():
    mapping = us.states.mapping("abbr", "fips", states=[us.states.DC, us.states.MD])
    assert len(mapping) == 2
    assert "DC" in mapping
    assert "MD" in mapping


# known bugs


def test_kentucky_uppercase():
    assert us.states.lookup("kentucky") == us.states.KY
    assert us.states.lookup("KENTUCKY") == us.states.KY


def test_wayoming():
    assert us.states.lookup("Wyoming") == us.states.WY
    assert us.states.lookup("Wayoming") is None


def test_dc():
    assert us.states.DC not in us.STATES


# shapefiles


@pytest.mark.skip
def test_head():
    import requests

    for state in us.STATES_AND_TERRITORIES:
        for url in state.shapefile_urls().values():
            resp = requests.head(url)
            assert resp.status_code == 200


# counts


def test_obsolete():
    assert len(us.OBSOLETE) == 3


def test_states():
    assert len(us.STATES) == 50


def test_territories():
    assert len(us.TERRITORIES) == 5


def test_contiguous():
    # Lower 48
    assert len(us.STATES_CONTIGUOUS) == 48


def test_continental():
    # Lower 48 + Alaska
    assert len(us.STATES_CONTINENTAL) == 49


# counties


COUNTY_FIPS_RE = re.compile(r"^\d{5}$")


def test_county_class():
    county = County(fips="01001", ns_code="00161526", name="Autauga County")
    assert county.fips == "01001"
    assert county.ns_code == "00161526"
    assert county.name == "Autauga County"
    assert repr(county) == "<County:Autauga County>"
    assert str(county) == "Autauga County"


def test_every_state_has_counties():
    for state in us.STATES_AND_TERRITORIES:
        assert isinstance(state.counties, list), f"{state.abbr} has no counties"


def test_county_fips_format():
    for state in us.STATES_AND_TERRITORIES:
        for county in state.counties:
            assert COUNTY_FIPS_RE.match(county.fips), f"{state.abbr}: bad county fips {county.fips!r}"


def test_county_fips_prefixed_by_state():
    for state in us.STATES_AND_TERRITORIES:
        for county in state.counties:
            assert county.fips.startswith(state.fips), (
                f"{state.abbr}: county {county.name} fips {county.fips} not prefixed by state fips {state.fips}"
            )
