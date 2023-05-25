.. image:: https://github.com/unitedstates/python-us/workflows/Tests/badge.svg
   :target: https://github.com/unitedstates/python-us/actions

US: The Greatest Package in the World
=====================================

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


Installation
------------

As per usual: ::

    pip install us


Features
--------

Easy access to state information: ::

    >>> import us
    >>> us.states.MD
    <State:Maryland>
    >>> us.states.MD.fips
    '24'
    >>> us.states.MD.name
    'Maryland'
    >>> us.states.MD.is_contiguous
    True

Includes territories too: ::

    >>> us.states.VI.name
    'Virgin Islands'
    >>> us.states.VI.is_territory
    True
    >>> us.states.MD.is_territory
    False

List of all (actual) states: ::

    >>> us.states.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...
    >>> us.states.TERRITORIES
    [<State:American Samoa>, <State:Guam>, <State:Northern Mariana Islands>, ...

And the whole shebang, if you want it: ::

    >>> us.states.STATES_AND_TERRITORIES
    [<State:Alabama>, <State:Alaska>, <State:American Samoa>, ...

For convenience, `STATES`, `TERRITORIES`, and `STATES_AND_TERRITORIES` can be
accessed directly from the `us` module: ::

    >>> us.states.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...
    >>> us.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>, ...

Some states like to be fancy and call themselves commonwealths: ::

    >>> us.states.COMMONWEALTHS
    [<State:Kentucky>, <State:Massachusetts>, <State:Pennsylvania>, <State:Virginia>]

There's also a list of obsolete territories: ::

    >>> us.states.OBSOLETE
    [<State:Dakota>, <State:Orleans>, <State:Philippine Islands>]

The state lookup method allows matching by FIPS code, abbreviation, and name: ::

    >>> us.states.lookup('24')
    <State:Maryland>
    >>> us.states.lookup('MD')
    <State:Maryland>
    >>> us.states.lookup('md')
    <State:Maryland>
    >>> us.states.lookup('maryland')
    <State:Maryland>

Get useful information: ::

    >>> state = us.states.lookup('maryland')
    >>> state.abbr
    'MD'


And for those days that you just can't remember how to spell Mississippi,
we've got phonetic name matching too: ::

    >>> us.states.lookup('misisipi')
    <State:Mississippi>


Shapefiles
----------

You want shapefiles too? As long as you want 2010 shapefiles, we've gotcha covered.

::

    >>> urls = us.states.MD.shapefile_urls()
    >>> sorted(urls.keys())
    ['block', 'blockgroup', 'cd', 'county', 'state', 'tract', 'zcta']
    >>> urls['block']
    'https://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2010/tl_2010_24_tabblock10.zip'

The `shapefile_urls()` method on the State object generates shapefile URLs for
the following regions:

* block
* blockgroup
* census tract (tract)
* congressional district (cd)
* county
* state
* zcta


Mappings
--------

Mappings between various state attributes are a common need. The `mapping()`
method will generate a lookup between two specified fields.

::

    >>> us.states.mapping('fips', 'abbr')
    {'01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', ...
    >>> us.states.mapping('abbr', 'name')
    {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', ...

This method uses `us.STATES_AND_TERRITORIES` as the default list of states
it will create a mapping for, but this can be overridden by passing an
additional states argument: ::

    >>> us.states.mapping('fips', 'abbr', states=[us.states.DC])
    {'11': 'DC'}


DC should be granted statehood
------------------------------

Washington, DC does not appear in `us.STATES` or any of the
related state lists, but is often treated as a state in practice and
should be granted statehood anyway. DC can be automatically included in these
lists by setting a `DC_STATEHOOD` environment variable to any truthy value
before importing this package.

::

    DC_STATEHOOD=1


CLI
----

When you need to know state information RIGHT AWAY, there's the *states* script.

::

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


Running Tests
-------------

GitHub Actions are set up to automatically run unit tests against any new
commits to the repo. To run these tests yourself: ::

    pipenv install --dev
    pipenv run pytest


Changelog
---------

3.0.1
~~~~~
* add support for Python 3.11
* upgrade to jellyfish 0.11.2


3.0.0
~~~~~

* upgrade to jellyfish 0.7.2
* drop support for Python 2.7
* add us.states.COMMONWEALTHS list of states that call themselves commonwealths 🎩
* add DC to STATES, STATES_AND_TERRITORIES, STATES_CONTIGUOUS, or STATES_CONTINENTAL when DC_STATEHOOD environment variable is set
* remove `region` parameter from `shapefile_urls()` method
* `mapping()` no longer includes obsolete states
* added type annotations


2.0.2
~~~~~

* restore DC in lookup() and mapping()


2.0.1
~~~~~

* fix Python 2.7 tests that ran with Python 3
* revert to jellyfish 0.6.1 to support Python 2.7


2.0.0
~~~~~

* add support for Python 3.7 and 3.8
* remove support for Python 3.4 and 3.5
* remove pickled objects and database in favor of pure Python code
* upgrade jellyfish to 0.7.2 to fix metaphone bug
* fixes for IN, KY, ND, and NM timezones
* set AZ timezone to America/Phoenix
* obsolete entries are no longer included in STATES_AND_TERRITORIES
* DC is no longer included in STATES, STATES_AND_TERRITORIES, STATES_CONTIGUOUS, or STATES_CONTINENTAL


1.0.0
~~~~~

* full Python 3.6 support
* use pytest


0.10.0
~~~~~~

* upgrade jellyfish to 0.5.3 to fix metaphone bug

0.9.0
~~~~~

* add information on whether a state is contiguous and/or continental,
  thanks to `chebee7i <https://github.com/chebee7i>`_

0.8.0
~~~~~

* add obsolete territories, thanks to `Ben Chartoff <https://github.com/bchartoff>`_
* fix packaging error, thanks to `Alexander Kulakov <https://github.com/momyc>`_


0.7.1
~~~~~

* upgrade to jellyfish 0.5.1 to fix metaphone case bug

0.7
~~~

* add time zones, thanks to `Paul Tagliamonte <https://github.com/paultag>`_
* Python 2.6 and 3.2 compatibility

0.6
~~~

* add AP-style state abbreviations
* use jellyfish instead of Metaphone package
* update to requests v1.0.4 for tests
* Python 3.3 compatibility

0.5
~~~

* fix state abbreviation for Nebraska

0.4
~~~

* add state capitals
* add years of statehood

0.3
~~~

* add mapping method to generate dicts of arbitrary fields

0.2
~~~

* add command line script for quick access to state data

0.1
~~~

* initial release
* state names and abbreviations
* FIPS codes
* lookup() method
* shapefile URLs for various regions
