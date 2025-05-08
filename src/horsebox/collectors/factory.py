from typing import (
    Dict,
    Optional,
    Type,
)

from horsebox.collectors import CollectorType
from horsebox.collectors.collector_fs import (
    CollectorFSByContent,
    CollectorFSByFilename,
    CollectorFSByLine,
)
from horsebox.collectors.collector_html import CollectorHtml
from horsebox.collectors.collector_rss import CollectorRSS
from horsebox.collectors.collector_raw import CollectorRaw
from horsebox.model.collector import Collector

__COLLECTORS: Dict[CollectorType, Type[Collector]] = {
    CollectorType.FS_BY_FILENAME: CollectorFSByFilename,
    CollectorType.FS_BY_CONTENT: CollectorFSByContent,
    CollectorType.FS_BY_LINE: CollectorFSByLine,
    CollectorType.RSS: CollectorRSS,
    CollectorType.RAW: CollectorRaw,
    CollectorType.HTML: CollectorHtml,
}


def get_collector(collector_type: CollectorType) -> Type[Collector]:
    """
    Get a collector factory.

    Args:
        collector_type (CollectorType): The type of the collector.
    """
    collector: Optional[Type[Collector]] = __COLLECTORS.get(collector_type)
    if not collector:
        raise ValueError('No collector found')

    return collector
