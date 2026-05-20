# Changelog

## 4.0.0

* add counties, thanks to [Ray Kiddy](https://github.com/rkiddy)
* add `clean_name()` method and `fallback_func` parameter to `lookup()` to provide customizable matching, thanks to [Max Filenko](https://github.com/mfilenko) and [Charlie Tonneslan](https://github.com/c-tonneslan)
* DC has returned to `STATES_AND_TERRITORIES`, thanks to [Kavi Gupta](https://github.com/kavigupta)
* add `us.states.enumeration()` for dynamic `Enum` construction from `State` attributes
* add `us.__version__` and deprecate `us.version`
* fix `py.typed` location, thanks to [johnw-bluemark](https://github.com/johnw-bluemark)
* add support for Python 3.13 and 3.14
* switch to [uv](https://docs.astral.sh/uv/) for development and packaging
* switch from black and flake8 to [ruff](https://docs.astral.sh/ruff/)
* thanks to maintainer [Pedro Camargo](https://github.com/pedrocamargo)


## 3.2.0

* add support for Python 3.12
* drop support for Python 3.6 and 3.7
* add birthday attribute to unitedstatesofamerica
* upgrade to jellyfish 1.x
* thanks to [Paul Hawk](https://github.com/pauldhawk), [David Gilman](https://github.com/dgilmanAIDENTIFIED), [Sergii Bondarenko](https://github.com/BR0kEN-), and [Pedro Camargo](https://github.com/pedrocamargo)


## 3.1.1

* add support for Python 3.11
* upgrade to jellyfish 0.11.2


## 3.0.0

* upgrade to jellyfish 0.7.2
* drop support for Python 2.7
* add us.states.COMMONWEALTHS list of states that call themselves commonwealths 🎩
* add DC to STATES, STATES_AND_TERRITORIES, STATES_CONTIGUOUS, or STATES_CONTINENTAL when DC_STATEHOOD environment variable is set
* remove `region` parameter from `shapefile_urls()` method
* `mapping()` no longer includes obsolete states
* added type annotations


## 2.0.2

* restore DC in `lookup()` and `mapping()`


## 2.0.1

* fix Python 2.7 tests that ran with Python 3
* revert to jellyfish 0.6.1 to support Python 2.7


## 2.0.0

* add support for Python 3.7 and 3.8
* remove support for Python 3.4 and 3.5
* remove pickled objects and database in favor of pure Python code
* upgrade jellyfish to 0.7.2 to fix metaphone bug
* fixes for IN, KY, ND, and NM timezones
* set AZ timezone to America/Phoenix
* obsolete entries are no longer included in STATES_AND_TERRITORIES
* DC is no longer included in STATES, STATES_AND_TERRITORIES, STATES_CONTIGUOUS, or STATES_CONTINENTAL


## 1.0.0

* full Python 3.6 support
* use pytest


## 0.10.0

* upgrade jellyfish to 0.5.3 to fix metaphone bug

## 0.9.0

* add information on whether a state is contiguous and/or continental,
  thanks to [chebee7i](https://github.com/chebee7i)

## 0.8.0

* add obsolete territories, thanks to [Ben Chartoff](https://github.com/bchartoff)
* fix packaging error, thanks to [Alexander Kulakov](https://github.com/momyc)


## 0.7.1

* upgrade to jellyfish 0.5.1 to fix metaphone case bug

## 0.7

* add time zones, thanks to [Paul Tagliamonte](https://github.com/paultag)
* Python 2.6 and 3.2 compatibility

## 0.6

* add AP-style state abbreviations
* use jellyfish instead of Metaphone package
* update to requests v1.0.4 for tests
* Python 3.3 compatibility

## 0.5

* fix state abbreviation for Nebraska

## 0.4

* add state capitals
* add years of statehood

## 0.3

* add mapping method to generate dicts of arbitrary fields

## 0.2

* add command line script for quick access to state data

## 0.1

* initial release
* state names and abbreviations
* FIPS codes
* `lookup()` method
* shapefile URLs for various regions
