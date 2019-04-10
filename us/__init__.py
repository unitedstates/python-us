from . import states  # noqa
from .states import (  # noqa
    STATES, STATES_CONTIGUOUS, STATES_CONTINENTAL,
    TERRITORIES, STATES_AND_TERRITORIES, OBSOLETE
)
from .unitedstatesofamerica import *  # noqa

__appname__ = 'us'
# Follow option 5 in this version-number-sourcing documentation
# https://packaging.python.org/guides/single-sourcing-package-version/
import pkg_resources
__version__ = pkg_resources.get_distribution(__appname__).version
