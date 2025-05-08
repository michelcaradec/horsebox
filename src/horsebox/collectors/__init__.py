from enum import Enum

class CollectorType(str, Enum):
    """Type of Collector."""

    FS_BY_FILENAME = 'filename'
    FS_BY_CONTENT = 'filecontent'
    FS_BY_LINE = 'fileline'
    RSS = 'rss'
    RAW = 'raw'
    HTML = 'html'
