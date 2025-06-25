from typing import List

from horsebox.cli import OPTION_COLLECT_AS_JSONL
from horsebox.cli.render import Format
from horsebox.collectors import CollectorType
from horsebox.collectors.factory import get_collector
from horsebox.commands.inspect import inspect
from horsebox.indexer.index import feed_index
from horsebox.indexer.metadata import IndexBuildArgs


def build(
    source: List[str],
    pattern: List[str],
    index: str,
    collector_type: CollectorType,
    collect_as_jsonl: bool,
    format: Format,
) -> None:
    """
    Build a persistent index.

    Args:
        source (List[str]): Locations from which to start indexing.
        pattern (List[str]): The containers to index.
        index (str): The location where to persist the index.
        collector_type (CollectorType): The collector to use.
        collect_as_jsonl (bool): Whether the JSON documents should be collected as JSON Lines or not.
        format (Format): The rendering format to use.
    """
    collector, extra_args = get_collector(
        collector_type,
        source,
        pattern,
    )

    feed_index(
        collector.create_instance(
            root_path=source,
            pattern=pattern,
            **({OPTION_COLLECT_AS_JSONL: collect_as_jsonl} | extra_args),
        ),
        index,
        IndexBuildArgs(
            source=source,
            pattern=pattern,
            collector_type=collector_type,
            collect_as_jsonl=collect_as_jsonl,
        ),
    )

    inspect(index, format)
