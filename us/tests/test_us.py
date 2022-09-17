from itertools import chain

import jellyfish  # type: ignore
import pytest  # type: ignore
import pytz

import us


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


# test metaphone


def test_jellyfish_metaphone():
    for state in chain(us.STATES_AND_TERRITORIES, us.OBSOLETE):
        assert state.name_metaphone == jellyfish.metaphone(state.name)


# mappings


def test_mapping():
    states = us.STATES[:5]
    assert us.states.mapping("abbr", "fips", states=states) == dict(
        (s.abbr, s.fips) for s in states
    )


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


@pytest.mark.skipif("config.getoption('dc_statehood')")
def test_dc_nostate():
    assert us.states.DC not in us.STATES


@pytest.mark.skipif("not config.getoption('dc_statehood')")
def test_dc_state():
    assert us.states.lookup("DC") == us.states.DC
    assert us.states.lookup("District of Columbia") == us.states.DC
    assert "DC" in us.states.mapping("abbr", "name")


def test_cache():
    key = "abbr:NC"
    sentinel = object()

    us.states._lookup_cache.clear()
    assert us.states.lookup("NC") == us.states.NC
    assert key in us.states._lookup_cache

    # We can't mock the cache so manipulate it directly
    us.states._lookup_cache[key] = sentinel
    assert us.states.lookup("NC") == sentinel

    us.states._lookup_cache.clear()


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


@pytest.mark.skipif("config.getoption('dc_statehood')")
def test_states():
    assert len(us.STATES) == 50


@pytest.mark.skipif("not config.getoption('dc_statehood')")
def test_states_dc():
    assert len(us.STATES) == 51


def test_territories():
    assert len(us.TERRITORIES) == 6


@pytest.mark.skipif("config.getoption('dc_statehood')")
def test_contiguous():
    # Lower 48
    assert len(us.STATES_CONTIGUOUS) == 48


@pytest.mark.skipif("not config.getoption('dc_statehood')")
def test_contiguous_dc():
    assert len(us.STATES_CONTIGUOUS) == 49


@pytest.mark.skipif("config.getoption('dc_statehood')")
def test_continental():
    # Lower 48 + Alaska
    assert len(us.STATES_CONTINENTAL) == 49


@pytest.mark.skipif("not config.getoption('dc_statehood')")
def test_continental_dc():
    assert len(us.STATES_CONTINENTAL) == 50

