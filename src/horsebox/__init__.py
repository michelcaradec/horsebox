from importlib.metadata import version

try:
    __version__ = version('horsebox')
except Exception:
    __version__ = ''
