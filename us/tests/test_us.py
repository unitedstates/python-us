import os.path
import re
import time
import urllib.error
import urllib.request
import warnings
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

import jellyfish
import pytest
import pytz

import us
from us.cli import states as states_cli
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


# cli


def test_cli_lookup(capsys, monkeypatch):
    # the counties attribute is a list of County objects, which used to crash
    # the "other attributes" loop when it tried to join them as strings
    monkeypatch.setattr("sys.argv", ["states", "MD"])
    states_cli.main()
    out = capsys.readouterr().out
    assert "Maryland" in out
    assert "counties" in out


# shapefiles

SHAPEFILE_REGIONS = {"block", "blockgroup", "cd", "county", "state", "tract", "zcta"}

# layers the Census Bureau only publishes as a single nationwide file in the
# 2020 vintage, so the URL is the same no matter which state you ask for
NATIONWIDE_2020_REGIONS = {"cd", "county", "state", "zcta"}

TIGER2020 = "https://www2.census.gov/geo/tiger/TIGER2020/"
TIGER2010 = "https://www2.census.gov/geo/tiger/TIGER2010/"


def test_shapefile_urls_default_to_2010():
    # the default is still 2010 until the 5.0 release
    assert us.states.DEFAULT_SHAPEFILE_VINTAGE == 2010

    with pytest.warns(DeprecationWarning):
        urls = us.states.MD.shapefile_urls()

    assert urls == {
        "tract": TIGER2010 + "TRACT/2010/tl_2010_24_tract10.zip",
        "cd": TIGER2010 + "CD/111/tl_2010_24_cd111.zip",
        "county": TIGER2010 + "COUNTY/2010/tl_2010_24_county10.zip",
        "state": TIGER2010 + "STATE/2010/tl_2010_24_state10.zip",
        "zcta": TIGER2010 + "ZCTA5/2010/tl_2010_24_zcta510.zip",
        "block": TIGER2010 + "TABBLOCK/2010/tl_2010_24_tabblock10.zip",
        "blockgroup": TIGER2010 + "BG/2010/tl_2010_24_bg10.zip",
    }


def test_shapefile_urls_default_matches_explicit_2010():
    with pytest.warns(DeprecationWarning):
        default_urls = us.states.MD.shapefile_urls()

    assert default_urls == us.states.MD.shapefile_urls(vintage=2010)


@pytest.mark.parametrize("state", [us.states.MD, us.states.PR])
def test_shapefile_urls_default_warns_about_the_5_0_change(state):
    with pytest.warns(DeprecationWarning) as record:
        state.shapefile_urls()

    assert len(record) == 1

    message = str(record[0].message)
    assert "shapefile_urls()" in message
    assert "2010" in message
    assert "2020" in message
    assert "5.0" in message
    # the warning should tell callers how to pin either vintage
    assert "vintage=2010" in message
    assert "vintage=2020" in message

    # stacklevel should point the warning at the caller, not at us/states.py
    assert os.path.basename(record[0].filename) == os.path.basename(__file__)


def test_shapefile_urls_explicit_vintage_does_not_warn():
    # passing a vintage is how callers opt out of the deprecation warning
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)

        for vintage in us.states.SHAPEFILE_VINTAGES:
            assert us.states.MD.shapefile_urls(vintage=vintage) is not None


def test_shapefile_urls_2020():
    # the vintage that will become the default in 5.0
    assert us.states.FUTURE_DEFAULT_SHAPEFILE_VINTAGE == 2020

    urls = us.states.MD.shapefile_urls(vintage=2020)
    assert urls == {
        "tract": TIGER2020 + "TRACT/tl_2020_24_tract.zip",
        "cd": TIGER2020 + "CD/tl_2020_us_cd116.zip",
        "county": TIGER2020 + "COUNTY/tl_2020_us_county.zip",
        "state": TIGER2020 + "STATE/tl_2020_us_state.zip",
        "zcta": TIGER2020 + "ZCTA520/tl_2020_us_zcta520.zip",
        "block": TIGER2020 + "TABBLOCK20/tl_2020_24_tabblock20.zip",
        "blockgroup": TIGER2020 + "BG/tl_2020_24_bg.zip",
    }


@pytest.mark.parametrize("vintage", us.states.SHAPEFILE_VINTAGES)
def test_shapefile_urls_cover_every_state_and_territory(vintage):
    for state in us.STATES_AND_TERRITORIES:
        urls = state.shapefile_urls(vintage=vintage)
        assert urls is not None, state
        assert set(urls) == SHAPEFILE_REGIONS, state

        for region, url in urls.items():
            assert url.startswith(f"https://www2.census.gov/geo/tiger/TIGER{vintage}/"), url
            assert url.endswith(".zip"), url
            if vintage == 2020 and region in NATIONWIDE_2020_REGIONS:
                assert "_us_" in url
            else:
                assert f"_{state.fips}_" in url, url


def test_shapefile_urls_without_fips():
    # obsolete states have no FIPS code, so there is nothing to build a URL from
    for state in us.OBSOLETE:
        assert state.fips is None
        for vintage in us.states.SHAPEFILE_VINTAGES:
            assert state.shapefile_urls(vintage=vintage) is None


def test_shapefile_urls_unsupported_vintage():
    with pytest.raises(ValueError, match="unsupported shapefile vintage"):
        us.states.MD.shapefile_urls(vintage=2000)


def _head_status(url: str, attempts: int = 3) -> int:
    """HEAD `url` and return its status code."""

    request = urllib.request.Request(url, method="HEAD")

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as resp:
                return resp.getcode()
        except urllib.error.HTTPError as exc:
            # a real answer from the server, including a 404 for a bad URL
            return exc.code
        except urllib.error.URLError:
            # DNS and connection hiccups are common when firing off a few
            # hundred requests, so retry before calling the URL broken
            if attempt == attempts:
                raise
            time.sleep(attempt)

    raise AssertionError("unreachable")


@pytest.mark.network
@pytest.mark.parametrize("vintage", us.states.SHAPEFILE_VINTAGES)
def test_shapefile_urls_are_live(vintage):
    """Check every generated URL against the Census Bureau.

    Deselected by default because it needs network access and makes a few
    hundred requests. Run it with `uv run pytest -m network`.
    """
    urls = set()
    for state in us.STATES_AND_TERRITORIES:
        state_urls = state.shapefile_urls(vintage=vintage)
        assert state_urls is not None
        urls.update(state_urls.values())

    # the nationwide 2020 layers repeat across states, so check each URL once
    unique_urls = sorted(urls)

    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses = dict(zip(unique_urls, pool.map(_head_status, unique_urls)))

    broken = {url: status for url, status in statuses.items() if status != 200}
    assert not broken, f"{len(broken)} of {len(unique_urls)} URLs did not return 200: {broken}"


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
