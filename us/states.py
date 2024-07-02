import os
import re
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin

import jellyfish  # type: ignore

FIPS_RE = re.compile(r"^\d{2}$")
ABBR_RE = re.compile(r"^[a-zA-Z]{2}$")

DC_STATEHOOD = bool(os.environ.get("DC_STATEHOOD"))


_lookup_cache: Dict[str, "State"] = {}


class State:
    abbr: str
    ap_abbr: Optional[str]
    capital: Optional[str]
    capital_tz: Optional[str]
    fips: Optional[str]
    is_territory: bool
    is_obsolete: bool
    is_contiguous: bool
    is_continental: bool
    name: str
    name_metaphone: str
    statehood_year: Optional[int]
    time_zones: List[str]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return f"<State:{self.name}>"

    def __str__(self) -> str:
        return self.name

    def shapefile_urls(self) -> Optional[Dict[str, str]]:
        """Shapefiles are available directly from the US Census Bureau:
        https://www.census.gov/cgi-bin/geo/shapefiles/index.php
        """

        fips = self.fips

        if not fips:
            return None

        base = "https://www2.census.gov/geo/tiger/TIGER2010/"
        urls = {
            "tract": urljoin(base, f"TRACT/2010/tl_2010_{fips}_tract10.zip"),
            "cd": urljoin(base, f"CD/111/tl_2010_{fips}_cd111.zip"),
            "county": urljoin(base, f"COUNTY/2010/tl_2010_{fips}_county10.zip"),
            "state": urljoin(base, f"STATE/2010/tl_2010_{fips}_state10.zip"),
            "zcta": urljoin(base, f"ZCTA5/2010/tl_2010_{fips}_zcta510.zip"),
            "block": urljoin(base, f"TABBLOCK/2010/tl_2010_{fips}_tabblock10.zip"),
            "blockgroup": urljoin(base, f"BG/2010/tl_2010_{fips}_bg10.zip"),
        }

        return urls


