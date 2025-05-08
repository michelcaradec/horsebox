from typing import List
from horsebox.cli.render import Format
from horsebox.collectors import CollectorType
from horsebox.collectors.factory import get_collector
from horsebox.commands.inspect import inspect
from horsebox.indexer.index import feed_index


def build(
    source: List[str],
    pattern: List[str],
    index: str,
    collector_type: CollectorType,
    format: Format,
) -> None:
    """
    Build a persistent index.

    Args:
        source (List[str]): Locations from which to start indexing.
        pattern (List[str]): The containers to index.
        index (str): The location where to persist the index.
        collector_type (CollectorType): The collector to use.
        format (Format): The rendering format to use.
    """
    collector = get_collector(collector_type)

    feed_index(
        collector.create_instance(
            root_path=source,
            pattern=pattern,
        ),
        index,
    )

    inspect(index, format)
