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
* URLs to shapefiles for state, census, congressional districts,
  counties, and census tracts

Congratulations, DC. As far as this package is concerned, you've got statehood.


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
    u'24'
    >>> us.states.MD.name
    u'Maryland'

Includes territories too: ::

    >>> us.states.VI.name
    u'Virgin Islands'
    >>> us.states.VI.is_territory
    True
    >>> us.states.MD.is_territory
    False

List of all (actual) states: ::

    >>> us.states.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>,...
    >>> us.states.TERRITORIES
    [<State:American Samoa>, <State:Guam>, <State:Northern Mariana Islands>,...

And the whole shebang, if you want it: ::

    >>> us.states.STATES_AND_TERRITORIES
    [<State:Alabama>, <State:Alaska>, <State:American Samoa>,...

For convenience, `STATES`, `TERRITORIES`, and `STATES_AND_TERRITORIES` can be
accessed directly from the `us` module: ::

    >>> us.states.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>,...
    >>> us.STATES
    [<State:Alabama>, <State:Alaska>, <State:Arizona>, <State:Arkansas>,...

The state lookup method allows matching by FIPS code, abbreviation, and name: ::

    >>> us.states.lookup('24')
    <State:Maryland>
    >>> us.states.lookup('MD')
    <State:Maryland>
    >>> us.states.lookup('md')
    <State:Maryland>
    >>> us.states.lookup('maryland')
    <State:Maryland>

And for those days that you just can't remember how to spell Mississippi,
we've got phonetic name matching too: ::

    >>> us.states.lookup('misisipi')
    <State:Mississippi>


Shapefiles
----------

You want shapefiles too? Gotcha covered.

::

    >>> shpurls = us.states.MD.shapefile_urls()
    >>> for region, url in shpurls.items():
    ...   print "%s: %s" % (region, url)
    ...
    county: http://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_24_county10.zip
    state: http://www2.census.gov/geo/tiger/TIGER2010/STATE/2010/tl_2010_24_state10.zip
    cd: http://www2.census.gov/geo/tiger/TIGER2010/CD/111/tl_2010_24_cd111.zip
    zcta: http://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_24_zcta510.zip
    tract: http://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_24_tract10.zip

The `shapefile_urls()` method on the State object generates shapefile URLs for
the following regions:

* state
* county
* congressional district
* zcta
* census tract

If you know what region you want, you can explicitly request it: ::

    >>> us.states.MD.shapefile_urls('county')
    u'http://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_24_county10.zip'


Mappings
--------

Mappings between various state attributes are a common need. The `mapping()`
method will generate a lookup between two specified fields.

::

    >>> us.states.mapping('fips', 'abbr')
    {u'30': u'MT', u'54': u'WV', u'42': u'PA', u'48': u'TX', u'45': u'SC',...
    >>> us.states.mapping('abbr', 'name')
    {u'WA': u'Washington', u'VA': u'Virginia', u'DE': u'Delaware',...


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
        name_metaphone: MRLNT
        statehood_year: 1788
        time_zones: America/New_York

      shapefiles:
        county: http://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_24_county10.zip
        state: http://www2.census.gov/geo/tiger/TIGER2010/STATE/2010/tl_2010_24_state10.zip
        cd: http://www2.census.gov/geo/tiger/TIGER2010/CD/111/tl_2010_24_cd111.zip
        zcta: http://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_24_zcta510.zip
        tract: http://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_24_tract10.zip


Contributing
------------

Your contributions are welcomed!

State data is stored in *data.db* and pickled using the *build.py* script.
If you modify *data.db*, please be sure to run the build script before
submitting a pull request.

Any changes other than additions to *data.db* should come with appropriate
tests in *test.py*. Also check to see if the *states* CLI script should be
modified to accommodate your change.

Changelog
---------

0.7
~~~~~~

* add time zones, thanks to [Paul Tagliamonte](http://github.com/paultag)
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