from enum import Enum

FILENAME_PIPE = '-'
"""File name used to represent a data source provided by a stream (pipe)."""

class CollectorType(str, Enum):
    """Type of Collector."""

    FILENAME = 'filename'
    FILECONTENT = 'filecontent'
    FILELINE = 'fileline'
    RSS = 'rss'
    RAW = 'raw'
    HTML = 'html'
    GUESS = 'guess'
