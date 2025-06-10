from horsebox.cli.render import (
    Format,
    render_warning,
)
from horsebox.collectors import FILENAME_PIPE
from horsebox.commands import build
from horsebox.indexer.index import open_index
from horsebox.indexer.metadata import get_build_args


def refresh(
    index: str,
    format: Format,
) -> None:
    """
    Refresh an index.

    Args:
        index (str): The location of the persisted index.
        format (Format): The rendering format to use.
    """
    t_index, _ = open_index(
        index,
        format,
        skip_expiration_warning=True,
    )
    if not t_index:
        return

    build_args = get_build_args(index)
    if not build_args:
        render_warning(f'The index {index} has no build arguments')
        return

    build_args.source = list(
        filter(
            lambda s: s != FILENAME_PIPE,
            build_args.source,
        )
    )
    if not build_args.source:
        render_warning(f'The index {index} has no identifiable data source')
        return

    build(
        build_args.source,
        build_args.pattern,
        index,
        build_args.collector_type,
        build_args.collect_as_jsonl,
        format,
    )
