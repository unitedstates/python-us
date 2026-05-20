[![Workflow status badge](https://github.com/unitedstates/python-us/workflows/Tests/badge.svg)](https://github.com/unitedstates/python-us/actions/workflows/pythonpackage.yml)

# US

A package for easily working with US and state metadata.

* all US states and territories
* postal abbreviations
* Associated Press style abbreviations
* FIPS codes
* capitals
* years of statehood
* time zones
* phonetic state name lookup
* is contiguous or continental
* URLs to shapefiles for state, census, congressional districts,
  counties, and census tracts


## Installation

As per usual:

```
pip install us
```

or

```
uv add us
```


## Development

This project uses [uv](https://docs.astral.sh/uv/) for development.

```
uv sync
uv run pytest
uv run ruff check us
uv run ruff format --check us
```


## Features

Easy access to state information:

```python
>>> import us
>>> us.states.MD
<State:Maryland>
>>> us.states.MD.fips
'24'
>>> us.states.MD.name
'Maryland'
>>> us.states.MD.is_contiguous
True
```

Includes territories too:

```python
>>> us.states.VI.name
'Virgin Islands'
>>> us.states.VI.is_territory
True
>>> us.states.MD.is_territory
False
```

List of all (actual) states:

```python
>>> us.states.STATES
[<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...
>>> us.states.TERRITORIES
[<State:American Samoa>, <State:Guam>, <State:Northern Mariana Islands>, ...
```

And the whole shebang, if you want it:

```python
>>> us.states.STATES_AND_TERRITORIES
[<State:Alabama>, <State:Alaska>, <State:American Samoa>, ...
```

For convenience, `STATES`, `TERRITORIES`, and `STATES_AND_TERRITORIES` can be
accessed directly from the `us` module:

```python
>>> us.states.STATES
[<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...
>>> us.STATES
[<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...
```

Some states like to be fancy and call themselves commonwealths:

```python
>>> us.states.COMMONWEALTHS
[<State:Kentucky>, <State:Massachusetts>, <State:Pennsylvania>, <State:Virginia>]
```

There's also a list of obsolete territories:

```python
>>> us.states.OBSOLETE
[<State:Dakota>, <State:Orleans>, <State:Philippine Islands>]
```

The state lookup method allows matching by FIPS code, abbreviation, and name:

```python
>>> us.states.lookup('24')
<State:Maryland>
>>> us.states.lookup('MD')
<State:Maryland>
>>> us.states.lookup('md')
<State:Maryland>
>>> us.states.lookup('maryland')
<State:Maryland>
```

Get useful information:

```python
>>> state = us.states.lookup('maryland')
>>> state.abbr
'MD'
```


And for those days that you just can't remember how to spell Mississippi,
we've got phonetic name matching too:

```python
>>> us.states.lookup('misisipi')
<State:Mississippi>
```


### Cleaning up messy input

If your lookup values come from user input or other unpredictable sources,
`clean_name()` can strip them down to something the lookup is more likely to
match. It lowercases the input, removes punctuation, and drops the filler
words `the`, `commonwealth`, `state`, and `of`:

```python
>>> us.states.clean_name(' The state OF idaho ')
'idaho'
>>> us.states.clean_name('Commonwealth of Virginia')
'virginia'
>>> us.states.lookup(us.states.clean_name('The State of Maryland!'))
<State:Maryland>
```

`clean_name` is a standalone helper and `lookup` does not call it
automatically. Apply it yourself when you want it.


### Custom fallback matching

`lookup` accepts an optional `fallback_func` that is called when none of the
built-in matching strategies find a state. It receives the original lookup
value and should return a `State` or `None`:

```python
>>> def my_fallback(val):
...     return us.states.AK if val == 'the big one' else None
>>> us.states.lookup('the big one', fallback_func=my_fallback)
<State:Alaska>
```

For the common case of matching against the start of a state name, the
included `startswith_fallback` helper does just that (case-insensitively):

```python
>>> us.states.lookup('calif', fallback_func=us.states.startswith_fallback)
<State:California>
```

Fallback results are cached separately per fallback function, so a cached
fallback match won't leak into lookups that pass a different fallback (or
no fallback at all).


### Shapefiles

You want shapefiles too? As long as you want 2010 shapefiles, we've gotcha covered.

```
>>> urls = us.states.MD.shapefile_urls()
>>> sorted(urls.keys())
['block', 'blockgroup', 'cd', 'county', 'state', 'tract', 'zcta']
>>> urls['block']
'https://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2010/tl_2010_24_tabblock10.zip'
```

The `shapefile_urls()` method on the State object generates shapefile URLs for
the following regions:

* block
* blockgroup
* census tract (tract)
* congressional district (cd)
* county
* state
* zcta


### Mappings

Mappings between various state attributes are a common need. The `mapping()`
method will generate a lookup between two specified fields.

```python
>>> us.states.mapping('fips', 'abbr')
{'01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', ...
>>> us.states.mapping('abbr', 'name')
{'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', ...
```

This method uses `us.STATES_AND_TERRITORIES` as the default list of states
it will create a mapping for, but this can be overridden by passing an
additional states argument:

```python
>>> us.states.mapping('fips', 'abbr', states=[us.states.DC])
{'11': 'DC'}
```


### DC should be granted statehood

Washington, DC does not appear in `us.STATES` or any of the
related state lists, but is often treated as a state in practice and
[should be granted statehood anyway](https://statehood.dc.gov/page/about-dc-statehood). DC can be automatically included in these
lists by setting a `DC_STATEHOOD` environment variable to any truthy value
before importing this package.

```
DC_STATEHOOD=1
```


## CLI

When you need to know state information RIGHT AWAY, there's the _states_ script.

```
$ states md

*** The great state of Maryland (MD) ***

    FIPS code: 24

    other attributes:
      ap_abbr: Md.
      capital: Annapolis
      capital_tz: America/New_York
      is_contiguous: True
      is_continental: True
      is_obsolete: False
      name_metaphone: MRLNT
      statehood_year: 1788
      time_zones: America/New_York

    shapefiles:
      tract: https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_24_tract10.zip
      cd: https://www2.census.gov/geo/tiger/TIGER2010/CD/111/tl_2010_24_cd111.zip
      county: https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_24_county10.zip
      state: https://www2.census.gov/geo/tiger/TIGER2010/STATE/2010/tl_2010_24_state10.zip
      zcta: https://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_24_zcta510.zip
      block: https://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2010/tl_2010_24_tabblock10.zip
      blockgroup: https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/tl_2010_24_bg10.zip
```

## Running Tests

GitHub Actions are set up to automatically run unit tests against any new
commits to the repo. To run these tests yourself:

```
uv sync
uv run pytest
```


## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.
