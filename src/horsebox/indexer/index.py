import os
from datetime import datetime
from time import monotonic_ns
from typing import (
    Optional,
    Tuple,
)

import tantivy

from horsebox.cli.config import config
from horsebox.cli.render import (
    Format,
    render_error,
    render_warning,
)
from horsebox.indexer.metadata import (
    get_timestamp,
    set_timestamp,
)
from horsebox.indexer.schema import get_schema
from horsebox.model.collector import Collector
from horsebox.utils.batch import batched


def feed_index(
    collector: Collector,
    index: Optional[str] = None,
) -> Tuple[tantivy.Index, int]:
    """
    Build an index.

    Args:
        collector (Collector): The collector used to collect the documents.
        index (Optional[str]): The path of the index.
            Defaults to None.

    Returns:
        Tuple[tantivy.Index, int]:
            (the index, the build time).
    """
    documents = collector.collect()

    if index:
        os.makedirs(index, exist_ok=True)

    t_index = tantivy.Index(
        get_schema(),
        index,
        reuse=False,
    )

    num_threads = (os.cpu_count() or 0) // 4
    writer: tantivy.IndexWriter = t_index.writer(num_threads=num_threads)

    start = monotonic_ns()

    for batch in batched(documents, config.index_batch_size):
        for document in batch:
            writer.add_document(tantivy.Document(**document))

        writer.commit()

    writer.wait_merging_threads()

    took = monotonic_ns() - start

    if index:
        set_timestamp(index, datetime.now())

    # Index must be reloaded for search to work
    t_index.reload()

    return (t_index, took)


def open_index(
    index: str,
    format: Format,
) -> Tuple[Optional[tantivy.Index], Optional[datetime]]:
    """
    Open an index.

    Args:
        index (str): The path of the index.
        format (Format): The rendering format to use.

    Returns:
        Optional[Tuple[tantivy.Index, Optional[datetime]]]:
            (index object, date of creation of the index).
    """
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}')
        return (None, None)

    t_index = tantivy.Index.open(index)
    timestamp = get_timestamp(index)

    if timestamp and format == Format.TXT:
        # Do not render warning in JSON mode, as it may be part of a processing pipeline
        age = datetime.now() - timestamp
        if age > config.index_expiration:
            render_warning(f'Index age limit reached: {str(age).split(".")[0]}')

    return (t_index, timestamp)
