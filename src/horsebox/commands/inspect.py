import os
from collections import OrderedDict
from functools import reduce
from typing import Any

import tantivy

from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.indexer.index import open_index
from horsebox.indexer.metadata import get_build_args


def inspect(
    index: str,
    format: Format,
) -> None:
    """
    Inspect an index.

    Args:
        index (str): The location of the persisted index.
        format (Format): The rendering format to use.
    """
    t_index, timestamp = open_index(index, format)
    if not t_index:
        return

    build_args = get_build_args(index)

    searcher: tantivy.Searcher = t_index.searcher()

    size = reduce(
        lambda acc, filename: acc + os.path.getsize(filename),
        os.scandir(index),
        0,
    )

    output: OrderedDict[str, Any] = OrderedDict(
        documents=searcher.num_docs,
        segments=searcher.num_segments,
        size=size,
        timestamp=timestamp,
    )
    if build_args:
        output['using'] = build_args.collector_type
        output['from'] = build_args.source
        output['pattern'] = build_args.pattern
        output['jsonl'] = build_args.collect_as_jsonl
        
    render(output, format)
