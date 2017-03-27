from . import states
from .states import (
    STATES, STATES_CONTIGUOUS, STATES_CONTINENTAL,
    TERRITORIES, STATES_AND_TERRITORIES, OBSOLETE
)
from . import counties
from .counties import COUNTIES
from .unitedstatesofamerica import *

__appname__ = 'us'
__version__ = '0.9.1'

def __link_states_and_counties():
    for c in COUNTIES:
        state = states.lookup(c.state_fips, field='fips')
        c.state = state
        state.counties.append(c)

__link_states_and_counties()
