from horsebox.cli.render import (
    Format,
    render_warning,
)
from horsebox.collectors import FILENAME_PIPE
from horsebox.commands import build_index
from horsebox.indexer.index import open_index


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
    t_index, _, build_args = open_index(
        index,
        format,
        skip_expiration_warning=True,
    )
    if not t_index:
        return

    if not build_args:
        render_warning(f'The index {index} has no build arguments')
        return

    build_args.source = [s for s in build_args.source if s != FILENAME_PIPE]
    if not build_args.source:
        render_warning(f'The index {index} has no identifiable data source')
        return

    build_index(
        build_args.source,
        build_args.pattern,
        index,
        build_args.collector_type,
        build_args.collect_as_jsonl,
        False,
        build_args.custom_analyzer,
        format,
    )
