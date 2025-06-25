from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Type,
)

from horsebox.cli.render import render_error
from horsebox.collectors import CollectorType
from horsebox.collectors.collector_fs import (
    CollectorFSByContent,
    CollectorFSByFilename,
    CollectorFSByLine,
)
from horsebox.collectors.collector_guess import guess_collector
from horsebox.collectors.collector_html import CollectorHtml
from horsebox.collectors.collector_raw import CollectorRaw
from horsebox.collectors.collector_rss import CollectorRSS
from horsebox.model.collector import Collector

__COLLECTORS: Dict[CollectorType, Type[Collector]] = {
    CollectorType.FILENAME: CollectorFSByFilename,
    CollectorType.FILECONTENT: CollectorFSByContent,
    CollectorType.FILELINE: CollectorFSByLine,
    CollectorType.RSS: CollectorRSS,
    CollectorType.RAW: CollectorRaw,
    CollectorType.HTML: CollectorHtml,
}


def get_collector(
    collector_type: CollectorType,
    source: List[str],
    pattern: List[str],
) -> Tuple[Type[Collector], Dict[str, Any]]:
    """
    Get a collector factory.

    Args:
        collector_type (CollectorType): The type of the collector.
        source (List[str]): Locations from which to start indexing.
        pattern (List[str]): The containers to index.

    Returns:
        Tuple[Type[Collector], Dict[str, Any]]:
            - The type of the collector.
            - Some extra arguments to use with the collector.
    """
    collector_type, extra_args = guess_collector(
        collector_type,
        source,
        pattern,
    )
    collector = __COLLECTORS.get(collector_type)
    if not collector:
        render_error('No collector found')

    return (collector, extra_args)
