import re
from itertools import chain

import jellyfish
import pytest
import pytz

import us
from us.states import County

# attribute


def test_attribute():
    for state in chain(us.STATES_AND_TERRITORIES, us.ASSOCIATED_STATES):
        assert state == getattr(us.states, state.abbr)


def test_version_deprecation():
    with pytest.warns(DeprecationWarning):
        version = us.version
    assert version == us.__version__


def test_valid_timezones():
    for state in chain(us.STATES_AND_TERRITORIES, us.ASSOCIATED_STATES):
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
    for state in chain(us.STATES_AND_TERRITORIES, us.OBSOLETE, us.ASSOCIATED_STATES):
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


# enumerations


def test_enumeration():
    states = us.STATES[:5]
    enum = us.states.enumeration("name", states=states)
    for state in states:
        assert enum[state.abbr].value == state.name


def test_enumeration_default_states():
    enum = us.states.enumeration("name")
    assert enum["VA"].value == "Virginia"
    assert enum["DC"].value == "District of Columbia"


def test_enumeration_default_value_field():
    enum = us.states.enumeration()
    assert enum["VA"].value == "Virginia"


def test_custom_enumeration():
    enum = us.states.enumeration("fips", states=[us.states.DC, us.states.MD])
    assert len(enum) == 2
    assert enum["DC"].value == us.states.DC.fips
    assert enum["MD"].value == us.states.MD.fips


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
    # `requests` is intentionally not declared as a dependency; this test
    # is permanently skipped and the import is dead code for ty.
    import requests  # ty: ignore[unresolved-import]

    for state in us.STATES_AND_TERRITORIES:
        urls = state.shapefile_urls()
        if urls is None:
            continue
        for url in urls.values():
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


# associated states (Compact of Free Association)


def test_associated_states_count():
    assert len(us.ASSOCIATED_STATES) == 3


def test_associated_states_not_in_states_and_territories():
    for state in us.ASSOCIATED_STATES:
        assert state not in us.STATES_AND_TERRITORIES


def test_associated_states_lookup_returns_none():
    # lookup() only scans STATES_AND_TERRITORIES, so associated states
    # are deliberately unreachable through it
    for state in us.ASSOCIATED_STATES:
        assert us.states.lookup(state.abbr) is None
        assert us.states.lookup(state.name) is None
        assert us.states.lookup(state.fips) is None


def test_associated_states_have_is_associated_flag():
    for state in us.ASSOCIATED_STATES:
        assert state.is_associated is True
    for state in chain(us.STATES_AND_TERRITORIES, us.OBSOLETE):
        assert state.is_associated is False


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
        assert state.fips is not None, f"{state.abbr}: missing state fips"
        for county in state.counties:
            assert county.fips.startswith(state.fips), (
                f"{state.abbr}: county {county.name} fips {county.fips} not prefixed by state fips {state.fips}"
            )
