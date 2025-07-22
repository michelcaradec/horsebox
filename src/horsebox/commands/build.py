from typing import (
    List,
    Optional,
    Union,
)

from horsebox.cli import (
    OPTION_COLLECT_AS_JSONL,
    OPTION_DRY_RUN,
)
from horsebox.cli.render import Format
from horsebox.collectors import CollectorType
from horsebox.collectors.factory import get_collector
from horsebox.collectors.pattern import explode_pattern
from horsebox.commands.inspect import inspect
from horsebox.indexer.analyzer import CustomAnalyzerDef
from horsebox.indexer.analyzer.factory import load_custom_analyzer_def
from horsebox.indexer.build_args import IndexBuildArgs
from horsebox.indexer.index import feed_index


def build_index(
    source: List[str],
    pattern: List[str],
    index: str,
    collector_type: CollectorType,
    collect_as_jsonl: bool,
    dry_run: bool,
    analyzer: Optional[Union[str, CustomAnalyzerDef]],
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
        dry_run (bool): Whether the build of the index should be simulated or done.
        analyzer (Optional[Union[str, CustomAnalyzerDef]]):
            The file containing the definition of the custom analyzer, or the custom analyzer definition.
        format (Format): The rendering format to use.
    """
    source, pattern = explode_pattern(source, pattern)
    collector, extra_args = get_collector(
        collector_type,
        source,
        pattern,
    )

    custom_analyzer: Optional[CustomAnalyzerDef] = None
    if isinstance(analyzer, CustomAnalyzerDef):
        custom_analyzer = analyzer
    elif isinstance(analyzer, str):
        custom_analyzer = load_custom_analyzer_def(analyzer)

    feed_index(
        collector.create_instance(
            root_path=source,
            pattern=pattern,
            **(
                {
                    OPTION_COLLECT_AS_JSONL: collect_as_jsonl,
                    OPTION_DRY_RUN: dry_run,
                }
                | extra_args
            ),
        ),
        index,
        IndexBuildArgs(
            source=source,
            pattern=pattern,
            collector_type=collector_type,
            collect_as_jsonl=collect_as_jsonl,
            custom_analyzer=custom_analyzer,
        ),
        format,
    )

    inspect(index, format)
