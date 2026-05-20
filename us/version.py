try:
    from importlib.metadata import version

    __version__ = version("us")
except Exception:
    __version__ = "unknown"
