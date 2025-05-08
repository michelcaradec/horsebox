import os
from collections import OrderedDict
from functools import reduce

import tantivy

from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.indexer.index import open_index


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

    searcher: tantivy.Searcher = t_index.searcher()

    size = reduce(
        lambda acc, filename: acc + os.path.getsize(filename),
        os.scandir(index),
        0,
    )

    output = OrderedDict(
        documents=searcher.num_docs,
        segments=searcher.num_segments,
        size=size,
        timestamp=timestamp,
    )
    render(output, format)
