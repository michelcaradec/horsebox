from enum import Enum

class CollectorType(str, Enum):
    """Type of Collector."""

    FILENAME = 'filename'
    FILECONTENT = 'filecontent'
    FILELINE = 'fileline'
    RSS = 'rss'
    RAW = 'raw'
    HTML = 'html'
