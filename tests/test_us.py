import pytest
import us


# attribute

def test_attribute():
    for state in us.STATES_AND_TERRITORIES:
        assert state == getattr(us.states, state.abbr)


# maryland lookup

def test_fips():
    assert us.states.lookup('24') == us.states.MD
    assert us.states.lookup('51') != us.states.MD


def test_abbr():
    assert us.states.lookup('MD') == us.states.MD
    assert us.states.lookup('md') == us.states.MD
    assert us.states.lookup('VA') != us.states.MD
    assert us.states.lookup('va') != us.states.MD


def test_name():
    assert us.states.lookup('Maryland') == us.states.MD
    assert us.states.lookup('maryland') == us.states.MD
    assert us.states.lookup('Maryland', field='name') == us.states.MD
    assert us.states.lookup('maryland', field='name') is None
    assert us.states.lookup('murryland') == us.states.MD
    assert us.states.lookup('Virginia') != us.states.MD


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


# mappings

def test_mapping():
    states = us.STATES[:5]
    assert us.states.mapping('abbr', 'fips', states=states) == \
        dict((s.abbr, s.fips) for s in states)


# known bugs

def test_kentucky_uppercase():
    assert us.states.lookup('kentucky') == us.states.KY
    assert us.states.lookup('KENTUCKY') == us.states.KY


# shapefiles

@pytest.mark.skip
def test_head():
    import requests
    for state in us.STATES_AND_TERRITORIES:
        for region, url in state.shapefile_urls().items():
            resp = requests.head(url)
            assert resp.status_code == 200


# counts

def test_obsolete():
    assert len(us.OBSOLETE) == 3


def test_states():
    assert len(us.STATES) == 51


def test_territories():
    assert len(us.TERRITORIES) == 5


def test_contiguous():
    # Lower 48 + DC
    assert len(us.STATES_CONTIGUOUS) == 49


def test_continental():
    # Lower 48 + DC + Alaska
    assert len(us.STATES_CONTINENTAL) == 50
