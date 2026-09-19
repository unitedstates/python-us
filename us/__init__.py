from .states import (
    STATES,
    STATES_CONTIGUOUS,
    STATES_CONTINENTAL,
    TERRITORIES,
    STATES_AND_TERRITORIES,
    OBSOLETE,
    ASSOCIATED_STATES,
)
from .unitedstatesofamerica import name, abbr, birthday

try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("us")
except Exception:
    __version__ = "unknown"


# Deprecated support for us.version. Remove in the 5.0 release.
def __getattr__(name):
    if name == "version":
        from warnings import warn

        warn("us.version is deprecated, use us.__version__ instead", DeprecationWarning)
        return __version__
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "STATES",
    "STATES_CONTIGUOUS",
    "STATES_CONTINENTAL",
    "TERRITORIES",
    "STATES_AND_TERRITORIES",
    "OBSOLETE",
    "ASSOCIATED_STATES",
    "name",
    "abbr",
    "birthday",
    "__version__",
]