def lookup(val, field: Optional[str] = None, use_cache: bool = True) -> Optional[State]:
    """Semi-fuzzy state lookup. This method will make a best effort
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

    matched_state = None

    if field is None:
        if FIPS_RE.match(val):
            field = "fips"
        elif ABBR_RE.match(val):
            val = val.upper()
            field = "abbr"
        else:
            val = jellyfish.metaphone(val)
            field = "name_metaphone"

    # see if result is in cache
    cache_key = f"{field}:{val}"
    if use_cache and cache_key in _lookup_cache:
        matched_state = _lookup_cache[cache_key]

    for state in STATES_AND_TERRITORIES:
        if val == getattr(state, field):
            matched_state = state
            if use_cache:
                _lookup_cache[cache_key] = state

    return matched_state


def mapping(from_field: str, to_field: str, states: Optional[Iterable[State]] = None) -> Dict[Any, Any]:
    if states is None:
        states = STATES_AND_TERRITORIES
    return {getattr(s, from_field): getattr(s, to_field) for s in states}


AL = State(
    **{
        "fips": "01",
        "name": "Alabama",
        "abbr": "AL",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1819,
        "capital": "Montgomery",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Ala.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "ALBM",
    }
)


AK = State(
    **{
        "fips": "02",
        "name": "Alaska",
        "abbr": "AK",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": True,
        "statehood_year": 1959,
        "capital": "Juneau",
        "capital_tz": "America/Anchorage",
        "ap_abbr": "Alaska",
        "time_zones": ["America/Anchorage", "America/Adak"],
        "name_metaphone": "ALSK",
    }
)


AS = State(
    **{
        "fips": "60",
        "name": "American Samoa",
        "abbr": "AS",
        "is_territory": True,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": "Pago Pago",
        "capital_tz": "Pacific/Samoa",
        "ap_abbr": None,
        "time_zones": ["Pacific/Samoa"],
        "name_metaphone": "AMRKN SM",
    }
)


AZ = State(
    **{
        "fips": "04",
        "name": "Arizona",
        "abbr": "AZ",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1912,
        "capital": "Phoenix",
        "capital_tz": "America/Phoenix",
        "ap_abbr": "Ariz.",
        "time_zones": ["America/Phoenix"],
        "name_metaphone": "ARSN",
    }
)


AR = State(
    **{
        "fips": "05",
        "name": "Arkansas",
        "abbr": "AR",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1836,
        "capital": "Little Rock",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Ark.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "ARKNSS",
    }
)


CA = State(
    **{
        "fips": "06",
        "name": "California",
        "abbr": "CA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1850,
        "capital": "Sacramento",
        "capital_tz": "America/Los_Angeles",
        "ap_abbr": "Calif.",
        "time_zones": ["America/Los_Angeles"],
        "name_metaphone": "KLFRN",
    }
)


CO = State(
    **{
        "fips": "08",
        "name": "Colorado",
        "abbr": "CO",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1876,
        "capital": "Denver",
        "capital_tz": "America/Denver",
        "ap_abbr": "Colo.",
        "time_zones": ["America/Denver"],
        "name_metaphone": "KLRT",
    }
)


CT = State(
    **{
        "fips": "09",
        "name": "Connecticut",
        "abbr": "CT",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Hartford",
        "capital_tz": "America/New_York",
        "ap_abbr": "Conn.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "KNKTKT",
    }
)


DK = State(
    **{
        "fips": None,
        "name": "Dakota",
        "abbr": "DK",
        "is_territory": False,
        "is_obsolete": True,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": None,
        "capital": "Yankton",
        "capital_tz": "America/Chicago",
        "ap_abbr": None,
        "time_zones": ["America/Chicago"],
        "name_metaphone": "TKT",
    }
)


DE = State(
    **{
        "fips": "10",
        "name": "Delaware",
        "abbr": "DE",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1787,
        "capital": "Dover",
        "capital_tz": "America/New_York",
        "ap_abbr": "Del.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "TLWR",
    }
)


DC = State(
    **{
        "fips": "11",
        "name": "District of Columbia",
        "abbr": "DC",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": None,
        "capital": None,
        "capital_tz": "America/New_York",
        "ap_abbr": "D.C.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "TSTRKT OF KLMB",
    }
)


FL = State(
    **{
        "fips": "12",
        "name": "Florida",
        "abbr": "FL",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1845,
        "capital": "Tallahassee",
        "capital_tz": "America/New_York",
        "ap_abbr": "Fla.",
        "time_zones": ["America/New_York", "America/Chicago"],
        "name_metaphone": "FLRT",
    }
)


GA = State(
    **{
        "fips": "13",
        "name": "Georgia",
        "abbr": "GA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Atlanta",
        "capital_tz": "America/New_York",
        "ap_abbr": "Ga.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "JRJ",
    }
)


GU = State(
    **{
        "fips": "66",
        "name": "Guam",
        "abbr": "GU",
        "is_territory": True,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": "Hagåtña",
        "capital_tz": "Pacific/Guam",
        "ap_abbr": None,
        "time_zones": ["Pacific/Guam"],
        "name_metaphone": "KM",
    }
)


HI = State(
    **{
        "fips": "15",
        "name": "Hawaii",
        "abbr": "HI",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": 1959,
        "capital": "Honolulu",
        "capital_tz": "Pacific/Honolulu",
        "ap_abbr": "Hawaii",
        "time_zones": ["Pacific/Honolulu"],
        "name_metaphone": "HW",
    }
)


ID = State(
    **{
        "fips": "16",
        "name": "Idaho",
        "abbr": "ID",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1890,
        "capital": "Boise",
        "capital_tz": "America/Denver",
        "ap_abbr": "Idaho",
        "time_zones": ["America/Denver", "America/Los_Angeles"],
        "name_metaphone": "ITH",
    }
)


IL = State(
    **{
        "fips": "17",
        "name": "Illinois",
        "abbr": "IL",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1818,
        "capital": "Springfield",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Ill.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "ILNS",
    }
)


IN = State(
    **{
        "fips": "18",
        "name": "Indiana",
        "abbr": "IN",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1816,
        "capital": "Indianapolis",
        "capital_tz": "America/Indiana/Indianapolis",
        "ap_abbr": "Ind.",
        "time_zones": [
            "America/Chicago",
            "America/Indiana/Indianapolis",
            "America/Indianapolis",
            "America/Indiana/Winamac",
            "America/Indiana/Vincennes",
            "America/Indiana/Vevay",
            "America/Indiana/Tell_City",
            "America/Indiana/Petersburg",
            "America/Indiana/Marengo",
            "America/Indiana/Knox",
            "America/Knox_IN",
            "America/New_York",
        ],
        "name_metaphone": "INTN",
    }
)


IA = State(
    **{
        "fips": "19",
        "name": "Iowa",
        "abbr": "IA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1846,
        "capital": "Des Moines",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Iowa",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "IW",
    }
)


KS = State(
    **{
        "fips": "20",
        "name": "Kansas",
        "abbr": "KS",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1861,
        "capital": "Topeka",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Kan.",
        "time_zones": ["America/Chicago", "America/Denver"],
        "name_metaphone": "KNSS",
    }
)


KY = State(
    **{
        "fips": "21",
        "name": "Kentucky",
        "abbr": "KY",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1792,
        "capital": "Frankfort",
        "capital_tz": "America/New_York",
        "ap_abbr": "Ky.",
        "time_zones": [
            "America/Chicago",
            "America/New_York",
            "America/Kentucky/Louisville",
            "America/Kentucky/Monticello",
        ],
        "name_metaphone": "KNTK",
    }
)


LA = State(
    **{
        "fips": "22",
        "name": "Louisiana",
        "abbr": "LA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1812,
        "capital": "Baton Rouge",
        "capital_tz": "America/Chicago",
        "ap_abbr": "La.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "LXN",
    }
)


ME = State(
    **{
        "fips": "23",
        "name": "Maine",
        "abbr": "ME",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1820,
        "capital": "Augusta",
        "capital_tz": "America/New_York",
        "ap_abbr": "Maine",
        "time_zones": ["America/New_York"],
        "name_metaphone": "MN",
    }
)


MD = State(
    **{
        "fips": "24",
        "name": "Maryland",
        "abbr": "MD",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Annapolis",
        "capital_tz": "America/New_York",
        "ap_abbr": "Md.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "MRLNT",
    }
)


MA = State(
    **{
        "fips": "25",
        "name": "Massachusetts",
        "abbr": "MA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Boston",
        "capital_tz": "America/New_York",
        "ap_abbr": "Mass.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "MSXSTS",
    }
)


MI = State(
    **{
        "fips": "26",
        "name": "Michigan",
        "abbr": "MI",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1837,
        "capital": "Lansing",
        "capital_tz": "America/New_York",
        "ap_abbr": "Mich.",
        "time_zones": ["America/New_York", "America/Chicago"],
        "name_metaphone": "MXKN",
    }
)


MN = State(
    **{
        "fips": "27",
        "name": "Minnesota",
        "abbr": "MN",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1858,
        "capital": "Saint Paul",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Minn.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "MNST",
    }
)


MS = State(
    **{
        "fips": "28",
        "name": "Mississippi",
        "abbr": "MS",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1817,
        "capital": "Jackson",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Miss.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "MSSP",
    }
)


MO = State(
    **{
        "fips": "29",
        "name": "Missouri",
        "abbr": "MO",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1821,
        "capital": "Jefferson City",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Mo.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "MSR",
    }
)


MT = State(
    **{
        "fips": "30",
        "name": "Montana",
        "abbr": "MT",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1889,
        "capital": "Helena",
        "capital_tz": "America/Denver",
        "ap_abbr": "Mont.",
        "time_zones": ["America/Denver"],
        "name_metaphone": "MNTN",
    }
)


NE = State(
    **{
        "fips": "31",
        "name": "Nebraska",
        "abbr": "NE",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1867,
        "capital": "Lincoln",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Neb.",
        "time_zones": ["America/Chicago", "America/Denver"],
        "name_metaphone": "NBRSK",
    }
)


NV = State(
    **{
        "fips": "32",
        "name": "Nevada",
        "abbr": "NV",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1864,
        "capital": "Carson City",
        "capital_tz": "America/Los_Angeles",
        "ap_abbr": "Nev.",
        "time_zones": ["America/Los_Angeles", "America/Denver"],
        "name_metaphone": "NFT",
    }
)


NH = State(
    **{
        "fips": "33",
        "name": "New Hampshire",
        "abbr": "NH",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Concord",
        "capital_tz": "America/New_York",
        "ap_abbr": "N.H.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "N HMPXR",
    }
)


NJ = State(
    **{
        "fips": "34",
        "name": "New Jersey",
        "abbr": "NJ",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1787,
        "capital": "Trenton",
        "capital_tz": "America/New_York",
        "ap_abbr": "N.J.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "N JRS",
    }
)


NM = State(
    **{
        "fips": "35",
        "name": "New Mexico",
        "abbr": "NM",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1912,
        "capital": "Santa Fe",
        "capital_tz": "America/Denver",
        "ap_abbr": "N.M.",
        "time_zones": ["America/Denver"],
        "name_metaphone": "N MKSK",
    }
)


NY = State(
    **{
        "fips": "36",
        "name": "New York",
        "abbr": "NY",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Albany",
        "capital_tz": "America/New_York",
        "ap_abbr": "N.Y.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "N YRK",
    }
)


NC = State(
    **{
        "fips": "37",
        "name": "North Carolina",
        "abbr": "NC",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1789,
        "capital": "Raleigh",
        "capital_tz": "America/New_York",
        "ap_abbr": "N.C.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "NR0 KRLN",
    }
)


ND = State(
    **{
        "fips": "38",
        "name": "North Dakota",
        "abbr": "ND",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1889,
        "capital": "Bismarck",
        "capital_tz": "America/North_Dakota/Center",
        "ap_abbr": "N.D.",
        "time_zones": [
            "America/Boise",
            "America/Chicago",
            "America/North_Dakota/Beulah",
            "America/North_Dakota/Center",
            "America/North_Dakota/New_Salem",
        ],
        "name_metaphone": "NR0 TKT",
    }
)


MP = State(
    **{
        "fips": "69",
        "name": "Northern Mariana Islands",
        "abbr": "MP",
        "is_territory": True,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": "Saipan",
        "capital_tz": "Pacific/Guam",
        "ap_abbr": None,
        "time_zones": ["Pacific/Guam"],
        "name_metaphone": "NR0RN MRN ISLNTS",
    }
)


OH = State(
    **{
        "fips": "39",
        "name": "Ohio",
        "abbr": "OH",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1803,
        "capital": "Columbus",
        "capital_tz": "America/New_York",
        "ap_abbr": "Ohio",
        "time_zones": ["America/New_York"],
        "name_metaphone": "OH",
    }
)


OK = State(
    **{
        "fips": "40",
        "name": "Oklahoma",
        "abbr": "OK",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1907,
        "capital": "Oklahoma City",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Okla.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "OKLHM",
    }
)


OR = State(
    **{
        "fips": "41",
        "name": "Oregon",
        "abbr": "OR",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1859,
        "capital": "Salem",
        "capital_tz": "America/Los_Angeles",
        "ap_abbr": "Ore.",
        "time_zones": ["America/Los_Angeles", "America/Boise"],
        "name_metaphone": "ORKN",
    }
)


OL = State(
    **{
        "fips": None,
        "name": "Orleans",
        "abbr": "OL",
        "is_territory": False,
        "is_obsolete": True,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": None,
        "capital": None,
        "capital_tz": None,
        "ap_abbr": None,
        "time_zones": ["America/Chicago"],
        "name_metaphone": "ORLNS",
    }
)


PA = State(
    **{
        "fips": "42",
        "name": "Pennsylvania",
        "abbr": "PA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1787,
        "capital": "Harrisburg",
        "capital_tz": "America/New_York",
        "ap_abbr": "Pa.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "PNSLFN",
    }
)


PI = State(
    **{
        "fips": None,
        "name": "Philippine Islands",
        "abbr": "PI",
        "is_territory": False,
        "is_obsolete": True,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": None,
        "capital_tz": None,
        "ap_abbr": None,
        "time_zones": ["Asia/Singapore"],
        "name_metaphone": "FLPN ISLNTS",
    }
)


PR = State(
    **{
        "fips": "72",
        "name": "Puerto Rico",
        "abbr": "PR",
        "is_territory": True,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": "San Juan",
        "capital_tz": "America/Puerto_Rico",
        "ap_abbr": None,
        "time_zones": ["America/Puerto_Rico"],
        "name_metaphone": "PRT RK",
    }
)


RI = State(
    **{
        "fips": "44",
        "name": "Rhode Island",
        "abbr": "RI",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1790,
        "capital": "Providence",
        "capital_tz": "America/New_York",
        "ap_abbr": "R.I.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "RHT ISLNT",
    }
)


SC = State(
    **{
        "fips": "45",
        "name": "South Carolina",
        "abbr": "SC",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Columbia",
        "capital_tz": "America/New_York",
        "ap_abbr": "S.C.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "S0 KRLN",
    }
)


SD = State(
    **{
        "fips": "46",
        "name": "South Dakota",
        "abbr": "SD",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1889,
        "capital": "Pierre",
        "capital_tz": "America/Chicago",
        "ap_abbr": "S.D.",
        "time_zones": ["America/Chicago", "America/Denver"],
        "name_metaphone": "S0 TKT",
    }
)


TN = State(
    **{
        "fips": "47",
        "name": "Tennessee",
        "abbr": "TN",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1796,
        "capital": "Nashville",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Tenn.",
        "time_zones": ["America/Chicago", "America/New_York"],
        "name_metaphone": "TNS",
    }
)


TX = State(
    **{
        "fips": "48",
        "name": "Texas",
        "abbr": "TX",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1845,
        "capital": "Austin",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Texas",
        "time_zones": ["America/Chicago", "America/Denver"],
        "name_metaphone": "TKSS",
    }
)


UT = State(
    **{
        "fips": "49",
        "name": "Utah",
        "abbr": "UT",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1896,
        "capital": "Salt Lake City",
        "capital_tz": "America/Denver",
        "ap_abbr": "Utah",
        "time_zones": ["America/Denver"],
        "name_metaphone": "UT",
    }
)


VT = State(
    **{
        "fips": "50",
        "name": "Vermont",
        "abbr": "VT",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1791,
        "capital": "Montpelier",
        "capital_tz": "America/New_York",
        "ap_abbr": "Vt.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "FRMNT",
    }
)


VI = State(
    **{
        "fips": "78",
        "name": "Virgin Islands",
        "abbr": "VI",
        "is_territory": True,
        "is_obsolete": False,
        "is_contiguous": False,
        "is_continental": False,
        "statehood_year": None,
        "capital": "Charlotte Amalie",
        "capital_tz": "America/Puerto_Rico",
        "ap_abbr": None,
        "time_zones": ["America/Puerto_Rico"],
        "name_metaphone": "FRJN ISLNTS",
    }
)


VA = State(
    **{
        "fips": "51",
        "name": "Virginia",
        "abbr": "VA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1788,
        "capital": "Richmond",
        "capital_tz": "America/New_York",
        "ap_abbr": "Va.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "FRJN",
    }
)


WA = State(
    **{
        "fips": "53",
        "name": "Washington",
        "abbr": "WA",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1889,
        "capital": "Olympia",
        "capital_tz": "America/Los_Angeles",
        "ap_abbr": "Wash.",
        "time_zones": ["America/Los_Angeles"],
        "name_metaphone": "WXNKTN",
    }
)


WV = State(
    **{
        "fips": "54",
        "name": "West Virginia",
        "abbr": "WV",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1863,
        "capital": "Charleston",
        "capital_tz": "America/New_York",
        "ap_abbr": "W.Va.",
        "time_zones": ["America/New_York"],
        "name_metaphone": "WST FRJN",
    }
)


WI = State(
    **{
        "fips": "55",
        "name": "Wisconsin",
        "abbr": "WI",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1848,
        "capital": "Madison",
        "capital_tz": "America/Chicago",
        "ap_abbr": "Wis.",
        "time_zones": ["America/Chicago"],
        "name_metaphone": "WSKNSN",
    }
)


WY = State(
    **{
        "fips": "56",
        "name": "Wyoming",
        "abbr": "WY",
        "is_territory": False,
        "is_obsolete": False,
        "is_contiguous": True,
        "is_continental": True,
        "statehood_year": 1890,
        "capital": "Cheyenne",
        "capital_tz": "America/Denver",
        "ap_abbr": "Wyo.",
        "time_zones": ["America/Denver"],
        "name_metaphone": "YMNK",
    }
)


OBSOLETE: List[State] = [DK, OL, PI]
TERRITORIES: List[State] = [AS, GU, MP, PR, VI]
STATES: List[State] = [
    AL,
    AK,
    AZ,
    AR,
    CA,
    CO,
    CT,
    DE,
    FL,
    GA,
    HI,
    ID,
    IL,
    IN,
    IA,
    KS,
    KY,
    LA,
    ME,
    MD,
    MA,
    MI,
    MN,
    MS,
    MO,
    MT,
    NE,
    NV,
    NH,
    NJ,
    NM,
    NY,
    NC,
    ND,
    OH,
    OK,
    OR,
    PA,
    RI,
    SC,
    SD,
    TN,
    TX,
    UT,
    VT,
    VA,
    WA,
    WV,
    WI,
    WY,
]
STATES_CONTIGUOUS: List[State] = [
    AL,
    AZ,
    AR,
    CA,
    CO,
    CT,
    DE,
    FL,
    GA,
    ID,
    IL,
    IN,
    IA,
    KS,
    KY,
    LA,
    ME,
    MD,
    MA,
    MI,
    MN,
    MS,
    MO,
    MT,
    NE,
    NV,
    NH,
    NJ,
    NM,
    NY,
    NC,
    ND,
    OH,
    OK,
    OR,
    PA,
    RI,
    SC,
    SD,
    TN,
    TX,
    UT,
    VT,
    VA,
    WA,
    WV,
    WI,
    WY,
]
STATES_CONTINENTAL: List[State] = [
    AL,
    AK,
    AZ,
    AR,
    CA,
    CO,
    CT,
    DE,
    FL,
    GA,
    ID,
    IL,
    IN,
    IA,
    KS,
    KY,
    LA,
    ME,
    MD,
    MA,
    MI,
    MN,
    MS,
    MO,
    MT,
    NE,
    NV,
    NH,
    NJ,
    NM,
    NY,
    NC,
    ND,
    OH,
    OK,
    OR,
    PA,
    RI,
    SC,
    SD,
    TN,
    TX,
    UT,
    VT,
    VA,
    WA,
    WV,
    WI,
    WY,
]

STATES_AND_TERRITORIES: List[State] = STATES + TERRITORIES

COMMONWEALTHS: List[State] = [KY, MA, PA, VA]

if DC_STATEHOOD:
    STATES.append(DC)
    STATES_AND_TERRITORIES.append(DC)
    STATES_CONTIGUOUS.append(DC)
    STATES_CONTINENTAL.append(DC)
